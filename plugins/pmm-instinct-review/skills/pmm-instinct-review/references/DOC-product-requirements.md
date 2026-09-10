---
doc_type: DOC
normative: false
requires: []
status: Draft
version: "0.3.0"
owner: toolkit-maintainers
consumers:
  - Claude Code adopters
  - Codex adopters
  - public plugin reviewers
change_control: Pull request review
---

# PMM Instinct Review — Product requirements (`0.3.0` draft)

## Purpose

PMM Instinct Review is a local improvement loop that turns repeated, evidence-backed working
preferences into durable instructions without allowing a model, hook, or schedule to approve
its own guidance. `0.3.0` adds self-contained native Claude Code capture, extraction, review,
and receipt execution to the existing Codex and portable package.

The binding operator procedures are `RUN-workflow.md` and, for native Claude adoption,
`RUN-claude-setup.md`. This document defines outcomes and guardrails; it does not authorize a
release or the promotion of any particular rule.

## Users and outcomes

| User | Need | Outcome |
|---|---|---|
| Claude Code adopter | Install from a Toolkit checkout without a marketplace | Discoverable personal skill, two owned hooks, disabled default, complete local runtime |
| Claude Code user | Learn from eligible completed sessions | Fast minimized capture and detached exact-model extraction in a Claude-owned store |
| Codex user | Continue the existing native workflow | No change to Codex commands, state, hooks, or approval boundaries |
| Portable user | Review an explicit candidate bundle | Isolated review-only workflow without native-store access |
| Reviewer | Decide whether a pattern is durable | Evidence card and an explicit `accept`, `reject`, `edit`, or exact `match` decision |
| Instruction owner | Promote an eligible instinct | Exact destination preview, separate approval, immutable receipt, bounded execution |
| Toolkit maintainer | Review a public candidate | Complete tests, fictional examples, provenance/privacy evidence, and an exact diff |

## Runtime ownership

| Runtime | State | Native session source | Global instruction target |
|---|---|---|---|
| Claude standalone | `~/.claude/pmm-instinct-review-data/` | Claude transcript named by native hook, read-only | `~/.claude/CLAUDE.md` |
| Claude local plugin | `${CLAUDE_PLUGIN_DATA}/instinct-review/` | Claude transcript named by native hook, read-only | `~/.claude/CLAUDE.md` |
| Codex | `~/.codex/instinct-review/` | Eligible Codex rollout, read-only | `~/.codex/AGENTS.md` |
| Portable | Required explicit safe root | None | None |

No runtime may infer, merge, migrate, or fall back to another runtime's store. Mutable state
must remain outside the installed package.

## Goals

1. Make one public package self-contained for native Claude, existing Codex, and portable use.
2. Provide a detailed, no-marketplace Claude setup path that preserves unrelated user state.
3. Keep native lifecycle hooks fast; run all model work in a detached recoverable worker.
4. Minimize and redact evidence before persistence or model processing.
5. Preserve separate human gates for candidate review and exact promotion approval.
6. Allow background execution only after an immutable digest-bound approval receipt exists.
7. Preserve public `0.2.0` Codex and portable behavior without destructive migration.

## Non-goals

- Auto-accepting a candidate, creating an approval receipt, or weakening confirmation.
- Merging governed patches, approving pull requests, publishing, or sending instructions to a
  hosted PMM service.
- Reading Claude desktop chats, silently backfilling Claude history, or capturing a transcript
  that a native lifecycle hook did not identify.
- Requiring a marketplace, connector, database, vector store, or telemetry service.
- Directly writing governed `RUN-*.md`, `REF-*.md`, or `STD-*.md` files from a worker.
- Deleting native history or adopter-owned state during disable or uninstall.

## Functional requirements

### PIRC-REQ-001 — Self-contained dual-runtime package

Every Claude manifest, hook, script, prompt, schema, setup document, and runtime dependency
must resolve inside `plugins/pmm-instinct-review/` or its explicit adopter-owned state. The
existing Codex and portable files remain available. No public file may resolve a private
checkout or author-specific path.

### PIRC-REQ-002 — Standalone Claude install without a marketplace

The package-root installer supports live-symlink and pinned-copy modes. A fresh state root is
disabled; a valid receipt-owned upgrade preserves and truthfully reports existing state. An
unowned pre-enabled or pre-acknowledged root is refused. The installer links the nested skill
at `~/.claude/skills/pmm-instinct-review`, owns exactly one `SessionStart` and one
`SessionEnd` settings handler, preserves unrelated settings, backs up a changed settings
file, refuses occupied destinations, and performs a narrow uninstall that preserves state.

### PIRC-REQ-003 — Disabled default and explicit privacy acknowledgement

Install and status do not enable capture. First enablement requires an explicit acknowledgement
that bounded redacted user/assistant text is stored locally and sent to the configured Claude
model. Missing Claude fails closed. The setup procedure must keep capture disabled until its
separate bare-mode authentication preflight succeeds.

The extractor uses Claude Code `--bare`. It cannot use an ordinary Claude subscription
login/keychain. This candidate supports an inherited `ANTHROPIC_API_KEY` or supported
Bedrock, Vertex AI, or Microsoft Foundry provider credentials; the installer does not store
credentials and the runtime does not pass a custom `--settings` file.

### PIRC-REQ-004 — Fast non-model hooks

`SessionEnd` performs only consent/eligibility checks, atomic capture-request spooling, and a
fully detached launch. The worker streams normalization and atomic evidence persistence before
extraction. `SessionStart` performs only fixed layout validation, a forced detached launch, and
one bounded read of the worker-produced status snapshot; stale recovery, review reconciliation,
and retained-store enumeration run in the worker. It may emit one bounded snapshot brief. No
lifecycle hook invokes a model. Hook commands use package-relative or
installer-resolved paths and a supported Claude command-hook shape. The standalone settings
handler carries its own shutdown budget. The optional plugin handler is asynchronous because a
plugin timeout cannot extend Claude Code's shared SessionEnd budget; standalone installation is
required for reliable non-interactive `claude -p` capture.

### PIRC-REQ-005 — Minimized isolated Claude evidence

Capture accepts only enabled, acknowledged main sessions meeting the post-normalization user
message minimum. It excludes sidechains, subagents, workers, extractors, system/developer
content, context-only wrappers, reasoning, tools, results, patches, and world state. It keeps
only bounded redacted user/assistant text in one private evidence object under the explicit
Claude state root. Native history is read-only.

### PIRC-REQ-006 — Bounded Claude extraction

The worker uses the exact configured model, `--bare`, JSON output, the bundled JSON Schema,
one maximum turn, no session persistence, non-interactive permissions, an empty built-in tool
set, and explicit `--disallowedTools "mcp__*"` so MCP tools are unavailable. It sends only
bounded evidence on standard input, accepts zero to five validated candidates, treats zero as success, and
persists neither raw stderr nor evidence text in operational logs.

### PIRC-REQ-007 — Recoverable idempotent queue

Jobs bind runtime, session ID, transcript digest, and schema version. Claude states are
`queued`, `processing`, `retryable`, `completed`, and `failed`. Writes and locks are atomic,
stale leases recover, automatic attempts stop at the configured ceiling, manual retry is
explicit, and duplicate hook delivery cannot create another job.

### PIRC-REQ-008 — Human-gated review and retention

Claude provides read-only priority listing, explicit zero-candidate resolution, and confirmed
`accept`, `reject`, `edit`, and exact type-aware `match`. A worker never creates an instinct.
Normalized evidence is deleted only after every candidate in its audit has a human decision;
audits, suggestions, decisions, instincts, and sanitized state remain.

### PIRC-REQ-009 — Receipt-bound promotion automation

Promotion first produces an exact preview binding instinct, destination class, delivery mode,
target path, current target digest, rule, rationale, insertion, full resulting text, and
resulting digest. A separate confirmed command creates an immutable receipt. Only then may a
worker apply the exact local result or create an exact governed review patch. Execution is
idempotent, reuses an existing approval for the same preview, binds outcomes to the approved
target/result, recovers an exact write interrupted before outcome persistence, and refuses
target drift or receipt tampering.

### PIRC-REQ-010 — Narrow destinations and delivery modes

- `global`: local-only to `~/.claude/CLAUDE.md`;
- `project`: local-only to an exact `CLAUDE.md`;
- `skill`: review-only to an exact `RUN-*.md` or `REF-*.md`; and
- `standard`: review-only to an exact `STD-*.md`.

Installed packages, plugin caches, and runtime state are never valid destinations. Governed
review delivery writes a patch and does not change its target.

### PIRC-REQ-011 — Explicit ownership and updates

Every command receives an explicit standalone state root, plugin-data root, or deliberately
configured `PMM_INSTINCT_STATE_ROOT`. Symlink installs follow a validated Toolkit checkout;
copy installs remain pinned until deliberate replacement. Disable and uninstall preserve
state. No mode infers an ambient home-directory store.

### PIRC-REQ-012 — Detailed setup and truthful receipts

`RUN-claude-setup.md` covers boundary disclosure, closure, authentication preflight,
check/install, hooks, discovery, consent, smoke testing, extraction, review, receipt promotion,
update, disable, conflicts, and uninstall. A final receipt distinguishes passed, failed, and
not-run stages and may not claim native readiness without an authenticated lifecycle check.

### PIRC-REQ-013 — Complete fictional examples

One independently authored Northstar Reports scenario covers installation, configuration,
minimized evidence, queue, suggestion, decision, instinct, promotion preview/receipt/outcome,
governed patch behavior, and before/after Claude instructions. Every value is fictional;
network values use `.invalid`, and linked digests are internally consistent.

### PIRC-REQ-014 — `0.2.0` compatibility

Existing Codex and portable commands, hooks, state contracts, examples, and tests remain valid.
The Claude runtime is additive, standard-library only, and isolated. Status/list operations do
not destructively migrate or rewrite legacy state.

### PIRC-REQ-015 — Public privacy, provenance, and security

The candidate contains no private session, state, identifier, destination, credential,
author-machine path, or reversible alias map. Public review includes secret/path scans, human
narrative review, Draft rights/privacy evidence, and exact-set provenance inventory. Example
paths are clearly fictional.

### PIRC-REQ-016 — Exact release boundary

Only approved manifest paths may change. Focused and complete tests and repository validators
must pass. Release evidence reports checks actually run. Background workers cannot approve,
merge, publish, or bypass the final pull-request review.

## Approval gates

| Gate | Human decision | Pass condition |
|---|---|---|
| G0 — Package | Is this exact candidate ready for review? | Complete package, Draft evidence, exact diff, tests pass |
| G1 — Local trust | May hooks be installed and trusted? | Skill and both hook commands inspected; unrelated settings preserved |
| G2 — Privacy | May future sessions be captured? | Exact acknowledgement plus supported bare-mode credentials |
| G3 — Evidence/extraction | Is the result safe to review? | Eligible minimized evidence; exact model; schema-valid zero-to-five output |
| G4 — Instinct | Is this cluster a durable rule? | User explicitly accepts, rejects, edits, or matches; no routing at this gate |
| G5 — Promotion | May this exact destination/result be executed? | Exact preview digest receives a separate confirmation; target remains unchanged |
| G6 — Governed delivery/release | May a patch or package advance? | Normal repository and pull-request review; receipt never substitutes for it |

## Reliability, privacy, and rollback

- State writes are atomic and worker ownership uses narrow locks.
- Extraction failures become bounded `retryable` or visible terminal `failed` state.
- Operational logs are transcript-free and errors are sanitized.
- Native history remains untouched; normalized evidence follows decision-complete retention.
- `off` stops new capture. Uninstall removes only owned hook entries and the personal-skill
  symlink. State deletion and promoted-rule reversal are separate user/governance actions.

## Compatibility and safe degradation

Claude CLI flags and hook schemas are external interfaces. Unsupported hosts remain disabled
and report the exact missing capability. A Claude subscription login alone does not satisfy
the bare-mode extractor authentication prerequisite. Portable mode is an explicit alternative,
not a silent fallback for failed native setup. A missing native smoke check blocks a readiness
claim but does not affect the existing Codex/portable workflow.

## Acceptance summary

The public submission must prove package closure; standalone install/rollback; consent and
isolation; capture privacy and hook timing; exact background extraction; queue recovery;
human review and retention; receipt-bound local and governed delivery; fictional digest
integrity; Codex/portable regression; public safety; exact diff; and a stop before merge.
Detailed cases are in `DOC-submission-test-cases.md`.
