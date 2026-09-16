---
doc_type: REF
normative: true
requires:
  - RUN-govern-skills-setup-workflow-v1.0.md
  - STD-ai-skill-governance-prd-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-runtime-enforcement-v1.0.md
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Claude Code users
  - Codex users
  - repository owners
  - new adopters
change_control: Project owner approval
---

# Governance Adoption Guide

## Purpose

Help a capable local agent copy the useful governance architecture into an existing
repository. The guide starts with readable documents and repository conventions. It does
not require an installer, plugin, registry, hook, CI workflow, hosted service, or new tool.

The agent may claim only what it observes. A written policy can guide behavior, but it does
not prove that a validator, hook, capability restriction, human approval service, or
publisher exists.

## 1. Inspect before asking setup questions

1. Resolve the target repository and applicable instruction files.
2. Inspect Git state without modifying it.
3. Inventory existing skills, runbooks, standards, references, templates, examples,
   registries, validators, CI, hooks, and external-boundary configuration.
4. Identify existing naming, metadata, ownership, lifecycle, dependency, and review
   conventions.
5. Compare those conventions with this package and list compatible reuse, conflicts, and
   missing decisions.
6. Infer routine facts from evidence. Ask the owner only for material scope, authority, or
   destination decisions that inspection cannot resolve.

Do not create directories, copy templates, enable tools, or trust a hook during inspection.

## 2. Explain the primitives

Use the separation below when proposing architecture:

| Primitive | Owns | Must not silently own |
|---|---|---|
| `SKILL.md` | Discovery, routing, and shared boundaries | A long mode-specific procedure |
| `RUN-*.md` | Ordered setup and execution | General knowledge unrelated to execution |
| `STD-*.md` | Stable reusable rules | Adopter-specific mutable configuration |
| `REF-*.md` | Focused knowledge or mode guidance | The canonical workflow |
| Template | Blank artifact shape | Real adopter data |
| Example | Fictional completed depth | Evidence for a real decision |
| Script | Repeatable deterministic mechanics | Product judgment or human authority |
| Policy decision | Shared allow/deny reasoning | Harness payload parsing |
| Harness adapter | Payload normalization | Duplicated policy |
| Capability boundary | Removal of a prohibited capability | A claim based only on model compliance |

This architecture makes later changes local: update a trigger in `SKILL.md`, insert a step
in the RUN, revise a reusable rule in an STD, expand mode knowledge in a REF, evolve artifact
shape in a template, clarify depth in an example, or change repeatable mechanics in a script.

## 3. Report setup readiness

Produce this table before a file plan:

| Layer or blocker | Current state | Evidence | Gap | Proposed action | Approval authority | Verification |
|---|---|---|---|---|---|---|

Use only:

- `ready` — directly verified for the named scope;
- `configured-inactive` — present but deliberately disabled or untrusted;
- `missing` — no qualifying implementation was found;
- `blocked` — a conflict, failure, or missing decision prevents progress; or
- `not-applicable` — the adopter explicitly excluded the layer's side effect.

For documents-only adoption, assess repository instructions, skill and workflow structure,
document metadata, dependencies, templates/examples, approval wording, destinations, and
fixture-test readiness. Assess registries, validators, CI, hooks, capability restrictions,
external approval, and publishers separately only when present or selected.

## 4. Choose the smallest useful scope

Default to documents only. The owner may separately select:

1. a canonical skill registry;
2. a local static validator;
3. a required CI check;
4. a Claude Code or Codex runtime guard;
5. administrator-protected filesystem, network, tool, or credential boundaries;
6. an external approval verifier; or
7. a narrow publisher adapter.

Selecting one does not select the others. Do not infer identities, owners, lifecycle states,
release destinations, bypass permissions, or administrator authority.

## 5. Prepare the exact file plan

Map each proposed artifact to an existing compatible convention or explain why a new one is
needed. For every path, show:

- `add`, `modify`, `leave unchanged`, or `conflict`;
- the primitive role and governing standard;
- whether content is copied, adapted, or newly authored;
- the selected enforcement class;
- adopter-owned configuration or state used by it;
- approval authority; and
- a verification method.

The plan must include source and destination mappings, expected fixture artifacts, and the
setup-receipt path. Stop before writing. Approval applies only to the displayed boundary;
a material path or content change returns the plan to review.

## 6. Apply documents-first adoption

After scoped approval:

1. Recheck Git state and target collisions.
2. Apply only approved paths.
3. Reuse compatible local conventions and preserve unrelated content.
4. Keep adopter mapping, configuration, state, output, and receipts outside the package.
5. Validate metadata, dependencies, links, exact-one-RUN structure, and repository-specific
   rules.
6. Run the isolated fictional fixture and write the receipt.

Documents-only adoption can end `ready` for its named scope. Describe it as
`instruction-only`, not technically enforced.

## 7. Add optional validation or enforcement

When the owner selects an optional layer, read the corresponding STD first. Prefer one
shared deterministic rule or policy decision with thin adapters. Require administrator
activation and negative tests for runtime or capability layers.

For strong approval or publication boundaries, the ordinary agent must be unable to rewrite
the controlling policy, forge authority, reach alternate publisher paths, or access
publisher credentials. A repository-local hook alone is a runtime guard.

## 8. Verify and report

Run positive and negative checks proportional to the selected scope. For each denied action,
verify the side effect did not occur. Record failed, skipped, unavailable, and
not-applicable checks distinctly.

End with one overall status:

- `ready` for every required check in the named scope;
- `ready-with-optional-limitations` when only non-required integrations are unavailable; or
- `blocked` when a required check or decision is unresolved.

Name the scope directly, for example: “ready for documents-only skill governance.” Do not
say governance is generally enforced.

## 9. Maintain the pattern

When updating later, begin at the primitive that owns the change:

- invocation problem: `SKILL.md`;
- execution order or gate: RUN;
- reusable rule: STD;
- detailed mode guidance: REF;
- artifact structure: template;
- demonstrated depth or edge case: example;
- repeatable mechanical failure: script or validator;
- cross-harness decision drift: shared policy plus adapter tests;
- bypass risk: capability boundary or external authority.

Update dependencies, versioned documents, examples, tests, and the setup receipt when their
contracts change. Retaining small superseded documents is acceptable when the repository's
lifecycle policy favors explicit history.

## Stop conditions

Stop and keep the affected scope blocked when:

- repository instructions or the target root are unresolved;
- a packaged default conflicts with a canonical adopter convention;
- required destinations are unsafe or outside approval;
- proposed paths differ from the approved plan;
- an approval, owner, lifecycle state, or external authority is unverified;
- a runtime or capability claim cannot be proven;
- a required negative test fails or is not run; or
- the setup receipt is stale.
