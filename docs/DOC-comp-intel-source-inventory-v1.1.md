---
doc_type: DOC
normative: false
requires:
  - STD-approval-gates-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-skill-dependencies-v1.0.md
status: Draft
version: "1.1"
owner: alex-bea
consumers:
  - comp-intel maintainers
  - implementation reviewers
  - security reviewers
change_control: Pull request review
---

# Competitive Intelligence Conditional Setup Source Inventory (v1.1)

## 1. Purpose and boundary

This advisory inventory records the bounded sources and dispositions for separating public
`comp-intel` setup from normal execution. It supersedes the v1.0 inventory for current setup
architecture. The shipped skill package remains the runtime source of truth.

Private source content, organization mappings, competitor facts, positioning, people, customers,
deals, evidence, and historical runs are never public dependencies. They informed functional
depth only. The existing fictional HarborKey example remains the safe public content model.

## 2. Dispositions

| Disposition | Meaning |
|---|---|
| `retain-public` | Keep the current public artifact and behavior. |
| `rewrite-generic` | Preserve the job while removing organization assumptions. |
| `replace-with-template-or-schema` | Replace mutable or adopter-owned content with a blank contract and fictional example. |
| `interface-only` | Document the boundary without bundling a source, service, credential, or downstream system. |
| `retain-private` | Use only as private design evidence. |
| `exclude` | Remove from the current public runtime architecture. |

## 3. Inventory

| ID | Source path or pattern | Role | Sensitivity | Public equivalent | Disposition | Target | Rationale | Requirements | Verification |
|---|---|---|---|---|---|---|---|---|---|
| INV-CISR-001 | private `skills/comp-intel/SKILL.md` | Golden router | high | public `SKILL.md` | rewrite-generic | same public path | Preserve triggers and boundaries with conditional setup routing. | CISR-REQ-001, CISR-REQ-004 | Router and link tests |
| INV-CISR-002 | private normal workflow reference | Golden analyst method | high | `references/RUN-workflow.md` | rewrite-generic | same public path | Preserve collection, evidence, synthesis, review, and local apply without private sources. | CISR-REQ-001, CISR-REQ-002 | Analyst parity and focused tests |
| INV-CISR-003 | private persona and stakeholder profiles | Analysis lens | critical personal | analyst contract and stakeholder-lens template | retain-private | none | Public role-based lens already preserves the useful method. | CISR-REQ-001, CISR-REQ-011 | Person-data and private-term scans |
| INV-CISR-004 | private channel and source reference | Source mapping | critical identifiers | source-map template | replace-with-template-or-schema | setup contract and setup config | Adopters supply their own approved locators and permissions. | CISR-REQ-003, CISR-REQ-006 | Mapping and privacy tests |
| INV-CISR-005 | private registry references | Durable competitor state | critical strategy | competitor-registry and market-pack templates | replace-with-template-or-schema | retained public templates | Preserve fields and relationships, not entities or facts. | CISR-REQ-001, CISR-REQ-011 | Template parity |
| INV-CISR-006 | private positioning references | Comparative state | critical strategy | positioning templates | replace-with-template-or-schema | retained public templates | Preserve claims, proof, holds, counters, and gaps without private content. | CISR-REQ-001, CISR-REQ-011 | Template parity and semantic review |
| INV-CISR-007 | private `outputs/competitive/*-report.md` | Real briefings | confidential | fictional briefing | retain-private | none | Calibrate depth only. | CISR-REQ-001, CISR-REQ-011 | Manual comparison |
| INV-CISR-008 | private `outputs/competitive/*-signals.md` | Real evidence caches | critical | fictional evidence log | retain-private | none | Preserve evidence classes and limitations, never records. | CISR-REQ-001, CISR-REQ-011 | Manual comparison and denylist scan |
| INV-CISR-009 | private persistent tracker files | Real tracker state | critical | fictional trackers | retain-private | none | Preserve append-only relationships without rows. | CISR-REQ-001, CISR-REQ-011 | Structural comparison |
| INV-CISR-010 | private `state/runs/comp-intel-*.yaml` | Real run records | internal | run template and schema | retain-private | none | Confirm resume and artifact needs without importing history. | CISR-REQ-001, CISR-REQ-011 | Field comparison |
| INV-CISR-011 | public `RUN-onboarding.md` | Setup execution | public | same file | exclude | remove | A second RUN conflicts with the sole normal RUN contract. | CISR-REQ-002, CISR-REQ-005 | Exact-one-RUN test |
| INV-CISR-012 | public `DOC-setup-and-mapping.md` | Setup detail | public | same file | exclude | replace with setup REF | Current setup detail belongs in a conditionally loaded contract. | CISR-REQ-005 | Removal and link tests |
| INV-CISR-013 | public `RUN-workflow.md` | Normal execution | public | same file | retain-public | same file | Preserve complete normal workflow and add only readiness preflight. | CISR-REQ-001, CISR-REQ-002 | Parity tests |
| INV-CISR-014 | public analyst, evidence, review, and troubleshooting references | Method support | public | same files | retain-public | same files | They are self-contained and do not store adopter setup. | CISR-REQ-001 | Package validator |
| INV-CISR-015 | public human templates and HarborKey example | Content model | synthetic | same files | retain-public | same files | Existing example is complete, fictional, and non-reversible. | CISR-REQ-001, CISR-REQ-011 | Framework tests |
| INV-CISR-016 | public controller, schemas, and JSON fixtures | Optional deterministic support | public and synthetic | same files | retain-public | same files | Preserve current evidence and approval mechanics. | CISR-REQ-001, CISR-REQ-012 | Foundation tests |
| INV-CISR-017 | no private setup contract | Setup architecture | none found | old onboarding and setup docs | replace-with-template-or-schema | `REF-comp-intel-setup-contract.md` | Separate first-run and repair detail from normal execution. | CISR-REQ-005 | Setup validator |
| INV-CISR-018 | no private readiness setup config | Setup configuration | none found | none | replace-with-template-or-schema | `assets/setup-config.yaml` | Add blank source, destination, reviewer, data-root, and receipt mapping. | CISR-REQ-006 | YAML tests |
| INV-CISR-019 | no private readiness receipt | Readiness state | none found | none | replace-with-template-or-schema | `assets/setup-receipt.yaml` | Store identity and checks outside the package. | CISR-REQ-007, CISR-REQ-008 | Receipt tests |
| INV-CISR-020 | approved live source capabilities | Source interfaces | credential risk | manual workflow and adapter seam | interface-only | setup contract | No connector, account, credential, or live locator ships. | CISR-REQ-003, CISR-REQ-011 | Capability and negative safety tests |
| INV-CISR-021 | adopter data and output roots | Destination interfaces | adopter-owned | current local-state guidance | replace-with-template-or-schema | setup config and contract | Make containment, mode, retention, review, and write check explicit. | CISR-REQ-006, CISR-REQ-009 | Destination tests |
| INV-CISR-022 | fictional setup config, receipt, and smoke test | Setup evidence | synthetic | none | replace-with-template-or-schema | `examples/fixtures/` | Demonstrate configured-sources setup and all four states safely. | CISR-REQ-010 | Isolated fixture run |
| INV-CISR-023 | external publication, messaging, CRM, schedules, notifications, and approval creation | External effects | credential risk | explicitly outside scope | interface-only | setup contract | Setup never grants external mutation. | CISR-REQ-011 | Negative assertions |
| INV-CISR-024 | focused tests | Verification | public | same test module | rewrite-generic | same test module | Replace two-RUN assertions and add setup coverage. | CISR-REQ-001 through CISR-REQ-012 | Focused suite |
| INV-CISR-025 | catalog, export manifest, governed docs, privacy review, and IP inventory | Governance | public | existing records | rewrite-generic | current candidate records | Describe exact package and provenance accurately. | CISR-REQ-012 | Document, link, and inventory checks |

## 4. Template and example coverage

Real private examples were found for briefings, evidence caches, registries, positioning,
stakeholder lenses, trackers, and run records. They remain private. The HarborKey scenario
already supplies complete fictional counterparts for every human-facing operating template.

No real setup contract, readiness configuration, receipt, or four-state smoke test was found.
Those artifacts use blank public schemas and independently fictional completed fixtures.

## 5. Closure boundaries

- `references/RUN-workflow.md` is the sole normal RUN.
- The setup profile is `configured-sources`.
- A matching `ready` receipt bypasses detailed setup; other states route to the setup contract.
- Setup and operational state are external to the package.
- Optional sources fail visibly and never trigger an undeclared fallback.
- The fictional smoke test has no live integration or external side effect.
- Publication, messages, schedules, notifications, CRM mutation, and external approvals remain
  separate workflows.
- Archived Codex requirements and the v1.0 inventory remain non-binding history.

## 6. Conclusion

The candidate preserves the existing public analyst product and adds only the closure required
for conditional configured-source setup. Every public target is an existing generic artifact,
a blank setup contract or schema, a fictional fixture, a focused test, or a governance record.
Every private-content path remains private or is represented only by a generic interface.
