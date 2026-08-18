---
name: pre-read-sharpener
version: 1.0.0
description: Tighten a supplied executive pre-read into a decision-oriented document without research or invented facts.
references:
  - path: references/RUN-pre-read-sharpener-workflow.md
    role: runbook
---

# Pre-Read Sharpener

## Role

Review and rewrite an existing pre-read so an executive can make a decision quickly. Do
not generate a pre-read from scratch or add facts absent from the source.

## Triggers

- "sharpen this pre-read"
- "tighten this pre-read"
- "review my pre-read"

## Output

Return a concise rewrite with a decision request, context, options, tradeoffs,
recommendation, and open questions. Mark missing decision-critical information as
`[Missing]`.

Follow `references/RUN-pre-read-sharpener-workflow.md`.
