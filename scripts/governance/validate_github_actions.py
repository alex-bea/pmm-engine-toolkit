#!/usr/bin/env python3
"""Validate the public GitHub Actions supply-chain and permission policy."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
EXPECTED_WORKFLOWS = {"ci.yml", "dependency-review.yml"}
PINNED_ACTIONS = {
    "actions/checkout": "3d3c42e5aac5ba805825da76410c181273ba90b1",
    "actions/setup-python": "5fda3b95a4ea91299a34e894583c3862153e4b97",
    "actions/dependency-review-action": "a1d282b36b6f3519aa1f3fc636f609c47dddb294",
}
USES_RE = re.compile(r"^\s*-?\s*uses:\s*([^@\s]+)@([^\s#]+)", re.MULTILINE)
WRITE_PERMISSION_RE = re.compile(r"^\s+[a-z][a-z-]*:\s*write\s*$", re.MULTILINE)
RUN_EVENT_CONTEXT_RE = re.compile(
    r"(?:run:\s*[^\n]*|run:\s*\|(?P<body>(?:\n\s+[^\n]+)+))",
    re.MULTILINE,
)


def validate_workflow(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    try:
        parsed = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return [f"{path.name}: invalid YAML: {exc}"]
    if not isinstance(parsed, dict):
        return [f"{path.name}: workflow root must be a mapping"]

    if "pull_request_target:" in text:
        errors.append(f"{path.name}: pull_request_target is prohibited")
    if "${{ secrets." in text:
        errors.append(f"{path.name}: CI workflows must not reference repository secrets")
    if not re.search(r"^permissions:\n\s+contents:\s+read\s*$", text, re.MULTILINE):
        errors.append(f"{path.name}: top-level permissions must set contents: read")
    if WRITE_PERMISSION_RE.search(text):
        errors.append(f"{path.name}: write permission is prohibited")
    if not re.search(r"^concurrency:\s*$", text, re.MULTILINE):
        errors.append(f"{path.name}: concurrency cancellation policy is required")
    if "runs-on: ubuntu-24.04" not in text:
        errors.append(f"{path.name}: jobs must use the fixed ubuntu-24.04 runner")

    job_count = len(re.findall(r"^\s{4}runs-on:\s+", text, re.MULTILINE))
    timeout_count = len(re.findall(r"^\s{4}timeout-minutes:\s+", text, re.MULTILINE))
    if job_count == 0 or timeout_count != job_count:
        errors.append(f"{path.name}: every job must declare timeout-minutes")

    for action, ref in USES_RE.findall(text):
        if action.startswith("./"):
            continue
        if not re.fullmatch(r"[0-9a-f]{40}", ref):
            errors.append(f"{path.name}: {action} is not pinned to a full commit SHA")
            continue
        expected = PINNED_ACTIONS.get(action)
        if expected is None:
            errors.append(f"{path.name}: unreviewed external action {action}")
        elif ref != expected:
            errors.append(f"{path.name}: {action} SHA differs from the reviewed pin")

    for match in RUN_EVENT_CONTEXT_RE.finditer(text):
        command = match.group(0)
        if "${{ github.event." in command:
            errors.append(f"{path.name}: untrusted event context must not be interpolated into run")

    if "actions/checkout@" in text and not re.search(
        r"actions/checkout@[0-9a-f]{40}[^\n]*\n(?:\s+[^\n]*\n){0,6}\s+persist-credentials:\s+false",
        text,
    ):
        errors.append(f"{path.name}: checkout must disable persisted credentials")
    return errors


def main() -> int:
    errors: list[str] = []
    actual = {path.name for path in WORKFLOW_DIR.glob("*.yml")}
    if actual != EXPECTED_WORKFLOWS:
        errors.append(
            f"workflow inventory mismatch: missing={sorted(EXPECTED_WORKFLOWS-actual)} "
            f"extra={sorted(actual-EXPECTED_WORKFLOWS)}"
        )
    for path in sorted(WORKFLOW_DIR.glob("*.yml")):
        errors.extend(validate_workflow(path))
    if errors:
        print("GitHub Actions validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(actual)} SHA-pinned, least-privilege workflows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

