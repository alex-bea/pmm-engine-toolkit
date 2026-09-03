# Setup and adopter mapping

Create a working directory owned by the adopter. Do not put live configuration, evidence,
private sources, reports, or mutable registries inside the installed skill.

## Minimum setup

Copy and fill:

1. `assets/market-pack-template.yaml` — market and roster;
2. `assets/source-map-template.md` — approved sources and searches;
3. `assets/competitor-registry-template.md` — current durable knowledge;
4. `assets/positioning-context-template.md` — reviewed claims and counter-positioning; and
5. `assets/tracker-templates.md` — empty operational trackers.

Optionally copy `assets/stakeholder-lens-template.yaml`. Create an `evidence/` folder and an
`outputs/` folder. Copy `assets/run-record-template.md` and
`assets/evidence-log-template.md` when starting each run. Suggested adopter-owned layout:

```text
competitive-intel/
├── markets/<market-id>/
│   ├── market-pack.yaml
│   ├── source-map.md
│   ├── competitor-registry.md
│   ├── positioning-context.md
│   ├── stakeholder-lens.yaml        # optional
│   └── trackers.md
├── runs/<run-id>/
│   ├── run.md
│   ├── evidence-log.md
│   ├── evidence-review.md
│   ├── draft-briefing.md
│   └── proposed-changes.md
└── outputs/
```

The layout is a convention, not a runtime requirement. Keep the same functional separation if
you use different paths.

## Map before live use

Review every item with its owner:

- organization, product, market, competitor, and alias names;
- ambiguous aliases and required context filters;
- internal channels, folders, notes, users, and permitted local roots;
- web domains, product pages, blogs, changelogs, pricing pages, and repositories;
- developer communities and official social accounts;
- connector or tool permissions and whether each source is required or optional;
- sensitivity labels, retention rules, and public-output restrictions;
- current competitor records and their last-verified dates;
- approved product claims and positioning owners;
- optional consented stakeholder priorities;
- evidence reviewer and registry-change reviewer;
- output owner, storage path, and any separate publication process; and
- downstream battlecards, sales enablement, planning, or reporting workflows.

Do not infer missing organization-specific values. Leave a visible placeholder and block only
the step that depends on it.

## Market boundaries

Write a one-paragraph market definition and explicit exclusions. A good boundary explains:

- which buyer, user, use case, or job defines competition;
- which product area the run covers;
- why each active competitor belongs;
- what adjacent tools remain watchlist only; and
- what would trigger a roster change.

Use one registry and positioning file per market when comparison criteria differ materially.

## First run

Run a baseline before recurring scans. Choose and record an absolute extended window, verify
the full roster, capture the current narrative and pricing state for every competitor, seed the
gap tracker, and review all durable facts before applying them.

The fictional package under `examples/fictional-devtools/` shows every minimum file filled in.

## Optional structured setup

The controller can initialize a separate fictional data root:

```text
python3 <skill-directory>/scripts/comp_intel.py init --data-root <explicit-empty-path>
python3 <skill-directory>/scripts/comp_intel.py doctor --data-root <explicit-path> --market synthetic-devtools --json
```

It creates JSON-compatible structured files for deterministic testing. Use those contracts only
if you want controller-managed runs; the Markdown templates are the default human-readable
starter kit.
