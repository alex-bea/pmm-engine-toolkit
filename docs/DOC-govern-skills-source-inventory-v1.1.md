---
doc_type: DOC
normative: false
requires:
  - STD-evidence-privacy-v1.0.md
status: Draft
version: "1.1"
owner: alex-bea
consumers:
  - govern-skills maintainers
  - privacy reviewers
  - release reviewers
change_control: Pull request review and project-owner approval
---

# Public Govern Skills Conditional Setup Source Inventory (v1.1)

## Scope

This inventory covers the conditional-setup amendment to the standalone public
`govern-skills` package. It identifies design sources, current public artifacts, candidate
transformations, exclusions, and verification for each artifact family. The optional
plugin is comparison evidence only and remains unchanged.

## Disposition vocabulary

- `retain-public`: keep the existing public artifact unchanged.
- `revise-public`: update a public artifact using public-compatible, newly authored text.
- `replace-public`: remove a superseded public artifact and add its approved replacement.
- `add-public`: add a new public artifact with no populated private data.
- `exclude-private`: use only to understand behavior; do not copy content or locators.

## Inventory

| ID | Source or evidence | Role | Classification | Disposition | Public target | Preserved behavior or constraint | Verification |
|---|---|---|---|---|---|---|---|
| INV-GCS-001 | Existing public standalone `SKILL.md` | Discovery and routing | public | revise-public | `skills/govern-skills/SKILL.md` | Preserve governance modes and boundaries; add conditional readiness routing. | Focused routing tests. |
| INV-GCS-002 | Existing public standalone README | Adoption guide | public | revise-public | `skills/govern-skills/README.md` | Preserve direct-copy route and primitive explanation; add Setup and Normal use. | Link and setup-contract validation. |
| INV-GCS-003 | Existing combined public RUN v1.0 | Setup and normal workflow | public | replace-public | normal RUN v1.1 plus setup contract | Preserve workflow behavior while separating frequently used normal steps from setup detail. | Exact-one-RUN and heading checks. |
| INV-GCS-004 | Existing public adoption REF | Inspect-first guidance | public | revise-public | same REF path | Preserve adoption method; route readiness through the setup contract. | Dependency and link checks. |
| INV-GCS-005 | Eight public standard mirrors | Stable governance rules | public | retain-public | same eight paths | No content change. | Byte comparison with canonical standards and base revision. |
| INV-GCS-006 | Existing blank governance templates | Adoptable document shapes | public | retain-public | `assets/templates/*` | No setup-state role is added to these existing templates. | Diff comparison. |
| INV-GCS-007 | Existing Markdown output template | Detailed evidence report | public | retain-public | `assets/output-template.md` | Remains optional human-readable evidence, not readiness state. | Diff comparison and README wording. |
| INV-GCS-008 | Existing fictional repository mapping | Legacy fictional source/destination evidence | synthetic public | retain-public | same fixture path | Preserve its three declared legacy expected files. | Existing isolated test. |
| INV-GCS-009 | Existing fictional Markdown receipt | Detailed fictional evidence | synthetic public | retain-public | same fixture path | Preserve human-readable demonstration and staleness wording. | Existing isolated test. |
| INV-GCS-010 | Conditional setup framework | Structural setup requirements | reusable design | rewrite-generic | setup contract and YAML shapes | Use profile, routing, mapping, safety, receipt, and repair concepts only. | Contract validator. |
| INV-GCS-011 | Private golden governance entrypoint and workflow | Behavioral completeness reference | private | exclude-private | public entrypoint, RUN, and adoption REF | Preserve generic modes and truthfulness; copy no private path, entity, state, or example. | Denylist and human non-reversibility review. |
| INV-GCS-012 | Blank setup configuration design | Machine-readable mapping | generic | add-public | `assets/setup-config.yaml` | Required fields, placeholders, stable adopter-owned paths, no live defaults. | Key and placeholder tests. |
| INV-GCS-013 | Blank receipt design | Machine-readable readiness | generic | add-public | `assets/setup-receipt.yaml` | Ready/missing/stale/blocked contract, digests, checks, limitations, normal entrypoint. | Key and route tests. |
| INV-GCS-014 | Acorn Studio setup configuration | Completed safe example | synthetic | add-public | `examples/fixtures/setup-config.yaml` | Documents-only scope and invented temporary paths. | Fixture assertions and privacy scan. |
| INV-GCS-015 | Acorn Studio YAML receipt | Completed safe example | synthetic | add-public | `examples/fixtures/setup-receipt.yaml` | Ready only for fictional documents-only scope. | Fixture assertions. |
| INV-GCS-016 | Fictional smoke-test procedure | Safe-test contract | synthetic | add-public | `examples/fixtures/setup-smoke-test.md` | Isolated copy, package immutability, exact artifacts, no external mutation. | Focused test and manual review. |
| INV-GCS-017 | Existing fictional example index | Example routing | synthetic public | revise-public | `examples/EX-synthetic.md` | Link both YAML state and optional Markdown evidence. | Link checks. |
| INV-GCS-018 | Existing focused public tests | Deterministic package checks | public source | revise-public | `tests/test_govern_skills.py` | Preserve closure and mirror tests; add split-contract and YAML checks without new runtime dependency. | Unit suite. |
| INV-GCS-019 | Public skill-pack validator | Distribution validation | public source | revise-public | `scripts/governance/validate_skill_pack.py` | Update only govern-skills required paths and expected RUN. | Full validator. |
| INV-GCS-020 | Public catalog and export manifest | Discovery and scope | public documentation | revise-public | same paths | Describe conditional setup, stable state, and unchanged plugin boundary. | Document audit and link review. |
| INV-GCS-021 | v1.0 governed requirements and inventory | Design history | public documentation | revise-public | same v1.0 paths | Mark superseded; retain history. | Metadata audit. |
| INV-GCS-022 | v1.1 governed requirements and inventory | Candidate authority record | project-authored | add-public | v1.1 DOC paths | Capture requirements, traceability, source dispositions, and approval boundary. | Document audit. |
| INV-GCS-023 | Candidate privacy review and generated IP inventory | Publication evidence | project-authored/generated | add/revise-public | approved legal paths | Record provenance, sanitization, checks, risks, and every public artifact. | Repeatable inventory digest and scan. |
| INV-GCS-024 | Public `skill-governance` plugin | Optional advanced distribution | public | retain-public | `plugins/skill-governance/**` | Must remain unchanged; standalone setup does not depend on it. | Base-revision directory digest and manifest diff. |

## Excluded material

- private repository roots, worktrees, account and channel identifiers, registries, state,
  approvals, outputs, and completed setup records;
- private source prose, distinctive examples, quotes, entity aliases, and substitution maps;
- credentials, secret names tied to a real environment, external publisher configuration,
  and production locators; and
- changes to the public plugin, standard contents, root README, interface metadata, existing
  templates, release notes, or any path outside the approved manifest.

## Traceability

| Requirement family | Inventory IDs |
|---|---|
| Conditional route and one normal RUN | INV-GCS-001 through INV-GCS-004, INV-GCS-010, INV-GCS-018, INV-GCS-019 |
| Stable configuration and receipt | INV-GCS-007 through INV-GCS-015 |
| Fictional safe test and privacy | INV-GCS-008, INV-GCS-009, INV-GCS-014 through INV-GCS-017, INV-GCS-023 |
| Compatibility and unchanged boundaries | INV-GCS-005, INV-GCS-006, INV-GCS-019, INV-GCS-020, INV-GCS-024 |
| Governed review and approval | INV-GCS-021 through INV-GCS-023 |

## Review boundary

Gate A approved review-package digest
`sha256:a89b73485f12abf208521aec14713e003904fea2febc5a97d3b4ee8982990002`
and only its manifest paths. A new target, plugin change, standard change, populated real
configuration, live integration, or additional file path requires a new digest-bound
review. Gate B must bind to the exact pull-request revision and does not authorize merge.
