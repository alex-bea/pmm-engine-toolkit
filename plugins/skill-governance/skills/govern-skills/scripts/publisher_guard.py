#!/usr/bin/env python3
"""Credential-isolated publisher guard for a publish-ready governed run."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable

from governance_control import (
    WorkflowControlError,
    assert_publish_authorized,
    load_run,
    mark_published,
    write_run,
)
from governance_policy import PolicyError, read_structured


Runner = Callable[..., subprocess.CompletedProcess[str]]


class PublisherError(PolicyError):
    """Raised when the publisher boundary is missing, invalid, or rejects a request."""


def _outside_repo(path: Path, repo: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(repo.resolve())
    except ValueError:
        return True
    return False


def load_publisher_config(path: Path, repo: Path) -> dict[str, Any]:
    if not path.is_absolute():
        raise PublisherError("publisher configuration path must be absolute")
    resolved = path.resolve(strict=False)
    if not _outside_repo(resolved, repo):
        raise PublisherError("publisher configuration must be outside the repository")
    if not resolved.is_file():
        raise PublisherError("publisher configuration is unavailable")
    data = read_structured(resolved)
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise PublisherError("publisher configuration schema_version must be 1")
    if data.get("enabled") is not True or data.get("approved") is not True:
        raise PublisherError("publisher adapter is not enabled and approved")
    command = data.get("command")
    if not isinstance(command, list) or not command or not all(isinstance(item, str) for item in command):
        raise PublisherError("publisher command must be a non-empty string list")
    if len(command) != 1:
        raise PublisherError(
            "publisher command must name one external executable; requests are supplied on stdin"
        )
    executable = Path(command[0])
    if not executable.is_absolute() or not _outside_repo(executable, repo):
        raise PublisherError("publisher executable must be absolute and outside the repository")
    if not executable.resolve(strict=False).is_file():
        raise PublisherError("publisher executable is unavailable")
    adapter_id = data.get("adapter_id")
    if not isinstance(adapter_id, str) or not adapter_id:
        raise PublisherError("adapter_id must be a non-empty string")
    operations = data.get("allowed_operations")
    if not isinstance(operations, list) or not operations or not all(
        isinstance(item, str) and item for item in operations
    ):
        raise PublisherError("allowed_operations must be a non-empty string list")
    timeout = data.get("timeout_seconds", 30)
    if not isinstance(timeout, int) or timeout < 1 or timeout > 120:
        raise PublisherError("timeout_seconds must be between 1 and 120")
    return data


def publish_run(
    *, root: Path, run_path: str, config_path: Path, operation: str,
    runner: Runner = subprocess.run,
) -> dict[str, Any]:
    config = load_publisher_config(config_path, root)
    if operation not in config["allowed_operations"]:
        raise PublisherError("publication operation is not approved")
    _, run = load_run(root, run_path)
    verified = assert_publish_authorized(run, root)
    staging = run["artifacts"]["staging"]
    request = {
        "run_id": run["run_id"],
        "operation": operation,
        "artifact_path": staging["path"],
        "artifact_sha256": staging["sha256"],
        "approval_ref": verified["approval_ref"],
    }
    try:
        completed = runner(
            config["command"], input=json.dumps(request, sort_keys=True), text=True,
            capture_output=True, timeout=config.get("timeout_seconds", 30), check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise PublisherError(f"publisher adapter failed: {exc}") from exc
    if completed.returncode != 0:
        raise PublisherError("publisher adapter rejected or failed the operation")
    try:
        response = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise PublisherError("publisher adapter returned invalid JSON") from exc
    if not isinstance(response, dict) or response.get("published") is not True:
        raise PublisherError("publisher adapter did not confirm publication")
    for field in ("run_id", "operation", "artifact_path", "artifact_sha256", "approval_ref"):
        if response.get(field) != request[field]:
            raise PublisherError(f"publisher response {field} does not match the request")
    receipt_id = response.get("receipt_id")
    published_at = response.get("published_at")
    if not isinstance(receipt_id, str) or not receipt_id:
        raise PublisherError("publisher receipt_id is missing")
    if not isinstance(published_at, str) or not published_at:
        raise PublisherError("publisher published_at is missing")
    try:
        parsed_time = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PublisherError("publisher published_at must be ISO-8601") from exc
    if parsed_time.utcoffset() is None:
        raise PublisherError("publisher published_at must include a timezone")
    receipt = {
        "operation": operation,
        "receipt_id": receipt_id,
        "published_at": published_at,
        "artifact_sha256": staging["sha256"],
    }
    write_run(root, run_path, mark_published(run, receipt))
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--run", required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--operation", required=True)
    args = parser.parse_args(argv)
    try:
        receipt = publish_run(
            root=args.repo.resolve(), run_path=args.run,
            config_path=args.config, operation=args.operation,
        )
        print(json.dumps(receipt, sort_keys=True))
        return 0
    except (PublisherError, WorkflowControlError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
