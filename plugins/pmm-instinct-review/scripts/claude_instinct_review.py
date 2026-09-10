#!/usr/bin/env python3
"""List and apply human-gated Claude instinct review decisions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pmm_instinct_claude import resolve_paths, resolve_zero_candidates, review_backlog, review_cluster  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-root")
    parser.add_argument("--plugin-data")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list-priority")
    zero = commands.add_parser("resolve-zero")
    zero.add_argument("--confirm", action="store_true")
    review = commands.add_parser("review")
    review.add_argument("--cluster", required=True)
    review.add_argument("--decision", choices=("accept", "reject", "edit", "match"), required=True)
    review.add_argument("--edited-rule")
    review.add_argument("--edited-rationale")
    review.add_argument("--strong-correction", action="store_true")
    review.add_argument("--contradicted", action="store_true")
    review.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    paths = resolve_paths(args.state_root, plugin_data=args.plugin_data)
    try:
        if args.command == "list-priority":
            result = review_backlog(paths)
        elif args.command == "resolve-zero":
            result = resolve_zero_candidates(paths, confirm=args.confirm)
        else:
            result = review_cluster(
                paths,
                args.cluster,
                args.decision,
                confirm=args.confirm,
                edited_rule=args.edited_rule,
                edited_rationale=args.edited_rationale,
                strong_correction=args.strong_correction,
                contradicted=args.contradicted,
            )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, PermissionError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
