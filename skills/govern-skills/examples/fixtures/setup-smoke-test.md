# Govern Skills Fictional Setup Smoke Test

This procedure uses only invented Acorn Studio data. Run it in a newly created temporary
directory, never in an adopter's production repository.

## Inputs

- the complete copied `govern-skills` package;
- `fictional-repository-map.yaml`;
- `setup-config.yaml`;
- `setup-receipt.yaml`; and
- the blank templates under `assets/`.

## Procedure

1. Copy the complete package to `packages/govern-skills` under the temporary root and
   record a digest of every package-relative path and byte.
2. Create `workspace/acorn-notes/AGENTS.md` and an empty
   `workspace/acorn-notes/agent-skills/` directory using synthetic content only.
3. Confirm the package contains exactly one `RUN-*.md`, named
   `RUN-govern-skills-workflow-v1.1.md`, plus the setup contract.
4. Create only the three output files declared by `fictional-repository-map.yaml` using the
   packaged templates and fictional Markdown receipt.
5. Copy the fictional setup configuration and YAML receipt to
   `workspace/acorn-notes/.agents/govern-skills/`.
6. Validate local links, required setup keys, expected file paths, non-collision behavior,
   and that all setup state is outside the installed package.
7. Compare the package digest with the value recorded in step 1.

## Expected result

- The package is unchanged.
- The three legacy expected files and two YAML setup-state files exist only under the
  isolated fictional workspace.
- The YAML receipt is `ready` for `documents-only`, points to
  `references/RUN-govern-skills-workflow-v1.1.md`, and marks optional layers not applicable.
- No plugin installation, hook activation, CI mutation, approval creation, messaging,
  notifications, scheduling, publishing, network call, or production-state write occurs.

Any missing path, collision, package mutation, failed check, or prohibited side effect
keeps the result `blocked`.
