"""Normalize raw adapter candidates into attributable evidence records."""

from __future__ import annotations

import hashlib
import re
from datetime import date, datetime
from typing import Any

from .contracts import CATEGORIES, CONFIDENCE_LEVELS, EVIDENCE_CLASSIFICATIONS, SENSITIVITIES, validate_evidence
from .io_utils import digest_value


TOKEN_RE = re.compile(r"[a-z0-9]+")
NEAR_DUPLICATE_ALGORITHM = "jaccard-title-summary-v1"
NEAR_DUPLICATE_THRESHOLD = 0.82


def normalize_candidates(
    candidates: list[dict[str, Any]],
    *,
    market: dict[str, Any],
    window_from: date,
    window_to: date,
    observed_at: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    competitor_ids = {item["competitor_id"] for item in market["competitors"]}
    evidence_by_id: dict[str, dict[str, Any]] = {}
    rejected: list[dict[str, str]] = []
    exact_duplicates: list[dict[str, str]] = []
    out_of_window: list[dict[str, str]] = []

    for index, candidate in enumerate(candidates):
        competitor_id = candidate.get("competitor_id")
        if competitor_id not in competitor_ids:
            rejected.append({"candidate": str(index), "reason": f"unknown competitor_id {competitor_id}"})
            continue
        included, date_reason = _in_window(candidate, window_from, window_to)
        if not included:
            out_of_window.append({"native_id": str(candidate.get("native_id")), "reason": date_reason})
            continue
        prepared = dict(candidate)
        if date_reason.startswith("no event or publication date"):
            prepared["limitations"] = list(prepared.get("limitations", [])) + [
                "Event and publication dates are unavailable; retained by market policy."
            ]
        record = _record(prepared, market["market_id"], observed_at)
        errors = validate_evidence(record)
        if errors:
            rejected.append({"candidate": str(candidate.get("native_id")), "reason": "; ".join(errors)})
            continue
        existing = evidence_by_id.get(record["evidence_id"])
        if existing is not None:
            existing["collection"]["observations"] += 1
            exact_duplicates.append({"kept": record["evidence_id"], "duplicate_native_id": record["source"]["native_id"]})
            continue
        evidence_by_id[record["evidence_id"]] = record

    records = sorted(evidence_by_id.values(), key=lambda item: item["evidence_id"])
    _link_revisions(records)
    _link_events(records)
    near_duplicates = _near_duplicates(records)
    coverage = {
        "candidates_seen": len(candidates),
        "accepted_evidence": len(records),
        "rejected": rejected,
        "out_of_window": out_of_window,
        "exact_duplicates": exact_duplicates,
        "near_duplicates": near_duplicates,
        "near_duplicate_policy": {
            "algorithm": NEAR_DUPLICATE_ALGORITHM,
            "version": "1",
            "threshold": NEAR_DUPLICATE_THRESHOLD,
            "auto_delete": False,
        },
    }
    return records, coverage


def semantic_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return the stable projection used by evidence-manifest hashing."""
    projected = {key: value for key, value in record.items() if key != "collection"}
    source = dict(projected["source"])
    source.pop("observed_at", None)
    projected["source"] = source
    return projected


def _record(candidate: dict[str, Any], market_id: str, observed_at: str) -> dict[str, Any]:
    summary = candidate["summary"].strip()
    classification = candidate.get("classification", "reported")
    confidence = candidate.get("confidence", "medium")
    limitations = list(candidate.get("limitations", []))
    source_type = candidate["source_type"]
    if source_type in {"search_snippet", "unattributed_summary"}:
        classification = "reported" if classification == "verified" else classification
        confidence = "low"
        limitations.append("Discovery text was not verified against an accessible primary page.")
    if classification not in EVIDENCE_CLASSIFICATIONS:
        classification = "reported"
    if confidence not in CONFIDENCE_LEVELS:
        confidence = "unknown"
    sensitivity = candidate.get("sensitivity", "public")
    if sensitivity not in SENSITIVITIES:
        sensitivity = "restricted"
    category = candidate.get("category", "other")
    if category not in CATEGORIES:
        category = "other"
    version = str(candidate.get("source_version") or candidate.get("modified_at") or digest_value({"title": candidate["title"], "summary": summary}))
    identity = {
        "adapter_id": candidate["_adapter_id"],
        "source_id": candidate["_source_id"],
        "native_id": candidate["native_id"],
        "source_version": version,
    }
    evidence_id = "ev_" + hashlib.sha256(str(sorted(identity.items())).encode("utf-8")).hexdigest()[:20]
    return {
        "schema_version": 1,
        "evidence_id": evidence_id,
        "market_id": market_id,
        "competitor_id": candidate["competitor_id"],
        "source": {
            "adapter_id": candidate["_adapter_id"],
            "adapter_version": candidate["_adapter_version"],
            "source_id": candidate["_source_id"],
            "source_type": source_type,
            "canonical_uri": candidate["canonical_uri"],
            "native_id": candidate["native_id"],
            "source_version": version,
            "title": candidate["title"],
            "published_at": candidate.get("published_at"),
            "modified_at": candidate.get("modified_at"),
            "event_at": candidate.get("event_at"),
            "observed_at": observed_at,
            "query_id": candidate.get("_query_id"),
        },
        "content": {
            "summary": summary,
            "excerpt": candidate.get("excerpt"),
            "content_digest": digest_value({"title": candidate["title"], "summary": summary, "excerpt": candidate.get("excerpt")}),
        },
        "classification": classification,
        "confidence": confidence,
        "category": category,
        "signal_type": candidate.get("signal_type", "other"),
        "sensitivity": sensitivity,
        "public_safe": bool(candidate.get("public_safe", sensitivity == "public")),
        "limitations": sorted(set(limitations)),
        "relationships": {"corroborates": [], "conflicts_with": [], "supersedes": []},
        "collection": {"observations": 1, "metadata": candidate.get("metadata", {})},
        "event_key": candidate.get("event_key"),
        "conflict_key": candidate.get("conflict_key"),
    }


def _candidate_day(candidate: dict[str, Any]) -> tuple[date | None, str]:
    for field in ("event_at", "published_at"):
        raw = candidate.get(field)
        if raw:
            return datetime.fromisoformat(raw.replace("Z", "+00:00")).date(), field
    return None, "unknown"


def _in_window(candidate: dict[str, Any], start: date, end: date) -> tuple[bool, str]:
    candidate_day, field = _candidate_day(candidate)
    if candidate_day is None:
        return True, "no event or publication date; retained with explicit limitation"
    if start <= candidate_day < end:
        return True, f"{field} is in range"
    return False, f"{field} {candidate_day.isoformat()} outside [{start.isoformat()}, {end.isoformat()})"


def _link_revisions(records: list[dict[str, Any]]) -> None:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for record in records:
        source = record["source"]
        key = (source["adapter_id"], source["source_id"], source["native_id"])
        groups.setdefault(key, []).append(record)
    for group in groups.values():
        if len(group) < 2:
            continue
        ordered = sorted(group, key=lambda item: (item["source"].get("modified_at") or item["source"].get("published_at") or "", item["evidence_id"]))
        for previous, current in zip(ordered, ordered[1:]):
            current["relationships"]["supersedes"].append(previous["evidence_id"])


def _link_events(records: list[dict[str, Any]]) -> None:
    corroboration: dict[str, list[dict[str, Any]]] = {}
    conflicts: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        if record.get("event_key"):
            corroboration.setdefault(record["event_key"], []).append(record)
        if record.get("conflict_key"):
            conflicts.setdefault(record["conflict_key"], []).append(record)
    for group in corroboration.values():
        source_references = {record["source"]["canonical_uri"] for record in group}
        if len(source_references) < 2:
            continue
        for record in group:
            record["relationships"]["corroborates"] = sorted(item["evidence_id"] for item in group if item is not record)
    for group in conflicts.values():
        summaries = {record["content"]["summary"] for record in group}
        if len(summaries) < 2:
            continue
        for record in group:
            record["relationships"]["conflicts_with"] = sorted(item["evidence_id"] for item in group if item is not record)


def _tokens(record: dict[str, Any]) -> set[str]:
    text = f"{record['source']['title']} {record['content']['summary']}".lower()
    return set(TOKEN_RE.findall(text))


def _near_duplicates(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for index, left in enumerate(records):
        left_tokens = _tokens(left)
        for right in records[index + 1:]:
            if left["competitor_id"] != right["competitor_id"]:
                continue
            right_tokens = _tokens(right)
            union = left_tokens | right_tokens
            score = len(left_tokens & right_tokens) / len(union) if union else 1.0
            if score < 0.5:
                continue
            results.append({
                "left": left["evidence_id"],
                "right": right["evidence_id"],
                "algorithm": NEAR_DUPLICATE_ALGORITHM,
                "version": "1",
                "normalized_fields": ["source.title", "content.summary"],
                "score": round(score, 4),
                "threshold": NEAR_DUPLICATE_THRESHOLD,
                "decision": "candidate_near_duplicate" if score >= NEAR_DUPLICATE_THRESHOLD else "distinct",
            })
    return results
