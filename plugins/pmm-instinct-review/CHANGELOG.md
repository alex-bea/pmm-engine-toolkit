# PMM Instinct Review changelog

## 0.3.0 — Draft

- Added a self-contained native Claude Code runtime while preserving the `0.2.0` Codex and
  portable adapters.
- Added a no-marketplace installer for symlink or pinned-copy use. It installs the nested
  personal skill and exactly one owned `SessionStart` and `SessionEnd` hook, while preserving
  unrelated Claude settings and adopter-owned state.
- Added disabled-by-default, consented Claude session capture with conversation-only
  normalization, bounded redaction, digest idempotence, and isolated local state.
- Added detached, exact-model Claude extraction with no tools, no session persistence, one
  maximum turn, strict JSON Schema validation, bounded retries, and stale-lease recovery.
- Added human-gated Claude review and exact promotion previews. A separately confirmed,
  immutable receipt may be executed in the background; local instruction updates are atomic,
  while governed destinations receive review patches rather than direct writes.
- Added a detailed Claude setup RUN and a complete fictional Northstar Reports lifecycle.

This candidate remains a draft until its pull request and release evidence are approved. It
does not auto-approve candidates, merge governed changes, publish content, or share Claude and
Codex state.

## 0.2.0

- Added automatic eligible-session capture and background extraction for Codex.
- Added isolated portable candidate import and review.
- Added ranked, bucketed review; exact matching; two-stage promotion; narrow retention; and
  fictional contract examples.
