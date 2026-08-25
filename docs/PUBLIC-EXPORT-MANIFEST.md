# Public Export Manifest

## Approved v1 boundary

This local fresh-history repository contains the 26 skills listed in `SKILL-CATALOG.md`,
Diffguard Lite, shared public standards, reusable templates, synthetic examples, and tests.
The root governance set covers contributions, conduct, project decisions, security,
support, privacy, licensing, and independent setup.

It also contains the `skill-governance` Codex plugin, its public marketplace entry, and three
self-contained governance skills that can be installed independently from GitHub.

## Package contract

Every skill includes:

- `SKILL.md` with public trigger metadata and operating instructions;
- `agents/openai.yaml` with user-facing metadata;
- at least one workflow runbook under `references/`;
- `assets/output-template.md` plus any required config/schema templates;
- `examples/EX-synthetic.md` containing fictional data; and
- local scripts when the workflow has deterministic validation or transformation logic.

The repository validator enforces this contract and checks declared local dependencies.

Plugin governance skills additionally include the canonical standards they enforce,
deterministic initializer/audit/fix scripts, installable schemas and templates, and generic
examples with optional PMM profiles. The document audit is read-only and validates only
opted-in Markdown structure and local paths. CI verifies mirrored standards against `docs/`.

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

Public CI is defined by SHA-pinned, least-privilege workflows under `.github/workflows/`;
its security properties and required checks are documented in [`CI.md`](CI.md).

The repository is licensed under Apache-2.0. The independent all-ref and tracked-tree
secrets scan is recorded in [`security/SECRET-AUDIT-2026-08-18.md`](security/SECRET-AUDIT-2026-08-18.md).
The per-artifact provenance and redistribution review is recorded in
[`legal/IP-RIGHTS-REVIEW-2026-08-18.md`](legal/IP-RIGHTS-REVIEW-2026-08-18.md). Before
creating a public remote, confirm repository name and ownership. Then apply and verify the
versioned branch, Actions, CodeQL, dependency, secret-scanning, and vulnerability-reporting
baseline in
[`security/GITHUB-SECURITY-CONTROLS.md`](security/GITHUB-SECURITY-CONTROLS.md).
