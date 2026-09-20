# Competitive-intelligence starter kit

This package is a reusable version of a working competitive-intelligence practice. It gives
an AI coding agent the analyst instructions, templates, review gates, and fictional example
needed to run the practice with your sources and market context.

The default workflow is document-led. You do not need the bundled Python controller, a
specific connector, or a particular AI product. Claude Code, Codex, or another agent can
follow the same method when it can read local files and access sources you authorize.

## Install

Copy the entire `comp-intel` directory into the skill location used by your agent. Keep its
subdirectories together so all package-relative links resolve.

- Claude Code repository install: `.claude/skills/comp-intel/`
- Codex repository install: `.agents/skills/comp-intel/`
- Source toolkit: `skills/comp-intel/`

Then ask the agent to use `comp-intel` or invoke `$comp-intel` in runtimes that support
explicit skill names.

## Setup

`comp-intel` uses the `configured-sources` profile. A live organizational run requires a
reviewed source map, approved adopter positioning, a competitor registry, authorized source
access, reviewer roles, and adopter-owned local destinations.

Detailed installation and first-run guidance lives in
`references/REF-comp-intel-setup-contract.md`. Normal analysis lives in
`references/RUN-workflow.md`; when setup is `ready`, the normal route does not load the setup
contract.

Keep completed setup state outside the installed package at stable workspace-owned paths:

```text
{authorized-workspace}/.pmm-skills/comp-intel/setup-config.yaml
{authorized-workspace}/.pmm-skills/comp-intel/setup-receipt.yaml
```

Start from `assets/setup-config.yaml` and `assets/setup-receipt.yaml`. The receipt status means:

- `ready`: package and configuration identities match and every required check passes;
- `missing`: required setup state or the receipt does not exist;
- `stale`: package, configuration, setup contract, or required mapping changed; and
- `blocked`: a required source, permission, path, destination, or validation check failed.

Dates in the receipt are audit metadata, not automatic expiry. Never put credentials in the
configuration or receipt. A secret belongs in the adopter's normal credential mechanism and
the setup file records only the mechanism and required permission.

### Safe setup test

Before connecting organizational sources, follow
`examples/fixtures/setup-smoke-test.md` with the fictional
`examples/fixtures/setup-config.yaml` and `examples/fixtures/setup-receipt.yaml`. Use a copied
package and a separate temporary workspace. The test disables live web, communication,
repository-host, publishing, messaging, notifications, scheduling, approval creation, and
production writes.

### Diagnose and repair

Ask the agent to use `$comp-intel` to diagnose setup. It will compare package and configuration
identity, validate required mappings and permissions, test local destinations without
overwriting data, and name the exact repair. Repair updates only confirmed setup state and
preserves existing evidence, registries, trackers, approvals, and reports.

## First live setup

You can begin with an adopter website plus competitor names and homepages:

```text
Use $comp-intel to set up this market and prepare it for a first baseline.
```

The agent will:

1. create a separate adopter-owned workspace for the selected market;
2. propose official product, pricing, blog, changelog, release, documentation, repository,
   and social sources from supplied homepages;
3. ask you to verify candidates before writing them to the canonical source map;
4. inspect only available internal-source metadata, then request permission before reading
   content;
5. ask whether you have other relevant sources;
6. draft adopter positioning from approved sources for your review;
7. verify required paths, permissions, reviewers, and local destinations;
8. record a digest-bound `ready` receipt outside the package; and
9. enter `references/RUN-workflow.md` in `baseline` mode.

Research and rendering may continue after the interactive decisions. Unverified candidates
stay in `onboarding-state.md`; they never become canonical sources automatically.

## Adopter-owned working files

Copy these templates into the configured market and run directories, never into the installed
skill as live state:

| Template | Purpose |
|---|---|
| `assets/onboarding-state-template.md` | Setup progress, pending source candidates, approvals, and resume point |
| `assets/market-pack-template.yaml` | Market boundary, roster, aliases, analysis categories, and date policy |
| `assets/source-map-template.md` | Verified competitor, adopter, internal, local, and community sources |
| `assets/adopter-positioning-template.md` | Approved audience, problem, category, value, claims, proof, and comparison criteria |
| `assets/competitor-registry-template.md` | Durable facts, current narrative, pricing, watch items, and source dates |
| `assets/positioning-context-template.md` | Competitor comparisons, counters, concessions, gaps, and watches |
| `assets/stakeholder-lens-template.yaml` | Optional role-based priorities used to rank, not manufacture, signals |
| `assets/tracker-templates.md` | Battlecard gaps, narrative changes, and unconfirmed evaluation signals |
| `assets/run-record-template.md` | Scope, inputs, capabilities, stage history, artifacts, and resume point |
| `assets/evidence-log-template.md` | Source coverage plus accepted, rejected, conflicting, and limited evidence |
| `assets/output-template.md` | Evidence-backed briefing and proposed state changes |

The fictional HarborKey example begins at `examples/EX-synthetic.md` and fills all eleven
human-readable templates at mature depth using only invented facts and reserved `.invalid`
URLs.

## Run it

Useful prompts include:

```text
Use $comp-intel to run a standard scan for [market] from [start date] through [end date].
Stop for evidence review and do not update the registry yet.
```

```text
Use $comp-intel to resume run [run ID] from evidence review and prepare the draft briefing.
```

The sole normal runbook, `references/RUN-workflow.md`, supports:

- `baseline`: establish the first current-state registry with an adopter-chosen window;
- `standard`: scan a recent absolute window and report material changes;
- `collection-only`: gather and normalize evidence, then stop; and
- `resume`: continue from saved evidence without silently recollecting it.

## Package map

| Document | Purpose |
|---|---|
| `SKILL.md` | Routes ready normal work, explicit setup, and non-ready states |
| `references/RUN-workflow.md` | Sole normal collection, analysis, review, and local-update workflow |
| `references/REF-comp-intel-setup-contract.md` | Conditional installation, mappings, permissions, test, receipt, diagnosis, and repair |
| `references/REF-analyst-contract.md` | Evidence quality, analyst judgment, gap rules, and executive-writing standards |
| `references/DOC-evidence-and-claims.md` | Evidence and claim dates, conflicts, confidence, and traceability |
| `references/DOC-review-and-apply.md` | Human review gates and safe local apply |
| `references/DOC-troubleshooting.md` | Safe degradation and workflow failure handling |
| `assets/*-template.*` | Blank reusable market, evidence, registry, tracker, and report structures |
| `examples/EX-synthetic.md` | Full-depth fictional baseline and setup-test entrypoint |
| `scripts/` and `assets/schemas/` | Optional deterministic controller and machine-readable contracts |

## Safety boundary

Keep live mappings, customer or deal context, private messages, stakeholder profiles,
credentials, setup state, evidence, reports, registries, and trackers in the adopter-owned
workspace—not in the installed skill or a public fork. Local evidence or state approval does
not authorize publication, messages, CRM changes, schedules, notifications, or other external
mutation.
