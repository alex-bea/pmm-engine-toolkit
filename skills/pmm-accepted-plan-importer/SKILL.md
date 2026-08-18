---
name: pmm-accepted-plan-importer
description: Import an explicitly approved plan into a repository-local acceptance ledger and stage its tracker mapping. Use when a plan was accepted outside the repository; never infer acceptance or write tracker state before confirmation.
---

# Accepted Plan Importer

1. Read `docs/STD-work-tracker-v1.0.md` and `docs/STD-approval-gates-v1.0.md`.
2. Follow `references/RUN-workflow.md`.
3. Use `scripts/import_plan.py` to create a deterministic ledger proposal.
4. Render the proposal with `assets/output-template.md`.
5. Use `examples/EX-synthetic.md` only as synthetic input.

Record acceptance evidence separately from tracker state. Require a second approval before tracker writes.
