---
doc_type: DOC
normative: false
requires:
  - DOC-pre-read-sharpener-source-inventory-v1.1.md
  - STD-approval-gates-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-skill-dependencies-v1.0.md
  - STD-skill-structure-v1.0.md
status: Draft
version: "1.1"
owner: alex-bea
consumers:
  - pre-read-sharpener maintainers
  - Claude Code users
  - Codex users
change_control: Pull request review and project-owner approval
---

# Public Pre-Read Sharpener Product Requirements (v1.1)

## Document purpose and authority

This Draft defines the faithful, generic, setup-ready, and directly installable public
`skills/pre-read-sharpener` package. It consolidates the merged v1.0 editorial requirements
with the v1.1 first-run setup contract. The companion source inventory is advisory evidence.
The installed skill's sole setup-and-execution RUN, templates, references, and fixtures
implement these requirements but may not narrow or contradict them.

The private implementation informed public editorial structure and depth but is not a public
runtime dependency. The setup framework was adapted to this skill's actual local inputs and
outputs. Private content, real pre-reads, populated mappings, receipts, registry state, and
history are not distributed.

## Problem

The v1.0 public package faithfully performs the editorial job, but its only RUN begins at
draft intake. A first-time adopter cannot verify package closure, map how drafts enter the
workflow, confirm writable local destinations, store configuration and readiness evidence
outside the package, or run a bounded fictional test before using a potentially confidential
draft.

Without a setup mapping and receipt, an installation can appear usable while containing a
broken link, unsafe output location, unavailable agent runtime, or stale configuration. The
package needs a setup-first entrypoint without changing its proven review-and-rewrite method
or adding an external integration.

## Users and jobs

| User | Job |
|---|---|
| Product or marketing leader | Tighten an existing executive pre-read around one decision without adding facts. |
| Executive reader | Find the decision, recommendation, tradeoffs, reversal cost, and concrete outcome in under two minutes. |
| First-time adopter | Verify a copied package, map local sources and destinations, and run a safe fictional test before using a real draft. |
| Recurring user | Rely on a current setup receipt and know when package or configuration changes require revalidation. |
| Maintainer | Preserve editorial fidelity, setup closure, privacy, deterministic structure, and governed traceability through later changes. |

## Golden implementation and public evolution

The golden editorial implementation contains one seven-step workflow, one exact user-facing
rewrite template, four decision anchors, ten binary criteria, a maximum of three repair
rounds, deterministic file naming, same-file edit handling, and actionable errors. The
merged v1.0 public package preserves that behavior and includes a complete independently
fictional source/output pair.

Version 1.1 adds one sole setup-and-execution RUN with ten setup sections, blank source and
destination mapping, adopter-owned configuration and receipts, permission checks, an
isolated fictional smoke test, readiness states, staleness rules, and repair behavior. The
complete v1.0 execution method moves under Normal execution without changing its output
contract.

No qualifying real private artifact completed the canonical output template, and no real
pre-read setup receipt was found. Public examples therefore demonstrate written contracts
with independently fictional evidence and do not claim historical production use of every
field.

## Goals

- Preserve the complete ordered review-and-rewrite workflow and exact output template.
- Preserve the four anchors, ten binary criteria, bounded repair loop, source-only evidence,
  and no-research scope.
- Preserve local persistence, deterministic naming, collision suffixing, and same-file edits.
- Make the sole RUN a setup and execution wizard with package, runtime, mapping, permission,
  test, receipt, repair, and normal-operation guidance.
- Keep configuration, receipts, drafts, tests, and generated outputs in adopter-owned or
  temporary workspace paths outside the installed package.
- Provide blank reusable setup assets and one complete fictional setup fixture and receipt.
- Verify package closure and safe local operation before a real draft is processed.
- Keep the skill agent-neutral and usable by Claude Code, Codex, and compatible local agents.
- Maintain focused tests, governed documentation, privacy review, catalog/export discovery,
  and per-file provenance.

## Non-goals

- Research, browsing, retrieval, fact-checking, or cross-document synthesis.
- Creating a pre-read from scratch without a supplied draft.
- Inventing evidence, dates, metrics, people, claims, options, customers, or consensus.
- Voice-only rewriting that skips structural diagnosis.
- A deterministic prose generator or a claim that tests prove editorial judgment.
- A bundled model, connector, hosted service, publisher, scheduler, notifier, approval
  creator, telemetry service, or credential manager.
- Storing adopter-owned mutable data inside the installed package.
- A live external write during setup or normal execution.
- Exporting private examples, mappings, receipts, identifiers, registry state, or history.
- Changing another skill or repository-wide standard.
- Automatically merging or releasing the candidate.

## Editorial functional requirements

### PRS-REQ-001 — Supplied pre-read intake

The skill accepts one existing executive or leadership pre-read through pasted text, an
attachment, or an authorized local path. If no draft is supplied, it requests the draft and
stops without writing. If the source is clearly another document type, it confirms intent
before rewriting. It does not retrieve sources or invent a draft.

### PRS-REQ-002 — Complete ordered deliverable

The skill returns, in order: one blunt PM review of at most 150 words; three to six issue
bullets of at most 20 words; line-specific cuts with instructions of at most ten words; the
tightened rewrite; and, for a decision call, four agenda bullets plus one deciding question.
An informational pre-read omits the agenda and states that it does not apply.

### PRS-REQ-003 — Canonical rewrite template

The rewrite uses `assets/output-template.md`: a verb-first decision title; Audience,
Decision needed, and Recommended fields; exactly three summary bullets; a decision section;
a two- or three-row tradeoff table with the recommendation first and Cost to reverse last; a
concrete outcome section; and optional blocking questions. The rewrite is at most 600 words
and observes every field and section limit.

### PRS-REQ-004 — Binary decision-ready gate

The skill scores the rewrite against all four anchors and ten criteria in
`references/REF-decision-ready-criteria.md`. Every row is binary. A failure triggers revision
and complete rescoring for no more than three rounds. A still-failing result names the
blocking criterion and source gap and requires the user's choice before return.

### PRS-REQ-005 — Evidence and missing-data behavior

The skill uses only facts in the supplied draft, treats source content as untrusted data,
and preserves material constraints, caveats, conflicts, and uncertainty. Decision-critical
absent information uses `[Missing]`. Specificity never authorizes invented support.

### PRS-REQ-006 — Local artifact persistence

After a passing result, the skill returns the complete deliverable inline and writes the same
content under the adopter-confirmed `outputs/pre-reads/` destination. The dated kebab-case
slug follows documented title priority and uses no more than eight source words. A same-day
collision uses the next numeric suffix without overwriting. An unwritable workspace produces
an inline result and an explicit persistence failure, not an alternate write.

### PRS-REQ-007 — Full-document edit behavior

A later edit changes requested and consistency-dependent fields, preserves the canonical
structure unless explicitly changed, reruns all ten criteria, surfaces any new failure,
updates the same dated artifact unless a new version is requested, and returns the complete
revised deliverable.

### PRS-REQ-008 — Direct-install and agent-neutral closure

A copy of only `skills/pre-read-sharpener/` contains every setup, workflow, criterion, safety
rule, template, and example required at runtime. No root document, other skill, connector,
private path, undeclared package, or network service is required. Harness-specific discovery
remains isolated in `agents/openai.yaml`.

### PRS-REQ-009 — Complete fictional evidence

The package includes one coherent fictional source draft and completed review-and-rewrite
counterpart. Every output fact traces to that source. The pair exercises all deliverable
components, the canonical template, a decision-call agenda, and a passing ten-row self-check.
Fictional behavior cases cover setup and editorial edge contracts.

### PRS-REQ-010 — Public discovery and governed documentation

The skill retains its name, folder, primary invocation, and valid discovery metadata. The
starter guide, public catalog, export manifest, Draft requirements, Draft source inventory,
and candidate privacy review describe the setup-ready package accurately.

### PRS-REQ-011 — Privacy and provenance

The candidate contains no private entity, person, internal product term, identifier, URL,
metric, quote, claim, source phrase, path, populated mapping, real receipt, or
private-to-fictional alias. Automated scanning and human non-reversibility review supplement
the Draft candidate IP/privacy review and regenerated complete IP inventory.

### PRS-REQ-012 — Approval and release boundary

Implementation starts only from an exact-digest owner-approved review package and current
public `main`, remains inside the approved path manifest, runs or honestly labels every
applicable check, opens one focused pull request, and stops before merge or release for
project-owner review.

## Setup functional requirements

### PRSW-REQ-001 — Sole setup-and-execution RUN

The package contains exactly one `references/RUN-*.md` file named
`RUN-pre-read-sharpener-setup-workflow.md`. It contains the ten required setup headings and
the complete editorial workflow under `## 10. Normal execution`. `SKILL.md` routes install,
configure, verify, diagnose, first-use, and normal requests to it.

### PRSW-REQ-002 — Installation and dependency checks

The wizard resolves every required package file and link relative to the installed skill,
checks compatible-agent availability and required local access, and blocks readiness on a
missing file, broken link, unavailable required runtime, or unsafe path. It never repairs a
public installation by referencing a private repository.

### PRSW-REQ-003 — Source mapping

The blank mapping uses the exact Source ID, Purpose, Kind, Locator, Authorization method,
Data class, Required, and Read check fields. Normal setup maps one supplied draft as paste,
attachment, or authorized file. The smoke test maps only the bundled fictional draft. No
external source or undeclared fallback exists.

### PRSW-REQ-004 — Output destinations

The blank mapping uses the exact Destination ID, Artifact, Location, Write mode, Visibility,
Retention, External approval, Required, and Write check fields. The adopter confirms local
deliverable, configuration, receipt, and test paths outside the package. Missing, ambiguous,
unwritable, colliding, or unsafe required destinations block setup. External publication is
unconfigured and forbidden.

### PRSW-REQ-005 — Configuration and state

The completed mapping records package identity, source and destination IDs, timezone,
retention, permission mechanisms, test fixture and destination, and receipt location at an
adopter-owned workspace path. The mapping, receipt, and generated pre-reads are the only
mutable state. No cache, schedule, or background process is required.

### PRSW-REQ-006 — Permissions, secrets, and approvals

Setup verifies package and source read access plus required local destination write access.
It names mechanisms but stores no credential values. Source permission never grants
publishing, messaging, notification, scheduling, approval creation, network mutation, or a
different destination.

### PRSW-REQ-007 — Safe fictional test run

`examples/fixtures/setup-smoke-test.md` supplies a complete fictional mapping, isolated
destination, expected artifacts, invariants, and completed fictional receipt. The test uses
only bundled synthetic input, writes only to a temporary workspace, exercises the full
transformation and collision behavior, suppresses external and production writes, and
records passed, failed, skipped, and unavailable checks separately.

### PRSW-REQ-008 — Setup receipt and staleness

The receipt records package and configuration identity, mapping readiness, dependency and
permission results, fixture method, expected and actual artifacts, validation outcomes,
skipped checks, files created, residual limitations, overall status, and normal entrypoint or
repair action. States are `ready`, `ready-with-optional-limitations`, and `blocked`. A receipt
is stale after a package revision, required mapping, dependency set, or configuration digest
change.

### PRSW-REQ-009 — Normal workflow preservation

Setup may gate first use but does not change intake, diagnosis, ordered output, agenda,
self-check, repair, persistence, collision, return, edit, or error behavior. The output
template, criteria, fictional editorial pair, and evidence/privacy reference remain unchanged.

### PRSW-REQ-010 — Discovery and versioned documentation

Discovery metadata remains unchanged. README, catalog, and export records describe setup.
The v1.0 requirements and inventory remain Superseded history and link to full v1.1
replacements. All package and governed-document links resolve.

### PRSW-REQ-011 — Synthetic setup evidence and privacy

Blank assets contain placeholders rather than authoring defaults. The setup fixture is
visibly fictional, uses only bundled synthetic input and temporary paths, and contains no
private mapping, receipt, identifier, secret, or reversible alias. Candidate scanning,
human review, setup-amendment privacy review, and IP regeneration cover the exact revision.

### PRSW-REQ-012 — Candidate and release gate

The setup amendment starts from the approved digest and current public base, changes only the
approved paths, passes or honestly labels all checks, and stops at a new unmerged pull
request. Setup readiness does not grant merge, release, or external publication authority.

## Content and package requirements

The directly installable package contains concise trigger metadata; unchanged discovery
metadata, output template, criteria, privacy reference, and fictional editorial pair; one
sole setup-and-execution RUN; blank mapping and receipt assets; a complete fictional setup
fixture; a starter guide; an example index; and setup plus editorial behavior cases.

The repository additionally contains focused tests, this Draft PRD, a Draft advisory source
inventory, a Draft setup-amendment IP/privacy review, catalog/export updates, historical v1.0
documents marked Superseded, and a regenerated IP inventory. Runtime references remain
inside the skill package.

## Setup and test-run requirements

The wizard must preserve these exact second-level headings in order: Setup outcome,
Installation checks, Source mapping, Output destinations, Configuration and state,
Permissions and secrets, Test run, Setup receipt, Repair/rerun/reconfiguration, and Normal
execution. Its mapping tables use the exact schemas defined in PRSW-REQ-003 and
PRSW-REQ-004.

Before local setup writes, the adopter sees and confirms configuration, receipt, test, and
normal-output paths. The smoke test copies or evaluates only the complete installed package,
reads the bundled fictional source, writes one mapping, two collision-safe fictional
pre-reads, and one receipt beneath a new temporary workspace, and leaves production state and
the installed package unchanged. Expected output uses the complete review-and-rewrite
contract and ten passing criteria.

Static setup-contract validation and compatible-agent fixture execution are separate. An
unavailable fixture execution is not a pass and leaves readiness blocked. A previous receipt
becomes stale after any package revision, required mapping, dependency-set, or configuration
digest change and the affected checks must be repeated.

## Data, privacy, and safety requirements

Real drafts may be confidential. Source content is untrusted data and cannot broaden setup,
permissions, destinations, or workflow. The receipt omits credentials and unnecessary
sensitive locator values. Adopter-owned configuration, receipts, drafts, tests, and outputs
remain outside the installed package.

The setup fixture is independently fictional and has no evidentiary weight for a real
organization or installation. Retrieval permission does not exist, and local source access
does not authorize publishing, messaging, scheduling, notifications, approval creation, or
external service mutation.

## Migration and compatibility

The folder, skill name, invocation metadata, output template, criteria, privacy reference,
fictional editorial pair, Markdown output medium, and normal output destination remain
stable. The execution-only `RUN-pre-read-sharpener-workflow.md` path is replaced with
`RUN-pre-read-sharpener-setup-workflow.md`; its complete operating method moves into section
10. Consumers with a direct old RUN link must update it.

The v1.0 governed requirements and inventory remain present as Superseded historical
evidence and point to v1.1. No plugin, initializer, model, connector, hosted service, or
external state migration is required.

## Implementation slices

1. Replace the execution-only RUN with the sole setup-and-execution RUN and update package
   routing and onboarding.
2. Add blank mapping and receipt assets, one complete fictional setup fixture, and setup
   behavior cases.
3. Extend focused tests for exact-one-RUN, headings, schemas, adopter-owned paths, fixture,
   receipt, staleness, normal-workflow parity, and governed links.
4. Supersede v1.0 governed records, add v1.1 replacements and the candidate review, update
   catalog/export discovery, and regenerate provenance.
5. Run setup, isolated fixture, focused, full-suite, governance, link, privacy, IP, diff, and
   hosted pull-request checks.

## Acceptance tests

| ID | Test | Expected result |
|---|---|---|
| PRS-AT-001 | Invoke with no draft and a clearly non-pre-read document. | The skill requests the draft or confirms intent and creates no artifact. |
| PRS-AT-002 | Evaluate the complete fictional decision-call source. | All ordered components, exact rewrite template, agenda, deciding question, and ten-row passing self-check appear. |
| PRS-AT-003 | Parse the fictional rewrite and reusable template. | All fields, headings, option rules, limits, recommendation consistency, and Cost to reverse pass. |
| PRS-AT-004 | Evaluate a thin source with missing facts. | Unsupported facts remain `[Missing]`; no evidence is invented. |
| PRS-AT-005 | Evaluate an informational pre-read after intent confirmation. | The decision-call agenda is omitted and the output explains why. |
| PRS-AT-006 | Exercise a quality failure through three repair rounds. | The blocker is named and the user is asked before a failing result returns. |
| PRS-AT-007 | Exercise first save, collision save, and later edit. | The slug, suffix, and same-file edit behavior pass after complete rescoring. |
| PRS-AT-008 | Copy only the skill directory and resolve routed paths. | The package works without repository-root or private dependencies. |
| PRS-AT-009 | Trace fictional output to source and run privacy scans. | Every fact resolves and no private or unfinished content appears. |
| PRS-AT-010 | Run focused, full-suite, package, document, link, and IP checks. | Every available required check passes; unavailable checks remain explicit. |
| PRS-AT-011 | Compare candidate diff with the approved manifest. | Only approved paths change. |
| PRS-AT-012 | Verify approval and pull-request state. | Exact-digest approval precedes implementation and the pull request remains unmerged. |
| PRSW-AT-001 | Count RUN files and inspect routing. | Exactly one setup-workflow RUN exists and `SKILL.md` routes setup and execution to it. |
| PRSW-AT-002 | Resolve required files from an isolated copy. | All package-local resources resolve without the private repository. |
| PRSW-AT-003 | Parse blank and fictional source mappings. | The exact schema, supplied-draft contract, and synthetic fixture source pass. |
| PRSW-AT-004 | Parse destinations and probe temporary paths. | Required paths are outside the package; unsafe or unwritable paths block readiness. |
| PRSW-AT-005 | Inspect configuration, permission, and secret handling. | Used fields are mapped and no secret or external authority is stored. |
| PRSW-AT-006 | Run the setup-contract validator. | Sole RUN, headings, tables, fixture, receipt states, and safety terms pass. |
| PRSW-AT-007 | Execute the fictional fixture in a temporary workspace. | Mapping, two collision-safe pre-reads, and receipt are created without production or external writes. |
| PRSW-AT-008 | Change package or configuration digest. | The prior receipt becomes stale and affected checks rerun. |
| PRSW-AT-009 | Re-evaluate existing editorial cases and retained artifacts. | Normal behavior and unchanged artifacts remain faithful. |
| PRSW-AT-010 | Run complete repository validation. | Every available required check passes; unavailable checks remain explicit. |
| PRSW-AT-011 | Run denylist scan and human review. | No private path, mapping, receipt, secret, alias, or reversible narrative appears. |
| PRSW-AT-012 | Compare diff and pull-request state with the approval. | Only approved paths change and the follow-up pull request remains unmerged. |

## Traceability

| Requirement | Public artifacts | Acceptance tests |
|---|---|---|
| PRS-REQ-001 | `SKILL.md`, setup RUN, behavior cases | PRS-AT-001, PRS-AT-002 |
| PRS-REQ-002 | Setup RUN, completed fictional output | PRS-AT-002 |
| PRS-REQ-003 | Output template, setup RUN, completed fictional output | PRS-AT-002, PRS-AT-003 |
| PRS-REQ-004 | Criteria, setup RUN, behavior cases | PRS-AT-002, PRS-AT-006, PRS-AT-010 |
| PRS-REQ-005 | Template, setup RUN, privacy reference, behavior cases | PRS-AT-003, PRS-AT-004, PRS-AT-009 |
| PRS-REQ-006 | `SKILL.md`, README, setup RUN, mapping | PRS-AT-007, PRS-AT-008 |
| PRS-REQ-007 | Setup RUN, behavior cases, focused test | PRS-AT-007, PRS-AT-010 |
| PRS-REQ-008 | Package-local resources and isolated copy | PRS-AT-008, PRS-AT-010 |
| PRS-REQ-009 | Example index, fictional pair, fixtures | PRS-AT-002 through PRS-AT-009 |
| PRS-REQ-010 | README, metadata, catalog, export, governed docs | PRS-AT-008, PRS-AT-010, PRS-AT-011 |
| PRS-REQ-011 | Fictional evidence, source inventory, candidate review, IP inventory | PRS-AT-009 through PRS-AT-011 |
| PRS-REQ-012 | Approval record, manifest, verification, pull request | PRS-AT-010 through PRS-AT-012 |
| PRSW-REQ-001 | `SKILL.md`, sole setup RUN | PRSW-AT-001, PRSW-AT-006 |
| PRSW-REQ-002 | Setup RUN, README, complete package | PRSW-AT-002, PRSW-AT-006 |
| PRSW-REQ-003 | Mapping asset, setup RUN, fixture | PRSW-AT-003, PRSW-AT-007 |
| PRSW-REQ-004 | Mapping asset, setup RUN, fixture | PRSW-AT-004, PRSW-AT-007 |
| PRSW-REQ-005 | Mapping and receipt assets, setup RUN | PRSW-AT-004, PRSW-AT-005, PRSW-AT-008 |
| PRSW-REQ-006 | Setup RUN, mapping asset, privacy reference | PRSW-AT-005, PRSW-AT-007 |
| PRSW-REQ-007 | Setup fixture, fictional pair, setup RUN | PRSW-AT-006, PRSW-AT-007 |
| PRSW-REQ-008 | Receipt asset, setup fixture, behavior cases | PRSW-AT-007, PRSW-AT-008 |
| PRSW-REQ-009 | Setup RUN and unchanged editorial artifacts | PRSW-AT-009, PRSW-AT-010 |
| PRSW-REQ-010 | README, v1.1 docs, catalog, export | PRSW-AT-002, PRSW-AT-010 |
| PRSW-REQ-011 | Fixture, candidate review, IP inventory | PRSW-AT-011, PRSW-AT-012 |
| PRSW-REQ-012 | Review package, governed docs, tests, pull request | PRSW-AT-010 through PRSW-AT-012 |

## Assumptions, constraints, and safe degradation

- The skill requires a compatible local agent and local file access but no fixed model,
  Python dependency, network service, connector, secret, scheduler, or publisher.
- A pasted draft may have no persistent source path; setup still records literal input mode
  and its authorization method.
- Static tests prove structure, links, deterministic limits, and traceability but cannot
  prove editorial quality across every model execution.
- If compatible-agent fixture execution is unavailable, static setup checks may pass but
  overall readiness remains `blocked`.
- If the source is too thin to pass specificity without invention, normal execution retains
  `[Missing]` and the bounded failure behavior.
- If the mapped workspace later becomes unwritable, the skill may return a passing result
  inline but reports persistence failure and does not write elsewhere.
- A fictional setup receipt proves schema coherence, not historical production use.

## Approval and release gates

1. The exact setup-amendment review digest must be owner-approved before implementation.
2. Implementation starts from refreshed current public `main` and stays inside the approved
   eighteen-path manifest.
3. Setup-contract, isolated-fixture, focused, full-suite, skill-pack, strict document, link,
   privacy, provenance, diff, and hosted checks pass or remain honestly unavailable.
4. This document and the candidate setup IP/privacy review remain Draft until the exact
   pull-request revision is reviewed.
5. The pull request requires project-owner Gate B approval and may not be merged or released
   automatically.
