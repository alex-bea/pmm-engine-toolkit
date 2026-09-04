---
doc_type: DOC
normative: false
requires:
  - ../STD-evidence-privacy-v1.0.md
  - ../PUBLIC-EXPORT-MANIFEST.md
status: Draft
version: "1.0"
owner: Alex Bea
consumers:
  - Maintainers
  - Security reviewers
  - Public contributors
change_control: Pull request review
---

# Competitive-Intelligence Sanitized Example IP and Privacy Review — 2026-09-03

Status: Draft pending pull-request approval.

## Candidate reviewed

This review covers `skills/comp-intel/examples/fictional-embedded-wallets/`, its index, the
public package and catalog descriptions, the source-inventory row, the tests that govern the
example, and the corresponding IP-inventory changes. The candidate replaces the prior thin
developer-tools walkthrough with one complete limited baseline for fictional adopter HarborKey
and six fictional embedded-wallet competitors.

The optional controller configuration, mappings, schemas, scripts, and JSON fixtures are not
changed by this candidate. Adopter data, live source connections, real-company examples,
external publication, and marketplace packaging remain outside scope.

## Structural provenance

The private wallets workflow was used as an authoring reference for reusable document shapes,
information categories, workflow stages, analytical relationships, and expected depth. It is
not a runtime or installation dependency. No source document, row, excerpt, source identifier,
private mapping, or generated output is published.

The public set contains one completed counterpart for each of the 11 human-readable templates.
Its structures are project-authored adaptations for the public package.

## Sanitization method

The example uses a coherent but wholly invented scenario. Every organization, product, person,
customer, channel, channel identifier, document title, URL, quotation, claim, price, date,
transaction, acquisition, evaluation, and deal fact was replaced with a new fictional value.
All web addresses use reserved `.invalid` domains, and internal references use explicitly
fictional URI schemes or labels.

Sanitization preserved only reusable abstractions: the source families, roster and status
policy, positioning fields, evidence classes, review gates, registry relationships, gap and
signal trackers, run chronology, coverage behavior, and proposed-change boundary. No
one-to-one private-to-fictional alias map was created or published. The fictional facts are not
intended to encode, summarize, or permit reconstruction of any specific private fact.

## Privacy and evidence safeguards

- Candidate links remain outside the canonical source map until adopter verification.
- Internal content is represented only by invented evidence and is labeled internal.
- Internal evidence cannot support an external claim without corroborating public evidence.
- Conflicting, rejected, duplicate, superseded, and out-of-window records remain visible.
- The briefing is explicitly `LIMITED COVERAGE` and identifies premature comparisons.
- All registry and tracker changes remain proposed until review of the exact draft.
- Live mappings, evidence, credentials, stakeholder context, registries, trackers, and reports
  remain adopter-owned and outside the installed skill.

## Verification evidence

- Skill Creator validation: pass.
- Competitive-intelligence package validation: pass.
- Golden-example contract: 13 tests pass, covering template parity, semantic fields,
  placeholder rejection, source-family coverage, input counts, cross-file IDs, chronology,
  table shape, reserved domains, private terms, evidence classes, safety states, and
  evidence-to-claim traceability.
- Full unit suite: 123 tests pass.
- Public skill-package validator: 25 skills and two plugins pass.
- Governed-document strict audit: 35 documents pass, including this review.
- GitHub Actions validator: three SHA-pinned, least-privilege workflows pass.
- IP inventory regenerated for 336 artifacts with no missing or extra paths.
- Supplemental scan: no known private wallet-workflow entity, employee, channel, source URL,
  absolute-path, or credential-pattern finding remains in `skills/comp-intel/`.

Any content change requires the relevant checks to be rerun.

## Publication conditions

- Keep this review and the example visibly Draft until pull-request approval.
- Review the exact diff before merge and preserve the synthetic-only package boundary.
- Do not add an alias map, private source, real fact, real URL, or unreviewed quotation.
- Perform a separate review before adding real-company examples, external datasets, binaries,
  bundled source connections, or marketplace packaging.

This is a repository-content review, not legal advice.
