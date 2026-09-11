# PMM Instinct Review `0.3.1` (draft)

PMM Instinct Review is a local, human-gated improvement loop for durable working preferences:

```text
eligible evidence -> bounded extraction/import -> ranked human review
-> approved instinct -> exact promotion preview -> separate approval -> bounded execution
```

The package supports three deliberately isolated modes:

| Mode | Evidence source | Extraction | Promotion | State root |
|---|---|---|---|---|
| Codex | Eligible completed Codex main sessions | Detached Codex worker | Confirmed Codex destination write | `~/.codex/instinct-review/` |
| Native Claude | Eligible completed Claude Code main sessions | Detached Claude worker | Receipt-bound local write or governed review patch | `~/.claude/pmm-instinct-review-data/` |
| Portable | Explicit adopter-owned candidate JSON | None | None | Required explicit `--state-root` |

No mode reads another mode's store. The package has no hosted service, telemetry, database,
connector, or marketplace dependency. Python 3.10+ and the standard library are sufficient
for the bundled runtime. Native extraction additionally needs the corresponding authenticated
agent CLI.

This `0.3.1` release remains a draft until its focused and repository validation, required
security evidence, pull-request review, and repository release gates are complete. It closes
two public Codex fidelity gaps against the private PMM Engine Codex path; it does not claim
parity with the private Claude transaction architecture. Native Claude behavior from `0.3.0`
is preserved.

## Privacy and human control

Installation does not enable capture. Native Codex and Claude capture require an explicit
local-storage acknowledgement. When enabled, the runtime keeps only bounded, redacted
user/assistant text from eligible main sessions in its adopter-owned state root. It excludes
system/developer context, reasoning, tools, tool results, patches, world state, sidechains,
subagents, and extractor/worker sessions. Native session history is read-only and is never
deleted.

The extractor receives minimized evidence as untrusted data and may return no more than five
schema-valid candidates; zero candidates is valid. Native Claude extraction disables built-in
and MCP tools. Codex extraction runs in an ephemeral read-only sandbox and its prompt prohibits
tool use, but the Codex runtime does not claim that tools are technically unavailable.
Operational logs contain state, counts, and sanitized errors, never transcript text. Pattern
redaction is not perfect, so do not enable capture where local transcript-derived storage or
applicable native model/provider processing is prohibited, and avoid putting secrets into
sessions.

Two separate human decisions remain mandatory:

1. accept, reject, edit, or exactly match a candidate cluster; and
2. approve the exact runtime-specific promotion preview.

In native Claude mode, that preview and approval bind the target and content digests; a
background worker may execute the resulting immutable receipt. It cannot create the approval,
change its target, approve an instinct, merge a governed change, or publish anything. Codex
keeps its separate preview-and-confirmed-apply transaction model: exact target selection is
human-owned and revalidated before apply, without a Claude-style immutable receipt.

## Install for native Claude Code without a marketplace

Use the detailed [Claude setup RUN](skills/pmm-instinct-review/references/RUN-claude-setup.md)
on the destination machine. From this package directory, inspect first, then choose one mode:

```bash
python3 scripts/install_claude_instinct_review.py --check
python3 scripts/install_claude_instinct_review.py --install --mode symlink
# Or create a pinned snapshot:
python3 scripts/install_claude_instinct_review.py --install --mode copy
```

Symlink mode follows the checked-out Toolkit package after a validated update. Copy mode
creates a pinned package at `~/.claude/pmm-instinct-review/`. Both modes link the nested skill
into `~/.claude/skills/pmm-instinct-review`, add only this package's two handlers to
`~/.claude/settings.json`, back up settings when changed, and refuse occupied destinations.
A fresh install leaves capture disabled. A valid receipt-owned upgrade preserves the existing
runtime state and reports its observed enablement/acknowledgement in the new installation
receipt. Restart Claude Code, then inspect `/skills` and `/hooks`.

Only after the user understands and accepts the local evidence boundary, enable capture:

```bash
python3 scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data status
python3 scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data on --acknowledge-privacy
```

Before enabling, verify the worker's bare-mode authentication. `--bare` does not use an
ordinary Claude subscription login/keychain, and this release does not pass `--settings` for
an `apiKeyHelper`. It requires an inherited `ANTHROPIC_API_KEY` or supported Bedrock, Vertex
AI, or Microsoft Foundry provider credentials. Keep capture disabled unless the detailed RUN's
bare-mode request succeeds; binary discovery alone does not verify authentication. The enable
command fails closed when Claude Code itself is unavailable. If credentials are later revoked,
extraction fails visibly and retryably without persisting provider output. `SessionEnd` only
spools a small consent-checked metadata request and starts a fully detached worker. That worker
normalizes and persists bounded evidence before extraction; the model call never runs inside
the hook. `SessionStart` performs fixed layout checks, force-launches the detached worker, and
reads only one bounded worker-produced status snapshot. Retained-store scans, stale recovery,
already-authorized review cleanup, extraction, receipt execution, and summary refresh all run
in the detached worker. At most one snapshot brief is emitted per Claude session.

The standalone installer is the supported adoption path and installs a five-second user-settings
`SessionEnd` budget. The optional plugin form marks `SessionEnd` asynchronous because Claude's
plugin-provided timeout does not raise the shared 1.5-second shutdown budget. For reliable
non-interactive `claude -p` capture, use the standalone installer: Claude can cancel an async hook
at non-interactive teardown even though this hook never performs the model call itself.

Review remains explicit:

```bash
python3 scripts/claude_instinct_review.py \
  --state-root ~/.claude/pmm-instinct-review-data list-priority
python3 scripts/claude_instinct_review.py \
  --state-root ~/.claude/pmm-instinct-review-data review \
  --cluster CLUSTER_ID --decision accept --confirm
```

For promotion, first generate and inspect an exact preview. This example targets one project
`CLAUDE.md`; substitute an absolute path on the destination machine:

```bash
python3 scripts/claude_instinct_promote.py \
  --state-root ~/.claude/pmm-instinct-review-data preview \
  --instinct INSTINCT_ID --target /absolute/project/CLAUDE.md \
  --destination-class project --delivery local

python3 scripts/claude_instinct_promote.py \
  --state-root ~/.claude/pmm-instinct-review-data approve \
  --preview-digest PREVIEW_SHA256 --confirm
```

The approval command idempotently creates or returns one immutable receipt for the exact
preview and starts its executor. If the target has changed since preview, execution refuses
it. If an interrupted executor already wrote the exact approved result, its next run verifies
that digest and finishes the missing outcome without rewriting the target. `global` and `project` destinations are local
Claude instruction writes. `skill` (`RUN-*.md` or `REF-*.md`) and `standard` (`STD-*.md`)
destinations must use `--delivery review`; the worker creates a patch and stops at
`awaiting_review` without changing the governed target.

The optional `.claude-plugin/plugin.json` and `hooks/claude-hooks.json` support local-plugin
validation and interactive development. They are not required by the standalone installer and
are not the supported capture path for `claude -p` sessions.

## Install for Codex

```bash
codex plugin marketplace add alex-bea/pmm-engine-toolkit --ref main
codex plugin add pmm-instinct-review@pmm-engine-toolkit
```

Open `/hooks`, inspect the plugin-relative `SessionStart` and `SessionEnd` handlers, and trust
them separately. Then ask:

```text
Use $pmm-instinct-review to enable continuous learning with the exact Codex model I choose. I
acknowledge local chat storage.
```

Inspect status before enabling. First successful enablement requires a non-empty exact model,
unless one is already persisted in the Codex store:

```bash
python3 skills/pmm-instinct-review/scripts/instinct_review.py status
python3 skills/pmm-instinct-review/scripts/instinct_review.py \
  on --acknowledge-local-chat-storage --model <exact-model>
```

The model string is adopter-owned configuration; the Codex adapter supplies no default. It is
persisted before capture becomes enabled. New hook and backfill jobs use only that persisted
model, even if a SessionEnd event reports another value. A legacy enabled store with no model
does not create normalized evidence, an audit, or a queue job: capture returns `skipped` with
reason `unconfigured_model`, while preflight reports `model_policy: false`. Run `on --model
<exact-model>` after reviewing the privacy boundary to repair that state. Repair first forces
capture off; a failed executable preflight leaves the model persisted but capture disabled.

Codex route configuration also remains adopter-owned. `run_routes` maps a source-skill slug to
one exact relative `references/RUN-*.md` path. `voice_ref_routes` accepts either its legacy
single-string form or a non-empty ordered list of relative `references/REF-*.md` paths:

```json
{
  "run_routes": {
    "weekly-decision-report": "references/RUN-weekly-decision-report.md"
  },
  "voice_ref_routes": {
    "weekly-decision-report": [
      "references/REF-report-voice.md",
      "references/REF-evidence-framing.md"
    ]
  }
}
```

Routes are hints, not write authority. Each value must be relative, contain no parent
traversal, use the required filename family, resolve to an existing writable regular file
inside an independently discovered user-owned source-skill root, and stay outside the
installed package and plugin cache. Without `run_routes`, dynamic RUN discovery remains
available only when exactly one eligible file exists.

When one validated RUN or REF remains, preview may select it. When several remain, preview is
non-applicable and returns `reason: multiple-eligible-targets` with the exact absolute
`eligible_targets`; it does not persist an applicable preview or choose the first path. The
owner must select one of the recomputed choices exactly:

```bash
python3 skills/pmm-instinct-review/scripts/instinct_review.py promote \
  --instinct INSTINCT_ID --destination ref --target /exact/eligible/REF-file.md
```

Only after reviewing that exact preview may the owner repeat the same arguments with `--apply
--confirm`. An arbitrary, stale, or newly ineligible `--target` fails closed. Capture remains
consent-gated, extraction stays detached and schema-constrained, and candidate review remains
separate from promotion.

## Use the isolated portable adapter

Portable mode can be called from Claude Code, Codex, or another local agent. It reviews only
the explicitly supplied fictional or adopter-owned candidate bundle:

```bash
python3 skills/pmm-instinct-review/scripts/instinct_review.py \
  --adapter portable \
  --state-root "$PWD/.local/instinct-review" \
  import-candidates ./candidate-bundle.json --confirm

python3 skills/pmm-instinct-review/scripts/instinct_review.py \
  --adapter portable \
  --state-root "$PWD/.local/instinct-review" \
  list-priority
```

Portable mode supports `status`, `list-priority`, `snapshot-priority`, `resolve-zero`,
`review`, `cleanup`, and `import-candidates`. Capture, hooks, extraction, retries, backfill,
enablement, and promotion fail closed. It never falls back to a native agent store.

## Smoke check and recovery

For native Claude, follow the setup RUN through disabled inspection, `/skills` and `/hooks`
review, explicit consent, one eligible synthetic session, detached extraction, one human
review, and one exact receipt. Do not claim native readiness until that lifecycle passes on an
authenticated Claude-capable machine. Failures remain visible as `retryable` or `failed` jobs:

```bash
python3 scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data retry
python3 scripts/claude_instinct_worker.py \
  --state-root ~/.claude/pmm-instinct-review-data --drain
```

Disable and uninstall without deleting state:

```bash
python3 scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data off
python3 scripts/install_claude_instinct_review.py --uninstall --confirm
```

Uninstall removes only owned hook entries and the owned personal-skill symlink. It preserves
unrelated Claude settings, native history, and `~/.claude/pmm-instinct-review-data/`. Copy-mode
snapshots are deliberately not overwritten or silently deleted; update them only through the
explicit procedure in the setup RUN.

See the [product requirements](skills/pmm-instinct-review/references/DOC-product-requirements.md),
[implementation blueprint](skills/pmm-instinct-review/references/DOC-implementation-blueprint.md),
[workflow](skills/pmm-instinct-review/references/RUN-workflow.md), and
[submission tests](skills/pmm-instinct-review/references/DOC-submission-test-cases.md) for the
complete public contract.
