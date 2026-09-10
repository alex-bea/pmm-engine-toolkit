---
doc_type: DOC
normative: false
requires:
  - ../../plugins/pmm-instinct-review/skills/pmm-instinct-review/references/DOC-product-requirements.md
  - ../../plugins/pmm-instinct-review/skills/pmm-instinct-review/references/RUN-workflow.md
  - ../../plugins/pmm-instinct-review/skills/pmm-instinct-review/references/RUN-claude-setup.md
status: Draft
version: "0.3.0"
owner: toolkit-maintainers
consumers:
  - plugin adopters
  - public toolkit maintainers
change_control: Pull request review
---

# PMM Instinct Review plugin `0.3.0` — draft release notes

Status: unmerged release candidate with complete local automated verification. A real Claude
Code lifecycle smoke test and pull-request owner review remain required before merge or release.

## Added

- A self-contained native Claude Code runtime with package-relative `SessionStart` and
  `SessionEnd` hooks, a no-marketplace standalone installer, and an optional local-plugin
  manifest.
- Disabled-by-default, user-owned Claude state isolated from Codex state and from the installed
  package.
- Bounded conversation-only normalization, redaction, duplicate-event idempotence, and a
  detached extraction worker that requests the exact configured Claude model, disables tools,
  validates zero-to-five candidates against the bundled schema, and applies bounded retries.
- Bundle-local Claude status, backlog, review, retry, promotion-preview, approval, and worker
  commands.
- Immutable promotion approvals bound to the source guidance, exact target, current target
  digest, proposed result, and preview digest. A background worker may apply an approved local
  result; governed delivery writes a review patch without mutating the target.
- A detailed Claude setup and recovery runbook plus a complete fictional Claude lifecycle
  alongside the existing fictional Codex lifecycle.

## Changed

- The package, catalog, manifests, and governed documents advance from `0.2.0` to `0.3.0` and
  describe Codex, native Claude, and isolated portable modes separately.
- Public privacy and security guidance now covers Claude transcript-derived evidence, Anthropic
  model processing, user-settings hooks, state retention, and the locally bypassable trust
  boundary.
- Repository governance validates the two manifests, separate hook variables, Claude package
  closure, setup runbook, runtime assets, and fictional fixtures.

## Preserved compatibility and safeguards

The existing Codex runtime, marketplace path, state root, capture hooks, portable review-only
adapter, fictional Codex lifecycle, and focused regression suite remain in place. Native
capture is opt-in in both runtimes. Portable mode still cannot capture native sessions or
promote instructions. Review decisions and promotion approvals remain human-only.

## Non-goals

This candidate does not add a Claude marketplace release, hosted service, telemetry, historical
Claude backfill, shared Codex/Claude memory, automatic approval, pull-request creation, merge,
tagging, or external publishing. It does not claim that user-controlled local hooks form a
non-bypassable security boundary.

## Verification status

The table records results from the frozen local candidate. It keeps unavailable and future
checks distinct from passes.

| Check | Candidate result |
|---|---|
| Focused Codex and portable regression suite | Pass: 57 tests |
| Focused public Claude closure and behavior suite | Pass: 79 tests |
| Mirrored private Claude regression suites | Pass: 84 tests; the seven public/private Claude runtime and launcher files are byte-identical |
| Complete repository unit suite | Pass: 235 tests |
| Repository skill-pack validator | Pass: 25 standalone skills, two plugins, and declared dependencies validated |
| Skill-package quick validation | Pass |
| Strict governed-document audit | Pass: 55 governed documents, zero findings |
| GitHub Actions structure, `actionlint`, and `zizmor` | Pass: three workflows validated; no unsuppressed findings |
| Publicizer private-term scan | Pass for the complete plugin; exact-slice findings were limited to five pre-existing unchanged matches in three modified files and were diff-adjudicated |
| Tracked-tree Gitleaks scan | Pass: zero findings with Gitleaks `8.30.1` |
| Generated IP inventory exact-set check | Pass: 427 rows for 427 artifacts |
| Approved-manifest comparison | Pass: 57 of 57 paths, comprising 36 additions and 21 modifications, with no extras or action mismatches |
| Real Claude Code lifecycle smoke test | Not run; this host has no `claude` executable, so the destination-machine test remains required |
| Hosted pull-request checks | Pass: CodeQL, dependency review, governance, and Python 3.10–3.14 tests |

An unavailable, skipped, stale, or failing required check blocks a release-readiness claim.
These local results support pull-request review only; they do not authorize merge or release.
