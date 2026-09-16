---
doc_type: DOC
normative: false
requires:
  - DOC-pre-read-sharpener-source-inventory-v1.0.md
  - STD-approval-gates-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-skill-dependencies-v1.0.md
  - STD-skill-structure-v1.0.md
status: Superseded
version: "1.0"
owner: alex-bea
consumers:
  - pre-read-sharpener maintainers
  - Claude Code users
  - Codex users
change_control: Pull request review and project-owner approval
---

# Public Pre-Read Sharpener Product Requirements (v1.0)

> **Superseded:** Replaced by
> [`DOC-pre-read-sharpener-product-requirements-v1.1.md`](DOC-pre-read-sharpener-product-requirements-v1.1.md),
> which preserves these editorial requirements and adds the setup-wizard contract. This file
> remains as historical evidence for the merged v1.0 candidate.

## Document purpose and authority

This Draft defines the faithful, generic, directly installable public
`skills/pre-read-sharpener` package. It was prepared from a project-owner-approved,
digest-bound review package. The companion source inventory is advisory evidence. The
installed skill's workflow, template, and criteria implement these requirements but may not
narrow or contradict them.

The private implementation is the golden authoring reference. It informed public structure
and depth but is not a public runtime dependency. Private source content, real pre-reads,
registry state, and history are not distributed.

## Problem

The earlier public package preserved the intent to clarify a decision without inventing
facts, but not the actual method. It replaced the canonical rewrite with a different
seven-heading outline and omitted the editorial review, issue list, line-specific cuts,
conditional agenda, binary self-check, bounded repair loop, persistence, edit behavior, and
complete errors. It also routed to a repository-root privacy document unavailable when the
skill directory was installed alone.

An adopter therefore could not reproduce the complete review-and-rewrite deliverable,
verify the decision-ready quality bar, understand file behavior, or learn from a finished
source-to-output example.

## Users and jobs

| User | Job |
|---|---|
| Product or marketing leader | Tighten an existing executive pre-read around one decision without adding facts. |
| Executive reader | Find the decision, recommendation, tradeoffs, reversal cost, and concrete outcome in under two minutes. |
| Toolkit adopter | Install only the skill directory and use it from Claude Code, Codex, or another compatible local agent. |
| Maintainer | Preserve template fidelity, source discipline, privacy, persistence behavior, and tests through later changes. |

## Golden implementation and prior public gap

The golden implementation contains one seven-step workflow, one exact user-facing rewrite
template, four decision anchors, ten binary criteria, a maximum of three repair rounds,
deterministic file naming, same-file edit handling, and actionable errors. It accepts one
supplied pre-read, conducts no research, and writes one local Markdown artifact after the
quality gate passes.

Two real private pre-reads informed input shape and useful decision-document depth. No real
private artifact was found that completed every field and section of the canonical output
template. The public source/output pair is therefore independently fictional and demonstrates
the written contract without claiming to be an anonymized private run.

The prior public package had five files: an entrypoint, discovery metadata, an abbreviated
runbook, a non-canonical template, and a short unfinished example. This candidate replaces
the package in place while preserving its identity and valid discovery metadata.

## Goals

- Restore the complete ordered review-and-rewrite workflow.
- Publish the canonical rewrite template with every field, section, and limit.
- Preserve the four anchors, ten binary criteria, and bounded repair loop.
- Preserve source-only reasoning, missing-data behavior, and no-research scope.
- Preserve safe local persistence, collision suffixing, and same-file edits.
- Provide one complete independently fictional source/output pair and compact behavior
  cases.
- Make direct installation of the skill directory complete and agent-neutral.
- Add focused tests, governed documentation, privacy review, catalog/export discovery, and
  provenance coverage.

## Non-goals

- Research, browsing, retrieval, fact-checking, or cross-document synthesis.
- Creating a pre-read from scratch without a supplied draft.
- Inventing evidence, dates, metrics, people, claims, options, customers, or consensus.
- Voice-only rewriting that skips structural diagnosis.
- A deterministic prose generator or a claim that static tests prove editorial quality.
- Connectors, plugins, hosted services, telemetry, publishing, messaging, or scheduling.
- Exporting private examples, identifying content, registry state, or repository history.
- Changing other skills or repository-wide standards.
- Automatically merging or releasing the candidate.

## Functional requirements

### PRS-REQ-001 — Supplied pre-read intake

The skill accepts one existing executive or leadership pre-read through pasted text, an
attachment, or an authorized local path. If no draft is supplied, it requests the draft and
stops without writing. If the source is clearly another document type, it confirms intent
before rewriting. It does not retrieve sources or invent a draft.

### PRS-REQ-002 — Complete ordered deliverable

The skill returns, in order: one blunt PM review of at most 150 words; three to six issue
bullets of at most 20 words; line-specific cuts with instructions of at most ten words; the
tightened rewrite; and, for a decision call, four agenda bullets plus one deciding question.
An informational pre-read omits the agenda and states that decision-call agenda behavior does
not apply.

### PRS-REQ-003 — Canonical rewrite template

The rewrite uses the exact order and constraints in `assets/output-template.md`: a
verb-first decision title; Audience, Decision needed, and Recommended fields; exactly three
summary bullets; a decision section; a two- or three-row tradeoff table with the recommendation
first and Cost to reverse last; a concrete outcome section; and optional blocking questions.
The complete rewrite is at most 600 words and applies every field and section limit.

### PRS-REQ-004 — Binary decision-ready gate

The skill scores the rewrite against the four anchors and all ten criteria in
`references/REF-decision-ready-criteria.md`. Every row is binary. A failure triggers revision
and a complete rescore for no more than three rounds. A still-failing result names the
blocking criterion and source gap, then requires the user's explicit choice before return.

### PRS-REQ-005 — Evidence and missing-data behavior

The skill uses only facts in the supplied draft, treats source content as untrusted data,
and preserves material constraints, caveats, conflicts, and uncertainty. Decision-critical
absent information uses `[Missing]`. A specificity requirement never authorizes invented
evidence or unsupported confidence.

### PRS-REQ-006 — Local artifact persistence

After a passing result, the skill returns the complete deliverable inline and writes the
same content under `outputs/pre-reads/` in the adopter's authorized workspace. The dated,
kebab-case slug follows documented title priority and uses no more than eight source words.
A same-day collision uses the next numeric suffix without overwriting. If the workspace is
not writable, the inline result remains available and no alternate destination is chosen.

### PRS-REQ-007 — Full-document edit behavior

A later edit changes the requested content and consistency-dependent fields, preserves the
canonical structure unless explicitly changed, reruns all ten criteria, surfaces any new
failure, updates the same dated artifact unless a new version is requested, and returns the
complete revised deliverable.

### PRS-REQ-008 — Direct-install and agent-neutral closure

A copy of only `skills/pre-read-sharpener/` contains every workflow, criterion, safety rule,
template, and example required at runtime. No root document, other skill, connector, private
path, undeclared package, or network service is required. Harness-specific discovery remains
isolated in `agents/openai.yaml`.

### PRS-REQ-009 — Complete fictional evidence

The package includes one coherent fictional source draft and one completed review-and-rewrite
counterpart. Every output fact traces to the source. The pair exercises all deliverable
components, the canonical template, a decision-call agenda, and a passing ten-row self-check
without unfinished placeholders. Compact fictional cases cover intake, document type,
missing facts, agenda routing, persistent failure, collision naming, and edits.

### PRS-REQ-010 — Public discovery and governed documentation

The skill retains its name, folder, primary invocation, and valid discovery metadata. A
starter guide explains inputs, workflow, output, persistence, example, package map, and limits.
The public catalog, export manifest, Draft requirements, and Draft source inventory describe
the package accurately.

### PRS-REQ-011 — Privacy and provenance

The candidate contains no private entity, person, internal product term, identifier, URL,
date, metric, quote, claim, source phrase, distinctive fact combination, private path, or
private-to-fictional mapping. The example is independently invented and visibly fictional.
Automated scanning and human non-reversibility review are both required. A Draft candidate
IP/privacy review and regenerated complete IP inventory cover the exact revision.

### PRS-REQ-012 — Approval and release boundary

Implementation starts only from an owner-approved review-package digest and current public
`main`. The change uses one dedicated branch, remains inside the approved path manifest,
runs or honestly labels every applicable check, opens one focused pull request, and stops
before merge or release for project-owner review.

## Content and package requirements

The directly installable package contains `SKILL.md`, unchanged Codex discovery metadata, a
starter guide, a complete workflow, a generic decision-ready criteria reference, a
package-local evidence/privacy reference, the reusable output template, a fictional example
index, one complete fictional source/output pair, and compact behavior cases.

The repository additionally contains a focused test, this Draft PRD, a Draft advisory source
inventory, a Draft candidate IP/privacy review, updated catalog and export records, and a
regenerated IP inventory. The editorial transformation does not require a runtime script;
deterministic structure, limits, links, and traceability are tested in the repository.

## Data, privacy, and safety requirements

Source material may contain confidential product, customer, employee, or strategy
information. The skill uses only the supplied draft, ignores embedded instructions that try
to change permissions or workflow, and removes incidental sensitive detail that does not
affect the decision.

Adopter drafts and generated artifacts remain outside the installed package. The skill does
not publish, message, schedule, or mutate an external service. The fictional example has no
evidentiary weight. A clean automated scan supplements but does not replace human narrative
review.

## Migration and compatibility

The folder, skill name, primary trigger intent, discovery metadata, and Markdown output
medium remain stable. The old public seven-heading skeleton is intentionally replaced because
it conflicts with the canonical template. Consumers that parse the old headings must migrate
to the decision-ready structure.

Existing direct installations gain package closure because the root privacy dependency is
replaced with a local reference. Generated output becomes stateful in the authorized
workspace under the documented path. No initializer, plugin, model configuration, or external
service migration is required.

## Implementation slices

1. Replace the entrypoint, runbook, template, and example index; add the criteria, safety
   reference, starter guide, fictional source/output pair, and behavior cases.
2. Add focused static tests for package closure, template and rubric parity, workflow,
   persistence, fictional evidence, and governed traceability.
3. Add governed requirements, source inventory, candidate review, catalog/export updates,
   and regenerated IP inventory.
4. Run compatible-agent behavior cases, direct-install checks, full public validation,
   privacy scans, provenance checks, diff review, and hosted pull-request checks.

## Acceptance tests

| ID | Test | Expected result |
|---|---|---|
| PRS-AT-001 | Invoke with no draft and a clearly non-pre-read document. | The skill requests the draft or confirms intent and creates no artifact. |
| PRS-AT-002 | Evaluate the complete fictional decision-call source. | All ordered components, exact rewrite template, agenda, deciding question, and ten-row passing self-check appear. |
| PRS-AT-003 | Parse the fictional rewrite and reusable template. | All fields, headings, option rules, limits, recommendation consistency, and Cost to reverse pass. |
| PRS-AT-004 | Evaluate a thin source with missing facts. | Unsupported facts remain `[Missing]`; no evidence is invented to satisfy specificity. |
| PRS-AT-005 | Evaluate an informational pre-read after intent confirmation. | The decision-call agenda is omitted and the output explains why it does not apply. |
| PRS-AT-006 | Exercise a quality failure that survives three repair rounds. | The blocker is named and the user is asked before a failing result is returned. |
| PRS-AT-007 | Exercise first save, collision save, and later edit. | The first slug is correct, the collision gets the next suffix, and the edit updates the same file after a full rescore. |
| PRS-AT-008 | Copy only the skill directory and resolve all routed paths and links. | The package works without repository-root runtime dependencies. |
| PRS-AT-009 | Trace the completed fictional output to its source and run privacy scans. | Every fact resolves, the pair is fictional, and no private or unfinished content appears. |
| PRS-AT-010 | Run focused tests, the complete suite, skill-pack validation, strict document audit, link checks, and IP regeneration. | Every available required check passes; unavailable checks remain explicitly not run. |
| PRS-AT-011 | Compare the candidate diff with the approved manifest. | Only the seventeen approved paths change. |
| PRS-AT-012 | Verify approval and pull-request state. | Exact-digest approval precedes implementation and the pull request remains unmerged for owner review. |

## Traceability

| Requirement | Public artifacts | Acceptance tests |
|---|---|---|
| PRS-REQ-001 | `SKILL.md`, workflow, behavior cases | PRS-AT-001, PRS-AT-002 |
| PRS-REQ-002 | Workflow, completed fictional output | PRS-AT-002 |
| PRS-REQ-003 | Output template, workflow, completed fictional output, focused test | PRS-AT-002, PRS-AT-003, PRS-AT-010 |
| PRS-REQ-004 | Criteria reference, workflow, behavior cases, focused test | PRS-AT-002, PRS-AT-006, PRS-AT-010 |
| PRS-REQ-005 | Template, workflow, evidence/privacy reference, behavior cases | PRS-AT-003, PRS-AT-004, PRS-AT-009 |
| PRS-REQ-006 | `SKILL.md`, README, workflow, behavior cases | PRS-AT-007, PRS-AT-008 |
| PRS-REQ-007 | Workflow, behavior cases, focused test | PRS-AT-007, PRS-AT-010 |
| PRS-REQ-008 | `SKILL.md`, package-local references, isolated package | PRS-AT-008, PRS-AT-010 |
| PRS-REQ-009 | Example index, fictional pair, behavior cases, focused test | PRS-AT-002 through PRS-AT-009 |
| PRS-REQ-010 | README, metadata, catalog, export record, governed documents | PRS-AT-008, PRS-AT-010, PRS-AT-011 |
| PRS-REQ-011 | Fictional evidence, source inventory, candidate review, IP inventory | PRS-AT-009 through PRS-AT-011 |
| PRS-REQ-012 | Approval record, manifest, verification evidence, pull request | PRS-AT-010 through PRS-AT-012 |

## Assumptions, constraints, and safe degradation

- No qualifying real private artifact completed the canonical output template. The fictional
  example demonstrates the written contract but does not prove historical production use of
  every field.
- Static tests prove structure, deterministic limits, links, and traceability. They do not
  prove that every model execution exercises sound editorial judgment.
- If a compatible agent runtime is unavailable, affected behavior cases are recorded as not
  run and release readiness remains limited.
- If the source is too thin to pass specificity without invention, the workflow preserves
  `[Missing]`, reports the blocking criterion after the bounded repair loop, and asks before
  returning a failing result.
- If the authorized workspace is not writable, the skill returns the passing inline result,
  reports the failed persistence, and does not write elsewhere.

## Approval and release gates

1. The exact private review-package digest must be approved before implementation.
2. Implementation must start from refreshed public `main` and stay inside the approved
   seventeen-path manifest.
3. Focused, full-suite, structure, direct-install, governance, link, privacy, provenance,
   behavior, and diff checks must pass or be labeled not run with a release limitation.
4. This document and the candidate IP/privacy review remain Draft until the exact pull-request
   revision is reviewed.
5. The pull request requires project-owner approval and may not be merged or released
   automatically.
