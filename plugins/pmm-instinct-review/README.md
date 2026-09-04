# PMM Instinct Review `0.2.0` (draft)

PMM Instinct Review is a local, human-gated improvement loop for durable working
preferences:

```text
eligible evidence -> bounded candidate extraction/import -> ranked review
-> approved instinct -> exact promotion preview -> separate write approval
```

The Codex adapter can capture eligible completed sessions automatically after explicit
consent. The portable adapter lets Codex, Claude Code, or another local work agent review an
explicit candidate bundle in an isolated adopter-owned directory. Portable mode does not
capture sessions, run hooks or models, read native agent stores, or promote instructions.

This `0.2.0` release remains a draft until its pull request is approved. The package uses
Python 3.11+ and the standard library only.

## Privacy and consent

Installation does not enable capture. Codex enablement records explicit consent before any
chat-derived state is created. Confirm that local transcript-derived storage and a second
Codex model invocation comply with the policies for the device and source material.

The plugin has no telemetry or hosted PMM service and never changes native session history.
Codex normalized user/assistant text is redacted, bounded, stored temporarily under
`~/.codex/instinct-review/`, and removed only after every candidate associated with the audit
has a decision. Operational logs contain state, counts, and sanitized errors—not transcript
text. Plugin removal preserves the adopter-owned state directory.

Imported candidate text and normalized transcript text are untrusted evidence. Neither is
executed as instructions. Review and promotion are separate human decisions.

## Install for Codex

```bash
codex plugin marketplace add alex-bea/pmm-engine-toolkit --ref main
codex plugin add pmm-instinct-review@pmm-engine-toolkit
```

If `codex` is not on `PATH`, use the executable bundled with the installed Codex host. Open
`/hooks`, inspect the plugin-relative `SessionStart` and `SessionEnd` hooks, and trust them
separately. Then ask:

```text
Use $pmm-instinct-review to enable continuous learning. I acknowledge local chat storage.
```

Enablement fails closed if Python, the Codex executable, the extractor schema, or model policy
cannot be resolved. The SessionEnd hook only captures and launches a detached worker; model
work remains outside the hook timeout.

## Use the isolated portable adapter

Portable review is an explicit CLI surface that can be invoked from either Codex or Claude
Code. Choose a state root that is outside native agent stores and outside the installed plugin:

```bash
python3 plugins/pmm-instinct-review/skills/pmm-instinct-review/scripts/instinct_review.py \
  --adapter portable \
  --state-root "$PWD/.local/instinct-review" \
  import-candidates ./candidate-bundle.json --confirm

python3 plugins/pmm-instinct-review/skills/pmm-instinct-review/scripts/instinct_review.py \
  --adapter portable \
  --state-root "$PWD/.local/instinct-review" \
  list-priority
```

Portable commands are limited to `status`, `list-priority`, `snapshot-priority`,
`resolve-zero`, `review`, `cleanup`, and `import-candidates`. Capture, hooks, backfill, queue
workers, enablement, retries, and promotion fail closed. Adapter selection never falls back to
Codex state.

The import file is a JSON array. Each item requires `id`, `lesson`, `source`, `observed_on`,
and a non-empty `evidence` array; optional `type` and `skill` values refine clustering. See
[`assets/state-contracts.md`](skills/pmm-instinct-review/assets/state-contracts.md) and the
fictional example set for complete contracts.

## Operator requests

Use `$pmm-instinct-review` for:

- continuous learning status, on, or off;
- a bounded five-session Codex backfill dry run and confirmed apply;
- queue drain, failed-job retry, or processed-evidence cleanup;
- the three backlog buckets: zero candidates, positive clusters, and missing suggestions;
- voice-first priority listing or an explicitly persisted priority snapshot;
- one confirmed `accept`, `reject`, `edit`, or type-aware exact `match` decision; and
- a promotion destination selection, exact preview, then matching apply confirmation.

Positive clusters rank by review area, support, source-skill breadth, repository/cwd breadth,
newness, and recency. The candidate card contains what happened, user feedback, proposed
behavior, rationale, support/source, dates, and match state. It contains no routing. An
approved instinct records its conservative destination suggestion, but no path is resolved
until promotion review.

Promotion requires an active instinct with confidence of at least `0.5`. Supported Codex
destinations are `project`, `global`, `both`, `run`, `ref`, and `standard`. The exact target,
managed-section insertion, and duplicate status are persisted in a signed preview. Apply
stages every target before replacement and requires a second confirmation. A successful or
already-covered result becomes terminal and leaves the default promotion queue.

Voice-to-REF promotion is adopter-configured through `voice_ref_routes` in
`~/.codex/instinct-review/config.json`. The target must already exist, be writable, and be
outside the plugin cache. The runtime never guesses a private route.

## Runtime state

Codex owns:

```text
~/.codex/instinct-review/
├── config.json
├── sessions/
│   └── instinct-priority.json
├── queue/
├── instincts/
├── logs/
└── state/
```

Portable mode owns exactly the explicit `--state-root` with the same review-state folders.
It does not read or write `~/.codex`, a Claude store, or another adapter root.

## Controlled smoke test

1. Confirm `status` reports capture disabled and creates no state.
2. Inspect and trust both Codex hooks.
3. Enable with the privacy acknowledgment.
4. Complete an eligible main task with at least five user turns and a durable correction.
5. Confirm the audit and queued, succeeded, or visibly retryable extraction state.
6. Run `list-priority`; inspect one card and record an explicit decision.
7. Confirm native history remains and normalized evidence is removed only after all decisions.
8. For an eligible instinct, select a destination, inspect the exact preview, then separately
   confirm apply. Confirm its status becomes `promoted` or `covered`.

A valid zero-candidate extraction is success and remains in its own explicitly resolved
bucket. Read-only status and priority listing do not create or migrate state.

## Rollback and recovery

Turn Codex capture off before uninstalling. Removing the plugin does not delete adopter-owned
state. Reinstallation can recover retryable queued jobs. Delete a state root only as a
separate, explicit local data-management action. Existing `0.1.0` records load with
conservative in-memory defaults; status does not rewrite them.

Detailed contracts are in the bundled [product requirements](skills/pmm-instinct-review/references/DOC-product-requirements.md),
[implementation blueprint](skills/pmm-instinct-review/references/DOC-implementation-blueprint.md),
[workflow](skills/pmm-instinct-review/references/RUN-workflow.md), and
[submission tests](skills/pmm-instinct-review/references/DOC-submission-test-cases.md).
