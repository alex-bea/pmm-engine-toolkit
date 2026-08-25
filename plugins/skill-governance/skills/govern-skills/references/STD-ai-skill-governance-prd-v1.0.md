---
doc_type: STD
normative: true
requires:
  - STD-skill-structure-v1.0.md
  - STD-governance-document-metadata-v1.0.md
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Codex users
  - skill maintainers
change_control: Pull request review
---

# AI Skill Governance Standard

## Purpose and authority

Keep skill packages consistent, reviewable, safe, portable, and independently installable.
This standard owns skill registration, lifecycle, ownership, activation, deprecation, and
approval boundaries. The skill-structure standard owns the files inside a skill package.

## Registry

Every governed skill must have exactly one entry in
`.agents/governance/skill-registry.yaml`. The registry is the source of truth for:

- `name`: the lowercase kebab-case skill name;
- `folder`: the repository-relative package path;
- `version`: the governed contract version;
- `owner`: one accountable person or role;
- `status`: `draft`, `active`, `deprecated`, or `archived`; and
- `replacement`: the successor skill name when status is `deprecated`.

An unregistered folder is not an active governed skill. Generated catalogs are views and
must never override the registry.

## Lifecycle

| Status | Meaning | Execution rule |
|---|---|---|
| `draft` | Being built or evaluated | Manual testing only with user authorization |
| `active` | Registered, tested, and supported | May be used for authorized work |
| `deprecated` | Replaced or being retired | Do not use for new work; name a replacement |
| `archived` | Removed from live skill roots | Retain only for history or migration |

Activate a skill only after its package validates, deterministic scripts pass tests, a
synthetic end-to-end example has been exercised, and the owner approves activation.

## Change rules

- Review changes to behavior, inputs, outputs, permissions, dependencies, or references.
- Increment the governed version when the contract changes materially.
- Treat removed fields, removed steps, renamed interfaces, and incompatible output changes
  as breaking changes.
- Keep source material traceable. Mark missing facts instead of inventing them.
- Never silently add, remove, or weaken an approval gate.
- Preserve old versions or provide a migration path when compatibility breaks.

## Agent authority

An agent may inspect files and produce an advisory audit without approval. It must show the
intended paths and changes, then obtain explicit approval before initializing governance,
applying fixes, changing lifecycle state, publishing, performing an external write, or
taking a destructive action. Approval for one action does not authorize a broader action.

## Privacy and IP

- Never commit credentials, private URLs, internal identifiers, personal data, customer
  data, or unlicensed third-party content.
- Use generic templates in reusable packages and synthetic examples.
- Provide sensitive context only at runtime from an authorized user.
- Do not impersonate a person or use a voice profile without consent.

## Validation

Before release, confirm registry and folder agreement, required files, dependency closure,
metadata, lifecycle state, synthetic examples, tests, and public-safety rules. Advisory
findings are the default for local adoption. Blocking CI is an explicit opt-in.
