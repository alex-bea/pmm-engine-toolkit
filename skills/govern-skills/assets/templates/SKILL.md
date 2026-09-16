---
name: skill-name
description: Describe the concrete job and when this skill should be used, including one useful boundary that prevents likely misrouting.
---

# Skill Name

## Job

State the outcome this skill produces and the evidence or inputs it may use.

## Workflow

1. Read the one registered workflow under `references/`.
2. Load only the standards, references, templates, and examples required for the selected
   mode.
3. Inspect current state before proposing a write.
4. Stop at every approval or authority boundary defined by the workflow.
5. Verify the observable result and report checks not run.

## Boundaries

- Preserve user intent and unrelated work.
- Keep mutable adopter data outside the installed skill package.
- Do not invent evidence, approval, ownership, lifecycle, or external authority.

## Output

Name the returned artifact, file destination behavior, and any required receipt.
