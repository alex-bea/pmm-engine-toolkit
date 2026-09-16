---
doc_type: DOC
normative: false
requires:
  - ../DOC-pre-read-sharpener-product-requirements-v1.1.md
  - ../DOC-pre-read-sharpener-source-inventory-v1.1.md
  - ../STD-evidence-privacy-v1.0.md
status: Draft
version: "1.0"
owner: alex-bea
consumers:
  - pre-read-sharpener maintainers
  - privacy reviewers
  - release reviewers
change_control: Pull request review
---

# Pre-Read Sharpener Setup-Wizard IP and Privacy Review (2026-09-15)

## Review scope

This review covers the setup-wizard amendment to the public
`skills/pre-read-sharpener/` package: its sole setup-and-execution RUN, blank setup mapping
and receipt assets, fictional smoke fixture, setup behavior cases, package routing and guide,
focused tests, v1.1 governed requirements and inventory, catalog/export updates, and generated
IP inventory entries.

It does not approve private source publication, a live external integration, merge, release,
or external publication.

## Approval lineage

The faithful editorial package from pull request 19 is merged at public commit
`accf82de3bf980c200f095d188101a7d4aa7e852`. The project owner approved the separate setup
amendment review package with evidence digest
`sha256:25d0dae4f6476473c1d4fd175505ef4a62e7bda5ac2c575cf248e2f48b994cfb` on
September 15, 2026. The candidate is limited to the eighteen approved paths. Gate B must
bind to the exact follow-up pull-request revision; this review does not authorize merge.

## Authoring provenance

The private pre-read implementation remains the authoring reference for editorial workflow,
template, criteria, repair, persistence, edits, and errors. Those behaviors were already
generalized and reviewed in the merged public package and remain unchanged in this amendment.

The internal publicizer setup framework informed the generic ten-section setup structure,
mapping schemas, safe-test requirements, receipt fields, staleness rules, and readiness
states. It did not supply private source locators, output paths, approval records, receipts,
or authoring-machine defaults. The public setup text, blank templates, fixture values, tests,
and governed documentation are project-authored for this repository.

## Sanitization method

The candidate preserves reusable setup structure while excluding identifying context:

- private repository roots, worktrees, remotes, run directories, branches, and authoring
  paths are absent from the public package;
- blank assets use adopter placeholders and package-relative public paths;
- the setup fixture uses only the already-public fictional Harborline source plus invented
  temporary workspace paths, digests, runtime label, and timestamp;
- no populated private source map, output destination, configuration, or receipt appears;
- permission mechanisms are named without credentials or environment-variable values;
- setup and normal execution explicitly deny retrieval, publishing, messaging,
  notifications, scheduling, approval creation, network mutation, and production writes;
  and
- no private-to-fictional substitution map was created or published.

## Setup mapping and receipt review

The blank setup mapping covers one user-supplied draft, the bundled fictional fixture, and
an explicit `none` external-source interface. It covers local output, configuration,
receipt, and temporary test destinations plus an explicit `none` external destination. The
adopter must confirm actual paths, authorization mechanisms, timezone, and retention.

The blank receipt records package and configuration identity, readiness by source and
destination ID, installation and permission results, fixture execution, expected and actual
artifacts, skipped checks, files created, limitations, overall status, and next action. It
instructs adopters to omit credentials and unnecessary sensitive locators. Both artifacts
must be copied to adopter-owned paths outside the installed package.

## Fictional fixture review

The smoke fixture is visibly labeled fictional. It uses the existing Harborline Guided
Import source and completed output only as bundled synthetic evidence. Its install root,
workspace, digests, runtime name, timestamp, mappings, and receipt are invented test values,
not defaults or transformed private state.

The fixture expects one completed setup mapping, two collision-safe fictional pre-reads, and
one setup receipt beneath an isolated temporary workspace. It disables every external and
production mutation. The compatible-agent execution used only the bundled source, produced
the full ordered deliverable and ten passing criteria, created the numeric-suffix collision
artifact, wrote the receipt, and left the copied package unchanged.

## Privacy and safety safeguards

- Real drafts remain user-supplied, authorized, and untrusted.
- No research, retrieval, cross-document synthesis, or invented support is permitted.
- Configuration, receipts, drafts, tests, and generated outputs stay outside the installed
  package.
- Missing, ambiguous, unwritable, colliding, or unsafe required destinations block setup.
- No secret or external adapter is required or bundled.
- Static validation is kept separate from compatible-agent fixture execution.
- Failed, skipped, and unavailable checks cannot be represented as passes.
- A receipt becomes stale after package, required mapping, dependency, or configuration
  digest changes.
- Setup readiness authorizes only the mapped local workflow and does not authorize sharing,
  publication, merge, or release.

## Verification evidence

Local candidate verification is complete. Hosted pull-request checks and Gate B review
remain pending. No unrun check is represented as passing.

| Check | Status | Evidence |
|---|---|---|
| Review package and Gate A | pass | Contract 1.1 validates at the exact approved digest and records owner approval. |
| Setup-contract validator | pass | Sole setup-workflow RUN, ten headings, both mapping tables, fixture links, readiness states, and safety terms pass. |
| Focused pre-read tests | pass | All 16 focused tests pass in the hash-locked repository environment. |
| Isolated copied-package fixture | pass | Package closure, source resolution, full transformation, ten criteria, collision suffixing, receipt creation, source traceability, and unchanged installed copy pass. |
| Stale-receipt probe | pass | A changed configuration digest differs from the receipt digest and requires revalidation. |
| Complete public unit suite | pass | All 283 tests pass in the hash-locked repository environment. |
| Public skill-package validator | pass | Validated 25 standalone skills, two plugins, and declared dependencies. |
| Strict governed-document audit | pass | Audited 72 governed documents with no findings. |
| GitHub Actions validator and read-only security plan | pass | Validated three SHA-pinned least-privilege workflows; plan generation completed without mutation. |
| Link, catalog, export, and dependency checks | pass | Focused tests, strict document audit, and package validation resolved active package and governed links. |
| IP inventory regeneration | pass | Deterministic regeneration produced 466 records with unchanged repeated-run digest `92caea72950d17d45262429950017601dec131b987956ea7e94e393311107766`. |
| Private-denylist candidate scan | pass | The complete skill package returned zero findings with the run-specific private denylist. |
| Manual non-reversibility review | pass; owner review pending | Added-line review found no private terms, authoring paths, secret patterns, copied private mappings, or reversible aliases. |
| Diff-to-approved-manifest check | pass | Exactly the approved eighteen paths changed; retained editorial artifacts and discovery metadata remained unchanged. |
| Hosted pull-request checks | not run | Required after the pull request opens. |

## Residual risk

Automated scanning cannot prove that prose and paths are independently conceived, so human
comparison remains required. The compatible-agent fixture proves one complete synthetic
path, not editorial quality for every real draft or runtime. The fictional receipt proves
schema coherence, not historical production use.

The skill may process confidential drafts in an adopter-authorized workspace. Users remain
responsible for selecting safe local paths, protecting their configuration and output, and
reviewing generated pre-reads before sharing them.

## Publication conditions

- Complete every applicable local and hosted check or state the exact limitation.
- Keep this review and the v1.1 requirements Draft until the exact pull-request revision is
  reviewed.
- Do not add private examples, live internal locators, populated mappings, credentials,
  receipts, or an alias map.
- Perform a new review before adding retrieval, connectors, hosted services, live external
  writes, real-company examples, binaries, or background processes.
- Require Gate B project-owner approval before merge or release.

This is a repository-content review, not legal advice.
