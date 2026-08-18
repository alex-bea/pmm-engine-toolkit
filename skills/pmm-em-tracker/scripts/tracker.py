#!/usr/bin/env python3
"""Validate a compact roadmap/epic/task tracker stored as YAML or JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


STATUSES = {"icebox", "todo", "active", "blocked", "done"}


def load(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise ValueError("YAML input requires PyYAML; JSON works without dependencies") from exc
        data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("tracker root must be a mapping")
    return data


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    roadmaps = {item.get("id") for item in data.get("roadmaps", []) if isinstance(item, dict)}
    epics = {item.get("id"): item for item in data.get("epics", []) if isinstance(item, dict)}
    seen: set[str] = set()
    for kind in ("roadmaps", "epics", "tasks"):
        for item in data.get(kind, []):
            if not isinstance(item, dict) or not item.get("id") or not item.get("title"):
                errors.append(f"{kind}: every record needs id and title")
                continue
            if item["id"] in seen:
                errors.append(f"duplicate id: {item['id']}")
            seen.add(item["id"])
    for epic_id, epic in epics.items():
        if epic.get("roadmap") not in roadmaps:
            errors.append(f"{epic_id}: unknown roadmap {epic.get('roadmap')}")
    for task in data.get("tasks", []):
        if not isinstance(task, dict) or not task.get("id"):
            continue
        if task.get("epic") not in epics:
            errors.append(f"{task['id']}: unknown epic {task.get('epic')}")
        if task.get("status") not in STATUSES:
            errors.append(f"{task['id']}: invalid status {task.get('status')}")
        criteria = task.get("acceptance_criteria")
        if not isinstance(criteria, list) or not criteria:
            errors.append(f"{task['id']}: acceptance_criteria must be a non-empty list")
        if task.get("status") == "blocked" and not task.get("blocked_reason"):
            errors.append(f"{task['id']}: blocked task needs blocked_reason")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate"])
    parser.add_argument("tracker", type=Path)
    args = parser.parse_args()
    errors = validate(load(args.tracker))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Tracker is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
