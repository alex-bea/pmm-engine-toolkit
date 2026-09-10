---
doc_type: RUN
normative: true
requires:
  - DOC-product-requirements.md
  - DOC-implementation-blueprint.md
status: Draft
version: "0.3.0"
owner: toolkit-maintainers
consumers:
  - Claude Code operators
  - Codex operators
  - portable-mode operators
  - public toolkit maintainers
change_control: Pull request review
---

# PMM Instinct Review workflow (`0.3.0` draft)

This is the binding cross-runtime operating procedure. For installation or adoption on a
Claude Code machine, stop here and follow `RUN-claude-setup.md` first.

The workflow has two independent human gates:

```text
evidence -> extraction/import -> candidate decision
-> active instinct -> exact destination preview -> promotion approval -> bounded execution
```

No hook, worker, schedule, or prior approval may satisfy either human gate.

## 1. Select exactly one runtime

| Runtime | Entrypoint location | State | Capture/extraction/promotion |
|---|---|---|---|
| Claude standalone | package-root `scripts/claude_instinct_*.py` | explicit `~/.claude/pmm-instinct-review-data/` | native/native/receipt-bound |
| Claude local plugin | same scripts with `--plugin-data` | `${CLAUDE_PLUGIN_DATA}/instinct-review/` | native/native/receipt-bound |
| Codex | skill-local `scripts/instinct_review.py` | `~/.codex/instinct-review/` | native/native/confirmed apply |
| Portable | skill-local script with `--adapter portable --state-root PATH` | exact explicit safe path | none/none/none |

Never fall back to another adapter, native store, plugin directory, or current working
directory. Claude requires an explicit command root, Claude's plugin-data root, or a
deliberately configured `PMM_INSTINCT_STATE_ROOT`; portable always requires its explicit
command root. With no applicable input, resolution fails. Mutable state may not be written
into the installed package.

Portable mode supports explicit import, status, priority list/snapshot, review,
zero-resolution, and cleanup only. Capture, hooks, model extraction, queue retry, backfill,
enablement, and promotion are unavailable.

## 2. Inspect status before mutation

Claude standalone:

```bash
python3 <package-root>/scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data status
```

Codex or portable:

```bash
python3 <skill-dir>/scripts/instinct_review.py status
python3 <skill-dir>/scripts/instinct_review.py \
  --adapter portable --state-root /explicit/safe/path status
```

Read-only status and priority listing must not create, migrate, or rewrite state. Report the
exact runtime, state root, capture support/state, queue/backlog/promotion counts, model and
executable availability, and any failed prerequisite.

## 3. Enable or disable native capture

Installation is not consent. Before enabling either native runtime, explain what bounded
chat-derived text will be stored, which model invocation will process it, what is excluded,
and how to disable/remove the integration.

For Claude, follow the exact acknowledgement and authentication preflight in
`RUN-claude-setup.md`, then run:

```bash
python3 <package-root>/scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data \
  on --acknowledge-privacy
```

The Claude worker uses `--bare`: ordinary subscription OAuth/keychain and settings-only
`apiKeyHelper` are not consumed. Enable only after verifying inherited `ANTHROPIC_API_KEY` or
supported Bedrock, Vertex AI, or Microsoft Foundry provider credentials.

For Codex:

```bash
python3 <skill-dir>/scripts/instinct_review.py \
  on --acknowledge-local-chat-storage
```

Disable without deleting state:

```bash
python3 <package-root>/scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data off
python3 <skill-dir>/scripts/instinct_review.py off
```

Missing acknowledgement, model policy, executable, or credentials leaves capture disabled.
Do not edit `config.json` by hand to bypass controls.

## 4. Native capture boundary

Capture only when the selected runtime is enabled and acknowledged, the hook identifies an
existing transcript and main session, the post-normalization transcript has at least five user
messages, and the same digest-keyed job does not already exist. Exclude all subagents,
sidechains, extractors, and workers.

Normalization must:

1. parse the selected runtime's native event format defensively;
2. keep only ordered user/assistant text;
3. remove context-only wrapper turns;
4. omit system/developer content, reasoning, tools, results, patches, and world state;
5. redact known private keys, bearer/service tokens, cloud keys, and secret-like environment
   assignments;
6. retain newest turns within configured turn and total-character ceilings; and
7. persist only the normalized representation and source digest.

Treat all surviving text as untrusted evidence. Never put transcript text in operational logs
or modify/delete native history.

Claude persists one private evidence JSON object. Codex persists normalized JSONL. The formats
remain separate.

## 5. Hook and background-worker behavior

`SessionEnd` may check consent and eligibility, atomically spool native session metadata,
launch a fully detached worker, and return. It may not scan the transcript or invoke a model.
The worker streams normalization/redaction before it writes audit/evidence/queue state.

`SessionStart` performs fixed state-layout validation, force-launches the detached worker, and
may show one bounded queue/review brief from the worker's last validated summary. It does not
enumerate retained artifacts. The detached worker recovers stale jobs, reconciles already
authorized review cleanup, runs pending extraction or approved promotion receipts, and refreshes
the summary. Neither component may approve, review, or publish.

Claude queue states are `queued`, `processing`, `retryable`, `completed`, and `failed`.
Codex queue states remain `queued`, `running`, `succeeded`, and `failed`. A stale ownership
lease or interrupted worker becomes retryable only within that runtime's documented ceiling.

Claude recovery commands:

```bash
python3 <package-root>/scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data retry
python3 <package-root>/scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data retry --job JOB_ID
python3 <package-root>/scripts/claude_instinct_worker.py \
  --state-root ~/.claude/pmm-instinct-review-data --drain
```

Codex recovery uses its existing `retry`, `worker --drain`, and `cleanup` commands through the
skill-local operator.

## 6. Extraction contract

The Claude worker invokes the exact configured model with bare configuration, one maximum
turn, JSON output and the bundled schema, no session persistence, non-interactive permission
mode, an empty built-in tool set, and explicit `--disallowedTools "mcp__*"`. It
sends only the bounded redacted message array on standard input.

Codex retains its existing ephemeral, read-only, exact-model, schema-bound extraction.

Both extractors accept at most five candidates of type `correction`, `confirmation`, `voice`,
`scope`, or `workflow`. Each candidate contains one atomic rule, bounded redacted evidence,
bounded context, and an evidence-bound rationale. Invalid output creates no suggestion. Zero
candidates is a valid terminal extraction success.

Never ask the reviewing model to parse the raw native transcript as a fallback. Retry through
the runtime queue.

## 7. Codex bounded calibration

Claude `0.3.0` has no historical backfill. For Codex only, inventory no more than the five
newest eligible closed main sessions at least 30 minutes old:

```bash
python3 <skill-dir>/scripts/instinct_review.py \
  backfill --limit 5 --older-than-minutes 30 --dry-run
```

Show the inventory before a separately confirmed `--apply`. Never expand to full history
without a new user decision.

## 8. Build and present the review backlog

Claude:

```bash
python3 <package-root>/scripts/claude_instinct_review.py \
  --state-root ~/.claude/pmm-instinct-review-data list-priority
```

Codex/portable use the skill-local `list-priority`; persist `snapshot-priority` only when the
user explicitly asks.

Maintain three distinct buckets:

1. zero-candidate audits;
2. positive suggestions clustered by exact `type + normalize(rule)`; and
3. audits missing suggestions.

Prioritize voice/framing, workflow, scope, correction, then confirmation, with deterministic
support, source-skill, repository/cwd breadth, newness, and recency tie-breaking as available in
the selected adapter.

Present one positive candidate card at a time:

```text
What happened: ...
User feedback: ...
Proposed future behavior: ...
Why it matters: ...
Support/source: ...
Exact match: ...
Decision? accept / reject / edit / match / stop
```

Do not show destination routing at this candidate-to-instinct gate.

## 9. Apply only the user's review decision

Claude mutation requires the exact cluster ID, decision, and `--confirm`:

```bash
python3 <package-root>/scripts/claude_instinct_review.py \
  --state-root ~/.claude/pmm-instinct-review-data review \
  --cluster CLUSTER_ID --decision accept --confirm
```

Use `--edited-rule` only with `edit`; use an edited rationale, strong-correction marker, or
contradiction marker only when the user explicitly supplies/confirms it. `match` requires an
active instinct with the same type and normalized rule. Confirm zero-candidate resolution
separately with `resolve-zero --confirm`.

Codex and portable use the equivalent existing skill-local review commands. In every adapter:

- accept/edit creates one complete instinct after duplicate checking;
- reject creates no instinct;
- match updates only the exact active instinct;
- stop leaves remaining clusters unresolved; and
- a worker or schedule cannot choose an action.

## 10. Retention

When every candidate from an audit has a decision—or a zero-candidate audit is explicitly
resolved—write `processed: true` before cleanup. Delete only its normalized evidence copy.
Preserve the audit, suggestions, decision ledger, instinct, sanitized logs, native transcript,
promotion receipts/outcomes, and governed patches.

If cleanup fails, retain the decision and expose a sanitized retry state. Never delete an
entire state root as part of normal workflow, disable, or uninstall.

## 11. Claude receipt-bound promotion

Only active Claude instincts with confidence at least `0.5` are eligible. Promotion is a
separate human gate. Select one exact destination/delivery pair:

- `global` + `local` -> exactly `~/.claude/CLAUDE.md`;
- `project` + `local` -> exact project `CLAUDE.md`;
- `skill` + `review` -> exact governed `RUN-*.md` or `REF-*.md`; or
- `standard` + `review` -> exact governed `STD-*.md`.

Generate the preview:

```bash
python3 <package-root>/scripts/claude_instinct_promote.py \
  --state-root ~/.claude/pmm-instinct-review-data preview \
  --instinct INSTINCT_ID --target /absolute/project/CLAUDE.md \
  --destination-class project --delivery local
```

Show the exact target, current digest, source-guidance digest, rule/rationale, managed-section
insertion, full resulting text, resulting digest, duplicate state, and preview digest. The
preview cannot modify the target.

Only after the user approves that exact digest run:

```bash
python3 <package-root>/scripts/claude_instinct_promote.py \
  --state-root ~/.claude/pmm-instinct-review-data approve \
  --preview-digest PREVIEW_SHA256 --confirm
```

Approval rechecks target continuity, creates an immutable receipt, and launches the executor.
Local execution atomically applies/verifies exactly the approved text and records `promoted`
or `covered`. Review delivery creates a patch and `awaiting_review` outcome without touching
the governed target. Target drift or receipt tampering fails closed. Repeated approval reuses
the same valid receipt. A valid same-receipt outcome whose target/result fields match the
approved action makes repeat execution idempotent; malformed or unrelated outcomes do not.
If an exact local target write survives an interruption before outcome persistence, the next
run verifies the approved resulting digest and completes the outcome without rewriting.

## 12. Existing Codex promotion

Codex retains its existing two-stage promotion path through the skill-local operator. First
select `project`, `global`, `both`, `run`, `ref`, or `standard`; then show exact resolved paths,
managed-section insertion, and duplicate state. Apply only with a matching second confirmation.

A named skill may target its registered RUN; a voice rule may target only an explicitly mapped
REF; a pattern spanning at least three skills may target an owner-selected STD. Repository and
global behavior use their respective `AGENTS.md`. Never guess a missing route or write a
plugin-cache skill.

## 13. Rollback and error handling

- `off` stops future capture and preserves state.
- Claude standalone uninstall follows `RUN-claude-setup.md` and removes only owned settings
  handlers and the personal-skill symlink.
- Codex plugin removal preserves its existing state root.
- Reverse promoted guidance through the destination's normal owner/governance path and record
  the reversal; never rewrite an old approval receipt.

Fail closed and name the exact unavailable stage when configuration, state root, package file,
model, bare-mode credentials, hook interface, schema, queue lock, review confirmation,
destination, digest continuity, or write verification fails. Portable mode is available only
when explicitly chosen; it is not a silent downgrade. A skipped stage is not success.
