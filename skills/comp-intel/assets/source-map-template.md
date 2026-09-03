# Competitive-intelligence source map

Status: adopter-owned draft

Market: `[market or product area]`

Owner: `[owner]`

Last reviewed: `[YYYY-MM-DD]`

This file tells the analyst where it may look and how. Delete source types you do not use.
Never place passwords, tokens, or secret values here.

## Source policy

- Absolute run window: `[provided at run time]`
- Required sources: `[sources whose failure blocks the run]`
- Optional sources: `[sources whose failure is reported but does not block]`
- Allowed local roots: `[explicit folders]`
- Sensitivity labels: `[public, internal, confidential, or your equivalents]`
- Retention rule: `[how long evidence and reports are retained]`

## Competitor discovery terms

| Competitor | Canonical name | Aliases or product names | Ambiguity filters | Status |
|---|---|---|---|---|
| `[name]` | `[name]` | `[aliases]` | `[terms that prevent false matches]` | `active / monitor / watchlist / dormant` |

Use aliases in collection, but write the canonical name in outputs.

## Cross-competitor context terms

Adapt these to the market:

- competitor, alternative, comparison, versus, migration, switching;
- objection, battlecard, evaluation, proof of concept;
- win, loss, selected, replaced, displaced;
- pricing, packaging, discount, contract;
- launch, release, partnership, acquisition, integration; and
- reliability, performance, compliance, security, support, developer experience.

## Authorized internal sources

Internal sources are optional and adopter-owned. Include only sources the operator is allowed
to access.

| Source ID | System and location | Why it matters | Required? | Search pattern | Sensitivity | Owner |
|---|---|---|---|---|---|---|
| `[internal-source]` | `[channel, folder, or collection]` | `[signal expected]` | `yes / no` | `[competitor aliases + context terms]` | `[label]` | `[owner]` |

For each useful item capture source ID, stable message or file reference, date, author, exact
quote or faithful paraphrase, competitor, and signal type. Suggested signal types are
`mention`, `objection`, `win-context`, `loss-context`, `product-comparison`, and
`pricing-signal`. Keep outcome status unconfirmed unless the adopter's review process confirms
it.

## Developer and community sources

| Source ID | Community or repository | Scope | Required? | Query pattern | Authority notes |
|---|---|---|---|---|---|
| `[community-source]` | `[forum, issue tracker, community, repository]` | `[active competitors only, unless baseline]` | `no` | `[competitor] + [migration / pain point / comparison term]` | `[first-party, user report, anonymous, etc.]` |

Classify useful records as `developer-pain-point`, `competitive-comparison`, or
`migration-signal`. A user report can establish that the user made the report; it does not by
itself prove a general product condition.

## First-party web targets

Create one row per active competitor. During a baseline, include the full roster.

| Competitor | Homepage | Product/docs | Blog/news | Changelog/releases | Pricing | Repository | Watch for |
|---|---|---|---|---|---|---|---|
| `[name]` | `[URL]` | `[URL]` | `[URL]` | `[URL]` | `[URL or “none found”]` | `[URL or n/a]` | `[claims, audience, capabilities, packaging]` |

Rules:

- Check the pricing target for every active competitor on every standard run.
- Prefer an announcement, release note, or changelog over a docs page when establishing that
  a capability shipped.
- Record publication date when available and observation date always.
- A missing page or failed fetch is a limitation, not proof of absence.
- Read the source page. A search snippet is discovery evidence only.

## Narrative-change capture

For each competitor being compared, preserve:

| Field | Prior evidence | Current evidence |
|---|---|---|
| Headline | `[text, date, source]` | `[text, date, source]` |
| Subheadline | `[text, date, source]` | `[text, date, source]` |
| Primary CTA | `[text, date, source]` | `[text, date, source]` |
| Category and audience | `[text, date, source]` | `[text, date, source]` |
| Proof points | `[text, date, source]` | `[text, date, source]` |

## Targeted social enrichment

Use official social accounts only after collection finds a notable funding event, acquisition,
major partnership, or product launch. Record URL, author, date, exact quote, and visible
engagement metrics when relevant. Social is enrichment, not the primary discovery method.

| Competitor | Official account | Use only for | Notes |
|---|---|---|---|
| `[name]` | `[URL or handle]` | `[material event types]` | `[limits]` |

## Optional source people or stakeholder map

Use roles rather than personal profiles when possible.

| Role or consented person | Domain | Signals to prioritize | Fidelity notes |
|---|---|---|---|
| `[role]` | `[market, product, sales, partnerships, etc.]` | `[what they can reliably report]` | `[direct owner, second-hand, historical, etc.]` |

## Query recipes

Write the exact searches the agent should repeat. Examples:

```text
"[competitor]" AND (pricing OR packaging OR contract)
"[competitor]" AND (migration OR switching OR replaced)
"[competitor]" AND (launch OR release OR partnership OR acquisition)
site:[official-domain] [product or claim]
```

Keep connector-specific syntax here, not in `SKILL.md`, so adopters can change tools without
rewriting the method.

