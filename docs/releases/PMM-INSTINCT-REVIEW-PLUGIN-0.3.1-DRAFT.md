---
doc_type: DOC
normative: false
requires:
  - ../../plugins/pmm-instinct-review/skills/pmm-instinct-review/references/DOC-product-requirements.md
  - ../../plugins/pmm-instinct-review/skills/pmm-instinct-review/references/RUN-workflow.md
  - ../legal/IP-PRIVACY-REVIEW-PMM-INSTINCT-REVIEW-0.3.1-2026-09-11.md
status: Draft
version: "0.3.1"
owner: toolkit-maintainers
consumers:
  - plugin adopters
  - public toolkit maintainers
change_control: Pull request review
---

# PMM Instinct Review plugin `0.3.1` — draft release notes

Status: locally verified implementation candidate. The approved review package authorizes a
narrow private-PMM-Engine-Codex parity slice. Focused tests, repository validation, security
scans, and exact inventory regeneration are recorded below. The native Codex lifecycle smoke
was not run. Hosted checks passed on PR #17 for implementation commit `90d5177`; project-owner
final review remains pending before merge or release. This Draft does not authorize either
action.

## Changed for Codex

- First successful enablement requires a non-empty exact `--model` unless one is already
  persisted. The normalized identifier is stored before capture becomes enabled.
- New SessionEnd and backfill jobs use only the persisted extractor model. Session metadata is
  not fallback model authority.
- A legacy enabled/null-model store returns `skipped` / `unconfigured_model` without creating
  normalized evidence, an audit, or a queue job; preflight reports `model_policy: false`.
  Repair forces capture off until executable/schema/model preflight succeeds.
- Adopter-owned `run_routes` can identify one exact safe relative `references/RUN-*.md` file.
- `voice_ref_routes` retains the existing string form and also accepts an ordered non-empty
  list of safe relative `references/REF-*.md` files.
- Route resolution validates filename family, file type, writability, canonical containment in
  the independently discovered source-skill root, and exclusion from installed-package/plugin
  cache paths.
- Multiple valid RUN or REF paths return `applicable: false`, reason
  `multiple-eligible-targets`, and exact `eligible_targets`. An applicable preview requires an
  exact recomputed `promote --target` selection; the runtime never chooses the first path.

## Preserved behavior

Consent, eligible-session filtering, evidence minimization/redaction, detached extraction,
queue recovery, human candidate review, duplicate checks, separate promotion confirmation,
staged Codex writes, portable isolation, and uninstall state preservation remain in scope for
regression protection. Native Claude extraction remains tool-disabled. Codex extraction
remains ephemeral, read-only, schema-bound, and prompt-prohibited from tool use; it does not
claim technical tool unavailability.

Native Claude scripts, hooks, state, extraction, review, immutable promotion receipts/outcomes,
governed patch delivery, installation, and uninstall behavior are unchanged apart from shared
package/version documentation.

## Compatibility

Existing explicit-model queue jobs remain drainable. Existing string-valued voice routes
remain valid. Missing `run_routes` is treated as an in-memory empty map; unambiguous dynamic
RUN discovery remains available. Read-only operations do not rewrite `0.3.0`-shape state.
Legacy null-model state is preserved and receives actionable remediation rather than an
implicit model.

## Non-goals

This candidate does not publish a private model, registry, route map, repository identity, or
runtime record. It does not redesign Codex capture, migrate old state, add telemetry or a
hosted service, automate approval, merge, or publication. It does not give Codex the private
Claude receipt-bound transaction architecture; the parity claim is limited to private Codex
model authority and routing outcomes.

## Verification status

| Check | Candidate result |
|---|---|
| Focused Codex model/routing suite | Pass: included in 80 passing Codex/portable tests |
| Existing Codex and portable regression suite | Pass: 80 tests |
| Native Claude non-regression suite | Pass: 79 tests |
| Complete repository unit suite | Pass: 266 tests |
| Syntax compilation and skill-pack validator | Pass: compileall; 25 standalone skills and two plugins validated |
| Governed-document and package-link validation | Pass: 65 governed documents with no findings; nested skill valid |
| Exact approved-manifest comparison | Pass: 29 modifications and five additions; no extra path |
| IP inventory regeneration/exact-set check | Pass: 448 artifacts; repeat generation is identical |
| Changed-set private-term, path, and narrative review | Pass: scanner clean; independent reviews found no remaining actionable issue |
| Tracked-tree Gitleaks scan | Pass: Gitleaks 8.30.1, zero findings; adjacent exact JSON report is `[]` |
| Native Codex smoke | Not run: no separately authorized isolated hook lifecycle and adopter-selected smoke model were used in this workspace |
| Hosted pull-request checks | Pass on PR #17 at `90d5177`: CodeQL, dependency review, governance, and Python 3.10–3.14 |
| Project-owner final review | Pending |

An unavailable, skipped, stale, or failing required check blocks a release-readiness claim.
This document does not authorize merge, tagging, publication, or installation into production
workflows.
