"""Governed state machine for the offline competitive-intelligence workflow."""

from __future__ import annotations

import copy
import os
import secrets
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .adapters import adapter_for
from .contracts import (
    parse_day,
    utc_timestamp,
    validate_approval,
    validate_claim,
    validate_config,
    validate_market_pack,
    validate_registry,
    validate_run,
)
from .io_utils import (
    append_jsonl,
    atomic_write_bytes,
    atomic_write_json,
    atomic_write_jsonl,
    canonical_bytes,
    digest_bytes,
    digest_value,
    ensure_within,
    parse_jsonl,
    read_json,
)
from .normalize import normalize_candidates, semantic_record


CONTROLLER_VERSION = "0.1.0"
PACKAGE_ROOT = Path(__file__).resolve().parents[2]
EXIT_CODES = {
    "usage/config": 2,
    "capability": 3,
    "collection": 4,
    "validation": 5,
    "approval": 6,
    "conflict": 7,
    "synthesis": 8,
    "write": 9,
    "privacy": 10,
}
SENSITIVITY_RANK = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}


class WorkflowError(RuntimeError):
    def __init__(
        self,
        category: str,
        message: str,
        *,
        run_id: str | None = None,
        stage: str | None = None,
        next_actions: list[str] | None = None,
    ) -> None:
        super().__init__(message)
        self.category = category
        self.code = EXIT_CODES[category]
        self.run_id = run_id
        self.stage = stage
        self.next_actions = next_actions or []

    def result(self) -> dict[str, Any]:
        return {
            "status": "error",
            "code": self.code,
            "category": self.category,
            "message": str(self),
            "run_id": self.run_id,
            "stage": self.stage,
            "warnings": [],
            "next_actions": self.next_actions,
        }


class CompIntelController:
    """Library boundary shared by the Desktop skill and future runtime adapters."""

    def __init__(self, data_root: Path | str) -> None:
        candidate = Path(data_root).expanduser()
        if not candidate.is_absolute():
            candidate = Path.cwd() / candidate
        self.data_root = candidate.resolve(strict=False)

    def init(self) -> dict[str, Any]:
        if self.data_root.exists() and any(self.data_root.iterdir()):
            raise WorkflowError(
                "usage/config",
                f"data root is not empty: {self.data_root}",
                next_actions=["Choose a new empty data root.", "Run validate against the existing root."],
            )
        self.data_root.mkdir(parents=True, exist_ok=True)
        for relative in ("markets", "fixtures", "local", "state/markets", "runs", "outputs/reports"):
            (self.data_root / relative).mkdir(parents=True, exist_ok=True)

        config = read_json(PACKAGE_ROOT / "assets/config-template.yaml")
        market = read_json(PACKAGE_ROOT / "examples/fixtures/synthetic-market-pack.json")
        fixture = read_json(PACKAGE_ROOT / "examples/fixtures/synthetic-source.json")
        local_fixture = read_json(PACKAGE_ROOT / "examples/fixtures/local-source.json")
        mapping = read_json(PACKAGE_ROOT / "assets/mapping-template.yaml")
        errors = validate_config(config) + validate_market_pack(market)
        if errors:
            raise WorkflowError("validation", "bundled templates are invalid: " + "; ".join(errors))
        atomic_write_json(self.data_root / "config.json", config)
        atomic_write_json(self.data_root / "markets/synthetic-devtools.json", market)
        atomic_write_json(self.data_root / "fixtures/synthetic-source.json", fixture)
        atomic_write_json(self.data_root / "local/local-source.json", local_fixture)
        atomic_write_json(self.data_root / "mapping.json", mapping)
        registry = self._empty_registry(market)
        atomic_write_json(self._registry_path(market["market_id"]), registry)
        return self._success(
            "initialized adopter-owned competitive-intelligence data",
            stage="initialized",
            extra={
                "data_root": str(self.data_root),
                "market_id": market["market_id"],
                "mapping_checklist": "mapping.json",
            },
            next_actions=["Run doctor for synthetic-devtools.", "Replace every unmapped item before configuring live organization sources."],
        )

    def doctor(self, market_id: str) -> dict[str, Any]:
        _, market = self._load_market(market_id)
        capabilities: list[dict[str, Any]] = []
        blocking: list[str] = []
        warnings: list[str] = []
        for source in market["sources"]:
            if not source["enabled"]:
                capability = {
                    "source_id": source["source_id"],
                    "adapter_id": source["adapter_id"],
                    "state": "disabled",
                    "message": "disabled by market pack",
                    "required": source["required"],
                }
            else:
                adapter = adapter_for(source["adapter_id"])
                if adapter is None:
                    capability = {
                        "source_id": source["source_id"],
                        "adapter_id": source["adapter_id"],
                        "state": "missing",
                        "message": "adapter is not included in this foundation slice",
                        "required": source["required"],
                    }
                else:
                    capability = adapter.probe(source, self.data_root).as_dict()
                    capability["required"] = source["required"]
            capabilities.append(capability)
            if capability["state"] not in {"available", "disabled"}:
                message = f"{source['source_id']}: {capability['message']}"
                if source["required"]:
                    blocking.append(message)
                else:
                    warnings.append(message)
        return self._success(
            "capability preflight complete",
            stage=None,
            warnings=warnings,
            extra={"market_id": market_id, "capabilities": capabilities, "blocking": blocking},
            next_actions=["Resolve missing required capabilities before collection."] if blocking else ["Collect an absolute date window."],
        )

    def collect(
        self,
        market_id: str,
        window_from: str,
        window_to: str,
        *,
        observed_at: str | None = None,
        run_id: str | None = None,
        runtime_mode: str = "interactive",
    ) -> dict[str, Any]:
        _, market = self._load_market(market_id)
        start = parse_day(window_from, "from")
        end = parse_day(window_to, "to")
        if start >= end:
            raise WorkflowError("usage/config", "from must be before exclusive to")
        observed = observed_at or utc_timestamp()
        _parse_timestamp(observed, "observed_at")
        if runtime_mode not in {"interactive", "scheduled"}:
            raise WorkflowError("usage/config", "runtime_mode must be interactive or scheduled")
        preflight = self.doctor(market_id)
        if preflight["blocking"]:
            raise WorkflowError(
                "capability",
                "required capability is unavailable: " + "; ".join(preflight["blocking"]),
                next_actions=["Run doctor after correcting the required source mapping."],
            )

        resolved_run_id = run_id or self._new_run_id()
        if not resolved_run_id.startswith("run_") or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for char in resolved_run_id):
            raise WorkflowError("usage/config", "run_id must begin with run_ and contain only letters, digits, underscore, or hyphen")
        run_dir = self._run_dir(resolved_run_id)
        if run_dir.exists():
            raise WorkflowError("conflict", f"run already exists: {resolved_run_id}", run_id=resolved_run_id)
        run_dir.mkdir(parents=True)
        for relative in ("collection/raw", "approvals", "synthesis", "reviews"):
            (run_dir / relative).mkdir(parents=True, exist_ok=True)
        run = {
            "schema_version": 2,
            "run_id": resolved_run_id,
            "market_id": market_id,
            "market_pack_version": market["version"],
            "controller_version": CONTROLLER_VERSION,
            "runtime": {"host": "codex", "mode": runtime_mode, "model": None},
            "window": {"from": window_from, "to": window_to, "semantics": "from inclusive; to exclusive"},
            "stage": "initialized",
            "capabilities": {"manifest": "capabilities.json"},
            "artifacts": {},
            "transitions": [],
            "warnings": list(preflight["warnings"]),
            "errors": [],
            "created_at": observed,
            "updated_at": observed,
        }
        atomic_write_json(run_dir / "capabilities.json", preflight["capabilities"])
        atomic_write_json(run_dir / "run.json", run)
        self._transition(run, "collecting", observed)
        self._persist_run(run)

        candidates, source_coverage, collection_warnings, collection_errors = self._collect_sources(market)
        run["warnings"].extend(collection_warnings)
        run["errors"].extend(collection_errors)
        required_failure = bool(collection_errors)
        atomic_write_jsonl(run_dir / "collection/raw/candidates.jsonl", candidates)

        evidence, normalization = normalize_candidates(
            candidates,
            market=market,
            window_from=start,
            window_to=end,
            observed_at=observed,
        )
        atomic_write_jsonl(run_dir / "collection/evidence.jsonl", evidence)
        evidence_core = {
            "schema_version": 1,
            "market_id": market_id,
            "window": {"from": window_from, "to": window_to, "semantics": "from inclusive; to exclusive"},
            "evidence_ids": [record["evidence_id"] for record in evidence],
            "record_digests": {record["evidence_id"]: digest_value(semantic_record(record)) for record in evidence},
        }
        evidence_digest = digest_value(evidence_core)
        manifest = dict(evidence_core)
        manifest.update({"record_count": len(evidence), "evidence_digest": evidence_digest})
        manifest_path = run_dir / "collection/evidence-manifest.json"
        atomic_write_json(manifest_path, manifest)
        competitor_coverage = self._competitor_coverage(market, evidence)
        for item in competitor_coverage:
            if item["status"] == "active" and item["evidence_count"] == 0:
                run["warnings"].append(
                    f"active competitor {item['competitor_id']} has no accepted evidence in this window"
                )
        coverage = {
            "schema_version": 1,
            "run_id": resolved_run_id,
            "market_id": market_id,
            "sources": source_coverage,
            "competitors": competitor_coverage,
            "normalization": normalization,
            "limitations": sorted(set(run["warnings"])),
        }
        atomic_write_json(run_dir / "collection/coverage.json", coverage)
        run["artifacts"].update({
            "evidence": self._artifact(run_dir, "collection/evidence.jsonl"),
            "evidence_manifest": self._artifact(run_dir, "collection/evidence-manifest.json"),
            "coverage": self._artifact(run_dir, "collection/coverage.json"),
        })
        if required_failure:
            self._transition(run, "failed", observed)
            self._persist_run(run)
            raise WorkflowError(
                "collection",
                "required source collection failed; partial evidence retained",
                run_id=resolved_run_id,
                stage="failed",
                next_actions=["Inspect coverage and create a recorded retry or new run."],
            )
        self._transition(run, "evidence_review", observed)
        self._persist_run(run)
        review = self._render_evidence_review(run, manifest, coverage, evidence)
        atomic_write_bytes(run_dir / "reviews/evidence-review.md", review.encode("utf-8"))
        atomic_write_json(run_dir / "reviews/evidence-approval-template.json", self._approval_template(run, "evidence"))
        return self._success(
            "collection complete; workflow stopped at evidence review",
            run_id=resolved_run_id,
            stage="evidence_review",
            warnings=run["warnings"],
            extra={
                "evidence_digest": evidence_digest,
                "evidence_count": len(evidence),
                "review_path": str(run_dir / "reviews/evidence-review.md"),
                "approval_template": str(run_dir / "reviews/evidence-approval-template.json"),
            },
            next_actions=["Review coverage and evidence.", "Create an approval record outside the run and install it with approve-evidence."],
        )

    def _collect_sources(
        self, market: dict[str, Any]
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str], list[str]]:
        candidates: list[dict[str, Any]] = []
        source_coverage: list[dict[str, Any]] = []
        warnings: list[str] = []
        errors: list[str] = []
        for source in market["sources"]:
            if not source["enabled"]:
                source_coverage.append({"source_id": source["source_id"], "status": "disabled", "required": source["required"]})
                continue
            adapter = adapter_for(source["adapter_id"])
            if adapter is None:
                source_coverage.append({"source_id": source["source_id"], "status": "unavailable", "required": source["required"]})
                continue
            result = adapter.collect(source, self.data_root)
            candidates.extend(result.candidates)
            status = "complete" if result.complete else "partial"
            source_coverage.append({
                "source_id": source["source_id"],
                "adapter_id": source["adapter_id"],
                "required": source["required"],
                "status": status,
                "candidates": len(result.candidates),
                "checkpoint": result.checkpoint,
                "warnings": result.warnings,
                "errors": result.errors,
            })
            warnings.extend(f"{source['source_id']}: {warning}" for warning in result.warnings)
            if not result.complete:
                message = f"{source['source_id']}: " + "; ".join(result.errors)
                if source["required"]:
                    errors.append(message)
                else:
                    warnings.append(message)
        return candidates, source_coverage, warnings, errors

    def _competitor_coverage(
        self, market: dict[str, Any], evidence: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        return [
            {
                "competitor_id": competitor["competitor_id"],
                "status": competitor["status"],
                "evidence_count": sum(
                    record["competitor_id"] == competitor["competitor_id"] for record in evidence
                ),
                "source_types": sorted({
                    record["source"]["source_type"]
                    for record in evidence
                    if record["competitor_id"] == competitor["competitor_id"]
                }),
            }
            for competitor in market["competitors"]
        ]

    def status(self, run_id: str) -> dict[str, Any]:
        run = self._load_run(run_id)
        integrity = self._artifact_errors(run)
        return self._success(
            "run status loaded" if not integrity else "run status loaded with integrity failures",
            run_id=run_id,
            stage=run["stage"],
            warnings=run["warnings"] + integrity,
            extra={"run": run, "integrity": "valid" if not integrity else "invalid"},
            next_actions=self._next_actions(run),
        )

    def install_evidence_approval(
        self, run_id: str, approval_file: Path | str, *, invocation_mode: str = "interactive"
    ) -> dict[str, Any]:
        self._require_interactive(invocation_mode, "install approvals")
        run = self._load_run(run_id)
        self._require_stage(run, "evidence_review")
        approval = read_json(Path(approval_file).expanduser().resolve(strict=True))
        self._validate_approval_record(run, approval, role="evidence_manifest", authorized_role="evidence_reviewer")
        target = self._run_dir(run_id) / "approvals/evidence.json"
        atomic_write_json(target, approval)
        self._audit(run, "approval_installed", {"approval_id": approval["approval_id"], "role": "evidence_manifest"})
        return self._success(
            "evidence approval installed",
            run_id=run_id,
            stage=run["stage"],
            extra={"approval_id": approval["approval_id"]},
            next_actions=["Submit a schema-valid synthesis package created only from this approved evidence set."],
        )

    def submit_synthesis(
        self, run_id: str, package_file: Path | str, *, invocation_mode: str = "interactive"
    ) -> dict[str, Any]:
        self._require_interactive(invocation_mode, "synthesize")
        run = self._load_run(run_id)
        self._require_stage(run, "evidence_review")
        self._require_valid_artifacts(run)
        self._require_installed_approval(run, "evidence")
        package = read_json(Path(package_file).expanduser().resolve(strict=True))
        evidence = parse_jsonl(self._run_dir(run_id) / "collection/evidence.jsonl")
        manifest = read_json(self._run_dir(run_id) / "collection/evidence-manifest.json")
        registry = self._load_registry(run["market_id"])
        errors = self._validate_synthesis_package(package, run, evidence, manifest, registry)
        if errors:
            raise WorkflowError(
                "synthesis",
                "synthesis package is invalid: " + "; ".join(errors),
                run_id=run_id,
                stage=run["stage"],
                next_actions=["Revise the package without changing the approved evidence set."],
            )
        timestamp = utc_timestamp()
        self._transition(run, "synthesizing", timestamp)
        self._persist_run(run)
        run_dir = self._run_dir(run_id)
        atomic_write_json(run_dir / "synthesis/synthesis-package.json", package)
        atomic_write_jsonl(run_dir / "synthesis/claims.jsonl", package["claims"])
        atomic_write_json(run_dir / "synthesis/proposed-change-set.json", package["proposed_change_set"])
        report = self._render_report(run, manifest, read_json(run_dir / "collection/coverage.json"), evidence, package)
        atomic_write_bytes(run_dir / "synthesis/report-draft.md", report.encode("utf-8"))
        run["artifacts"].update({
            "synthesis_package": self._artifact(run_dir, "synthesis/synthesis-package.json"),
            "claims": self._artifact(run_dir, "synthesis/claims.jsonl"),
            "change_set": self._artifact(run_dir, "synthesis/proposed-change-set.json"),
            "report_draft": self._artifact(run_dir, "synthesis/report-draft.md"),
        })
        self._transition(run, "draft_review", timestamp)
        self._persist_run(run)
        atomic_write_json(run_dir / "reviews/apply-approval-template.json", self._approval_template(run, "change_set"))
        return self._success(
            "synthesis package validated; draft and proposed changes await review",
            run_id=run_id,
            stage="draft_review",
            extra={
                "report_path": str(run_dir / "synthesis/report-draft.md"),
                "change_set_path": str(run_dir / "synthesis/proposed-change-set.json"),
                "approval_template": str(run_dir / "reviews/apply-approval-template.json"),
            },
            next_actions=["Review claims, limitations, executive brief, tracker events, and proposed state changes."],
        )

    def install_apply_approval(
        self, run_id: str, approval_file: Path | str, *, invocation_mode: str = "interactive"
    ) -> dict[str, Any]:
        self._require_interactive(invocation_mode, "install approvals")
        run = self._load_run(run_id)
        self._require_stage(run, "draft_review")
        self._require_valid_artifacts(run)
        approval = read_json(Path(approval_file).expanduser().resolve(strict=True))
        self._validate_approval_record(run, approval, role="change_set", authorized_role="apply_approver")
        target = self._run_dir(run_id) / "approvals/apply.json"
        atomic_write_json(target, approval)
        self._audit(run, "approval_installed", {"approval_id": approval["approval_id"], "role": "change_set"})
        self._transition(run, "apply_ready", utc_timestamp(), approval_id=approval["approval_id"])
        self._persist_run(run)
        return self._success(
            "apply approval installed",
            run_id=run_id,
            stage="apply_ready",
            extra={"approval_id": approval["approval_id"]},
            next_actions=["Apply the approved change set while its base registry digest still matches."],
        )

    def apply(self, run_id: str, *, invocation_mode: str = "interactive") -> dict[str, Any]:
        self._require_interactive(invocation_mode, "apply canonical changes")
        run = self._load_run(run_id)
        self._require_stage(run, "apply_ready")
        self._require_valid_artifacts(run)
        self._require_installed_approval(run, "apply")
        change_set = read_json(self._run_dir(run_id) / "synthesis/proposed-change-set.json")
        registry_path = self._registry_path(run["market_id"])
        lock_path = registry_path.with_suffix(".lock")
        lock_descriptor: int | None = None
        try:
            try:
                lock_descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                os.write(lock_descriptor, canonical_bytes({"run_id": run_id, "created_at": utc_timestamp()}))
            except FileExistsError as exc:
                raise WorkflowError(
                    "conflict",
                    f"market apply lock already exists: {lock_path}",
                    run_id=run_id,
                    stage=run["stage"],
                    next_actions=["Inspect lock ownership and use an explicit recovery process if it is stale."],
                ) from exc
            registry = self._load_registry(run["market_id"])
            if run_id in registry.get("applied_runs", []):
                output = self.data_root / f"outputs/reports/{run_id}.md"
                if not output.is_file():
                    shutil.copyfile(self._run_dir(run_id) / "synthesis/report-draft.md", output)
                self._transition(run, "complete", utc_timestamp())
                self._persist_run(run)
                return self._success("previously applied run reconciled to complete", run_id=run_id, stage="complete")
            current_digest = digest_value(registry)
            if current_digest != change_set["base_registry_digest"]:
                conflict = {
                    "schema_version": 1,
                    "run_id": run_id,
                    "expected_base_digest": change_set["base_registry_digest"],
                    "current_base_digest": current_digest,
                    "resolution": "Create and review a new change set against the current state.",
                }
                atomic_write_json(self._run_dir(run_id) / "reviews/apply-conflict.json", conflict)
                self._transition(run, "blocked", utc_timestamp())
                run["errors"].append("base registry digest changed before apply")
                self._persist_run(run)
                raise WorkflowError(
                    "conflict",
                    "base registry digest changed; canonical state was not modified",
                    run_id=run_id,
                    stage="blocked",
                    next_actions=["Review reviews/apply-conflict.json and create a new run or change set."],
                )
            updated = copy.deepcopy(registry)
            claims = {claim["claim_id"]: claim for claim in parse_jsonl(self._run_dir(run_id) / "synthesis/claims.jsonl")}
            applied_changes = self._apply_changes(updated, change_set, claims)
            updated.setdefault("applied_runs", []).append(run_id)
            updated.setdefault("history", []).append({
                "run_id": run_id,
                "change_set_id": change_set["change_set_id"],
                "evidence_digest": change_set["evidence_digest"],
                "applied_at": utc_timestamp(),
                "changes": applied_changes,
            })
            atomic_write_json(registry_path, updated)
            output = self.data_root / f"outputs/reports/{run_id}.md"
            shutil.copyfile(self._run_dir(run_id) / "synthesis/report-draft.md", output)
            run["application"] = {
                "path": f"state/markets/{run['market_id']}.json",
                "sha256": digest_bytes(registry_path.read_bytes()),
            }
            self._transition(run, "complete", utc_timestamp())
            self._persist_run(run)
            return self._success(
                "approved competitive state changes applied",
                run_id=run_id,
                stage="complete",
                extra={"changes_applied": len(applied_changes), "registry_digest": digest_value(updated), "report_path": str(output)},
                next_actions=["Use approved outputs through a separately governed downstream workflow; publication is not included."],
            )
        finally:
            if lock_descriptor is not None:
                os.close(lock_descriptor)
                lock_path.unlink(missing_ok=True)

    def validate(self, run_id: str | None = None, market_id: str | None = None) -> dict[str, Any]:
        config = self._load_config()
        errors = validate_config(config)
        markets = [market_id] if market_id else sorted(config["markets"])
        for selected in markets:
            try:
                _, market = self._load_market(selected)
            except WorkflowError as exc:
                errors.append(str(exc))
                continue
            errors.extend(validate_market_pack(market))
            try:
                registry = self._load_registry(selected)
                errors.extend(validate_registry(registry, selected))
            except WorkflowError as exc:
                errors.append(str(exc))
        if run_id:
            try:
                run = self._load_run(run_id)
                errors.extend(validate_run(run))
                errors.extend(self._artifact_errors(run))
            except WorkflowError as exc:
                errors.append(str(exc))
        if errors:
            raise WorkflowError("validation", "validation failed: " + "; ".join(errors), run_id=run_id)
        return self._success("configuration and selected state are valid", run_id=run_id, stage=None, extra={"markets": markets})

    def _load_config(self) -> dict[str, Any]:
        if not self.data_root.is_dir():
            raise WorkflowError("usage/config", f"data root does not exist: {self.data_root}")
        path = ensure_within(self.data_root / "config.json", self.data_root, must_exist=True)
        try:
            value = read_json(path)
        except ValueError as exc:
            raise WorkflowError("usage/config", str(exc)) from exc
        errors = validate_config(value)
        if errors:
            raise WorkflowError("validation", "invalid config: " + "; ".join(errors))
        return value

    def _load_market(self, market_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
        config = self._load_config()
        relative = config["markets"].get(market_id)
        if relative is None:
            raise WorkflowError("usage/config", f"unknown market: {market_id}")
        try:
            path = ensure_within(self.data_root / relative, self.data_root, must_exist=True)
            market = read_json(path)
        except ValueError as exc:
            raise WorkflowError("usage/config", str(exc)) from exc
        errors = validate_market_pack(market)
        if market.get("market_id") != market_id:
            errors.append("market_pack.market_id does not match config key")
        if errors:
            raise WorkflowError("validation", "invalid market pack: " + "; ".join(errors))
        return config, market

    def _run_dir(self, run_id: str) -> Path:
        return ensure_within(self.data_root / "runs" / run_id, self.data_root)

    def _load_run(self, run_id: str) -> dict[str, Any]:
        try:
            run = read_json(ensure_within(self._run_dir(run_id) / "run.json", self.data_root, must_exist=True))
        except ValueError as exc:
            raise WorkflowError("validation", str(exc), run_id=run_id) from exc
        errors = validate_run(run)
        if errors:
            raise WorkflowError("validation", "invalid run state: " + "; ".join(errors), run_id=run_id)
        if run.get("run_id") != run_id:
            raise WorkflowError("validation", "run ID does not match its directory", run_id=run_id)
        return run

    def _registry_path(self, market_id: str) -> Path:
        return ensure_within(self.data_root / f"state/markets/{market_id}.json", self.data_root)

    def _load_registry(self, market_id: str) -> dict[str, Any]:
        try:
            registry = read_json(
                ensure_within(self._registry_path(market_id), self.data_root, must_exist=True)
            )
        except ValueError as exc:
            raise WorkflowError("validation", str(exc)) from exc
        errors = validate_registry(registry, market_id)
        if errors:
            raise WorkflowError("validation", "invalid registry: " + "; ".join(errors))
        return registry

    def _empty_registry(self, market: dict[str, Any]) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "market_id": market["market_id"],
            "competitors": {
                competitor["competitor_id"]: {
                    "display_name": competitor["display_name"],
                    "status": competitor["status"],
                    "capabilities": {},
                    "positioning": {},
                    "pricing": {},
                    "narrative": {},
                    "history": [],
                }
                for competitor in market["competitors"]
            },
            "trackers": {"battlecard_gaps": [], "narrative_changes": [], "win_loss_signals": []},
            "applied_runs": [],
            "history": [],
        }

    def _new_run_id(self) -> str:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        return f"run_{stamp}_{secrets.token_hex(4)}"

    def _transition(self, run: dict[str, Any], target: str, at: str, *, approval_id: str | None = None) -> None:
        allowed = {
            "initialized": {"collecting", "blocked"},
            "collecting": {"evidence_review", "needs_attention", "failed"},
            "evidence_review": {"synthesizing", "collecting"},
            "synthesizing": {"draft_review", "failed"},
            "draft_review": {"apply_ready", "synthesizing"},
            "apply_ready": {"complete", "blocked"},
        }
        current = run["stage"]
        if target not in allowed.get(current, set()):
            raise WorkflowError("validation", f"invalid transition {current} -> {target}", run_id=run["run_id"], stage=current)
        event = {"from": current, "to": target, "at": at}
        if approval_id:
            event["approval_id"] = approval_id
        run["transitions"].append(event)
        run["stage"] = target
        run["updated_at"] = at
        self._audit(run, "transition", event)

    def _persist_run(self, run: dict[str, Any]) -> None:
        errors = validate_run(run)
        if errors:
            raise WorkflowError("validation", "refusing to persist invalid run: " + "; ".join(errors), run_id=run.get("run_id"))
        atomic_write_json(self._run_dir(run["run_id"]) / "run.json", run)

    def _audit(self, run: dict[str, Any], event_type: str, details: dict[str, Any]) -> None:
        append_jsonl(self._run_dir(run["run_id"]) / "audit.jsonl", {
            "schema_version": 1,
            "run_id": run["run_id"],
            "event_type": event_type,
            "recorded_at": utc_timestamp(),
            "controller_version": CONTROLLER_VERSION,
            "details": details,
        })

    def _artifact(self, run_dir: Path, relative: str) -> dict[str, str]:
        path = run_dir / relative
        return {"path": relative, "sha256": digest_bytes(path.read_bytes())}

    def _artifact_errors(self, run: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        run_dir = self._run_dir(run["run_id"])
        for role, artifact in run.get("artifacts", {}).items():
            try:
                path = ensure_within(run_dir / artifact["path"], run_dir, must_exist=True)
            except (KeyError, OSError, ValueError) as exc:
                errors.append(f"{role}: {exc}")
                continue
            actual = digest_bytes(path.read_bytes())
            if actual != artifact.get("sha256"):
                errors.append(f"{role}: digest mismatch")
        return errors

    def _require_valid_artifacts(self, run: dict[str, Any]) -> None:
        errors = self._artifact_errors(run)
        if errors:
            raise WorkflowError(
                "validation",
                "artifact integrity failed: " + "; ".join(errors),
                run_id=run["run_id"],
                stage=run["stage"],
                next_actions=["Restore the exact recorded artifacts or create a new run."],
            )

    def _require_stage(self, run: dict[str, Any], required: str) -> None:
        if run["stage"] != required:
            raise WorkflowError(
                "validation",
                f"operation requires stage {required}; run is {run['stage']}",
                run_id=run["run_id"],
                stage=run["stage"],
                next_actions=self._next_actions(run),
            )

    def _approval_template(self, run: dict[str, Any], role: str) -> dict[str, Any]:
        artifact = run["artifacts"]["evidence_manifest" if role == "evidence" else "change_set"]
        stage = "evidence_review" if role == "evidence" else "draft_review"
        approver_role = "evidence_reviewer" if role == "evidence" else "apply_approver"
        return {
            "schema_version": 1,
            "approval_id": "replace-with-stable-approval-id",
            "run_id": run["run_id"],
            "stage": stage,
            "decision": "approved",
            "artifact": {
                "role": "evidence_manifest" if role == "evidence" else "change_set",
                "path": artifact["path"],
                "sha256": artifact["sha256"],
            },
            "approver": {"id": "replace-with-authorized-identity", "role": approver_role},
            "decided_at": "replace-with-ISO-8601-timestamp",
            "comment": "replace-with-review-note",
        }

    def _validate_approval_record(self, run: dict[str, Any], approval: dict[str, Any], *, role: str, authorized_role: str) -> None:
        errors = validate_approval(approval)
        artifact_key = "evidence_manifest" if role == "evidence_manifest" else "change_set"
        expected = run["artifacts"].get(artifact_key)
        if approval.get("run_id") != run["run_id"]:
            errors.append("approval.run_id: does not match run")
        required_stage = "evidence_review" if role == "evidence_manifest" else "draft_review"
        if approval.get("stage") != required_stage:
            errors.append(f"approval.stage: must be {required_stage}")
        if approval.get("decision") != "approved":
            errors.append("approval.decision: must be approved")
        artifact = approval.get("artifact", {})
        if artifact.get("role") != role:
            errors.append(f"approval.artifact.role: must be {role}")
        if expected and (artifact.get("path") != expected["path"] or artifact.get("sha256") != expected["sha256"]):
            errors.append("approval.artifact: path or digest is stale")
        approver = approval.get("approver", {})
        config = self._load_config()
        if approver.get("role") != authorized_role:
            errors.append(f"approval.approver.role: must be {authorized_role}")
        if approver.get("id") not in config["reviewers"][authorized_role]:
            errors.append("approval.approver.id: identity is not authorized for this role")
        if errors:
            raise WorkflowError("approval", "approval is invalid: " + "; ".join(errors), run_id=run["run_id"], stage=run["stage"])

    def _require_installed_approval(self, run: dict[str, Any], kind: str) -> dict[str, Any]:
        path = self._run_dir(run["run_id"]) / f"approvals/{kind}.json"
        try:
            approval = read_json(path)
        except ValueError as exc:
            raise WorkflowError(
                "approval",
                f"missing installed {kind} approval",
                run_id=run["run_id"],
                stage=run["stage"],
                next_actions=[f"Install a digest-bound {kind} approval record."],
            ) from exc
        role = "evidence_manifest" if kind == "evidence" else "change_set"
        authorized = "evidence_reviewer" if kind == "evidence" else "apply_approver"
        self._validate_approval_record(run, approval, role=role, authorized_role=authorized)
        return approval

    def _validate_synthesis_package(
        self,
        package: Any,
        run: dict[str, Any],
        evidence: list[dict[str, Any]],
        manifest: dict[str, Any],
        registry: dict[str, Any],
    ) -> list[str]:
        if not isinstance(package, dict):
            return ["package must be an object"]
        required = ("schema_version", "run_id", "market_id", "evidence_digest", "claims", "report", "proposed_change_set")
        errors = [f"package.{field}: required" for field in required if field not in package]
        if errors:
            return errors
        errors.extend(self._validate_package_identity(package, run, manifest))
        evidence_by_id = {record["evidence_id"]: record for record in evidence}
        claims = package.get("claims") if isinstance(package.get("claims"), list) else []
        if not isinstance(package.get("claims"), list):
            errors.append("package.claims: must be an array")
        claim_errors, claim_ids = self._validate_claims(
            claims, run, evidence_by_id, set(registry["competitors"])
        )
        errors.extend(claim_errors)
        errors.extend(self._validate_report(package.get("report"), claims, claim_ids, evidence_by_id))
        errors.extend(
            self._validate_change_set(
                package.get("proposed_change_set"), run, manifest, registry, claim_ids
            )
        )
        return errors

    def _validate_package_identity(
        self, package: dict[str, Any], run: dict[str, Any], manifest: dict[str, Any]
    ) -> list[str]:
        errors: list[str] = []
        if package.get("schema_version") != 1:
            errors.append("package.schema_version: must be 1")
        if package.get("run_id") != run["run_id"] or package.get("market_id") != run["market_id"]:
            errors.append("package run_id or market_id does not match")
        if package.get("evidence_digest") != manifest["evidence_digest"]:
            errors.append("package.evidence_digest is stale")
        return errors

    def _validate_claims(
        self,
        claims: list[Any],
        run: dict[str, Any],
        evidence_by_id: dict[str, dict[str, Any]],
        competitor_ids: set[str],
    ) -> tuple[list[str], set[str]]:
        errors: list[str] = []
        claim_ids: set[str] = set()
        for index, claim in enumerate(claims):
            claim_errors, claim_id = self._validate_claim_entry(
                claim, index, run, evidence_by_id, competitor_ids
            )
            errors.extend(claim_errors)
            if isinstance(claim_id, str):
                if claim_id in claim_ids:
                    errors.append(f"package.claims[{index}].claim_id: duplicate")
                claim_ids.add(claim_id)
        return errors, claim_ids

    def _validate_claim_entry(
        self,
        claim: Any,
        index: int,
        run: dict[str, Any],
        evidence_by_id: dict[str, dict[str, Any]],
        competitor_ids: set[str],
    ) -> tuple[list[str], Any]:
        label = f"package.claims[{index}]"
        errors = validate_claim(claim, label)
        if not isinstance(claim, dict):
            return errors, None
        if claim.get("market_id") != run["market_id"]:
            errors.append(f"{label}.market_id: mismatch")
        if claim.get("competitor_id") not in competitor_ids:
            errors.append(f"{label}.competitor_id: unknown competitor")
        support = claim.get("evidence_ids", [])
        if not isinstance(support, list) or not all(isinstance(item, str) for item in support):
            support = []
        if claim.get("claim_type") != "unknown" and not support:
            errors.append(f"{label}: material claim needs evidence")
        supporting = [evidence_by_id[item] for item in support if item in evidence_by_id]
        missing = [item for item in support if item not in evidence_by_id]
        errors.extend(self._validate_claim_support(claim, supporting, missing, label))
        return errors, claim.get("claim_id")

    def _validate_claim_support(
        self,
        claim: dict[str, Any],
        supporting: list[dict[str, Any]],
        missing: list[str],
        label: str,
    ) -> list[str]:
        errors: list[str] = []
        if missing:
            errors.append(f"{label}.evidence_ids: unknown {missing}")
        if any(item["classification"] in {"missing", "rejected"} for item in supporting):
            errors.append(f"{label}: rejected or missing evidence cannot support a claim")
        has_conflict = any(item["relationships"]["conflicts_with"] for item in supporting)
        declares_conflict = any(
            "conflict" in limitation.lower() for limitation in claim.get("limitations", [])
        )
        if has_conflict and not declares_conflict:
            errors.append(f"{label}: conflicting support requires an explicit limitation")
        strong_support = any(
            item["confidence"] == "high"
            and item["source"]["source_type"] not in {"search_snippet", "unattributed_summary"}
            for item in supporting
        )
        if claim.get("confidence") == "high" and supporting and not strong_support:
            errors.append(f"{label}: high confidence lacks strong support")
        if supporting:
            required_rank = max(SENSITIVITY_RANK[item["sensitivity"]] for item in supporting)
            if SENSITIVITY_RANK.get(claim.get("sensitivity"), 99) < required_rank:
                errors.append(f"{label}.sensitivity: cannot downgrade supporting evidence")
        return errors

    def _validate_report(
        self,
        report: Any,
        claims: list[Any],
        claim_ids: set[str],
        evidence_by_id: dict[str, dict[str, Any]],
    ) -> list[str]:
        errors: list[str] = []
        report_fields = ("executive_signals", "coverage", "limitations", "material_changes", "implications", "open_questions", "next_actions", "selected_claim_ids", "public_safe")
        if not isinstance(report, dict):
            return ["package.report: must be an object"]
        for field in report_fields:
            if field not in report:
                errors.append(f"package.report.{field}: required")
        for field in ("coverage", "limitations", "open_questions"):
            values = report.get(field)
            if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
                errors.append(f"package.report.{field}: must be a string array")
        if not isinstance(report.get("public_safe"), bool):
            errors.append("package.report.public_safe: must be a boolean")
        selected = report.get("selected_claim_ids", [])
        selected_valid = isinstance(selected, list) and all(
            isinstance(item, str) and item in claim_ids for item in selected
        )
        if not selected_valid:
            errors.append("package.report.selected_claim_ids: contains an unknown claim")
        executive_signals = report.get("executive_signals")
        if isinstance(executive_signals, list) and len(executive_signals) > 2:
            errors.append("package.report.executive_signals: maximum is 2")
        statement_claim_ids, statement_errors = self._validate_report_statements(report, claim_ids)
        errors.extend(statement_errors)
        selected_set = set(selected) if selected_valid else set()
        if not statement_claim_ids.issubset(selected_set):
            errors.append("package.report.selected_claim_ids: must include every claim used by report statements")
        if report.get("public_safe") is True:
            errors.extend(self._validate_public_report(claims, selected_set, evidence_by_id))
        return errors

    def _validate_report_statements(
        self, report: dict[str, Any], claim_ids: set[str]
    ) -> tuple[set[str], list[str]]:
        used_claim_ids: set[str] = set()
        errors: list[str] = []
        for section in ("executive_signals", "material_changes", "implications", "next_actions"):
            statements = report.get(section)
            if not isinstance(statements, list):
                errors.append(f"package.report.{section}: must be an array")
                continue
            for index, statement in enumerate(statements):
                if not isinstance(statement, dict) or not isinstance(statement.get("text"), str) or not statement["text"].strip():
                    errors.append(f"package.report.{section}[{index}]: must contain text")
                    continue
                support = statement.get("claim_ids")
                support_valid = isinstance(support, list) and bool(support) and all(
                    isinstance(item, str) and item in claim_ids for item in support
                )
                if not support_valid:
                    errors.append(f"package.report.{section}[{index}].claim_ids: must contain known claims")
                    continue
                used_claim_ids.update(support)
        return used_claim_ids, errors

    def _validate_public_report(
        self,
        claims: list[Any],
        selected: set[str],
        evidence_by_id: dict[str, dict[str, Any]],
    ) -> list[str]:
        selected_claims = [
            claim for claim in claims
            if isinstance(claim, dict) and claim.get("claim_id") in selected
        ]
        for claim in selected_claims:
            has_private_support = any(
                not evidence_by_id[item].get("public_safe")
                for item in claim.get("evidence_ids", [])
                if item in evidence_by_id
            )
            if claim.get("sensitivity") != "public" or has_private_support:
                return ["package.report: public-safe report selects non-public support"]
        return []

    def _validate_change_set(
        self,
        change_set: Any,
        run: dict[str, Any],
        manifest: dict[str, Any],
        registry: dict[str, Any],
        claim_ids: set[str],
    ) -> list[str]:
        errors: list[str] = []
        if not isinstance(change_set, dict):
            return ["package.proposed_change_set: must be an object"]
        required = ("schema_version", "change_set_id", "run_id", "market_id", "base_registry_digest", "evidence_digest", "changes", "status")
        errors.extend(
            f"package.proposed_change_set.{field}: required"
            for field in required if field not in change_set
        )
        if change_set.get("schema_version") != 1:
            errors.append("change set schema_version must be 1")
        if not isinstance(change_set.get("change_set_id"), str) or not change_set.get("change_set_id"):
            errors.append("change set change_set_id must be a non-empty string")
        if change_set.get("run_id") != run["run_id"] or change_set.get("market_id") != run["market_id"]:
            errors.append("change set run or market mismatch")
        if change_set.get("evidence_digest") != manifest["evidence_digest"]:
            errors.append("change set evidence digest mismatch")
        if change_set.get("base_registry_digest") != digest_value(registry):
            errors.append("change set base registry digest mismatch")
        if change_set.get("status") != "proposed":
            errors.append("change set status must be proposed")
        changes = change_set.get("changes")
        if not isinstance(changes, list):
            errors.append("change set changes must be an array")
        else:
            for index, change in enumerate(changes):
                errors.extend(self._validate_change(change, index, registry, claim_ids))
        return errors

    def _validate_change(self, change: Any, index: int, registry: dict[str, Any], claim_ids: set[str]) -> list[str]:
        label = f"change_set.changes[{index}]"
        if not isinstance(change, dict):
            return [f"{label}: must be an object"]
        operation = change.get("operation")
        errors: list[str] = []
        support = change.get("claim_ids")
        support_valid = isinstance(support, list) and bool(support) and all(
            isinstance(item, str) and item in claim_ids for item in support
        )
        if not support_valid:
            errors.append(f"{label}.claim_ids: must contain known claims")
        if operation == "set_field":
            errors.extend(self._validate_set_field_change(change, label, registry))
        elif operation == "append_tracker_event":
            errors.extend(self._validate_tracker_change(change, label))
        else:
            errors.append(f"{label}.operation: unsupported")
        return errors

    def _validate_set_field_change(
        self, change: dict[str, Any], label: str, registry: dict[str, Any]
    ) -> list[str]:
        errors: list[str] = []
        path = change.get("path")
        if not isinstance(path, list) or len(path) < 4 or path[0] != "competitors":
            errors.append(f"{label}.path: must target competitors.<id>.<field>")
        elif path[1] not in registry["competitors"] or path[2] not in {
            "capabilities", "positioning", "pricing", "narrative", "status"
        }:
            errors.append(f"{label}.path: target is not allowed")
        elif any(
            not isinstance(part, str) or not part or part in {"__class__", "__dict__"}
            for part in path
        ):
            errors.append(f"{label}.path: contains an unsafe segment")
        if "value" not in change:
            errors.append(f"{label}.value: required")
        return errors

    def _validate_tracker_change(self, change: dict[str, Any], label: str) -> list[str]:
        errors: list[str] = []
        if change.get("tracker") not in {
            "battlecard_gaps", "narrative_changes", "win_loss_signals"
        }:
            errors.append(f"{label}.tracker: invalid")
        if not isinstance(change.get("event"), dict):
            errors.append(f"{label}.event: must be an object")
        return errors

    def _apply_changes(self, registry: dict[str, Any], change_set: dict[str, Any], claims: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
        applied: list[dict[str, Any]] = []
        for change in change_set["changes"]:
            if change["operation"] == "set_field":
                cursor: Any = registry
                for part in change["path"][:-1]:
                    cursor = cursor.setdefault(part, {})
                field = change["path"][-1]
                previous = copy.deepcopy(cursor.get(field))
                cursor[field] = copy.deepcopy(change["value"])
                applied.append({
                    "operation": "set_field",
                    "path": change["path"],
                    "previous": previous,
                    "value": change["value"],
                    "claim_ids": change["claim_ids"],
                    "evidence_ids": sorted({evidence_id for claim_id in change["claim_ids"] for evidence_id in claims[claim_id]["evidence_ids"]}),
                })
                competitor = registry["competitors"][change["path"][1]]
                competitor.setdefault("history", []).append({"change_set_id": change_set["change_set_id"], "path": change["path"], "previous": previous, "claim_ids": change["claim_ids"]})
            else:
                event = copy.deepcopy(change["event"])
                event.update({"change_set_id": change_set["change_set_id"], "claim_ids": change["claim_ids"]})
                existing = registry["trackers"][change["tracker"]]
                event_digest = digest_value(event)
                if not any(item.get("event_digest") == event_digest for item in existing):
                    event["event_digest"] = event_digest
                    existing.append(event)
                applied.append({"operation": "append_tracker_event", "tracker": change["tracker"], "event_digest": event_digest, "claim_ids": change["claim_ids"]})
        return applied

    def _render_evidence_review(self, run: dict[str, Any], manifest: dict[str, Any], coverage: dict[str, Any], evidence: list[dict[str, Any]]) -> str:
        lines = [
            f"# Evidence review: {run['market_id']}", "",
            "Status: Draft — evidence approval required before synthesis.", "",
            f"- Run ID: `{run['run_id']}`",
            f"- Window: `{run['window']['from']}` through `{run['window']['to']}` (end exclusive)",
            f"- Evidence digest: `{manifest['evidence_digest']}`",
            f"- Evidence records: {len(evidence)}", "",
            "## Coverage and limitations", "",
        ]
        for source in coverage["sources"]:
            lines.append(f"- {source['source_id']}: {source['status']} ({'required' if source['required'] else 'optional'})")
        for competitor in coverage["competitors"]:
            lines.append(
                f"- {competitor['competitor_id']}: {competitor['evidence_count']} accepted evidence record(s)"
            )
        for limitation in coverage["limitations"]:
            lines.append(f"- Limitation: {limitation}")
        lines.extend(["", "## Evidence", "", "| ID | Competitor | Category | Classification | Confidence | Source |", "|---|---|---|---|---|---|"])
        for record in evidence:
            lines.append(f"| `{record['evidence_id']}` | {record['competitor_id']} | {record['category']} | {record['classification']} | {record['confidence']} | {record['source']['title']} |")
        lines.extend(["", "Conversation is not an approval system of record. Use the digest-bound approval template.", ""])
        return "\n".join(lines)

    def _render_report(self, run: dict[str, Any], manifest: dict[str, Any], coverage: dict[str, Any], evidence: list[dict[str, Any]], package: dict[str, Any]) -> str:
        report = package["report"]
        claims = {item["claim_id"]: item for item in package["claims"]}
        evidence_by_id = {item["evidence_id"]: item for item in evidence}
        lines = [
            f"# Competitive briefing: {run['market_id']}", "",
            "Status: Draft — apply approval does not authorize external publication.", "",
            f"- Run ID: `{run['run_id']}`",
            f"- Window: `{run['window']['from']}` through `{run['window']['to']}` (end exclusive)",
            f"- Evidence digest: `{manifest['evidence_digest']}`", "",
            "## Executive signals", "",
        ]
        lines.extend(
            f"- {item['text']} (claims: {', '.join(item['claim_ids'])})"
            for item in report["executive_signals"]
        )
        if not report["executive_signals"]:
            lines.append("- No stakeholder-relevant signal selected.")
        for heading, key in (
            ("Coverage", "coverage"),
            ("Limitations", "limitations"),
            ("Material changes", "material_changes"),
            ("Implications", "implications"),
            ("Open questions", "open_questions"),
            ("Proposed next actions", "next_actions"),
        ):
            lines.extend(["", f"## {heading}", ""])
            if key in {"material_changes", "implications", "next_actions"}:
                lines.extend(
                    f"- {item['text']} (claims: {', '.join(item['claim_ids'])})"
                    for item in report[key]
                )
                if not report[key]:
                    lines.append("- None recorded.")
            else:
                lines.extend(f"- {item}" for item in report[key] or ["None recorded."])
        lines.extend(["", "## Claims and evidence", "", "| Claim | Type | Confidence | Evidence |", "|---|---|---|---|"])
        for claim_id in report["selected_claim_ids"]:
            claim = claims[claim_id]
            links = ", ".join(f"`{item}`" for item in claim["evidence_ids"]) or "Missing"
            lines.append(f"| {claim['text']} | {claim['claim_type']} | {claim['confidence']} | {links} |")
        lines.extend(["", "## Evidence index", "", "| ID | Classification | Source | Date |", "|---|---|---|---|"])
        selected_evidence = sorted({item for claim_id in report["selected_claim_ids"] for item in claims[claim_id]["evidence_ids"]})
        for evidence_id in selected_evidence:
            record = evidence_by_id[evidence_id]
            lines.append(f"| `{evidence_id}` | {record['classification']} | {record['source']['canonical_uri']} | {record['source'].get('published_at') or 'Unknown'} |")
        lines.extend(["", "## Proposed state changes", ""])
        for change in package["proposed_change_set"]["changes"]:
            target = ".".join(change.get("path", [])) or change.get("tracker", "unknown")
            lines.append(f"- {change['operation']}: `{target}` (claims: {', '.join(change['claim_ids'])})")
        lines.append("")
        return "\n".join(lines)

    def _next_actions(self, run: dict[str, Any]) -> list[str]:
        return {
            "evidence_review": ["Review evidence and install a digest-bound evidence approval."],
            "draft_review": ["Review claims and proposed changes, then install an apply approval."],
            "apply_ready": ["Apply before the canonical base digest changes."],
            "complete": ["Consume approved local outputs through a separately governed workflow."],
            "blocked": ["Inspect the conflict artifact and create a new reviewed proposal."],
            "failed": ["Inspect coverage and create a recorded retry or new run."],
        }.get(run["stage"], ["Inspect the run record for the allowed next transition."])

    def _require_interactive(self, invocation_mode: str, operation: str) -> None:
        if invocation_mode != "interactive":
            raise WorkflowError(
                "approval",
                f"{operation} is not permitted for a non-interactive worker",
                next_actions=["Continue from Codex Desktop through the configured human review flow."],
            )

    def _success(
        self,
        message: str,
        *,
        run_id: str | None = None,
        stage: str | None = None,
        warnings: list[str] | None = None,
        extra: dict[str, Any] | None = None,
        next_actions: list[str] | None = None,
    ) -> dict[str, Any]:
        result: dict[str, Any] = {
            "status": "ok",
            "code": 0,
            "message": message,
            "run_id": run_id,
            "stage": stage,
            "warnings": warnings or [],
            "next_actions": next_actions or [],
        }
        if extra:
            result.update(extra)
        return result


def _parse_timestamp(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise WorkflowError("usage/config", f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise WorkflowError("usage/config", f"{label} must include a timezone")
    return parsed
