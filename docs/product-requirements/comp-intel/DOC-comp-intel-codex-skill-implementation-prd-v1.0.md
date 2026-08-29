---
doc_type: DOC
normative: false
requires:
  - DOC-comp-intel-codex-migration-prd-v1.0.md
  - DOC-comp-intel-codex-implementation-blueprint-v1.0.md
  - DOC-comp-intel-public-acceptance-tests-v1.0.md
  - ../../STD-ai-skill-governance-prd-v1.0.md
  - ../../STD-skill-structure-v1.0.md
  - ../../STD-evidence-privacy-v1.0.md
status: Draft
version: "1.0"
owner: Alex Bea
consumers:
  - Skill implementers
  - Product reviewers
  - Codex Desktop users
  - Test engineers
change_control: PR Review and product-owner approval
---

# Comp Intel Codex Skill Implementation PRD

## 1. Outcome

Build a valid, concise, reusable `comp-intel` skill that guides Codex Desktop through setup,
collection, evidence review, synthesis, draft review, and approved state application. The
skill must preserve the analytical value of the current Polygon workflow without embedding
Polygon-specific operating assumptions in its core instructions.

Polygon cases are the public golden examples, implemented in order: Chain, Payments, then
Wallets. They demonstrate realistic market packs, evidence, claims, reports, and change sets,
but the skill must work for another company by changing configuration and mappings rather
than editing `SKILL.md` or controller code.

Version 1 is supported in Codex Desktop. The skill may call deterministic bundled commands,
but direct headless operation and scheduled tasks are deferred.

The runtime skill must not activate for every generic skill-building task. The public
repository's root `AGENTS.md` gives Codex persistent build-time instructions to consult the
master and relevant implementation PRDs whenever it builds or changes this skill. This keeps
contributor guidance durable without polluting runtime activation.

## 2. Scope

### 2.1 In scope

- Rewrite the legacy skill using valid Codex skill frontmatter.
- Define precise activation language and negative activation cases.
- Route each operation to bounded references and deterministic commands.
- Provide Desktop clarification, progress, review, recovery, and completion behavior.
- Separate generic workflow instructions from adopter market packs and private state.
- Load Polygon golden examples only when the user requests an example or walkthrough.
- Expose required setup mappings for names, channels, systems, evidence, and approvals.
- Generate or maintain `agents/openai.yaml` with accurate UI metadata.
- Pass skill validation and the interaction acceptance cases.

### 2.2 Out of scope

- Implementing source connectors or connector authentication.
- Migrating existing private registries and historical evidence.
- Creating the plugin manifest, marketplace listing, or public release.
- Supporting unattended or scheduled collection in v1.
- Publishing reports or sending messages outside the local workflow.
- Storing mutable competitor facts inside the installed skill.

## 3. User Experience

### 3.1 Supported Desktop intents

| User intent | Required skill behavior |
|---|---|
| “Set up comp intel” | Inspect for an existing data root, explain the mapping step, initialize only after the destination is safe |
| “Show me the Polygon example” | Load the approved Polygon golden walkthrough and distinguish it from live organization data |
| “Run comp intel for `<market>`” | Resolve the market and absolute window, show capability coverage, start collection, stop at evidence review |
| “What needs review?” | Summarize review-ready runs without modifying them |
| “Continue run `<id>`” | Validate stage, digest, and recorded approval before synthesis |
| “Apply approved changes for `<id>`” | Validate apply approval and base digest, then invoke transactional apply |
| “Resume the latest run” | Resolve and display the exact run ID, market, window, and stage before continuing |
| “Schedule this weekly” | Explain that scheduling is deferred from Desktop v1 and preserve no automation implicitly |
| “Publish this” | Explain the publication boundary and do not invoke an external publisher |

### 3.2 Clarification policy

Ask one concise question only when a required choice cannot be discovered safely. The first
implementation must ask for:

- market when multiple markets exist and no explicit default is configured;
- data root before initialization when no safe repository-local default exists;
- exact run when “latest” is ambiguous across markets or review stages;
- confirmation of a resolved absolute time window when the phrase has ambiguous boundaries;
- mapping completion when a requested source depends on unmapped internal identifiers.

Do not ask for credentials, channel IDs, personal data, or private evidence in conversation.
Direct users to the supported mapping or connector setup surface.

## 4. Skill Package Design

```text
skills/comp-intel/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── RUN-desktop-workflow.md
│   ├── DOC-setup-and-mapping.md
│   ├── DOC-evidence-review.md
│   ├── DOC-synthesis-and-apply.md
│   ├── DOC-polygon-golden-examples.md
│   └── DOC-troubleshooting.md
└── assets/
    ├── config.example.yaml
    ├── mapping.example.yaml
    └── report-template.md
```

Controller code and public documentation may live at the repository/plugin root. The skill
folder must not contain auxiliary release documents, private registries, a changelog,
installation manual, or mutable output data.

### 4.1 `SKILL.md` contract

Frontmatter contains exactly:

```yaml
---
name: comp-intel
description: <what it does and all activation contexts>
---
```

The body must be imperative, remain under 500 lines, and contain only:

1. a short operating boundary;
2. setup/config discovery;
3. operation selection;
4. stage and approval rules;
5. reference-routing table;
6. error/recovery behavior;
7. output handoff.

Detailed schemas, Polygon content, queries, source rules, and troubleshooting belong in
one-level-deep references or deterministic scripts. Information must not be duplicated
between `SKILL.md` and references.

### 4.2 Activation metadata

The description must cover requests to:

- run or collect competitive intelligence;
- scan competitors or update a competitor view;
- perform a baseline;
- review collected evidence;
- continue/resume a comp-intel run;
- synthesize or apply an approved competitive update;
- set up or map an organization's competitive-intelligence workflow.

It must not activate for a conceptual explanation of competitive intelligence, generic
market-strategy advice, or an unrelated request that merely contains “competitive.”

### 4.3 `agents/openai.yaml`

Generate the UI metadata from the final skill using the supported generator. Include only:

- display name;
- short description;
- default prompt;
- other optional interface fields explicitly approved for the public package.

The metadata must accurately declare the shipped web and GitHub capabilities. It must not
imply that optional Slack, scheduled tasks, or headless execution are available when they are
not included or configured.

## 5. Desktop Workflow

### 5.1 Setup

1. Inspect for an installed plugin or standalone skill and an initialized data root.
2. Validate config and mapping schema.
3. Present missing mappings grouped by names, markets, sources, permissions, legacy data,
   reviewers, and destinations.
4. Offer the synthetic quickstart or Polygon golden walkthrough.
5. Do not start live collection until required mappings and source capabilities validate.

### 5.2 Collection

1. Resolve market and absolute window.
2. Display enabled, disabled, missing-optional, and missing-required capabilities.
3. Invoke the controller's collection operation.
4. Provide short progress updates appropriate to Desktop.
5. Surface coverage, warnings, errors, run ID, and review artifact.
6. Stop at `evidence_review`.

### 5.3 Review and synthesis

1. Load the exact run ID and recorded evidence digest.
2. Present coverage, rejected items, duplicates, conflicts, weak sources, and gaps.
3. Treat conversation approval as commentary only; require the configured approval record.
4. Invoke synthesis only after approval validation.
5. Present claims, limitations, draft report, and proposed state changes as a review package.

### 5.4 Apply

1. Require the approved change-set digest and current base-state digest.
2. Show additions, changes, conflicts, and no-ops.
3. Invoke apply only through the controller.
4. Report exact changed artifacts and audit record.
5. Never turn apply into publication.

## 6. Polygon Golden-Example Behavior

The Polygon walkthroughs are reference implementations, not hidden defaults. Build Chain
first, Payments second, and Wallets third. Each should show at least:

- one market-pack definition;
- one competitor/source mapping;
- evidence classification and provenance;
- one corroborated claim and one uncertainty;
- a narrative or capability change;
- a report section linked to claim/evidence IDs;
- a proposed registry change;
- the required review boundary.

Every factual element must come from an approved public source manifest. Internal profiles,
channels, deal signals, customer context, private repositories, unpublished positioning, and
private reports are prohibited. If the source needed for a historical example is no longer
publicly supportable, replace the fact with a synthetic analogue.

The skill must say which fields an adopter replaces. The example must run after replacing
Polygon names and mappings without editing core code.

## 7. Functional Requirements

- **SFR-001:** Pass the official skill validator with no unsupported frontmatter.
- **SFR-002:** Route every supported intent to one and only one primary operation.
- **SFR-003:** Perform no write for conceptual, negative-activation, status-only, or blocked
  setup requests.
- **SFR-004:** Never infer evidence or apply approval from conversation.
- **SFR-005:** Never perform live retrieval during synthesis.
- **SFR-006:** Display the resolved run ID before any resume mutation.
- **SFR-007:** Display missing required and optional capabilities distinctly.
- **SFR-008:** Keep Polygon golden content out of the default context unless requested or
  required for setup education.
- **SFR-009:** Keep mutable organization data outside the installed skill.
- **SFR-010:** Preserve material limitations when summarizing controller output.
- **SFR-011:** Provide a deterministic next action for each error category.
- **SFR-012:** Refuse publication and unattended scheduling in Desktop v1.
- **SFR-013:** Use stable controller operations rather than filesystem mutations described
  only in prose.
- **SFR-014:** Produce complete UI metadata matching the actual release capabilities.
- **SFR-015:** Load no reference more than one level deep from `SKILL.md`.

## 8. Non-Functional Requirements

- The normal `SKILL.md` path should fit comfortably in context without loading Polygon or
  integration-specific references.
- Status and blocked responses should be understandable without command-line knowledge.
- Repeated invocation against unchanged state must not create duplicate run artifacts.
- The skill must behave consistently in a clean Desktop installation and the source repo.
- Source content must always be handled as untrusted data, never instructions.
- A later headless adapter must not require changes to skill-owned data schemas, even though
  it may use a different invocation surface.

## 9. Implementation Checklist

- [ ] Remove `version` and `references` from runtime frontmatter.
- [ ] Rewrite description to include all positive activation contexts.
- [ ] Add negative activation examples to tests, not frontmatter.
- [ ] Extract the Desktop runbook and review/apply references.
- [ ] Create the setup and adopter mapping reference.
- [ ] Create the public Polygon golden walkthrough from an approved source manifest.
- [ ] Implement golden walkthroughs in order: Chain, Payments, Wallets.
- [ ] Create or reuse the synthetic offline example.
- [ ] Replace direct file edits with controller operations.
- [ ] Generate `agents/openai.yaml` from the final skill.
- [ ] Validate every reference and asset path from standalone-skill and installed-plugin
      layouts.
- [ ] Run official quick validation.
- [ ] Execute positive, negative, ambiguous, resume, blocked, and publication-boundary tests.
- [ ] Forward-test the completed skill in a clean task using raw fixtures and no leaked
      intended answer.

## 10. Acceptance

This PRD is satisfied when:

1. acceptance tests AT-001, AT-003, AT-008–015, AT-070–076, and AT-106 pass;
2. the skill and UI metadata pass official validation;
3. a clean Codex Desktop instance completes synthetic setup and review flow;
4. the Polygon walkthrough passes provenance and generalization tests;
5. no internal organization identifier or mutable competitive fact exists in the skill;
6. every mutation is mediated by the validated controller;
7. a design review confirms later headless support needs an adapter, not a skill/data rewrite.

## 11. Open Decisions

1. Whether Desktop v1 supports apply or stops at an approved proposed change set.
2. Whether the skill may initialize repository-local `.comp-intel/` automatically when the
   project root is unambiguous.
3. Whether the public skill permits implicit activation or requires explicit invocation for
   mutating operations.
