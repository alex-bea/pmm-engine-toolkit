---
name: sales-one-pager
version: 1.0.0
description: Create a concise prospect-facing one-pager from approved product and customer inputs without research or invented claims.
references:
  - path: references/RUN-sales-one-pager-workflow.md
    role: runbook
---

# Sales One-Pager

## Role

Convert approved source material into either a prospect-specific or product-comparison
one-pager. Treat the supplied positioning sheet as authoritative; mark missing evidence
instead of filling gaps.

## Triggers

- "write a sales one-pager"
- "create a product one-pager"
- "prepare a prospect brief"

## Output

Return a single one-pager with the problem, relevant capability, evidence, differentiation,
implementation considerations, and a clear next step. Do not use customer names, logos,
pricing, or competitor assertions without explicit approval.

Follow `references/RUN-sales-one-pager-workflow.md`.
