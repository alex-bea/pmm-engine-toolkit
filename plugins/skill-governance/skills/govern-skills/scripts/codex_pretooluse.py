#!/usr/bin/env python3
"""Codex PreToolUse adapter for the shared governance policy."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
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
    tool = str(payload.get("tool_name") or payload.get("toolName") or payload.get("name") or "")
    data = payload.get("tool_input") or payload.get("toolInput") or payload.get("arguments") or {}
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            data = {"command": data}
    if not isinstance(data, dict):
        data = {}
    raw_command = str(data.get("cmd") or data.get("command") or "")
    command = raw_command if tool == "Bash" else ""
    patch_text = str(data.get("patch") or data.get("input") or "")
    if tool == "apply_patch" and not patch_text:
        patch_text = raw_command
    operation, controlled, publisher_guard = command_metadata(command)
    paths = [
        value
        for key in ("path", "file_path", "filePath", "target", "workdir")
        if isinstance((value := data.get(key)), str)
    ]
    paths.extend(
        match.group(1).strip()
        for match in re.finditer(
            r"^\*\*\* (?:Add|Update|Delete) File:\s*(.+)$",
            patch_text,
            re.MULTILINE,
        )
    )
    return {
        "harness": "codex",
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
