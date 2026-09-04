# Competitive briefing: Fictional developer observability

Status: Draft — example only; all content is fictional.

Coverage status: **LIMITED COVERAGE**

| Run | Mode | Window | Prepared | Evidence review |
|---|---|---|---|---|
| fictional-devtools-us-2026-08-26 | baseline | 2026-06-01 to 2026-08-26 | 2026-08-26 | Approved by Fictional PMM, 2026-08-26 10:00Z |

## Top signal

BluePeak expanded from an individual deployment-speed story to team-level visibility and
released a team usage dashboard (Observed: E-001, E-002, E-003). This matters to the fictional
team-adoption priority because LaunchPad has no reviewed response for team reporting
(Inference: C-002). Ask the positioning owner to define the comparison criterion before the
next enablement update (Recommendation: C-003).

## Competitor activity

### BluePeak

- **What changed — Observed:** BluePeak released and documented a team usage dashboard and
  changed its homepage headline toward what teams ship and use (E-001, E-002, E-003).
- **Why it matters — Inference:** The combined product and headline change suggests an
  expansion from individual developers toward team buyers (C-002).
- **Affected audience/use case:** Engineering teams evaluating shared release visibility.
- **Positioning coverage:** MISSING for team-level dashboards; STRONG for connecting release
  health to feature adoption.
- **Recommended response:** Open one gap for a reviewed dashboard-comparison criterion.
- **Limitations:** No evidence establishes adoption, dashboard export, role-based access, or
  which plan includes the capability.

### CedarWorks

No material verified change. One low-confidence community report is retained as attributed
evidence (E-005) and is not sufficient for an executive signal or registry change.

## Narrative shifts

| Competitor | Type | Prior | Current | Implication | Evidence |
|---|---|---|---|---|---|
| BluePeak | expansion | “Ship without guessing.” | “See what every team ships and uses.” | Inference: BluePeak is broadening toward team adoption and leadership visibility. | E-008, E-003 |

## Positioning and battlecard gaps

| Competitor claim | Coverage | Existing response | Missing piece | Evidence | Proposed owner |
|---|---|---|---|---|---|
| BluePeak offers a team usage dashboard. | MISSING | No reviewed dashboard comparison | Decision criterion and proof for LaunchPad's team reporting | E-001, E-002 | Fictional positioning owner |

## Stakeholder relevance

The signal maps directly to the configured Team adoption priority. The lens elevated it but did
not change its evidence labels, confidence, or sensitivity.

## Actions

| Action | Type | Owner | Timing | Supporting claims |
|---|---|---|---|---|
| Define and review a dashboard comparison criterion. | enablement review | Fictional positioning owner | Before next battlecard update | C-001, C-002, C-003 |
| Check dashboard plan entitlement in the next scan. | research | Fictional analyst | Next standard run | C-004 |

## Coverage

| Source class | Competitors covered | Result | Limitations |
|---|---|---|---|
| Homepage and product | BluePeak, CedarWorks, Northstar Labs | complete | Fictional sources only |
| Pricing | BluePeak, CedarWorks | partial | Northstar public pricing was not found |
| Blog, changelog, and releases | Full roster | partial | Several separate Northstar surfaces were not found |
| Documentation and repositories | Full roster | partial | No repository was found; Northstar docs were not found |
| Community and approved internal context | BluePeak, CedarWorks | partial | One isolated report; internal evidence cannot support public claims |

## Limitations and unknowns

- No evidence proves BluePeak customer adoption, dashboard export, role-based access, or plan
  entitlement.
- Northstar comparisons are premature beyond its verified homepage, product page, and blog.
- Missing source families reduce confidence in claims of market-wide completeness.

## Source enrichment

- **Highest-value source to add next:** proposed BluePeak customer-stories page at
  `https://bluepeak.example.invalid/customers/`.
- **Gap it would resolve:** whether BluePeak publishes customer adoption proof for its team
  dashboard story.
- **Verification step:** the PMM should approve, replace, or reject the candidate in
  `onboarding-state.md`; only an approved link is copied into `source-map.md` and used later.

## Claims and evidence

| Claim ID | Statement | Type | Confidence | Evidence |
|---|---|---|---|---|
| C-001 | BluePeak released and documented a fictional team usage dashboard. | observed | high | E-001, E-002 |
| C-002 | BluePeak appears to be expanding from individual developer messaging toward team visibility. | inference | medium | E-001, E-003, E-008 |
| C-003 | LaunchPad should review its dashboard comparison guidance. | recommendation | medium | C-001, C-002 |
| C-004 | BluePeak dashboard plan entitlement is unknown. | unknown | high | E-004 |

## Proposed state changes

| Target | Field/event | Prior | Proposed | Support | Decision |
|---|---|---|---|---|---|
| Registry / BluePeak | Core claim | not established | Team deployment and usage visibility | E-001, E-003 | pending |
| Registry / BluePeak | Last verified | not established | 2026-08-25 | E-001–E-004 | pending |
| Narrative tracker | New change | none | BluePeak expansion row | E-008, E-003 | pending |
| Battlecard-gap tracker | New gap | none | Team dashboard comparison criterion | E-001, E-002 | pending |
