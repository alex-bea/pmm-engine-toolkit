# PMM Instinct Review changelog

## 0.3.1 — Draft

- Closed two bounded public-Codex fidelity gaps against the private PMM Engine Codex path;
  this is not a port of the private Claude transaction architecture.
- First Codex enablement now requires a non-empty exact extractor model unless one is already
  persisted. New capture and backfill jobs use only that persisted model, never SessionEnd
  metadata. A legacy enabled store with no model skips capture as `unconfigured_model` without
  creating normalized evidence, an audit, or a queue job.
- Added adopter-owned `run_routes` for exact `references/RUN-*.md` selection and extended
  `voice_ref_routes` to accept either the existing string form or an ordered list of
  `references/REF-*.md` choices.
- Added fail-closed target selection: routes remain confined to discovered writable user-owned
  skill roots, ambiguous candidates return `multiple-eligible-targets`, and an owner must pass
  an exact eligible `promote --target` value before a preview is applicable.
- Preserved native Claude, portable, hook, normalization, extraction, review, retention, and
  existing promotion semantics apart from shared package-version references.

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
