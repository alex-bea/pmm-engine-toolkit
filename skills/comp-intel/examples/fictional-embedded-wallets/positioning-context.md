# Fictional HarborKey competitive positioning context

Status: Draft — proposed baseline comparison; example only

Market: `harborkey-embedded-wallets`

Owner: Fictional HarborKey PMM

Created: 2026-09-01T11:30:00Z

Upstream adopter position: `adopter-positioning.md`, approved 2026-08-31T15:50:00Z

Every organization, claim, source, and conclusion is fictional. Approval of the upstream
adopter position does not approve the competitor analysis below.

## How to use this file

- **STRONG:** a specific reviewed HarborKey response exists.
- **WEAK:** a relevant response exists but proof, scope, or review is incomplete.
- **MISSING:** no useful response exists; the example proposes a battlecard gap.
- **CONFLICTING:** approved internal positions or reviewed evidence disagree.

Never convert a fictional competitor weakness into a HarborKey strength without an approved
HarborKey claim.

## Adopter claims currently usable

| Claim ID | Claim | Audience/use case | Status | Proof/source | Restrictions | Last reviewed |
|---|---|---|---|---|---|---|
| HK-CL-01 | HarborKey applies one policy model to authentication sessions and transaction permissions. | Platform and security teams | reviewed | HK-SRC-01, HK-SRC-02 | Do not imply reduced incidents | 2026-08-31 |
| HK-CL-02 | HarborKey accounts support documented user-controlled export and recovery. | Applications requiring portability | reviewed | HK-SRC-02 | Integration-specific availability | 2026-08-31 |
| HK-CL-03 | HarborKey combines authentication, smart-account controls, sponsorship, and execution in one SDK. | Application developers | reviewed | HK-SRC-01, HK-SRC-02 | Do not imply every module is mandatory | 2026-08-31 |
| HK-CL-04 | HarborKey will connect wallet execution with settlement orchestration. | Enterprise money movement | hold | HK-SRC-04 | Unannounced future work; never use as a shipped counter | 2026-08-31 |
| HK-CL-05 | A production migration can be completed in five business days. | Incumbent replacement | hold | HK-SRC-05 | Missing repeatable proof | 2026-08-31 |

## Versus AsterPort

### Their primary claim

AsterPort claims to provide wallets and money movement in one platform following its fictional
integration with SummitPay. Evidence: E-002, observed 2026-08-31.

### Where the adopter is strong

- HarborKey has reviewed public support for one policy model spanning authentication sessions
  and transaction permissions (HK-CL-01).
- HarborKey documents user-controlled account export and recovery (HK-CL-02); AsterPort's
  migration and export path remains unverified.

### Where the competitor is strong or the adopter concedes

- AsterPort can lead with an existing fictional payment-platform relationship and newly shipped
  transfer controls (E-001, E-002).
- HarborKey has no approved proof that its migration is faster or easier.

### Reframe

Move the comparison from the number of bundled modules to whether one reviewable policy and
ownership model remains consistent across onboarding, execution, recovery, and exit.

### Useful buyer question

“If you change providers later, how will user identities, account authority, policies, and
recovery paths move without recreating accounts?”

### Missing or weak responses

- `[COUNTER NEEDED]` Produce repeatable migration evidence before making a speed comparison.
- `[DRAFT — NEEDS REVIEW]` Compare published transfer-control scope after plan entitlement is
  confirmed.

### Watch signals

- Verified migration guide, account export, Growth-plan entitlement, or bundled SummitPay price.

### Sources

- E-001 through E-004, E-013, and E-014; public and approved internal evidence with the
  restrictions in `evidence-log.md`.

## Versus BrindleAuth

### Their primary claim

BrindleAuth claims institutional controls without onboarding friction and now frames its
fictional owner as proof of enterprise readiness. Evidence: E-005 and E-006.

### Where the adopter is strong

- HarborKey has a reviewed public account-export claim (HK-CL-02) and a unified SDK claim
  covering both onboarding and execution controls (HK-CL-03).

### Where the competitor is strong or the adopter concedes

- BrindleAuth has a stronger published institutional-owner story and more explicit
  administrative-control documentation (E-005, BA-WEB-07).
- HarborKey lacks approved enterprise-scale or procurement proof.

### Reframe

Separate inherited owner credibility from evidence that the wallet product itself provides the
required controls, portability, support, and operating model.

### Useful buyer question

“Which controls are native to the wallet product, which come from the parent platform, and
which require an enterprise contract?”

### Missing or weak responses

- `[COUNTER NEEDED]` HarborKey needs reviewed enterprise-scale and support evidence.
- `[DRAFT — NEEDS REVIEW]` Public and internal BrindleAuth pricing may describe different
  packages; do not claim a price disadvantage yet.

### Watch signals

- Owner-platform bundles, compliance proof, published service levels, and enterprise pricing.

### Sources

- E-005 through E-007 and E-015; public and approved internal evidence with restrictions.

## Versus EmberPass

### Their primary claim

EmberPass claims programmable wallets for automated commerce after a fictional rebrand and
product launch. Evidence: E-010, E-011, and E-018.

### Where the adopter is strong

- HarborKey can use its reviewed policy-continuity claim for current authentication and
  transaction-permission comparisons (HK-CL-01).
- HarborKey can use its reviewed unified-SDK claim when the buyer needs onboarding and account
  controls together (HK-CL-03).

### Where the competitor is strong or the adopter concedes

- EmberPass has shipped public automated-spending controls and current release evidence
  (E-011, E-018).
- HarborKey's settlement-orchestration direction is on hold and cannot counter a shipped
  competitor capability (HK-CL-04).

### Reframe

Compare the scope, auditability, and lifecycle of current policy controls rather than competing
on an unapproved future category promise.

### Useful buyer question

“Which automated actions can a developer constrain, revoke, audit, and recover today?”

### Missing or weak responses

- `[COUNTER NEEDED]` Review whether HarborKey's current policy model covers each shipped
  EmberPass control.
- `[CONFLICTING]` Internal future direction overlaps EmberPass's current public narrative, but
  the HarborKey language remains on content hold.

### Watch signals

- Customer adoption, settlement partners, production scale, and generally available policy
  controls.

### Sources

- E-010, E-011, E-018, and E-024; public evidence only for current competitor claims.

## Versus CinderKey

### Their primary claim

CinderKey claims reliable wallet authentication and recovery. Evidence: CK-WEB-01 and E-008.

### Where the adopter is strong

- HarborKey's reviewed position covers both authentication and transaction policy, while
  CinderKey's reviewed public material is authentication-led (HK-CL-01, HK-CL-03, E-008).

### Where the competitor is strong or the adopter concedes

- CinderKey has a simple reliability message and established recovery documentation.

### Reframe

Ask whether the team needs authentication alone or one lifecycle across authentication,
account policy, execution, and recovery.

### Useful buyer question

“Will authentication and transaction permissions be managed and audited in the same policy
system?”

### Missing or weak responses

- `[DRAFT — NEEDS REVIEW]` One community complaint cannot support a reliability attack.

### Watch signals

- Dated SDK releases, broad migration reports, or new enterprise policy controls.

### Sources

- E-008, E-016, and E-023; CK-WEB-01 through CK-WEB-09.

## Versus Dovetail Wallets

### Their primary claim

Dovetail claims to turn sign-in into wallet activation for product-led teams. Evidence: E-009.

### Where the adopter is strong

- HarborKey's reviewed comparison can extend beyond onboarding into policy continuity,
  execution, and account export (HK-CL-01 through HK-CL-03).

### Where the competitor is strong or the adopter concedes

- Dovetail publishes simple entry pricing and a focused conversion story (E-009, E-022).

### Reframe

Compare total lifecycle control and portability after activation, not onboarding conversion
alone.

### Useful buyer question

“After a user activates a wallet, what controls, recovery options, and exit paths does your team
need to own?”

### Missing or weak responses

- `[COUNTER NEEDED]` HarborKey has no approved comparative conversion proof.

### Watch signals

- Public conversion studies, enterprise policy controls, or account export.

### Sources

- E-009 and E-022; DW-WEB-01 through DW-WEB-09.

## Versus FableAccount

### Their primary claim

FableAccount claims programmable account infrastructure for infrastructure developers.
Evidence: E-012 and E-025.

### Where the adopter is strong

- HarborKey packages authentication, account controls, sponsorship, and execution in one
  reviewed SDK position (HK-CL-03).

### Where the competitor is strong or the adopter concedes

- FableAccount offers lower-level signing and policy modules with public repository activity
  (E-012).

### Reframe

Compare a complete user onboarding and account lifecycle with the engineering work needed to
assemble separate low-level components.

### Useful buyer question

“Do you want programmable signing primitives, or an operated user-account lifecycle that also
includes authentication, recovery, sponsorship, and support?”

### Missing or weak responses

- `[COUNTER NEEDED]` Quantify the implementation and operating work of a composed stack before
  claiming lower total effort.

### Watch signals

- End-user authentication, managed recovery, hosted sponsorship, or repeated full-stack
  evaluations.

### Sources

- E-012, E-025, and E-026; FA-WEB-01 through FA-WEB-09.

## Global limitations

- All data is fictional and must never be presented as market evidence.
- HarborKey lacks approved enterprise-scale, migration-time, and conversion proof.
- Internal evaluation reports are attributed and unconfirmed, not win/loss conclusions.
- Missing changelog, release, repository, and pricing surfaces limit some competitor histories.
- HK-CL-04 and HK-CL-05 are on hold and cannot support current competitive claims.

## Change log

| Date | Section | Change | Evidence | Reviewer |
|---|---|---|---|---|
| 2026-09-01 | Initial baseline | Proposed six competitor comparisons, three active gaps, two monitored positions, and one watchlist reframe | Reviewed evidence set in `evidence-log.md` | pending exact-draft review |
