#!/usr/bin/env python3
"""Preview, approve, and inspect receipt-bound Claude promotions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pmm_instinct_claude import (  # noqa: E402
    approve_promotion,
    create_promotion_preview,
    execute_promotion_receipts,
    promotion_counts,
    resolve_paths,
    start_detached_worker,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-root")
    parser.add_argument("--plugin-data")
    commands = parser.add_subparsers(dest="command", required=True)
    preview = commands.add_parser("preview")
    preview.add_argument("--instinct", required=True)
    preview.add_argument("--target", required=True)
    preview.add_argument("--destination-class", choices=("global", "project", "skill", "standard"), required=True)
    preview.add_argument("--delivery", choices=("local", "review"), required=True)
    preview.add_argument("--edited-rule")
    preview.add_argument("--edited-rationale")
    approve = commands.add_parser("approve")
    approve.add_argument("--preview-digest", required=True)
    approve.add_argument("--confirm", action="store_true")
    commands.add_parser("status")
    commands.add_parser("execute")
    args = parser.parse_args()
    paths = resolve_paths(args.state_root, plugin_data=args.plugin_data)
    try:
        if args.command == "preview":
            result = create_promotion_preview(
                paths,
                instinct_id=args.instinct,
                target=args.target,
                destination_class=args.destination_class,
                delivery=args.delivery,
                edited_rule=args.edited_rule,
                edited_rationale=args.edited_rationale,
            )
        elif args.command == "approve":
            result = approve_promotion(paths, args.preview_digest, confirm=args.confirm)
            start_detached_worker(paths, root=ROOT)
        elif args.command == "execute":
            result = execute_promotion_receipts(paths)
        else:
            result = promotion_counts(paths)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, PermissionError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
