# Complete fictional example

Everything in this example is invented. Organizations, products, quotes, events, sources,
people, and results are fictional. Reserved `.invalid` URLs deliberately do not resolve.

The example shows a standard run for a fictional developer-tools market. Read the files in
this order:

| File | What it demonstrates |
|---|---|
| [`market-pack.yaml`](fictional-devtools/market-pack.yaml) | Market boundary, roster, mode defaults, and status policy |
| [`source-map.md`](fictional-devtools/source-map.md) | Filled source targets, aliases, search terms, and permissions |
| [`competitor-registry.md`](fictional-devtools/competitor-registry.md) | Durable facts and prior narrative before the run |
| [`positioning-context.md`](fictional-devtools/positioning-context.md) | Reviewed adopter claims, counter-positioning, concessions, and gaps |
| [`stakeholder-lens.yaml`](fictional-devtools/stakeholder-lens.yaml) | Optional priorities used to rank the briefing |
| [`run-record.md`](fictional-devtools/run-record.md) | Scope, loaded inputs, stage history, limitations, and resume point |
| [`evidence-log.md`](fictional-devtools/evidence-log.md) | Accepted, conflicting, private, and rejected records plus coverage |
| [`draft-briefing.md`](fictional-devtools/draft-briefing.md) | The finished evidence-backed briefing and proposed changes |
| [`trackers.md`](fictional-devtools/trackers.md) | Proposed battlecard and narrative rows after review |

## What happens in the run

1. The operator selects `standard`, market `fictional-devtools`, and the absolute window
   `2026-08-18` through the exclusive end date `2026-08-26`.
2. The agent loads the registry, source map, positioning file, and optional product-lead lens.
3. Collection finds a fictional BluePeak dashboard release and documentation, a changed
   homepage headline, unchanged pricing, one community report, one private local note, and a
   search snippet that is rejected as final evidence.
4. The evidence review accepts the first-party sources, keeps the community report at low
   confidence, restricts the private note to internal output, and excludes the snippet.
5. Synthesis concludes that BluePeak expanded its narrative from individual deployment speed
   to team visibility. LaunchPad has a reviewed workflow-speed counter but no reviewed
   dashboard-comparison response, so the run proposes one battlecard gap.
6. The stakeholder lens elevates this as the one executive signal because it affects the
   configured team-adoption priority. The lens does not alter confidence or public safety.
7. The proposed registry and tracker changes remain pending until the exact draft is reviewed.

## Optional controller example

The JSON fixtures in `fixtures/` exercise the bundled deterministic controller using the same
fictional market. They are intentionally more mechanical than the document-led example. Use
them when testing structured manifests and approvals; they are not required for a normal run.
