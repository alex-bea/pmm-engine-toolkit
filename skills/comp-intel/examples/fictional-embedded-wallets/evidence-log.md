# Fictional HarborKey competitive-intelligence evidence log

Run: `harborkey-wallets-2026-09-01`

Market: `harborkey-embedded-wallets`

Mode: baseline

Window: 2026-05-01 through 2026-09-01 (exclusive end)

Evidence review: approved by Fictional HarborKey PMM on 2026-09-01T11:00:00Z

Every organization, source, author, event, quotation, and value is invented. The records model
the information mix of a mature run without reproducing any private evidence.

## Coverage

| Source class | Source IDs | Competitors covered | Result | Limitation |
|---|---|---|---|---|
| Homepage and product | AP-WEB-01 through AP-WEB-02; BA-WEB-01 through BA-WEB-02; CK-WEB-01 through CK-WEB-02; DW-WEB-01 through DW-WEB-02; EP-WEB-01 through EP-WEB-02; FA-WEB-01 through FA-WEB-02 | full roster | complete | Current pages do not establish adoption |
| Pricing | AP-WEB-03, BA-WEB-03, CK-WEB-03, DW-WEB-03, EP-WEB-03, FA-WEB-03 | full roster | partial | FableAccount pricing not found; enterprise terms incomplete |
| Blogs, changelogs, and releases | verified public source map | full roster | partial | CinderKey lacks dated changelog and release surfaces |
| Documentation and repositories | verified public source map | full roster | partial | AsterPort, BrindleAuth, and Dovetail repositories not found |
| Approved Slack | INT-01 through INT-03 | AsterPort, BrindleAuth | complete | Attributed internal reports are not confirmed outcomes |
| Approved local notes | INT-04 | FableAccount | complete | One fictional note; not a system of record |
| Community | COM-01 | CinderKey | partial | One isolated attributed report |
| Official social | AP-WEB-09 through FA-WEB-09 | EmberPass | event-triggered | Used only to enrich an already material launch |

## Evidence records

| ID | Competitor | Date(s) | Source | Content | Label | Confidence | Sensitivity | Disposition/limitation |
|---|---|---|---|---|---|---|---|---|
| E-001 | AsterPort | published 2026-08-24; observed 2026-08-31 | Fictional first-party release, `https://asterport.example.invalid/releases/transfer-policies/` | AsterPort announced per-session transfer limits and approval rules. | observed | high | public | accepted; release does not prove plan entitlement or adoption |
| E-002 | AsterPort | observed 2026-08-31 | Fictional homepage, `https://asterport.example.invalid/` | The homepage says “Wallets and money movement in one platform” and identifies fictional SummitPay ownership. | observed | high | public | accepted; current narrative only |
| E-003 | AsterPort | captured 2026-05-12; reviewed 2026-08-31 | Fictional approved prior capture, `artifact://harborkey-history/asterport-homepage-2026-05-12` | The prior headline was “Wallet onboarding for every app.” | observed | high | internal | accepted for narrative comparison; not for external quotation |
| E-004 | AsterPort | observed 2026-08-31 | Fictional pricing page, `https://asterport.example.invalid/pricing/` | A free sandbox and a Growth plan priced at 0.04 fictional units per active wallet are displayed. | observed | high | public | accepted; enterprise discounts and transfer-control entitlement unknown |
| E-005 | BrindleAuth | observed 2026-08-31 | Fictional homepage, `https://brindleauth.example.invalid/` | The homepage says “Institutional controls without onboarding friction” and leads with enterprise teams. | observed | high | public | accepted; owner credibility is not product proof |
| E-006 | BrindleAuth | published 2026-07-18; observed 2026-08-31 | Fictional acquisition announcement, `https://brindleauth.example.invalid/insights/ironclad-acquisition/` | Fictional Ironclad Systems announced its acquisition of BrindleAuth. | observed | high | public | accepted; commercial integration details unknown |
| E-007 | BrindleAuth | observed 2026-08-31 | Fictional pricing page, `https://brindleauth.example.invalid/pricing/` | The public Launch plan is 249 fictional units monthly and enterprise pricing is custom. | observed | high | public | accepted; compare with internal E-015 without assuming contradiction |
| E-008 | CinderKey | observed 2026-08-31; page undated | Fictional documentation, `https://docs.cinderkey.example.invalid/recovery/` | Documentation describes account restoration after loss of an authentication method. | observed | medium | public | accepted; page date and production adoption unknown |
| E-009 | Dovetail Wallets | observed 2026-08-31 | Fictional homepage, `https://dovetail-wallets.example.invalid/` | The headline remains “Turn sign-in into wallet activation.” | observed | high | public | accepted; no material narrative change in-window |
| E-010 | EmberPass | published 2026-08-28; observed 2026-08-31 | Fictional rebrand announcement, `https://emberpass.example.invalid/journal/introducing-emberpass/` | The provider renamed itself from fictional Hearth Accounts and repositioned around automated commerce. | observed | high | public | accepted; rebrand alone does not establish product breadth |
| E-011 | EmberPass | published 2026-08-28; observed 2026-08-31 | Fictional product release, `https://emberpass.example.invalid/releases/automated-spending/` | EmberPass announced delegated sessions, recipient rules, and spending limits. | observed | high | public | accepted; customer adoption and general availability not established |
| E-012 | FableAccount | released 2026-08-20; observed 2026-08-31 | Fictional repository release, `https://code.example.invalid/fableaccount/sdk/releases/v4/` | Version 4 added composable signing-policy modules. | observed | medium | public | accepted; repository release does not prove hosted-service availability |
| E-013 | AsterPort | message 2026-08-19; reviewed 2026-09-01 | Fictional approved Slack record, `slack://wallet-evaluations/msg-104` | A fictional evaluator reportedly preferred using an existing SummitPay relationship but asked whether accounts could be exported. | attributed report | medium | internal | accepted for internal analysis; evaluation outcome unconfirmed |
| E-014 | AsterPort | message 2026-08-22; reviewed 2026-09-01 | Fictional approved Slack record, `slack://wallet-migrations/msg-227` | A fictional engineer described uncertainty about moving keys and user identities from AsterPort. | attributed report | medium | internal | accepted with attribution; not a measured migration result |
| E-015 | BrindleAuth | message 2026-08-26; reviewed 2026-09-01 | Fictional approved Slack record, `slack://wallet-evaluations/msg-311` | A fictional evaluator reported a 2,400-unit monthly BrindleAuth quote including support and administration. | attributed report | low | internal | accepted but unresolved against E-007; may be a custom package |
| E-016 | CinderKey | posted 2026-08-12; observed 2026-08-31 | Fictional community post, `https://forum.example.invalid/wallet-builders/cinder-recovery-42/` | One fictional user reported a recovery failure after an SDK update. | attributed report | low | public | accepted with limitation; isolated report cannot support a general reliability claim |
| E-017 | AsterPort | date unknown; observed 2026-08-31 | Fictional search snippet | The snippet calls AsterPort “the universal market leader.” | attributed report | low | public | rejected; underlying source was not reviewed and the superlative is unsupported |
| E-018 | EmberPass | posted 2026-08-28; observed 2026-08-31 | Fictional official social post, `https://social.example.invalid/emberpass/posts/88` | The official account announced automated spending policies and linked E-011. | observed | medium | public | accepted only as launch enrichment; E-011 remains primary |
| E-019 | Dovetail Wallets | published 2026-04-15; observed 2026-08-31 | Fictional release archive, `https://dovetail-wallets.example.invalid/releases/spring-onboarding/` | Dovetail announced an onboarding redesign before the baseline window. | observed | high | public | out-of-window; retained as current-state history, not an in-window event |
| E-020 | AsterPort | published 2026-08-25; observed 2026-08-31 | Fictional syndicated release copy | The item repeats the transfer-policy announcement in E-001 without new detail. | attributed report | medium | public | duplicate of E-001; excluded from synthesis |
| E-021 | AsterPort | captured 2026-05-15; reviewed 2026-08-31 | Fictional approved prior pricing capture | The old Growth plan used a 0.05 fictional-unit active-wallet rate. | observed | high | internal | superseded by current public E-004; retained for pricing history |
| E-022 | Dovetail Wallets | observed 2026-08-31 | Fictional pricing page, `https://dovetail-wallets.example.invalid/pricing/` | Growth is listed at 179 fictional units monthly plus active-wallet usage. | observed | high | public | accepted; support pricing undisclosed |
| E-023 | CinderKey | observed 2026-08-31 | Fictional pricing page, `https://cinderkey.example.invalid/pricing/` | Developer is free and Team is 99 fictional units monthly. | observed | high | public | accepted; overage terms unclear |
| E-024 | EmberPass | observed 2026-08-31 | Fictional pricing page, `https://emberpass.example.invalid/pricing/` | Starter is 200 fictional units monthly and Growth is 600 plus transaction usage. | observed | high | public | accepted; enterprise minimums unknown |
| E-025 | FableAccount | observed 2026-08-31 | Fictional homepage, `https://fableaccount.example.invalid/` | FableAccount describes itself as programmable account infrastructure for developers. | observed | high | public | accepted; no end-user authentication product is shown |
| E-026 | FableAccount | note dated 2026-08-27; reviewed 2026-09-01 | Fictional approved local note, `note://approved/wallet-evaluations/fable-07` | A fictional evaluator asked whether FableAccount plus separate authentication would provide more control than HarborKey. | attributed report | medium | internal | accepted for internal analysis; no decision or outcome recorded |

## Revisions, duplicates, and conflicts

- E-004 supersedes E-021 as AsterPort's current public Growth price; E-021 remains historical.
- E-020 duplicates E-001 and is excluded from synthesis.
- E-007 and E-015 are unresolved, not necessarily contradictory: the public plan and reported
  custom quote may cover different support and administration scopes.
- E-003 supplies prior narrative evidence but is internal and cannot be quoted externally.
- E-018 corroborates that EmberPass promoted E-011; it does not independently prove adoption.

## Rejected and out-of-window items

- E-017 is rejected because only an unsupported search snippet was available.
- E-019 is outside the configured window and may inform current-state history only.
- E-020 is a duplicate and adds no independent support.
- E-021 is superseded for current pricing but retained as a prior state.

## Unknowns and limitations

- AsterPort migration, account export, and transfer-control plan entitlement are unknown.
- BrindleAuth's reported custom quote cannot be compared directly with its public Launch plan.
- CinderKey lacks dated changelog and release surfaces.
- EmberPass customer adoption, production scale, and general availability are unknown.
- FableAccount public pricing was not found.
- Internal evaluation reports do not establish wins, losses, or market-wide buyer preference.

## Proposed evidence-review decision

The fictional PMM approved E-001 through E-016, E-018, and E-022 through E-026 with their
labels and restrictions. E-015 remains an unresolved internal report. E-017 was rejected,
E-019 was kept out of the in-window synthesis, E-020 was excluded as a duplicate, and E-021
was retained only as superseded pricing history. Any change to this set requires a new review.
