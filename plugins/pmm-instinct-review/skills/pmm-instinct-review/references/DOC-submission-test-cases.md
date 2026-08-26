# PMM Instinct Review — Public Submission Test Cases

These test cases are written for a public plugin reviewer. They use only local, synthetic
inputs and do not require an account, private repository, credentials, or network service.
The final submission should include all five positive and all three negative cases.

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

## Reviewer notes

- The plugin is local-only and has no server, external connector, or reviewer credential.
- The plugin's own unit suite covers the same paths with synthetic fixtures, including
  rationale schema rejection, candidate-card routing separation, retry/recovery, duplicate
  coverage, confidence thresholds, staged multi-target writes, RUN/REF/standard routing,
  multi-candidate cleanup, and local-state persistence.
- If testing against a real Codex installation, use only a disposable profile or deliberately
  fictional conversations. Never provide real customer, employer, or personal content as a
  public submission fixture.
