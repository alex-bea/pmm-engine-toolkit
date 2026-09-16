---
name: govern-skills
description: Copy and adapt a documents-first skill-governance pattern into a repository, or audit and update an existing pattern. Use for skill structure, RUN/STD/REF architecture, lifecycle, approval gates, setup receipts, validators, or optional enforcement layers; do not require a plugin or claim technical enforcement from documents alone.
---

# Govern Skills

## Job

Help a repository owner make AI skills understandable, maintainable, and honestly governed.
The default outcome is an adapted set of documents, templates, examples, and explicit
approval boundaries, not a plugin or security system.

## Required workflow

1. For installation, setup, copying, configuration, first use, or readiness diagnosis, read
   `references/RUN-govern-skills-setup-workflow-v1.0.md` and
   `references/REF-governance-adoption-guide-v1.0.md` before any write.
2. For audits or updates, read the same RUN file's normal-execution section and only the
   `STD-*.md` files relevant to the decision.
3. Inspect applicable repository instructions, Git state, existing skill/document roles,
   naming, metadata, registries, validators, and optional harness surfaces.
4. Present evidence, compatibility gaps, and an exact proposed file plan. Adapt to
   compatible local conventions instead of imposing this package's layout.
5. Obtain approval for the exact write boundary, apply only that boundary, and verify the
   selected scope.
6. Report each control as `instruction-only`, `static-validator`, `runtime-guard`,
   `capability-boundary`, or `external-authority`.

## Boundaries

- A readable rule is not a runtime block, capability restriction, or human approval.
- Keep completed mappings, configuration, mutable state, outputs, and setup receipts outside
  the installed package.
- Never overwrite a conflicting canonical instruction, registry, schema, or validator.
- Do not invent owners, lifecycle states, approval events, or publication authority.
- Hooks, CI, registries, protected infrastructure, external verifiers, and publishers are
  optional layers that require separate selection, authority, and evidence.
- Preserve unrelated work and stop when a required source, destination, permission, or
  decision is unresolved.

## Output

Return a setup-readiness report or governance finding first. For a proposed change, include
the exact paths, action per path, selected enforcement class, approval authority, and
verification method. After an approved setup, write the receipt using
`assets/output-template.md` at the adopter-selected location.
