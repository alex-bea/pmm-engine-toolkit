# Public Skill Catalog

The categories are mutually exclusive by each skill's primary job.

## Portfolio planning and workflow design

- `pm-prioritizer` — reduce a plan to an MVP and explicit deferred scope.
- `pmm-em-tracker` — maintain local roadmap, epic, and task state.
- `pmm-plan-scaffolder` — turn an accepted idea into a governed plan.
- `pmm-plan-auditor` — find drift between plans and tracker state.
- `pmm-launch-scaffolder` — create a complete launch workspace.

## Personal execution and reporting

- `daily-starter` — build a focused daily brief from local inputs.
- `manage-up` — prepare an evidence-based manager update.
- `pmm-habits` — turn weekly evidence into behavior changes.
- `notes-weekly-team-comms` — transform notes into weekly communications.
- `status-update` — summarize accomplishments and active work.

## Intelligence and analysis

- `people-intelligence` — create consented stakeholder briefs.
- `comp-intel` — synthesize sourced competitive signals.
- `pmm-weekly-impact` — connect shipped work to outcomes and next bets.

## Marketing and sales drafting or review

- `guidance-review` — check copy against a supplied claims guide.
- `linkedin-ghostwriter` — draft from consented voice profiles and sources.
- `marketing-brief` — create an evidence-bound marketing brief.
- `pre-read-sharpener` — make an executive pre-read decision-ready.
- `product-page-copywriter` — draft product and use-case page copy.
- `sales-one-pager` — produce a prospect-facing one-pager.
- `strategic-narrative-coach` — stress-test narrative logic.

## Release and signal operations

- `meeting-notes-scaffolder` — scaffold reusable meeting-note capture.
- `slack-monitor-scaffolder` — scaffold review-first channel monitoring.
- `weekly-summary-promoter` — promote approved summaries into durable artifacts.

## Repository hygiene

- `git-sweep` — inspect and safely clean merged Git worktrees.

## Global workflows

- `pmm-accepted-plan-importer` — import an approved plan into governed local state.

## Installable Codex plugins (draft)

- `pmm-instinct-review` — capture eligible completed Codex sessions locally, extract
  reviewable preferences with a second ephemeral Codex call, and promote only guidance
  approved at both the review and destination gates. It also imports explicit candidate
  JSON from the retired standalone package.

All 25 standalone packages include a `SKILL.md`, `agents/openai.yaml`, a runbook, a reusable asset,
and a synthetic example. Deterministic workflows also include scripts and tests. See the
standards and templates in `docs/` before modifying a package. The plugin follows the
Codex plugin manifest and hook contracts in addition to the bundled-skill contract.
