---
doc_type: DOC
normative: false
requires:
  - DOC-product-requirements.md
  - RUN-workflow.md
  - RUN-claude-setup.md
status: Draft
version: "0.3.1"
owner: toolkit-maintainers
consumers:
  - public plugin contributors
  - public plugin reviewers
change_control: Pull request review
---

# PMM Instinct Review — Implementation blueprint (`0.3.1` draft)

## Purpose

This blueprint maps the public requirements to the package's implementation and verification
surfaces. The RUN documents remain the binding operator procedures. Claude, Codex, and
portable are separate adapters; satisfying one adapter by reading another adapter's state is
an implementation failure. The `0.3.1` change is private-Codex fidelity expressed through
generic adopter-owned configuration, not private-Claude transaction parity.

## Guardrails

1. Keep model work bounded: minimized evidence in, zero-to-five schema-valid candidates out.
2. Keep deterministic behavior standard-library only and unit-testable without a model call.
3. Preserve the candidate-to-instinct and exact instinct-to-promotion human gates.
4. Treat transcripts, candidates, and model output as untrusted data.
5. Run no model inside a lifecycle hook and expose every retry/failure state.
6. Delete only decision-complete normalized evidence; native history is untouchable.
7. Never let a worker create approval, retarget a receipt, merge, publish, or directly write a
   governed RUN, REF, or STD.
8. Keep mutable state outside the installed package and refuse ambient cross-runtime fallback.
9. Require one persisted Codex model before capture and never infer it from session metadata.
10. Treat route configuration and `--target` as untrusted hints; validate, confine, recompute,
    and fail closed before choosing a RUN or REF.

## Component map

| Layer | Public files | Responsibility | Verification |
|---|---|---|---|
| Package manifests | `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json` | Declare separate Codex and optional Claude local-plugin surfaces | Manifest/version/skill-path checks |
| Public skill | `skills/pmm-instinct-review/SKILL.md`, `agents/openai.yaml` | Trigger, runtime selection, reference routing, safety boundary | Frontmatter and package-link checks |
| Procedures | `references/RUN-workflow.md`, `RUN-claude-setup.md` | Runtime operation and detailed no-marketplace adoption | Governed-document and manual workflow review |
| Claude hook wiring | `hooks/claude-hooks.json`, `scripts/claude_instinct_hook.py` | Fast settings dispatch plus async optional-plugin SessionEnd | Supported command shape, async plugin contract, no model call, timing tests |
| Claude deterministic core | `scripts/pmm_instinct_claude.py` | State resolution, normalization, queue, extraction validation, review, receipts, outcomes | Focused Claude unit tests |
| Claude controls | `scripts/claude_instinct_capture.py`, `claude_instinct_worker.py`, `claude_instinct_review.py`, `claude_instinct_promote.py` | Explicit CLI for each lifecycle stage | CLI/error/confirmation tests |
| Claude installer | `scripts/install_claude_instinct_review.py` | Nested personal skill, two owned settings hooks, backup, narrow uninstall | Symlink/copy/conflict/preservation tests |
| Claude extractor | `assets/claude-extractor-prompt.md`, `claude-extractor-schema.json` | Untrusted-evidence instruction and exact output shape | Closure, schema, zero/positive/invalid tests |
| Claude default config | `assets/claude-config-template.json` | Disabled state, bounds, retry and model contract | Runtime-default equality test |
| Codex/portable core | `skills/pmm-instinct-review/scripts/` | Persisted-model-only Codex jobs, confined exact RUN/multi-REF choices, preserved review/promotion, and explicit portable import | Model/routing matrix plus complete regression suite |
| Codex adopter config | nested `assets/config-template.json` | Disabled null-model default plus empty `run_routes` and `voice_ref_routes` schemas | Defaults, parsing, compatibility, and confinement tests |
| Contracts/examples | nested `assets/` and `examples/fictional-northstar-reports/` | Blank output/state contracts and inert fictional lifecycles | Link, schema, identifier, and digest tests |

All Claude runtime imports resolve inside the package root. The installer supports the public
nested skill layout; it must not expect a private root-level `SKILL.md`.

## Native Claude state design

Standalone state is `~/.claude/pmm-instinct-review-data/`; local-plugin state is
`${CLAUDE_PLUGIN_DATA}/instinct-review/`. Explicit resolution produces:

```text
<state-root>/
├── config.json
├── capture-inbox/{request-id}.json
├── sessions/{audit.md,evidence.json,suggestions.md}
├── queue/{job-id}.json
├── instincts/{instinct-id}.md
├── logs/{job-id}.log
├── promotion-receipts/{receipt-digest}.json
├── promotion-outcomes/{receipt-digest}.json
├── promotion-changesets/{receipt-digest}.patch
└── state/{locks,brief-markers,review-ledger,promotion-previews,installation-receipt}
```

Directories and private state files use owner-only permissions where supported. Atomic writes
create a temporary sibling and replace the destination. Locks are created exclusively and are
always narrow to extraction or promotion execution.

### Configuration and authentication

The default is disabled with no acknowledgement. First enablement records the acknowledgement
and verifies a Claude executable. The extraction subprocess inherits credentials but never
persists them.

Because the worker invokes `claude --bare`, ordinary Claude subscription OAuth/keychain state
is not used. This release supports an inherited `ANTHROPIC_API_KEY` or supported Bedrock,
Vertex AI, or Microsoft Foundry provider credentials. It does not pass `--settings`, so an
`apiKeyHelper` configured only in Claude settings is not consumed. Setup must preflight this
before capture is enabled.

### Evidence and idempotence

The Claude normalizer reads JSONL defensively, accepts only user/assistant text blocks,
excludes sidechains and non-conversation records, removes context-only wrappers, redacts known
secret forms, and applies newest-first turn/character ceilings. Eligibility is checked after
normalization.

The transcript file's SHA-256 is stored with the evidence but never altered. The job ID binds
`claude`, session ID, transcript digest, and schema version. A second delivery resolves the
same queue path and returns without duplicating evidence.

### Queue and worker

| State | Meaning | Allowed progression |
|---|---|---|
| `queued` | Captured and ready | `processing` |
| `processing` | One worker holds a lease | `completed`, `retryable`, `failed` |
| `retryable` | Attempt failed or stale lease recovered | `processing` |
| `completed` | Valid suggestion file exists, including zero candidates | Human review |
| `failed` | Attempt ceiling reached | Explicit retry to `queued` |

The extraction command uses the exact configured model and includes `--bare`, `-p`, JSON
output, the bundled JSON Schema, `--max-turns 1`, `--no-session-persistence`,
`--permission-mode dontAsk`, and `--tools ""`. The empty tool set disables built-in tools;
`--disallowedTools "mcp__*"` explicitly denies MCP tools. The only standard input is the
minimized evidence message array. Output is accepted only from the structured-output envelope
and then validated again by deterministic code.

### Review and retention

The backlog parser creates three buckets and exact `type + normalized rule` clusters. Voice
has the highest review-area weight, followed by workflow, scope, correction, and confirmation;
support and skill/cwd breadth contribute deterministically. Listing does not mutate.

The confirmed review command appends one schema-v2 decision event whose occurrences bind the
session, transcript-derived job, suggestion result, and pre-processing audit digests. For
`accept`/`edit` it also writes one complete instinct; exact `match` updates only a
same-type/same-rule active instinct. `reject` creates no instinct. Once every cluster occurrence
in an audit has an exact matching authorization, the runtime marks it processed and deletes
only its evidence file. Legacy or malformed ledgers fail closed.

### Promotion receipts and execution

The preview serializer reads the exact target and source guidance, then produces full resulting
text under the managed heading. Its canonical digest covers every action field, including the
source-guidance digest. Approval verifies the
preview digest, rechecks the target digest, embeds the unchanged action in a receipt, and
canonically digests that receipt.

The executor verifies the receipt and target again. Local delivery atomically writes and
verifies the exact result, then marks the instinct `promoted` or duplicate `covered`. Review
delivery emits a unified diff and records `awaiting_review` without target mutation. Only a
valid same-receipt outcome bound to the approved target/result makes repeat execution a no-op.
An interrupted exact local write is recognized by its approved resulting digest and completed
without rewriting the target.

## Codex model and route parity

The nested `scripts/instinct_review.py` and `pmm_instinct/` implementation continues to own
Codex state under `~/.codex/instinct-review/`, use the existing plugin hooks and queue states
(`queued`, `running`, `succeeded`, `failed`), and retain bounded backfill, human review, and
confirmed destination application.

### Persisted model flow

The default config stays disabled and leaves `extractor_model` null so the package never
publishes an adopter choice. First `on` either receives a non-empty `--model` or reuses a
non-empty persisted value. It writes the normalized model before `enabled: true`, then runs
preflight. New SessionEnd and backfill capture resolve the model only from config; event or
native-history metadata cannot override or supply it. A legacy enabled/null-model store returns
`skipped` / `unconfigured_model` before normalization or artifact creation. Status remains
read-only and preflight reports `model_policy: false` until the operator repairs the config
through `on --model <exact-model>`.

Existing queued jobs with their own explicit non-empty model remain drainable. No read-only
command or config load rewrites legacy state.

### Route parsing and confinement

`run_routes` maps one source skill to one relative `references/RUN-*.md` value.
`voice_ref_routes` parses its legacy string or an ordered non-empty list of relative
`references/REF-*.md` values and removes duplicates without changing first-occurrence order.
Parsing rejects wrong types and empty list values.

Resolution starts from independently discovered user-owned roots for the exact source-skill
slug. Each candidate is canonicalized and must stay within that root, match the requested
filename family, be an existing writable regular file, and remain outside the package/plugin
cache. Absolute paths, `..`, cross-skill paths, directories, symlink escapes, missing paths,
wrong families, and non-writable files are ineligible. A configured value never expands the
search boundary.

Without a configured RUN, existing dynamic discovery is a fallback only when it yields one
eligible path. One eligible RUN/REF produces the ordinary applicable preview. Multiple paths
produce only `applicable: false`, `reason: multiple-eligible-targets`, and exact absolute
`eligible_targets`. The CLI exposes `--target` only as an exact member selector. Preview and
apply recompute eligibility; they reject stale or arbitrary values and never pick the first
candidate based on filesystem or configuration order.

### Unchanged adapters

Portable mode still requires an explicit safe state root and imported candidate JSON, with
capture/extraction/promotion unavailable. Claude modules, state, hooks, extraction, review,
receipts, and promotion are unchanged apart from shared package/version documentation. Codex
does not gain Claude's immutable approval receipts, outcome ledger, or detached promotion
executor in this release.

## Requirement traceability

| Requirement | Primary implementation | Minimum test evidence |
|---|---|---|
| PIRC-REQ-001 | both manifests, package-root Claude runtime/assets, preserved nested runtime | isolated copied-package closure |
| PIRC-REQ-002 | installer, nested skill, user settings hooks | symlink/copy, backup, conflict, narrow uninstall |
| PIRC-REQ-003 | config defaults and capture control | status non-enabling, acknowledgement and auth failure |
| PIRC-REQ-004 | hook script, worker summary, and hook manifest | no retained-store scan or subprocess model call in hook; forced detached launch |
| PIRC-REQ-005 | normalizer/capture core | role/tool/sidechain/subagent/redaction/bounds matrix |
| PIRC-REQ-006 | extractor assets and worker | exact flags/model/stdin; zero/positive/invalid/failure |
| PIRC-REQ-007 | digest ID, atomic queue, lease/locks/retry | duplicate, stale lease, ceiling, manual retry |
| PIRC-REQ-008 | review CLI, ledger, cleanup | list-only, decisions, exact match, multi-candidate retention |
| PIRC-REQ-009 | preview, receipt, executor | missing confirmation, tamper, drift, apply, idempotence |
| PIRC-REQ-010 | destination validator | allowed pairs and forbidden package/state/cache targets |
| PIRC-REQ-011 | explicit resolver and installer modes | no ambient/cross-runtime fallback; update behavior |
| PIRC-REQ-012 | both RUNs and output template | closure and native-machine setup receipt review |
| PIRC-REQ-013 | fictional Claude subtree | schema, cross-ID, canonical digest, exact before/after diff |
| PIRC-REQ-014 | compatibility loaders, existing nested and Claude runtimes/tests | legacy state plus full Claude/Codex/portable regression |
| PIRC-REQ-015 | public policy/evidence/inventory | secret/path/provenance/narrative scans |
| PIRC-REQ-016 | validator, tests, release evidence | exact manifest diff and stop-before-merge check |
| PIRC-REQ-017 | Codex config, enablement, capture/backfill | fresh/reused/null model and event-metadata override tests |
| PIRC-REQ-018 | config template and RUN/REF route parser/resolver | string/list compatibility, ordered dedupe, root/family/confinement matrix |
| PIRC-REQ-019 | promotion preview/apply and CLI `--target` | single/ambiguous/stale/arbitrary target matrix; no first-candidate selection |

## Delivery sequence

1. **Contract:** update this blueprint, product requirements, both RUNs, state/output
   contracts, and test cases together.
2. **Package closure:** add the Claude manifest, hooks, assets, scripts, and nested-skill-aware
   installer; prove an isolated copy has no outside dependency.
3. **Install disabled:** exercise both installer modes in disposable Claude homes, preserve
   unrelated settings, and verify capture is off.
4. **Capture/extract:** exercise eligible and excluded fictional transcript cases, exact
   bare-mode credentials, queue recovery, and schema boundaries.
5. **Review:** prove listing is read-only, all mutations require confirmation, matching is
   exact, and retention waits for every decision.
6. **Promote:** prove exact preview/receipt continuity, local atomic execution, governed patch
   behavior, drift refusal, and idempotence.
7. **Codex parity:** prove model persistence precedes enablement, new jobs ignore event model
   metadata, null-model legacy capture creates nothing, and RUN/REF ambiguity requires an exact
   validated target.
8. **Compatibility/safety:** run the existing suite, complete fictional digest checks,
   repository validators, and privacy/provenance review.
9. **Pull request:** stage only approved paths, open one unmerged pull request, wait for checks,
   and leave final release as a maintainer decision.

## Test blueprint

| Family | Required cases |
|---|---|
| Closure | manifests, hooks, imports, assets, nested skill, installer in isolated package copy |
| Installer | disabled default, symlink/copy, exact two hooks, backup, idempotence, conflicts, unrelated settings, narrow uninstall |
| Claude auth/config | explicit root, no ambient fallback, acknowledgement, missing binary, missing bare-mode credentials, exact model |
| Normalization/capture | malformed JSONL, user/assistant text, tools/wrappers excluded, sidechain/subagent/worker excluded, redaction, bounds, minimum messages, digest duplicate |
| Hooks | no synchronous extraction, fast return, stale recovery, one-time brief, detached launch |
| Extraction | exact CLI flags/environment/stdin/schema, empty built-ins plus `mcp__*` denial, zero/positive output, invalid envelope/schema, timeout/nonzero result, sanitized log |
| Queue | atomic transitions, single lock, stale lease, attempt ceiling, manual retry |
| Review | three buckets, voice-first stable order, no mutation on list, all decisions confirmed, exact match, evidence-only cleanup |
| Promotion | eligibility, destination pairs, exact digests, no receipt without confirmation, tamper/drift, local write, duplicate, governed patch, repeat execution |
| Fixtures | exact file set, fictional-only data, linked IDs, canonical digests, before/after diff |
| Regression | complete existing Codex/portable suite and read-only legacy-state stability |
| Codex model authority | missing/blank/persisted model, persistence-before-enable, event mismatch, backfill, legacy null skip/no artifacts |
| Codex routes | exact configured RUN, unique discovered fallback, string/list REF, dedupe order, confinement, multiple-choice payload, exact/stale target |
| Governance | governed docs, links, package validator, secret/path scan, exact diff, Draft release evidence |

## Change checklist

Before altering behavior, update a requirement, the relevant RUN step, implementation mapping,
fixture/contract, and test together. Re-run the focused Claude suite, existing Codex/portable
suite, Codex model/routing matrix, full unit discovery, package/governance validators, link and privacy scans, and
`git diff --check`. Report any unavailable authenticated Claude smoke check rather than
substituting a different runtime.
