---
name: guidance-review
version: 1.0.0
description: Review marketing copy against a supplied claims guide and return a prioritized, evidence-based revision list.
references:
  - path: references/RUN-guidance-review-workflow.md
    role: runbook
---

# Guidance Review

## Role

Review marketing copy for claim accuracy, required disclosures, unsupported absolutes, and
audience clarity. Use only the copy and claims guide supplied for the review. This is a
writing-quality workflow, not legal advice.

## Triggers

- "review this marketing copy"
- "run guidance review"
- "check these claims"

## Inputs

- draft copy
- a product- or organization-approved claims guide
- the intended audience and publication channel

If the claims guide is missing, review for generic risks only and label the result
`needs approved claims guide`.

## Output

Return a table of findings with severity, quoted source text, concern, and a proposed
revision. Do not approve regulated, financial, health, legal, security, or availability
claims without an owner-approved source.

Follow `references/RUN-guidance-review-workflow.md`.
