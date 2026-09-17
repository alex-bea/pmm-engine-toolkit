---
doc_type: DOC
normative: false
requires:
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-skill-dependencies-v1.0.md
status: Draft
version: "1.2"
owner: alex-bea
consumers:
  - pre-read-sharpener maintainers
  - implementation reviewers
  - privacy reviewers
change_control: Pull request review
---

# Pre-Read Sharpener Source Inventory (v1.2)

## Purpose and boundary

This advisory inventory records the bounded functional closure for the conditional-setup
public `pre-read-sharpener` package. It covers editorial behavior, setup routing, source and
destination mapping, mutable configuration, receipt state, isolated test evidence, and
governance artifacts.

Private material was authoring evidence only. No private content, identifying example,
populated mapping, real receipt, registry data, absolute path, approval record, or reversible
alias is a public runtime dependency.

## Dispositions

| Disposition | Meaning |
|---|---|
| `retain-public` | Keep a correct, self-contained public artifact. |
| `rewrite-generic` | Preserve useful behavior while removing private assumptions. |
| `replace-with-template-or-schema` | Publish a blank reusable schema and fictional evidence instead of adopter data. |
| `interface-only` | Define an input, output, runtime, state, or governance boundary without bundling an implementation. |
| `retain-private` | Use only as non-public authoring evidence. |
| `exclude` | Do not publish or depend on the item. |

## Bounded inventory

| ID | Source or interface | Role and direction | Sensitivity | Public disposition | Public target | Requirements | Verification |
|---|---|---|---|---|---|---|---|
| INV-PRSR-001 | Private editorial entrypoint | Editorial seed | Mixed | `rewrite-generic` | `skills/pre-read-sharpener/SKILL.md` | PRSR-REQ-001, PRSR-REQ-004 | Trigger, routing, and direct-install tests |
| INV-PRSR-002 | Private normal editorial workflow | Runtime dependency | Mixed | `rewrite-generic` | `references/RUN-pre-read-sharpener-workflow.md` | PRSR-REQ-001, PRSR-REQ-002 | Exact-one-RUN and parity tests |
| INV-PRSR-003 | Private output blueprint | User-facing template | Mixed | `retain-public` | `assets/output-template.md` | PRSR-REQ-001 | Structure and limit tests |
| INV-PRSR-004 | Private decision-quality rubric | Quality-gate dependency | Mixed | `retain-public` | `references/REF-decision-ready-criteria.md` | PRSR-REQ-001 | Four-anchor and ten-row tests |
| INV-PRSR-005 | Real private completed pre-reads | Design evidence | Confidential | `retain-private` | none | PRSR-REQ-011 | Exclusion, denylist, and human review |
| INV-PRSR-006 | User-supplied draft | Per-run upstream input | Adopter-owned | `interface-only` | intake workflow and `PRS-SRC-DRAFT` | PRSR-REQ-001, PRSR-REQ-011 | No-retrieval and untrusted-input tests |
| INV-PRSR-007 | Inline response | Immediate downstream output | Adopter-owned | `interface-only` | normal RUN | PRSR-REQ-003, PRSR-REQ-004 | Inline-bypass case |
| INV-PRSR-008 | `outputs/pre-reads/YYYY-MM-DD-<slug>-pre-read.md` | Optional local output | Adopter-owned | `interface-only` | configured persistence route | PRSR-REQ-001, PRSR-REQ-003 | Destination and collision tests |
| INV-PRSR-009 | Setup profile and router | Conditional setup interface | Generic | `rewrite-generic` | `SKILL.md` and setup contract | PRSR-REQ-003, PRSR-REQ-004 | Ready and non-ready routing tests |
| INV-PRSR-010 | Source mapping | Setup data | Generic | `replace-with-template-or-schema` | setup contract and `assets/setup-config.yaml` | PRSR-REQ-005, PRSR-REQ-006 | Table and YAML tests |
| INV-PRSR-011 | Output destination mapping | Setup data | Generic | `replace-with-template-or-schema` | setup contract and `assets/setup-config.yaml` | PRSR-REQ-005, PRSR-REQ-006 | Table and YAML tests |
| INV-PRSR-012 | Setup receipt | Mutable readiness state | Adopter-owned | `replace-with-template-or-schema` | `assets/setup-receipt.yaml` | PRSR-REQ-007, PRSR-REQ-008 | Schema and status tests |
| INV-PRSR-013 | Installation and repair guidance | Human setup reference | Generic | `rewrite-generic` | README and setup contract | PRSR-REQ-005, PRSR-REQ-009 | Link and content tests |
| INV-PRSR-014 | Isolated fictional setup fixture | Setup evidence | Synthetic | `rewrite-generic` | `examples/fixtures/setup-smoke-test.md` | PRSR-REQ-010 | Isolated filesystem test |
| INV-PRSR-015 | Fictional editorial source/output pair | Runtime example | Synthetic | `retain-public` | `examples/fictional-rollout-decision/` | PRSR-REQ-001, PRSR-REQ-011 | Source traceability and output-shape tests |
| INV-PRSR-016 | Fictional example index | Example router | Synthetic | `rewrite-generic` | `examples/EX-synthetic.md` | PRSR-REQ-004, PRSR-REQ-010 | Link and wording tests |
| INV-PRSR-017 | Behavioral cases | Behavioral contract | Synthetic | `rewrite-generic` | `examples/fixtures/behavior-cases.md` | PRSR-REQ-004, PRSR-REQ-008 | Case-ID assertions |
| INV-PRSR-018 | v1.1 combined setup-and-execution RUN | Superseded public runtime file | Public | `exclude` | remove and replace with normal RUN | PRSR-REQ-002, PRSR-REQ-004 | Removal and exact-one-RUN tests |
| INV-PRSR-019 | v1.1 Markdown setup mapping | Superseded public setup file | Public | `exclude` | replace with setup config YAML | PRSR-REQ-006 | Removal and schema tests |
| INV-PRSR-020 | v1.1 Markdown setup receipt | Superseded public setup file | Public | `exclude` | replace with setup receipt YAML | PRSR-REQ-007 | Removal and schema tests |
| INV-PRSR-021 | Focused public tests | Deterministic verification | Public | `rewrite-generic` | `tests/test_pre_read_sharpener.py` | PRSR-REQ-001 through PRSR-REQ-012 | Focused and complete suites |
| INV-PRSR-022 | v1.0 and v1.1 design records | Historical governance evidence | Public | `retain-public` | mark v1.1 superseded and add v1.2 | PRSR-REQ-012 | Strict document audit |
| INV-PRSR-023 | Catalog and export manifest | Discovery and export boundary | Public | `rewrite-generic` | same paths | PRSR-REQ-012 | Link and content checks |
| INV-PRSR-024 | Candidate privacy review and IP inventory | Release evidence | Public | `rewrite-generic` | new review and regenerated inventory | PRSR-REQ-011, PRSR-REQ-012 | Scan, human review, and deterministic regeneration |
| INV-PRSR-025 | Connectors, secrets, schedules, publishers, notifications | External systems | Credential-risk | `interface-only` | explicit none interface | PRSR-REQ-005, PRSR-REQ-011 | Negative safety assertions |

## Closure boundaries

- **Editorial implementation:** The entrypoint, normal workflow, rubric, template,
  generated-output interface, and public fictional pair are bounded. No editorial template
  or criterion changes in v1.2.
- **Normal input:** One pasted, attached, or authorized local draft. No retrieval fallback.
- **Normal output:** Inline output is always available. Local persistence is optional and
  uses a confirmed output root with collision-safe filenames.
- **Setup profile:** `local-persistence`. Inline work bypasses setup. Persistent writes use
  a current adopter-owned receipt.
- **Source mapping:** Normal execution has one adopter-supplied draft. The test has one
  bundled fictional source. Web, document-store, communication, and secondary evidence
  sources are explicit `none` interfaces.
- **Output destinations:** Inline response, local deliverable, configuration, receipt, and
  temporary test paths are bounded. External publishing and messaging are `none` interfaces.
- **Configuration and state:** Blank YAML schemas are distributed. Completed configuration,
  receipt, and generated pre-reads live outside the installed package.
- **Routing:** `ready` enters normal execution without setup detail. `missing`, `stale`, and
  `blocked` enter setup only when persistence is requested.
- **Runtime:** A compatible local agent and filesystem access are interfaces, not bundled
  implementations. No fixed model, package dependency, network service, secret, or adapter
  is required.
- **Examples:** The editorial pair and setup fixture are independently fictional. No real
  pre-read, mapping, output, or receipt is distributed.
- **Governance:** Focused tests, v1.2 records, catalog/export entries, privacy review, and IP
  inventory are in scope. Shared standards, CI configuration, plugins, other skills, merge,
  and release remain bounded interfaces.

## Public template and example mapping

| Public template | Completed fictional example | Evidence limitation |
|---|---|---|
| `skills/pre-read-sharpener/assets/output-template.md` | `skills/pre-read-sharpener/examples/fictional-rollout-decision/review-and-rewrite.md` | No qualifying completed private output used every public field. |
| `skills/pre-read-sharpener/assets/setup-config.yaml` | Completed configuration in `skills/pre-read-sharpener/examples/fixtures/setup-smoke-test.md` | No real pre-read setup configuration is distributed. |
| Source and destination mappings in the setup contract | Mapping tables in `skills/pre-read-sharpener/examples/fixtures/setup-smoke-test.md` | The fixture is independently fictional. |
| `skills/pre-read-sharpener/assets/setup-receipt.yaml` | Completed receipt in `skills/pre-read-sharpener/examples/fixtures/setup-smoke-test.md` | No completed real setup receipt is distributed. |

This inventory remains advisory. The shipped package and approved v1.2 requirements govern
runtime behavior after exact-revision review.
