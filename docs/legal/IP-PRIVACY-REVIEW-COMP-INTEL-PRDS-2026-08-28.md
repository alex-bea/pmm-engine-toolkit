---
doc_type: DOC
normative: false
requires:
  - ../product-requirements/comp-intel/README.md
  - ../STD-evidence-privacy-v1.0.md
status: Draft
version: "1.0"
owner: Alex Bea
consumers:
  - Maintainers
  - Security reviewers
  - Public contributors
change_control: Pull request review
---

# Competitive-Intelligence PRD IP and Privacy Review — 2026-08-28

Status: draft pending pull-request approval.

## Candidate reviewed

This review covers the competitive-intelligence product-requirements directory, its root
Codex routing instructions, and the repository index and manifest changes that expose the
suite. It covers documentation only. It does not approve or review a future controller,
connector, private-data migration, public golden-example corpus, or plugin binary.

## Provenance and redistribution assessment

- The documents are project-authored architecture and product requirements derived from an
  analysis of the author's existing workflow.
- Private implementation materials informed the analysis but are not distributed as source
  dependencies, fixtures, registries, examples, or copied runtime content.
- Claude, Codex, OpenAI, GitHub, Slack, and Polygon are used only as nominative product,
  compatibility, migration, or golden-example references. No logos, screenshots, slogans,
  third-party datasets, source code, or product collateral are included.
- Official documentation appears as external hyperlinks; linked content is not reproduced.
- The candidate is suitable for inclusion under the repository's Apache-2.0 license, subject
  to pull-request approval and the conditions below.

## Privacy and semantic-leak assessment

The candidate was reviewed for developer-specific paths, credentials, account and channel
identifiers, private customer or deal data, stakeholder profiles, unpublished positioning,
private competitor records, and private workflow outputs. None are intended to be present.
The master PRD now describes private migration evidence by category and explicitly states
that private source paths are not public dependencies.

The public Polygon material in this candidate is a requirements-level golden-example policy
only. It contains no public-source corpus, extracted claims, or derived competitive output.
Those later artifacts require their own source manifest, provenance review, semantic-leak
review, and exact-digest approval.

## Publication conditions

- Keep every product-requirements document marked `Draft` until its stated review and
  approval process completes.
- Require adopters to map their own internal names, channels, systems, permissions,
  intelligence data, reviewers, and output destinations; do not ship or infer those values.
- Build named golden examples only from approved public sources and keep synthetic fixtures
  fictional and visibly labeled.
- Re-run the repository validator, test suite, path inventory, private-pattern scan, link
  check, and manual semantic review whenever the candidate changes.
- Perform a fresh rights and privacy review for implementation code, external quotations,
  datasets, images, binaries, or public-source evidence added later.

This is a repository-content review, not legal advice.
