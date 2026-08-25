---
name: example-skill
description: Describe the user outcome and the concrete situations that should trigger this skill.
---

# Example Skill

## Overview

State the job, boundaries, and non-goals in one or two sentences.

## Workflow

1. Inspect the repository and required inputs.
2. Load only the references needed for the selected task.
3. Produce an advisory plan before any write.
4. Request approval for local, external, or destructive changes at the applicable gate.
5. Execute deterministic helpers and verify the result.

## Inputs and missing information

- Name each required input.
- Preserve `[Missing]` when a decision-critical fact is absent.
- Do not infer permission, evidence, or sensitive values.

## Output contract

State the output path or format, evidence labels, assumptions, validation, and exit behavior.

## Resources

List only resources that actually exist in the skill package. State when to read each
reference, when to run each deterministic script, and which assets are copied into output.
Remove this section when the skill has no bundled resources.
