---
name: govern-skills
description: Initialize, audit, and safely repair portable Codex skill governance covering package structure, naming, trigger metadata, registry entries, lifecycle, dependency closure, evidence quality, and approval gates. Use when a user asks to govern a repository, standardize skills, install the governance pack, audit skill quality, fix mechanical governance drift, create a skill registry, or add opt-in governance CI.
---

# Govern Skills

## Overview

Establish a repository-owned contract for consistently shaped Codex skills. Keep audits
read-only and advisory by default. Gate every initializer or fix write behind a displayed
plan and explicit user approval.

## Workflow

1. Resolve the target repository and inspect its instructions, Git status, skill roots,
   existing governance files, and dependency system.
2. Run the deterministic audit before proposing changes:

   ```bash
   python3 scripts/govern_skills.py audit --repo <repository>
   ```

3. Read only the standards needed to explain the findings:

   - Read `references/STD-skill-structure-v1.0.md` for package layout, names, `SKILL.md`,
     and `agents/openai.yaml`.
   - Read `references/STD-ai-skill-governance-prd-v1.0.md` for registry, lifecycle,
     ownership, activation, deprecation, and agent authority.
   - Read `references/STD-governance-document-metadata-v1.0.md` for governed document
     identity and the `SKILL.md` metadata exception.
   - Read `references/STD-skill-dependencies-v1.0.md` for direct-install and dependency
     closure.
   - Read `references/STD-skill-primitives-v1.0.md` for authoring quality and testing.
   - Read `references/STD-approval-gates-v1.0.md` before any write.
   - Read `references/STD-evidence-privacy-v1.0.md` when skills use evidence, people,
     private context, high-stakes claims, or external connectors.

4. Classify each finding as mechanical and fixable, semantic and review-required, or an
   intentional local extension.
5. For initialization, run a dry-run and present the exact paths:

   ```bash
   python3 scripts/govern_skills.py initialize --repo <repository> --dry-run
   ```

   Add `--with-ci` only when the user explicitly opts into blocking CI.
6. For repair, run a dry-run. Use `--finding <ID>` when the user approves only one finding:

   ```bash
   python3 scripts/govern_skills.py fix --repo <repository> --dry-run
   ```

7. Wait for explicit approval. Then repeat the same command with `--apply` and re-run the
   audit. Do not translate a request for an audit into permission to write.
8. Report created, updated, unchanged, conflicting, and manual-review files separately.

## Write boundaries

- Never overwrite a differing standard, schema, template, skill file, or interface file.
- Preserve unrelated files and registry fields.
- Create missing registry entries as `draft`, version `0.1.0`, owner `unassigned`.
- Never promote a skill to `active`, choose an owner, invent a replacement, or weaken a
  gate without an explicit user decision.
- Treat `.agents/governance/manifest.yaml` as generated installation metadata. Show its
  update in the plan before writing it.
- Keep blocking CI opt-in. The normal `audit` command returns success with advisory
  findings; `audit --strict` returns nonzero when findings exist.

## Installed repository shape

Initialization installs standards, schemas, templates, a registry, a deterministic audit
script, and a versioned file-hash manifest under `.agents/governance/`. Repository skills
default to `.agents/skills/<skill-name>/`. The installer does not create or alter actual
skills without a separate approved fix.

Read `assets/examples/pmm-engine/EX-pmm-engine-skill-governance.md` only when the user
wants a PMM-specific example. Keep that profile separate from the generic rules.

## Failure handling

Stop and explain the exact conflict when a managed target already differs, metadata cannot
be parsed, the repository is ambiguous, or the requested fix needs semantic judgment. Do
not use `--apply` as a workaround for an unresolved conflict.
