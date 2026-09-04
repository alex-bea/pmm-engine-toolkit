---
doc_type: DOC
normative: false
requires:
  - ../../plugins/pmm-instinct-review/skills/pmm-instinct-review/references/DOC-product-requirements.md
  - ../../plugins/pmm-instinct-review/skills/pmm-instinct-review/references/RUN-workflow.md
status: Draft
version: "0.2.0"
owner: toolkit-maintainers
consumers:
  - plugin adopters
  - public toolkit maintainers
change_control: Pull request review
---

# PMM Instinct Review plugin `0.2.0` — draft release notes

Status: unmerged release candidate pending pull-request review.

## Added

- An explicit portable review-only adapter for Codex, Claude Code, or another local work
  agent. It requires an isolated state root and supports candidate import, status, priority,
  review, and cleanup without native-agent state access.
- Complete reusable configuration, state, instinct, status, bucket, card, installation, and
  promotion contracts.
- A full fictional Northstar Reports lifecycle connecting consent, minimized evidence,
  extraction, ranking, both human gates, and terminal guidance state.
- An explicit priority-snapshot command and stale active-instinct reporting.

## Changed

- Ranking is voice-first and includes support, source-skill breadth, repository/cwd breadth,
  newness, and recency.
- Exact matching now requires candidate type plus normalized rule.
- Instincts record source runtime, correction/contradiction state, suggested destination, and
  promotion outcome. The correction confidence bonus is explicit rather than inferred.
- Successful and already-covered promotions become terminal and leave the default queue.
- Product, implementation, workflow, and submission documents use governed Draft metadata.

## Preserved safeguards

The release retains disabled-by-default consent, partial-capture repair, linear context-wrapper
parsing, exact-model read-only extraction, atomic queue records, interrupted-job recovery,
multi-candidate evidence retention, preview signatures, plugin-cache refusal, staged
multi-target writes, and state preservation on disable/removal.

## Compatibility and non-goals

Existing `0.1.0` state loads with conservative in-memory defaults and is not rewritten by
status or priority listing. Codex commands remain available. This release does not add Claude
Code capture, private desktop hooks, hosted storage, telemetry, automatic decisions, merging,
tagging, or publishing.

## Verification evidence

| Check | Local result |
|---|---|
| `python3 -m unittest tests.test_instinct_review_plugin` | 57 tests passed |
| `.venv/bin/python -m unittest discover -s tests` | 144 tests passed; all three workflow checks passed |
| `python3 scripts/governance/validate_skill_pack.py` | 25 standalone skills and two plugins validated |
| Strict governed-document audit | 46 governed Markdown documents; no findings |
| Publicizer scan with run-specific external denylist | `CLEAN` for the complete plugin candidate |
| Gitleaks 8.30.1 full working-tree scan | 0 findings |
| IP inventory | 369 artifacts; exact-set check passed |
| `git diff --check origin/main` | Passed |
| Approved-manifest comparison | 42 approved paths, 42 changed paths, none missing or unexpected |

The host's unpinned system Python initially lacked PyYAML, so four unrelated test modules
could not import. The repository's hash-pinned dependencies were installed into its ignored
virtual environment and the complete 144-test suite then passed. Hosted pull-request checks
have not run yet and remain required. Companion Draft legal/security evidence records the
privacy, rights, and scanning basis. An unavailable or skipped check blocks a release-
readiness claim.
