# Fictional HarborKey competitive-intelligence run record

Status: in progress — example only; baseline draft complete and awaiting review

| Field | Value |
|---|---|
| Run ID | harborkey-wallets-2026-09-01 |
| Market | harborkey-embedded-wallets |
| Mode | baseline |
| Window | 2026-05-01 through 2026-09-01 (exclusive end) |
| Started | 2026-09-01T09:00:00Z |
| Last updated | 2026-09-01T11:30:00Z |
| Operator | Fictional analyst agent |
| Output directory | `workspace://harborkey/competitive-intel/runs/harborkey-wallets-2026-09-01/` |
| Current stage | draft-review |
| Coverage status | limited |

Every person, path, source, event, and value in this record is fictional.

## Inputs loaded

- Onboarding state: `onboarding-state.md`, setup gates complete 2026-08-31T15:50:00Z
- Market pack: `market-pack.yaml`, version 1.0.0
- Verified source map: `source-map.md`, approved 2026-08-31T15:25:00Z
- Approved adopter positioning: `adopter-positioning.md`, approved by Fictional HarborKey PMM
  2026-08-31T15:50:00Z
- Competitor registry: starter roster from `market-pack.yaml`; proposed baseline is
  `competitor-registry.md`
- Comparative positioning context: none at start; proposed baseline is
  `positioning-context.md`
- Stakeholder lens: `stakeholder-lens.yaml`, approved fictional role-based lens
- Optional downstream inputs: three approved fictional Slack channels, three fictional Drive
  documents, one local evaluation-note file, and one developer forum

## Source capabilities

| Source | Required? | Available? | Last attempted | Limitation |
|---|---|---|---|---|
| verified-public-web | yes | partial | 2026-09-01T10:20:00Z | All homepages available; some pricing, changelog, release, and repository sources not found |
| approved-internal-slack | no | yes | 2026-09-01T09:45:00Z | Approved channels and baseline window only; reports remain internal |
| approved-drive-context | no | yes | 2026-08-31T15:40:00Z | Three approved documents; one contains confidential future direction |
| approved-local-notes | no | yes | 2026-09-01T09:50:00Z | One fictional file; not a system of record |
| approved-community | no | partial | 2026-09-01T10:10:00Z | Isolated reports remain attributed |

## Stage history

| Stage | Started | Completed | Artifact | Review/decision | Notes |
|---|---|---|---|---|---|
| configure | 2026-09-01T09:00:00Z | 2026-09-01T09:10:00Z | market, source, positioning, and lens files | n/a | Verified source map and approved adopter positioning loaded |
| collect | 2026-09-01T09:10:00Z | 2026-09-01T10:40:00Z | `evidence-log.md` | pending | Full roster and approved sources checked; missing surfaces recorded |
| evidence-review | 2026-09-01T10:45:00Z | 2026-09-01T11:00:00Z | `evidence-log.md` | approved by Fictional HarborKey PMM | Accepted, rejected, duplicate, out-of-window, superseded, conflicting, and restricted records resolved |
| synthesize | 2026-09-01T11:00:00Z | 2026-09-01T11:30:00Z | briefing, registry, positioning, and trackers | n/a | Two executive signals and limited baseline draft prepared |
| draft-review | 2026-09-01T11:30:00Z | — | `draft-briefing.md` and proposed state files | pending | Stop before local apply |

## Current blocker or next action

The fictional PMM must review the exact briefing, registry, comparative positioning, and
tracker changes. If approved, apply only those local files and record the change counts. The
proposed AsterPort migration guide remains unavailable until separately verified and added to
`source-map.md`.

## Integrity notes

- The source map version predates adopter-positioning approval, which predates collection.
- The evidence review applies only to the evidence set listed in `evidence-log.md`.
- No proposed registry, positioning, or tracker change has been applied.
- Any change to an approved input makes dependent review records stale.
