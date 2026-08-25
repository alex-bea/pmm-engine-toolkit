---
doc_type: STD
normative: true
requires:
  - STD-ai-skill-governance-prd-v1.0.md
  - STD-skill-dependencies-v1.0.md
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Codex users
  - skill authors
change_control: Pull request review
---

# Skill Structure Standard

## Package location and naming

Use `.agents/skills/<skill-name>/` for repository-installed Codex skills. A source
distribution or plugin may use `skills/<skill-name>/` inside its own package. Use lowercase
kebab-case, keep names under 64 characters, prefer a short verb-led name, and make the
folder name equal the skill name.

## Package shape

```text
<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/        # detailed knowledge and workflow contracts
├── scripts/           # deterministic helpers
├── assets/            # templates and files copied into outputs
└── examples/          # synthetic inputs, outputs, and edge cases
```

Only `SKILL.md` is universally required. Include other directories only when they support
the skill's actual behavior. A public governed skill must also satisfy the dependency
closure standard.

## `SKILL.md` contract

YAML frontmatter must contain exactly `name` and `description`. Put version, owner,
lifecycle, dependencies, and deployment targets in the external governance registry or
manifest, not in Codex trigger metadata.

The body must concisely define:

1. the job and its boundaries;
2. the operating workflow;
3. required inputs and missing-input behavior;
4. the output and evidence contract;
5. approval points and write boundaries;
6. deterministic scripts and when to run them; and
7. which references to read for each task variant.

Keep `SKILL.md` under 500 lines. Put detailed standards, schemas, and domain knowledge in
directly linked `references/` files so they are loaded only when needed.

## `agents/openai.yaml`

Quote all string values and provide:

- `interface.display_name`;
- `interface.short_description`, between 25 and 64 characters; and
- `interface.default_prompt`, including the exact `$skill-name` invocation.

Do not declare tools, icons, colors, or invocation policy unless the package actually uses
them.

## Quality bar

A skill is complete when a new contributor can run it using only declared local resources
and approved inputs; its outputs distinguish evidence, inference, and missing facts; its
write behavior is explicit; repeated execution is safe or clearly classified; failures
stop with actionable guidance; and representative tests and synthetic examples pass.
