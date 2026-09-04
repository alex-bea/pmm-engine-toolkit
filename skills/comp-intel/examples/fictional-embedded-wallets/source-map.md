# Fictional HarborKey competitive-intelligence source map

Status: Verified — example only

Market: `harborkey-embedded-wallets`

Scope: HarborKey Wallet Platform embedded-wallet infrastructure

Owner: Fictional HarborKey PMM

Version/verified date: 2026-08-31T15:25:00Z

Every organization, source, account, path, and value in this file is invented. All web
addresses use reserved `.invalid` domains. The unresolved AsterPort migration-guide candidate
remains in `onboarding-state.md` and is not canonical here.

## Verification rules

- Each homepage was supplied by the fictional PMM.
- Other public URLs were proposed from homepage navigation, footers, sitemaps, or searches and
  then verified by the fictional PMM.
- `not found` means the named surfaces were checked; it does not prove that a source is absent.
- Internal metadata was inspected before content access, and only approved content scopes are
  recorded below.
- Future runs may use only the verified entries in this file.

## Source policy

- Required sources: one verified homepage for every rostered competitor
- Crucial enrichment targets: product, pricing, blog, changelog, releases, documentation,
  repository, and official social sources
- Optional sources: approved Slack, Drive, local evaluation notes, and developer communities
- Allowed local roots: `./approved-notes/`
- Sensitivity labels: public, internal, confidential
- Retention rule: raw run evidence for 90 days; reviewed durable facts remain in the registry
- Publication boundary: internal or confidential evidence may guide analysis but cannot support
  public claims without corroborating public evidence

## Competitor roster and aliases

| Competitor | Homepage | Aliases/product names | Ambiguity filters | Status | Market relevance |
|---|---|---|---|---|---|
| AsterPort | `https://asterport.example.invalid/` | Aster Port, AsterPort SDK | wallet, authentication, embedded account | active | Direct embedded-wallet competitor now bundled with a fictional payments platform |
| BrindleAuth | `https://brindleauth.example.invalid/` | Brindle Auth, Brindle Wallets | wallet, identity, developer | active | Direct competitor combining wallet onboarding with an institutional owner narrative |
| CinderKey | `https://cinderkey.example.invalid/` | Cinder Key | wallet, authentication, SDK | monitor | Established authentication-led wallet provider with a reliability position |
| Dovetail Wallets | `https://dovetail-wallets.example.invalid/` | Dovetail, Dovetail SDK | wallet, onboarding, conversion | monitor | Conversion-led wallet provider relevant to product-led application teams |
| EmberPass | `https://emberpass.example.invalid/` | Ember Pass, EmberPass Finance | wallet, fintech, programmable account | active | Rebranded wallet platform expanding into automated money movement |
| FableAccount | `https://fableaccount.example.invalid/` | Fable Account, Fable SDK | smart account, wallet infrastructure, signing | watchlist | Lower-level programmable-account infrastructure that may expand into a full SDK |

## Verified competitor sources

Use one row per source. Every row below is fictional.

| Source ID | Competitor | Type | Verified URL or result | Discovered from | Why it matters | Official confidence | Verified by/date | Cadence | Limitations |
|---|---|---|---|---|---|---|---|---|---|
| AP-WEB-01 | AsterPort | homepage | `https://asterport.example.invalid/` | Adopter supplied | Category, audience, narrative, CTA | high | Fictional PMM, 2026-08-31 | every-run | Current page only |
| AP-WEB-02 | AsterPort | product | `https://asterport.example.invalid/wallet-platform/` | Homepage navigation | Authentication, accounts, transaction capabilities | high | Fictional PMM, 2026-08-31 | every-run | Feature presence does not prove adoption |
| AP-WEB-03 | AsterPort | pricing | `https://asterport.example.invalid/pricing/` | Homepage navigation | User and signature packaging | high | Fictional PMM, 2026-08-31 | every-run | Enterprise terms undisclosed |
| AP-WEB-04 | AsterPort | blog | `https://asterport.example.invalid/news/` | Homepage footer | Announcements and ownership framing | high | Fictional PMM, 2026-08-31 | every-run | Fictional newsroom |
| AP-WEB-05 | AsterPort | changelog | `https://asterport.example.invalid/changelog/` | Product navigation | Incremental shipped changes | high | Fictional PMM, 2026-08-31 | every-run | Does not contain migration guidance |
| AP-WEB-06 | AsterPort | releases | `https://asterport.example.invalid/releases/` | Homepage footer | Dated major releases | high | Fictional PMM, 2026-08-31 | every-run | Release date does not prove availability to every plan |
| AP-WEB-07 | AsterPort | docs | `https://docs.asterport.example.invalid/` | Homepage navigation | Capability detail and constraints | high | Fictional PMM, 2026-08-31 | every-run | Documentation alone does not prove shipping |
| AP-WEB-08 | AsterPort | repository | not found — homepage, docs, footer, and site search checked 2026-08-31 | Documented search | Code and release verification if public | high | Fictional PMM, 2026-08-31 | every-run | Absence not proven |
| AP-WEB-09 | AsterPort | social | `https://social.example.invalid/asterport` | Homepage footer | Event-triggered announcement enrichment | high | Fictional PMM, 2026-08-31 | event-triggered | Not a primary discovery source |
| BA-WEB-01 | BrindleAuth | homepage | `https://brindleauth.example.invalid/` | Adopter supplied | Category, audience, ownership narrative | high | Fictional PMM, 2026-08-31 | every-run | Current page only |
| BA-WEB-02 | BrindleAuth | product | `https://brindleauth.example.invalid/platform/` | Homepage navigation | Wallet, identity, and administrative controls | high | Fictional PMM, 2026-08-31 | every-run | Packaging detail incomplete |
| BA-WEB-03 | BrindleAuth | pricing | `https://brindleauth.example.invalid/pricing/` | Homepage navigation | Monthly-user and support tiers | high | Fictional PMM, 2026-08-31 | every-run | Contract discounts unknown |
| BA-WEB-04 | BrindleAuth | blog | `https://brindleauth.example.invalid/insights/` | Homepage navigation | Acquisition and product announcements | high | Fictional PMM, 2026-08-31 | every-run | Fictional source |
| BA-WEB-05 | BrindleAuth | changelog | `https://docs.brindleauth.example.invalid/changelog/` | Documentation navigation | Shipped product changes | high | Fictional PMM, 2026-08-31 | every-run | Includes release entries |
| BA-WEB-06 | BrindleAuth | releases | not found — changelog is the documented release surface | Homepage and site search | Separate release archive | high | Fictional PMM, 2026-08-31 | baseline | Changelog used instead |
| BA-WEB-07 | BrindleAuth | docs | `https://docs.brindleauth.example.invalid/` | Homepage navigation | Technical and security detail | high | Fictional PMM, 2026-08-31 | every-run | Scale claims not independently tested |
| BA-WEB-08 | BrindleAuth | repository | not found — homepage, docs, and site search checked 2026-08-31 | Documented search | Public code and release feed | high | Fictional PMM, 2026-08-31 | every-run | Absence not proven |
| BA-WEB-09 | BrindleAuth | social | `https://social.example.invalid/brindleauth` | Homepage footer | Ownership and launch enrichment | high | Fictional PMM, 2026-08-31 | event-triggered | Not a primary discovery source |
| CK-WEB-01 | CinderKey | homepage | `https://cinderkey.example.invalid/` | Adopter supplied | Reliability narrative and audience | high | Fictional PMM, 2026-08-31 | every-run | Current page only |
| CK-WEB-02 | CinderKey | product | `https://cinderkey.example.invalid/embedded-wallets/` | Homepage navigation | Authentication and recovery capabilities | high | Fictional PMM, 2026-08-31 | every-run | No admin-policy detail |
| CK-WEB-03 | CinderKey | pricing | `https://cinderkey.example.invalid/pricing/` | Homepage navigation | Active-user tiers | high | Fictional PMM, 2026-08-31 | every-run | Overage terms unclear |
| CK-WEB-04 | CinderKey | blog | `https://cinderkey.example.invalid/blog/` | Homepage navigation | Announcements and technical guidance | high | Fictional PMM, 2026-08-31 | every-run | Latest relevant post is older than run window |
| CK-WEB-05 | CinderKey | changelog | not found — product, docs, footer, and site search checked 2026-08-31 | Documented search | Incremental product changes | high | Fictional PMM, 2026-08-31 | every-run | Absence not proven |
| CK-WEB-06 | CinderKey | releases | not found — blog and repository release pages checked 2026-08-31 | Documented search | Dated shipping proof | high | Fictional PMM, 2026-08-31 | every-run | Absence not proven |
| CK-WEB-07 | CinderKey | docs | `https://docs.cinderkey.example.invalid/` | Product navigation | SDK and recovery behavior | high | Fictional PMM, 2026-08-31 | every-run | Documentation has no visible version date |
| CK-WEB-08 | CinderKey | repository | `https://code.example.invalid/cinderkey/sdk/` | Documentation footer | Public SDK activity | medium | Fictional PMM, 2026-08-31 | every-run | Fictional repository host; organization link supplied by docs |
| CK-WEB-09 | CinderKey | social | `https://social.example.invalid/cinderkey` | Homepage footer | Event-triggered enrichment | high | Fictional PMM, 2026-08-31 | event-triggered | Not a primary discovery source |
| DW-WEB-01 | Dovetail Wallets | homepage | `https://dovetail-wallets.example.invalid/` | Adopter supplied | Conversion narrative and audience | high | Fictional PMM, 2026-08-31 | every-run | Current page only |
| DW-WEB-02 | Dovetail Wallets | product | `https://dovetail-wallets.example.invalid/product/` | Homepage navigation | Onboarding and wallet capabilities | high | Fictional PMM, 2026-08-31 | every-run | Enterprise controls unclear |
| DW-WEB-03 | Dovetail Wallets | pricing | `https://dovetail-wallets.example.invalid/pricing/` | Homepage navigation | Active-wallet pricing | high | Fictional PMM, 2026-08-31 | every-run | Support pricing undisclosed |
| DW-WEB-04 | Dovetail Wallets | blog | `https://dovetail-wallets.example.invalid/blog/` | Homepage navigation | Product and regional announcements | high | Fictional PMM, 2026-08-31 | every-run | Fictional source |
| DW-WEB-05 | Dovetail Wallets | changelog | `https://docs.dovetail-wallets.example.invalid/changelog/` | Documentation navigation | Incremental product changes | high | Fictional PMM, 2026-08-31 | every-run | Update dates available |
| DW-WEB-06 | Dovetail Wallets | releases | `https://dovetail-wallets.example.invalid/releases/` | Blog navigation | Major launches | high | Fictional PMM, 2026-08-31 | every-run | No download artifacts |
| DW-WEB-07 | Dovetail Wallets | docs | `https://docs.dovetail-wallets.example.invalid/` | Homepage navigation | SDK and integration detail | high | Fictional PMM, 2026-08-31 | every-run | Public documentation only |
| DW-WEB-08 | Dovetail Wallets | repository | not found — homepage, docs, and site search checked 2026-08-31 | Documented search | Public code and release verification | high | Fictional PMM, 2026-08-31 | every-run | Absence not proven |
| DW-WEB-09 | Dovetail Wallets | social | `https://social.example.invalid/dovetail-wallets` | Homepage footer | Event-triggered enrichment | high | Fictional PMM, 2026-08-31 | event-triggered | Not a primary discovery source |
| EP-WEB-01 | EmberPass | homepage | `https://emberpass.example.invalid/` | Adopter supplied | Rebrand, category, audience, narrative | high | Fictional PMM, 2026-08-31 | every-run | Current page only |
| EP-WEB-02 | EmberPass | product | `https://emberpass.example.invalid/automated-wallets/` | Homepage navigation | Programmable accounts and spending controls | high | Fictional PMM, 2026-08-31 | every-run | Customer adoption not established |
| EP-WEB-03 | EmberPass | pricing | `https://emberpass.example.invalid/pricing/` | Homepage navigation | Wallet and transaction pricing | high | Fictional PMM, 2026-08-31 | every-run | Enterprise minimums unclear |
| EP-WEB-04 | EmberPass | blog | `https://emberpass.example.invalid/journal/` | Homepage navigation | Rebrand and product announcements | high | Fictional PMM, 2026-08-31 | every-run | Fictional source |
| EP-WEB-05 | EmberPass | changelog | `https://docs.emberpass.example.invalid/changelog/` | Documentation navigation | Incremental shipping evidence | high | Fictional PMM, 2026-08-31 | every-run | Feature flags not visible |
| EP-WEB-06 | EmberPass | releases | `https://emberpass.example.invalid/releases/` | Homepage footer | Dated major releases | high | Fictional PMM, 2026-08-31 | every-run | Plan availability may differ |
| EP-WEB-07 | EmberPass | docs | `https://docs.emberpass.example.invalid/` | Homepage navigation | Policy and integration behavior | high | Fictional PMM, 2026-08-31 | every-run | Does not prove production scale |
| EP-WEB-08 | EmberPass | repository | `https://code.example.invalid/emberpass/sdk/` | Documentation footer | SDK activity and tagged releases | medium | Fictional PMM, 2026-08-31 | every-run | Fictional repository host |
| EP-WEB-09 | EmberPass | social | `https://social.example.invalid/emberpass` | Homepage footer | Launch announcement enrichment | high | Fictional PMM, 2026-08-31 | event-triggered | Not a primary discovery source |
| FA-WEB-01 | FableAccount | homepage | `https://fableaccount.example.invalid/` | Adopter supplied | Lower-level account position | high | Fictional PMM, 2026-08-31 | every-run | Adjacent rather than direct |
| FA-WEB-02 | FableAccount | product | `https://fableaccount.example.invalid/infrastructure/` | Homepage navigation | Signing and account-control capabilities | high | Fictional PMM, 2026-08-31 | every-run | No end-user authentication product |
| FA-WEB-03 | FableAccount | pricing | not found — homepage, docs, and site search checked 2026-08-31 | Documented search | Packaging and evaluation | high | Fictional PMM, 2026-08-31 | every-run | Pricing absence not proven |
| FA-WEB-04 | FableAccount | blog | `https://fableaccount.example.invalid/blog/` | Homepage navigation | Partnerships and launches | high | Fictional PMM, 2026-08-31 | every-run | Fictional source |
| FA-WEB-05 | FableAccount | changelog | `https://docs.fableaccount.example.invalid/changelog/` | Documentation navigation | Incremental product change | high | Fictional PMM, 2026-08-31 | every-run | Uses repository tags for detail |
| FA-WEB-06 | FableAccount | releases | `https://code.example.invalid/fableaccount/sdk/releases/` | Repository navigation | Dated SDK releases | medium | Fictional PMM, 2026-08-31 | every-run | Repository release, not hosted-service availability |
| FA-WEB-07 | FableAccount | docs | `https://docs.fableaccount.example.invalid/` | Homepage navigation | Signing, policy, and latency detail | high | Fictional PMM, 2026-08-31 | every-run | Self-published technical claims |
| FA-WEB-08 | FableAccount | repository | `https://code.example.invalid/fableaccount/sdk/` | Documentation footer | Code and release activity | medium | Fictional PMM, 2026-08-31 | every-run | Fictional repository host |
| FA-WEB-09 | FableAccount | social | `https://social.example.invalid/fableaccount` | Homepage footer | Event-triggered enrichment | high | Fictional PMM, 2026-08-31 | event-triggered | Not a primary discovery source |

## Competitor source coverage

| Competitor | Product | Pricing | Blog/news | Changelog | Releases | Docs | Repository | Social | Coverage note |
|---|---|---|---|---|---|---|---|---|---|
| AsterPort | verified | verified | verified | verified | verified | verified | not found | verified | Strong first-party coverage; migration guidance unresolved |
| BrindleAuth | verified | verified | verified | verified | changelog used | verified | not found | verified | Strong public coverage; contract pricing remains unknown |
| CinderKey | verified | verified | verified | not found | not found | verified | verified | verified | Limited shipping chronology |
| Dovetail Wallets | verified | verified | verified | verified | verified | verified | not found | verified | Strong public coverage; enterprise-control detail weak |
| EmberPass | verified | verified | verified | verified | verified | verified | verified | verified | Strong public coverage; adoption proof missing |
| FableAccount | verified | not found | verified | verified | verified | verified | verified | verified | Watchlist coverage strong except pricing |

## Approved adopter sources

| Source ID | System/type | Verified location | Positioning use | Access scope | Sensitivity | Approved by/date | Limitations |
|---|---|---|---|---|---|---|---|
| HK-SRC-01 | website | `https://harborkey.example.invalid/` | Audience, problem, category, value | Public page | public | Fictional PMM, 2026-08-31 | Summary claims only |
| HK-SRC-02 | documentation | `https://docs.harborkey.example.invalid/` | Product behavior, claim support, constraints | Public documentation | public | Fictional PMM, 2026-08-31 | No customer outcomes |
| HK-SRC-03 | Drive | `HarborKey Product Narrative` | Category, differentiation, approved language | Approved document body | internal | Fictional PMM, 2026-08-31 | No direct external quotation |
| HK-SRC-04 | Drive | `HarborKey Wallet Priorities` | Comparison priorities and future direction | Approved document body | confidential | Fictional PMM, 2026-08-31 | Contains unannounced work |
| HK-SRC-05 | Drive | `HarborKey Proof Library` | Technical proof and internal tests | Approved document body | internal | Fictional PMM, 2026-08-31 | Scale sample incomplete |

## Approved internal competitive sources

| Source ID | System | Verified location | Why it matters | Access scope | Search pattern | Sensitivity | Approved by/date | Limitations |
|---|---|---|---|---|---|---|---|---|
| INT-01 | Slack | `#wallet-product-feedback` | Product pain and feature comparisons | Approved messages in baseline window | Competitor aliases plus policy, recovery, onboarding | internal | Fictional PMM, 2026-08-31 | Reports remain attributed |
| INT-02 | Slack | `#wallet-evaluations` | Pricing, ownership, and buyer criteria | Approved messages in baseline window | Competitor aliases plus pricing, selected, evaluation | internal | Fictional PMM, 2026-08-31 | Outcomes remain unconfirmed |
| INT-03 | Slack | `#wallet-migrations` | Switching, export, and implementation friction | Approved messages in baseline window | Competitor aliases plus migration, keys, export | internal | Fictional PMM, 2026-08-31 | No customer identity may enter public output |
| INT-04 | local files | `workspace://harborkey/approved-notes/wallet-evaluations.md` | PMM-supplied evaluation context | One approved fictional file | Competitor aliases plus decision criteria | internal | Fictional PMM, 2026-08-31 | Not a system of record |

## Optional community sources

| Source ID | Community or repository | Scope | Query pattern | Authority notes | Approved by/date |
|---|---|---|---|---|---|
| COM-01 | `https://forum.example.invalid/wallet-builders/` | All rostered competitors | Alias plus migration, reliability, pricing, recovery | User reports remain attributed and non-generalizable | Fictional PMM, 2026-08-31 |

## Cross-competitor context terms

- wallet SDK, embedded account, authentication, recovery, export, key portability;
- smart account, session policy, spending limit, sponsorship, transaction permission;
- migration, replacement, integration, evaluation, selected, rejected;
- pricing, active wallet, signature, transaction, support, enterprise;
- acquisition, rebrand, partnership, bundled platform, money movement; and
- reliability, conversion, latency, compliance, developer experience.

## Narrative-change baseline

| Competitor | Field | Prior evidence | Current evidence |
|---|---|---|---|
| AsterPort | headline/category | “Wallet onboarding for every app,” fictional capture dated 2026-05-12 | “Wallets and money movement in one platform,” AP-WEB-01 observed 2026-08-31 |
| BrindleAuth | ownership/audience | Independent developer-wallet narrative, fictional capture dated 2026-05-20 | Institutional identity-and-wallet narrative, BA-WEB-01 observed 2026-08-31 |
| CinderKey | headline | “Wallet authentication that keeps working,” fictional capture dated 2026-06-03 | Same language, CK-WEB-01 observed 2026-08-31 |
| Dovetail Wallets | headline | “Turn sign-in into wallet activation,” fictional capture dated 2026-06-10 | Same language, DW-WEB-01 observed 2026-08-31 |
| EmberPass | brand/category | Former fictional brand focused on embedded accounts, capture dated 2026-05-18 | EmberPass “Programmable wallets for automated commerce,” EP-WEB-01 observed 2026-08-31 |
| FableAccount | category | “Signing infrastructure for developers,” fictional capture dated 2026-07-01 | “Programmable account infrastructure,” FA-WEB-01 observed 2026-08-31 |

## Query recipes

```text
("AsterPort" OR "Aster Port") AND (pricing OR migration OR export)
("BrindleAuth" OR "Brindle Auth") AND (acquisition OR enterprise OR evaluation)
("CinderKey" OR "Dovetail Wallets") AND (reliability OR onboarding OR switching)
("EmberPass" OR "FableAccount") AND (automated OR policy OR smart account)
site:asterport.example.invalid wallet pricing
site:emberpass.example.invalid release policy
```

## Change log

| Date | Change | Verification decision | Reviewer |
|---|---|---|---|
| 2026-08-31T15:25:00Z | Created source map from six supplied homepages, verified derived public targets, and approved internal-source metadata | Approved for baseline; unresolved migration candidate remains in onboarding state | Fictional HarborKey PMM |
