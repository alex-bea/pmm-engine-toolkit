---
doc_type: DOC
normative: false
requires:
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-skill-dependencies-v1.0.md
status: Superseded
version: "1.1"
owner: alex-bea
consumers:
  - pre-read-sharpener maintainers
  - implementation reviewers
  - privacy reviewers
change_control: Pull request review
---

# Pre-Read Sharpener Source Inventory (v1.1)

> Superseded by
> [`DOC-pre-read-sharpener-source-inventory-v1.2.md`](DOC-pre-read-sharpener-source-inventory-v1.2.md),
> which inventories the conditional setup bundle. Retained as advisory design history; do
> not use this version as the current package inventory.

## Purpose and boundary

This advisory inventory records the bounded functional closure for the setup-ready public
`pre-read-sharpener` package. It consolidates the editorial lineage documented in v1.0 with
the source mapping, output destinations, configuration, setup receipt, runtime interface,
safe fixture, and current public files required by v1.1.

Private materials were authoring evidence only. No private source content, identifying
example, populated mapping, real receipt, registry data, absolute path, approval record, or
reversible alias is a public runtime dependency.

## Dispositions

| Disposition | Meaning |
|---|---|
| `retain-public` | Keep a correct, self-contained public artifact unchanged. |
| `rewrite-generic` | Preserve useful behavior while removing private assumptions or adapting it to setup. |
| `replace-with-template-or-schema` | Publish a blank reusable contract plus fictional evidence instead of adopter data. |
| `interface-only` | Define an input, output, runtime, state, or governance boundary without bundling an implementation. |
| `retain-private` | Use only as non-public authoring evidence. |
| `exclude` | Do not publish or depend on the item. |

## Bounded inventory

| ID | Source or interface | Role and direction | Sensitivity | Public disposition | Public target | Requirements | Verification |
|---|---|---|---|---|---|---|---|
| INV-PRS11-001 | Private pre-read entrypoint and workflow | Editorial seed and dependency | Mixed | `rewrite-generic` | `SKILL.md` and sole setup RUN | PRS-REQ-001, PRS-REQ-002, PRS-REQ-008, PRSW-REQ-001, PRSW-REQ-009 | Trigger, routing, workflow-parity, and direct-install tests |
| INV-PRS11-002 | Private output blueprint | Canonical user-facing template | Mixed | `retain-public` | `assets/output-template.md` | PRS-REQ-003, PRS-REQ-005, PRSW-REQ-009 | Byte comparison and structure tests |
| INV-PRS11-003 | Private decision-quality rubric | Four anchors and ten binary tests | Mixed | `retain-public` | `references/REF-decision-ready-criteria.md` | PRS-REQ-004, PRSW-REQ-009 | Byte comparison and ten-row tests |
| INV-PRS11-004 | Real private decision pre-reads | Input-shape design evidence | Confidential | `retain-private` | Existing fictional public pair only | PRS-REQ-009, PRS-REQ-011, PRSW-REQ-011 | Exclusion, denylist, and human review |
| INV-PRS11-005 | Private output family | Generated user artifact | Potentially confidential | `interface-only` | Mapped `outputs/pre-reads/` destination | PRS-REQ-006, PRS-REQ-011, PRSW-REQ-004 | Destination and collision tests |
| INV-PRS11-006 | Private registry and governance history | Discovery and authoring evidence | Internal | `retain-private` | Public metadata, catalog, and governed docs | PRS-REQ-010, PRS-REQ-011, PRSW-REQ-010 | Confirm no runtime dependency |
| INV-PRS11-007 | Generic setup-wizard framework | Setup authoring structure | Generic | `rewrite-generic` | `references/RUN-pre-read-sharpener-setup-workflow.md` | PRSW-REQ-001 through PRSW-REQ-009 | Setup-contract validator and human adaptation review |
| INV-PRS11-008 | User-supplied pre-read | Normal upstream input | Adopter-owned | `interface-only` | `PRS-SRC-DRAFT` mapping and intake workflow | PRS-REQ-001, PRS-REQ-005, PRSW-REQ-003, PRSW-REQ-006 | Source-read and no-retrieval cases |
| INV-PRS11-009 | Bundled fictional draft | Setup-test input | Synthetic | `retain-public` | `examples/fictional-rollout-decision/source-draft.md` | PRS-REQ-009, PRSW-REQ-003, PRSW-REQ-007 | Fictional label and source traceability |
| INV-PRS11-010 | External evidence source | Optional upstream interface | None | `interface-only` | Explicit `none` source row | PRS-REQ-005, PRSW-REQ-003, PRSW-REQ-006 | Confirm no connector or fallback |
| INV-PRS11-011 | Normal deliverable destination | Generated output | Adopter-owned | `interface-only` | `PRS-DST-OUTPUT` mapping | PRS-REQ-006, PRSW-REQ-004 | Writable-path, collision, and no-fallback tests |
| INV-PRS11-012 | Setup configuration | Mutable mapping state | Adopter-owned | `replace-with-template-or-schema` | `assets/setup-mapping.md` | PRSW-REQ-003 through PRSW-REQ-006 | Schema, placeholder, and outside-package tests |
| INV-PRS11-013 | Setup receipt | Mutable readiness state | Adopter-owned | `replace-with-template-or-schema` | `assets/setup-receipt.md` | PRSW-REQ-008, PRSW-REQ-011 | Receipt-field, status, staleness, and secret checks |
| INV-PRS11-014 | Isolated test destination | Setup-test output | Synthetic | `interface-only` | `PRS-DST-TEST` mapping | PRSW-REQ-004, PRSW-REQ-007 | Temporary-root and production-isolation checks |
| INV-PRS11-015 | External publication or messaging destination | Downstream external side effect | None | `interface-only` | Explicit `none` destination row | PRS-REQ-011, PRSW-REQ-004, PRSW-REQ-006 | Confirm no adapter or callable publisher |
| INV-PRS11-016 | Compatible local agent | Runtime interface | Mixed | `interface-only` | Installation check and documented agent procedure | PRS-REQ-008, PRSW-REQ-002, PRSW-REQ-007 | Availability probe and isolated fixture execution |
| INV-PRS11-017 | Current public README and `SKILL.md` | Onboarding and routing | Public | `rewrite-generic` | Same paths | PRS-REQ-001, PRS-REQ-008, PRS-REQ-010, PRSW-REQ-001, PRSW-REQ-010 | Frontmatter, link, and content tests |
| INV-PRS11-018 | Current execution-only RUN | Public operating procedure | Public | `rewrite-generic` | Replace with sole setup-workflow RUN | PRS-REQ-001 through PRS-REQ-007, PRSW-REQ-001, PRSW-REQ-009 | Exact-one-RUN and behavior-parity tests |
| INV-PRS11-019 | Current discovery metadata | Harness metadata | Public | `retain-public` | `agents/openai.yaml` | PRS-REQ-010, PRSW-REQ-010 | Byte comparison and package validator |
| INV-PRS11-020 | Current output template, criteria, and privacy reference | Runtime dependencies | Public | `retain-public` | Same paths | PRS-REQ-003 through PRS-REQ-005, PRS-REQ-008, PRSW-REQ-009 | Byte comparison and focused tests |
| INV-PRS11-021 | Current fictional editorial source/output pair | Complete synthetic behavior evidence | Synthetic | `retain-public` | Same paths | PRS-REQ-009, PRS-REQ-011, PRSW-REQ-007, PRSW-REQ-011 | Fact traceability and byte comparison |
| INV-PRS11-022 | Current example index and behavior cases | Synthetic routing and edge contracts | Synthetic | `rewrite-generic` | Same paths plus setup links and cases | PRS-REQ-009, PRSW-REQ-007 through PRSW-REQ-009 | Link and case-ID assertions |
| INV-PRS11-023 | Fictional setup mapping and receipt | Complete synthetic setup evidence | Synthetic | `replace-with-template-or-schema` | `examples/fixtures/setup-smoke-test.md` | PRSW-REQ-003 through PRSW-REQ-008, PRSW-REQ-011 | Fixture completeness and isolated execution |
| INV-PRS11-024 | Focused public tests | Deterministic verification | Public | `rewrite-generic` | `tests/test_pre_read_sharpener.py` | PRS-REQ-003 through PRS-REQ-012, PRSW-REQ-001 through PRSW-REQ-012 | Focused and complete unit suites |
| INV-PRS11-025 | v1.0 requirements and source inventory | Historical governed evidence | Public | `retain-public` | Same files marked Superseded with v1.1 links | PRS-REQ-010, PRS-REQ-012, PRSW-REQ-010 | Strict metadata and replacement-link audit |
| INV-PRS11-026 | Public catalog and export manifest | Discovery and export boundary | Public | `rewrite-generic` | Same paths | PRS-REQ-010, PRS-REQ-011, PRSW-REQ-010, PRSW-REQ-011 | Link and content checks |
| INV-PRS11-027 | Candidate privacy review and IP inventory | Provenance and publication evidence | Public | `rewrite-generic` | Setup-amendment review and regenerated inventory | PRS-REQ-011, PRS-REQ-012, PRSW-REQ-011, PRSW-REQ-012 | Strict audit, scan, human review, and deterministic regeneration |
| INV-PRS11-028 | Public structure, dependency, privacy, metadata, and approval standards | Repository governance | Public | `interface-only` | No standard change | PRS-REQ-008, PRS-REQ-010 through PRS-REQ-012, PRSW-REQ-010 through PRSW-REQ-012 | Skill-pack, document, privacy, and approval checks |

## Closure boundaries

- **Editorial implementation:** The entrypoint, complete workflow, rubric, template, real
  private input examples, generated-output interface, and public fictional pair are bounded.
  No editorial template or criterion changes in v1.1.
- **Source mapping:** Normal execution has one adopter-supplied draft. The safe test has one
  bundled fictional source. Web, document-store, communication, and secondary evidence
  sources are explicit `none` interfaces.
- **Output destinations:** Deliverable, configuration, receipt, and test artifacts live in
  adopter-owned or temporary paths outside the installed package. External publishing,
  messaging, notifications, scheduling, and approval creation are explicit `none` interfaces.
- **Configuration and state:** The completed setup mapping, receipt, and generated pre-reads
  are the complete mutable state. No cache, background worker, or schedule exists.
- **Runtime:** A compatible local agent and basic file access are interfaces, not bundled
  implementations. No fixed model, Python dependency, network service, secret, or adapter is
  required for normal use.
- **Examples:** The existing editorial pair and new setup fixture are independently
  fictional. No real pre-read, mapping, output, or receipt is distributed.
- **Current package:** Every current package file has a disposition. Discovery metadata,
  output template, criteria, privacy reference, and fictional editorial pair remain unchanged.
- **Governance:** Focused tests, v1.1 documents, catalog/export records, candidate privacy
  review, and generated IP inventory are in scope. Shared standards, CI configuration,
  plugins, other skills, merge, and release remain bounded interfaces.

## Public template and example mapping

| Public template | Completed fictional example | Evidence limitation |
|---|---|---|
| `skills/pre-read-sharpener/assets/output-template.md` | `skills/pre-read-sharpener/examples/fictional-rollout-decision/review-and-rewrite.md` | No qualifying completed real private output was found. |
| `skills/pre-read-sharpener/assets/setup-mapping.md` | `skills/pre-read-sharpener/examples/fixtures/setup-smoke-test.md` | No real pre-read setup mapping was found. |
| `skills/pre-read-sharpener/assets/setup-receipt.md` | Completed fictional receipt in `skills/pre-read-sharpener/examples/fixtures/setup-smoke-test.md` | No completed real pre-read setup receipt was found. |

This inventory remains advisory. The shipped package and approved v1.1 requirements govern
runtime behavior after exact-revision review.
