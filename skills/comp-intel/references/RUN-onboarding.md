# First-run onboarding

Use this runbook when an individual PMM is setting up a market, when the required market
files do not exist, or when the user asks to rebuild setup. The target is about 30 minutes of
PMM attention. Research and rendering may continue after the interactive questions finish.

The setup flow is:

```text
Define market → discover sources → verify sources → draft adopter positioning →
approve positioning → run baseline → recommend enrichment
```

Do not start competitor comparison before the source map is verified and the adopter's
positioning is approved. A limited website-only baseline is allowed after those gates.

## Files created

Create one adopter-owned directory for each product, geography, or product-geography
combination:

```text
competitive-intel/markets/<market-id>/
├── onboarding-state.md
├── market-pack.yaml
├── source-map.md
├── adopter-positioning.md
├── competitor-registry.md
├── positioning-context.md
└── trackers.md
```

Similar markets may repeat or reference the same sources, but each market must state why a
source and competitor are relevant to that product or geography. Never hide scope inside a
shared, ambiguous market record.

Copy the matching files from `assets/` and fill them as the setup progresses. The source map
is the canonical source list for future runs. Pending source candidates belong in
`onboarding-state.md`, not in `source-map.md`.

## 1. Explain the setup

Tell the PMM, in plain language:

- the skill builds a sourced competitor baseline and reusable registry;
- setup starts from their website and competitor homepages;
- the agent will propose official source links for verification;
- internal channels and files are never read before the PMM approves them;
- the agent will draft adopter positioning for review before comparing competitors; and
- sparse inputs still produce a limited baseline plus a prioritized enrichment plan.

Then ask for all information the PMM can provide in one response:

1. adopter product or organization name;
2. adopter homepage;
3. product, geography, or product-geography scope;
4. a short market description if known;
5. competitor names and homepages; and
6. any supplied product documents, priority notes, or positioning sources.

Do not require the PMM to know the full source architecture.

## 2. Create the market workspace

Create a collision-safe market ID and fill `market-pack.yaml`. Record:

- `scope_type`: `product`, `geography`, or `product-geography`;
- product and geography values, using `not-applicable` when appropriate;
- market definition and explicit exclusions;
- adopter product and homepage;
- each competitor's canonical name and homepage; and
- paths to this market's source map and adopter-positioning file.

Create `onboarding-state.md` immediately so an interrupted setup can resume without repeating
approved steps.

## 3. Discover competitor sources

The PMM-provided homepage authorizes public discovery from that site and the open web. For
each competitor, inspect the homepage, navigation, footer, sitemap when available, and search
results pointing to likely official domains. Propose candidates for:

- product or solution pages;
- pricing or packaging;
- blog or newsroom;
- changelog;
- release notes;
- product documentation;
- official repositories or release feeds when relevant; and
- official social accounts.

Treat changelog and release notes as separate candidates when both exist. Do not assume a
subdomain or social account is official merely because its name matches.

Present one review table with competitor, source type, candidate URL, how it was found, why it
matters, and confidence that it is official. The PMM may approve, reject, replace, or mark a
source as not found. Keep unresolved candidates in `onboarding-state.md`.

Only after the PMM verifies a candidate may it be written to `source-map.md`. Record verifier
and verification date. For every crucial source type without a verified link, record
`not found` plus the search performed; never fabricate a URL.

## 4. Suggest internal context without reading it

Identify which source tools are available and tell the PMM what each could collect if
authorized. Offer to use any relevant available system; none is mandatory. If Slack or Drive
access is available, begin there. Inspect only source metadata: channel or collection names,
descriptions, document titles, owners, folders, and modified dates. Do not read messages or
document bodies yet.

Suggest a small, manageable group of likely Slack channels and Drive files first. Around three
of each is a useful default, not a quota. Explain why each may improve product positioning or
competitive coverage. Ask the PMM which sources may be read, and then ask whether they have
any other sources to share.

After approval, read only the selected content and add only those approved sources to
`source-map.md`, including access scope, sensitivity, market relevance, and limitations.
Declined or pending suggestions remain in `onboarding-state.md` and are not searched later.

Useful optional inputs include product strategy, launch briefs, roadmap context, customer or
sales notes, existing battlecards, win/loss material, repositories, developer communities,
research folders, and priority documents. Do not prescribe a fixed list.

## 5. Draft adopter positioning

Read the verified adopter homepage and any approved product sources. Fill
`adopter-positioning.md` with:

- target audiences;
- customer problem;
- category;
- value proposition;
- differentiators;
- claims;
- proof points; and
- comparison criteria.

Every material statement must cite a source or be labeled as an inference, assumption, or
missing fact. Do not add objections during initial onboarding. Do not use confidential roadmap
language as a current public claim.

Present the draft, source coverage, unsupported claims, and missing proof to the PMM. Revise as
needed. When they approve the exact draft, record `Approved`, reviewer, review date, and the
approved source-map version in the file.

## 6. Check readiness

A market is ready for the first baseline when it has:

- explicit product/geography scope;
- at least one competitor with a verified homepage;
- a canonical source map containing verified URLs and reviewed `not found` results, with no
  pending candidates;
- an adopter homepage or approved product source; and
- approved adopter positioning.

Missing competitor blog, changelog, release, pricing, product, documentation, repository, or
social sources reduces coverage but does not block the baseline. Show the missing categories
before proceeding.

## 7. Run the first baseline

Follow `references/RUN-workflow.md` in `baseline` mode. Create the first registry, evidence
log, comparative positioning context, trackers, and briefing.

If meaningful source categories are missing, label the briefing `LIMITED COVERAGE` near the
top. Explain:

- what was reviewed;
- what was unavailable or unverified;
- which claims or comparisons remain premature;
- how confidence was affected; and
- the highest-value source to add next.

Do not delay a useful website-only baseline merely because optional internal context is
missing.

## 8. Recommend enrichment

After the baseline, use actual evidence gaps to propose additional competitor sources. Start
from links or source families discoverable from the verified competitor websites. Typical
examples include customer stories needed to assess adoption, a release archive needed to
establish shipping dates, a pricing FAQ needed to resolve packaging, or an official account
needed to confirm launch messaging.

Walk the PMM through the single highest-value missing source first. For every new candidate,
repeat the same flow:

```text
Propose → PMM verifies → save to source-map.md → use in a later run
```

Then update `onboarding-state.md` to `Complete` and record the next recommended action.

## Resume behavior

On resume, show the market, completed stages, pending verification decisions, positioning
status, baseline status, and next action. Never reinterpret a pending candidate as verified or
an unreviewed positioning draft as approved.
