# Fictional onboarding state

Status: Complete — example only

| Field | Value |
|---|---|
| Market ID | fictional-devtools-us |
| Scope type | product-geography |
| Product | LaunchPad Analytics |
| Geography | United States |
| Started | 2026-08-26T08:30:00Z |
| Last updated | 2026-08-26T09:00:00Z |
| Current stage | complete |
| Next action | Verify the proposed BluePeak customer-stories source before the next run |

## Setup checklist

- [x] Market scope and exclusions recorded
- [x] Adopter homepage recorded
- [x] Competitor names and homepages recorded
- [x] Competitor source candidates proposed
- [x] Verified sources saved to `source-map.md`
- [x] Available internal-source metadata inspected
- [x] Internal source suggestions reviewed by the adopter
- [x] Other sources requested from the adopter
- [x] Adopter positioning drafted from approved sources
- [x] Adopter positioning approved
- [x] First baseline draft completed
- [x] Coverage limitations explained
- [x] Highest-value next source proposed

## Competitor-source verification review

The fictional PMM supplied each homepage. The agent followed homepage navigation and official
site results, then presented these candidates before writing the source map.

| Competitor | Type | Candidate | Discovered from | Official confidence | Decision |
|---|---|---|---|---|---|
| BluePeak | product | `https://bluepeak.example.invalid/product/` | Homepage navigation | high | verified |
| BluePeak | pricing | `https://bluepeak.example.invalid/pricing/` | Homepage navigation | high | verified |
| BluePeak | releases | `https://bluepeak.example.invalid/releases/` | Homepage footer | high | verified |
| BluePeak | docs | `https://docs.bluepeak.example.invalid/` | Homepage navigation | high | verified |
| BluePeak | social | `https://social.example.invalid/bluepeak` | Homepage footer | high | verified |
| BluePeak | customer stories | `https://bluepeak.example.invalid/customers/` | Product-page navigation | high | pending enrichment verification |
| CedarWorks | product, pricing, blog, changelog, docs, social | See `source-map.md` | Homepage navigation and footer | high | verified |
| Northstar Labs | product, blog, social | See `source-map.md` | Homepage navigation and footer | high | verified |

Missing changelog, release, pricing, documentation, or repository sources are recorded as
verified `not found` results in `source-map.md`; no likely URL was invented.

## Internal-source suggestions

The agent used names, descriptions, owners, folders, and modified dates only. It did not read
message or document content before the fictional PMM decided.

| System | Candidate | Metadata used | Why suggested | Decision |
|---|---|---|---|---|
| Slack | `#fictional-product-feedback` | Name and description | Likely product audience and proof context | approved |
| Slack | `#fictional-sales-evaluations` | Name and description | Likely competitor evaluation signals | approved |
| Slack | `#fictional-general` | Name only | Broad company context | declined |
| Drive | `LaunchPad Product Narrative` | Title, owner role, modified date | Likely category, value, and differentiation | approved |
| Drive | `LaunchPad 2026 Priorities` | Title, owner role, modified date | Likely comparison priorities | approved |
| Drive | `LaunchPad Archive Notes` | Title and old modified date | Possible history but likely stale | declined |

When asked about other sources, the PMM also approved a fictional local evaluation-note folder.

## Positioning review

| Draft | Status | Reviewer | Reviewed | Source-map version | Remaining gap |
|---|---|---|---|---|---|
| `adopter-positioning.md` | approved | Fictional individual PMM | 2026-08-26 | 2026-08-26 | Setup-speed claim lacks public proof |

## Baseline and enrichment

| Baseline | Coverage | Briefing | Highest-value source next | Reason |
|---|---|---|---|---|
| draft complete; review pending | limited | `draft-briefing.md` | BluePeak customer stories | Could establish whether the dashboard has adoption proof |
