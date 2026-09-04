# Complete fictional example

Everything in this example is invented. Organizations, products, quotes, events, sources,
people, and results are fictional. Reserved `.invalid` URLs deliberately do not resolve.

The example shows the full first-run onboarding and limited baseline for a fictional
developer-tools product in one geography. Read the files in this order:

| File | What it demonstrates |
|---|---|
| [`onboarding-state.md`](fictional-devtools/onboarding-state.md) | Homepage-led discovery, source decisions, internal metadata suggestions, approvals, and next-source recommendation |
| [`market-pack.yaml`](fictional-devtools/market-pack.yaml) | Product-geography boundary, adopter website, competitor homepages, and market-specific file paths |
| [`source-map.md`](fictional-devtools/source-map.md) | Canonical verified competitor, adopter, Slack, Drive, local, and community sources |
| [`adopter-positioning.md`](fictional-devtools/adopter-positioning.md) | Sourced audience, problem, category, value, differentiation, claims, proof, and comparison criteria approved before analysis |
| [`competitor-registry.md`](fictional-devtools/competitor-registry.md) | Durable competitor facts and narrative populated by the baseline |
| [`positioning-context.md`](fictional-devtools/positioning-context.md) | Post-research counter-positioning, concessions, and gaps |
| [`stakeholder-lens.yaml`](fictional-devtools/stakeholder-lens.yaml) | Optional priorities used to rank the briefing |
| [`run-record.md`](fictional-devtools/run-record.md) | Scope, loaded inputs, stage history, limitations, and resume point |
| [`evidence-log.md`](fictional-devtools/evidence-log.md) | Accepted, conflicting, private, and rejected records plus coverage |
| [`draft-briefing.md`](fictional-devtools/draft-briefing.md) | The finished evidence-backed briefing and proposed changes |
| [`trackers.md`](fictional-devtools/trackers.md) | Proposed battlecard and narrative rows after review |

## What happens in the run

1. The PMM supplies the LaunchPad website, a United States product scope, and three competitor
   homepages. The agent creates market `fictional-devtools-us`.
2. The agent follows those homepages to propose product, pricing, blog, changelog, release,
   documentation, repository, and social sources. The PMM verifies the links before the agent
   writes `source-map.md`.
3. The agent inspects only Slack and Drive metadata, suggests likely channels and documents,
   receives content-access decisions, and asks for other sources.
4. The agent drafts `adopter-positioning.md` from the verified LaunchPad sources. The PMM
   approves it with explicit missing-proof limitations.
5. The agent runs a baseline for `2026-06-01` through the exclusive end date `2026-08-26`.
   Collection finds a fictional BluePeak dashboard release and documentation, a changed
   homepage headline, unchanged pricing, one community report, one private local note, and a
   search snippet that is rejected as final evidence.
6. The evidence review accepts the first-party sources, keeps the community report at low
   confidence, restricts the private note to internal output, and excludes the snippet.
7. Synthesis concludes that BluePeak expanded its narrative from individual deployment speed
   to team visibility. LaunchPad has a reviewed release-to-adoption differentiator but no
   dashboard-comparison response, so the run proposes one battlecard gap.
8. The stakeholder lens elevates this as the one executive signal because it affects the
   configured team-adoption priority. The lens does not alter confidence or public safety.
9. The briefing is labeled `LIMITED COVERAGE`, explains the missing adoption proof, and asks
   the PMM to verify the proposed BluePeak customer-stories source next.
10. The proposed registry and tracker changes remain pending until the exact draft is reviewed.

## Optional controller example

The JSON fixtures in `fixtures/` exercise the bundled deterministic controller using the same
fictional market. They are intentionally more mechanical than the document-led example. Use
them when testing structured manifests and approvals; they are not required for a normal run.
