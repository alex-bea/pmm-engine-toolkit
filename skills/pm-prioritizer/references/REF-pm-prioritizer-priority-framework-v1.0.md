```yaml
doc_type: REF
normative: true
requires: []
```

**Status:** Draft v1.0
**Owner:** PMM Engine Contributors
**Consumers:** Claude AI Agent, pm-prioritizer RUN workflow
**Change control:** PR Review

---

## 0. Purpose

This reference defines the classification, lane assignment, pass-through criteria, and
scope-reduction rules used by the PM Prioritizer.

---

## 1. Plan Classification

| Classification | When to assign |
|---|---|
| `execution_build` | The plan has actionable implementation changes, is intended to become a tracker-driving `PLAN` doc, and would reasonably create or update tracker tasks. Includes infra, governance, and tooling work — not just marketing output. |
| `non_build_strategy` | Strategy, positioning, or analysis that does not decompose into tracker tasks. Research plans, competitive landscape reviews, and narrative frameworks fall here. |
| `reference_only` | Exploratory, historical, or context-only. Would not drive any tracker work even if promoted. |

**Rule:** classify based on what the plan *does*, not what it *says about itself*. A plan
titled "Strategy" that contains concrete implementation steps is `execution_build`.

---

## 2. Lane Assignment

| Lane | Maps to tracker `team` | Assign when |
|---|---|---|
| `marketing` | `marketing` | The primary output is user-visible, GTM-adjacent, launch-related, narrative, release, or content work |
| `foundation` | `product` | The primary output is workflow platform, governance, tracker, validation, skill infrastructure, or internal enablement |

**Tie-breaker:** if a plan has both marketing and foundation elements, assign based on the
*primary deliverable*. If genuinely joint, assign `foundation` and note in the reason.

---

## 3. Pass-Through Criteria

A plan passes through unchanged when **all four** conditions hold:

1. **Effort ceiling:** total estimated effort is 3 working days or less
2. **Task ceiling:** no single task exceeds 2 working days
3. **Coherence:** the plan serves one job-to-be-done with no materially distinct sub-goals
4. **Completeness:** no deferred slice is required to make the MVP logically coherent

If any condition fails, the plan must go through scope reduction.

**Estimation guidance:** estimate based on implementation complexity, not elapsed calendar
time. A task that requires 4 hours of focused work is ~0.5 working days.

---

## 4. Scope Reduction Rules

### 4a. Marketing lane — MVP slice

The minimum viable launch slice: the smallest set of changes that produces one shippable
output or enables one user-facing capability.

Prioritize:
- One complete output over partial versions of multiple outputs
- Working end-to-end flow over polished individual steps
- External visibility over internal polish

### 4b. Foundation lane — minimal enabling slice

The smallest change that directly unlocks one named next output task, workflow run, or
tracked decision.

Hard constraints:
- Completes in 2 working days or less
- Touches one primary surface or contract
- Must name the specific thing it unblocks

Exclude unless strictly required for the named unblock:
- Generalization across multiple workflows
- Framework hardening or abstraction
- Multi-workflow rollout
- Polish, documentation, and cleanup beyond what the unblock requires

### 4c. Deferred tier assignment

| Tier | Meaning | Assign when |
|---|---|---|
| `v1` | High-value follow-on | Clear user value, should ship next after MVP |
| `v2` | Lower priority or speculative | Nice-to-have, no timeline commitment, may never ship |

### 4d. Kill criteria

Kill a slice when:
- It serves a hypothetical future need with no current unblock target
- It duplicates capability that already exists elsewhere
- The effort-to-value ratio is clearly negative

---

## 5. Over-Trigger Policy

The prioritizer should run on every `execution_build` plan unless the user explicitly
bypasses with one of these phrases:

- "scaffold directly"
- "skip prioritization"

Over-triggering is better than missing a plan that needed scope reduction.

---

## 6. Bypass Recording

When a bypass phrase is detected, the prioritizer returns `result: skipped` with
`reason: user_bypass` so the scaffolder can record the decision.
