# Work Tracker Standard v1.0

## Canonical model

Store tracker records under `state/work/` using three levels:

- roadmap: outcome horizon containing epics
- epic: coherent outcome containing tasks
- task: independently verifiable unit of work

Required task fields are `id`, `title`, `status`, `epic`, and `acceptance_criteria`.
Allowed statuses are `icebox`, `todo`, `active`, `blocked`, and `done`. A blocked task
must record a reason. A done task must satisfy its acceptance criteria.

Generated views are derived artifacts and never override canonical records. New plans
must declare their tracker role and mapped record ID. External tracker adapters may be
added, but local state remains runnable without them.
