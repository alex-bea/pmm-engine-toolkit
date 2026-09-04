#!/usr/bin/env python3
"""Claude Code PreToolUse adapter for the shared governance policy."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
from typing import Any

from governance_policy import (
    PolicyError,
    command_metadata,
    decide,
    decision_record,
    find_repo,
    load_policy,
)


def normalize(payload: dict[str, Any], repo: Path, policy: dict[str, Any]) -> dict[str, Any]:
    tool = str(payload.get("tool_name") or payload.get("toolName") or "")
    data = payload.get("tool_input") or payload.get("toolInput") or {}
    if not isinstance(data, dict):
        data = {}
    command = str(data.get("command") or "")
    operation, controlled, publisher_guard = command_metadata(command)
    paths = [
        value
        for key in (
            "file_path", "filePath", "notebook_path", "path", "target_path"
        )
        if isinstance((value := data.get(key)), str)
    ]
    return {
        "harness": "claude",
        "tool_name": tool,
        "command": command,
        "operation": operation,
        "controlled": controlled,
        "publisher_guard": publisher_guard,
        "target_paths": paths,
        "execution_mode": policy.get("execution_mode", "interactive"),
    }


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        if not isinstance(payload, dict):
            raise PolicyError("hook payload must be a mapping")
        start = Path(str(payload.get("cwd") or os.getcwd()))
        repo = find_repo(start)
        if repo is None:
            return 0
        _, policy = load_policy(repo)
        decision = decide(normalize(payload, repo, policy), policy, repo)
    except (json.JSONDecodeError, OSError, PolicyError, ValueError) as exc:
        print(f"GOV_HOOK_EVALUATION_FAILED: {exc}", file=sys.stderr)
        return 2
    print(decision_record(decision), file=sys.stderr)
    return 0 if decision.result == "allow" else 2


if __name__ == "__main__":
    raise SystemExit(main())
