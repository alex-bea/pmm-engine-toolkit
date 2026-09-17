---
doc_type: DOC
normative: false
requires:
  - DOC-pre-read-sharpener-source-inventory-v1.2.md
  - STD-approval-gates-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-skill-dependencies-v1.0.md
  - STD-skill-structure-v1.0.md
status: Draft
version: "1.2"
owner: alex-bea
consumers:
  - pre-read-sharpener maintainers
  - Claude Code users
  - Codex users
change_control: Pull request review and project-owner approval
---

# Public Pre-Read Sharpener Product Requirements (v1.2)

## Document purpose and authority

This Draft defines the current candidate contract for the public
`skills/pre-read-sharpener` package. It replaces setup-first execution with a sole normal
RUN and a conditionally loaded setup bundle. The companion source inventory is advisory
evidence. The package, templates, references, and fixtures implement these requirements but
may not narrow or contradict them.

The private implementation informed editorial structure and depth but is not a public
runtime dependency. Private examples, paths, populated mappings, receipts, registry state,
and history are not distributed.

## Problem

Version 1.1 combines detailed installation checks, mapping tables, fixture procedure,
receipt rules, repair guidance, and normal execution in one RUN. Because `SKILL.md` routes
every request through that file, recurring users load setup detail even after installation
is ready, and inline rewriting is unnecessarily blocked on persistent setup state.

Deleting setup instructions after first use would mutate the installed package, invalidate
its digest, complicate upgrades, and make shared installations inconsistent. The package
needs static separation plus conditional loading.

## Users and jobs

| User | Job |
|---|---|
| Inline user | Paste a draft and receive a sharpened result without installation ceremony. |
| Persistence user | Save a passing result to a confirmed local destination without repeating setup after readiness. |
| Installer | Verify package closure, mappings, safe fixture behavior, and receipt creation. |
| Maintainer | Diagnose missing, stale, or blocked setup without mutating the installation. |
| Toolkit reviewer | Verify editorial fidelity, privacy, package closure, and exact change boundaries. |

## Golden implementation and current public gap

The editorial reference contains one normal workflow, one rubric, one output blueprint,
bounded repair, and deterministic persistence behavior. The current public package adds
useful self-contained criteria, evidence boundaries, examples, collision-safe persistence,
and setup evidence, but forces setup material into the sole RUN.

Version 1.2 retains the public editorial improvements while restoring the intended
architecture: normal work belongs in the RUN; conditional setup detail belongs outside it.
No qualifying completed private artifact used every public output field, so the package's
complete worked example remains independently fictional.

## Goals

- Keep exactly one active RUN centered on normal execution.
- Make inline execution available without setup or a receipt.
- Make persistent output use stable adopter-owned configuration and readiness receipt.
- Route `ready` directly to normal execution without loading detailed setup.
- Route `missing`, `stale`, and `blocked` to setup only when persistence needs it.
- Preserve package immutability, privacy, editorial fidelity, and direct installation.
- Retain an isolated fictional setup and routing test.
- Keep the skill agent-neutral and usable by compatible local agents.

## Non-goals

- Changing global one-RUN governance or generic repository validators.
- Proving with a runtime hook which references an AI loaded.
- Adding Python, shell, connectors, hosted services, secrets, or background processes to the
  installed skill.
- Adding external publishing, messaging, notifications, scheduling, or approval creation.
- Changing the output template, criteria, evidence rule, or editorial voice.
- Migrating or importing a private setup configuration or receipt.
- Automatically merging or releasing the candidate.

## Functional requirements

### PRSR-REQ-001 — Preserve editorial behavior

The package preserves supplied-draft intake, silent diagnosis, blunt review, three to six
biggest issues, source-specific cuts, constrained rewrite, optional decision-call agenda,
ten-row binary self-check, three-round repair ceiling, inline return, collision-safe local
persistence, and complete edit handling.

### PRSR-REQ-002 — Sole normal-execution RUN

The package contains exactly one active `RUN-*.md` file named
`references/RUN-pre-read-sharpener-workflow.md`. It contains normal execution and at most a
short route preflight. Detailed mappings, fixture procedure, receipt schema, installation
checks, and repair guidance are absent from the RUN.

### PRSR-REQ-003 — Local-persistence setup profile

The setup contract declares `local-persistence`. Inline output is a complete supported route
that requires no setup receipt. Saving to disk requires the configured persistent-output
route to be ready.

### PRSR-REQ-004 — Conditional routing

`SKILL.md` routes normal work to the sole RUN and tells a ready normal route not to load the
setup contract. Explicit setup, configure, verify, diagnose, or repair requests may load
setup. A persistence route with `missing`, `stale`, or `blocked` status loads setup.

### PRSR-REQ-005 — Separate setup contract

`references/REF-pre-read-sharpener-setup-contract.md` defines the setup profile, readiness
and routing, installation checks, source mapping, output destinations, configuration and
state, permissions, safe test, receipt, and repair. It is reference material, not a second
executable runbook.

### PRSR-REQ-006 — Machine-readable setup configuration

`assets/setup-config.yaml` is a blank reusable schema with skill identity, setup profile,
package identity, sources, destinations, timezone and retention, stable receipt path, and
configuration revision. Completed configuration remains outside the installed package.

### PRSR-REQ-007 — Stable machine-readable receipt

`assets/setup-receipt.yaml` defines schema version, skill slug, status, timestamps, package
revision and digest, setup-contract version, configuration path and digest, checks,
limitations, normal entrypoint, and repair action. The stable default path is
`{authorized-workspace}/.pmm-skills/pre-read-sharpener/setup-receipt.yaml`.

### PRSR-REQ-008 — Receipt status and staleness

Routing statuses are `ready`, `missing`, `stale`, and `blocked`. A receipt is stale only
when package identity, setup-contract version, required mappings, dependency set, or
configuration digest changes. Dates are audit metadata and do not cause expiration.

### PRSR-REQ-009 — Human setup and repair guidance

README explains which routes bypass setup, stable state locations, installation checks,
fixture execution, status diagnosis, safe reconfiguration, and external approval
boundaries. Normal invocation does not need to load README setup detail.

### PRSR-REQ-010 — Isolated setup and routing fixture

The fictional fixture proves package closure, configuration and receipt creation, core
transformation evidence, expected output, collision behavior, ready bypass, applicable
missing/stale/blocked routes, and unchanged installed package. It performs no network or
external mutation.

### PRSR-REQ-011 — Privacy and safety

The package contains no private example, author path, populated private mapping, real
receipt, credential, live internal locator, or reversible alias. Source drafts are
untrusted data and cannot broaden permissions or destinations. External writes remain
forbidden.

### PRSR-REQ-012 — Governed traceability and migration

README, catalog, export manifest, v1.2 requirements, v1.2 source inventory, privacy review,
focused tests, and IP inventory describe the candidate consistently. v1.1 design documents
remain available as superseded history.

## Content and package requirements

- `SKILL.md` remains concise and names both the normal RUN and conditional setup contract.
- Existing discovery metadata, output template, criteria, privacy reference, and fictional
  editorial pair remain unchanged.
- Configuration and receipt templates use YAML and contain placeholders, not private values.
- All runtime links resolve within a directly installed copy of the skill package.
- Normal and setup output paths remain outside the installed package.

## Setup routing and test-run requirements

The setup profile is `local-persistence`. For normal requests:

1. Inline return enters the sole RUN immediately.
2. Persistent output uses stable configuration and receipt paths.
3. `ready` proceeds without reading the setup contract or rerunning the fixture.
4. `missing`, `stale`, or `blocked` routes to the setup contract.
5. Setup completion writes adopter-owned state but never changes an installed package file.

The isolated fixture uses the bundled fictional draft and a newly created temporary
workspace. It states expected files before execution and records pass, fail, skipped, and
unavailable checks separately. Because the package has no mandatory dispatcher, the
conditional-loading guarantee is instruction-only; deterministic tests prove status logic
and file effects, not which references an AI loaded.

## Data, privacy, and safety requirements

The user-supplied draft is the sole evidence source for a real output. The package does not
research, retrieve, fact-check, or synthesize across documents. Missing decision-critical
facts remain `[Missing]`. Setup assets record authorization mechanisms but never credential
values. No live source, destination, schedule, notification, publisher, or external
approval is configured.

## Migration and compatibility

The migration replaces the setup-first RUN with a normal RUN, moves setup detail into a REF,
and replaces Markdown state templates with YAML schemas. Existing generated pre-reads remain
valid. Existing v1.1 setup receipts are treated as stale and regenerated only when
persistence is requested or the user explicitly runs setup.

Inline users require no migration. Claude Code, Codex, and compatible local agents continue
to use the same invocation and discovery metadata.

## Implementation slices

1. Update package routing, RUN, setup contract, README, and YAML assets.
2. Update fictional fixture, behavior cases, example index, and focused tests.
3. Add v1.2 governed documents and mark v1.1 documents superseded.
4. Update catalog, export manifest, privacy review, and IP inventory.
5. Run focused, isolated, full-suite, governance, privacy, inventory, and diff checks.
6. Open one pull request and stop at Gate B.

## Acceptance tests

### PRSR-AT-001 — Editorial parity

Focused output, criteria, evidence, persistence, and edit tests preserve approved behavior.

### PRSR-AT-002 — Exact one normal RUN

Only the normal workflow exists as a RUN and detailed setup tables are absent from it.

### PRSR-AT-003 — Inline bypass

A supplied draft with inline output begins without config, receipt, setup contract, or
fixture execution.

### PRSR-AT-004 — Ready persistence route

Matching configuration and a `ready` receipt allow the normal RUN to write only the
confirmed deliverable without modifying setup state.

### PRSR-AT-005 — Non-ready routing

Missing receipt, changed digest, and failed required check resolve to `missing`, `stale`,
and `blocked`, routing to setup only for persistence.

### PRSR-AT-006 — Setup-bundle structure

The setup validator passes the RUN, REF, README, YAML, fixture, profile, state, mapping, and
safety contracts.

### PRSR-AT-007 — Isolated fixture

A copied package and separate workspace produce configuration, receipt, collision-safe
fictional outputs, and identical before/after package hashes.

### PRSR-AT-008 — Stable receipt semantics

Dates do not expire readiness; package or configuration identity changes produce `stale`.

### PRSR-AT-009 — Package closure

A copy of only `skills/pre-read-sharpener/` resolves every declared resource.

### PRSR-AT-010 — Safety boundary

No network, publication, notification, scheduling, approval creation, or external write
occurs in setup or normal execution.

### PRSR-AT-011 — Privacy and IP

Private-denylist scanning, human non-reversibility review, and deterministic IP inventory
regeneration cover all candidate paths with no unadjudicated finding.

### PRSR-AT-012 — Repository and diff validation

Focused and complete public suites, skill validation, strict governed-document audit,
GitHub Actions validation, security plan, and manifest diff check pass with only approved
paths changed.

## Traceability

| Requirement | Inventory | Implementation artifacts | Acceptance tests |
|---|---|---|---|
| PRSR-REQ-001 | INV-PRSR-001 through INV-PRSR-008 | SKILL, normal RUN, retained editorial assets | PRSR-AT-001 |
| PRSR-REQ-002 | INV-PRSR-002, INV-PRSR-018 | normal RUN, removal of combined RUN | PRSR-AT-002, PRSR-AT-006 |
| PRSR-REQ-003 | INV-PRSR-007 through INV-PRSR-009 | SKILL, setup contract | PRSR-AT-003, PRSR-AT-004 |
| PRSR-REQ-004 | INV-PRSR-009, INV-PRSR-016, INV-PRSR-017 | SKILL, cases, example index | PRSR-AT-003 through PRSR-AT-005 |
| PRSR-REQ-005 | INV-PRSR-010, INV-PRSR-011, INV-PRSR-013 | setup contract, README | PRSR-AT-006, PRSR-AT-009 |
| PRSR-REQ-006 | INV-PRSR-010, INV-PRSR-011, INV-PRSR-019 | setup configuration | PRSR-AT-006 through PRSR-AT-008 |
| PRSR-REQ-007 | INV-PRSR-012, INV-PRSR-020 | setup receipt | PRSR-AT-004, PRSR-AT-006 through PRSR-AT-008 |
| PRSR-REQ-008 | INV-PRSR-012, INV-PRSR-017 | receipt schema and behavior cases | PRSR-AT-005, PRSR-AT-008 |
| PRSR-REQ-009 | INV-PRSR-013 | README | PRSR-AT-006, PRSR-AT-009 |
| PRSR-REQ-010 | INV-PRSR-014 through INV-PRSR-017 | setup fixture and behavior cases | PRSR-AT-003 through PRSR-AT-007 |
| PRSR-REQ-011 | INV-PRSR-005, INV-PRSR-015, INV-PRSR-024, INV-PRSR-025 | fixtures, privacy review, scan | PRSR-AT-010, PRSR-AT-011 |
| PRSR-REQ-012 | INV-PRSR-021 through INV-PRSR-024 | tests, v1.2 docs, catalog, export, IP | PRSR-AT-012 |

## Assumptions, constraints, and safe degradation

- The package is a prompt-and-reference skill with no mandatory executable helper.
- Inline work remains available when persistent output is unconfigured or unwritable.
- A persistence failure returns the complete inline result and reports the failed write; it
  never silently chooses another location.
- A missing runtime capability in the isolated fixture is `unavailable`, not a pass.
- Real drafts may be confidential; adopters control local storage and sharing.

## Approval and release gates

1. Implementation starts only after project-owner approval of the exact review evidence.
2. Implementation remains within the approved public change manifest.
3. Required checks pass or are reported as not run with blocked readiness.
4. Candidate privacy and governed documents remain Draft through review.
5. Gate B approves the exact pull-request revision.
6. No merge or release occurs before that approval.
