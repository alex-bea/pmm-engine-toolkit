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

# Competitive-Intelligence Framework IP and Privacy Review — 2026-09-03

Status: draft pending pull-request approval.

## Candidate reviewed

This review covers the public `skills/comp-intel/` package changes that translate a mature
private operating method into a generic analyst workflow, fillable templates, and a fictional
worked example. The candidate includes the guided onboarding runbook, resumable setup record,
verified source-map structure, adopter-positioning approval file, limited-baseline behavior,
and source-enrichment handoff. It also covers the related catalog, contributor-routing,
export-manifest, test, and IP-inventory changes in the same candidate.

It does not cover adopter data, live source connections, private migration, external
publication, a marketplace submission, or any future real-company example.

## Provenance and redistribution

- The workflow language, templates, examples, and tests are project-authored.
- The private package was used only to identify reusable process structure and completeness
  criteria. No private source excerpt, registry row, counter-positioning, channel identifier,
  person-specific profile, customer/deal record, or generated output is included.
- The worked example uses invented organizations, products, claims, events, and evidence.
  Reserved `.invalid` domains are intentionally non-resolving.
- Existing controller source and schemas remain under the repository's Apache-2.0 boundary;
  this candidate changes their positioning and one generic roster enum, not their provenance.

## Privacy and semantic-leak checks

The package was checked for known organization and product names from the private source,
private channel patterns, developer-specific absolute paths, credential patterns, and real
customer or deal information. No finding remains in `skills/comp-intel/`.

Live mappings, evidence, stakeholder context, registries, trackers, and reports are explicitly
adopter-owned and stored outside the installed skill. The templates require sensitivity and
public-safety labels. Candidate URLs remain outside the canonical source map until adopter
verification, and internal message or document contents remain unread until the adopter grants
access. The workflow keeps publication and external messaging out of scope.

## Verification evidence

- Skill Creator validation: pass.
- Competitive-intelligence contract validation: pass.
- Full unit suite: 117 tests pass.
- Public skill-package validator: 25 skills and two plugins pass.
- Governed-document strict audit: 34 documents pass, including this review.
- GitHub Actions validator: three pinned, least-privilege workflows pass.
- IP inventory regenerated for the complete candidate.

## Publication conditions

- Keep this review and the example visibly Draft until pull-request approval.
- Re-run the complete verification suite after any candidate change.
- Review the exact diff before merge and preserve the synthetic-only package boundary.
- Perform a separate review before adding external quotations, live datasets, real-company
  examples, bundled source connections, binaries, or marketplace packaging.

This is a repository-content review, not legal advice.
