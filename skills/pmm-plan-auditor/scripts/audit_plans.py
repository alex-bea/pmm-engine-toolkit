#!/usr/bin/env python3
"""Report plan-to-tracker mapping drift without modifying files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FIELD = re.compile(r"^(tracker_id|tracker_role|status):\s*[\"']?([^\"'\n]+)", re.MULTILINE)


def load_tracker(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise ValueError("YAML input requires PyYAML; JSON works without dependencies") from exc
        return yaml.safe_load(text)


def audit(plans_dir: Path, tracker: dict) -> list[dict[str, str]]:
    ids = {item.get("id") for key in ("roadmaps", "epics", "tasks") for item in tracker.get(key, [])}
    findings: list[dict[str, str]] = []
    for plan in sorted(plans_dir.glob("*.md")):
        fields = dict(FIELD.findall(plan.read_text(encoding="utf-8")))
        tracker_id = fields.get("tracker_id", "").strip()
        role = fields.get("tracker_role", "").strip()
        if not role:
            findings.append({"plan": plan.name, "finding": "missing tracker_role"})
        elif role != "reference-only" and (not tracker_id or tracker_id == "[Missing]"):
            findings.append({"plan": plan.name, "finding": "missing tracker_id"})
        elif role != "reference-only" and tracker_id not in ids:
            findings.append({"plan": plan.name, "finding": f"unknown tracker_id {tracker_id}"})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plans_dir", type=Path)
    parser.add_argument("tracker", type=Path)
    args = parser.parse_args()
    findings = audit(args.plans_dir, load_tracker(args.tracker))
    print(json.dumps(findings, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
