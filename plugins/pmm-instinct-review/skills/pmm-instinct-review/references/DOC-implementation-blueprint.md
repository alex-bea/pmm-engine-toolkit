# PMM Instinct Review — Implementation Blueprint

## Purpose

This document maps the public plugin's product requirements to its implementation. It is for
maintainers and work AIs changing the package. The executable user procedure remains in
`RUN-workflow.md`.

## Design rules

1. Keep model work bounded by a fixed input boundary and strict output schema.
2. Keep all path resolution, queue handling, clustering, scoring, routing, and retention
   deterministic and testable.
3. Preserve the two human gates: candidate-to-instinct and instinct-to-promotion.
4. Treat normalized session text as untrusted data. Never execute it as an instruction.
5. Preserve native Codex history and mutate only files owned by the user's local runtime.
6. Prefer a narrow skill or repository destination over general user-level instructions.
7. Keep this package self-contained: standard-library Python, plugin-relative paths, local
   configuration, and no private registry or repository dependency.

## Component map

| Component | Path | Responsibility |
|---|---|---|
| Plugin manifest | `.codex-plugin/plugin.json` | Declares the installable plugin and public metadata |
| Marketplace record | `.agents/plugins/marketplace.json` | Makes the plugin available from the repository marketplace |
| Hooks | `hooks/hooks.json` | Declares plugin-root-resolved SessionStart and SessionEnd commands |
| Skill entrypoint | `skills/pmm-instinct-review/SKILL.md` | Routes user requests and carries the safety contract |
| Operator CLI | `scripts/instinct_review.py` | Parses commands and enforces explicit confirmation flags |
| Runtime core | `scripts/pmm_instinct/runtime.py` | Capture, normalization, queueing, extraction, clustering, review, routing, promotion, and cleanup |
| Extractor assets | `assets/extractor-prompt.md`, `assets/extractor-schema.json` | Bounded candidate task and accepted output shape |
| Operator runbook | `references/RUN-workflow.md` | Binding procedure for enablement, review, promotion, retention, and rollback |
| Product docs | `references/DOC-*.md` | Product intent, implementation traceability, and submission test evidence |
| Test suite | `tests/test_instinct_review_plugin.py` | Synthetic end-to-end and contract coverage |

## Local state contract

```text
~/.codex/instinct-review/
├── config.json
├── sessions/
│   ├── YYYY-MM-DD-HHMM-{session-id}-audit.md
│   ├── {session-id}-normalized.jsonl
│   └── {session-id}-suggestions.md
├── queue/{session-id}.json
├── instincts/pmm-instinct-YYYY-MM-DD-NNN.md
├── logs/{session-id}.log
└── state/
```

This directory is user-owned, outside the plugin cache, and survives plugin removal. Do not
add another persistence location without updating the privacy policy, tests, and release
evidence.

## Data contracts

### Queue state

| State | Meaning | Permitted next state |
|---|---|---|
| `queued` | Eligible capture awaits extraction | `running` |
| `running` | The single worker owns the job | `succeeded` or `failed` |
| `succeeded` | A valid suggestion file exists; zero candidates is valid | Review |
| `failed` | Extraction did not complete or validate | Retryable queue state up to the configured limit, then manual retry |

Queue records use atomic writes. A worker lock prevents concurrent drains; it does not grant
approval or broaden any write capability.

### Candidate output

Accepted extractor output contains at most five objects with only these fields:

```json
{
  "type": "correction|confirmation|voice|scope|workflow",
  "rule": "one sentence",
  "evidence": "short redacted excerpt",
  "context": "bounded context"
}
```

The runtime validates type, fields, lengths, and source skill discovery before rendering a
suggestion. Model-supplied confidence, unrestricted destinations, or executable content are
not part of the contract.

### Instinct state

An owner-approved instinct contains a unique ID, type, confidence, support count, created and
last-seen dates, source context, suggested destination, and promotion record. A rejected
cluster creates no instinct. `match` updates only the exact active match.

## Requirement-to-test map

| Requirement | Covered in the public test suite |
|---|---|
| Plugin package is complete and public-safe | Manifest, marketplace, hook, runtime-dependency, and path tests |
| Capture is disabled and eligible-only | Default config, disabled capture, minimum turns, subagent, and idempotent capture tests |
| Normalized evidence is minimized | Event preference, fallback dedupe, excluded records, wrapper removal, redaction, and size-limit tests |
| Extraction is controlled | Configured-model, no-fallback, schema, valid worker, retry-limit, lock, and restart-recovery tests |
| Review requires a decision | Accept, reject, edit, match, zero-candidate, and multi-candidate cleanup tests |
| Promotion is separately gated | Threshold, preview, explicit confirmation, duplicate, project/global/both, and skill-target tests |
| Local state is recoverable | Cleanup retry, state durability, and independent plugin-path tests |
| Backfill is bounded | Five-session inventory and explicit-apply test |

## Change procedure

1. Read the product requirements, this blueprint, `RUN-workflow.md`, the privacy policy, and
   the relevant tests before editing behavior.
2. Classify the change: packaging, capture, normalization, extractor schema, queue, review,
   promotion routing, retention, or documentation.
3. For any behavior, approval, privacy, or retention change, update the product requirements
   and runbook in the same pull request.
4. Add or revise a synthetic test before relying on a new deterministic behavior.
5. Preserve plugin-relative paths and standard-library-only runtime behavior.
6. Run the complete public validation suite, regenerate the IP inventory, run a fresh secrets
   scan, and update the IP review whenever the published tree changes.
7. Do not make user capture active as part of a test, install, or release process.

## Release procedure

1. Run the full test suite, public package validator, workflow validator, and static
   whitespace check from a clean worktree.
2. Confirm all examples and test data are fictional, and that no personal data, credentials,
   internal identifiers, or private session artifacts enter the published tree.
3. Regenerate `docs/legal/IP-INVENTORY.csv`; it must match the final file list exactly.
4. Refresh the tracked-tree and reachable-history secrets-scan reports after the final
   documentation and code changes.
5. Update the IP-rights review and draft release notes with the final scope and known limits.
6. Open a focused pull request, wait for required hosted checks and independent review, then
   merge through the repository's branch-protection policy.
7. Create a release/tag only after the merge and final release checklist pass.

## Rollback procedure

If a release discovers a privacy, safety, or correctness issue, remove marketplace guidance
or release visibility through the repository's normal release controls, publish a fixed
version, and explain the affected behavior in release notes. Local users can turn learning off
immediately and remove the plugin; neither action should delete their local state without an
explicit separate request.
