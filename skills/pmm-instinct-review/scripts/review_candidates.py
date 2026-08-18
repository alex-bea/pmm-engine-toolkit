#!/usr/bin/env python3
"""Validate and rank local lesson candidates without promoting them."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = {"id", "lesson", "source", "observed_on", "evidence"}


def review(records: list[dict]) -> tuple[list[dict], list[str]]:
    valid: list[dict] = []
    errors: list[str] = []
    for index, record in enumerate(records):
        missing = REQUIRED - set(record)
        if missing:
            errors.append(f"record {index}: missing {sorted(missing)}")
            continue
        evidence = record.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{record['id']}: evidence must be a non-empty list")
            continue
        scored = dict(record)
        scored["evidence_count"] = len(evidence)
        scored["promotion_status"] = "review-required"
        valid.append(scored)
    valid.sort(key=lambda item: (-item["evidence_count"], item["id"]))
    return valid, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidates", type=Path)
    args = parser.parse_args()
    records = json.loads(args.candidates.read_text(encoding="utf-8"))
    valid, errors = review(records)
    print(json.dumps({"candidates": valid, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
