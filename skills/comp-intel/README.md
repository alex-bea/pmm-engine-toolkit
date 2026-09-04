# Competitive-intelligence starter kit

This package is a reusable version of a working competitive-intelligence practice. It gives
an AI coding agent the analyst instructions, templates, review gates, and fictional example
needed to run the practice with your sources and your market context.

The default workflow is document-led. You do not need the bundled Python controller, a
specific connector, or a particular AI product. Claude Code, Codex, or another agent can
follow the same steps as long as it can read local files and access the sources you authorize.

## Install

Copy the entire `comp-intel` directory into the skill location used by your agent. Keep its
subdirectories together so all relative links resolve.

- Claude Code repository install: `.claude/skills/comp-intel/`
- Codex repository install: `.agents/skills/comp-intel/`
- Source toolkit: `skills/comp-intel/`

Then ask the agent to use `comp-intel` or invoke `$comp-intel` in runtimes that support
explicit skill names.

## Your first 30 minutes

Start with your product website plus competitor names and homepages. Ask:

```text
Use $comp-intel to set up this market and run my first baseline.
```

The agent will:

1. create a separate workspace for the product, geography, or product-geography scope;
2. use each competitor homepage to propose official product, pricing, blog, changelog,
   release-note, documentation, repository, and social sources;
3. ask you to verify those links before saving them to the canonical source map;
4. inspect available Slack and Drive metadata, suggest a manageable set of likely sources,
   and ask permission before reading any content;
5. ask whether you have other useful sources;
6. draft your product positioning from approved sources and revise it with you;
7. record your positioning approval; and
8. run the first baseline, clearly labeling limited coverage and recommending what to add next.

The target is about 30 minutes of PMM attention. Research and rendering may continue after the
interactive setup. Read `references/RUN-onboarding.md` for the exact procedure.

## What to bring and where it goes

You can start with only the first two rows. The agent proposes the rest and records each
decision as setup progresses.

| Information or source | Required to start? | Saved in |
|---|---|---|
| Product name, website, and product/geography scope | yes | `market-pack.yaml` |
| Competitor names and homepages | yes | `market-pack.yaml` |
| Proposed competitor product, pricing, blog, changelog, release, docs, repository, and social links | agent discovers; PMM verifies | Pending in `onboarding-state.md`; verified results in `source-map.md` |
| Approved product docs, positioning, strategy, priorities, or proof | no | Access record in `source-map.md`; synthesized position in `adopter-positioning.md` |
| Approved Slack channels, Drive files, local notes, or other internal sources | no | `source-map.md` with approved access scope and sensitivity |
| Existing competitor facts or past narrative captures | no | `competitor-registry.md` and, when comparative, `positioning-context.md` |
| Optional stakeholder or business priorities | no | `stakeholder-lens.yaml` |

## Files the setup creates

Create an adopter-owned folder outside the installed skill and copy these templates into it:

| Copy this file | What you fill in |
|---|---|
| `assets/market-pack-template.yaml` | Market name, competitor roster, analysis categories, and date policy |
| `assets/onboarding-state-template.md` | Setup progress, pending source candidates, approvals, and safe resume point |
| `assets/source-map-template.md` | Verified competitor and adopter sources used by future runs |
| `assets/adopter-positioning-template.md` | Approved audience, problem, category, value, differentiation, claims, proof, and comparison criteria |
| `assets/competitor-registry-template.md` | Durable competitor facts, current narrative, watch items, and source dates |
| `assets/positioning-context-template.md` | Post-research competitor comparisons, counters, concessions, and missing responses |
| `assets/stakeholder-lens-template.yaml` | Optional decision priorities used to rank—not manufacture—signals |
| `assets/tracker-templates.md` | Battlecard gaps, narrative changes, and unconfirmed win/loss signals |
| `assets/run-record-template.md` | Mode, scope, loaded inputs, stage history, and safe resume point |
| `assets/evidence-log-template.md` | Source coverage plus accepted, rejected, conflicting, and limited evidence |
| `assets/output-template.md` | The briefing produced for each run |

Follow `references/DOC-setup-and-mapping.md` for the setup checklist. The complete fictional
worked example starts at `examples/EX-synthetic.md`.

## Run it

Useful prompts include:

```text
Use $comp-intel to set up a competitor registry and source map for this market.
```

```text
Use $comp-intel to run a standard scan for [market] from [start date] through [end date].
Use my files in [folder], stop for evidence review, and do not update the registry yet.
```

```text
Use $comp-intel to resume run [run ID] from evidence review and prepare the draft briefing.
```

The runbook supports four modes:

- `baseline`: establish the first current-state registry with a longer adopter-chosen window;
- `standard`: scan a recent absolute window and report material changes;
- `collection-only`: gather and normalize evidence, then stop;
- `resume`: continue from saved evidence without silently recollecting it.

## What each package document does

| Document | Purpose |
|---|---|
| `SKILL.md` | Routes the agent, states boundaries, and defines the end-to-end output contract |
| `references/RUN-onboarding.md` | Guides first-run source discovery, verification, positioning approval, baseline, and enrichment |
| `references/RUN-workflow.md` | Gives the exact collection, analysis, review, and update procedure |
| `references/REF-analyst-contract.md` | Defines evidence quality, analyst judgment, gap rules, and executive-writing standards |
| `references/DOC-setup-and-mapping.md` | Shows how to replace placeholders with your market, sources, permissions, and owners |
| `references/DOC-evidence-and-claims.md` | Defines the evidence log and rules for claims, dates, conflicts, and confidence |
| `references/DOC-review-and-apply.md` | Defines the human review gates and safe local-update procedure |
| `references/DOC-troubleshooting.md` | Explains safe degradation and failure handling |
| `assets/*-template.*` | Provides blank, reusable working files for the adopter's own context |
| `examples/EX-synthetic.md` | Walks through a complete fictional run and links each filled example file |
| `scripts/` and `assets/schemas/` | Optional deterministic controller for teams that need machine-checked manifests and approvals |

## Safety boundary

Keep live source mappings, customer or deal context, private messages, stakeholder profiles,
credentials, evidence, reports, registries, and trackers in the adopter-owned folder—not in
the installed skill or a public fork. The skill never grants authority to publish, message
people, change a CRM, or alter a battlecard outside the reviewed local workflow.
