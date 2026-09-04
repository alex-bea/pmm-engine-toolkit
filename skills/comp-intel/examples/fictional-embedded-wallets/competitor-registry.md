# Fictional HarborKey competitor registry — proposed baseline

Status: Draft — pending exact-draft review; example only

Market: `harborkey-embedded-wallets`

Owner: Fictional HarborKey PMM

Prepared: 2026-09-01T11:30:00Z

Every organization, product, event, source, and value is invented. This file demonstrates the
depth of a durable registry without reproducing a real registry row.

## Status policy

- `active`: verified material signal or live evaluation in the last 30 days
- `monitor`: direct competitor with no material signal in the last 30 days
- `watchlist`: adjacent provider with a named expansion or evaluation trigger
- `dormant`: no material signal or continuing market relevance in the last 180 days

## Roster

| Competitor | Product area | Core claim | Primary audience | Strengths | Weaknesses or constraints | Pricing | Ownership/partners | Status | Last verified |
|---|---|---|---|---|---|---|---|---|---|
| AsterPort | Embedded wallets plus transfers | “Wallets and money movement in one platform” (E-002) | Application developers and commerce platforms | Integrated payments distribution; new transfer controls (E-001, E-002) | Migration and account-export path not documented | Free sandbox; Growth 0.04 fictional units per active wallet; enterprise custom (E-004) | Acquired by fictional SummitPay (E-002) | active | 2026-08-31 |
| BrindleAuth | Wallet identity and administration | “Institutional controls without onboarding friction” (E-005) | Fintech and enterprise application teams | Administrative controls and institutional-owner distribution (E-005, E-006) | Public pricing and one internal quote do not reconcile (E-007, E-015) | Launch 249 fictional units monthly; enterprise custom (E-007) | Acquired by fictional Ironclad Systems (E-006) | active | 2026-08-31 |
| CinderKey | Authentication-led embedded wallets | “Wallet authentication that keeps working” (CK-WEB-01) | Consumer application developers | Long-lived authentication and recovery documentation (E-008) | No changelog or release archive; one isolated recovery complaint (E-016) | Developer free; Team 99 fictional units monthly (E-023) | Independent fictional provider | monitor | 2026-08-31 |
| Dovetail Wallets | Conversion-led wallet onboarding | “Turn sign-in into wallet activation” (E-009) | Product-led application teams | Streamlined onboarding and clear public packaging (E-009, E-022) | Enterprise policy and export controls are unclear | Growth 179 fictional units monthly plus usage (E-022) | Independent fictional provider | monitor | 2026-08-31 |
| EmberPass | Programmable wallets for automated commerce | “Programmable wallets for automated commerce” (E-010) | Fintech builders and software-agent platforms | Spending policies, transfer orchestration, and active SDK releases (E-011, E-018) | Customer adoption and production scale are unproven | Starter 200 fictional units monthly; Growth 600 plus transaction usage (E-024) | Rebranded from fictional Hearth Accounts (E-010) | active | 2026-08-31 |
| FableAccount | Smart-account and signing infrastructure | “Programmable account infrastructure” (E-025) | Infrastructure developers | Low-level signing, policy modules, and public repository activity (E-012, E-025) | No end-user authentication layer or public pricing | No public pricing found (FA-WEB-03) | Independent fictional provider | watchlist | 2026-08-31 |

## Current narrative

| Competitor | Headline/category | Audience | Main proof | CTA | Last changed | Evidence |
|---|---|---|---|---|---|---|
| AsterPort | Wallets and money movement in one platform | Commerce application teams | Transfer-policy release | Start building | 2026-08-24 | E-001, E-002, E-003 |
| BrindleAuth | Institutional controls without onboarding friction | Fintech and enterprise teams | New owner and administrative-control documentation | Request access | 2026-07-18 | E-005, E-006 |
| CinderKey | Wallet authentication that keeps working | Consumer application developers | Recovery documentation | Read the docs | stable in window | CK-WEB-01, E-008 |
| Dovetail Wallets | Turn sign-in into wallet activation | Product-led application teams | Public onboarding flow and pricing | Start free | stable in window | E-009, E-022 |
| EmberPass | Programmable wallets for automated commerce | Fintech and software-agent builders | Rebrand plus spending-policy launch | Explore the platform | 2026-08-28 | E-010, E-011, E-018 |
| FableAccount | Programmable account infrastructure | Wallet infrastructure developers | Public policy-module release | View repository | 2026-08-20 | E-012, E-025 |

## Extended profile: AsterPort

### Why this competitor matters

AsterPort is a direct wallet-onboarding competitor whose fictional owner gives it adjacent
payments distribution. Its move toward transfer controls contests HarborKey's claim that one
policy layer should span onboarding and transaction execution.

### Product and capabilities

- Provides hosted authentication, embedded account creation, recovery, and transfer controls
  (E-001, AP-WEB-02, AP-WEB-07).
- The 2026-08-24 release added per-session transfer limits and approval rules (E-001).

### Go-to-market and audience

- Leads with commerce application teams and the ability to add wallets inside an existing
  fictional SummitPay account (E-002).
- Uses owner distribution as part of its integrated-platform story; adoption impact is unknown.

### Pricing and packaging

- Publishes a sandbox tier and usage-priced Growth plan; enterprise discounts and support fees
  are not disclosed (E-004).

### Known evaluation context

- One approved internal report says a fictional evaluator preferred AsterPort's existing
  payments relationship but asked about account export (E-013, internal, unconfirmed).
- A separate migration discussion describes key-transfer uncertainty; it is not a measured
  implementation outcome (E-014, internal, unconfirmed).

### Watch items

- Publication of the pending migration guide, account-export support, or a bundled payments
  discount.

### Open questions

- Can an existing deployment migrate keys and user identities without account recreation?
- Are transfer controls available in the published Growth price?

### Sources

- E-001 through E-004, E-013, and E-014; AP-WEB-01 through AP-WEB-09.

## Extended profile: BrindleAuth

### Why this competitor matters

BrindleAuth is a direct enterprise competitor whose acquisition adds institutional security
distribution and changes its buyer story.

### Product and capabilities

- Combines wallet onboarding, identity checks, administrative roles, and transaction review
  controls (E-005, BA-WEB-02, BA-WEB-07).

### Go-to-market and audience

- Reframed from a developer-first product toward fintech and enterprise teams after its
  fictional acquisition (E-005, E-006).

### Pricing and packaging

- The public Launch plan is 249 fictional units monthly; one internal report describes a much
  larger quote, which may include enterprise services (E-007, E-015). Treat the two as
  unresolved rather than contradictory list prices.

### Known evaluation context

- E-015 is an approved internal attributed report, not a public pricing claim or confirmed loss.

### Watch items

- Bundled security pricing, owner-led cross-sell, and new enterprise compliance proof.

### Open questions

- Which administrative controls require an enterprise contract?
- Does the fictional owner bundle BrindleAuth with its security platform?

### Sources

- E-005 through E-007 and E-015; BA-WEB-01 through BA-WEB-09.

## Extended profile: CinderKey

### Why this competitor matters

CinderKey represents the established authentication-and-recovery benchmark for consumer
application teams.

### Product and capabilities

- Public documentation covers authentication recovery and account restoration (E-008).

### Go-to-market and audience

- Maintains a reliability-led developer message with no verified narrative change in-window.

### Pricing and packaging

- Publishes a free Developer tier and a 99-fictional-unit Team tier (E-023).

### Known evaluation context

- One community report describes a recovery failure after an SDK update (E-016). It remains an
  isolated attributed report and cannot establish general reliability.

### Watch items

- A dated release surface, migration complaints, or new enterprise positioning.

### Open questions

- How frequently is the SDK updated when no changelog or release archive is published?

### Sources

- E-008, E-016, E-023; CK-WEB-01 through CK-WEB-09.

## Extended profile: Dovetail Wallets

### Why this competitor matters

Dovetail is a direct onboarding competitor for product-led teams that prioritize conversion
and transparent entry pricing.

### Product and capabilities

- Public product material describes configurable sign-in and embedded account activation
  (E-009, DW-WEB-02, DW-WEB-07).

### Go-to-market and audience

- Leads with onboarding conversion and a self-service motion; the message remained stable in
  the baseline window (E-009).

### Pricing and packaging

- Publishes a 179-fictional-unit Growth plan plus active-wallet usage (E-022).

### Known evaluation context

- No approved internal evaluation record was found in the baseline window.

### Watch items

- Enterprise policy controls, public account export, or a shift from conversion to platform
  consolidation.

### Open questions

- Does Dovetail support one policy model across authentication and transaction execution?

### Sources

- E-009, E-022; DW-WEB-01 through DW-WEB-09.

## Extended profile: EmberPass

### Why this competitor matters

EmberPass is a direct wallet competitor expanding into automated money movement, the same
future category direction HarborKey has not yet approved for public use.

### Product and capabilities

- Public material describes programmable spending policies, delegated sessions, transfers,
  and an actively released SDK (E-011, E-018, EP-WEB-05 through EP-WEB-08).

### Go-to-market and audience

- Rebranded from a general embedded-account product to a fintech and automated-commerce
  platform (E-010).

### Pricing and packaging

- Publishes Starter and Growth tiers plus transaction usage; enterprise minimums remain
  unclear (E-024).

### Known evaluation context

- No approved internal record establishes that the new automated-commerce position has changed
  a buying decision.

### Watch items

- Customer proof, settlement partners, spending-policy adoption, and enterprise minimums.

### Open questions

- Are the new policy controls generally available or selectively enabled?
- Does the rebrand represent shipped platform breadth or primarily new messaging?

### Sources

- E-010, E-011, E-018, E-024; EP-WEB-01 through EP-WEB-09.

## Extended profile: FableAccount

### Why this competitor matters

FableAccount is a lower-level infrastructure provider rather than a complete onboarding
product. It becomes a direct threat only if it adds end-user authentication or is repeatedly
selected as the account layer in HarborKey evaluations.

### Product and capabilities

- Publishes signing, policy-module, and smart-account infrastructure with an active fictional
  repository (E-012, E-025).

### Go-to-market and audience

- Targets infrastructure developers rather than product teams seeking a full onboarding stack
  (E-025).

### Pricing and packaging

- No public pricing was found after the documented search in FA-WEB-03.

### Known evaluation context

- One local evaluation note asks whether FableAccount plus a separate authentication vendor
  would offer more control (E-026, internal, unconfirmed).

### Watch items

- Authentication, recovery UI, managed sponsorship, or repeated appearance in full-stack
  evaluations.

### Open questions

- What operational work remains for teams combining FableAccount with separate authentication?

### Sources

- E-012, E-025, E-026; FA-WEB-01 through FA-WEB-09.

## Segment or buyer map

| Segment or buyer | Competitors most relevant | Why | Comparison criteria | Last reviewed |
|---|---|---|---|---|
| Product-led consumer applications | CinderKey, Dovetail Wallets, AsterPort | Prioritize fast onboarding and self-service pricing | Conversion, recovery, active-wallet pricing, export | 2026-09-01 |
| Fintech and enterprise platforms | BrindleAuth, EmberPass, AsterPort | Need administrative controls, support, and money-movement context | Policy continuity, compliance proof, support, transaction pricing | 2026-09-01 |
| Infrastructure-first engineering teams | FableAccount, HarborKey, EmberPass | Need programmable accounts and control over execution | Signing model, policy modules, portability, integration work | 2026-09-01 |
| Incumbent replacement projects | AsterPort, CinderKey, Dovetail Wallets | Switching risk depends on identity and key migration | Migration path, export, recovery continuity, implementation proof | 2026-09-01 |

## Update log

The rows below are proposed and remain unapplied until draft review.

| Date | Competitor | Field | Prior value | New value | Evidence | Run | Reviewer |
|---|---|---|---|---|---|---|---|
| 2026-09-01 | AsterPort | Core claim | Not established | Wallets and money movement in one platform | E-002 | harborkey-wallets-2026-09-01 | pending |
| 2026-09-01 | BrindleAuth | Ownership and audience | Not established | Ironclad-owned; fintech and enterprise audience | E-005, E-006 | harborkey-wallets-2026-09-01 | pending |
| 2026-09-01 | EmberPass | Brand and current narrative | Former brand unknown | EmberPass; programmable wallets for automated commerce | E-010 | harborkey-wallets-2026-09-01 | pending |
| 2026-09-01 | FableAccount | Status | Unclassified | watchlist | E-012, E-025, E-026 | harborkey-wallets-2026-09-01 | pending |
