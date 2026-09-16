---
doc_type: DOC
normative: false
requires:
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-skill-dependencies-v1.0.md
status: Superseded
version: "1.0"
owner: alex-bea
consumers:
  - pre-read-sharpener maintainers
  - implementation reviewers
  - privacy reviewers
change_control: Pull request review
---

# Pre-Read Sharpener Source Inventory (v1.0)

> **Superseded:** Replaced by
> [`DOC-pre-read-sharpener-source-inventory-v1.1.md`](DOC-pre-read-sharpener-source-inventory-v1.1.md),
> which retains this editorial lineage and adds setup mappings, destinations, mutable state,
> fixture, receipt, and current public-package dispositions. This file remains as historical
> evidence for the merged v1.0 candidate.

## Purpose and boundary

This advisory inventory records the bounded functional closure used to expand the public
`pre-read-sharpener` package. It identifies reusable private structures without publishing
private source content, identifying examples, registry data, internal paths, or a reversible
alias map.

The private implementation was the golden authoring reference. The public target was the
same-named five-file package on public `main`. Private materials are not runtime or
installation dependencies.

## Dispositions

| Disposition | Meaning |
|---|---|
| `retain-public` | Keep a correct existing public artifact or mechanism. |
| `rewrite-generic` | Preserve useful behavior while removing private assumptions and facts. |
| `replace-with-template-or-schema` | Replace populated adopter data with a reusable contract and fictional example. |
| `interface-only` | Define a producer, consumer, state, or governance boundary without bundling it. |
| `retain-private` | Use only as private authoring evidence. |
| `exclude` | Do not publish or depend on the item. |

## Bounded inventory

| ID | Source or pattern | Role and direction | Sensitivity | Public equivalent before expansion | Disposition | Public target | Rationale | Requirements | Verification |
|---|---|---|---|---|---|---|---|---|---|
| INV-PRS-001 | Private pre-read-sharpener entrypoint | Runtime routing; seed | Mixed | Thin public entrypoint | `rewrite-generic` | `skills/pre-read-sharpener/SKILL.md` and README | Preserve the job, boundaries, package routing, and output contract without private manifest conventions. | PRS-REQ-001, PRS-REQ-002, PRS-REQ-006, PRS-REQ-008, PRS-REQ-010 | Frontmatter, closure, and workflow tests |
| INV-PRS-002 | Private workflow | Runtime procedure; dependency | Generic | Five-step public runbook | `rewrite-generic` | `references/RUN-pre-read-sharpener-workflow.md` | Restore intake, diagnosis, ordered output, repair, persistence, return, edits, and errors. | PRS-REQ-001 through PRS-REQ-007 | Workflow-content and behavior-case tests |
| INV-PRS-003 | Private output blueprint | Canonical user-facing template; dependency | Mixed | Different public outline | `rewrite-generic` | `assets/output-template.md` | Preserve every section, field, limit, option rule, and reversal column while generalizing examples. | PRS-REQ-003, PRS-REQ-005 | Template parity and example-limit tests |
| INV-PRS-004 | Private decision-quality rubric | Four anchors and ten binary tests; dependency | Mixed | None | `rewrite-generic` | `references/REF-decision-ready-criteria.md` | Preserve every test while removing named-person framing and private cross-references. | PRS-REQ-003, PRS-REQ-004, PRS-REQ-008 | Criterion-by-criterion parity test |
| INV-PRS-005 | Two private decision pre-reads and one duplicate historical record | Real examples; design evidence | Confidential | One incomplete synthetic paragraph | `retain-private` | Fictional source/output pair | The real documents inform input shape and depth but contain identifying facts and do not complete the canonical output template. | PRS-REQ-009, PRS-REQ-011 | Human structural review and exclusion check |
| INV-PRS-006 | Private change history, registry entries, and governance audits | Historical and governance evidence | Internal | Public catalog and validators | `retain-private` | Public source inventory and candidate review | These establish lineage but add no public runtime value. | PRS-REQ-010, PRS-REQ-011 | Confirm absence from package dependencies |
| INV-PRS-007 | Referenced historical prompt source | Unresolved design evidence | Internal | None | `exclude` | None | The historical path was unavailable; the authoritative workflow already embeds the complete directive. | PRS-REQ-010, PRS-REQ-011 | Record the limitation without reconstructing evidence |
| INV-PRS-008 | Private generated-output family | Output and mutable state | Potentially confidential | None | `interface-only` | README, workflow, and `outputs/pre-reads/` contract | No matching real output was found. Preserve the adopter-owned interface without publishing data. | PRS-REQ-006, PRS-REQ-008, PRS-REQ-011 | Path, collision, and write-boundary tests |
| INV-PRS-009 | User-supplied pre-read | Input; upstream | Adopter-owned and potentially confidential | Implicit public input | `interface-only` | `SKILL.md`, workflow, and safety reference | Define authorized intake, untrusted-data handling, and no-research behavior without bundling sources or connectors. | PRS-REQ-001, PRS-REQ-005, PRS-REQ-008 | Intake and missing-data cases |
| INV-PRS-010 | Human executive readers and meeting participants | Consumers; downstream | Mixed | Conversational output | `interface-only` | Markdown deliverable and agenda contract | Preserve the decision-ready output interface without packaging meetings or downstream tools. | PRS-REQ-002, PRS-REQ-003 | Completed-example review |
| INV-PRS-011 | Existing public entrypoint | Runtime router | Public | Same path | `rewrite-generic` | Same path | Remove the root dependency and restore the full behavior. | PRS-REQ-001, PRS-REQ-002, PRS-REQ-008 | Direct-install and parity tests |
| INV-PRS-012 | Existing public discovery metadata | Codex metadata | Public | Same path | `retain-public` | Same path | Existing display metadata and invocation are valid and remain unchanged. | PRS-REQ-010 | Skill-pack validator and byte comparison |
| INV-PRS-013 | Existing public runbook | Abbreviated runtime procedure | Public | Same path | `rewrite-generic` | Same path | The current five steps omit most golden behavior and use a conflicting skeleton. | PRS-REQ-001 through PRS-REQ-007 | Focused workflow test |
| INV-PRS-014 | Existing public output template | Non-canonical skeleton | Public | Same path | `rewrite-generic` | Same path | Replace it with the real constrained decision-ready template. | PRS-REQ-003, PRS-REQ-005 | Template and completed-example tests |
| INV-PRS-015 | Existing public synthetic paragraph | Incomplete fictional example | Synthetic | Same path | `rewrite-generic` | Example index plus fictional pair | Provide a supported and complete demonstration rather than an unfinished paragraph. | PRS-REQ-009, PRS-REQ-011 | Completeness, traceability, and privacy tests |
| INV-PRS-016 | Root privacy standard referenced by the old entrypoint | External package dependency | Public | Outside a direct skill install | `rewrite-generic` | `references/REF-evidence-and-privacy.md` | Bundle skill-relevant safeguards so direct installation is complete. | PRS-REQ-005, PRS-REQ-008, PRS-REQ-011 | Isolated package-copy check |
| INV-PRS-017 | Public validators and unit suite | Governance and verification | Public | Existing shared mechanisms | `interface-only` | Existing validators plus focused test | Reuse shared gates and add skill-specific structural and traceability coverage. | PRS-REQ-003 through PRS-REQ-012 | Focused and complete test suites |
| INV-PRS-018 | Public catalog, export manifest, and IP inventory | Discovery and provenance | Public | Existing shared records | `rewrite-generic` | Same records, updated for expansion | Preserve governance mechanisms while accurately recording the faithful package and new files. | PRS-REQ-010, PRS-REQ-011 | Link and regenerated-inventory checks |
| INV-PRS-019 | Public structure, dependency, privacy, metadata, and approval standards | Public constraints | Public | Root standards | `interface-only` | No standard changes | Apply current rules without making them direct-install runtime dependencies. | PRS-REQ-008, PRS-REQ-010, PRS-REQ-011, PRS-REQ-012 | Strict document, skill-pack, and approval checks |

## Closure boundaries

- **Private skill tree:** The entrypoint, workflow, criteria, template, two examples, and
  change history were inspected. Private files are represented by functional role rather
  than identifying path.
- **Real examples:** Two private pre-reads and one duplicate historical record were inspected
  for input structure and depth. None qualified as a completed canonical output, and none is
  distributed.
- **Generated outputs:** The documented output family had no matching real files. It is
  represented only as an adopter-owned interface.
- **Upstream systems:** Editors, document stores, file systems, and communication systems stop
  at the supplied-draft interface. No connector is required.
- **Downstream systems:** Human review and meetings stop at the stable Markdown deliverable.
- **Historical evidence:** Change history, registry entries, audits, and the unavailable
  historical prompt source are not public dependencies.
- **Current public package:** Every existing public file received a disposition; valid
  discovery metadata remains unchanged.
- **Repository governance:** Only standards, validators, discovery, provenance, and approval
  mechanisms that constrain this slice are in scope. No shared standard or plugin changes.

## Public template and example mapping

| Public template | Completed fictional example | Private basis |
|---|---|---|
| `skills/pre-read-sharpener/assets/output-template.md` | `skills/pre-read-sharpener/examples/fictional-rollout-decision/review-and-rewrite.md` | One canonical private template; no qualifying completed real output found |

This inventory remains advisory. The shipped package and approved requirements govern
runtime behavior after project-owner review.
