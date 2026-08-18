#!/usr/bin/env python3
"""Render a deterministic plan skeleton to stdout or a new local file."""

from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATE = """---
title: "{title}"
status: draft
tracker_role: {tracker_role}
tracker_id: "[Missing]"
---

# Objective

{objective}

# Non-goals

- [Missing]

# Evidence

- [Missing]

# MVP scope

- [Missing]

# Deferred scope

- [Missing]

# Milestones and acceptance criteria

- [Missing]

# Risks and dependencies

- [Missing]

# Ownership and decisions

- Owner: [Missing]
"""


def render(title: str, objective: str, tracker_role: str) -> str:
    return TEMPLATE.format(title=title, objective=objective, tracker_role=tracker_role)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--tracker-role", choices=["roadmap", "epic", "task", "reference-only"], default="epic")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = render(args.title, args.objective, args.tracker_role)
    if args.output:
        if args.output.exists():
            parser.error(f"refusing to overwrite {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(args.output)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
