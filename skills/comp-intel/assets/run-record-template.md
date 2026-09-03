# Competitive-intelligence run record

Status: in progress

| Field | Value |
|---|---|
| Run ID | `[stable run ID]` |
| Market | `[market ID]` |
| Mode | `[baseline / standard / collection-only / resume]` |
| Window | `[inclusive start]` through `[exclusive end]` |
| Started | `[timestamp]` |
| Last updated | `[timestamp]` |
| Operator | `[person or agent session]` |
| Output directory | `[adopter-owned path]` |
| Current stage | `[configure / collect / evidence-review / synthesize / draft-review / apply / complete / blocked]` |

## Inputs loaded

- Market pack: `[path + version/date]`
- Source map: `[path + version/date]`
- Competitor registry: `[path + version/date]`
- Positioning context: `[path + version/date or not provided]`
- Stakeholder lens: `[path + version/date or not provided]`
- Optional downstream inputs: `[paths or not provided]`

## Source capabilities

| Source | Required? | Available? | Last attempted | Limitation |
|---|---|---|---|---|
| `[source ID]` | `[yes/no]` | `[yes/no/partial]` | `[timestamp]` | `[details]` |

## Stage history

| Stage | Started | Completed | Artifact | Review/decision | Notes |
|---|---|---|---|---|---|
| configure | `[time]` | `[time]` | `[paths]` | n/a | `[notes]` |
| collect | `[time]` | `[time]` | `evidence-log.md` | pending | `[notes]` |

## Current blocker or next action

`[Exact blocker, owner, and safe next action. If unblocked, state the next stage.]`

## Integrity notes

Record hashes or version identifiers when the adopter needs exact-artifact binding. If any
reviewed artifact changes, mark the relevant review stale and repeat it.

