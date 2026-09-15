# Fictional Marketing Brief Behavior Cases

> **Fictional test fixture:** Every organization, launch, person, date, and fact below is
> invented. These cases define expected workflow behavior and are not evidence for a real
> product or market.

Use these cases to review the behavior described by `references/RUN-marketing-brief-workflow.md`.
They are deliberately compact and do not replace the complete fictional source-to-brief
example.

## CASE-MB-001: Source conflict

**Supplied input**

- Approved product specification: the feature exports CSV files only.
- Approved launch plan: launch date is November 12, 2026.
- Working meeting note: the feature exports CSV and PDF files on November 5, 2026.
- Two equal-authority approved messaging notes give different CTAs.

**Expected behavior**

- Use CSV-only scope from the product specification.
- Use November 12, 2026 from the approved launch plan.
- Do not blend the conflicting CTAs; mark the required CTA `[Missing]` and request a decision.

## CASE-MB-002: Tier selection

**Supplied input**

- Case A explicitly assigns Tier 3 to a small settings-label update.
- Case B describes a moderate feature launch across four approved channels without an
  assigned tier.
- Case C provides too little information to distinguish Tier 1 from Tier 2.

**Expected behavior**

- Preserve the explicitly approved Tier 3 in Case A.
- Apply the framework and select Tier 2 for Case B.
- Use the documented Tier 2 ambiguity default for Case C.

## CASE-MB-003: Multiple launches

**Supplied input**

- Launch A adds saved dashboard filters on October 8, 2026.
- Launch B adds workspace export controls on November 3, 2026.
- The launches share an audience but have different scope, timing, messages, and goals.

**Expected behavior**

- Report that two distinct launches were found.
- Produce two separate seven-section briefs.
- Do not use one launch to fill gaps in the other.

## CASE-MB-004: Missing information and research request

**Supplied input**

- A working note names a feature and primary audience but provides no approved owner, date,
  CTA, proof, distribution, or success goal.
- The user asks the agent to search the web for the missing details.

**Expected behavior**

- Decline to research or retrieve missing facts.
- Fill only supported fields.
- Mark unsupported required fields `[Missing]` and omit only optional fields the template
  permits the agent to omit.

## CASE-MB-005: Scoped edit

**Supplied input**

- A complete seven-section brief already exists.
- The user supplies an approved replacement CTA and asks to update Messaging only.

**Expected behavior**

- Update the CTA and any clearly required consistency reference.
- Preserve all seven sections and recheck every applicable limit.
- Return the full revised brief rather than an isolated Messaging fragment.
