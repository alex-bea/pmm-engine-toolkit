#!/usr/bin/env python3
"""Unified PreToolUse entrypoint for the shared governance policy."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

import claude_pretooluse
import codex_pretooluse
from governance_policy import (
    PolicyError,
    decide,
    decision_record,
    find_repo,
    load_policy,
)


SUPPORTED_HARNESSES = {"claude", "codex"}
CLAUDE_TOOL_NAMES = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
CODEX_TOOL_NAMES = {"apply_patch"}


def detect_harness(
    payload: dict[str, Any], explicit: str | None = None
) -> str:
    """Resolve one harness from trusted configuration or unambiguous payload shape."""
    candidates: list[tuple[str, str]] = []
    for source, value in (
        ("argument", explicit),
        ("environment", os.environ.get("GOVERNANCE_HARNESS")),
        ("payload", payload.get("harness")),
    ):
        if value is None or value == "":
            continue
        normalized = str(value).strip().lower()
        if normalized not in SUPPORTED_HARNESSES:
            raise PolicyError(f"unsupported {source} harness: {normalized}")
        candidates.append((source, normalized))
    configured = {value for _, value in candidates}
    if len(configured) > 1:
        raise PolicyError("conflicting harness identifiers")
    if configured:
        return configured.pop()

    tool = str(
        payload.get("tool_name")
        or payload.get("toolName")
        or payload.get("name")
        or ""
    )
    claude_signal = bool(
        {"tool_use_id", "transcript_path", "permission_mode"} & payload.keys()
        or tool in CLAUDE_TOOL_NAMES
    )
    codex_signal = bool(
        {"name", "arguments"} & payload.keys()
        or tool in CODEX_TOOL_NAMES
    )
    if claude_signal == codex_signal:
        raise PolicyError("hook payload does not identify exactly one supported harness")
    return "claude" if claude_signal else "codex"


def normalize(
    payload: dict[str, Any], harness: str, repo: Path, policy: dict[str, Any]
) -> dict[str, Any]:
    if harness == "claude":
        return claude_pretooluse.normalize(payload, repo, policy)
    if harness == "codex":
        return codex_pretooluse.normalize(payload, repo, policy)
    raise PolicyError(f"unsupported harness: {harness}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--harness", choices=sorted(SUPPORTED_HARNESSES))
    args = parser.parse_args(argv)
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        if not isinstance(payload, dict):
            raise PolicyError("hook payload must be a mapping")
        start = Path(str(payload.get("cwd") or os.getcwd()))
        repo = find_repo(start)
        if repo is None:
            return 0
        _, policy = load_policy(repo)
        harness = detect_harness(payload, args.harness)
        request = normalize(payload, harness, repo, policy)
        decision = decide(request, policy, repo)
    except (json.JSONDecodeError, OSError, PolicyError, ValueError) as exc:
        print(f"GOV_HOOK_EVALUATION_FAILED: {exc}", file=sys.stderr)
        return 2
    print(decision_record(decision), file=sys.stderr)
    return 0 if decision.result == "allow" else 2


if __name__ == "__main__":
    raise SystemExit(main())
