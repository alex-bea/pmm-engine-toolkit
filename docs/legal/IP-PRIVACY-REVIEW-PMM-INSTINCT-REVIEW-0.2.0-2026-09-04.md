---
doc_type: DOC
normative: false
requires:
  - ../../plugins/pmm-instinct-review/skills/pmm-instinct-review/references/DOC-product-requirements.md
  - ../STD-evidence-privacy-v1.0.md
status: Draft
version: "0.2.0"
owner: toolkit-maintainers
consumers:
  - public toolkit maintainers
change_control: Pull request review
---

# PMM Instinct Review `0.2.0` IP and privacy review

## Scope and decision

This Draft review covers the changed `plugins/pmm-instinct-review/` candidate and its direct
tests, catalog/export registration, release note, and legal/security evidence. It supports
pull-request review only; it does not approve merge or publication.

## Public-safe construction

- Runtime and documentation are project-authored generic implementations.
- Private behavior informed functional requirements, but no private source file, transcript,
  audit, suggestion, instinct, output, identifier, route table, or alias map is included.
- The Northstar Reports lifecycle is independently authored fiction. Its entities, dates,
  IDs, paths, language, metrics, and relationships are synthetic; web and email values use
  `.invalid`.
- Seven template families without a qualifying private instance were implemented from the
  approved contract and synthetic tests rather than represented as observed evidence.
- Portable review is an interface, not a copy of private Claude desktop capture, hooks,
  configuration, or runtime layout.

## Data boundary

Codex capture stays disabled until explicit consent and stores bounded redacted user/
assistant evidence under the adopter's local state root. Portable review requires an explicit
separate root and candidate import. The package has no telemetry, hosted service, secret,
credential, live customer data, mutable adopter data, or automatic publishing path.

## Verification basis

The final candidate is subject to the publicizer private-denylist scan, repository public-
safety validation, tracked-tree secret scan, complete unit suite, fictional cross-file tests,
and human narrative review. Machine evidence is recorded separately. Findings must be removed
or explicitly adjudicated before pull-request readiness is claimed.

## Residual risk

Automated matching cannot prove that all prose lacks a narrative resemblance to a private
session, and user-imported candidate data may contain sensitive content. Local skill discovery
may expose adopter-owned names to that adopter's process. These risks are bounded through
minimized local-only processing, explicit import/consent, untrusted-data handling, no bundled
private routes, a run-specific denylist, and final human review.
