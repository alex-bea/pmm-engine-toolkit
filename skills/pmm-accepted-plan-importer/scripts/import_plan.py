#!/usr/bin/env python3
"""Create an accepted-plan ledger proposal; write only with --write."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path


def proposal(plan: Path, approver: str, accepted_on: str, tracker_role: str) -> dict:
    raw = plan.read_bytes()
    return {
        "plan": plan.name,
        "source": str(plan),
        "accepted_by": approver,
        "accepted_on": accepted_on,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "tracker_role": tracker_role,
        "tracker_write_approved": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--approver", required=True)
    parser.add_argument("--accepted-on", default=date.today().isoformat())
    parser.add_argument("--tracker-role", choices=["roadmap", "epic", "task", "reference-only"], default="epic")
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    record = proposal(args.plan, args.approver, args.accepted_on, args.tracker_role)
    if args.write:
        if not args.ledger:
            parser.error("--ledger is required with --write")
        records = []
        if args.ledger.exists():
            records = json.loads(args.ledger.read_text(encoding="utf-8"))
        if any(item.get("sha256") == record["sha256"] for item in records):
            parser.error("plan content already exists in ledger")
        records.append(record)
        args.ledger.parent.mkdir(parents=True, exist_ok=True)
        args.ledger.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
