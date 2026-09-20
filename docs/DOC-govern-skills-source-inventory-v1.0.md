---
doc_type: DOC
normative: false
requires:
  - DOC-govern-skills-product-requirements-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-skill-dependencies-v1.0.md
status: Superseded
version: "1.0"
owner: alex-bea
consumers:
  - govern-skills maintainers
  - implementation reviewers
  - privacy reviewers
change_control: Pull request review
---

# Govern Skills Copy-Pattern Source Inventory (v1.0)

> Superseded by `DOC-govern-skills-source-inventory-v1.1.md`, which inventories the
> conditional-setup amendment and its unchanged boundaries.

This advisory inventory records the bounded design and public-target closure used for the
standalone package. Private source content and real operating data are not distributed.
Paths that identify golden artifacts describe their roles for provenance; they are not
runtime dependencies, adopter defaults, or a reversible private-to-fictional map.

| ID | Source path or pattern | Role | Direction | Sensitivity | Current public equivalent | Disposition | Target artifact | Rationale | Requirement IDs | Verification |
|---|---|---|---|---|---|---|---|---|---|---|
| INV-GCP-001 | Golden governance skill entrypoint | Canonical private entrypoint | seed | generic | Plugin-local `govern-skills/SKILL.md`; no standalone package | rewrite-generic | `skills/govern-skills/SKILL.md` | Preserve modes and truthfulness while making copy-by-agent the primary job and plugin use optional. | GCP-REQ-001, GCP-REQ-002, GCP-REQ-005 | Trigger, route, and privacy review. |
| INV-GCP-002 | Golden governance adoption guide | Private adoption sequence | dependency | generic | Plugin-local guide | rewrite-generic | Standalone package REF | Preserve inspect, report, decide, plan, approve, apply, verify, and status flow; default to documents only. | GCP-REQ-001, GCP-REQ-004, GCP-REQ-005 | Semantic parity matrix. |
| INV-GCP-003 | Golden governance workflow | Audit, repair, lifecycle, and enforcement workflow | dependency | generic | Plugin-local RUN v1.0 | rewrite-generic | Sole `RUN-govern-skills-setup-workflow-v1.0.md` | Consolidate setup and normal operation into the required single RUN without private repository assumptions. | GCP-REQ-003, GCP-REQ-004, GCP-REQ-006 | Setup-contract and workflow review. |
| INV-GCP-004 | Golden interface metadata | Interface metadata | dependency | generic | Plugin-local interface | rewrite-generic | Standalone `agents/openai.yaml` | Make the copy-and-adapt job discoverable without requiring plugin installation. | GCP-REQ-001, GCP-REQ-010 | Interface validator. |
| INV-GCP-005 | Golden skill history | Private skill history | design-evidence | internal | Plugin changelog | retain-private | None | Private version history is not required for the public standalone runtime. | GCP-REQ-009, GCP-REQ-010 | Confirm no public dependency. |
| INV-GCP-006 | Golden lifecycle and authority standard | Private lifecycle and authority standard | governance | mixed | Public generic STD already exists | retain-private | Package-local copy of the existing public STD | Use already-public generic text rather than sanitizing the richer populated private standard. | GCP-REQ-003, GCP-REQ-005, GCP-REQ-006 | Public-standard byte parity. |
| INV-GCP-007 | Golden document metadata standard | Private document metadata standard | governance | generic | Public generic STD already exists | retain-private | Package-local copy of the existing public STD | The public standard supplies a sufficient portable metadata contract. | GCP-REQ-003 | Public-standard byte parity. |
| INV-GCP-008 | Golden package structure standard | Private package structure standard | governance | mixed | Public v1.0 generic STD | retain-private | Package-local copy of the existing public v1.0 STD | Preserve portable shape from the public standard; exclude private sync, bead, and registry conventions. | GCP-REQ-002, GCP-REQ-003, GCP-REQ-006 | Public-standard byte parity. |
| INV-GCP-009 | Golden repository-structure standard | Private repository-wide layout | governance | internal | No package-local equivalent required | retain-private | None | The adopter's repository layout must be inspected and adapted, not replaced with the golden repository's topology. | GCP-REQ-004, GCP-REQ-007, GCP-REQ-009 | Confirm no copied private layout. |
| INV-GCP-010 | Golden shared-code architecture standard | Private shared-code architecture | governance | internal | Public primitives and dependency STDs | interface-only | Optional script-boundary guidance in the RUN | Preserve the principle that deterministic helpers are separate; do not prescribe the golden repository's script tree. | GCP-REQ-002, GCP-REQ-006 | Workflow language review. |
| INV-GCP-011 | Populated canonical golden registry | Populated canonical private registry | upstream | confidential | Public blank skill-registry template inside plugin | replace-with-template-or-schema | `assets/templates/governance-config.yaml` and fictional map | Preserve ownership and lifecycle categories without publishing entries, products, identities, targets, or persistence paths. | GCP-REQ-004, GCP-REQ-006, GCP-REQ-007, GCP-REQ-009 | Blank-template and synthetic-fixture review. |
| INV-GCP-012 | Golden repository instruction baseline | Repository instruction baseline | governance | generic | Public plugin AGENTS template | rewrite-generic | Standalone `assets/templates/AGENTS.md` | Preserve approval, digest, schedule, and publication categories while explicitly labeling instructions as non-enforcement. | GCP-REQ-003, GCP-REQ-005 | Template and fictional adoption review. |
| INV-GCP-013 | Golden setup and publicization contract | Setup, mapping, fixture, and receipt contract | design-evidence | internal | No public runtime dependency | retain-private | Sole public setup RUN and receipt template | Use the generic contract shape without exporting the private publicizer or its review history. | GCP-REQ-004, GCP-REQ-007, GCP-REQ-008 | Setup-contract validator. |
| INV-GCP-014 | Golden deterministic validation family | Governance validators and generated-view checks | governance | internal | Public skill-pack and document validators | interface-only | Public verification procedure | Adopters may reuse or write validators only when selected; documents-only setup does not copy private scripts. | GCP-REQ-005, GCP-REQ-006 | No private script dependency; public checks pass. |
| INV-GCP-015 | Golden governance behavior tests | Private behavior evidence | design-evidence | internal | Public governance-plugin tests | retain-private | New public focused test | Preserve behavior categories through new tests, not by copying private fixtures. | GCP-REQ-008, GCP-REQ-009, GCP-REQ-011 | Focused public suite. |
| INV-GCP-016 | Earlier governance publicization reviews | Historical publicizer evidence | design-evidence | confidential | Resulting public plugin package and PRs | retain-private | None | Prior reviews explain design history but contain private roots, candidates, and approval records. | GCP-REQ-009, GCP-REQ-012 | Confirm no content export. |
| INV-GCP-017 | Generated golden governance outputs | Generated private governance output family | output | internal | Public validators only | retain-private | None | Generated audits are not templates or runtime dependencies. | GCP-REQ-009 | Pattern-bounded exclusion review. |
| INV-GCP-018 | Adopter-selected repository root and applicable instruction files | Repository source map | upstream | mixed | Existing public adoption guide | interface-only | Source mapping in setup RUN and config template | The local agent inspects only the repository and instruction scope authorized by the adopter. | GCP-REQ-004, GCP-REQ-007 | Read-only preflight and mapping fixture. |
| INV-GCP-019 | Adopter skill roots, standards, registries, and existing validators | Governance source map | upstream | mixed | Existing plugin audit | interface-only | Source mapping in setup RUN and config template | Existing conventions are discovered and adapted rather than overwritten. | GCP-REQ-003, GCP-REQ-004, GCP-REQ-007 | Compatibility report. |
| INV-GCP-020 | Adopter-selected document, configuration, test, and receipt paths | Output destination map | downstream | mixed | Existing plugin initializer paths | replace-with-template-or-schema | Destination mapping in setup RUN and config template | Destinations are user-owned, confirmed before writes, and outside the installed package. | GCP-REQ-004, GCP-REQ-007 | Destination write checks. |
| INV-GCP-021 | Adopter-owned configuration and mutable state | Setup configuration and state | state | mixed | Plugin `.agents/governance/` layout | replace-with-template-or-schema | Blank config template plus adopter-selected location | Provide a suggested shape but do not silently create a canonical registry or mutable state. | GCP-REQ-004, GCP-REQ-007 | Config digest and location check. |
| INV-GCP-022 | Setup receipt interface | Setup receipt | setup | mixed | No qualifying private receipt | replace-with-template-or-schema | `assets/output-template.md` and fictional receipt | Record what was inspected, written, tested, skipped, and proven without secrets. | GCP-REQ-008 | Receipt completeness and staleness test. |
| INV-GCP-023 | Git, Markdown-capable editor, and compatible local coding agent | Runtime dependencies | setup | generic | Public toolkit requirements | interface-only | Installation checks in setup RUN | No plugin, package manager, hosted service, connector, or Python dependency is required for documents-only setup. | GCP-REQ-001, GCP-REQ-004, GCP-REQ-010 | Dependency probe and safe degradation. |
| INV-GCP-024 | Temporary fictional repository workspace | Safe test-run interface | setup | synthetic | Existing public fictional adoption example | replace-with-template-or-schema | `examples/fixtures/fictional-repository-map.yaml` | The test writes only to a temporary destination and disables hooks, CI mutation, approval creation, messaging, scheduling, and publishing. | GCP-REQ-008, GCP-REQ-009 | Isolated fixture execution. |
| INV-GCP-025 | `plugins/skill-governance/skills/govern-skills/SKILL.md` on public `main` | Current plugin entrypoint | public-current | public | Same path | retain-public | Same path unchanged | The plugin remains an optional advanced distribution; it does not become the standalone package source of truth. | GCP-REQ-001, GCP-REQ-010 | Diff check. |
| INV-GCP-026 | `plugins/skill-governance/skills/govern-skills/agents/openai.yaml` on public `main` | Current plugin discovery metadata | public-current | public | Same path | retain-public | Same path unchanged | Existing plugin invocation remains valid. | GCP-REQ-010, GCP-REQ-011 | Byte comparison. |
| INV-GCP-027 | `plugins/skill-governance/skills/govern-skills/references/*.md` on public `main` | Current plugin RUN, REF, and eight STD files | public-current | public | Same paths | retain-public | Same paths unchanged | The existing public documents are reusable design inputs; the plugin copy remains supported. | GCP-REQ-003, GCP-REQ-005, GCP-REQ-011 | Bounded family lists ten files; diff and mirror checks. |
| INV-GCP-028 | `plugins/skill-governance/skills/govern-skills/assets/schemas/*.json` on public `main` | Current optional enforcement schemas | public-current | public | Same paths | retain-public | Same paths unchanged | Schemas remain plugin-only optional enforcement support and are not required by the standalone copy route. | GCP-REQ-005, GCP-REQ-011 | Bounded family lists six files; JSON checks. |
| INV-GCP-029 | `plugins/skill-governance/skills/govern-skills/assets/templates/*` on public `main` | Current plugin installation templates | public-current | public | Same paths | retain-public | Only `claude-settings.json` changes for unified entrypoint | Retain nine templates; modify the Claude hook command only. | GCP-REQ-011 | Bounded family count, JSON/YAML checks, and diff review. |
| INV-GCP-030 | `plugins/skill-governance/skills/govern-skills/assets/examples/fictional/EX-governance-adoption.md` | Current plugin fictional example | public-current | synthetic | Same path | retain-public | Same path unchanged | Existing advanced enforcement example remains distinct from the new documents-only fixture. | GCP-REQ-009, GCP-REQ-011 | Diff and privacy review. |
| INV-GCP-031 | `plugins/skill-governance/skills/govern-skills/scripts/*.py` on public `main` | Current initializer, policy, control, adapters, verifier, and publisher | public-current | public | Same paths | rewrite-generic | Add unified adapter; minimally update initializer | Preserve seven existing scripts and behavior; add one delegating entrypoint with no policy duplication. | GCP-REQ-011 | Bounded family count, AST parse, and behavior matrix. |
| INV-GCP-032 | `plugins/skill-governance/hooks/hooks.json` on public `main` | Current Codex hook registration | public-current | public | Same path | rewrite-generic | Same path | Change only the command target from Codex-specific adapter to the unified adapter. | GCP-REQ-011 | Hook manifest and payload tests. |
| INV-GCP-033 | `plugins/skill-governance/.codex-plugin/plugin.json` and `CHANGELOG.md` | Plugin version and history | governance | public | Same paths | rewrite-generic | Same paths | Record the compatible patch-level adapter maintenance; do not make the plugin the default route. | GCP-REQ-011, GCP-REQ-012 | Manifest and changelog validation. |
| INV-GCP-034 | `skills/govern-skills/` on public `main` | Target standalone package | public-current | public | Absent | rewrite-generic | New standalone package | Create one self-contained package rather than requiring plugin installation. | GCP-REQ-001 through GCP-REQ-010 | Full package and isolated-copy validation. |
| INV-GCP-035 | Public root README, catalog, export manifest, and plugin guide | Discovery and distribution surfaces | governance | public | Existing files | rewrite-generic | Approved documentation updates | Present standalone copy first, plugin second, and preserve limitations. | GCP-REQ-001, GCP-REQ-010, GCP-REQ-011 | Link and claim review. |
| INV-GCP-036 | Public validators and unit suite | Validation interfaces | governance | public | Existing scripts and tests | rewrite-generic | Validator registration and two focused test files | Add only coverage required for the new standalone package and unified adapter. | GCP-REQ-008, GCP-REQ-010, GCP-REQ-011, GCP-REQ-012 | Focused and complete suites. |
| INV-GCP-037 | Public IP inventory, candidate legal review, and release notes | Provenance and release interfaces | governance | public | Existing inventory and prior reviews | rewrite-generic | New Draft reviews/notes and regenerated inventory | Record exact provenance and keep release pending until the candidate gate. | GCP-REQ-009, GCP-REQ-012 | Inventory parity and status review. |
| INV-GCP-038 | External plugin marketplace, GitHub release, hooks, CI settings, approval services, and publishers | External mutation interfaces | downstream | credential-risk | Existing optional plugin and external systems | interface-only | None before later approval | These surfaces are explicitly outside review-mode writes and default setup; absence is safe. | GCP-REQ-005, GCP-REQ-012 | Prove no external side effect occurred. |

## Closure Boundaries

- **Private skill closure:** Every file in the golden governance skill and every declared
  manifest dependency is represented. The populated registry and repo-wide
  standards are authoring evidence, not public runtime dependencies.
- **Private validators and tests:** These are bounded as implementation families because
  the public package does not copy their code. Only their behavior categories inform new,
  independently written public tests.
- **Generated history:** Private governance outputs and prior publicizer packages are
  bounded families retained for design and approval history; none is published.
- **Existing public plugin:** The current package is bounded by four exact families:
  ten reference documents, six schemas, nine templates, one fictional example, and seven
  Python scripts, plus its entrypoint and interface. All are retained; only the three named
  adapter-related paths and plugin metadata may change.
- **Target package:** `skills/govern-skills/` is absent on public `main`; every proposed file
  appears separately in the public change manifest.
- **Source map:** The adopter repository, instructions, skill roots, standards, and current
  checks are interfaces. The public package never embeds an adopter's completed mapping.
- **Output destinations:** Adopted documents, configuration, fixture output, and setup
  receipt use adopter-confirmed locations outside the package. No external destination is
  selected by default.
- **Mutable state:** The standalone workflow is stateless except for an adopter-owned
  configuration and setup receipt. Those files are not public package content.
- **Setup receipt:** No qualifying private receipt exists. A complete fictional receipt is
  required and cannot be represented as production evidence.
- **Runtime dependencies:** A local compatible agent, readable repository, and ordinary file
  access are the minimum. Git is used when present. Python, hooks, CI, plugins, and services
  are optional and must degrade safely.
- **Safe test:** The fixture test is confined to a temporary directory, uses synthetic
  inputs, and disables all external and authority-bearing actions.
- **External systems:** Marketplace, GitHub release, branch protection, approval verifier,
  publisher, credentials, and live connectors are interface-only and are not recursively
  inventoried or invoked.
