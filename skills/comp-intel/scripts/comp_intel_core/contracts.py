"""Dependency-free validation for the public workflow contracts."""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from typing import Any, Iterable


ID_RE = re.compile(r"^[a-z][a-z0-9-]{1,62}$")
STAGES = {
    "initialized", "collecting", "needs_attention", "evidence_review",
    "synthesizing", "draft_review", "apply_ready", "complete", "blocked", "failed",
}
EVIDENCE_CLASSIFICATIONS = {"verified", "reported", "inference", "missing", "rejected"}
CONFIDENCE_LEVELS = {"high", "medium", "low", "unknown"}
SENSITIVITIES = {"public", "internal", "confidential", "restricted"}
CLAIM_TYPES = {"observation", "attributed_report", "inference", "recommendation", "unknown"}
CATEGORIES = {"product", "positioning", "pricing", "go_to_market", "customer", "talent", "operations", "other"}


def _required(value: dict[str, Any], fields: Iterable[str], label: str, errors: list[str]) -> None:
    for field in fields:
        if field not in value:
            errors.append(f"{label}.{field}: required")


def _id(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        errors.append(f"{label}: must match {ID_RE.pattern}")


def _timestamp(value: Any, label: str, errors: list[str], *, nullable: bool = False) -> None:
    if value is None and nullable:
        return
    if not isinstance(value, str):
        errors.append(f"{label}: must be an ISO-8601 timestamp")
        return
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError
    except ValueError:
        errors.append(f"{label}: must be an ISO-8601 timestamp with timezone")


def parse_day(value: str, label: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label}: must be YYYY-MM-DD") from exc


def utc_timestamp(value: datetime | None = None) -> str:
    current = value or datetime.now(timezone.utc)
    return current.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_config(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["config: must be an object"]
    _required(value, ("schema_version", "markets", "reviewers"), "config", errors)
    if value.get("schema_version") != 1:
        errors.append("config.schema_version: must be 1")
    markets = value.get("markets")
    if not isinstance(markets, dict) or not markets:
        errors.append("config.markets: must be a non-empty object")
    else:
        for market_id, path in markets.items():
            _id(market_id, f"config.markets.{market_id}", errors)
            if not isinstance(path, str) or not path or path.startswith("/") or ".." in path.split("/"):
                errors.append(f"config.markets.{market_id}: must be a safe relative path")
    reviewers = value.get("reviewers")
    if not isinstance(reviewers, dict):
        errors.append("config.reviewers: must be an object")
    else:
        for role in ("evidence_reviewer", "apply_approver"):
            identities = reviewers.get(role)
            if not isinstance(identities, list) or not identities or not all(isinstance(item, str) and item for item in identities):
                errors.append(f"config.reviewers.{role}: must be a non-empty string array")
    return errors


def validate_market_pack(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["market_pack: must be an object"]
    _required(value, ("schema_version", "market_id", "display_name", "version", "competitors", "sources"), "market_pack", errors)
    if value.get("schema_version") != 1:
        errors.append("market_pack.schema_version: must be 1")
    _id(value.get("market_id"), "market_pack.market_id", errors)
    competitors = value.get("competitors")
    seen: set[str] = set()
    if not isinstance(competitors, list) or not competitors:
        errors.append("market_pack.competitors: must be a non-empty array")
    else:
        for index, competitor in enumerate(competitors):
            label = f"market_pack.competitors[{index}]"
            if not isinstance(competitor, dict):
                errors.append(f"{label}: must be an object")
                continue
            _required(competitor, ("competitor_id", "display_name", "status"), label, errors)
            competitor_id = competitor.get("competitor_id")
            _id(competitor_id, f"{label}.competitor_id", errors)
            if competitor_id in seen:
                errors.append(f"{label}.competitor_id: duplicate {competitor_id}")
            seen.add(competitor_id)
            if competitor.get("status") not in {"active", "monitor", "dormant"}:
                errors.append(f"{label}.status: invalid")
    sources = value.get("sources")
    source_ids: set[str] = set()
    if not isinstance(sources, list) or not sources:
        errors.append("market_pack.sources: must be a non-empty array")
    else:
        for index, source in enumerate(sources):
            label = f"market_pack.sources[{index}]"
            if not isinstance(source, dict):
                errors.append(f"{label}: must be an object")
                continue
            _required(source, ("source_id", "adapter_id", "required", "enabled", "config"), label, errors)
            source_id = source.get("source_id")
            _id(source_id, f"{label}.source_id", errors)
            if source_id in source_ids:
                errors.append(f"{label}.source_id: duplicate {source_id}")
            source_ids.add(source_id)
            if source.get("adapter_id") not in {"synthetic", "local_files", "web", "github", "slack"}:
                errors.append(f"{label}.adapter_id: unknown adapter")
            if not isinstance(source.get("required"), bool) or not isinstance(source.get("enabled"), bool):
                errors.append(f"{label}: required and enabled must be booleans")
            if not isinstance(source.get("config"), dict):
                errors.append(f"{label}.config: must be an object")
    return errors


def validate_candidate(value: Any, label: str = "candidate") -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return [f"{label}: must be an object"]
    _required(value, ("native_id", "canonical_uri", "title", "summary", "source_type", "competitor_id"), label, errors)
    for field in ("native_id", "canonical_uri", "title", "summary", "source_type", "competitor_id"):
        if field in value and (not isinstance(value[field], str) or not value[field].strip()):
            errors.append(f"{label}.{field}: must be a non-empty string")
    for field in ("published_at", "modified_at", "event_at"):
        if field in value:
            _timestamp(value[field], f"{label}.{field}", errors, nullable=True)
    if "category" in value and value["category"] not in CATEGORIES:
        errors.append(f"{label}.category: invalid")
    if "classification" in value and value["classification"] not in EVIDENCE_CLASSIFICATIONS:
        errors.append(f"{label}.classification: invalid")
    if "confidence" in value and value["confidence"] not in CONFIDENCE_LEVELS:
        errors.append(f"{label}.confidence: invalid")
    if "sensitivity" in value and value["sensitivity"] not in SENSITIVITIES:
        errors.append(f"{label}.sensitivity: invalid")
    return errors


def validate_evidence(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["evidence: must be an object"]
    _required(value, ("schema_version", "evidence_id", "market_id", "competitor_id", "source", "content", "classification", "confidence", "category", "sensitivity", "relationships"), "evidence", errors)
    if value.get("schema_version") != 1:
        errors.append("evidence.schema_version: must be 1")
    if value.get("classification") not in EVIDENCE_CLASSIFICATIONS:
        errors.append("evidence.classification: invalid")
    if value.get("confidence") not in CONFIDENCE_LEVELS:
        errors.append("evidence.confidence: invalid")
    if value.get("category") not in CATEGORIES:
        errors.append("evidence.category: invalid")
    if value.get("sensitivity") not in SENSITIVITIES:
        errors.append("evidence.sensitivity: invalid")
    source = value.get("source")
    if not isinstance(source, dict):
        errors.append("evidence.source: must be an object")
    else:
        _required(source, ("adapter_id", "source_id", "source_type", "canonical_uri", "native_id", "observed_at"), "evidence.source", errors)
        _timestamp(source.get("observed_at"), "evidence.source.observed_at", errors)
        _timestamp(source.get("published_at"), "evidence.source.published_at", errors, nullable=True)
    return errors


def validate_approval(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["approval: must be an object"]
    _required(value, ("schema_version", "approval_id", "run_id", "stage", "decision", "artifact", "approver", "decided_at"), "approval", errors)
    if value.get("schema_version") != 1:
        errors.append("approval.schema_version: must be 1")
    if value.get("stage") not in {"evidence_review", "draft_review"}:
        errors.append("approval.stage: invalid")
    if value.get("decision") not in {"approved", "rejected"}:
        errors.append("approval.decision: invalid")
    artifact = value.get("artifact")
    if not isinstance(artifact, dict):
        errors.append("approval.artifact: must be an object")
    else:
        _required(artifact, ("role", "path", "sha256"), "approval.artifact", errors)
    approver = value.get("approver")
    if not isinstance(approver, dict):
        errors.append("approval.approver: must be an object")
    else:
        _required(approver, ("id", "role"), "approval.approver", errors)
    _timestamp(value.get("decided_at"), "approval.decided_at", errors)
    return errors


def validate_claim(value: Any, label: str = "claim") -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return [f"{label}: must be an object"]
    _required(value, ("schema_version", "claim_id", "market_id", "competitor_id", "claim_type", "text", "evidence_ids", "confidence", "sensitivity", "limitations"), label, errors)
    if value.get("schema_version") != 1:
        errors.append(f"{label}.schema_version: must be 1")
    if not isinstance(value.get("claim_id"), str) or not value["claim_id"].strip():
        errors.append(f"{label}.claim_id: must be a non-empty string")
    if not isinstance(value.get("text"), str) or not value["text"].strip():
        errors.append(f"{label}.text: must be a non-empty string")
    if value.get("claim_type") not in CLAIM_TYPES:
        errors.append(f"{label}.claim_type: invalid")
    if value.get("confidence") not in CONFIDENCE_LEVELS:
        errors.append(f"{label}.confidence: invalid")
    if value.get("sensitivity") not in SENSITIVITIES:
        errors.append(f"{label}.sensitivity: invalid")
    if not isinstance(value.get("evidence_ids"), list):
        errors.append(f"{label}.evidence_ids: must be an array")
    elif not all(isinstance(item, str) and item for item in value["evidence_ids"]):
        errors.append(f"{label}.evidence_ids: entries must be non-empty strings")
    return errors


def validate_run(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["run: must be an object"]
    _required(value, ("schema_version", "run_id", "market_id", "controller_version", "runtime", "window", "stage", "artifacts", "transitions", "warnings", "errors"), "run", errors)
    if value.get("schema_version") != 2:
        errors.append("run.schema_version: must be 2")
    if value.get("stage") not in STAGES:
        errors.append("run.stage: invalid")
    window = value.get("window")
    if not isinstance(window, dict):
        errors.append("run.window: must be an object")
    else:
        try:
            start = parse_day(window.get("from"), "run.window.from")
            end = parse_day(window.get("to"), "run.window.to")
            if start >= end:
                errors.append("run.window: from must be before exclusive to")
        except ValueError as exc:
            errors.append(str(exc))
    return errors


def validate_registry(value: Any, market_id: str | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["registry: must be an object"]
    _required(value, ("schema_version", "market_id", "competitors", "trackers", "applied_runs", "history"), "registry", errors)
    if value.get("schema_version") != 1:
        errors.append("registry.schema_version: must be 1")
    if market_id is not None and value.get("market_id") != market_id:
        errors.append("registry.market_id: does not match selected market")
    if not isinstance(value.get("competitors"), dict) or not value.get("competitors"):
        errors.append("registry.competitors: must be a non-empty object")
    trackers = value.get("trackers")
    if not isinstance(trackers, dict):
        errors.append("registry.trackers: must be an object")
    else:
        for tracker in ("battlecard_gaps", "narrative_changes", "win_loss_signals"):
            if not isinstance(trackers.get(tracker), list):
                errors.append(f"registry.trackers.{tracker}: must be an array")
    if not isinstance(value.get("applied_runs"), list):
        errors.append("registry.applied_runs: must be an array")
    if not isinstance(value.get("history"), list):
        errors.append("registry.history: must be an array")
    return errors
