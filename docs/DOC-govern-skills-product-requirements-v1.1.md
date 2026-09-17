---
doc_type: DOC
normative: false
requires:
  - DOC-govern-skills-source-inventory-v1.1.md
  - STD-evidence-privacy-v1.0.md
status: Draft
version: "1.1"
owner: alex-bea
consumers:
  - Public Toolkit Maintainers
  - Claude Code Users
  - Codex Users
change_control: Pull request review and project-owner approval
---

# Public Govern Skills Conditional Setup Product Requirements (v1.1)

## Purpose and authority

This Draft updates the standalone public `govern-skills` copy-pattern package so routine
governance work does not repeatedly load setup instructions. It defines a sole normal RUN,
a conditional setup contract, adopter-owned machine-readable configuration and receipt,
and an isolated fictional smoke test. It does not authorize merge, release, plugin
activation, or any external side effect.

The existing v1.0 document remains as design history. This document supersedes its combined
setup-and-execution RUN and Markdown-only readiness model. The optional public
`skill-governance` plugin remains unchanged and is not a dependency.

## Problem

The public package already supports safe documents-first adoption, but its sole RUN mixes a
detailed setup contract with normal audit, repair, creation, lifecycle, and enforcement
work. Every invocation therefore pays the setup-context cost even when a verified adopter
configuration has not changed. The package also uses a detailed Markdown evidence report
as its only receipt shape, which is less stable for deterministic readiness routing.

## Goals

1. Keep exactly one RUN and make it the normal governance workflow.
2. Route setup, installation, configuration, verification, diagnosis, and setup repair to
   one conditionally loaded setup contract.
3. Route a normal request with a matching `ready` receipt directly to the normal RUN without
   loading setup detail.
4. Represent `ready`, `missing`, `stale`, and `blocked` explicitly.
5. Store completed configuration and readiness at stable adopter-owned paths outside the
   installed package.
6. Preserve the detailed Markdown receipt as optional human-readable evidence while making
   YAML the canonical readiness record.
7. Prove package closure and safe setup with independently fictional Acorn Studio fixtures.
8. Preserve the public plugin and all eight mirrored governance standards byte for byte.

## Non-goals

- Adding an installer, plugin, network connector, secret, service, scheduler, notifier, or
  publisher.
- Requiring CI, hooks, a registry, capability restrictions, or external approval services
  for documents-only readiness.
- Selecting a real repository owner, production path, retention policy, or enforcement
  layer on an adopter's behalf.
- Treating a date, static test, readable rule, or caller assertion as live authorization.
- Changing the optional plugin or the content of canonical and mirrored standards.

## Requirements

### GCS-REQ-001 — Conditional routing

`SKILL.md` must route explicit setup and missing, stale, or blocked readiness to the setup
contract. It must route a ready normal request to the sole normal RUN and say not to load
the setup contract on that path.

### GCS-REQ-002 — One normal RUN

The package must contain exactly one `RUN-*.md`, named
`references/RUN-govern-skills-workflow-v1.1.md`. It must cover audit, repair, create/update,
lifecycle, enforcement, exact write boundaries, verification, and error handling without
duplicating detailed setup mapping tables.

### GCS-REQ-003 — One complete setup contract

`references/REF-govern-skills-setup-contract.md` must declare the `local-persistence`
profile and specify readiness routing, installation checks, source mapping, output
destinations, configuration and state, permissions and secrets, a safe test, the receipt,
and repair. It must explicitly disable publishing, notifications, scheduling, and
production mutation during setup testing.

### GCS-REQ-004 — Stable adopter-owned state

The default completed paths are `.agents/govern-skills/setup-config.yaml` and
`.agents/govern-skills/setup-receipt.yaml` under the authorized adopter workspace. A
compatible canonical adopter convention may replace those paths. Completed state never
lives inside the installed package.

### GCS-REQ-005 — Machine-readable configuration

The blank setup configuration must identify the schema, skill, setup profile, installed
package, selected scope, sources, destinations, configuration path, receipt path, owner,
and real change-control mechanism without embedding a live adopter default.

### GCS-REQ-006 — Machine-readable receipt

The blank receipt must identify status, installation and verification times, package
revision and digest, setup-contract version, configuration path and digest, checks,
limitations, scope, and normal entrypoint. The receipt contains no credential values or
sensitive source locators.

### GCS-REQ-007 — Staleness semantics

A receipt becomes stale when its package revision or digest, setup-contract version,
required mapping, dependency set, selected enforcement layer, or configuration digest
changes. Dates are evidence only; there is no time-to-live.

### GCS-REQ-008 — Safe fictional test

The package must include complete fictional setup configuration, readiness receipt, and a
repeatable smoke-test procedure. The test copies the package to a new temporary directory,
creates only declared fictional artifacts, confirms package immutability, and performs no
network call or external or production mutation.

### GCS-REQ-009 — Backward-readable evidence

`assets/output-template.md` and the existing fictional Markdown receipt remain the detailed
human-readable evidence format. They do not substitute for the YAML readiness record.

### GCS-REQ-010 — Package and plugin compatibility

The adoption guide, example index, focused tests, package validator, catalog, export
manifest, governed documents, and legal inventory must describe the same split contract.
The public plugin and eight standard mirrors must remain unchanged.

### GCS-REQ-011 — Exact approval boundary

Implementation must begin only after exact-digest Gate A approval, change only the approved
manifest paths, open one pull request, pass local and hosted checks, and stop for Gate B on
the exact candidate revision. Gate B never authorizes merge.

## Readiness model

| Status | Required interpretation |
|---|---|
| `ready` | Every required check passes for the exact named repository, configuration, package, and scope. |
| `missing` | No current machine-readable receipt is available. |
| `stale` | A receipt exists but one or more bound inputs changed. |
| `blocked` | A required source, destination, permission, decision, or test failed or cannot run. |

Documents-only setup can be ready without optional validation or enforcement layers. Every
observed control remains classified as `instruction-only`, `static-validator`,
`runtime-guard`, `capability-boundary`, or `external-authority`.

## Acceptance tests

| ID | Test | Expected result |
|---|---|---|
| GCS-AT-001 | Inspect `references/RUN-*.md`. | Exactly one normal RUN exists; no setup mapping table appears in it. |
| GCS-AT-002 | Run the setup-contract validator. | Required headings, mapping headers, profile, routing states, safety terms, YAML assets, and fixture links pass. |
| GCS-AT-003 | Simulate ready normal work. | Routing names the normal RUN and says not to load setup detail. |
| GCS-AT-004 | Simulate explicit setup and missing, stale, and blocked receipts. | Every case routes to the setup contract. |
| GCS-AT-005 | Parse blank setup assets structurally. | Every required top-level field exists and contains no live adopter default. |
| GCS-AT-006 | Run the fictional smoke test in a temporary workspace. | Declared artifacts exist outside the copied package; the package digest is unchanged. |
| GCS-AT-007 | Inspect the fictional YAML receipt. | It is ready only for documents-only scope and points to the normal RUN. |
| GCS-AT-008 | Compare the plugin and eight standard mirrors with the base revision. | Every byte is unchanged. |
| GCS-AT-009 | Run public validation, unit, document, privacy, provenance, and manifest checks. | All applicable checks pass or a limitation is recorded without being called a pass. |
| GCS-AT-010 | Inspect pull-request state. | The diff is limited to approved paths, Gate B binds to the exact revision, and the PR remains unmerged. |

## Assumptions and constraints

- The default profile is `local-persistence` because readiness must survive between normal
  invocations but no external integration is required.
- The package is model-neutral; local agents are examples, not runtime dependencies.
- YAML assets are declarative contracts and no YAML library is required at runtime.
- A repository may use a compatible canonical state location instead of the suggested
  `.agents/` paths, but the receipt must bind to that exact configuration.
- A model-readable conditional route is `instruction-only`; deterministic tests prove the
  text and file behavior, not which reference a model actually loaded.

## Approval and release gates

The owner approved Gate A for review-package digest
`sha256:a89b73485f12abf208521aec14713e003904fea2febc5a97d3b4ee8982990002`
and only its manifest paths. Any additional path requires a new review digest and approval.
The candidate remains Draft and unmerged until hosted checks complete and the owner reviews
the exact pull-request revision at Gate B.
