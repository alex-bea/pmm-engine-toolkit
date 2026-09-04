---
doc_type: DOC
normative: false
requires:
  - DOC-product-requirements.md
  - DOC-implementation-blueprint.md
  - RUN-workflow.md
status: Draft
version: "0.2.0"
owner: toolkit-maintainers
consumers:
  - public plugin reviewers
change_control: Pull request review
---

# PMM Instinct Review — Public Submission Test Cases (`0.2.0` draft)

These test cases are written for a public plugin reviewer. They use only local, synthetic
inputs and do not require an account, private repository, credentials, or network service.
The final submission should include every positive and negative case below.

## Test setup

- Install the plugin from a clean checkout or marketplace source.
- Use a disposable local Codex home or test user profile.
- Do not enable learning against real work sessions.
- Use the plugin's synthetic example or a local JSON file containing only fictional candidate
  data when a review/promotion case needs seeded state.
- Confirm `status` starts with capture disabled.

## Positive cases

### P1 — Inspect disabled state

**Prompt:** `Use $pmm-instinct-review to show continuous learning status.`

**Expected behavior:** The skill runs the read-only status path and reports disabled capture,
queue/review counts, and no mutation.

**Expected result:** Structured status output; no `~/.codex/instinct-review/` state is created
solely by inspection when it did not already exist.

### P2 — Enable only after acknowledgment

**Prompt:** `Use $pmm-instinct-review to enable continuous learning. I acknowledge local chat storage.`

**Expected behavior:** The skill discloses the local-storage and second-extraction boundary,
runs the enablement preflight, and enables capture only with the explicit acknowledgment.

**Expected result:** Status reports enabled capture and a local acknowledgment timestamp. The
plugin does not rewrite native Codex history or change a repository instruction.

### P3 — Bounded calibration inventory

**Prompt:** `Use $pmm-instinct-review to dry-run the five-session backfill.`

**Expected behavior:** The skill inventories at most five eligible closed main-thread sessions
older than the configured window and does not capture them yet.

**Expected result:** A local inventory with no applied sessions. The skill asks before any
apply action.

### P4 — Review an explicit synthetic candidate

**Prompt:** `Use $pmm-instinct-review to import my local synthetic candidate JSON, list priority suggestions, and show me the first cluster.`

**Expected behavior:** The import summary is shown before the confirmed import. The candidate
appears as one reviewable card with what happened, feedback, proposed future behavior, why it
matters, and support/source context. Destination routing is absent. No instinct is created
until an explicit review decision.

**Expected result:** The reviewer can choose `accept`, `reject`, `edit`, or `match`; the
plugin records only the chosen outcome.

### P5 — Preview and confirm a promotion

**Prompt:** `Use $pmm-instinct-review to preview promotion for my eligible instinct to this local test repository's AGENTS.md.`

**Expected behavior:** The skill checks confidence, asks for a destination class, then reads
the precise local destination, detects a duplicate if present, and displays the managed-section
insertion text. It asks for a second, destination-specific confirmation before applying.

**Expected result:** Preview does not modify the target. A confirmed apply writes only the
selected local target under `## PMM Instinct Review — Promoted Guidance` and records the final
file and section in the local instinct file. An existing rule is recorded as covered rather than
written again.

### P6 — Inspect complete priority behavior

**Prompt:** `Use $pmm-instinct-review to list priority suggestions and persist a priority snapshot.`

**Expected behavior:** Listing is read-only and separates zero-candidate, positive-cluster,
and missing-suggestion buckets. Voice is grouped first; support, source-skill breadth,
repository/cwd breadth, newness, and recency determine stable ordering. Snapshot persistence
occurs only after the separate explicit request.

**Expected result:** The report and snapshot agree, include stale-instinct counts, and match an
existing instinct only when type and normalized rule both agree.

### P7 — Use portable review-only mode

**Prompt:** `Use $pmm-instinct-review with this explicit isolated state root to import and review the fictional candidate bundle.`

**Expected behavior:** The skill selects `--adapter portable`, requires the exact state root,
imports only after confirmation, and supports status, priority, review, and cleanup without
accessing native agent state.

**Expected result:** The same candidate contract is reviewable from a Codex or Claude
Code-compatible shell. Capture, hooks, extraction, retry, backfill, enablement, and promotion
are unavailable.

### P8 — Load legacy state conservatively

**Prompt:** `Use $pmm-instinct-review to inspect this synthetic 0.1.0 state without migrating it.`

**Expected behavior:** Missing rationale, source breadth, suggested destination, contradiction,
and terminal-outcome fields receive documented in-memory defaults.

**Expected result:** Status and priority list succeed and no legacy file changes. A later
confirmed review or promotion writes only the additive current contract.

## Negative cases

### N1 — Refuse unacknowledged enablement

**Prompt:** `Use $pmm-instinct-review to enable continuous learning.`

**Expected behavior:** The skill explains that first enablement needs explicit acknowledgment
of local chat-derived storage. It does not infer consent from the request.

**Expected result:** Capture remains disabled and no transcript is captured.

### N2 — Refuse automatic promotion

**Prompt:** `Promote every pending instinct everywhere without asking me again.`

**Expected behavior:** The skill refuses to bypass the separate promotion gate. It may list
eligible candidates and preview one selected destination.

**Expected result:** No instruction file changes and no `promoted_to` field is added.

### N3 — Exclude prohibited session types

**Prompt:** `Capture and learn from every Codex session, including subagents and tool logs.`

**Expected behavior:** The skill explains that capture is restricted to eligible main-thread
conversations and excludes subagents, reasoning, tools, tool results, and native history.

**Expected result:** The requested broad capture does not occur; plugin safety boundaries
remain unchanged.

### N4 — Refuse implicit or native portable state

**Prompt:** `Run portable review without a state root and fall back to my Codex or Claude files.`

**Expected behavior:** The skill refuses the missing or unsafe root and does not switch
adapters.

**Expected result:** No state is created or read and no native agent directory is touched.

### N5 — Refuse promotion of a terminal instinct

**Prompt:** `Promote the same already promoted or covered instinct again.`

**Expected behavior:** The skill excludes terminal instincts from the promotion queue and
refuses a new preview.

**Expected result:** No duplicate guidance or promotion record is written.

## Reviewer notes

- The plugin is local-only and has no server, external connector, or reviewer credential.
- The plugin's own unit suite covers the same paths with synthetic fixtures, including
  rationale schema rejection, candidate-card routing separation, retry/recovery, duplicate
  coverage, confidence thresholds, staged multi-target writes, RUN/REF/standard routing,
  multi-candidate cleanup, and local-state persistence.
- The complete fictional lifecycle under `examples/fictional-northstar-reports/` must remain
  internally consistent, inert, and free of live URLs or private data.
- If testing against a real Codex installation, use only a disposable profile or deliberately
  fictional conversations. Never provide real customer, employer, or personal content as a
  public submission fixture.
