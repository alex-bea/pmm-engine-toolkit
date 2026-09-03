# Competitive Intelligence for Codex — Archived Design Exploration

This directory preserves an earlier proposal for turning a mature competitive-intelligence
workflow into a larger Codex-specific product. The project later chose a smaller direction:
publish the proven analyst framework, fillable structures, and fictional example so users can
run them with their own agent and source access.

The shipped [`skills/comp-intel/`](../../../skills/comp-intel/README.md) package is the current
product direction and source of truth. The documents here are non-binding design history. Do
not use their Codex-only, bundled-adapter, real-company golden-pack, private-cutover, or plugin
requirements to expand the package unless a later product decision explicitly revives them.

All documents remain `Draft` and `normative: false`. They do not authorize implementation,
private cutover, release, or marketplace submission.

## Relationship to other design history

The [source inventory](../../DOC-comp-intel-source-inventory-v1.0.md), the
[skill-expansion product draft](../../DOC-comp-intel-product-requirements-v1.0.md), and this
suite record successive design explorations. None overrides the shipped package. Use them only
to understand prior tradeoffs or recover a deliberately revived requirement.

## Reading order for the archive

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

## Historical proposed direction

The linked documents proposed a reusable core, Codex Desktop target, bundled adapters,
real-company public examples, private migration, and a thin plugin wrapper. These decisions are
preserved for traceability but are not current requirements.

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

Root [`AGENTS.md`](../../../AGENTS.md) points maintainers to the shipped package and treats this
suite as design history. The runtime skill remains scoped to competitive-intelligence requests
and must not activate for unrelated skill authoring.
