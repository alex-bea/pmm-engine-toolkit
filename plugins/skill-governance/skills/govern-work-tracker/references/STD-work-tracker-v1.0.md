---
doc_type: STD
normative: true
requires:
  - STD-approval-gates-v1.0.md
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Codex users
  - project contributors
change_control: Pull request review
---

# Work Tracker Standard

## Canonical model

Store canonical records under `state/work/` using three levels:

- roadmap: an outcome horizon containing epics;
- epic: a coherent initiative containing tasks; and
- task: an independently verifiable execution slice.

Plans hold rationale and design. Tracker records hold current execution state. Generated
views are derived and must never override canonical records.

## Directory structure

```text
state/work/
├── roadmaps/<id>.yaml
├── epics/<id>.yaml
└── tasks/<id>.yaml
```

Files may use normal YAML or JSON-compatible YAML. The filename stem must equal the record
`id`, and IDs use lowercase kebab-case.

## Shared fields

Every record requires `id`, `title`, `status`, `rank`, and `updated_at`. Status is one of
`icebox`, `todo`, `active`, `blocked`, or `done`. Rank is a positive integer unique among
active siblings. Dates use `YYYY-MM-DD`.

Epics additionally require `roadmap_id`. Tasks require `epic_id` and a non-empty
`acceptance_criteria` list. Active and blocked tasks require `current_task`, `next_action`,
and `resume_from`. Blocked tasks require `blocked_reason`. Done tasks require a non-empty
`evidence` list showing how acceptance was verified.

Optional fields include `owner`, `summary`, `plan_path`, `related_paths`, `depends_on`, and
`labels`. Do not put long-form rationale into tracker YAML.

## Scope test

- If the record can contain multiple independent initiatives over time, use a roadmap.
- If it has one initiative-level outcome with multiple execution slices, use an epic.
- If it is one verifiable slice that can become done, use a task.

If a record satisfies more than one definition, narrow its scope before tracking it.

## Operations

Validate before and after edits. Create or update the smallest applicable record, preserve
unrelated fields, update `updated_at`, and report the resulting state. Do not activate a
record whose declared dependencies are incomplete. Do not mark a task done without evidence
that satisfies its acceptance criteria.

Initializer and fix workflows are dry-run by default. They may create missing structural
files after approval but must not invent goals, priorities, owners, acceptance criteria, or
evidence.

## Validation and CI

Validate types, required fields, IDs, filenames, statuses, parents, rank uniqueness,
dependencies, blocked-state context, and done-state evidence. Local audit is advisory by
default. Repositories may opt into blocking CI by invoking the validator with `--strict`.

PMM-specific team lanes, product tags, WIP limits, beads, and handoff fields are optional
profiles rather than requirements of this generic core.
