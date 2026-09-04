#!/usr/bin/env python3
"""Portable control plane for digest-bound, approval-gated workflow runs."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any

from approval_verifier import ApprovalVerificationError, verify_approval
from governance_policy import PolicyError, json_yaml, read_structured


SCHEMA_VERSION = 2
STAGES = (
    "initialized",
    "collection",
    "evidence_review",
    "claims_review",
    "framing_review",
    "copy_review",
    "staging_ready",
    "publish_ready",
    "published",
)
NEXT_STAGE = dict(zip(STAGES[:-1], STAGES[1:]))
ARTIFACT_BY_GATE = {
    "evidence": "evidence",
    "claims": "claims",
    "framing": "framing",
    "copy": "copy",
    "publish": "staging",
}
APPROVAL_FOR_TRANSITION = {
    ("evidence_review", "claims_review"): "evidence",
    ("claims_review", "framing_review"): "claims",
    ("framing_review", "copy_review"): "framing",
    ("copy_review", "staging_ready"): "copy",
    ("staging_ready", "publish_ready"): "publish",
}
ARTIFACTS_REQUIRED_AT_STAGE = {
    "evidence_review": ("evidence",),
    "claims_review": ("evidence", "claims"),
    "framing_review": ("evidence", "claims", "framing"),
    "copy_review": ("evidence", "claims", "framing", "copy"),
    "staging_ready": ("evidence", "claims", "framing", "copy", "staging"),
    "publish_ready": ("evidence", "claims", "framing", "copy", "staging"),
    "published": ("evidence", "claims", "framing", "copy", "staging"),
}
APPROVALS_REQUIRED_AT_STAGE = {
    "claims_review": ("evidence",),
    "framing_review": ("evidence", "claims"),
    "copy_review": ("evidence", "claims", "framing"),
    "staging_ready": ("evidence", "claims", "framing", "copy"),
    "publish_ready": ("evidence", "claims", "framing", "copy", "publish"),
    "published": ("evidence", "claims", "framing", "copy", "publish"),
}
ARTIFACT_REGISTRATION_STAGE = {
    "evidence": "collection",
    "claims": "evidence_review",
    "framing": "claims_review",
    "copy": "framing_review",
    "staging": "copy_review",
}
APPROVAL_STAGE = {
    "evidence": "evidence_review",
    "claims": "claims_review",
    "framing": "framing_review",
    "copy": "copy_review",
    "publish": "staging_ready",
}


class WorkflowControlError(PolicyError):
    """Raised when run state violates the governed workflow contract."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repo_path(root: Path, value: str, label: str) -> Path:
    raw = Path(value)
    if raw.is_absolute():
        raise WorkflowControlError(f"{label} must be repository-relative")
    target = (root.resolve() / raw).resolve(strict=False)
    try:
        target.relative_to(root.resolve())
    except ValueError as exc:
        raise WorkflowControlError(f"{label} must stay inside the repository") from exc
    return target


def _run_path(root: Path, value: str) -> Path:
    target = _repo_path(root, value, "run path")
    relative = target.relative_to(root.resolve())
    if relative.suffix != ".yaml" or relative.parts[:2] != ("state", "runs"):
        raise WorkflowControlError("run path must be a .yaml file under state/runs/")
    return target


def _atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(json_yaml(payload))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def load_source_policy(root: Path, relative: str) -> tuple[Path, dict[str, Any]]:
    path = _repo_path(root, relative, "source policy path")
    if not path.is_file():
        raise WorkflowControlError("source policy is unavailable")
    policy = read_structured(path)
    if not isinstance(policy, dict) or policy.get("schema_version") != 1:
        raise WorkflowControlError("source policy schema_version must be 1")
    if policy.get("status") != "active":
        raise WorkflowControlError("source policy must be active")
    sources = policy.get("allowed_sources")
    if not isinstance(sources, list) or not sources:
        raise WorkflowControlError("source policy must declare allowed_sources")
    authority = policy.get("approval_authority")
    if not isinstance(authority, dict):
        raise WorkflowControlError("source policy must declare approval_authority")
    if not isinstance(authority.get("authority_id"), str) or not authority["authority_id"]:
        raise WorkflowControlError("approval_authority.authority_id must be non-empty")
    verifier = authority.get("verifier_config")
    if not isinstance(verifier, str) or not Path(verifier).is_absolute():
        raise WorkflowControlError("approval_authority.verifier_config must be absolute")
    try:
        Path(verifier).resolve(strict=False).relative_to(root.resolve())
    except ValueError:
        pass
    else:
        raise WorkflowControlError("approval verifier configuration must be outside the repository")
    return path, policy


def build_initial_run(
    *, root: Path, workflow_id: str, run_id: str, policy_path: str, execution_mode: str
) -> dict[str, Any]:
    if execution_mode not in {"interactive", "scheduled"}:
        raise WorkflowControlError("execution_mode must be interactive or scheduled")
    policy_file, _ = load_source_policy(root, policy_path)
    return {
        "schema_version": SCHEMA_VERSION,
        "workflow_id": workflow_id,
        "run_id": run_id,
        "stage": "initialized",
        "runtime": {"execution_mode": execution_mode},
        "source_policy": {
            "path": policy_file.relative_to(root.resolve()).as_posix(),
            "sha256": sha256_file(policy_file),
        },
        "artifacts": {},
        "approvals": {},
        "transition_history": [],
    }


def load_run(root: Path, relative: str) -> tuple[Path, dict[str, Any]]:
    path = _run_path(root, relative)
    if not path.is_file():
        raise WorkflowControlError("run state is unavailable")
    run = read_structured(path)
    if not isinstance(run, dict):
        raise WorkflowControlError("run state must be a mapping")
    return path, run


def write_run(root: Path, relative: str, run: dict[str, Any]) -> Path:
    path = _run_path(root, relative)
    validate_run(run, root)
    _atomic_write(path, run)
    return path


def discover_runs(root: Path) -> list[str]:
    state_root = root / "state" / "runs"
    if not state_root.is_dir():
        return []
    results: list[str] = []
    for path in sorted(state_root.rglob("*.yaml")):
        try:
            payload = read_structured(path)
        except (OSError, PolicyError):
            continue
        if isinstance(payload, dict) and payload.get("schema_version") == SCHEMA_VERSION:
            results.append(path.relative_to(root).as_posix())
    return results


def _artifact_current(root: Path, artifact: dict[str, Any]) -> bool:
    path_value = artifact.get("path")
    digest = artifact.get("sha256")
    if not isinstance(path_value, str) or not isinstance(digest, str):
        return False
    path = _repo_path(root, path_value, "artifact path")
    return path.is_file() and sha256_file(path) == digest


def validate_run(run: dict[str, Any], root: Path) -> None:
    if run.get("schema_version") != SCHEMA_VERSION:
        raise WorkflowControlError(f"schema_version must be {SCHEMA_VERSION}")
    if run.get("stage") not in STAGES:
        raise WorkflowControlError("run stage is invalid")
    for field in ("workflow_id", "run_id"):
        if not isinstance(run.get(field), str) or not run[field].strip():
            raise WorkflowControlError(f"{field} must be a non-empty string")
    runtime = run.get("runtime")
    if not isinstance(runtime, dict) or runtime.get("execution_mode") not in {
        "interactive", "scheduled"
    }:
        raise WorkflowControlError("runtime.execution_mode is invalid")
    source = run.get("source_policy")
    if not isinstance(source, dict) or not isinstance(source.get("path"), str):
        raise WorkflowControlError("source_policy is invalid")
    policy_path, source_policy = load_source_policy(root, source["path"])
    if source.get("sha256") != sha256_file(policy_path):
        raise WorkflowControlError("source policy digest is stale")
    artifacts = run.get("artifacts")
    if not isinstance(artifacts, dict):
        raise WorkflowControlError("artifacts must be a mapping")
    for key, artifact in artifacts.items():
        if key not in set(ARTIFACT_BY_GATE.values()) or not isinstance(artifact, dict):
            raise WorkflowControlError(f"unsupported artifact record: {key}")
        if artifact.get("disposition") != "staging" or not _artifact_current(root, artifact):
            raise WorkflowControlError(f"artifact is missing or stale: {key}")
    for required in ARTIFACTS_REQUIRED_AT_STAGE.get(str(run["stage"]), ()):
        if required not in artifacts:
            raise WorkflowControlError(f"stage requires artifact: {required}")
    approvals = run.get("approvals")
    if not isinstance(approvals, dict):
        raise WorkflowControlError("approvals must be a mapping")
    for gate, approval in approvals.items():
        if gate not in ARTIFACT_BY_GATE or not isinstance(approval, dict):
            raise WorkflowControlError(f"unsupported approval record: {gate}")
        artifact = artifacts.get(ARTIFACT_BY_GATE[gate])
        if not isinstance(artifact, dict):
            raise WorkflowControlError(f"approval has no artifact: {gate}")
        if approval.get("decision") != "approved":
            raise WorkflowControlError(f"approval is not approved: {gate}")
        if approval.get("gate") != gate:
            raise WorkflowControlError(f"approval gate does not match its record: {gate}")
        for field in (
            "approver", "approval_ref", "reviewed_revision", "approved_at", "authority_id"
        ):
            if not isinstance(approval.get(field), str) or not approval[field].strip():
                raise WorkflowControlError(f"approval {field} is invalid: {gate}")
        try:
            approved_at = datetime.fromisoformat(
                approval["approved_at"].replace("Z", "+00:00")
            )
        except ValueError as exc:
            raise WorkflowControlError(f"approval approved_at is invalid: {gate}") from exc
        if approved_at.utcoffset() is None:
            raise WorkflowControlError(f"approval approved_at lacks timezone: {gate}")
        if approval.get("artifact_path") != artifact.get("path") or approval.get(
            "artifact_sha256"
        ) != artifact.get("sha256"):
            raise WorkflowControlError(f"approval is stale: {gate}")
        verifier_config = approval.get("verifier_config")
        if not isinstance(verifier_config, str) or not Path(verifier_config).is_absolute():
            raise WorkflowControlError(f"approval verifier_config is invalid: {gate}")
        authority = source_policy["approval_authority"]
        if approval["authority_id"] != authority["authority_id"]:
            raise WorkflowControlError(f"approval authority is invalid: {gate}")
        if Path(verifier_config).resolve(strict=False) != Path(
            authority["verifier_config"]
        ).resolve(strict=False):
            raise WorkflowControlError(f"approval verifier_config does not match policy: {gate}")
    for required in APPROVALS_REQUIRED_AT_STAGE.get(str(run["stage"]), ()):
        if required not in approvals:
            raise WorkflowControlError(f"stage requires verified approval: {required}")

    history = run.get("transition_history")
    if not isinstance(history, list):
        raise WorkflowControlError("transition_history must be a list")
    reached = "initialized"
    for entry in history:
        if not isinstance(entry, dict) or set(entry) != {"from", "to"}:
            raise WorkflowControlError("transition_history contains an invalid entry")
        if entry["from"] != reached or NEXT_STAGE.get(reached) != entry["to"]:
            raise WorkflowControlError("transition_history is not contiguous")
        reached = str(entry["to"])
    if reached != run["stage"]:
        raise WorkflowControlError("transition_history does not reach the current stage")

    publication = run.get("publication")
    if run["stage"] == "published":
        if not isinstance(publication, dict):
            raise WorkflowControlError("published run requires a publication receipt")
        for field in ("operation", "receipt_id", "published_at", "artifact_sha256"):
            if not isinstance(publication.get(field), str) or not publication[field]:
                raise WorkflowControlError(f"publication receipt is missing {field}")
    elif publication is not None:
        raise WorkflowControlError("publication receipt is permitted only at published")


def register_artifact(
    run: dict[str, Any], *, root: Path, key: str, relative_path: str
) -> dict[str, Any]:
    validate_run(run, root)
    if key not in set(ARTIFACT_BY_GATE.values()):
        raise WorkflowControlError("artifact key is invalid")
    if run["stage"] != ARTIFACT_REGISTRATION_STAGE[key]:
        raise WorkflowControlError(
            f"{key} may be registered only at {ARTIFACT_REGISTRATION_STAGE[key]}"
        )
    if run["runtime"]["execution_mode"] == "scheduled" and not (
        run["stage"] == "collection" and key == "evidence"
    ):
        raise WorkflowControlError("scheduled collection may register only evidence")
    path = _repo_path(root, relative_path, "artifact path")
    if not path.is_file():
        raise WorkflowControlError("artifact path does not exist")
    updated = deepcopy(run)
    updated["artifacts"][key] = {
        "path": path.relative_to(root.resolve()).as_posix(),
        "sha256": sha256_file(path),
        "disposition": "staging",
    }
    for gate, artifact_key in ARTIFACT_BY_GATE.items():
        if artifact_key == key:
            updated["approvals"].pop(gate, None)
    return updated


def transition(run: dict[str, Any], *, root: Path, target_stage: str) -> dict[str, Any]:
    validate_run(run, root)
    current = str(run["stage"])
    if NEXT_STAGE.get(current) != target_stage:
        raise WorkflowControlError(f"only the next stage is permitted from {current}")
    if target_stage == "published":
        raise WorkflowControlError("published stage is reserved for the publisher guard")
    if run["runtime"]["execution_mode"] == "scheduled" and target_stage not in {
        "collection", "evidence_review"
    }:
        raise WorkflowControlError("scheduled execution cannot advance a human-review gate")
    for required in ARTIFACTS_REQUIRED_AT_STAGE.get(target_stage, ()):
        if required not in run["artifacts"]:
            raise WorkflowControlError(f"target stage requires artifact: {required}")
    gate = APPROVAL_FOR_TRANSITION.get((current, target_stage))
    if gate and gate not in run["approvals"]:
        raise WorkflowControlError(f"target stage requires verified approval: {gate}")
    updated = deepcopy(run)
    updated["stage"] = target_stage
    updated["transition_history"].append({"from": current, "to": target_stage})
    return updated


def record_verified_approval(
    run: dict[str, Any], *, root: Path, gate: str, approval_ref: str,
    reviewed_revision: str,
) -> dict[str, Any]:
    validate_run(run, root)
    if run["runtime"]["execution_mode"] == "scheduled":
        raise WorkflowControlError("scheduled execution cannot create approval")
    if run["stage"] != APPROVAL_STAGE.get(gate):
        raise WorkflowControlError(
            f"{gate} approval may be recorded only at {APPROVAL_STAGE.get(gate)}"
        )
    artifact_key = ARTIFACT_BY_GATE.get(gate)
    artifact = run["artifacts"].get(artifact_key) if artifact_key else None
    if not isinstance(artifact, dict):
        raise WorkflowControlError(f"approval requires artifact: {artifact_key}")
    request = {
        "gate": gate,
        "approval_ref": approval_ref,
        "reviewed_revision": reviewed_revision,
        "artifact_path": artifact["path"],
        "artifact_sha256": artifact["sha256"],
    }
    _, source_policy = load_source_policy(root, run["source_policy"]["path"])
    authority = source_policy["approval_authority"]
    verifier_config = Path(authority["verifier_config"])
    verified = verify_approval(
        config_path=verifier_config, repo=root, request=request
    )
    if verified["authority_id"] != authority["authority_id"]:
        raise WorkflowControlError("verified authority does not match the source policy")
    updated = deepcopy(run)
    updated["approvals"][gate] = verified
    return updated


def assert_publish_authorized(run: dict[str, Any], root: Path) -> dict[str, Any]:
    validate_run(run, root)
    if run["runtime"]["execution_mode"] == "scheduled":
        raise WorkflowControlError("scheduled execution cannot publish")
    if run["stage"] != "publish_ready":
        raise WorkflowControlError("run is not publish_ready")
    approval = run["approvals"].get("publish")
    if not isinstance(approval, dict):
        raise WorkflowControlError("publish approval is missing")
    request = {
        "gate": "publish",
        "approval_ref": approval["approval_ref"],
        "reviewed_revision": approval["reviewed_revision"],
        "artifact_path": approval["artifact_path"],
        "artifact_sha256": approval["artifact_sha256"],
    }
    _, source_policy = load_source_policy(root, run["source_policy"]["path"])
    authority = source_policy["approval_authority"]
    expected_config = Path(authority["verifier_config"])
    recorded_config = Path(approval["verifier_config"])
    if recorded_config.resolve(strict=False) != expected_config.resolve(strict=False):
        raise WorkflowControlError("publish approval verifier does not match source policy")
    verified = verify_approval(config_path=expected_config, repo=root, request=request)
    if verified["authority_id"] != authority["authority_id"]:
        raise WorkflowControlError("verified authority does not match the source policy")
    return verified


def mark_published(run: dict[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    updated = deepcopy(run)
    updated["stage"] = "published"
    updated["publication"] = receipt
    updated["transition_history"].append({"from": "publish_ready", "to": "published"})
    return updated


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--run", required=True)
    init.add_argument("--workflow-id", required=True)
    init.add_argument("--run-id", required=True)
    init.add_argument("--policy", required=True)
    init.add_argument("--execution-mode", choices=("interactive", "scheduled"), required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("--run", required=True)
    commands.add_parser("validate-all")
    artifact = commands.add_parser("add-artifact")
    artifact.add_argument("--run", required=True)
    artifact.add_argument("--key", choices=tuple(ARTIFACT_BY_GATE.values()), required=True)
    artifact.add_argument("--path", required=True)
    advance = commands.add_parser("transition")
    advance.add_argument("--run", required=True)
    advance.add_argument("--to", choices=STAGES, required=True)
    approve = commands.add_parser("record-approval")
    approve.add_argument("--run", required=True)
    approve.add_argument("--gate", choices=tuple(ARTIFACT_BY_GATE), required=True)
    approve.add_argument("--approval-ref", required=True)
    approve.add_argument("--reviewed-revision", required=True)
    publish = commands.add_parser("can-publish")
    publish.add_argument("--run", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.command == "init":
            path = _run_path(root, args.run)
            if path.exists():
                raise WorkflowControlError("run state already exists")
            run = build_initial_run(
                root=root, workflow_id=args.workflow_id, run_id=args.run_id,
                policy_path=args.policy, execution_mode=args.execution_mode,
            )
            write_run(root, args.run, run)
            print(args.run)
            return 0
        if args.command == "validate-all":
            runs = discover_runs(root)
            for relative in runs:
                _, run = load_run(root, relative)
                validate_run(run, root)
            print(f"validated {len(runs)} schema-version-2 run(s)")
            return 0
        _, run = load_run(root, args.run)
        if args.command == "validate":
            validate_run(run, root)
            print(f"valid: {args.run}")
            return 0
        if args.command == "add-artifact":
            run = register_artifact(run, root=root, key=args.key, relative_path=args.path)
        elif args.command == "transition":
            run = transition(run, root=root, target_stage=args.to)
        elif args.command == "record-approval":
            run = record_verified_approval(
                run, root=root, gate=args.gate, approval_ref=args.approval_ref,
                reviewed_revision=args.reviewed_revision,
            )
        elif args.command == "can-publish":
            assert_publish_authorized(run, root)
            print(f"publish authorized: {args.run}")
            return 0
        write_run(root, args.run, run)
        print(args.run)
        return 0
    except (WorkflowControlError, ApprovalVerificationError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
