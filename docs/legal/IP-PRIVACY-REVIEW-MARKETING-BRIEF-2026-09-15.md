---
doc_type: DOC
normative: false
requires:
  - ../DOC-marketing-brief-product-requirements-v1.0.md
  - ../DOC-marketing-brief-source-inventory-v1.0.md
  - ../STD-evidence-privacy-v1.0.md
status: Draft
version: "1.0"
owner: alex-bea
consumers:
  - marketing-brief maintainers
  - privacy reviewers
  - release reviewers
change_control: Pull request review
---

# Marketing Brief Fidelity Correction IP and Privacy Review (2026-09-15)

## Review scope

This review covers the correction that restores generic writing and formatting constraints
to `skills/marketing-brief/`, adds fictional behavioral cases, strengthens focused tests,
clarifies the public product requirements, and regenerates the IP inventory.

It does not authorize private-source publication, connectors, data collection, model hosting,
external writes, merge, or release.

## Authoring provenance

The private PMM Engine implementation was used only to identify reusable workflow constraints
that the public package omitted. The restored constraints concern punctuation, tone, and
section separation. They contain no private fact, identity, product claim, or operating data.

Real private outputs were inspected only for structural coverage. No real output, source
excerpt, entity, fact, phrase, identifier, URL, metric, date, claim, or private-to-fictional
mapping is included in this candidate.

## Public changes and sanitization

- The output template now prohibits em dashes in final briefs.
- The output template restores a professional, pragmatic, direct, and slightly positive tone.
- The output template requires blank-line spacing instead of decorative section rules.
- The runbook explicitly binds every global template rule.
- The behavior-case fixture uses independently invented scenarios and contains no real
  organization, person, customer, partner, launch, metric, internal URL, or identifier.
- Existing fictional source and completed-brief examples remain unchanged.

## Behavioral evaluation

An ephemeral read-only Codex evaluation reviewed CASE-MB-001 through CASE-MB-005 against the
package contract. Source conflict, explicit/default tiering, multiple launches, missing data
with a research request, and scoped edits all passed at the contract level.

This result does not claim full end-to-end generation quality. It verifies that the fictional
cases correctly represent the documented workflow. Full generation quality would additionally
require checking generated briefs for evidence fidelity, completeness, exact structure, limits,
tone, privacy, and unsupported claims.

## Verification evidence

- Review-package approval digest: valid and owner-approved.
- Focused marketing-brief tests: 12 pass.
- Ephemeral compatible-agent contract evaluation: all five behavior cases pass; Tier case A,
  B, and C were assessed separately.
- Complete public unit suite: 267 pass.
- Public skill-package validator: 25 standalone skills and two plugins pass.
- GitHub Actions validator: three SHA-pinned, least-privilege workflows pass.
- Strict governed-document audit: 66 governed Markdown documents pass with no findings.
- Skill Creator package validation: pass.
- Read-only repository security-plan command: pass without external mutation.
- IP inventory: regenerated for 450 artifacts; a second regeneration produced the identical
  SHA-256 digest.
- Candidate privacy scan with the run-private denylist: clean. The scanner intentionally
  allowed the documented `[Missing]` marker in the missing-data fixture; the completed-example
  test separately confirms that the sole completed brief has no unfinished placeholder.
- Diff-boundary review: seven approved paths and no unapproved tracked path.

All available candidate checks passed. The compatible-agent result remains explicitly
contract-level rather than a full end-to-end generation-quality claim.

## Residual risk

Static checks and contract evaluation cannot guarantee that every model invocation will follow
subjective tone guidance or avoid punctuation drift. Automated privacy scanning cannot prove
that prose is non-identifying. Focused tests, human review, and pull-request review remain
required for later changes.

## Publication conditions

- Keep this document Draft until the exact pull-request revision is reviewed.
- Keep private evidence and the run-specific denylist outside the public repository.
- Run every available candidate check and label unavailable checks accurately.
- Require project-owner review before merge or release.

This is a repository-content review, not legal advice.
