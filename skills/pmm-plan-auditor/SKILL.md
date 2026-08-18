---
name: pmm-plan-auditor
description: Audit plan files against repository-local tracker state and report unmapped, stale, or contradictory records. Use for plan hygiene, mapping audits, or weekly governance review; scan read-only before proposing repairs.
---

# PMM Plan Auditor

1. Read `docs/STD-work-tracker-v1.0.md`.
2. Follow `references/RUN-workflow.md`.
3. Run `scripts/audit_plans.py <plans-dir> <tracker-file>` for deterministic discovery.
4. Render findings with `assets/output-template.md`.
5. Use `examples/EX-synthetic.md` only as synthetic evidence.

Separate observed drift from proposed repairs. Do not edit plans or tracker state during the scan.
