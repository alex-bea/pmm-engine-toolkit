# PMM Instinct Review state contracts

These contracts describe adopter-owned runtime state. Bundled examples are inert and are
never loaded as live state. JSON is UTF-8 and pretty-printed unless stated otherwise. The
runtime uses private directories and files (`0700` and `0600` where supported). Promotion
preserves an existing destination's permission mode and creates a new destination as `0600`.

## Store isolation

| Mode | State root | Native history | Other stores |
|---|---|---|---|
| Claude standalone | `~/.claude/pmm-instinct-review-data/` | Read-only | Never reads Codex, legacy Claude review, or plugin state |
| Claude local plugin | `${CLAUDE_PLUGIN_DATA}/instinct-review/` | Read-only | Uses plugin data when present; never infers a home-directory store |
| Codex | `~/.codex/instinct-review/` | Read-only | Never reads Claude state |
| Portable | Required explicit `--state-root` | Never read | Native-agent and installed-package roots are refused |

Mutable state may not live in the installed package or plugin cache. Disable and uninstall
preserve it. Deleting a state root is a separate user-controlled data action.

Resolution order is an explicit command root, `${CLAUDE_PLUGIN_DATA}/instinct-review/`, then
an explicitly configured `PMM_INSTINCT_STATE_ROOT`. With none of those inputs, resolution
fails; there is no ambient `~/.claude/` fallback.

## Claude configuration

Claude `config.json` starts from package-root `assets/claude-config-template.json`:

- `schema_version`: `1`;
- `enabled`: `false` until the explicit acknowledgement command;
- `privacy_acknowledged_at`: `null` until first consent;
- `min_user_messages`: `5`;
- `max_turns`: `200`;
- `max_normalized_chars`: `120000`;
- `max_attempts`: `3`;
- `processing_lease_seconds`: `900`;
- `extractor_model`: the exact configured Claude model, initially `sonnet`;
- `extractor_timeout_seconds`: `900`; and
- `claude_binary`: optional explicit executable path, initially `null`.

Status does not enable capture. First `on` requires `--acknowledge-privacy` and a resolvable
Claude executable. No model fallback is allowed.

## Claude state tree

```text
<claude-state-root>/
├── config.json
├── capture-inbox/{request-id}.json
├── sessions/
│   ├── YYYY-MM-DD-HHMM-{job-id}-audit.md
│   ├── {job-id}-evidence.json
│   └── {job-id}-suggestions.md
├── queue/{job-id}.json
├── instincts/pmm-instinct-YYYY-MM-DD-NNN.md
├── logs/{job-id}.log
├── promotion-receipts/{receipt-digest}.json
├── promotion-outcomes/{receipt-digest}.json
├── promotion-changesets/{receipt-digest}.patch
└── state/
    ├── installation.json
    ├── review-decisions.json
    ├── runtime-summary.json
    ├── promotion-previews/{preview-digest}.json
    └── briefed-{claude-session-id}
```

Locks under `state/` are temporary ownership markers, not approvals.

`state/runtime-summary.json` is a bounded worker-produced snapshot with its timestamp and
non-negative pending-extraction, review-ready, and pending-promotion counts. `SessionStart`
reads only this one file and force-launches the detached worker; it never recomputes the counts
or enumerates retained artifacts. The worker performs the exact scans, stale recovery,
already-authorized review cleanup, and snapshot refresh outside the hook.

Each capture request is a short-lived, consent-checked metadata envelope containing the native
session ID, canonical read-only transcript path, project directory, capture timestamp, retry
count, and sanitized last error. It contains no conversation text. `SessionEnd` writes the
envelope and launches a fully detached worker. The worker removes it after normalization
succeeds, is ineligible, reaches the configured retry ceiling, or fails request-contract
validation after a sanitized error is logged; a retryable capture failure retains the envelope
and records only a sanitized log entry. A corrupt duplicate envelope is replaced by the newly
validated request.

## Claude evidence JSON

One evidence object contains:

- `schema_version: 1`;
- `runtime: "claude"`;
- `session_id`;
- the native transcript's `transcript_sha256`;
- `captured_at`;
- `project_dir`;
- `messages`, an ordered array of `{role, text}` objects; and
- `redactions`, the replacement count.

Only bounded, redacted `user` and `assistant` text is persisted. Context-only wrapper turns,
system/developer content, reasoning, tool calls/results, patches, world state, subagents,
sidechains, and worker/extractor sessions are excluded. The runtime applies the turn and total
character ceilings before writing. Every surviving string remains untrusted evidence.

## Claude audit Markdown

The audit starts with `processed: false` and records `session_id`, `user_messages`, evidence
path in `normalized_transcript_path`, suggestion path, source transcript format/runtime,
transcript digest, redaction count, cwd, and detected skill. `processed: true` means every
candidate occurrence in that audit—or its confirmed zero-candidate occurrence—has an exact
job/result/audit-bound ledger authorization.

After that point, only the normalized evidence object is deleted. The audit, suggestion,
review ledger, instinct, promotion receipt/outcome, and native transcript remain.

## Claude queue JSON

The job ID is deterministic from runtime, session ID, transcript SHA-256, and schema version.
A record contains `schema_version`, `runtime`, `job_id`, `session_id`, `transcript_sha256`,
`state`, `attempts`, timestamps, lease state, evidence/audit/result paths, source format,
exact extractor model, evidence and audit SHA-256 values, candidate count and result SHA-256
after success, manual retry count, and sanitized `last_error`. The queue filename and derived
state-confined artifact names are authoritative; Markdown path fields are display-only. Review
accepts only a completed queue whose evidence, audit, and suggestion digests verify.

States are:

| State | Meaning | Next state |
|---|---|---|
| `queued` | Evidence is ready | `processing` |
| `processing` | One worker holds an unexpired lease | `completed`, `retryable`, or `failed` |
| `retryable` | A bounded attempt failed or a lease expired | `processing` |
| `completed` | A schema-valid suggestion exists; zero candidates is valid | Human review |
| `failed` | Automatic attempt ceiling reached | Explicit manual retry |

Queue changes use atomic replacement. Duplicate hook delivery for the same key returns an
existing schema-valid job; an invalid file occupying that identity is retained for operator
recovery and the capture request remains retryable. A sanitized log may record state,
candidate count, and a bounded error class; it
must not contain evidence or raw model stderr.

## Claude suggestion Markdown

The header records session ID, generation time, zero-to-five candidate count, detected skill,
and `source_runtime: claude`. Each candidate has exactly:

- `type`: `correction|confirmation|voice|scope|workflow`;
- `rule`: one non-empty sentence;
- `evidence`: a redacted excerpt of at most 160 characters;
- `context`: at most 300 characters;
- `why it matters`: a required evidence-bound rationale of at most 300 characters; and
- optional registered `skill`.

Invalid or over-limit model output produces no suggestion file. Zero candidates is a valid
completed suggestion.

## Claude review backlog and ledger

The read-only backlog has distinct `zero_candidate_audits`, `missing_suggestion_audits`, and
`clusters`. Clusters use exact `type + normalized rule` identity. Voice, workflow, scope,
correction, and confirmation are weighted in that review order; support and skill/cwd breadth
provide deterministic tie-breaking. Every cluster reports `exact_match_state: new|exact`
against active instincts using the same type-aware normalized-rule comparison.

`state/review-decisions.json` uses strict schema version 2. Each cluster maps to append-only
decision events containing `decision`, `decided_at`, optional `instinct_path`, and exact
occurrence records. Every occurrence binds the session ID, transcript-derived job ID,
transcript SHA-256, suggestion-result SHA-256, and pre-processing audit SHA-256. Reusing a
Claude session ID therefore cannot transfer an earlier decision to a new transcript or result.
Legacy or malformed ledgers fail closed and require operator repair; they never authorize
cleanup. Zero-candidate resolutions are separately occurrence-bound in the same ledger.

Decisions are `accept`, `reject`, `edit`, or exact type-aware `match`; all require `--confirm`.
A worker cannot write this ledger. Evidence for a multi-candidate audit remains until every
cluster occurrence from that audit has its own matching ledger authorization.

## Instinct Markdown

The runtime writes JSON-compatible values in YAML-style frontmatter. Required fields are
`id`, `type`, `confidence`, `created`, `last_seen`, `seen_count`, `status`, `source_skill`,
`source_skills`, `source_runtime`, `source_transcript_format`, `source_cwds`,
`strong_correction`, `contradicted`, `suggested_destination`, `promotion_outcome`, and
`promoted_to`. The body holds the approved atomic rule, evidence, and rationale.

Status is `active`, `promoted`, or `covered`. Only active instincts with confidence at least
`0.5` can be previewed. Support confidence is `0.30` for 1–2 sessions, `0.50` for 3–5,
`0.70` for 6–10, and `0.85` for 11+; an explicit strong correction adds `0.05`, and an
explicit contradiction subtracts `0.10`.

## Claude promotion preview and immutable receipt

`state/promotion-previews/{preview-digest}.json` binds:

- schema, instinct ID, destination class, and delivery mode;
- SHA-256 of the source instinct's original rule and rationale, so source drift is detected
  independently of an explicitly edited promoted rule;
- exact target path and its current SHA-256;
- approved rule and rationale;
- managed section and insertion;
- exact resulting text and resulting SHA-256;
- duplicate state and preview timestamp; and
- canonical `preview_digest` plus `confirmation_required: true`.

The canonical digest covers the payload before `preview_digest` and
`confirmation_required` are added. The separate confirmed approval verifies that digest and
rechecks the target digest. It then writes
`promotion-receipts/{receipt-digest}.json` containing `schema_version`, `preview_digest`,
`approved_at`, unchanged `approved_action`, and canonical `receipt_digest`. Receipt files are
immutable inputs to the executor; changing any bound field invalidates them.

Repeated confirmation of the same unchanged preview returns the existing receipt rather than
minting a second approval. Status counts only structurally valid digest-named receipts as
`approved`; malformed receipt files are reported separately as `invalid`. Outcome counts are
subsets of the valid approved receipts.

## Claude promotion outcome and governed patch

The executor writes at most one outcome for each receipt:

- local delivery writes the exact approved result atomically, verifies its digest, updates
  the instinct to terminal `promoted` or `covered`, and records target/result digest. If the
  exact target write succeeds but later instinct bookkeeping fails, the outcome stays applied
  and carries a sanitized bookkeeping warning rather than falsely reporting the target write
  as failed. If the target write succeeds but outcome persistence is interrupted, the next run
  recognizes the exact approved resulting digest and records the outcome without rewriting;
- review delivery leaves the target untouched, writes an exact unified diff under
  `promotion-changesets/`, and records `awaiting_review`; or
- invalid receipt, target drift, or write failure records `failed` with a sanitized error.

Destination rules are fixed: `global` is local-only to `~/.claude/CLAUDE.md`; `project` is
local-only to an exact `CLAUDE.md`; `skill` is review-only to `RUN-*.md` or `REF-*.md`; and
`standard` is review-only to `STD-*.md`. Installed bundles, runtime state, and plugin caches
are never valid targets. Re-execution is idempotent only when the existing outcome has a valid
same-receipt contract and its target/result fields match the approved action; malformed or
unbound outcome files cannot suppress pending execution.

## Standalone installation receipt

`state/installation.json` schema `2` is the ownership authority for standalone updates and
uninstall. Its canonical digest binds the install mode; Claude, source, active bundle, nested
skill, settings, backup, and state paths; the exact two hook identities; preservation flags;
and the capture/acknowledgement values observed at install time. A fresh install records both
observations as false. A valid receipt-owned upgrade preserves and truthfully records current
runtime state. Missing, malformed, or digest-mismatched receipts block update and uninstall;
ambiguous or modified PMM-looking hook handlers are preserved and also block mutation.

## Codex and portable contracts

Existing Codex contracts remain as shipped in `0.2.0`: normalized JSONL evidence, audit and
suggestion Markdown, `queued|running|succeeded|failed` queue state, bucketed review,
priority snapshots, complete instinct files, exact destination preview, and confirmed apply.
Portable mode uses the same review contracts only after explicit candidate import and cannot
capture, extract, or promote. Status/list commands load older state conservatively and do not
rewrite it.
