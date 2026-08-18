```yaml
doc_type: RUN
normative: true
requires:
  - REF-pm-prioritizer-priority-framework-v1.0
  - BP-pm-prioritizer-output-template-impl-v1.0
```

**Status:** Draft v1.0
**Owner:** PMM Engine Contributors
**Consumers:** Claude AI Agent, pmm-plan-scaffolder
**Change control:** PR Review

---

## 0. Overview

The PM Prioritizer evaluates a build-driving plan and returns a scope decision: pass
through unchanged, narrow to an MVP slice with deferred work tracked, or skip entirely.
It is invoked by the plan scaffolder before the draft-package step, or directly by the
user.

---

## Step 0 — Accept Input

Accept the plan as markdown. The plan may arrive from:

- **Plan scaffolder:** full plan body passed programmatically during scaffolding
- **Direct invocation:** user pastes or references a plan doc

Validate that the input contains an actionable body. If the input is empty, ambiguous, or
contains multiple unrelated plans, ask one focused clarifying question and stop.

---

## Step 1 — Load Context (Silent)

Load all reference files silently:

1. `REF-pm-prioritizer-priority-framework-v1.0.md` — classification, lane, and
   pass-through rules
2. `BP-pm-prioritizer-output-template-impl-v1.0.md` — output format

If available, load current tracker state summary:

- Active task count and WIP headroom
- Active epics under the likely parent roadmap

Do not output anything during this step.

---

## Step 2 — Classify (Silent)

Determine the plan classification:

| Classification | Criteria |
|---|---|
| `execution_build` | Has actionable implementation changes, intended to become tracker-driving work, would create or update tracker tasks |
| `non_build_strategy` | Strategy, positioning, or analysis work that does not decompose into tracker tasks |
| `reference_only` | Exploratory, historical, or context-only; not part of active execution |

If classification is `non_build_strategy` or `reference_only`, return immediately with
`result: skipped` and a one-sentence reason.

Assign a lane:

| Lane | Criteria |
|---|---|
| `marketing` | Output-facing, GTM-adjacent, launch, narrative, release, or user-visible work |
| `foundation` | Workflow platform, governance, tracker, validation, and internal enablement work |

The lane maps directly to the tracker `team` field: `marketing` lane = `marketing` team,
`foundation` lane = `product` team.

Do not output anything during this step.

---

## Step 3 — Evaluate Pass-Through

A plan qualifies for pass-through when **all** of these hold:

1. Total estimated effort is 3 working days or less
2. No single task exceeds 2 working days
3. The plan serves one coherent job-to-be-done
4. No materially distinct deferred slice is required to make the MVP coherent

If pass-through: return with `result: pass_through`, the assigned lane, and a one-sentence
reason. The plan body is not modified.

---

## Step 4 — Scope Reduce

If the plan does not qualify for pass-through, narrow it to an MVP slice.

### Marketing lane MVP

The minimum viable launch slice: the smallest set of changes that produces one shippable
output or enables one user-facing capability.

### Foundation lane minimal enabling slice

The smallest change that directly unlocks one named next output task, workflow run, or
tracked decision. Constraints:

- Completes in 2 working days or less
- Touches one primary surface or contract
- Excludes generalization, framework hardening, multi-workflow rollout, and polish unless
  one of those is strictly required for the named unblock

**Good slice example:** "Add icebox rendering plus thaw-task recovery for PM Prioritizer
deferred slices so one prioritized plan can be recovered cleanly from the tracker."

**Bad slice example:** "Build a generalized deferred-work recovery framework across all
tracker workflows."

### Produce the split

1. Rewrite `## Implementation Changes` (or equivalent) to contain only MVP work
2. Move deferred work into structured slices with tier assignment:
   - `v1` — high-value follow-on, next after MVP ships
   - `v2` — lower priority or speculative, no timeline commitment
3. Move killed work into a killed list with one-sentence rationale each
4. Preserve the full plan structure; do not discard deferred content

---

## Step 5 — Format Output

Return the structured result using the template in
`BP-pm-prioritizer-output-template-impl-v1.0.md`.

No preamble. No commentary outside the structured output. If invoked by the plan
scaffolder, the output is consumed programmatically. If invoked directly, present the
output as a formatted markdown block.

---

## Error Handling

| Situation | Action |
|---|---|
| Input is empty or ambiguous | Ask one clarifying question, then stop |
| Plan has no implementation changes section | Return `result: skipped` with reason |
| Cannot determine lane | Default to `foundation` and note uncertainty in reason |
| Effort estimation is uncertain | Err toward not passing through; scope-reduce instead |
| Multiple unrelated initiatives in one plan | Flag as over-scoped; ask user to split before prioritizing |
