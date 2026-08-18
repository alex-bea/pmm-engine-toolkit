---
name: marketing-brief
version: 1.0.0
description: Turn supplied launch inputs into a concise, evidence-bound marketing brief without research or invented claims.
references:
  - path: references/RUN-marketing-brief-workflow.md
    role: runbook
---

# Marketing Brief

## Role

Create one decision-ready marketing brief from source material the user provides. Preserve
uncertainty: missing facts remain `[Missing]`; they are never inferred.

## Triggers

- "write a marketing brief"
- "brief this launch"
- "turn these notes into a brief"

## Output

Use the structure in the runbook: audience, problem, change, value, proof, positioning,
launch tier, risks, and open questions. Return separate briefs for unrelated launches.

Follow `references/RUN-marketing-brief-workflow.md`.
