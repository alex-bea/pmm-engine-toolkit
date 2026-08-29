---
doc_type: DOC
normative: false
requires:
  - DOC-comp-intel-codex-migration-prd-v1.0.md
  - DOC-comp-intel-codex-implementation-blueprint-v1.0.md
  - DOC-comp-intel-public-acceptance-tests-v1.0.md
  - DOC-comp-intel-codex-skill-implementation-prd-v1.0.md
  - DOC-comp-intel-integrations-implementation-prd-v1.0.md
  - ../../STD-evidence-privacy-v1.0.md
  - ../../STD-approval-gates-v1.0.md
status: Draft
version: "1.0"
owner: Alex Bea
consumers:
  - Migration implementers
  - Private data owners
  - Product reviewers
  - Test engineers
change_control: PR Review and explicit migration approval
---

# Comp Intel Private Claude-to-Codex Migration PRD

## 1. Outcome

Move the private competitive-intelligence workflow from Claude to Codex Desktop without
losing source provenance, market coverage, current competitor state, historical evidence,
review status, or rollback capability. Convert reusable workflow behavior into the public
product while keeping internal names, channels, systems, stakeholder profiles, positioning,
deal intelligence, and unpublished product context in private adopter-owned market packs and
data roots.

The migration also produces the public Polygon golden examples in approved order: Chain,
then Payments, then Wallets. Those examples must be rebuilt from approved public sources;
they are not sanitized exports of private registries or reports.

## 2. Current Private Migration Surface

The migration must inventory and classify at least:

| Surface | Current role | Target |
|---|---|---|
| `skills/comp-intel/SKILL.md` | Claude/Codex discovery and operating instructions | Replaced by public generic skill plus private config |
| Runbook and persona references | Stage behavior, executive lens, output rules | Generic run references plus optional private stakeholder lenses |
| Payments, wallets, and chain registries | Roster, facts, sources, narrative, deal context | Separate versioned private market packs and structured competitor state |
| Positioning and lexicon references | Gap analysis and approved terminology | Private market-pack inputs with explicit sensitivity |
| Channel/source registry | Slack channels, search terms, web and social targets | Private source mapping consumed by generic adapters |
| Claude wrapper and settings | Headless invocation and permission list | Retire after Desktop cutover; do not import as product config |
| Reports, signals, snapshots, battlecards, trackers | Historical output and sometimes mutable state | Read-only archive plus selectively migrated structured records |
| Run beads | Coarse resume/completion state | Legacy references linked to schema-v2 run history |
| Governance checks | Registry and workflow validation | Repair current false-skip behavior, then replace with schema/contract tests |
| Work tracker and schedule records | Cadence and migration planning | Reconcile with actual runtime; keep separate from run state |
| Downstream skills/artifacts | Consumers of competitive conclusions | Compatibility renderers, then versioned structured interfaces |

Nothing is deleted or overwritten during discovery or conversion.

## 3. Migration Principles

1. Freeze by commit and artifact digest before conversion.
2. Convert with dry-run previews and explicit ambiguity reports.
3. Keep the legacy source read-only until cutover and rollback expiry.
4. Make structured state canonical; render temporary Markdown compatibility views.
5. Do not infer missing approvals, facts, dates, or source provenance.
6. Preserve rejected, superseded, contradictory, and uncertain evidence when policy permits.
7. Separate public Polygon examples from private data through an allowlist build.
8. Compare behavior and evidence quality, not identical prose.
9. Retire Claude only after an explicit, reversible cutover decision.

## 4. Private Mapping Deliverable

Create one private organization mapping that records:

- organization, product, and internal aliases;
- private market IDs and competitor IDs;
- Slack workspaces, channels, users, keywords, and access policy;
- GitHub organizations, public/private repositories, objects, and authority policy;
- company document systems and allowed roots;
- current registries, positioning, lexicons, reports, signals, snapshots, battlecards,
  trackers, and historical run locations;
- stakeholder profiles/lenses and sensitivity;
- evidence and apply reviewers;
- output owners and destinations;
- retention, public-safe rendering, and deletion policy.

The public mapping template lists these categories but contains no private value. The private
mapping is never committed to the public repository.

## 5. Migration Stages

### 5.1 Stage A — Freeze and inventory

- Record the exact legacy skill, references, wrapper, settings, helper scripts, checks,
  schedules, state, outputs, and downstream consumers by Git commit and hashes.
- Identify untracked or externally stored dependencies.
- Record last successful run, last complete source coverage, stale markets, and partial runs.
- Classify each asset: convert, render for compatibility, archive read-only, replace, or
  retire.
- Repair checker paths that silently skip current registries before treating a green check as
  evidence.

**Exit:** signed-off inventory with no unknown mutable source of truth.

### 5.2 Stage B — Schema mapping

Map legacy fields into config, market pack, competitor state, evidence, claim, run, approval,
change-set, and tracker-event schemas. Produce an explicit disposition for:

- facts without a source;
- sources without dates;
- narrative fields absent in one market;
- competitor rosters that differ between runbook and registry;
- repeated snapshots and same-day collisions;
- run beads without artifact hashes;
- reports marked complete despite blocked writes;
- deal/customer context subject to stricter retention;
- draft or unapproved positioning claims.

Unknown values remain unknown. A migration warning is not converted into a verified fact.

**Exit:** field-level mapping approved for all legacy shapes.

### 5.3 Stage C — Dry-run converters

Implement deterministic converters for each legacy shape. Every converter must emit:

- source path and digest;
- parser/converter version;
- parsed records;
- skipped, ambiguous, malformed, and conflicting records;
- proposed target files;
- schema results;
- public/private sensitivity;
- human-readable diff;
- no writes outside a staging destination.

Run converters against copies or read-only sources. Re-running against identical input must
produce identical proposed state.

**Exit:** every ambiguity has an owner disposition; no source file changed.

### 5.4 Stage D — Compatibility and downstream consumers

- Render legacy Markdown views from new structured state when a downstream consumer still
  requires them.
- Mark compatibility files generated and reject manual edits.
- Inventory each downstream reader and migrate it to the structured or versioned rendered
  interface.
- Keep tracker planning state separate from runtime run state.
- Remove compatibility rendering only in a later approved breaking change.

**Exit:** all downstream consumers are migrated or explicitly time-bounded on compatibility
views.

### 5.5 Stage E — Desktop canary

For each private market:

1. resolve one exact date window;
2. align enabled sources and known source limitations;
3. run Claude and Codex collection independently;
4. freeze both evidence sets;
5. compare relevant unique signals, first-party coverage, duplicates, date handling,
   conflicts, failures, and unsupported claims;
6. synthesize from the reviewed evidence sets;
7. compare material implications and proposed registry changes;
8. classify differences by source, adapter, schema, workflow, model, policy, or reviewer;
9. fix the reusable layer before adding private prompt exceptions.

Identical prose and ordering are not parity requirements.

**Exit:** the approved number of consecutive passing runs is met for every market.

### 5.6 Stage F — Cutover and rollback window

- Back up legacy canonical files and record digests.
- Make Codex structured state canonical through one explicit apply.
- Disable legacy mutation paths without deleting them.
- Update downstream consumers and operational documentation.
- Monitor the first production Desktop runs for coverage, runtime, failure, review effort,
  and state diffs.
- Retain the ability to render from and restore the frozen legacy state during the approved
  rollback window.

**Exit:** product owner closes the rollback window and separately authorizes Claude
retirement.

## 6. Polygon Golden-Example Extraction

Each public golden pack must be assembled independently of the private converter output.
Complete and approve Chain before implementing Payments; complete and approve Payments
before implementing Wallets:

1. select a representative Polygon scenario and behaviors to demonstrate;
2. identify current authoritative public sources for every included fact;
3. recreate the evidence records from those public sources;
4. write a public market-pack example with no internal mapping;
5. derive claims, report, and proposed change set through the new workflow;
6. review quotation, redistribution, licensing, accuracy, and currentness;
7. scan for private identifiers and semantic leakage;
8. approve the exact source manifest and example digest for public release.

Do not rename private customers, people, or channels to create a “sanitized” example. Replace
the scenario with public or synthetic material if the underlying logic would disclose
private context.

## 7. Parity Scorecard

| Dimension | Required measurement |
|---|---|
| Source coverage | Configured required/optional sources attempted and successfully read |
| Relevant-signal recall | Reviewed material signals found by each runtime |
| Precision | Reviewed irrelevant or duplicate signals |
| Provenance | Material claims with complete evidence links |
| Date accuracy | Correct event/publication/observation/window handling |
| State accuracy | Proposed registry changes accepted, rejected, no-op, or missed |
| Analysis quality | Material implications and limitations captured |
| Safety | Unauthorized writes, approval violations, private/public leakage |
| Reliability | Failure, retry, resume, and partial-completion honesty |
| Operations | Runtime, cost when available, and reviewer effort |

Thresholds must be approved before the first canary is scored. Recommendation: three
consecutive passing reviewed runs per market, zero unsupported material claims, zero
unauthorized writes, and 100% required-source outcome visibility.

## 8. Rollback Requirements

- Rollback never deletes new run evidence; it changes canonical-pointer/state ownership.
- The pre-cutover state and every migration input have recorded digests.
- A restore rehearsal runs before cutover.
- Converter version and mapping file remain available for diagnosis.
- Any post-cutover new facts are exported before restoring legacy canonical state.
- Claude credentials, schedulers, or mutation paths are not permanently destroyed until the
  rollback window closes.
- Destructive cleanup is a separate approved task with exact targets.

## 9. Implementation Checklist

- [ ] Freeze legacy commit and artifact inventory.
- [ ] Identify every external/untracked source dependency.
- [ ] Repair obsolete registry checks and add missing roster coverage.
- [ ] Approve private organization/source mapping.
- [ ] Approve schema field mappings and ambiguity policy.
- [ ] Build dry-run converters and deterministic fixtures.
- [ ] Convert each private market into a versioned market pack.
- [ ] Migrate or archive signals, reports, snapshots, trackers, and run beads.
- [ ] Build compatibility renderers and consumer inventory.
- [ ] Create and approve Polygon golden packs from public sources in order: Chain, Payments,
      Wallets.
- [ ] Run privacy and semantic-leak review on public candidates.
- [ ] Approve parity rubric and consecutive-run threshold.
- [ ] Execute canaries for each market using exact windows.
- [ ] Exercise restore and rollback.
- [ ] Cut over canonical state through an explicit approved change.
- [ ] Monitor initial Desktop production runs.
- [ ] Retire Claude only after an explicit closeout decision.

## 10. Acceptance

This PRD is satisfied when:

1. AT-110–116 pass against the private corpus;
2. no private source is modified by discovery or dry-run conversion;
3. all migrated canonical records validate and retain provenance or explicit unknown status;
4. downstream consumers have a supported structured or compatibility interface;
5. the Chain, Payments, and Wallets golden packs pass AT-007–008 without private leakage in
   the approved sequence;
6. every private market meets the approved canary threshold;
7. rollback has been rehearsed successfully;
8. the Claude wrapper remains available until the separate cutover approval succeeds.

## 11. Open Decisions

1. Whether existing Markdown registries remain compatibility views and for how long.
2. Whether the three current modes remain intact or become more granular market packs.
3. The exact parity thresholds and number of consecutive passing runs.
4. Evidence and apply approver identities and separation of duties.
5. The rollback-window duration.
