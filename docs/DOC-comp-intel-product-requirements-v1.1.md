---
doc_type: DOC
normative: false
requires:
  - DOC-comp-intel-source-inventory-v1.1.md
  - STD-approval-gates-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-skill-dependencies-v1.0.md
  - STD-skill-structure-v1.0.md
status: Draft
version: "1.1"
owner: alex-bea
consumers:
  - comp-intel maintainers
  - public adopters
  - security reviewers
change_control: Pull request review and project-owner approval
---

# Competitive Intelligence Conditional Setup Product Requirements (v1.1)

## 1. Purpose and authority

This Draft defines the current public candidate for separating `comp-intel` setup from normal
execution. It preserves the shipped analyst framework and corrects its two-RUN setup shape.
The installed package remains the runtime source of truth. Earlier comp-intel requirements and
the archived Codex suite remain design history.

This document does not authorize live source access, private migration, publication, merge, or
release. The candidate requires pull-request review and exact-revision project-owner approval.

## 2. Problem

The shipped skill has one onboarding RUN and one recurring RUN. That makes normal routing
ambiguous and causes setup detail to compete with execution. The package also lacks a stable
machine-readable setup configuration and readiness receipt, so it cannot distinguish a ready
installation from missing, stale, or blocked state without re-running onboarding.

The correction must retain the existing evidence discipline, two human review gates, fictional
example, controller behavior, schemas, adopter-owned mutable state, and no-publication boundary.

## 3. Users and jobs

| User | Job |
|---|---|
| Competitive analyst | Run a bounded, attributable market scan from approved sources. |
| PMM | Review evidence, implications, gaps, and proposed registry or tracker changes. |
| Installer | Map a market, sources, permissions, reviewers, data root, and destinations safely. |
| Recurring operator | Enter normal execution directly when setup identity remains current. |
| Maintainer | Diagnose and repair setup without editing installed package files. |
| Security reviewer | Prove source authorization, state separation, privacy, and side-effect boundaries. |

## 4. Product decisions

- The setup profile is `configured-sources`.
- `references/RUN-workflow.md` is the sole normal-execution RUN.
- `references/REF-comp-intel-setup-contract.md` owns installation, mapping, verification,
  fixture, receipt, diagnosis, and repair.
- A matching `ready` receipt routes directly to the normal RUN without loading setup detail.
- `missing`, `stale`, and `blocked` route to setup and prevent live collection.
- The bundled fictional smoke test is the only route that does not require organizational setup.
- Setup configuration, receipt, evidence, approvals, registries, trackers, and reports remain
  adopter-owned and outside the installed package.

## 5. Requirements

### CISR-REQ-001 — Preserve analyst fidelity

Preserve scoped configuration, bounded collection, coverage, normalization, duplicates,
conflicts, evidence review, evidence-bound synthesis, claim traceability, draft review, proposed
state changes, local apply, reporting, resume, limitations, and safe degradation.

### CISR-REQ-002 — One normal RUN

Exactly one active `RUN-*.md` exists: `references/RUN-workflow.md`. It contains normal execution
and only a short readiness preflight. Detailed setup tables and repair procedures remain outside
the RUN.

### CISR-REQ-003 — Configured-source readiness

A live run requires a selected market, reviewed source map, approved adopter positioning,
competitor registry, authorized required sources, reviewer policy, adopter-owned data root, and
safe local destinations. Missing optional sources degrade visibly; missing required sources
block.

### CISR-REQ-004 — Conditional routing

`SKILL.md` routes `ready` normal work to the sole RUN and says not to load detailed setup.
Explicit setup-family requests and `missing`, `stale`, or `blocked` state route to the setup
contract. Conversation alone is not a readiness record.

### CISR-REQ-005 — Setup contract

The separate setup REF defines profile, readiness, installation checks, source mapping, output
destinations, configuration and state, permissions and secrets, safe test, receipt, and repair.
It is not a second executable runbook.

### CISR-REQ-006 — Setup configuration

The blank YAML asset defines package identity, source mappings, destinations, reviewer roles,
data root, receipt path, and revision without live locators, identities, or credentials.

### CISR-REQ-007 — Setup receipt

The blank YAML receipt defines status, package and configuration identity, setup-contract
version, checks, limitations, created files, normal entrypoint, and repair action. Completed
state lives at the configured external path.

### CISR-REQ-008 — Readiness semantics

`ready` requires matching identity and passing required checks. Absent state is `missing`;
identity drift is `stale`; a failed required check is `blocked`. Timestamps are audit metadata
and do not expire setup automatically.

### CISR-REQ-009 — Operator guidance

The README explains installation, setup paths, routing, safe test, diagnosis, repair, normal
execution, optional controller support, and the boundary between local apply and publication.

### CISR-REQ-010 — Isolated fictional test

Completed fictional setup configuration and receipt fixtures plus a smoke test exercise package
closure, controller initialization, capability checks, collection through `evidence_review`, all
four routing states, local destinations, package immutability, and disabled external effects.

### CISR-REQ-011 — Privacy and external safety

No private entity, locator, person profile, customer, deal, claim, quote, metric, path,
credential, or populated mapping enters the package. Imported content remains untrusted. Setup
never grants publication, messaging, notification, scheduling, approval creation, or external
mutation.

### CISR-REQ-012 — Compatibility and release governance

Preserve invocation language, output structures, fictional analyst example, controller CLI,
schemas, and approval semantics. Update governed inventory, catalog, export manifest, tests,
privacy review, and deterministic IP inventory. Use one focused pull request and stop before
merge for exact-revision approval.

## 6. Package contract

```text
skills/comp-intel/
├── SKILL.md
├── README.md
├── references/
│   ├── RUN-workflow.md
│   ├── REF-comp-intel-setup-contract.md
│   └── existing analyst, evidence, review, and troubleshooting references
├── assets/
│   ├── setup-config.yaml
│   ├── setup-receipt.yaml
│   └── existing market, evidence, registry, tracker, output, and schema assets
└── examples/
    ├── EX-synthetic.md
    ├── fictional-embedded-wallets/
    └── fixtures/
        ├── setup-config.yaml
        ├── setup-receipt.yaml
        └── setup-smoke-test.md
```

## 7. Routing matrix

| Condition | State | Route | Live collection |
|---|---|---|---|
| Explicit setup, configure, verify, diagnose, or repair request | any | Setup contract | Only after ready |
| Receipt or required mapping absent | missing | Setup contract | blocked |
| Package, contract, or configuration identity changed | stale | Setup repair | blocked |
| Required capability, permission, path, destination, reviewer, or validation failed | blocked | Setup repair | blocked |
| Matching receipt and all required checks pass | ready | Sole normal RUN; do not load setup detail | allowed |
| Explicit bundled fictional smoke test | isolated test | Setup contract and fixture | no organizational access |

## 8. Data and safety

- Installed files are immutable reusable package content.
- Completed setup and operational state stay outside the package.
- Each source records purpose, kind, locator, authorization method, data class, requirement, and
  a read-only check.
- Each destination records artifact, location, write mode, visibility, retention, external
  approval, requirement, and a non-destructive write check.
- Secrets stay in the adopter's credential mechanism; configuration records only the mechanism
  and scope.
- Local evidence approval and local apply approval never authorize an external action.
- Scheduled workers may collect staging evidence but may not approve, apply, or publish.

## 9. Migration

Existing controller data roots and market files remain in place. The setup configuration points
to them; it does not import or rewrite them. An existing installation without a receipt becomes
`missing`, not corrupt. After verification, setup may create a receipt with local-write
authorization. Identity drift becomes `stale`; failed required checks become `blocked`.

Removal of the old onboarding RUN and setup document is atomic with the router, README, tests,
and new setup contract. Controller commands and schemas remain compatible.

## 10. Acceptance tests

| ID | Requirements | Pass condition |
|---|---|---|
| CISR-AT-001 | CISR-REQ-001 | Current analyst stages, gates, templates, examples, and controller behaviors remain. |
| CISR-AT-002 | CISR-REQ-002, CISR-REQ-005 | Exactly one normal RUN and one setup REF exist; detailed mappings occur only in the REF. |
| CISR-AT-003 | CISR-REQ-004, CISR-REQ-008 | A matching ready receipt bypasses detailed setup. |
| CISR-AT-004 | CISR-REQ-004, CISR-REQ-008 | Missing, stale, and blocked states stop live execution and route to repair. |
| CISR-AT-005 | CISR-REQ-003, CISR-REQ-006 | Required mappings, permissions, reviewers, data root, and destinations validate without live defaults. |
| CISR-AT-006 | CISR-REQ-007, CISR-REQ-008 | Receipt identity, checks, limitations, entrypoint, repair, and timestamp semantics validate. |
| CISR-AT-007 | CISR-REQ-010 | The copied package and separate temporary workspace complete the fictional test through evidence review. |
| CISR-AT-008 | CISR-REQ-010, CISR-REQ-011 | The package remains unchanged and no external or production side effect occurs. |
| CISR-AT-009 | CISR-REQ-009, CISR-REQ-012 | Direct-install links and declared resources resolve. |
| CISR-AT-010 | CISR-REQ-001, CISR-REQ-012 | Focused tests, full tests, package validation, document audit, links, and diff checks pass. |
| CISR-AT-011 | CISR-REQ-011 | Private-term, secret, path, live-domain, semantic, and IP checks have no unadjudicated finding. |
| CISR-AT-012 | CISR-REQ-012 | Changed paths equal the approved manifest; hosted checks and exact-revision review precede merge. |

## 11. Limitations

Static tests can verify instructions, file structure, mappings, and fixture behavior, but cannot
prove which references every AI runtime loaded. Conditional routing is instruction-only unless
an adopter installs an independent dispatcher or runtime guard. The package does not include
live web, Slack, Drive, repository-host, CRM, publisher, scheduler, notification, or external
approval adapters.

## 12. Approval and release

The candidate remains Draft until pull-request review and project-owner approval of the exact
revision. Approval covers local package content only. It does not approve live source collection,
private migration, external publication, messaging, scheduling, marketplace submission, or an
external release.
