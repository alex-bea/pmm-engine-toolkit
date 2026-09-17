---
doc_type: RUN
normative: true
requires:
  - STD-ai-skill-governance-prd-v1.0.md
  - STD-approval-gates-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-runtime-enforcement-v1.0.md
  - STD-skill-dependencies-v1.0.md
  - STD-skill-primitives-v1.0.md
  - STD-skill-structure-v1.0.md
status: Active
version: "1.1"
owner: alex-bea
consumers:
  - Claude Code users
  - Codex users
  - skill maintainers
change_control: Project owner approval
---

# Govern Skills Workflow

## 1. Preflight

Use this workflow only when the current setup receipt is `ready` for the requested
repository and scope. If setup is explicit or the receipt is missing, stale, or blocked,
return to `REF-govern-skills-setup-contract.md` before continuing.

Read applicable repository instructions, inspect Git state when available, and identify
the canonical skill roots, document conventions, registries, validators, and optional
enforcement surfaces. Preserve unrelated work. Load only the standards needed for the
selected mode.

## 2. Select one mode

- **Audit:** inspect skills, workflows, metadata, dependencies, lifecycle, evidence,
  approval boundaries, and actual enforcement layers. Report without writing.
- **Repair:** reproduce a deterministic finding, identify the owning rule, propose the
  smallest exact patch, obtain approval, apply it, and rerun focused checks.
- **Create or update:** separate discovery in `SKILL.md`, ordered execution in one RUN,
  stable rules in STDs, focused knowledge in REFs, output structures in templates,
  fictional depth in examples, and repeatable mechanics in scripts only when justified.
- **Lifecycle:** use the adopter's canonical registry when one exists. Do not create a
  registry merely because this package includes registry standards. Never choose owner,
  activation, deprecation, archival, or replacement state without authority.
- **Enforcement:** read `STD-runtime-enforcement-v1.0.md`; inventory alternate paths; put
  policy in one shared decision; keep harness adapters thin; test denial side effects; and
  distinguish runtime guards from protected capabilities and external authority.

## 3. Build the evidence record

For the selected scope, record current evidence, authority, compatibility gaps, applicable
standards, and each observed control's real class: `instruction-only`, `static-validator`,
`runtime-guard`, `capability-boundary`, or `external-authority`. Do not infer a stronger
layer from a weaker one or treat caller-supplied identity as verified human authority.

## 4. Propose the boundary

For each proposed path, show the action, primitive role, governing standard, selected
enforcement class, approval authority, and verification method. Reuse compatible local
conventions. Treat an existing differing canonical file as a conflict. Stop before writing
and obtain approval for the exact file plan or diff.

## 5. Apply approved changes

Recheck the target state, then modify only approved paths. Keep mutable configuration,
state, evidence, and receipts outside the installed package. Never invent owners,
lifecycle state, approval events, or publication authority. A material path or content
change invalidates the prior approval and returns the proposal to review.

## 6. Verify and report

Run positive and negative checks proportional to the selected control. Confirm that denied
side effects did not occur. Record failed, skipped, unavailable, and not-applicable checks
distinctly. Report the resulting control class and residual limitations; do not use the
unqualified word “enforced” when the actual layer is narrower.

If the work changes package dependencies, configuration, selected enforcement layers, or
the setup contract, mark the readiness receipt stale and route through setup repair.

## Error handling

| Condition | Required action |
|---|---|
| Repository root or controlling instructions are unresolved | Stop before writing and report the missing scope. |
| Canonical schemas or registries conflict | Present the conflict and request an owner decision. |
| Proposed paths differ from the approved plan | Invalidate write approval and return to review. |
| A validator contradicts a binding standard | Report a validator defect; do not redefine the standard silently. |
| Runtime policy cannot evaluate a sensitive action | Deny the action for that layer. |
| Human approval or external authority cannot be verified | Keep the gate pending. |
| Requested action exceeds documents-only scope | Stop and obtain separate approval for the optional layer. |
