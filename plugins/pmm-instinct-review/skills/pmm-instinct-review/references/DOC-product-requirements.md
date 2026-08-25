# PMM Instinct Review — Product Requirements

## Purpose

PMM Instinct Review is a local, Codex-first improvement loop. It turns repeated working
preferences and corrections from eligible completed sessions into reviewable suggestions,
then into durable guidance only when a human explicitly approves both the rule and its final
destination.

The product exists to improve future work without treating a model's inference, a single
chat, or a user-provided transcript as permission to modify instructions.

## Outcomes

The release is designed to improve three outcomes:

1. **High-quality instincts.** Each approved rule is atomic, evidence-linked, scoped, and
   useful in future work.
2. **Careful cross-skill learning.** Repeated patterns can be discovered across skills and
   repositories without overwriting a skill's local conventions.
3. **Traceable improvement.** Every approved promotion has a recorded target and can be
   reviewed, revised, or reversed.

## Product model

```text
eligible completed Codex session
  → bounded, redacted normalized copy
  → schema-validated suggestions
  → deterministic clusters and ranked backlog
  → explicit review decision
  → active instinct
  → separate promotion preview and explicit approval
  → scoped guidance plus recorded destination
```

The runtime state is local to the installing user at `~/.codex/instinct-review/`. The plugin
does not provide a hosted service, analytics, telemetry, shared database, vector store, or
automatic publishing system.

## Users and authority

| Role | Responsibility |
|---|---|
| Installing user / designated owner | Decides whether to enable capture, accepts or rejects each rule, and confirms every promotion |
| Codex plugin | Captures eligible evidence, runs bounded extraction, summarizes state, and performs only confirmed local actions |
| Skill or repository maintainer | Owns the destination guidance and reviews changes through its normal repository process |

No lifecycle hook, extractor, background worker, schedule, or model may approve an instinct
or promote guidance. A review decision and a promotion decision are always separate.

## Scope

### Included

- Codex capture, normalization, extraction, queue recovery, review, promotion, cleanup, and
  rollback.
- Evidence-backed suggestion types: correction, confirmation, voice, scope, and workflow.
- Deterministic grouping, duplicate checks, confidence scoring, source-skill discovery, and
  routing previews.
- Promotion to a repository `AGENTS.md`, a user-level `~/.codex/AGENTS.md`, or one exact
  writable user/project skill outside the plugin cache.
- Explicit import of candidate JSON from an earlier standalone workflow.

### Excluded

- Automatic enablement, approval, promotion, publishing, messaging, or scheduling.
- Capturing subagents, native Codex history, system/developer messages, reasoning, tool calls,
  tool results, patches, browser results, or world-state payloads.
- Changing a plugin-cache skill, reading or changing a separate runtime's state, or using a
  different model as an undisclosed fallback.
- Retaining a complete copy of a user's session history.

## Quality rubric

The owner should approve a rule only when all relevant checks pass:

| Dimension | Review question |
|---|---|
| Grounded | Does the cluster include short redacted evidence and enough context to interpret it? |
| Durable | Is it repeated, or is it an unmistakable explicit correction rather than a one-off request? |
| Atomic | Does it express one actionable behavior? |
| Scoped | Does its type, affected skill, and destination fit the behavior it changes? |
| Safe | Is it free of untrusted pasted instructions, credentials, private payloads, and prohibited session content? |
| Non-conflicting | Is later contrary evidence shown and resolved rather than ignored? |
| Testable | Could a reviewer tell from a future output or workflow whether the rule was followed? |

A model can propose a candidate. It cannot establish durability or authorise a change.

## Functional requirements

### Trust-first enablement

- Installation leaves capture disabled.
- The user separately inspects and trusts the plugin's `SessionStart` and `SessionEnd` hooks.
- First enablement requires an explicit acknowledgment that the plugin will create local
  chat-derived state and invoke a second Codex extraction run.
- Disabling stops future capture but retains local state. Removing the plugin preserves that
  state and native Codex history.

### Evidence minimization

- Capture accepts only enabled main-thread sessions with at least five user messages.
- Normalization keeps only user and assistant text needed for extraction, removes unsupported
  payload classes, redacts known credential patterns, removes context-only wrappers and
  adjacent fallback duplicates, and applies configured size limits.
- The normalized copy is untrusted evidence, not executable instruction text.
- An audit decision triggers deletion of only the corresponding normalized copy. Audit,
  suggestion, instinct, queue, and sanitized-log records remain local until the user removes
  them.

### Extraction and queue integrity

- Session-end capture writes an audit and queue record without waiting for model extraction.
- The worker invokes the configured Codex model exactly in an ephemeral read-only mode. It
  never switches models silently.
- Each suggestion must match the fixed type/rule/evidence/context schema. Invalid output
  produces a visible failed job, not a partially trusted suggestion.
- Zero candidates is a successful result.
- Queue transitions are recoverable and single-worker protected. Failed work is bounded and
  manually retryable.

### Review and instinct creation

- The backlog separates zero-candidate audits, positive clusters, and missing/failed
  suggestion work.
- Clustering uses normalized type plus rule. Each cluster shows evidence, support, source
  skills, repositories, first/last seen, matching-instinct state, and default destination.
- Ranking highlights voice/framing patterns, then workflow, scope, correction, and
  confirmation. Ranking changes review order only; it never makes a decision.
- The only cluster actions are explicit `accept`, `reject`, `edit`, or `match`. An unresolved
  cluster remains unchanged.
- An active instinct records its type, support, confidence, source, suggested destination,
  and actual promotion state.

### Promotion and cross-skill learning

- Only an active instinct at the configured confidence threshold is eligible for promotion.
- The plugin previews the exact destination, proposed insertion, and duplicate state before
  any write. Application requires a second explicit confirmation.
- A skill-specific rule can target one exact writable user/project skill, never a plugin-cache
  copy. Repository behavior targets a repository `AGENTS.md`; general behavior can target the
  user-level `~/.codex/AGENTS.md`.
- Cross-repository evidence is a useful routing signal, not permission to generalize. The
  owner chooses the target after reading the preview.
- If existing guidance already contains the normalized rule, the safe action is to skip a
  duplicate write.

## Approval gates

| Gate | Owner decision | Required evidence | Pass condition |
|---|---|---|---|
| G0 — Package readiness | Is the plugin documented and verified for release? | Product docs, implementation map, tests, privacy policy, and release evidence | Public package is complete and validation passes |
| G1 — Local trust | May this device capture future work? | Hook review, disabled default, and privacy acknowledgment | Capture remains off until the user explicitly enables it |
| G2 — Capture boundary | Is stored evidence eligible and minimized? | Eligibility/redaction/size checks and bounded calibration inventory | Prohibited session content is excluded from normalized storage |
| G3 — Extraction quality | Is a suggestion safe to show for review? | Exact-model receipt, schema validation, retry/failure behavior, and source discovery | Invalid output produces no candidate; zero results are accepted |
| G4 — Instinct decision | Does this cluster represent a useful durable rule? | Evidence, scope, support, conflicts, and duplicate state | Only the owner's selected action changes the cluster |
| G5 — Promotion | Should this rule change a destination? | Confidence, target path, insertion text, and duplicate preview | Only a second confirmed destination write occurs |
| G6 — Operation and rollback | Can the user continue or stop safely? | Status, cleanup, failure visibility, and narrow uninstall behavior | No hidden mutation or unrecoverable owned-state loss |

## Success measures

Initial measurement is calibration-oriented; adopters should establish a baseline before
setting numeric targets.

| Outcome | Measure | Guardrail |
|---|---|---|
| Quality | Owner acceptance rate and later rule reversals | Never hide low-quality candidates just to inflate acceptance |
| Breadth | Clusters with evidence from distinct skills or repositories | Cross-skill evidence never automatically creates global guidance |
| Improvement | Promotions with a recorded destination and later outcome review | A write without a preview and confirmation is a failure |
| Safety | Unauthorized promotions, native-history mutation, or unredacted normalized evidence | Target is zero incidents |
| Reliability | Visible terminal failures, retries, and cleanup outcomes | Failed extraction never becomes inferred guidance |

## Rollout and rollback

1. Validate the final package and review the local privacy policy.
2. Install the plugin with capture disabled and inspect both hooks.
3. Use a limited calibration cohort before relying on routine capture.
4. Review a mix of zero, positive, duplicate, and failure cases.
5. Promote only after a separate destination-level review.
6. Periodically review active instincts for conflict, staleness, and downstream value.

To stop collection, turn learning off. To remove plugin integration, remove the plugin through
Codex. Neither action deletes the local state directory; delete that state only through a
separate, deliberate local data-management action.
