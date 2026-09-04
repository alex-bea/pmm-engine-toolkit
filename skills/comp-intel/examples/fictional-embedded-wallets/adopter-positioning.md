# Fictional HarborKey product positioning

Status: Approved — example only

Market: `harborkey-embedded-wallets`

Product: HarborKey Wallet Platform

Geography: not-applicable

Owner: Fictional HarborKey PMM

Last reviewed: 2026-08-31T15:50:00Z

Approved source-map version: 2026-08-31T15:25:00Z

Every organization, claim, source, and value in this file is invented. This position is
approved only for the fictional baseline and carries the limitations stated below.

## Source coverage

| Source ID | Source | What it supports | Sensitivity | Limitation |
|---|---|---|---|---|
| HK-SRC-01 | `https://harborkey.example.invalid/` | Audience, problem, category, value | public | Homepage summarizes rather than proves capabilities |
| HK-SRC-02 | `https://docs.harborkey.example.invalid/` | Authentication, policy, and account behavior | public | Documentation does not establish customer outcomes |
| HK-SRC-03 | Fictional Drive file `HarborKey Product Narrative` | Category, differentiation, approved language | internal | Not approved for direct external quotation |
| HK-SRC-04 | Fictional Drive file `HarborKey Wallet Priorities` | Comparison priorities and future direction | confidential | Contains unannounced work; not usable as a current claim |
| HK-SRC-05 | Fictional Drive file `HarborKey Proof Library` | Technical proof and internal evaluation results | internal | Enterprise-scale sample is incomplete |

## Target audiences

| Audience | Job or need | Evidence | Confidence |
|---|---|---|---|
| Application developers | Add user-controlled wallets without building authentication and transaction policy from scratch | HK-SRC-01, HK-SRC-02 | high |
| Platform engineering teams | Apply consistent permissions across accounts, sessions, and sponsored transactions | HK-SRC-02, HK-SRC-03 | high |
| Product and security leaders | Balance onboarding conversion with account ownership, auditability, and recovery | HK-SRC-01, HK-SRC-03, HK-SRC-05 | medium |

## Customer problem

Software teams often assemble authentication, wallet creation, policy controls, recovery, and
transaction execution from separate components. That increases integration work and makes it
harder to apply one reviewable policy model across the user journey.

Evidence: HK-SRC-01, HK-SRC-02, HK-SRC-03.

## Category

Embedded-wallet infrastructure with programmable account and transaction controls.

Evidence: HK-SRC-01, HK-SRC-03.

## Value proposition

HarborKey gives application teams one developer platform for onboarding users, creating
portable accounts, and enforcing permissions from sign-in through transaction execution.

Evidence: HK-SRC-01, HK-SRC-02, HK-SRC-03.

## Differentiators

| Differentiator | Scope | Evidence | Claim status |
|---|---|---|---|
| One policy model covers authentication sessions and transaction permissions | Platform and security teams | HK-SRC-02, HK-SRC-03 | approved |
| Accounts can be exported through a documented user-controlled recovery process | Applications requiring portability | HK-SRC-02 | approved |
| Authentication, account abstraction, sponsorship, and policy controls share one SDK surface | Application developers | HK-SRC-01, HK-SRC-02 | approved |
| A settlement-orchestration connector will extend the platform into treasury workflows | Enterprise money movement | HK-SRC-04 | hold |
| Teams can migrate a production wallet deployment in five business days | Incumbent replacement | HK-SRC-05 | missing-proof |

## Claims and proof points

| Claim ID | Claim | Proof | Source IDs | Publicly usable? | Limitation |
|---|---|---|---|---|---|
| HK-CL-01 | HarborKey applies one policy model to authentication sessions and transaction permissions. | Public documentation describes shared policy objects and audit events. | HK-SRC-01, HK-SRC-02 | yes | Does not prove reduced security incidents |
| HK-CL-02 | HarborKey accounts support documented user-controlled export and recovery. | Public recovery and export documentation. | HK-SRC-02 | yes | Availability varies by integration pattern |
| HK-CL-03 | HarborKey combines authentication, smart-account controls, sponsorship, and execution in one SDK. | Public product and SDK documentation. | HK-SRC-01, HK-SRC-02 | yes | Does not mean every module is required |
| HK-CL-04 | HarborKey will connect wallet execution with settlement orchestration. | Fictional priority document only. | HK-SRC-04 | no | Unannounced future work; content hold |
| HK-CL-05 | A production migration can be completed in five business days. | One incomplete internal exercise. | HK-SRC-05 | no | Sample and repeatable method are missing |

## Comparison criteria

| Criterion | Why it matters to the audience | Adopter evidence | Priority |
|---|---|---|---|
| Policy continuity | Buyers need consistent controls from sign-in through execution | HK-SRC-02, HK-SRC-03 | high |
| Account ownership and export | Teams need a credible answer to vendor lock-in and recovery | HK-SRC-02 | high |
| Migration path | Replacement projects fail when key and identity transitions are unclear | HK-SRC-03, HK-SRC-05 | high |
| Developer integration surface | Multiple SDKs increase implementation and maintenance work | HK-SRC-01, HK-SRC-02 | high |
| Pricing predictability | Buyer comparisons depend on users, signatures, transactions, and support fees | HK-SRC-03 | medium |
| Enterprise controls and proof | Security and procurement teams need audit, availability, and scale evidence | HK-SRC-05 | medium |

## Assumptions and missing proof

- HarborKey has no approved enterprise-scale customer proof in this fictional example.
- The five-day migration statement cannot be used until a repeatable test and sample exist.
- The settlement-orchestration connector is future work and cannot counter a shipped feature.
- Public documentation does not quantify conversion improvement or operating-cost reduction.

## Review record

| Decision | Reviewer | Date | Source-map version | Notes |
|---|---|---|---|---|
| approved | Fictional HarborKey PMM | 2026-08-31T15:50:00Z | 2026-08-31T15:25:00Z | Approved for internal competitive analysis; HK-CL-04 and HK-CL-05 remain unusable externally |
