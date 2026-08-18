---
name: pmm-habits
version: 1.0.0
description: Run a reflective habits review against evidence the user provides; identify concrete next actions without accessing private services.
references:
  - path: references/RUN-pmm-habits-workflow.md
    role: runbook
---

# PMM Habits

## Role

Turn a user's stated professional habits and a supplied weekly evidence set into a concise
reflection. This skill does not access chat history, calendars, CRMs, or task tools.

## Triggers

- "run my habits check"
- "review my habits"
- "what should I apply this week"

## Inputs

- a habits list with observable behaviors
- a user-provided evidence set, such as notes, decisions, or drafts

## Output

For each habit, state the evidence, the relevant situation, and one next action. Never
invent a missed opportunity or attribute a statement to a person not present in the input.

Follow `references/RUN-pmm-habits-workflow.md`.
