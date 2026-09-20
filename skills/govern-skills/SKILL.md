---
name: govern-skills
description: Copy and adapt a documents-first skill-governance pattern into a repository, or audit and update an existing pattern. Use for skill structure, RUN/STD/REF architecture, lifecycle, approval gates, setup, readiness, setup receipts, validators, or optional enforcement layers; do not require a plugin or claim technical enforcement from documents alone.
---

# Govern Skills

## Job

Help a repository owner make AI skills understandable, maintainable, and honestly governed.
The default outcome is an adapted set of documents, templates, examples, and explicit
approval boundaries, not a plugin or security system.

## Route first

1. Inspect applicable repository instructions and identify the requested mode.
2. Treat these adopter-owned paths as stable defaults unless the repository already has a
   compatible convention:
   - configuration: `{authorized-workspace}/.agents/govern-skills/setup-config.yaml`;
   - readiness receipt: `{authorized-workspace}/.agents/govern-skills/setup-receipt.yaml`.
3. For an audit, repair, create/update, lifecycle, or enforcement request with a matching
   `ready` receipt, read `references/RUN-govern-skills-workflow-v1.1.md` and only the
   standards relevant to the decision. Do not load the setup contract during normal work.
4. For explicit setup, installation, configuration, verification, diagnosis, or repair of
   setup—or when the receipt is missing, stale, or blocked—read
   `references/REF-govern-skills-setup-contract.md` and follow its readiness route before
   normal execution.
5. For the bundled fictional test, use only the setup contract and
   `examples/fixtures/setup-smoke-test.md` in an isolated temporary directory.

## Operating boundary

- Inspect before writing. Present evidence, compatibility gaps, and an exact proposed file
  plan that follows compatible local conventions.
- Obtain approval for the exact write boundary, apply only that boundary, and verify the
  selected scope.
- Report each control as `instruction-only`, `static-validator`, `runtime-guard`,
  `capability-boundary`, or `external-authority`.
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
verification method. After approved setup, write the machine-readable readiness record from
`assets/setup-receipt.yaml`; use `assets/output-template.md` for detailed human-readable
evidence when the adopter requests it.
