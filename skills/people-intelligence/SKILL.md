---
name: people-intelligence
description: Build a consented, evidence-backed stakeholder brief and message-preparation prompt from approved professional sources. Use for collaboration planning and meeting preparation; do not infer sensitive traits, scrape accounts, or act on external systems.
---

# People Intelligence

Use this skill only for a stated professional purpose and evidence the user is authorized to provide. It supports three modes: a standalone stakeholder brief, a relational brief using an explicitly supplied reference brief, and a delta brief using an explicitly supplied prior brief.

1. Read `references/REF-evidence-privacy.md` before examining person-specific material.
2. Confirm the subject, intended audience, professional purpose, authority to use the evidence, and whether the user wants standalone, relational, or delta mode.
3. Follow `references/RUN-workflow.md`. Use `assets/evidence-corpus-template.md` when evidence needs structuring and `assets/source-map-template.yaml` only for adopter-owned optional sources.
4. Render `assets/output-template.md` and `assets/writing-prompt-template.md`. Separate direct evidence from inference, cite the source and date for material claims, and preserve uncertainty or conflict.
5. Return the result in the conversation by default. Save only to an explicit user-chosen local path after confirmation; never publish, message, schedule, scrape, or mutate an external system.

Use `examples/EX-synthetic.md` only as a fictional formatting reference. It is not evidence about a real person or organization.
