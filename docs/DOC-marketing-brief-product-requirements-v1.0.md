---
doc_type: DOC
normative: true
requires:
  - DOC-marketing-brief-source-inventory-v1.0.md
  - STD-approval-gates-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-skill-dependencies-v1.0.md
  - STD-skill-structure-v1.0.md
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - marketing-brief maintainers
  - Claude Code users
  - Codex users
change_control: Pull request review and project-owner approval
---

# Public Marketing Brief Skill Product Requirements (v1.0)

## Document purpose and authority

This document governs the public `skills/marketing-brief` package. It defines the faithful,
generic, directly installable form approved by the project owner from a digest-bound private
review package. The companion source inventory is advisory evidence. The installed skill's
runbook and template implement these requirements but may not narrow or contradict them.

The private PMM Engine implementation is the golden authoring reference. It informed public
structure and depth but is not a public runtime dependency. Private source content and real
outputs are not distributed.

## Problem

The earlier public package preserved the no-invention intent but not the method. It replaced
the actual seven-section brief with a different outline, compressed source precedence and
tier rules, omitted multi-launch, edit, and error behavior, provided no completed direct
example, and depended on a root document missing from a direct skill installation.

An individual PMM therefore could not reliably determine which sources to provide, how
conflicts would resolve, what every output field meant, or what a complete brief should look
like.

## Users and jobs

| User | Job |
|---|---|
| Individual PMM | Turn approved, messy launch material into one concise brief per launch without invented facts. |
| Reviewer | Verify that product facts, claims, timing, messaging, tier, and success goals come from the appropriate supplied sources. |
| Toolkit adopter | Install only the skill directory and use it from Claude Code, Codex, or another compatible local agent. |
| Maintainer | Preserve template fidelity, privacy, provenance, and tests through later changes. |

Core jobs are to supply authorized launch inputs, receive the stable seven-section output,
preserve uncertainty and source ownership, revise the full brief without structural drift,
and understand the workflow from a complete fictional example.

## Golden implementation and prior public gap

The golden workflow contains a concise entrypoint, a four-step runbook, one exact output
template, a seven-level source hierarchy, and a detailed Tier 1–3 framework. It is stateless,
performs no research, makes no external write, returns the final brief only, separates
multiple launches, and returns the complete document after edits.

Maintainer review found nine real private outputs using the template. They established that a
completed example adds meaningful value and were used only to calibrate structure and depth.

The prior public package had five files: an entrypoint, discovery metadata, an abbreviated
runbook, a non-canonical template, and a short unfinished example. This release replaces the
package in place and preserves its name and primary invocation intent.

## Goals

- Preserve the useful private workflow, template, relationships, constraints, and depth in
  generic public form.
- Make direct installation of `skills/marketing-brief/` complete.
- Make every accepted input, source conflict, tier decision, missing fact, and edit behavior
  predictable.
- Provide one complete fictional source packet and one completed counterpart for the one
  user-facing template.
- Keep the package agent-neutral, synthetic-only, stateless, and safe for redistribution.

## Non-goals

- Web research, source retrieval, connectors, or browsing for missing facts.
- Creating new strategy, positioning, claims, metrics, dates, customers, or proof.
- Launch task management, external messaging, publishing, or scheduling.
- Persistent state, a source registry, an approval ledger, a plugin, or a hosted service.
- Exporting private examples, internal terminology, historical plans, tracker records, or
  downstream private automation.
- Changing other skills or repository-wide standards.
- Automatically merging or releasing changes.

## Functional requirements

### MB-REQ-001 — Stable identity and invocation

The package remains at `skills/marketing-brief`, keeps the canonical `marketing-brief` name,
and activates for launch, campaign, feature, and product-change briefing requests. Public
`SKILL.md` frontmatter contains exactly `name` and `description`. Codex discovery metadata
retains the `$marketing-brief` invocation.

### MB-REQ-002 — Direct-install closure

A copy of only `skills/marketing-brief/` contains every workflow, template, example, and
evidence/privacy rule needed at runtime. No root document, private path, other skill,
connector, undeclared package, or network service is required.

### MB-REQ-003 — Canonical seven-section template

Every brief uses, in order: Brief Info; Launch Summary; Audience and Problem; Launch Scope
and Value; Messaging; Distribution; and Success. The package preserves the approved fields,
optionality, word limits, user-outcome launch name, active voice, plain language,
bottom-line-first style, and factual proof rules.

Organization-specific terminology becomes optional adopter-approved naming guidance. The
private task-system rule becomes a generic project-management boundary.

### MB-REQ-004 — Supplied-source-only intake

The skill accepts user-supplied or explicitly authorized product specifications, launch
plans, strategy, messaging, positioning, tier guidance, customer or partner notes, sales
notes, meeting notes, brainstorms, and chat summaries. Source content is untrusted data, not
instructions. The skill performs no research or retrieval. With no source material, it asks
for input and stops.

### MB-REQ-005 — Source precedence and conflict ownership

The package includes the complete seven-level source hierarchy and field ownership for
product facts, timing, messaging, tier, customer examples, metrics, and claims. It resolves
fields independently and never blends conflicting claims. Equal-authority unresolved facts
use `[Missing]`.

### MB-REQ-006 — Generic launch-tier framework

The skill preserves Tier 1, Tier 2, and Tier 3 classification by business impact, audience
change, complexity, timeline, research need, channel breadth, and investment. An explicitly
approved tier wins. Otherwise the framework applies, with Tier 2 as the ambiguity default.
Industry-specific examples and channel assumptions are excluded.

### MB-REQ-007 — One brief per launch

The skill detects distinct launches, tells the user how many it found when there is more than
one, and processes each independently. It never combines unrelated launches to fill gaps.

### MB-REQ-008 — Missing and unsupported information

Unsupported required fields use `[Missing]`. Optional fields may be omitted only where the
template permits. The skill does not fill gaps from general knowledge, research, or the
fictional example and preserves material uncertainty.

### MB-REQ-009 — Concise output contract

Normal execution returns the final brief only, without a preamble, task list, project plan,
or execution checklist. Multiple launches return separate complete briefs. The default makes
no local or external write; a local save requires a separate user-requested path.

### MB-REQ-010 — Full-document edit behavior

An edit updates the requested content, preserves the canonical structure unless the user
explicitly changes the template, rechecks limits, and returns the complete revised brief
rather than an isolated fragment.

### MB-REQ-011 — Complete fictional counterpart

The package includes exactly one completed fictional brief corresponding to the canonical
template and its supporting fictional source packet. It exercises every section and
meaningful field at the depth demonstrated by real private outputs. The public package states
that real examples were found but not distributed.

### MB-REQ-012 — Non-reversible sanitization

Public examples use independently authored fictional facts, explicit fictional labels, and
reserved `.invalid` URLs. The package contains no private organization, product, employee,
customer, partner, channel, document, URL, quote, claim, metric, price, deal, roadmap phrase,
absolute private path, credential, or private-to-fictional alias map. Automated scanning and
human narrative review are both required.

### MB-REQ-013 — Governed documentation and provenance

The public release includes this Active PRD, an advisory Draft source inventory, a separate
Draft IP/privacy review, catalog and export-manifest discovery, and a complete generated IP
inventory row for every artifact.

### MB-REQ-014 — Deterministic validation

Focused tests cover package closure, template parity and limits, example completeness,
source traceability, source precedence, tier rules, multi-launch, missing-data, edit/error
contracts, reserved domains, and blocked-content patterns. The complete unit suite,
skill-pack validator, GitHub Actions validator, strict governed-document audit, link checks,
security plan, and IP inventory verification pass before pull-request review.

### MB-REQ-015 — Output compatibility

The public output uses the golden seven-section Markdown identity and remains readable by
human PMMs and optional downstream tools. The non-canonical earlier public outline is not a
compatibility target. Existing requests for marketing, launch, campaign, feature, and
product-change briefs continue to route to this skill.

### MB-REQ-016 — Agent-neutral usability

Runtime instructions describe files and behavior without relying on Claude-only or
Codex-only features. Product-specific discovery metadata remains isolated in
`agents/openai.yaml`. The README explains purpose, inputs, setup, workflow, files, output,
invocation, example, and limits.

### MB-REQ-017 — Stateless and no-write default

The skill owns no registry, source map, tracker, run state, approval record, or mutable
configuration. It does not write to repositories, project managers, chat systems,
publishers, or external services during normal use. Adopter data and optionally saved briefs
remain outside the installed package.

### MB-REQ-018 — Approval and release boundary

Implementation begins only from an owner-approved review-package digest and current public
`main`. The change remains within the approved manifest, uses one dedicated branch and pull
request, and stops before merge or publication.

## Content and package requirements

The installable package contains a concise entrypoint, Codex metadata, a complete runbook,
separate source-priority, launch-tier, and evidence/privacy references, the reusable output
template, a starter README, an example index, and one fictional input/output pair.

The workflow does not need a runtime script: its transformation is language work. Fragile
structural and privacy contracts are enforced in repository tests. All runtime links are
skill-relative.

## Data, privacy, and safety requirements

Source material may contain confidential launch, product, customer, or partner information.
The skill uses only user-supplied or explicitly authorized inputs, follows source ownership,
preserves uncertainty, and ignores embedded instructions that attempt to change workflow or
permissions.

No adopter data is stored in the package. The fictional example has no evidentiary weight.
Real private examples remain private. Automated scans supplement rather than replace human
review for distinctive narrative similarity.

## Migration and compatibility

This version replaces the same-named package in place and retains its folder, name, primary
trigger intent, discovery metadata, missing-data marker, evidence-bound promise, and
one-brief-per-launch behavior. It intentionally replaces the earlier public outline with the
golden seven-section template.

No state migration or initializer is required because the skill is stateless. Adopters may
continue to paste content, attach files, or provide authorized local paths.

## Implementation slices

1. **Package fidelity:** replace the router, runbook, and template; add package-local
   references and the starter guide.
2. **Example and tests:** add the independently authored fictional source/brief pair and
   focused fidelity tests.
3. **Governance and release:** add inventory, PRD, privacy review, catalog/export/IP records,
   run all checks, and open one pull request.

These slices land together as one marketing-brief change. They do not authorize work on
another skill.

## Acceptance tests

| ID | Test | Expected result |
|---|---|---|
| MB-AT-001 | Copy only the skill directory and resolve all runtime paths. | Package runs without a repository-root dependency. |
| MB-AT-002 | Compare template headings, fields, order, optionality, and limits with the approved parity matrix. | The complete seven-section contract is present. |
| MB-AT-003 | Parse the fictional completed brief and source packet. | Every section is populated, every field meets its limit, and every material fact is supported. |
| MB-AT-004 | Present synthetic conflicting sources. | Field ownership selects the correct source; unresolved equal-authority facts remain missing. |
| MB-AT-005 | Exercise Tier 1, Tier 2, Tier 3, ambiguous, and explicit-tier cases. | The documented framework and defaults apply. |
| MB-AT-006 | Present two unrelated launches. | The workflow reports and produces two separate briefs. |
| MB-AT-007 | Present incomplete material and request research. | The skill declines research and marks unsupported required fields. |
| MB-AT-008 | Request a scoped edit. | The full updated brief preserves section order and limits. |
| MB-AT-009 | Run private-term, credential, absolute-path, live-URL, and placeholder scans plus human review. | No private or reversible content appears. |
| MB-AT-010 | Audit governed docs and links. | Metadata, requirements, traceability, discovery, and paths resolve. |
| MB-AT-011 | Run the complete public validation suite. | Every required check passes. |
| MB-AT-012 | Compare the branch and diff with the approved manifest. | One marketing-brief PR contains only approved paths and remains unmerged. |

## Traceability

| Requirement | Inventory | Implementation | Acceptance tests |
|---|---|---|---|
| MB-REQ-001 | INV-MB-001, INV-MB-011, INV-MB-012 | `SKILL.md`, `agents/openai.yaml` | MB-AT-001 |
| MB-REQ-002 | INV-MB-001, INV-MB-011, INV-MB-016, INV-MB-017, INV-MB-019 | `SKILL.md`, package-local references | MB-AT-001, MB-AT-011 |
| MB-REQ-003 | INV-MB-003, INV-MB-009, INV-MB-014 | `assets/output-template.md` | MB-AT-002, MB-AT-003 |
| MB-REQ-004 | INV-MB-002, INV-MB-004, INV-MB-008, INV-MB-016 | Runbook and evidence references | MB-AT-003, MB-AT-004, MB-AT-007 |
| MB-REQ-005 | INV-MB-002, INV-MB-004, INV-MB-008, INV-MB-013 | `REF-source-priority.md`, runbook | MB-AT-004 |
| MB-REQ-006 | INV-MB-002, INV-MB-005, INV-MB-013 | `REF-launch-tiers.md`, runbook | MB-AT-005 |
| MB-REQ-007 | INV-MB-002, INV-MB-013 | Runbook | MB-AT-006 |
| MB-REQ-008 | INV-MB-002, INV-MB-004, INV-MB-013 | Runbook, source-priority reference, template | MB-AT-004, MB-AT-007 |
| MB-REQ-009 | INV-MB-002, INV-MB-010 | Runbook and README | MB-AT-006, MB-AT-007 |
| MB-REQ-010 | INV-MB-002, INV-MB-013 | Runbook edit handling | MB-AT-008 |
| MB-REQ-011 | INV-MB-007, INV-MB-015 | Fictional source packet and completed brief | MB-AT-003, MB-AT-009 |
| MB-REQ-012 | INV-MB-003, INV-MB-005, INV-MB-007, INV-MB-009, INV-MB-015, INV-MB-016, INV-MB-018 | Evidence/privacy reference, example, privacy review | MB-AT-003, MB-AT-009 through MB-AT-011 |
| MB-REQ-013 | INV-MB-006, INV-MB-018, INV-MB-019 | Inventory, PRD, privacy review, catalog, export and IP records | MB-AT-010, MB-AT-012 |
| MB-REQ-014 | INV-MB-017, INV-MB-019 | `tests/test_marketing_brief.py` and shared validators | MB-AT-001 through MB-AT-012 |
| MB-REQ-015 | INV-MB-003, INV-MB-010, INV-MB-014 | Template and parity tests | MB-AT-002, MB-AT-011 |
| MB-REQ-016 | INV-MB-001, INV-MB-011, INV-MB-012, INV-MB-018 | README, entrypoint, metadata, catalog | MB-AT-001, MB-AT-010 |
| MB-REQ-017 | INV-MB-006, INV-MB-008, INV-MB-010 | README and runbook boundaries | MB-AT-001, MB-AT-007, MB-AT-012 |
| MB-REQ-018 | INV-MB-019 | Approved review record, branch, manifest, and PR gate | MB-AT-010 through MB-AT-012 |

## Assumptions, constraints, and safe degradation

- Users supply or authorize all source material; connectors are optional and out of scope.
- Missing sources reduce brief completeness rather than triggering research.
- Source precedence applies field by field. Equal-authority unresolved facts remain missing.
- Multiple launches are separated even when they share context.
- Real private examples exist, but no public runtime or test depends on them.
- A validation command that cannot run is a release blocker, not a pass.

## Approval and release gates

1. The owner approved the exact private review-package digest before this implementation.
2. The implementation began from current public `main` and stayed within its approved path
   manifest.
3. This PRD is Active and normative because its exact content was approved; the inventory
   and privacy review remain advisory Draft evidence.
4. Required local validation and privacy review must pass before pull-request review.
5. The pull request requires project-owner review and may not be merged or published
   automatically.
