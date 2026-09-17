# Fictional Pre-Read Sharpener Example

This example is entirely fictional. It demonstrates expected structure, source discipline,
and depth; it is not evidence for a real organization, product, customer, or market.

1. Read the fictional [`source draft`](fictional-rollout-decision/source-draft.md).
2. Compare it with the canonical [`output template`](../assets/output-template.md).
3. Review the completed
   [`review and rewrite`](fictional-rollout-decision/review-and-rewrite.md).
4. Use the compact [`behavior cases`](fixtures/behavior-cases.md) for edge-case evaluation.
5. Use the fictional [`setup smoke test`](fixtures/setup-smoke-test.md) only for persistent
   local output. It verifies package closure, YAML mappings, isolated output, receipt shape,
   conditional routing, collision behavior, and installed-package immutability.

Every factual statement in the completed rewrite is supported by the fictional source. The
example is formatting and behavior guidance only and must never supply a missing fact in
real work. Inline execution needs no setup. The fixture configuration and completed receipt
are fictional and must never be used as defaults for a real installation. A current `ready`
receipt routes persistent work directly to the normal RUN; `missing`, `stale`, and `blocked`
statuses route to the separate setup contract.
