#!/usr/bin/env python3
"""Fail-closed protocol for an external human-approval verifier."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import subprocess
from typing import Any, Callable

from governance_policy import PolicyError, read_structured


Runner = Callable[..., subprocess.CompletedProcess[str]]


class ApprovalVerificationError(PolicyError):
    """Raised when external human authority cannot be established."""


def _outside_repo(path: Path, repo: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(repo.resolve())
    except ValueError:
        return True
    return False


def load_verifier_config(path: Path, repo: Path) -> dict[str, Any]:
    if not path.is_absolute():
        raise ApprovalVerificationError("verifier configuration path must be absolute")
    resolved = path.resolve(strict=False)
    if not _outside_repo(resolved, repo):
        raise ApprovalVerificationError("verifier configuration must be outside the repository")
    if not resolved.is_file():
        raise ApprovalVerificationError("verifier configuration is unavailable")
    data = read_structured(resolved)
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ApprovalVerificationError("verifier configuration schema_version must be 1")
    if data.get("enabled") is not True:
        raise ApprovalVerificationError("approval verifier is not enabled")
    command = data.get("command")
    if not isinstance(command, list) or not command or not all(isinstance(item, str) for item in command):
        raise ApprovalVerificationError("verifier command must be a non-empty string list")
    if len(command) != 1:
        raise ApprovalVerificationError(
            "verifier command must name one external executable; requests are supplied on stdin"
        )
    executable = Path(command[0])
    if not executable.is_absolute() or not _outside_repo(executable, repo):
        raise ApprovalVerificationError("verifier executable must be absolute and outside the repository")
    if not executable.resolve(strict=False).is_file():
        raise ApprovalVerificationError("verifier executable is unavailable")
    reviewers = data.get("authorized_reviewers")
    if not isinstance(reviewers, list) or not reviewers or not all(
        isinstance(item, str) and item for item in reviewers
    ):
        raise ApprovalVerificationError("authorized_reviewers must be a non-empty string list")
    timeout = data.get("timeout_seconds", 10)
    if not isinstance(timeout, int) or timeout < 1 or timeout > 60:
        raise ApprovalVerificationError("timeout_seconds must be between 1 and 60")
    authority_id = data.get("authority_id")
    if not isinstance(authority_id, str) or not authority_id:
        raise ApprovalVerificationError("authority_id must be a non-empty string")
    return data


def _nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ApprovalVerificationError(f"{label} must be a non-empty string")
    return value.strip()


def verify_approval(
    *,
    config_path: Path,
    repo: Path,
    request: dict[str, Any],
    runner: Runner = subprocess.run,
) -> dict[str, Any]:
    config = load_verifier_config(config_path, repo)
    try:
        completed = runner(
            config["command"],
            input=json.dumps(request, sort_keys=True),
            text=True,
            capture_output=True,
            timeout=config.get("timeout_seconds", 10),
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ApprovalVerificationError(f"approval verifier failed: {exc}") from exc
    if completed.returncode != 0:
        raise ApprovalVerificationError("approval verifier rejected or could not verify the request")
    try:
        response = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ApprovalVerificationError("approval verifier returned invalid JSON") from exc
    if not isinstance(response, dict) or response.get("verified") is not True:
        raise ApprovalVerificationError("approval authority did not return verified=true")
    if response.get("decision") != "approved":
        raise ApprovalVerificationError("approval authority decision is not approved")
    for field in (
        "gate",
        "approval_ref",
        "reviewed_revision",
        "artifact_path",
        "artifact_sha256",
    ):
        expected = _nonempty(request.get(field), f"request.{field}")
        if response.get(field) != expected:
            raise ApprovalVerificationError(f"verified {field} does not match the request")
    approver = _nonempty(response.get("approver"), "response.approver")
    if approver not in config["authorized_reviewers"]:
        raise ApprovalVerificationError("verified approver is not authorized")
    if response.get("authority_id") != config["authority_id"]:
        raise ApprovalVerificationError("verified authority_id does not match configuration")
    approved_at = _nonempty(response.get("approved_at"), "response.approved_at")
    try:
        parsed_time = datetime.fromisoformat(approved_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ApprovalVerificationError("verified approved_at must be ISO-8601") from exc
    if parsed_time.utcoffset() is None:
        raise ApprovalVerificationError("verified approved_at must include a timezone")
    return {
        "decision": "approved",
        "gate": response["gate"],
        "approver": approver,
        "approval_ref": response["approval_ref"],
        "reviewed_revision": response["reviewed_revision"],
        "artifact_path": response["artifact_path"],
        "artifact_sha256": response["artifact_sha256"],
        "approved_at": approved_at,
        "authority_id": response["authority_id"],
        "verifier_config": str(config_path.resolve()),
    }
