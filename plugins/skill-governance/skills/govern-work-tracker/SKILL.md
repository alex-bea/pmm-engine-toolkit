---
name: govern-work-tracker
description: Initialize, audit, and safely repair a lightweight repository-native roadmap, epic, and task tracker with parent relationships, lifecycle states, ranks, acceptance criteria, resume context, and completion evidence. Use when a user asks to add or validate state/work tracking, check roadmap or task quality, repair tracker structure, or enable strict tracker validation in CI.
---

# Govern Work Tracker

## Overview

Maintain a small local tracker in which plans explain why and structured records state what
is actually queued, active, blocked, or done. Keep audits advisory and writes
approval-gated.

## Workflow

1. Resolve the repository, read its instructions, inspect Git status, and determine whether
   another tracker is already authoritative.
2. Run the read-only audit:

   ```bash
   python3 scripts/govern_work_tracker.py audit --repo <repository>
   ```

3. Read `references/STD-work-tracker-v1.0.md` for record boundaries, schemas, operations,
   evidence requirements, and validation rules. Read
   `references/STD-approval-gates-v1.0.md` before any initializer or fix write.
4. For a new tracker, run the initializer without writes and present every target path:

   ```bash
   python3 scripts/govern_work_tracker.py initialize --repo <repository> --dry-run
   ```

5. For missing managed files, run the fix workflow in dry-run mode:

   ```bash
   python3 scripts/govern_work_tracker.py fix --repo <repository> --dry-run
   ```

6. Ask for explicit approval. Repeat the approved command with `--apply`, then audit again.
7. Use `audit --strict` only for user-approved blocking CI or an explicit release check.

## Record decisions

- Use a roadmap for an outcome horizon that can contain independent initiatives.
- Use an epic for one coherent initiative that needs multiple execution slices.
- Use a task for one independently verifiable slice.
- Keep rationale in a linked plan and current execution state in `state/work/`.
- Require evidence before `done`; a draft or status assertion is not completion evidence.
- Keep contradictory evidence, blockers, and missing facts visible.

## Write boundaries

- Initialize directories, schemas, templates, and validators only after approval.
- Do not invent roadmap goals, epic scope, task priority, owners, acceptance criteria,
  blocker reasons, or completion evidence.
- Do not rewrite malformed records automatically.
- Never overwrite a differing managed file.
- Preserve optional local fields when editing an approved record.

## PMM profile

Read `assets/examples/pmm-engine/EX-pmm-engine-work-tracker.md` only when the user wants
PMM-specific examples.
Treat product tags, campaign phases, lanes, WIP limits, beads, and handoffs as optional
extensions to the generic core.

## Failure handling

Stop and request direction when an existing tracker has a different canonical model, parent
relationships are ambiguous, duplicate IDs exist, or a semantic repair would change
priority or scope. Report those findings without applying a guess.
