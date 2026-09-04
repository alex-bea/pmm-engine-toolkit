# Fictional HarborKey onboarding state

Status: Complete — example only

Every organization, person, source, event, and value in this file is invented.

| Field | Value |
|---|---|
| Market ID | harborkey-embedded-wallets |
| Scope type | product |
| Product | HarborKey Wallet Platform |
| Geography | not-applicable |
| Started | 2026-08-31T15:00:00Z |
| Last updated | 2026-09-01T11:30:00Z |
| Current stage | enrichment |
| Next action | Ask the fictional PMM to verify AsterPort's proposed migration guide before the next run |

## Setup checklist

- [x] Market scope and exclusions recorded
- [x] Adopter homepage recorded
- [x] Competitor names and homepages recorded
- [x] Competitor source candidates proposed
- [x] Verified sources and reviewed `not found` results saved to `source-map.md`
- [x] Available internal-source metadata inspected
- [x] Internal source suggestions reviewed by the adopter
- [x] Other sources requested from the adopter
- [x] Adopter positioning drafted from approved sources
- [x] Adopter positioning approved
- [x] First baseline draft completed
- [x] Coverage limitations explained
- [x] Highest-value next source proposed

## Pending competitor-source candidates

This candidate is intentionally absent from `source-map.md` until the fictional PMM verifies
it.

| Competitor | Type | Candidate URL | Discovered from | Why it matters | Official confidence | Decision |
|---|---|---|---|---|---|---|
| AsterPort | migration guide | `https://asterport.example.invalid/migrate/` | Product-page navigation | Could show whether AsterPort supports incumbent replacement and account export | medium | pending |

## Internal-source suggestions

The fictional agent inspected names, descriptions, owners, folders, and modified dates only.
It did not read message or document contents before the access decisions below.

| System | Candidate | Metadata used | Why suggested | Content-access decision |
|---|---|---|---|---|
| Slack | `#wallet-product-feedback` | Name and description | Likely product limitations and developer feedback | approved for baseline window |
| Slack | `#wallet-evaluations` | Name and description | Likely competitor and pricing comparisons | approved for baseline window |
| Slack | `#wallet-migrations` | Name and description | Likely switching and key-portability questions | approved for baseline window |
| Drive | `HarborKey Product Narrative` | Title, owner role, modified date | Likely audience, category, and differentiation | approved |
| Drive | `HarborKey Wallet Priorities` | Title, owner role, modified date | Likely comparison priorities and content holds | approved |
| Drive | `HarborKey Proof Library` | Title, folder, modified date | Likely support for claim review | approved |

When asked about other sources, the PMM approved one fictional local evaluation-notes folder
and one fictional developer forum. Both are recorded in `source-map.md`.

## Positioning review

| Draft path | Status | Reviewer | Reviewed | Approved source-map version | Remaining gaps |
|---|---|---|---|---|---|
| `adopter-positioning.md` | approved | Fictional HarborKey PMM | 2026-08-31T15:50:00Z | 2026-08-31T15:25:00Z | Migration-time claim and enterprise-scale proof remain unsupported |

## Baseline and enrichment

| Baseline status | Coverage status | Briefing | Highest-value source to add next | Reason |
|---|---|---|---|---|
| draft complete; review pending | limited | `draft-briefing.md` | AsterPort migration guide | Would test whether its integrated-platform narrative includes a credible switching path |
