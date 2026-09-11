#!/usr/bin/env python3
"""Fast SessionStart/SessionEnd bridge for the self-contained Claude runtime."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pmm_instinct_claude import (  # noqa: E402
    atomic_write_text,
    ensure_store,
    queue_capture_request,
    read_runtime_summary,
    resolve_paths,
    start_detached_worker,
)


def _payload() -> dict[str, object]:
    try:
        value = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def _marker(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "-", value)[:100] or "unknown"


def session_end(payload: dict[str, object], *, state_root: str | Path | None = None) -> int:
    session_id = str(payload.get("session_id") or "").strip()
    transcript = str(payload.get("transcript_path") or "").strip()
    if not session_id or not transcript:
        return 0
    try:
        paths = resolve_paths(state_root)
        result = queue_capture_request(paths, payload)
        if result.get("status") in {"queued", "exists"}:
            start_detached_worker(paths, root=ROOT)
    except (OSError, ValueError):
        return 0
    return 0


def session_start(payload: dict[str, object], *, state_root: str | Path | None = None) -> int:
    try:
        paths = resolve_paths(state_root)
        if not paths.state_root.exists():
            return 0
        ensure_store(paths, create_config=False)
        start_detached_worker(paths, root=ROOT, force=True)
        summary = read_runtime_summary(paths)
    except (OSError, ValueError):
        return 0
    pending = summary["pending_extraction"]
    ready = summary["review_ready"]
    promotion_pending = summary["pending_promotion"]
    if pending + ready + promotion_pending <= 0:
        return 0
    session_id = _marker(str(payload.get("session_id") or "unknown"))
    marker = paths.state / f"briefed-{session_id}"
    if marker.is_symlink() or marker.exists():
        return 0
    atomic_write_text(marker, "briefed\n")
    context = (
        f"PMM Instinct Review background snapshot ({summary['updated_at']}): "
        f"{pending} extraction job(s) pending, {ready} extracted session(s) "
        f"ready for human review, and {promotion_pending} approved promotion receipt(s) pending execution. "
        "No candidate or promotion is approved automatically."
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))
    return 0


def main() -> int:
    args = sys.argv[1:]
    state_root: str | None = None
    if len(args) == 3 and args[0] == "--state-root":
        state_root, event = args[1], args[2]
    elif len(args) == 1:
        event = args[0]
    else:
        print("usage: claude_instinct_hook.py [--state-root PATH] session-start|session-end", file=sys.stderr)
        return 2
    if event not in {"session-start", "session-end"}:
        return 2
    return session_start(_payload(), state_root=state_root) if event == "session-start" else session_end(_payload(), state_root=state_root)


if __name__ == "__main__":
    raise SystemExit(main())
