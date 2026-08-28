---
doc_type: DOC
normative: false
requires:
  - STD-approval-gates-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-skill-dependencies-v1.0.md
status: Draft
version: "1.0"
owner: alex-bea
consumers:
  - comp-intel maintainers
  - implementation reviewers
  - security reviewers
change_control: Pull request review
---

# Competitive Intelligence Source Inventory (v1.0)

## 1. Purpose and boundary

This inventory defines the bounded functional dependency closure for expanding the existing
public `comp-intel` skill. It records structural dependencies and public dispositions without
copying source-organization facts, people, channels, customers, deals, positioning, generated
outputs, or source excerpts.

The source baseline was inspected on 2026-08-28. The public baseline is the six-file package
already under [`skills/comp-intel/`](../skills/comp-intel/). The private seed is its canonical
`SKILL.md` plus the eight documents declared in that skill's manifest.

This is a dependency inventory, not permission to publish any source item. Only artifacts with
a public target and an approved implementation may enter the reusable package.

### 1.1 Closure rules

- Stable documents, configuration, scripts, and tests are named by repository-relative path.
- Dated or mutable artifacts are represented by path pattern; individual instances are not
  enumerated.
- Upstream and downstream skills stop at their interface contract. Their internal dependency
  trees are outside this closure.
- Raw messages, profile instances, customer records, and historical run contents are never
  inventoried individually.
- Historical plans and product-requirements documents are grouped as private design evidence.
  They are not public dependencies and must not be copied.

### 1.2 Dispositions

| Disposition | Meaning |
|---|---|
| `retain-public` | Keep the existing public artifact; later changes are additive or editorial. |
| `rewrite-generic` | Preserve the job while removing organization-specific assumptions and data. |
| `replace-with-template-or-schema` | Replace mutable or organization-owned content with a portable contract. |
| `interface-only` | Specify the boundary but do not bundle the producer, consumer, service, or data. |
| `retain-private` | Keep the artifact and its contents in the source environment only. |
| `exclude` | Do not ship or depend on the artifact in the public package. |

## 2. Current public package

| Source | Role / direction | Sensitivity | Current public equivalent | Disposition | Target artifact | Rationale | Requirements | Verification |
|---|---|---|---|---|---|---|---|---|
| `skills/comp-intel/SKILL.md` | Runtime router; public baseline | Public-safe | Same path | `rewrite-generic` | Same path | Keep the name and invocation language, but route only to skill-local resources and the governed staged workflow. | CI-PKG-001–004, CI-PRV-001 | Skill-pack validator; activation tests |
| `skills/comp-intel/agents/openai.yaml` | User-facing metadata; public baseline | Public-safe | Same path | `retain-public` | Same path | Existing display metadata and `$comp-intel` invocation are compatible with the target product. | CI-PKG-004 | Skill-pack validator |
| `skills/comp-intel/assets/config-template.yaml` | Adopter configuration; public baseline | Public-safe but underspecified | Same path | `rewrite-generic` | Same path plus `assets/market-pack-template.yaml` | Add data-root, market-pack, source-capability, reviewer, retention, and output settings without embedding live identifiers. | CI-CFG-001–003, CI-SRC-001–003 | Schema and initialization tests |
| `skills/comp-intel/assets/output-template.md` | Briefing renderer; public baseline | Public-safe but underspecified | Same path | `rewrite-generic` | Same path | Preserve the concise brief while adding evidence, limitations, digest, review, and change-set sections. | CI-OUT-001–002 | Golden render test |
| `skills/comp-intel/examples/EX-synthetic.md` | Fictional walkthrough; public baseline | Synthetic | Same path | `rewrite-generic` | Same path plus synthetic fixtures under `tests/fixtures/` | Expand the safe example into an offline end-to-end case; never replace it with real entities. | CI-CFG-003, CI-PRV-002, CI-QA-001 | Synthetic acceptance test |
| `skills/comp-intel/references/RUN-workflow.md` | Workflow summary; public baseline | Public-safe but incomplete | Same path | `rewrite-generic` | `references/RUN-comp-intel-workflow-v1.0.md` | Replace the six-step prompt with a governed review-gated runbook; update `SKILL.md` in the same implementation change. | CI-PKG-003, CI-RUN-001–005 | Document audit; stage-transition tests |

## 3. Private seed documents

The paths below identify source structure only. Their content remains private.

| Source | Role / direction | Sensitivity | Current public equivalent | Disposition | Target artifact | Rationale | Requirements | Verification |
|---|---|---|---|---|---|---|---|---|
| `skills/comp-intel/SKILL.md` | Private runtime entrypoint; inbound | High: organization, people, source and output assumptions | Public `SKILL.md` | `rewrite-generic` | `skills/comp-intel/SKILL.md` | Preserve the job and trigger language; remove private modes, identities, headless assumptions, and direct mutation. | CI-PKG-001–004, CI-PRV-001 | Negative privacy scan; trigger tests |
| `skills/comp-intel/references/RUN-comp-intel-workflow-prd-v3.0.0.md` | Canonical private runbook; inbound | High: private sources, identifiers, positioning and state paths | Public `RUN-workflow.md` | `rewrite-generic` | `references/RUN-comp-intel-workflow-v1.0.md` | Preserve collection, snapshots, gap analysis, briefing and resume concepts behind explicit reviews and portable contracts. | CI-RUN-001–005, CI-SRC-001–003 | Workflow and refusal tests |
| `skills/comp-intel/references/REF-comp-intel-persona-prd-v3.0.0.md` | Analysis lens, evidence rules and output format; inbound | High: person-specific framing and organization claims | Partial behavior in `SKILL.md` and output template | `rewrite-generic` | `references/DOC-comp-intel-analysis-contract-v1.0.md` | Retain source discipline and executive brevity; replace the named lens with a consented, optional stakeholder lens. | CI-EVD-001–003, CI-OUT-001, CI-PRV-001 | Claim traceability and lens-isolation tests |
| `skills/comp-intel/references/REF-comp-intel-channels-v3.0.0.md` | Source identifiers, queries and web targets; inbound | Critical: private channels, people and identifiers | `assets/config-template.yaml` | `replace-with-template-or-schema` | `references/REF-comp-intel-source-adapter-contract-v1.0.md`; `assets/config-template.yaml` | Adopters must map their own approved sources; no live source identity belongs in the package. | CI-CFG-001, CI-SRC-001–003, CI-PRV-001 | Forbidden-pattern scan; capability preflight tests |
| `skills/comp-intel/references/REF-comp-intel-competitor-registry-v3.0.0.md` | Market registry and mutable competitive state; bidirectional | Critical: deal context, private claims and organization positioning | None | `replace-with-template-or-schema` | `references/REF-comp-intel-registry-schema-v1.0.md`; `assets/market-pack-template.yaml` | Convert one organization-owned registry into a generic adopter-owned schema and fictional fixture. | CI-CFG-003, CI-STATE-001–002, CI-PRV-001 | Registry schema and clean-init tests |
| `skills/comp-intel/references/REF-comp-intel-chain-competitor-registry-v3.0.0.md` | Second market registry; bidirectional | High: organization strategy and deal context | None | `replace-with-template-or-schema` | Same generic registry schema and market-pack template | Market modes become configured market packs rather than bundled real registries. | CI-CFG-001–003, CI-STATE-002 | Multi-market fixture test |
| `skills/comp-intel/references/REF-comp-intel-wallets-competitor-registry-v3.0.0.md` | Third market registry; bidirectional | High: organization strategy and deal context | None | `replace-with-template-or-schema` | Same generic registry schema and market-pack template | One portable contract replaces all organization-specific registry variants. | CI-CFG-001–003, CI-STATE-002 | Multi-market fixture test |
| `skills/comp-intel/references/REF-comp-intel-chain-competitive-positioning-v3.0.0.md` | Counter-positioning knowledge; inbound and mutable | Critical: private positioning and approval state | None | `replace-with-template-or-schema` | `assets/positioning-context-template.md` | Ship an empty contract and synthetic example, never the source positioning. | CI-CFG-003, CI-PRV-001–002, CI-STATE-002 | Empty-template and privacy tests |
| `skills/comp-intel/references/REF-comp-intel-wallets-competitive-positioning-v3.0.0.md` | Counter-positioning knowledge; inbound and mutable | Critical: private positioning and roadmap context | None | `replace-with-template-or-schema` | Same positioning-context template | The template supports reviewed counter-claims without exposing source content. | CI-CFG-003, CI-PRV-001–002, CI-STATE-002 | Empty-template and privacy tests |

## 4. Transitive inputs and source capabilities

| Source | Role / direction | Sensitivity | Current public equivalent | Disposition | Target artifact | Rationale | Requirements | Verification |
|---|---|---|---|---|---|---|---|---|
| `docs/STD-lexicon-consumer-contract-v1.0.md` | Private terminology policy; inbound | Organization-specific | None | `interface-only` | `assets/policy-map-template.yaml` | Allow an adopter-provided terminology policy without a repository-root runtime dependency. | CI-PKG-003, CI-CFG-001, CI-PRV-001 | Direct-install closure test |
| `skills/_shared/lexicon/{market}/REF-*-lexicon-*.md` | Private terminology instances; inbound | High | None | `retain-private` | Adopter-owned policy map | Runtime data is supplied outside the installed package. | CI-CFG-002, CI-PRV-001 | Package-content scan |
| `skills/<product-workflow>/references/{positioning,persona}.md` | Product and buyer context; inbound interface | Critical | None | `retain-private` | `assets/market-pack-template.yaml`; `assets/positioning-context-template.md` | Record the required fields, not the source organization's narrative. | CI-CFG-001–003, CI-PRV-001 | Market-pack validation |
| `outputs/people/*-profile*.md` | Optional stakeholder lens; inbound pattern | Critical personal data | None | `replace-with-template-or-schema` | `assets/stakeholder-lens-template.yaml` | Real profiles never ship; adopters may supply a consented lens. | CI-PRV-001–003, CI-OUT-001 | Person-data scan; lens-isolation test |
| `outputs/bd-call-signals/case-study-opportunities.md` | Optional call-derived evidence; inbound | Critical customer and deal data | Local-file source option | `interface-only` | Local-file adapter using the evidence-input contract | The skill may read approved adopter files, but the file and producer stay outside the package. | CI-SRC-001–003, CI-PRV-001 | Optional-source absence and sensitivity tests |
| `outputs/bd-call-signals/competitor-landscape.md` | Optional deal-level landscape; inbound | Critical customer and deal data | Local-file source option | `interface-only` | Local-file adapter using the evidence-input contract | Treat as untrusted adopter evidence and never bundle an instance. | CI-SRC-001–003, CI-EVD-001–003 | Local-file adapter test |
| Runtime web retrieval | Public-source collection; inbound service | Variable, untrusted content | Mentioned in config template | `interface-only` | Source-adapter contract and controller capability | Optional adapter with URL/date capture, prompt-injection isolation and safe degradation. | CI-SRC-001–003, CI-EVD-001–003 | Web capability and failure tests |
| Runtime repository-host retrieval | Release and issue collection; inbound service | Variable, untrusted content | None | `interface-only` | Source-adapter contract and controller capability | Optional adapter; installation must not assume an account or credential. | CI-SRC-001–003, CI-PRV-003 | Missing-credential and pagination tests |
| Runtime communication-source retrieval | Internal-signal collection; inbound service | Critical private content | None | `interface-only` | Optional adapter configured by the adopter | The adapter is optional, least-privilege, review-bounded and contains no bundled workspace mapping. | CI-SRC-001–003, CI-PRV-001–003 | Capability, permission and privacy tests |

## 5. Runtime, configuration and validation surfaces

| Source | Role / direction | Sensitivity | Current public equivalent | Disposition | Target artifact | Rationale | Requirements | Verification |
|---|---|---|---|---|---|---|---|---|
| `config/capability-registry.yaml` | Private skill registration and persistence declaration; control plane | Organization-specific | `docs/SKILL-CATALOG.md` | `interface-only` | Catalog and future public package manifest | Public capability claims must match implemented behavior; private registry state does not ship. | CI-PKG-001, CI-QA-002 | Catalog/package parity test |
| `config/source-maps.yaml` | Private source identity map; inbound configuration | Critical identifiers | `assets/config-template.yaml` | `replace-with-template-or-schema` | Adopter-owned source mappings validated by config schema | Replace live identities with empty mapping fields and examples using fictional values. | CI-CFG-001–003, CI-PRV-001 | Forbidden-pattern and config tests |
| `scripts/collection/run-comp-intel.py` | Legacy process runner; execution | Critical runtime paths and tool identities | None | `rewrite-generic` | `skills/comp-intel/scripts/comp_intel.py` | Replace the legacy host command with a runtime-neutral deterministic controller. | CI-PKG-003, CI-RUN-001–005, CI-QA-001 | CLI and stage tests |
| `scripts/lib/bead_emitter.py` | Legacy run-state writer; output | Internal persistence convention | None | `replace-with-template-or-schema` | `assets/run-state.schema.json`; controller | Preserve resume and artifact accounting with unique run IDs, immutable evidence digests and explicit stages. | CI-RUN-002–004, CI-STATE-001 | State-transition tests |
| `scripts/governance/backfill-beads.py` | Legacy history backfill; migration | Private historical state | None | `exclude` | None in public v1 | Public v1 initializes clean state and does not import private historical runs. | CI-MIG-002 | Package-content scan |
| `scripts/governance/check-comp-intel.py` | Legacy cross-file checker; validation | Coupled to private filenames and mutable Markdown | None | `rewrite-generic` | `skills/comp-intel/scripts/validate_comp_intel.py` | Validate generic schemas, digests, source identity, state transitions and package closure. | CI-QA-001–002 | Validator unit tests |
| `tests/test_bead_emitter.py`; `tests/test_backfill_beads.py` | Legacy state tests; verification | Synthetic test logic mixed with legacy contracts | None | `rewrite-generic` | `skills/comp-intel/tests/` and public root acceptance tests | Retain useful failure cases while replacing legacy file and phase assumptions. | CI-QA-001, CI-MIG-002 | Public test suite |
| `tests/retrieval/comp-intel-runbook.yaml` | Private trigger-to-runbook retrieval test; verification | Low, private path coupling | None | `rewrite-generic` | Public activation and reference-routing tests | Preserve positive retrieval coverage and add negative activation cases. | CI-PKG-002–004, CI-QA-001 | Retrieval test |
| `scripts/governance/run-control.py` and workflow-control library | Prior digest-bound design evidence; control plane | Private implementation | None | `interface-only` | Public controller requirements only | Reuse the concepts of immutable digests and explicit approvals without creating a code dependency. | CI-RUN-002–004, CI-STATE-001 | Approval and digest tests |

## 6. Mutable state and generated outputs

No source instance in this section may be copied. Each pattern becomes adopter-owned data
under the configured data root.

| Source | Role / direction | Sensitivity | Current public equivalent | Disposition | Target artifact | Rationale | Requirements | Verification |
|---|---|---|---|---|---|---|---|---|
| `outputs/competitive/*-signals.md` | Collected evidence cache; output/input on resume | Potentially private and untrusted | None | `replace-with-template-or-schema` | `assets/evidence-record.schema.json`; run manifest | Normalize evidence before review and bind synthesis to its digest. | CI-EVD-001–003, CI-RUN-001–003 | Deterministic manifest and resume tests |
| `outputs/competitive/*-report.md` | Human briefing; output | Potentially private | `assets/output-template.md` | `replace-with-template-or-schema` | Output template plus approved-claim renderer | Render from approved claims and retain evidence/digest provenance. | CI-OUT-001–002, CI-STATE-002 | Golden render test |
| `outputs/competitive/positioning/*-snapshot.md` | Dated competitor snapshots; bidirectional | Potentially private | None | `replace-with-template-or-schema` | `assets/claim-record.schema.json`; `assets/positioning-context-template.md` | Structured claims are canonical; Markdown is a deterministic dated view. | CI-EVD-001, CI-STATE-002, CI-OUT-001 | Claim and render tests |
| `outputs/competitive/battlecard-gaps.md` | Shared gap tracker; bidirectional | Private strategy | None | `replace-with-template-or-schema` | `assets/change-set.schema.json`; tracker schema | Changes remain proposed until separately approved and atomically applied. | CI-RUN-004, CI-STATE-002 | Concurrency and apply tests |
| `outputs/competitive/narrative-tracker.md` | Narrative history; bidirectional | Private strategy | None | `replace-with-template-or-schema` | Claim and registry schemas | Preserve dated history without subjective in-place mutation during collection. | CI-EVD-001–003, CI-STATE-002 | Narrative-proof test |
| `outputs/competitive/win-loss-log.md` | Deal-signal tracker; bidirectional | Critical customer data | None | `replace-with-template-or-schema` | Sensitive tracker schema under adopter data root | Never bundle rows; require explicit sensitivity and confirmation state. | CI-PRV-001–003, CI-STATE-002 | Sensitivity propagation test |
| `state/runs/comp-intel-*.yaml` | Resume and completion state; bidirectional pattern | Internal run metadata | None | `replace-with-template-or-schema` | `assets/run-state.schema.json` | Use collision-resistant run identity, immutable stage history, digests, approvals and error ledger. | CI-RUN-002–004, CI-STATE-001 | Same-day, resume and corrupt-state tests |

## 7. Downstream consumers

| Source | Role / direction | Sensitivity | Current public equivalent | Disposition | Target artifact | Rationale | Requirements | Verification |
|---|---|---|---|---|---|---|---|---|
| `skills/product-page-copywriter/references/RUN-product-page-copywriter-lp-copy-workflow-prd-v1.0.md` | Reads snapshots and gaps; outbound consumer | Can expose private claims | No public coupling required | `interface-only` | Versioned approved-claim, report and rendered-snapshot interface | Consumers may read only approved, attributable outputs and must preserve source status. | CI-OUT-001–002, CI-STATE-002 | Consumer contract fixture |
| `skills/slack-thread-battlecard/{SKILL.md,references/RUN-*.md}` | Reads snapshots and gaps; outbound consumer | Can expose private strategy | No public coupling required | `interface-only` | Versioned approved-claim and change-set interface | Do not bundle the consumer; document how it distinguishes approved claims from open gaps. | CI-OUT-001, CI-RUN-004 | Consumer contract fixture |
| `skills/marketing-opportunity-scanner/references/RUN-marketing-opportunity-scanner-workflow-prd-v1.0.md` | Checks latest snapshots; outbound consumer | Potentially private | No public coupling required | `interface-only` | Run manifest and rendered-snapshot interface | A consumer can detect an existing tracked signal without reading raw evidence. | CI-STATE-001–002, CI-OUT-002 | Consumer contract fixture |

## 8. Historical design evidence

| Source | Role / direction | Sensitivity | Current public equivalent | Disposition | Target artifact | Rationale | Requirements | Verification |
|---|---|---|---|---|---|---|---|---|
| `docs/workbench/{master requirements, implementation blueprint, acceptance plan, four implementation PRDs}` | Prior private design inputs; analysis only | Mixed private context and obsolete decisions | This inventory and the public PRD | `exclude` | None | Reconcile reusable decisions during authoring, but make the public PRD self-contained and free of inaccessible dependencies. | CI-MIG-002, CI-PRV-001, CI-QA-002 | Public-link and package-content scans |

## 9. Closure conclusion

The functional closure contains:

- six existing public package files;
- one private skill entrypoint and eight manifest-declared documents;
- nine transitive input or source-capability interfaces;
- nine runtime, configuration, validation or prior-control surfaces;
- seven mutable output/state families;
- three downstream consumer interfaces; and
- one grouped family of historical private design evidence.

Repository searches also surfaced dated run instances, work-tracker records, audits, plans,
generated views and narrative mentions. They are not functional package dependencies. Dated
instances are covered by the patterns in §6; historical planning material is covered by §8;
tracker and audit mentions require no runtime interface.

Every copied-content path ends in `retain-private` or `exclude`. Every public target is either
an existing public artifact, a generic schema/template, or an interface contract. This is the
required publication boundary for the implementation PRD.
