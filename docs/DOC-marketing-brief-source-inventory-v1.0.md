---
doc_type: DOC
normative: false
requires:
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-skill-dependencies-v1.0.md
status: Draft
version: "1.0"
owner: alex-bea
consumers:
  - marketing-brief maintainers
  - implementation reviewers
  - privacy reviewers
change_control: Pull request review
---

# Marketing Brief Source Inventory (v1.0)

## Purpose and boundary

This advisory inventory records the bounded functional closure used to expand the public
`marketing-brief` package. It identifies reusable private structures without publishing
private source content, real output text, organization-specific terminology, internal paths,
or a reversible alias map.

The private PMM Engine implementation was the golden authoring reference. The public target
was the same-named five-file package on public `main`. Private materials are not runtime or
installation dependencies.

## Dispositions

| Disposition | Meaning |
|---|---|
| `retain-public` | Keep a correct existing public artifact or mechanism. |
| `rewrite-generic` | Preserve useful behavior while removing private assumptions and facts. |
| `replace-with-template-or-schema` | Replace populated adopter data with a reusable contract and fictional example. |
| `interface-only` | Define a producer, consumer, or governance boundary without bundling it. |
| `retain-private` | Use only as private authoring evidence. |
| `exclude` | Do not publish or depend on the item. |

## Bounded inventory

| ID | Source or pattern | Role and direction | Sensitivity | Public equivalent before expansion | Disposition | Public target | Rationale | Requirements | Verification |
|---|---|---|---|---|---|---|---|---|---|
| INV-MB-001 | Private marketing-brief `SKILL.md` | Runtime entrypoint; seed | Generic structure with private manifest conventions | Thin public `SKILL.md` | `rewrite-generic` | `skills/marketing-brief/SKILL.md` | Preserve the real job and boundaries using public two-key frontmatter and package-local paths. | MB-REQ-001, MB-REQ-002, MB-REQ-016 | Frontmatter, trigger, and closure tests |
| INV-MB-002 | Private marketing-brief runbook | Workflow; dependency | Generic with organization-specific wording | Abbreviated public runbook | `rewrite-generic` | `references/RUN-marketing-brief-workflow.md` | Restore intake, analysis, exact filling, output, editing, and error behavior. | MB-REQ-004 through MB-REQ-010 | Workflow-content and behavior-contract tests |
| INV-MB-003 | Private output blueprint | Canonical user-facing template; dependency | Mixed | Different ten-field public outline | `rewrite-generic` | `assets/output-template.md` | Preserve seven sections, fields, limits, and writing rules while generalizing naming and task-system guidance. | MB-REQ-003, MB-REQ-015 | Exact parity and example-limit tests |
| INV-MB-004 | Private source-priority reference | Conflict resolution; dependency | Generic | One public paragraph | `rewrite-generic` | `references/REF-source-priority.md` | The seven-level hierarchy and field ownership are required for reliable filling. | MB-REQ-004, MB-REQ-005, MB-REQ-008 | Priority and conflict tests |
| INV-MB-005 | Private launch-tier reference | Tier classification; dependency | Mixed | One public paragraph | `rewrite-generic` | `references/REF-launch-tiers.md` | Preserve Tier 1–3 decision depth while removing industry and channel assumptions. | MB-REQ-006, MB-REQ-012 | Tier content and privacy tests |
| INV-MB-006 | Private changelog, source instructions, original template, implementation plan, and tracker record | Historical design evidence | Internal or mixed | None | `retain-private` | None | These establish lineage but add no public runtime value. | MB-REQ-013, MB-REQ-017 | Confirm absence from package dependencies |
| INV-MB-007 | Private `outputs/briefs/*-marketing-brief.md` | Real output family | Confidential | Incomplete synthetic paragraph | `retain-private` | Fictional source and completed output pair | Nine real outputs were reviewed for structure and depth; none is distributed. | MB-REQ-011, MB-REQ-012 | Human structural review and privacy scan |
| INV-MB-008 | User-supplied specifications, launch plans, strategy, messaging, research, and working notes | Input sources; upstream | Adopter-owned and potentially confidential | Implicit public input description | `interface-only` | README, source-priority, and evidence references | Define accepted inputs and ownership without bundling data or connectors. | MB-REQ-004, MB-REQ-005, MB-REQ-017 | Intake and missing-data tests |
| INV-MB-009 | Optional adopter terminology guidance | Naming input; upstream | Adopter-owned | Root-level general privacy guidance | `replace-with-template-or-schema` | README and source-packet convention | Replace a private organization naming rule with adopter-approved terminology input. | MB-REQ-003, MB-REQ-012 | Generic-language and scan checks |
| INV-MB-010 | Human PMMs and optional downstream content workflows | Output consumers; downstream | Mixed | Conversational public output | `interface-only` | README and runbook output contract | Keep output reusable without bundling unrelated consumers or private automation. | MB-REQ-009, MB-REQ-015, MB-REQ-017 | Output and boundary tests |
| INV-MB-011 | Existing public `SKILL.md` | Public runtime router | Public | Same path | `rewrite-generic` | Same path | Remove the repository-root dependency and restore faithful behavior. | MB-REQ-001, MB-REQ-002, MB-REQ-016 | Direct-install test |
| INV-MB-012 | Existing public `agents/openai.yaml` | Codex discovery metadata | Public | Same path | `retain-public` | Same path | Existing display metadata and invocation remain accurate. | MB-REQ-001, MB-REQ-016 | Skill-pack validator |
| INV-MB-013 | Existing public runbook | Abbreviated workflow | Public | Same path | `rewrite-generic` | Same path | Add the missing workflow and error contracts. | MB-REQ-004 through MB-REQ-010 | Focused tests |
| INV-MB-014 | Existing public output template | Thin public template | Public | Same path | `rewrite-generic` | Same path | Replace the non-golden shape with the canonical seven-section template. | MB-REQ-003, MB-REQ-015 | Template parity test |
| INV-MB-015 | Existing public synthetic example | Incomplete example paragraph | Synthetic | Same path | `rewrite-generic` | Example index plus `fictional-report-filters/` | Provide a complete direct example for the real template. | MB-REQ-011, MB-REQ-012 | Completeness, trace, and reserved-domain tests |
| INV-MB-016 | Root evidence/privacy standard referenced by old public `SKILL.md` | External package dependency | Public | Outside a direct skill install | `rewrite-generic` | `references/REF-evidence-and-privacy.md` | Bundle only the skill-relevant safeguards so the installed package is complete. | MB-REQ-002, MB-REQ-012 | Isolated package-copy test |
| INV-MB-017 | Public package validator and unit suite | Governance and verification | Public | Existing shared mechanism | `interface-only` | Existing validators plus `tests/test_marketing_brief.py` | Reuse shared gates and add focused fidelity coverage. | MB-REQ-014 | Complete validation suite |
| INV-MB-018 | Public catalog, export manifest, and IP inventory | Discovery and provenance | Public | Existing shared records | `retain-public` | Same records, updated for this expansion | Preserve existing governance mechanisms and add this package's changed files. | MB-REQ-013, MB-REQ-016 | Link and regenerated-inventory checks |
| INV-MB-019 | Public metadata, dependency, privacy, approval, and structure standards | Public change constraints | Public | Root standards | `interface-only` | No standard change | Apply them to the package and governed docs without making them runtime dependencies. | MB-REQ-002, MB-REQ-013, MB-REQ-014, MB-REQ-018 | Strict governed-document audit |

## Closure boundaries

- **Real outputs:** Nine private files matched the output family. They are collapsed into one
  pattern because they share one canonical template. Two were inspected deeply; no path,
  content, or identifying detail is published here.
- **Upstream systems:** Document stores, chat systems, file systems, and source-authoring
  workflows stop at the supplied-input interface. The public skill requires no connector.
- **Downstream systems:** Human review and optional content workflows stop at the Markdown
  brief interface. Unrelated private automations are not packaged.
- **Historical evidence:** Source instructions, the original template, plan, changelog, and
  tracker state remain private design history.
- **Mutable state:** The skill is stateless. Adopter sources and optionally saved outputs stay
  outside the installed package.
- **Repository governance:** Only standards and validators that constrain this public slice
  are in scope. No public standard or plugin changes.

## Public template and example mapping

| Public template | Completed fictional example | Private basis |
|---|---|---|
| `skills/marketing-brief/assets/output-template.md` | `skills/marketing-brief/examples/fictional-report-filters/marketing-brief.md` | One canonical private template and nine real private outputs reviewed only for structure and depth |

This inventory remains advisory. The Active product requirements and shipped package govern
runtime behavior.
