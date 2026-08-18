# Public Export Manifest

## Approved v1 boundary

This local fresh-history repository contains the 26 skills listed in `SKILL-CATALOG.md`,
Diffguard Lite, shared public standards, reusable templates, synthetic examples, and tests.

## Package contract

Every skill includes:

- `SKILL.md` with public trigger metadata and operating instructions;
- `agents/openai.yaml` with user-facing metadata;
- at least one workflow runbook under `references/`;
- `assets/output-template.md` plus any required config/schema templates;
- `examples/EX-synthetic.md` containing fictional data; and
- local scripts when the workflow has deterministic validation or transformation logic.

The repository validator enforces this contract and checks declared local dependencies.

## Generalization rules applied

- Existing safe templates were retained, including the PM Prioritizer framework and format.
- Company positioning, customer and employee references, personal profiles, account IDs,
  service-specific configuration, and real operating examples were not copied.
- Integration-dependent workflows now expose config templates and review-first adapter
  boundaries. No connector is required to use the local workflow.
- Global workflows were converted from private runtime state to explicit local input paths.
- Examples use fictional organizations and people and must never be treated as evidence.

## Verification

Run:

```bash
python3 scripts/governance/validate_skill_pack.py
python3 -m unittest discover -s tests
```

The repository is licensed under Apache-2.0. Before creating a public remote, perform an
independent secrets scan, review repository name and ownership, and confirm publication
authorization.
