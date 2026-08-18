---
name: pmm-em-tracker
description: Maintain and validate a repository-local roadmap, epic, and task tracker. Use when creating, activating, blocking, completing, or reporting tracked work; do not mutate an external tracker without explicit approval.
---

# PMM EM Tracker

1. Read `docs/STD-work-tracker-v1.0.md` and `docs/STD-approval-gates-v1.0.md`.
2. Follow `references/RUN-workflow.md`.
3. Use `assets/output-template.md` for status summaries and `assets/tracker-example.yaml`
   as the schema example.
4. Run `scripts/tracker.py validate <tracker-file>` before accepting a write.
5. Use `examples/EX-synthetic.md` only as synthetic tracker data.

Treat local tracker records as canonical. Never mark work done without satisfied acceptance criteria.
