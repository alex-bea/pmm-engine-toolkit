#!/usr/bin/env python3
"""Configure and inspect the self-contained native Claude instinct runtime."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pmm_instinct_claude import (  # noqa: E402
    load_config,
    resolve_paths,
    retry_failed,
    runtime_status,
    start_detached_worker,
    update_config,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-root")
    parser.add_argument("--plugin-data")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    enable = commands.add_parser("on")
    enable.add_argument("--acknowledge-privacy", action="store_true")
    enable.add_argument("--model")
    enable.add_argument("--claude-binary")
    commands.add_parser("off")
    retry = commands.add_parser("retry")
    retry.add_argument("--job")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        paths = resolve_paths(args.state_root, plugin_data=args.plugin_data)
        if args.command == "status":
            print(json.dumps(runtime_status(paths), indent=2, sort_keys=True))
            return 0
        if args.command == "off":
            update_config(paths, enabled=False)
            print(json.dumps({"enabled": False, "state_preserved": True}, sort_keys=True))
            return 0
        if args.command == "retry":
            count = retry_failed(paths, job_id=args.job)
            if count:
                start_detached_worker(paths, root=ROOT)
            print(json.dumps({"requeued": count}, sort_keys=True))
            return 0
        if not args.acknowledge_privacy:
            raise PermissionError("--acknowledge-privacy is required before capture can be enabled")
        current = load_config(paths, create=True)
        updates: dict[str, object] = {
            "enabled": True,
            "privacy_acknowledged_at": current.get("privacy_acknowledged_at")
            or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        if args.model:
            updates["extractor_model"] = args.model
        if args.claude_binary:
            updates["claude_binary"] = args.claude_binary
        update_config(paths, **updates)
        status = runtime_status(paths)
        if not status["claude_binary"]:
            update_config(paths, enabled=False)
            raise RuntimeError("Claude Code executable is unavailable; capture remains disabled")
        print(json.dumps(status, indent=2, sort_keys=True))
        return 0
    except (OSError, PermissionError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
