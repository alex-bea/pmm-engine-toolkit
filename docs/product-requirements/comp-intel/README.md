# Competitive Intelligence for Codex — Draft Product Requirements

This directory is the public, product-agnostic specification for moving a mature
competitive-intelligence workflow from Claude to Codex. It is a design and implementation
planning suite, not a statement that the target product is already available.

The current `skills/comp-intel/` package remains a lightweight, evidence-bound public skill.
The documents here define the larger target: deterministic workflow control, reusable data
contracts, review-gated state changes, adapter-based collection, public golden examples,
private migration, and easy Codex Desktop installation.

All documents are `Draft`. Implementation, private cutover, GitHub release, and marketplace
submission each require the reviews and approvals specified in the suite.

## Reading order

1. [Master product requirements](DOC-comp-intel-codex-migration-prd-v1.0.md) — product
   decisions, current-state analysis, target behavior, boundaries, risks, and success
   criteria.
2. [Implementation blueprint](DOC-comp-intel-codex-implementation-blueprint-v1.0.md) —
   target architecture, package shape, schemas, controller stages, adapter seam, and delivery
   sequence.
3. Read the implementation PRD for the slice being built:
   - [Codex skill](DOC-comp-intel-codex-skill-implementation-prd-v1.0.md)
   - [Integrations](DOC-comp-intel-integrations-implementation-prd-v1.0.md)
   - [Private Claude-to-Codex migration](DOC-comp-intel-private-migration-prd-v1.0.md)
   - [Public distribution](DOC-comp-intel-public-distribution-prd-v1.0.md)
4. [Public acceptance tests](DOC-comp-intel-public-acceptance-tests-v1.0.md) — executable
   release criteria spanning static checks, adapters, offline workflows, Desktop behavior,
   security, portability, migration, and publication.

## Binding product direction

- The core is reusable and product-agnostic.
- Polygon is the public golden example, delivered in the order Chain, Payments, then
  Wallets, using approved public evidence only.
- A fully synthetic pack supports offline, deterministic validation.
- Version 1 targets Codex Desktop and preserves a clean future headless seam.
- Base integrations are web, GitHub, synthetic fixtures, and local files. Slack is optional.
- The GitHub repository is canonical. A thin plugin wrapper may make installation and
  integration mapping easier; it is not the architectural source of truth.

## Public-adopter mapping requirement

Before connecting the workflow to real organizational data, every adopter must explicitly
map and approve:

- internal product, market, competitor, and stakeholder names;
- channels, users, repositories, domains, and source queries;
- company systems, connector capabilities, and minimum permissions;
- existing intelligence records, provenance, retention, and sensitivity;
- evidence and apply reviewers, approval records, and separation of duties; and
- output locations, downstream consumers, and publication boundaries.

The public package must not infer these values, ship Polygon values as live defaults, or
copy private legacy data into public examples. Private migration evidence remains outside
this repository.

## Contributor rule

Root [`AGENTS.md`](../../../AGENTS.md) instructs Codex to load this suite whenever work
touches the competitive-intelligence skill, controller, integrations, migration, tests, or
distribution. The runtime skill remains scoped to competitive-intelligence requests and
must not activate for unrelated skill authoring.
