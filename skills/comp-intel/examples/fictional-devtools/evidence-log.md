# Fictional evidence log

Run: `fictional-devtools-us-2026-08-26`

Market: `fictional-devtools-us`

Mode: baseline

Window: 2026-06-01 through 2026-08-26 (exclusive end)

Evidence review: approved by Fictional individual PMM on 2026-08-26 at 10:00Z

## Coverage

| Source class | Competitors | Result | Limitation |
|---|---|---|---|
| First-party releases | BluePeak, CedarWorks | complete | Northstar is watchlist and had no trigger |
| Pricing | BluePeak, CedarWorks | complete | Prices are fictional demonstration data |
| Homepage narrative | BluePeak | complete | Prior comparison available only for BluePeak |
| Community | BluePeak, CedarWorks | partial | One isolated user report |
| Authorized local notes | BluePeak | complete | Internal-only; cannot support public output |
| Prior narrative capture | BluePeak | complete | Approved internal artifact; supports comparison but not public quotation |

## Records

| ID | Competitor | Date(s) | Source | Content | Label | Confidence | Sensitivity | Disposition/limitation |
|---|---|---|---|---|---|---|---|---|
| E-001 | BluePeak | published 2026-08-21; observed 2026-08-25 | Fictional first-party release, `https://bluepeak.example.invalid/releases/team-dashboard/` | BluePeak announced a team usage dashboard. | observed | high | public | accepted; release does not prove adoption |
| E-002 | BluePeak | updated 2026-08-21; observed 2026-08-25 | Fictional docs, `https://docs.bluepeak.example.invalid/team-dashboard/` | Documentation describes per-project usage charts and team filters. | observed | high | public | accepted; corroborates E-001, does not establish plan availability |
| E-003 | BluePeak | observed 2026-08-25 | Fictional homepage, `https://bluepeak.example.invalid/` | Headline is now “See what every team ships and uses.” | observed | high | public | accepted; compare with E-008 |
| E-004 | BluePeak | observed 2026-08-25 | Fictional pricing, `https://bluepeak.example.invalid/pricing/` | Free and Team $40/month remain displayed; dashboard entitlement is not stated. | observed | high | public | accepted; package inclusion unknown |
| E-005 | CedarWorks | posted 2026-08-22; observed 2026-08-25 | Fictional community post, `https://forum.example.invalid/t/cedar-limit/42` | One named fictional user reports reaching a CedarWorks usage limit. | attributed report | low | public | accepted with limitation; isolated report, no generalization |
| E-006 | BluePeak | event 2026-08-23; observed 2026-08-25 | Fictional approved local note, `note://evaluations/bluepeak-17` | A fictional evaluator asked whether BluePeak's Team price includes dashboard export. | attributed report | medium | internal | accepted for internal analysis; excluded from public-safe claims |
| E-007 | BluePeak | unknown; observed 2026-08-25 | Fictional search snippet | Snippet says BluePeak is “the market leader.” | attributed report | low | public | rejected; underlying source not reviewed and superlative unsupported |
| E-008 | BluePeak | observed 2026-08-10; reviewed 2026-08-26 | Fictional approved prior capture, `artifact://approved-archive/bluepeak-homepage-2026-08-10` | Prior homepage headline was “Ship without guessing.” | observed | high | internal | accepted for narrative comparison; not approved for external quotation |

## Conflicts and unknowns

- E-001 establishes release; E-004 does not state which plan includes it. Entitlement is
  unknown, not contradictory.
- No evidence establishes customer adoption, export, or role-based access.
- E-005 is a single attributed report and does not establish a general CedarWorks limitation.

## Proposed evidence-review decision

The fictional PMM accepted E-001 through E-006 and E-008 with their labels and restrictions,
and rejected E-007. E-008 may support internal narrative comparison but not external
quotation. Any change to this evidence set requires a new review.
