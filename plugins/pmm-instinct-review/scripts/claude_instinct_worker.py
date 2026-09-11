#!/usr/bin/env python3
"""Drain native Claude extraction jobs and approved promotion receipts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pmm_instinct_claude import (  # noqa: E402
    drain_capture_requests,
    drain_extraction_queue,
    execute_promotion_receipts,
    reconcile_review_finalizations,
    refresh_runtime_summary,
    resolve_paths,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-root")
    parser.add_argument("--plugin-data")
    parser.add_argument("--drain", action="store_true", required=True)
    parser.add_argument("--job")
    parser.add_argument("--claude-binary")
    args = parser.parse_args()
    paths = resolve_paths(args.state_root, plugin_data=args.plugin_data)
    capture = drain_capture_requests(paths)
    reconciliation = reconcile_review_finalizations(paths)
    extraction = drain_extraction_queue(paths, job_id=args.job, claude_binary=args.claude_binary)
    promotion = execute_promotion_receipts(paths)
    summary = refresh_runtime_summary(paths)
    print(json.dumps({
        "capture": capture,
        "reconciliation": reconciliation,
        "extraction": extraction,
        "promotion": promotion,
        "summary": summary,
    }, sort_keys=True))
    healthy = all(
        result["status"] in {"complete", "locked"}
        for result in (capture, reconciliation, extraction, promotion)
    )
    return 0 if healthy else 1


if __name__ == "__main__":
    raise SystemExit(main())
