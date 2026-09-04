# PMM Instinct Review state contracts

These public contracts describe adopter-owned state. Bundled examples are inert and are never
loaded as live state by default. JSON is UTF-8 and pretty-printed unless the contract is JSONL;
Markdown fields are UTF-8. Runtime-created files use owner-only permissions where supported.

## Configuration

`config.json` follows `config-template.json`. `enabled` defaults to `false`; first Codex
enablement requires `privacy_acknowledged_at`. Limits are positive integers. `retention` is
`until_reviewed`. `extractor_model: null` means the eligible Codex session model is required,
not that a fallback model may be chosen. `voice_ref_routes` is an adopter-owned mapping from a
discovered skill slug to one relative `REF-*.md` path.

## Normalized evidence JSONL

Each line has exactly `index` (positive integer), `role` (`user` or `assistant`), and `text`
(redacted non-empty string). Only eligible chat turns appear. Context wrappers, tools,
reasoning, world state, and native-system records do not. The configured turn and total
character ceilings apply before persistence.

## Audit Markdown

An audit filename begins with `YYYY-MM-DD-HHMM-` and ends in `-audit.md`. It records
`processed`, `session_id`, `user_messages`, `transcript_path`, `normalized_transcript_path`,
`suggestions_path`, `source_runtime`, `source_transcript_format`, `cwd`, `skill`, and `model`.
The native transcript is read-only. `processed: true` means every candidate from that audit—or
the explicitly confirmed zero-candidate bucket—has a decision.

## Queue JSON

Queue records contain `session_id`, `state`, `attempts`, `extractor_model`, evidence/audit/
suggestion paths, source metadata, timestamps, recovery state, candidate count, and a sanitized
error. States are `queued`, `running`, `succeeded`, or `failed`. A stale `running` job may be
retried until `max_attempts`; zero candidates is a successful result.

## Suggestion Markdown

The header records `session_id`, `skill`, and `candidates`. Every `## Candidate N` records
`type`, `rule`, `evidence`, `context`, and `why it matters`. Types are `correction`,
`confirmation`, `voice`, `scope`, or `workflow`. At most five candidates are accepted. The
rationale is required and no longer than 300 characters.

## Review ledger

`state/review-decisions.json` maps a type-aware cluster ID to the decision, covered session
IDs, review timestamp, and optional instinct path. This ledger prevents a multi-candidate
audit from losing its normalized evidence before every candidate has a decision.

## Priority snapshot JSON

`sessions/instinct-priority.json` is created only by `snapshot-priority`. It records schema and
generation metadata, all three backlog buckets, active/promotion/stale instinct counts, the
priority summary, voice-first areas, and complete serialized clusters. Cluster fields include
type, normalized rule, area, evidence/rationale, support, source skills, repositories/cwds,
first/last seen, score/tier, and `new` or `exact` match state. `list-priority` returns the same
live report without writing this file.

## Instinct Markdown

Use `instinct-template.md`. Status values are `active`, `promoted`, or `covered`. Only active
instincts with confidence at least `0.5` enter the default promotion queue. Support bands are
`0.30` for 1–2, `0.50` for 3–5, `0.70` for 6–10, and `0.85` for 11+. An explicitly strong
correction adds `0.05`; an explicit contradiction subtracts `0.10`. Missing `0.1.0` fields
receive conservative in-memory defaults and are not written by status.

## Promotion preview JSON

`state/promotion-preview-{instinct-id}.json` stores a signature and timestamp for the exact
instinct, destination class, rule, rationale, insertion, and target paths shown to the owner.
Apply recomputes the preview and refuses a mismatch. Destination files are staged before
replacement. `promotion_outcome` and `status` become `promoted` when at least one insertion is
written, or `covered` when every target already contains the normalized rule.

## Status and installation receipts

Status is a read-only JSON object containing adapter, capture support, config, queue counts,
three-bucket backlog summary, active/promotion/stale instinct counts, snapshot path, store, and
capture preflight or its explicit non-applicability. Installation/enablement receipts contain
the selected adapter, state root, disabled/default state, consent timestamp when present,
preflight checks, and whether state is preserved on disable or removal.
