# Fictional run record

Status: in progress — example only; baseline draft complete and awaiting review

| Field | Value |
|---|---|
| Run ID | fictional-devtools-us-2026-08-26 |
| Market | fictional-devtools-us |
| Mode | baseline |
| Window | 2026-06-01 through 2026-08-26 (exclusive end) |
| Started | 2026-08-26T09:00:00Z |
| Last updated | 2026-08-26T10:15:00Z |
| Operator | Fictional analyst agent |
| Output directory | `/example/fictional-company/competitive-intel/runs/fictional-devtools-us-2026-08-26/` |
| Current stage | draft-review |
| Coverage status | limited |

## Inputs loaded

- Onboarding state: `onboarding-state.md`, setup gates complete 2026-08-26
- Market pack: `market-pack.yaml`
- Verified source map: `source-map.md`, approved 2026-08-26
- Approved adopter positioning: `adopter-positioning.md`, approved 2026-08-26
- Competitor registry: starter roster from `market-pack.yaml`; proposed baseline is
  `competitor-registry.md`
- Comparative positioning context: none at start; proposed baseline is
  `positioning-context.md`
- Stakeholder lens: `stakeholder-lens.yaml`, example only
- Optional downstream inputs: one fictional approved local evaluation-note folder

## Stage history

| Stage | Started | Completed | Artifact | Review/decision | Notes |
|---|---|---|---|---|---|
| configure | 09:00Z | 09:05Z | input files above | n/a | Verified source map and approved adopter positioning loaded |
| collect | 09:05Z | 09:50Z | `evidence-log.md` | pending | Full roster checked; Northstar source coverage limited |
| evidence-review | 09:50Z | 10:00Z | `evidence-log.md` | approved by Fictional PMM | E-001 through E-006 and E-008 accepted; E-007 rejected |
| synthesize | 10:00Z | 10:15Z | briefing, registry, positioning, and trackers | n/a | Limited baseline draft prepared |
| draft-review | 10:15Z | — | `draft-briefing.md` and proposed state files | pending | Stop before local apply |

## Next action

Review the exact briefing and proposed registry, comparative positioning, and tracker files.
If approved without changes, apply those local files and record the counts. The proposed
BluePeak customer-stories source remains outside the canonical source map until the PMM
verifies it.
