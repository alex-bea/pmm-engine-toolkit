```yaml
doc_type: BP
normative: true
requires:
  - REF-pm-prioritizer-priority-framework-v1.0
```

**Status:** Draft v1.0
**Owner:** PMM Engine Contributors
**Consumers:** Claude AI Agent, pmm-plan-scaffolder
**Change control:** PR Review

---

## 0. Purpose

This blueprint defines the structured output format for the PM Prioritizer. The output is
consumed by the plan scaffolder to create MVP tasks and icebox placeholders.

---

## 1. Output Structure

```markdown
## Prioritizer Result

- **Result:** {pass_through | prioritized | skipped}
- **Classification:** {execution_build | non_build_strategy | reference_only}
- **Lane:** {marketing | foundation}
- **Reason:** {one-sentence explanation of the routing decision}

### MVP Scope

{If result is `prioritized`: the rewritten Implementation Changes section containing
only MVP work. If result is `pass_through`: "Plan passes through unchanged." If result
is `skipped`: "Plan skipped — not an execution build."}

### Deferred Slices

{If result is `prioritized`: one entry per deferred slice. If no deferred slices: "None."}

| # | Tier | Title | JTBD Summary | Source Section |
|---|---|---|---|---|
| 1 | v1 | {slice title} | {one-sentence job-to-be-done} | {plan section heading} |
| 2 | v2 | {slice title} | {one-sentence job-to-be-done} | {plan section heading} |

### Killed Slices

{If any slices are killed: one entry per killed slice. If none: "None."}

| # | Title | Reason |
|---|---|---|
| 1 | {slice title} | {one-sentence kill rationale} |
```

---

## 2. Field Rules

| Field | Constraint |
|---|---|
| `Result` | Exactly one of: `pass_through`, `prioritized`, `skipped` |
| `Classification` | Exactly one of: `execution_build`, `non_build_strategy`, `reference_only` |
| `Lane` | Exactly one of: `marketing`, `foundation` |
| `Reason` | One sentence. No hedging. State the decisive factor. |
| `MVP Scope` | Full replacement text for `## Implementation Changes`. Must be self-contained — a reader should understand the MVP without seeing deferred slices. |
| `Deferred Slices` | One row per slice. Title should be a clear, actionable phrase. JTBD Summary is one sentence describing the job the slice serves. Source Section is the plan heading the work was moved from. |
| `Killed Slices` | One row per slice. Reason is one sentence. |

---

## 3. Scaffolder Consumption Contract

When the plan scaffolder receives a `prioritized` result:

1. Replace the plan's `## Implementation Changes` (or `## What Changes`) with the MVP Scope text
2. Append deferred sections to the PLAN doc:
   - `## V1 Later` containing v1-tier deferred slices
   - `## V2 Later` containing v2-tier deferred slices (if any)
   - `## Killed or Parked` containing killed slices (if any)
3. Create one `icebox` tracker task per deferred slice, using:
   - `title` from the Deferred Slices table
   - `next_action` from the JTBD Summary
   - `slice_tier` from the Tier column
   - `source_plan_section` from the Source Section column
   - `slice_family_id` generated as `{epic-id}-{plan-stem}`

When the scaffolder receives `pass_through` or `skipped`, no plan modifications are made.
