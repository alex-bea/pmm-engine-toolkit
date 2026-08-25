---
doc_type: STD
normative: true
requires: []
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Codex users
  - governance maintainers
change_control: Pull request review
---

# Governance Document Metadata Standard

## Authority classes

`STD` and `RUN` documents are binding. `DOC`, `REF`, and `BP` documents are binding only
when `normative: true`. Plans, examples, reports, and generated outputs are evidence or
intent unless another binding document explicitly promotes them.

## Canonical metadata

New or materially changed governed Markdown uses YAML frontmatter with:

```yaml
---
doc_type: STD
normative: true
requires: []
status: Active
version: "1.0"
owner: accountable-owner
consumers:
  - intended consumer
change_control: Pull request review
---
```

`status` is `Draft`, `Active`, `Deprecated`, `Superseded`, or `Archived`. `owner` is one
accountable person or role. `requires` lists direct functional dependencies. The filename,
document type, title, status, and version must agree. Deprecation and supersession must name
a replacement when one exists.

## `SKILL.md` exception

Codex `SKILL.md` frontmatter contains exactly `name` and `description`. Store its version,
owner, lifecycle, and dependency metadata in `.agents/governance/skill-registry.yaml` and
the governance-pack manifest.

## Change control

Changes to binding documents require review. Required-field, authority, compatibility, or
behavior changes require a version increment. A validator defect does not silently change
the written standard.
