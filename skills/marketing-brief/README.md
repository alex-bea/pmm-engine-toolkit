# Marketing Brief Starter Guide

## What this skill is

`marketing-brief` turns approved but messy launch material into one concise, structured
marketing brief per launch. It fills a fixed template. It does not research missing facts,
invent strategy, or turn the brief into a project plan.

Use it when you have a product specification, launch plan, messaging, customer notes, meeting
notes, or a mixture of those sources and need a reliable brief for review.

## Five-minute setup

Gather the sources you already have. You do not need every source, but the brief will be more
complete when you provide:

1. an approved product specification or PRD;
2. an approved launch plan with owner, timing, channels, and goals;
3. approved positioning or messaging;
4. customer, partner, sales, or beta notes tied to the launch;
5. optional approved terminology or product-naming guidance.

Paste the material, attach local files, or provide paths the agent is authorized to read.
Tell the agent which documents are approved and which are working notes. The skill never
requires a connector and does not browse for missing information.

## How it works

1. **Accept input:** Identify each distinct launch and the supplied sources.
2. **Resolve evidence:** Apply the source hierarchy and classify the launch tier.
3. **Fill the template:** Populate all seven sections using only supported facts. Mark
   unsupported required fields `[Missing]`.
4. **Return the brief:** Produce one complete brief per launch. Later edits preserve the
   full template.

## Source hierarchy

When sources disagree, the more authoritative source for that field wins:

1. final PRD or approved product specification;
2. approved launch plan or campaign brief;
3. approved PM, PMM, or go-to-market strategy;
4. approved messaging or positioning;
5. launch-tier framework;
6. launch-specific customer, partner, or sales notes;
7. meeting notes, brainstorms, or chat summaries.

See [`references/REF-source-priority.md`](references/REF-source-priority.md) for field
ownership and conflict rules.

## What you receive

Every brief uses this exact section order:

1. Brief Info
2. Launch Summary
3. Audience and Problem
4. Launch Scope and Value
5. Messaging
6. Distribution
7. Success

The reusable template is [`assets/output-template.md`](assets/output-template.md). The
fictional report-filter example includes both the
[`source packet`](examples/fictional-report-filters/source-packet.md) and its
[`completed brief`](examples/fictional-report-filters/marketing-brief.md).

## Invocation

In Claude Code, Codex, or another compatible agent, ask:

```text
Use $marketing-brief to turn these approved launch inputs into a concise brief.
```

If you provide material for two launches, the skill creates two briefs. If you request an
edit, it returns the complete updated brief rather than an isolated fragment.

## Package map

| File | Purpose |
|---|---|
| `SKILL.md` | Trigger, operating boundaries, and runtime routing |
| `references/RUN-marketing-brief-workflow.md` | Complete execution and error-handling procedure |
| `references/REF-source-priority.md` | Source ownership, conflicts, and missing-data rules |
| `references/REF-launch-tiers.md` | Generic Tier 1–3 classification and effort framework |
| `references/REF-evidence-and-privacy.md` | Package-local evidence and privacy safeguards |
| `assets/output-template.md` | Canonical seven-section output template |
| `examples/EX-synthetic.md` | Example index and interpretation guidance |
| `examples/fictional-report-filters/` | Complete fictional input and output pair |

## Limits

- No web research or source retrieval.
- No invented facts, claims, dates, metrics, customers, or proof.
- No campaign task plan, publishing, messaging, or external write.
- No adopter data is stored inside the installed skill.
- The fictional example demonstrates format and depth; it is not market evidence.

Maintainer review found real private outputs that exercise the canonical template. They were
used only to verify useful structure and depth and are not distributed with this package.
