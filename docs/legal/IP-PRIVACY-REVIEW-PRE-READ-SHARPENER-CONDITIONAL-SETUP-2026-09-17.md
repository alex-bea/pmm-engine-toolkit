---
doc_type: DOC
normative: false
requires:
  - ../DOC-pre-read-sharpener-product-requirements-v1.2.md
  - ../DOC-pre-read-sharpener-source-inventory-v1.2.md
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

# Pre-Read Sharpener Conditional Setup IP and Privacy Review (2026-09-17)

## Review scope

This Draft covers the conditional-setup amendment to public `skills/pre-read-sharpener/`:
its sole normal RUN, conditional setup contract, blank YAML configuration and receipt,
fictional setup/routing evidence, behavior cases, package router and guide, focused tests,
v1.2 governed requirements and inventory, catalog/export records, and generated IP inventory.

It does not approve private source publication, a live external integration, merge, release,
or external publication.

## Approval lineage

The setup-first package is present on public `main` at base commit
`f84dd4a82906945cfe124c98fd5a101614351734`. The project owner approved the conditional
setup review package with evidence digest
`sha256:b2e521fc208a5fce71497aee1ea22670f5d7e53e9ca9c34ad5c5d5a5fd08081c` on
September 17, 2026. The candidate is limited to the twenty-one approved paths. Gate B must
bind to the exact pull-request revision; this review does not authorize merge.

## Authoring provenance

The editorial workflow, output structure, binary criteria, bounded repair, persistence,
edit handling, and error behavior were generalized in the existing public package and
remain materially unchanged.

The conditional setup framework informed the split RUN/reference architecture, profile,
mapping tables, YAML schemas, safe-test requirements, receipt fields, staleness rules, and
routing states. It supplied no private locator, output path, approval record, populated
configuration, receipt, or authoring-machine default. Candidate prose, schemas, fixtures,
tests, and governed documents are project-authored for this public repository.

## Sanitization method

The candidate preserves reusable structure while excluding identifying context:

- no private repository root, worktree, remote, run directory, or authoring path appears;
- blank YAML assets use adopter placeholders and package-relative public paths;
- the fixture uses only the public fictional Harborline source/output pair plus invented
  temporary paths, digests, revision, and timestamps;
- no populated private source map, destination, configuration, or receipt appears;
- permission mechanisms are named without credentials or environment-variable values;
- normal and setup instructions deny retrieval, publishing, messaging, notifications,
  scheduling, approval creation, network mutation, and production writes; and
- no private-to-fictional substitution map was created or published.

## Setup configuration and receipt review

The blank configuration covers one user-supplied draft, one bundled fictional fixture, and
local output, configuration, receipt, and test destinations. External sources and external
mutation are explicit `none` interfaces in the setup contract. The adopter confirms actual
paths, authorization mechanisms, timezone, and retention.

The blank receipt records package and configuration identity, setup-contract version,
required checks, limitations, normal entrypoint, and repair action without credentials or
unnecessary sensitive locators. Completed state belongs at stable adopter-owned paths
outside the installed package.

## Conditional routing and fixture review

Inline work bypasses setup. Persistent work with a current `ready` receipt enters the sole
normal RUN without rereading setup detail or rerunning the fixture. Missing, stale, and
blocked persistence routes enter the setup contract. Dates are evidence, not expiry.

The fixture is visibly fictional and uses an isolated install copy plus a separate temporary
workspace. It expects YAML state and two collision-safe fictional outputs, verifies package
hash stability, and exercises ready, missing, stale, and blocked results. It disables every
external and production mutation. Conditional loading remains instruction-only because the
package includes no mandatory dispatcher; deterministic tests prove status semantics and
filesystem effects, not which reference an AI loaded.

## Privacy and safety safeguards

- Real drafts remain user-supplied, authorized, and untrusted.
- No research, retrieval, cross-document synthesis, or invented support is permitted.
- Configuration, receipts, drafts, tests, and generated outputs stay outside the package.
- Missing, ambiguous, unwritable, or unsafe persistent destinations block persistence while
  leaving inline output available.
- No secret or external adapter is required or bundled.
- Failed, skipped, and unavailable checks cannot be represented as passes.
- Setup completion never deletes or rewrites installed package files.
- Readiness authorizes only the mapped local workflow and does not authorize sharing,
  publication, merge, or release.

## Verification evidence

Local candidate verification is complete. Hosted pull-request checks and Gate B review
remain pending. No unrun check is represented as passing.

| Check | Status | Evidence |
|---|---|---|
| Review package and Gate A | pass | Contract 1.2 validates at the exact approved digest and records owner approval. |
| Setup-contract validator | pass | Sole normal RUN, separate setup contract, local-persistence profile, YAML assets, fixture links, mappings, routing states, and safety terms pass. |
| Focused pre-read tests | pass | All 19 focused tests pass in the repository environment. |
| Isolated copied-package fixture | pass | Package closure, external YAML state, collision-safe fictional outputs, receipt status logic, and unchanged installation pass deterministically. |
| Complete public unit suite | pass | All 291 tests pass in the repository environment. |
| Public skill-package validator | pass | Validated 26 standalone skills, two plugins, and declared dependencies. |
| Strict governed-document audit | pass | Audited 89 governed Markdown documents with no findings. |
| GitHub Actions validator and read-only security plan | pass | Validated three SHA-pinned least-privilege workflows; plan generation completed without mutation. |
| IP inventory regeneration | pass | Two runs produced 496 records and identical digest `779b9970819671e328b4da0ec92fe4bec6fd261f48ac34c48527d957c3d2445e`. |
| Private-denylist candidate scan | pass | The complete skill package returned zero findings with the run-specific private denylist. |
| Manual non-reversibility review | pass; owner review pending | Candidate paths contain no private terms, authoring paths, copied mapping, real receipt, or reversible alias. |
| Diff-to-approved-manifest check | pass | Exactly the approved twenty-one paths changed; retained editorial and discovery artifacts remain unchanged where required. |
| Hosted pull-request checks | not run | Required after the pull request opens. |

## Residual risk

Automated scanning cannot prove that prose and paths are independently conceived, so human
comparison remains required. The deterministic fixture proves file behavior and status
logic, not editorial judgment for every real draft or actual AI reference loading. The
fictional receipt proves schema coherence, not historical production use.

The skill may process confidential drafts in an adopter-authorized workspace. Users remain
responsible for safe paths, state protection, and review before sharing.

## Publication conditions

- Complete every applicable local and hosted check or state the exact limitation.
- Keep this review and v1.2 requirements Draft through exact-revision review.
- Do not add private examples, live locators, populated mappings, credentials, real receipts,
  or an alias map.
- Perform a new review before adding retrieval, connectors, hosted services, external writes,
  real-company examples, binaries, or background processes.
- Require Gate B project-owner approval before merge or release.

This is a repository-content review, not legal advice.
