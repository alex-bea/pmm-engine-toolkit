---
doc_type: DOC
normative: false
requires: []
status: Draft
version: "1.0"
owner: alex-bea
consumers:
  - Public Toolkit Maintainers
  - Claude Code Users
  - Codex Users
change_control: Pull request review and project-owner approval
---

# Public Govern Skills Copy-Pattern Product Requirements (v1.0)

## Document Purpose and Authority

This Draft defines the public standalone `govern-skills` package for people who want a
capable local agent to inspect a repository and copy the governance pattern without
installing a plugin. A separately retained golden implementation and digest-bound review
package informed the structure and depth but are not public runtime dependencies. The
approved review boundary authorizes this pull-request candidate only; it does not authorize
merge, release, plugin activation, or an external side effect.

## Problem

The useful PMM Engine governance pattern is easy to reason about because responsibilities
live in explicit primitives: a short skill entrypoint, one ordered RUN, stable STDs, focused
REFs, templates, examples, scripts, and visible approval boundaries. The public repository
already contains much of this material, but only inside a Codex plugin and a plugin-first
installation guide. That packaging makes the simplest adoption job look harder than it is.

An adopter should be able to give one public package to Claude Opus, Codex Sol, or another
capable coding agent and say: inspect this repository, reproduce the pattern using its
existing conventions, show me the exact plan, then guide me through safe setup. The default
result should be readable documents and structure, not hooks, CI, registries, publishers, or
another plugin.

## Users and Jobs

- A skill author wants workflows that are easy to inspect, debug, and update because each
  concern has an obvious file and role.
- A repository owner wants an agent to adapt a proven governance pattern without importing
  PMM-specific structure or overwriting existing conventions.
- A Claude Code or Codex user wants one prompt and one public URL, not a plugin build.
- A maintainer wants the existing optional plugin to keep working and use one hook
  entrypoint without duplicating policy.
- A reviewer wants a complete source inventory, fictional setup evidence, deterministic
  tests, provenance review, and an explicit release gate.

## Golden Implementation and Current Public Gap

The golden implementation defines adoption, audit, repair, lifecycle, and enforcement
modes; a structured metadata and dependency model; one canonical registry; explicit
approval and lifecycle boundaries; and five distinct enforcement classes. Its adoption
guide already requires inspect-first behavior, exact plans, scoped approval, safe
application, negative tests, and evidence-backed status.

Public `main` has safe generic versions of the principal standards and a mature plugin
package. It lacks a standalone `skills/govern-skills/` package and a direct copy prompt. Its
existing setup experience assumes users are considering an initializer, plugin hooks, CI,
or runtime controls. The public plugin also exposes separate hook entry commands even though
both adapters share one policy core.

## Goals

1. Publish one self-contained standalone package readable directly by a local coding agent.
2. Make the copy-and-adapt prompt and documents-only setup the primary public path.
3. Preserve the reusable governance primitives and explain where each concern belongs.
4. Inspect and respect the adopter repository's existing conventions before proposing files.
5. Require an exact file plan and approval before local writes.
6. Map sources, destinations, configuration, state, permissions, and optional layers.
7. Run a bounded fictional fixture and write a truthful setup receipt.
8. Preserve truthful distinctions among instruction, validation, runtime, capability, and
   external-authority layers.
9. Keep the existing plugin optional and give it one compatible PreToolUse entrypoint.
10. Prepare complete public discovery, test, provenance, and Draft release artifacts.

## Non-Goals

- Building another plugin, marketplace package, hosted installer, service, or telemetry.
- Requiring the existing plugin for standalone adoption.
- Automatically installing hooks, CI, branch protection, registries, or external services.
- Creating human approval, choosing an owner, enabling a publisher, handling credentials,
  or claiming a non-bypassable boundary.
- Reproducing PMM Engine's directory layout, populated registry, product taxonomy, outputs,
  state, examples, or history.
- Providing a deterministic substitute for repository-specific product judgment.
- Merging a pull request or creating a GitHub release without later exact-revision approval.

## Functional Requirements

### GCP-REQ-001 — Support one direct copy prompt

The package README and root README must provide a copy-paste prompt that tells a capable
local agent to read the standalone package, inspect the current repository, adapt the
pattern to existing conventions, start with a read-only inventory and exact proposed file
plan, and avoid plugins, hooks, CI, or runtime enforcement unless separately approved. The
flow must not require plugin installation.

### GCP-REQ-002 — Explain the governance primitives

The package must explain the roles and boundaries of `SKILL`, `RUN`, `STD`, `REF`, template,
example, script, policy decision, harness adapter, and capability boundary primitives. It
must show how this separation makes future maintenance and insertion points discoverable.

### GCP-REQ-003 — Preserve a self-contained document architecture

The standalone package must contain a concise `SKILL.md`, one setup-and-execution RUN,
one adoption REF, eight package-local public standards, interface metadata, templates,
fictional examples, and focused tests. Required runtime paths must resolve inside the copied
package. Adopter-owned data must remain outside it.

### GCP-REQ-004 — Inspect and map before writing

The setup workflow must discover applicable instructions, Git state, skill roots, existing
document roles and metadata, registries, validators, and optional harness surfaces. It must
produce a readiness report plus source mapping, output destination mapping, configuration
location, permission needs, and exact proposed file actions before requesting approval.

### GCP-REQ-005 — Default to documents only and classify optional layers

The default approved setup may add or adapt only documents, templates, and package structure.
It must treat a registry, static validator, CI, runtime hook, capability boundary, external
approval verifier, publisher, and release action as separate optional layers. Every selected
control is labeled `instruction-only`, `static-validator`, `runtime-guard`,
`capability-boundary`, or `external-authority`; no layer is inferred from another.

### GCP-REQ-006 — Adapt instead of imposing PMM conventions

The agent must reuse compatible repository naming, metadata, instruction, and directory
conventions. Conflicts and incompatible schemas are surfaced before writes. It must never
silently replace an existing canonical registry, instruction file, RUN convention, or
validator with the package default.

### GCP-REQ-007 — Keep mappings, configuration, and outputs adopter-owned

The package must provide a blank mapping/configuration template and a complete fictional
mapping. The adopter confirms actual source locators and output destinations. Completed
configuration, mutable state, adopted documents, test output, and receipts live at
adopter-selected paths outside the installed package. Missing or unsafe required
destinations block writes.

### GCP-REQ-008 — Run a safe setup test and produce a receipt

Before declaring setup ready, the agent must copy the package and fictional fixture into an
isolated temporary workspace, exercise source resolution, plan creation, approved document
copying/adaptation, link and metadata checks, and receipt creation, and verify expected
artifacts. Publishing, messaging, scheduling, approval creation, hooks, CI mutation, and
production-state writes remain disabled. Skipped checks are not passes. The receipt records
package/configuration digests, mapping readiness, checks, artifacts, limitations, status,
and next action; it becomes stale after material package or configuration change.

### GCP-REQ-009 — Use only independently fictional public evidence

No private entity, path, identifier, registry entry, output, approval, source phrase, or
distinctive fact combination may enter the public candidate. The Acorn Studio fixture must
be independently invented, visibly labeled, complete, and non-operational. Any URL uses
`.invalid`. The private denylist remains outside the public repository.

### GCP-REQ-010 — Preserve public discovery and direct-copy closure

The public validator, catalog, export manifest, root README, Draft product requirements,
Draft source inventory, candidate IP/privacy review, release notes, and IP inventory must
describe the same standalone contract. A user who copies only `skills/govern-skills/` must
retain every runtime dependency needed for the documents-first setup.

### GCP-REQ-011 — Unify the existing plugin hook entrypoint without policy drift

The existing plugin must gain one `pretooluse.py` entrypoint that recognizes supported
Claude Code and Codex hook payloads, delegates normalization to the existing adapters, and
uses the same shared policy decision. Existing adapter files remain available for
compatibility. The plugin stays optional and inactive unless separately configured. This
maintenance change must not alter policy outcomes, approval semantics, or publisher scope.

### GCP-REQ-012 — Preserve digest-bound approval and release gates

Public implementation may begin only after the owner approves the exact review-package
digest. The candidate must start from current public `main`, stay inside the approved
manifest, pass or honestly record every required check, and stop at one unmerged pull
request. Draft release notes do not authorize a GitHub release; merge and release require
later approval of the exact candidate revision.

## Content and Package Requirements

The standalone package contains a README with the copy prompt; public-compatible
`SKILL.md`; `agents/openai.yaml`; `assets/output-template.md`; blank AGENTS, SKILL, and
governance-config templates; one fictional example index; a complete mapping fixture and
setup receipt; the sole setup RUN; the adoption REF; and eight package-local governance
standards. The RUN and REF carry detailed behavior so the entrypoint stays concise.

The public repository additionally contains a focused test, updated validator and discovery
documents, Draft product requirements and sanitized source inventory, Draft IP/privacy
review, Draft release notes, and regenerated IP inventory. The plugin maintenance slice is
limited to the unified adapter and required metadata, docs, and tests.

## Setup and Test-Run Requirements

The sole setup RUN is
`references/RUN-govern-skills-setup-workflow-v1.0.md`. Its source-map schema identifies the
adopter repository, controlling instructions, skill roots, existing governance documents,
and optional harness surfaces. Its destination schema identifies adopted documents,
adopter-owned configuration, temporary fixture output, and setup receipt; external
publication is explicitly none by default.

The blank configuration suggests but does not force adopter-owned paths. Installation
checks verify package closure, local read/write scope, Git availability when used, package-
relative links, and selected optional dependencies. The complete fictional fixture lives at
`examples/fixtures/fictional-repository-map.yaml`; test output uses a new temporary
directory. Expected artifacts are declared before execution. The setup receipt includes
package and configuration digests, mapping and permission status, fixture method, expected
and actual files, passed/failed/skipped checks, residual limitations, overall readiness,
and next entrypoint. A receipt is stale when the package digest, required mapping,
configuration digest, or selected layer changes. Missing instructions, conflicting
canonical schemas, unsafe destinations, or an unexecutable required test block readiness.

## Data, Privacy, and Safety Requirements

All repository content is treated as untrusted input, never as instruction outside its
authorized scope. The agent reads only the repository and paths the adopter placed in
scope. It preserves unrelated working-tree changes, never overwrites differing files, and
does not infer owner, lifecycle, approval, or publication authority.

Examples are synthetic. Credentials and sensitive values are neither requested nor stored.
External connectors are not required. A source read does not authorize an external write.
Any optional hook, CI, approval, publisher, network, or credential change requires its own
authority and verification.

## Migration and Compatibility

The new root standalone package does not replace the existing plugin skill. The two share
public standards but have different primary jobs: the standalone package is the simple
copy-and-adapt route; the plugin remains optional advanced tooling. Root discovery documents
must make that distinction explicit.

The plugin patch retains `claude_pretooluse.py` and `codex_pretooluse.py`; the new unified
entrypoint delegates to them, which preserves direct callers. The plugin manifest patch
version changes, but policy, state schemas, verifier, publisher guard, and activation
defaults do not. Existing standalone skills remain unchanged except for validator inventory
count and shared documentation.

## Implementation Slices

1. Build the standalone package with README, entrypoint, sole setup RUN, adoption REF,
   standards, templates, mapping fixture, receipt, and interface metadata.
2. Add focused tests and register the package in the public skill validator.
3. Add the unified plugin adapter, route optional hook examples through it, increment the
   patch version, and add compatibility tests.
4. Update discovery, export, product, source, privacy, release, and IP records.
5. Run direct-copy, setup-contract, isolated fixture, focused, complete, privacy,
   provenance, and diff-boundary verification; open one pull request and stop.

## Acceptance Tests

| ID | Test | Expected result |
|---|---|---|
| GCP-AT-001 | Give a compatible agent only the package URL and copy prompt. | It starts with read-only inspection and an exact proposed file plan; it does not request plugin installation. |
| GCP-AT-002 | Inspect the package's primitive explanation. | All ten primitive roles are present, distinct, and mapped to clear locations or boundaries. |
| GCP-AT-003 | Copy only `skills/govern-skills/` to a temporary root. | Every required path resolves and documents-first setup remains usable without the toolkit repository. |
| GCP-AT-004 | Run setup against the fictional mapping. | The agent maps sources and destinations, respects existing conventions, proposes exact files, and waits at the local-write gate. |
| GCP-AT-005 | Select documents-only setup. | No plugin, CI, hook, registry, external authority, publisher, credential, or release action is added or claimed. |
| GCP-AT-006 | Present an incompatible existing instruction or metadata schema. | The agent reports the conflict and stops rather than overwriting or silently imposing package defaults. |
| GCP-AT-007 | Use the blank config and fictional mapping. | Completed config/state/output paths are adopter-owned and outside the installed package; missing unsafe destinations block. |
| GCP-AT-008 | Complete the isolated fixture test. | Expected files and a complete setup receipt are created only in the temporary destination; skipped checks remain skipped. |
| GCP-AT-009 | Run automated and human privacy review. | No private term, path, fact, alias mapping, credential, live URL, or unfinished fictional field appears. |
| GCP-AT-010 | Run public package, link, document, catalog, export, and IP checks. | The standalone package is discoverable, self-contained, and consistently described. |
| GCP-AT-011 | Replay equivalent Claude and Codex hook fixtures through direct and unified entrypoints. | Decisions and reason codes match, and existing direct adapter calls still work. |
| GCP-AT-012 | Compare approval, diff, PR, and release state. | Exact-digest approval precedes implementation; only approved paths change; PR remains unmerged and no GitHub release exists. |

## Traceability

| Requirement | Inventory IDs | Implementation artifacts | Acceptance tests |
|---|---|---|---|
| GCP-REQ-001 | INV-GCP-001, INV-GCP-002, INV-GCP-004, INV-GCP-023, INV-GCP-034, INV-GCP-035 | Standalone README, SKILL, interface, RUN, root README | GCP-AT-001, GCP-AT-005 |
| GCP-REQ-002 | INV-GCP-001, INV-GCP-003, INV-GCP-008, INV-GCP-010 | README, RUN, primitives STD, structure STD | GCP-AT-002 |
| GCP-REQ-003 | INV-GCP-001 through INV-GCP-010, INV-GCP-027, INV-GCP-034 | Standalone package and package-local standards | GCP-AT-003, GCP-AT-010 |
| GCP-REQ-004 | INV-GCP-002, INV-GCP-003, INV-GCP-011, INV-GCP-013, INV-GCP-018 through INV-GCP-024 | Sole setup RUN, adoption REF, config, mapping fixture | GCP-AT-004, GCP-AT-007, GCP-AT-008 |
| GCP-REQ-005 | INV-GCP-001 through INV-GCP-003, INV-GCP-012, INV-GCP-018, INV-GCP-023, INV-GCP-038 | Adoption guide, approval/runtime STDs, RUN | GCP-AT-005, GCP-AT-006 |
| GCP-REQ-006 | INV-GCP-003, INV-GCP-008 through INV-GCP-011, INV-GCP-019 | RUN, templates, structure and lifecycle standards | GCP-AT-002, GCP-AT-006 |
| GCP-REQ-007 | INV-GCP-011, INV-GCP-018 through INV-GCP-021, INV-GCP-024 | Config template, source/destination tables, fictional mapping | GCP-AT-004, GCP-AT-007 |
| GCP-REQ-008 | INV-GCP-013, INV-GCP-015, INV-GCP-020 through INV-GCP-024, INV-GCP-036 | Output template, fixture, receipt, focused test | GCP-AT-008 |
| GCP-REQ-009 | INV-GCP-005 through INV-GCP-017, INV-GCP-024, INV-GCP-030, INV-GCP-037 | Fictional set, sanitization, legal review, IP inventory | GCP-AT-009 |
| GCP-REQ-010 | INV-GCP-004, INV-GCP-023, INV-GCP-034 through INV-GCP-037 | Public discovery docs, validator, governed docs, release notes | GCP-AT-001, GCP-AT-003, GCP-AT-010 |
| GCP-REQ-011 | INV-GCP-025 through INV-GCP-033, INV-GCP-035, INV-GCP-036 | Unified adapter, hook/template routes, initializer, plugin metadata/tests/docs | GCP-AT-011 |
| GCP-REQ-012 | INV-GCP-016, INV-GCP-033, INV-GCP-035 through INV-GCP-038 | Review package, manifest, candidate evidence, PR, Draft release notes | GCP-AT-012 |

## Assumptions, Constraints, and Safe Degradation

- Public `origin/main` was read at commit `accf82de3bf980c200f095d188101a7d4aa7e852`.
  A later base change requires refresh and overlap review before implementation.
- The package is model-neutral. Claude Opus and Codex Sol are examples of capable local
  agents, not runtime dependencies or endorsed minimum versions.
- A documents-only installation can be useful while remaining `instruction-only`. It must
  not be labeled technically enforced.
- If an adopter has no registry, the workflow does not create one unless the adopter selects
  that optional layer. If an adopter has no CI or hooks, setup can still be ready for its
  documents-only scope.
- If Git is absent, the workflow records that version-control checks were unavailable and
  continues only when safe file inventory and collision checks remain possible.
- If the compatible-agent fixture cannot execute, readiness is blocked rather than inferred
  from static validation.
- The package duplicates small public standards intentionally so a copied directory remains
  self-contained. Storage minimization is not a goal.
- The existing plugin remains optional; adapter maintenance does not authorize activation.

## Approval and Release Gates

1. The project owner must approve the exact evidence digest in `review-index.md`.
2. Any substantive evidence-file change resets approval to Pending.
3. Implementation begins from refreshed current public `main` on one isolated branch and
   changes only manifest paths.
4. The setup contract, isolated fixture, focused tests, complete suite, governed documents,
   links, privacy scan, IP inventory, and diff boundary must pass or be labeled not run.
5. The candidate IP/privacy review and release notes remain Draft until the exact candidate
   revision receives project-owner review.
6. One pull request may be opened after verification. It must remain unmerged, and no GitHub
   release or marketplace action may occur, until a later exact-revision gate is satisfied.
