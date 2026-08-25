#!/usr/bin/env python3
"""Operate the portable Codex instinct-review lifecycle."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pmm_instinct.runtime import (
    apply_backfill,
    apply_promotion,
    backlog,
    capture_session,
    cleanup_processed,
    discover_backfill,
    drain_queue,
    import_candidates,
    iso_now,
    load_config,
    preflight,
    promotion_preview,
    resolve_paths,
    retry_failed,
    resolve_zero_candidate_audits,
    review_cluster,
    runtime_status,
    safe_session_id,
    start_detached_worker,
    update_config,
)


CLI_PATH = Path(__file__).resolve()


def _json(payload: object) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _read_hook_payload() -> dict[str, object]:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _session_end(paths) -> int:
    payload = _read_hook_payload()
    session_id = str(payload.get("session_id") or payload.get("id") or "").strip()
    transcript_path = str(payload.get("transcript_path") or "").strip()
    if not session_id or not transcript_path:
        return 0
    try:
        result = capture_session(
            paths,
            session_id=session_id,
            transcript_path=transcript_path,
            cwd=str(payload.get("cwd") or ""),
            model=str(payload.get("model") or ""),
        )
        if result.get("status") == "queued":
            start_detached_worker(paths, CLI_PATH)
    except Exception:
        # Hooks are advisory and must never block the user's session lifecycle.
        return 0
    return 0


def _session_start(paths) -> int:
    payload = _read_hook_payload()
    try:
        start_detached_worker(paths, CLI_PATH)
        pending = int(backlog(paths)["positive_suggestions"])
        session_id = safe_session_id(str(payload.get("session_id") or payload.get("id") or "unknown"))
        marker = paths.state / f"briefed-{session_id}"
        if pending > 0 and not marker.exists():
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text(iso_now() + "\n", encoding="utf-8")
            _json(
                {
                    "additionalContext": (
                        f"PMM Instinct Review has {pending} unreviewed suggestion"
                        f"{'s' if pending != 1 else ''}. Invoke $pmm-instinct-review to review them."
                    )
                }
            )
    except Exception:
        return 0
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", help="Override ~/.codex (useful for tests and isolated installs).")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("status", help="Show capture, queue, review, and promotion status.")

    enable = commands.add_parser("on", help="Enable capture after the privacy acknowledgment.")
    enable.add_argument("--acknowledge-local-chat-storage", action="store_true")
    enable.add_argument("--model", help="Override the SessionEnd model for every extraction.")
    enable.add_argument("--codex-binary", help="Persist an explicit Codex executable path.")
    commands.add_parser("off", help="Disable new capture while preserving state.")

    backfill = commands.add_parser("backfill", help="Inventory or capture recent eligible sessions.")
    backfill.add_argument("--limit", type=int, default=5)
    backfill.add_argument("--older-than-minutes", type=int, default=30)
    backfill_mode = backfill.add_mutually_exclusive_group(required=True)
    backfill_mode.add_argument("--dry-run", action="store_true")
    backfill_mode.add_argument("--apply", action="store_true")

    worker = commands.add_parser("worker", help="Drain the extraction queue.")
    worker_mode = worker.add_mutually_exclusive_group(required=True)
    worker_mode.add_argument("--drain", action="store_true")
    worker_mode.add_argument("--session")
    worker.add_argument("--codex-binary")

    retry = commands.add_parser("retry", help="Requeue failed extraction jobs.")
    retry.add_argument("--session")
    commands.add_parser("cleanup", help="Remove normalized transcripts for processed audits.")
    commands.add_parser("list-priority", help="List ranked unreviewed suggestion clusters.")
    resolve_zero = commands.add_parser("resolve-zero", help="Mark zero-candidate audits reviewed.")
    resolve_zero.add_argument("--confirm", action="store_true")

    review = commands.add_parser("review", help="Apply one explicit review decision.")
    review.add_argument("--cluster", required=True)
    review.add_argument("--decision", choices=("accept", "reject", "edit", "match"), required=True)
    review.add_argument("--edited-rule")
    review.add_argument("--confirm", action="store_true")

    promote = commands.add_parser("promote", help="Preview or apply one instinct promotion.")
    promote.add_argument("--instinct", required=True)
    promote.add_argument("--destination", choices=("project", "global", "both", "skill", "edit", "no"))
    promote.add_argument("--project")
    promote.add_argument("--edited-rule")
    promote.add_argument("--apply", action="store_true")
    promote.add_argument("--confirm", action="store_true")

    importer = commands.add_parser("import-candidates", help="Import legacy explicit candidate JSON.")
    importer.add_argument("candidate_file", type=Path)
    importer.add_argument("--cwd", default="")
    importer.add_argument("--confirm", action="store_true")

    hook = commands.add_parser("hook", help=argparse.SUPPRESS)
    hook.add_argument("event", choices=("session-start", "session-end"))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    paths = resolve_paths(args.codex_home)
    try:
        if args.command == "hook":
            return _session_start(paths) if args.event == "session-start" else _session_end(paths)
        if args.command == "status":
            _json(runtime_status(paths))
            return 0
        if args.command == "on":
            config = load_config(paths, create=True)
            if not config.get("privacy_acknowledged_at") and not args.acknowledge_local_chat_storage:
                raise PermissionError("first enablement requires --acknowledge-local-chat-storage")
            proposed = {}
            if args.model is not None:
                proposed["extractor_model"] = args.model.strip() or None
            if args.codex_binary is not None:
                proposed["codex_binary"] = args.codex_binary
            if proposed:
                update_config(paths, **proposed)
            receipt = preflight(paths, codex_binary=args.codex_binary)
            if not receipt["ok"]:
                raise RuntimeError(f"enablement preflight failed: {receipt['checks']}")
            updates = {"enabled": True}
            if not config.get("privacy_acknowledged_at"):
                updates["privacy_acknowledged_at"] = iso_now()
            updated = update_config(paths, **updates)
            _json({"enabled": updated["enabled"], "privacy_acknowledged_at": updated["privacy_acknowledged_at"], "preflight": receipt})
            return 0
        if args.command == "off":
            _json({"enabled": update_config(paths, enabled=False)["enabled"], "state_preserved": True})
            return 0
        if args.command == "backfill":
            inventory = discover_backfill(paths, limit=max(0, args.limit), older_than_minutes=max(0, args.older_than_minutes))
            _json({"inventory": inventory, "applied": apply_backfill(paths, inventory) if args.apply else []})
            return 0
        if args.command == "worker":
            result = drain_queue(paths, session_id=args.session, codex_binary=args.codex_binary)
            _json(result)
            return 0 if result["status"] in {"complete", "locked"} else 1
        if args.command == "retry":
            count = retry_failed(paths, args.session)
            _json({"requeued": count, "session_id": args.session})
            return 0
        if args.command == "cleanup":
            _json(cleanup_processed(paths))
            return 0
        if args.command == "list-priority":
            _json(backlog(paths))
            return 0
        if args.command == "resolve-zero":
            _json(resolve_zero_candidate_audits(paths, confirm=args.confirm))
            return 0
        if args.command == "review":
            _json(
                review_cluster(
                    paths,
                    args.cluster,
                    args.decision,
                    edited_rule=args.edited_rule,
                    confirm=args.confirm,
                )
            )
            return 0
        if args.command == "promote":
            kwargs = {
                "destination": args.destination,
                "project": args.project,
                "edited_rule": args.edited_rule,
            }
            if args.apply:
                _json(apply_promotion(paths, args.instinct, confirm=args.confirm, **kwargs))
            else:
                _json(promotion_preview(paths, args.instinct, **kwargs))
            return 0
        if args.command == "import-candidates":
            _json(import_candidates(paths, args.candidate_file, cwd=args.cwd, confirm=args.confirm))
            return 0
    except (FileNotFoundError, json.JSONDecodeError, PermissionError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
