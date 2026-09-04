# Competitive-intelligence source map

Status: Verified

Market: `[market-id]`

Scope: `[product, geography, or product-geography]`

Owner: `[individual PMM]`

Version/verified date: `[YYYY-MM-DD or version]`

This is the canonical source list for future runs. It contains verified competitor URLs,
reviewed `not found` results, and adopter-approved internal sources only. Keep pending or
rejected candidates in `onboarding-state.md`. Never place passwords, tokens, or secret values
here.

## Verification rules

- A competitor homepage supplied by the adopter may be used to discover other public sources.
- Product pages, pricing, blogs, changelogs, release notes, documentation, repositories, and
  social accounts must be proposed to the adopter before becoming canonical.
- Record `not found` only after documenting the search; do not invent a likely URL.
- Internal channel and file metadata may support suggestions. Do not read contents before the
  adopter approves access.
- A new or replacement source is not available to later runs until this file is updated with
  verifier and verification date.

## Source policy

- Required sources: `[sources whose failure blocks the run]`
- Optional sources: `[sources whose failure is reported but does not block]`
- Allowed local roots: `[explicit folders]`
- Sensitivity labels: `[public, internal, confidential, or adopter equivalents]`
- Retention rule: `[how long evidence and reports are retained]`
- Publication boundary: `[where source content may and may not appear]`

## Competitor roster and aliases

| Competitor | Homepage | Aliases/product names | Ambiguity filters | Status | Market relevance |
|---|---|---|---|---|---|
| `[name]` | `[adopter-verified homepage]` | `[aliases]` | `[terms preventing false matches]` | `active / monitor / watchlist / dormant` | `[relevance to this product/geography]` |

Use aliases during collection but canonical names in outputs.

## Verified competitor sources

Use one row per source so verification and collection cadence remain explicit.

| Source ID | Competitor | Type | Verified URL or result | Discovered from | Why it matters | Official confidence | Verified by/date | Cadence | Limitations |
|---|---|---|---|---|---|---|---|---|---|
| `[source-id]` | `[name]` | `homepage / product / pricing / blog / changelog / releases / docs / repository / social` | `[URL or “not found — search recorded”]` | `[adopter/homepage/navigation/sitemap/search]` | `[market relevance]` | `high / medium / low` | `[reviewer, YYYY-MM-DD]` | `every-run / baseline / event-triggered` | `[constraint]` |

For each competitor, attempt to identify:

- homepage;
- product or solution pages;
- pricing or packaging;
- blog or newsroom;
- changelog;
- release notes;
- product documentation;
- official repository or release feed when relevant; and
- official social accounts.

These are crucial discovery targets, not a license to fabricate missing links. A verified
homepage is sufficient for a limited first baseline if missing categories are visible.

## Competitor source coverage

| Competitor | Product | Pricing | Blog/news | Changelog | Releases | Docs | Repository | Social | Coverage note |
|---|---|---|---|---|---|---|---|---|---|
| `[name]` | `verified / not found` | `verified / not found` | `verified / not found` | `verified / not found` | `verified / not found` | `verified / not found` | `verified / n/a / not found` | `verified / not found` | `[effect on baseline]` |

## Approved adopter sources

Start with the adopter homepage. Add product pages, documentation, positioning, strategy,
priority, proof, or other sources only after the adopter approves them.

| Source ID | System/type | Verified location | Positioning use | Access scope | Sensitivity | Approved by/date | Limitations |
|---|---|---|---|---|---|---|---|
| `[source-id]` | `[website / Drive / local file / other]` | `[URL or stable reference]` | `[audience/problem/category/value/differentiation/claim/proof/comparison criteria]` | `[what may be read]` | `[label]` | `[reviewer, YYYY-MM-DD]` | `[constraint]` |

## Approved internal competitive sources

The onboarding agent may suggest Slack channels, Drive files, and other sources from metadata.
Only approved entries belong here.

| Source ID | System | Verified location | Why it matters | Access scope | Search pattern | Sensitivity | Approved by/date | Limitations |
|---|---|---|---|---|---|---|---|---|
| `[source-id]` | `[Slack / Drive / local files / other]` | `[channel, file, folder, or collection]` | `[expected signal]` | `[content and date scope approved]` | `[competitor aliases + context terms]` | `[label]` | `[reviewer, YYYY-MM-DD]` | `[constraint]` |

For useful internal evidence, capture stable reference, date, author or owner, exact quote or
faithful paraphrase, competitor, and signal type. Suggested types include `mention`,
`objection`, `win-context`, `loss-context`, `product-comparison`, and `pricing-signal`.
Win/loss status remains unconfirmed unless the adopter's authoritative process confirms it.

## Optional community sources

| Source ID | Community or repository | Scope | Query pattern | Authority notes | Approved by/date |
|---|---|---|---|---|---|
| `[source-id]` | `[forum, issue tracker, community, repository]` | `[which competitors]` | `[migration / pain / comparison terms]` | `[first-party, user report, anonymous, etc.]` | `[reviewer, YYYY-MM-DD]` |

Community records are attributed reports unless stronger evidence supports the underlying
condition. Do not generalize one report to the market.

## Cross-competitor context terms

Adapt these to the market:

- competitor, alternative, comparison, versus, migration, switching;
- objection, battlecard, evaluation, proof of concept;
- win, loss, selected, replaced, displaced;
- pricing, packaging, discount, contract;
- launch, release, partnership, acquisition, integration; and
- reliability, performance, compliance, security, support, developer experience.

## Narrative-change baseline

| Competitor | Field | Prior evidence | Current evidence |
|---|---|---|---|
| `[name]` | `headline / subheadline / CTA / category / audience / proof` | `[text, date, source]` | `[text, date, source]` |

## Query recipes

Write exact repeatable searches. Keep connector-specific syntax here rather than in
`SKILL.md`.

```text
"[competitor]" AND (pricing OR packaging OR contract)
"[competitor]" AND (migration OR switching OR replaced)
"[competitor]" AND (launch OR release OR partnership OR acquisition)
site:[official-domain] [product or claim]
```

## Change log

| Date | Change | Verification decision | Reviewer |
|---|---|---|---|
| `[YYYY-MM-DD]` | `[source added, replaced, rejected, or marked not found]` | `[reason]` | `[reviewer]` |
