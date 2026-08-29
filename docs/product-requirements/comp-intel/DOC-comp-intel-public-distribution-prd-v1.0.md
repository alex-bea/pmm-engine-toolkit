---
doc_type: DOC
normative: false
requires:
  - DOC-comp-intel-codex-migration-prd-v1.0.md
  - DOC-comp-intel-codex-implementation-blueprint-v1.0.md
  - DOC-comp-intel-public-acceptance-tests-v1.0.md
  - DOC-comp-intel-codex-skill-implementation-prd-v1.0.md
  - DOC-comp-intel-integrations-implementation-prd-v1.0.md
  - DOC-comp-intel-private-migration-prd-v1.0.md
  - ../../STD-skill-structure-v1.0.md
  - ../../STD-evidence-privacy-v1.0.md
  - ../../STD-approval-gates-v1.0.md
  - ../../../AGENTS.md
status: Draft
version: "1.0"
owner: Alex Bea
consumers:
  - Release implementers
  - Public adopters
  - Security reviewers
  - Plugin reviewers
change_control: PR Review and explicit public-release approval
---

# Comp Intel Public Distribution Implementation PRD

## 1. Outcome

Publish one versioned, skill-first GitHub repository that another computer can load into
Codex Desktop without access to this private repository, developer-specific paths, or Polygon
internal systems. The repository is the architectural source of truth. It includes a thin
plugin wrapper for easy installation and integration bundling, but the workflow remains a
portable standalone skill with a reusable controller, approved public Polygon golden
examples, a synthetic offline quickstart, and an adopter mapping flow.

Root `AGENTS.md` must make Codex consult the master and relevant implementation PRDs for every
task that builds, changes, tests, or distributes this skill. The runtime `comp-intel` skill
does not activate for unrelated skill-building tasks; build-time persistence belongs in
repository instructions, while runtime activation remains task-specific.

The release must make the public/private boundary obvious: users supply and map their own
internal names, channels, company systems, permissions, existing intelligence data,
reviewers, and output destinations. The package does not pretend those mappings can be
inferred safely.

## 2. Release Channels

### 2.1 Required v1 channel

- Public GitHub repository containing root `AGENTS.md`, the standalone skill, controller,
  schemas, tests, PRDs, documentation, thin plugin wrapper, and release tags.
- Installation instructions for both the standalone skill and the supported plugin wrapper
  path available at release time.
- Immutable version tags and release artifact digest.

### 2.2 Optional channel

- Codex universal plugin directory/marketplace entry after the GitHub-installable artifact
  passes clean-machine acceptance and the applicable submission process.

Marketplace timing is an open product decision. The GitHub artifact must not depend on a
marketplace-only file or private repository submodule.

There is no separate starter repository in v1. The canonical repository contains examples
and a starter mapping template without becoming the user's mutable data root.

### 2.3 Deferred channels

- Headless-only package or scheduler image.
- Hosted service.
- Organization-managed deployment bundle.
- Companion connectors beyond the approved v1 integration set.

## 3. Public Artifact Contents

```text
competitive-intelligence/
├── AGENTS.md
├── .codex-plugin/plugin.json
├── .agents/plugins/marketplace.json   # optional catalog entry
├── skills/comp-intel/
├── scripts/
├── schemas/
├── examples/
│   ├── polygon-golden/chain/
│   ├── polygon-golden/payments/
│   ├── polygon-golden/wallets/
│   └── synthetic-devtools/
├── tests/
├── docs/
├── LICENSE
└── NOTICE
```

### 3.1 Repository-owned content

- Root build-time `AGENTS.md` and the public PRD suite.
- Skill instructions and `agents/openai.yaml`.
- Deterministic controller and approved adapters.
- Versioned schemas and templates.
- Polygon golden source manifest and approved derived outputs.
- Synthetic offline fixtures and expected outputs.
- Public test suite.
- Installation, mapping, privacy, upgrade, troubleshooting, removal, and contribution docs.
- License and third-party notices.

### 3.2 Prohibited content

- Credentials, tokens, cookies, connection exports, or secret configuration.
- Absolute developer paths.
- Internal channel, workspace, user, repository, document, or system IDs.
- Employee/stakeholder profiles and communication preferences.
- Customer, deal, win/loss, or private call information.
- Internal positioning, unapproved claims, or unpublished roadmaps.
- Private evidence excerpts or transformed summaries that disclose the same private fact.
- Mutable adopter state, approvals, reports, or run history.
- Claude-specific settings or permission allowlists.

## 4. Repository Guidance, Plugin Wrapper, and Skill Discovery

- **DFR-001:** Root `AGENTS.md` must route Codex to the master PRD and the relevant skill,
  integration, migration, distribution, and acceptance documents for every build task.
- **DFR-002:** Keep `skills/comp-intel` as the canonical standalone workflow source and make
  all runtime references resolve from the documented skill or plugin installation.
- **DFR-003:** Ship a valid thin `.codex-plugin/plugin.json` with stable ID, version, display
  metadata, and declared components.
- **DFR-004:** Include valid `agents/openai.yaml` metadata matching shipped web, GitHub,
  synthetic, and local-file capabilities; label Slack optional and configured separately.
- **DFR-005:** A fresh Codex Desktop process must discover the installed skill.
- **DFR-006:** A standalone skill load must support its documented subset; the plugin wrapper
  may add integration wiring but cannot define different workflow semantics.
- **DFR-007:** No build-time rule may force the runtime skill to activate for unrelated
  skill-building work.

## 5. Polygon Golden Examples

### 5.1 Purpose

Polygon examples prove the system can represent a real, complex product and competitor
landscape. They are documentation, evaluation fixtures, and a starting point for adopter
mapping—not default live intelligence.

Implement and publish them in order: Chain, Payments, then Wallets. A later pack cannot bypass
the review gates because an earlier pack has been approved.

### 5.2 Required controls

- **DFR-020:** Every material fact has an allowed public source and evidence ID.
- **DFR-021:** The source manifest records URL, title, publication/observation dates,
  authority class, quotation/redistribution notes, and review status.
- **DFR-022:** Each golden artifact records its source-manifest and generator digests.
- **DFR-023:** A named public-release approver accepts the exact artifact digest.
- **DFR-024:** Public facts are revalidated at release; stale examples are dated explicitly.
- **DFR-025:** No private input is used to fill a gap in the public example.
- **DFR-026:** Replacing Polygon mappings through the documented interface produces a valid
  non-Polygon market pack without code changes.

The synthetic pack remains the offline deterministic quickstart and security fixture. It is
not replaced by the Polygon pack.

## 6. Adopter Mapping Experience

The public release must include a setup checklist and machine-validated mapping template for:

1. organization and product names;
2. market IDs, competitor IDs, and aliases;
3. public domains and first-party source rules;
4. Slack workspaces, channels, users, and query terms when Slack ships;
5. GitHub organizations, repositories, and authority rules when GitHub ships;
6. company document systems and allowed roots;
7. existing registries, reports, signals, snapshots, battlecards, trackers, and run state;
8. stakeholder lenses and sensitivity;
9. reviewer and approver roles;
10. retention, public-safe rendering, and output destinations;
11. required versus optional integrations and minimum permissions.

- **DFR-030:** The mapping template contains placeholders or public examples only.
- **DFR-031:** Setup never writes Polygon values into live adopter config without explicit
  selection.
- **DFR-032:** Missing mappings remain visible with dependent capabilities.
- **DFR-033:** Documentation explains which existing intelligence can be imported, archived,
  or intentionally left unmigrated.
- **DFR-034:** Secrets are connected through supported platform mechanisms, not mapping
  files.

## 7. Desktop Installation and First Run

The public quickstart must take a new user through:

1. install plugin in Codex Desktop;
2. confirm skill discovery in a fresh task/process;
3. select a writable adopter data root;
4. run the synthetic offline example;
5. inspect evidence review and digest behavior;
6. optionally open the Polygon golden walkthrough;
7. copy the mapping template into adopter-owned data;
8. map one market and local/public source;
9. run capability preflight;
10. perform a first Desktop collection and stop at review.

The quickstart may not require Slack, GitHub, a private account, marketplace access, or
headless execution.

## 8. Documentation Requirements

Public repository documentation must include:

- product overview, intended users, non-goals, and evidence model;
- Desktop installation and supported-version matrix;
- synthetic quickstart;
- Polygon golden-example walkthrough and source manifest;
- adopter mapping guide;
- data-root, privacy, and retention guide;
- approved integration setup and minimum permissions;
- evidence review, approval, synthesis, and apply behavior;
- backup, upgrade, schema migration, and rollback;
- uninstall and data-preservation behavior;
- troubleshooting and diagnostics;
- headless/scheduled roadmap with an explicit v1 non-support statement;
- contribution, security-reporting, license, and provenance information.

Auxiliary installation and release documentation belongs at the plugin/repository level, not
inside the skill folder.

## 9. Versioning, Update, and Removal

- **DFR-040:** Use semantic versioning for the plugin and independent versions for schemas.
- **DFR-041:** Publish a compatibility matrix for plugin, schema, and minimum Codex version.
- **DFR-042:** Upgrades may replace plugin files but never adopter config, evidence, state,
  approvals, or reports.
- **DFR-043:** Data migration is explicit, dry-run capable, transactional, and reversible
  where documented.
- **DFR-044:** Uninstall removes plugin files and preserves adopter data.
- **DFR-045:** Destructive data cleanup is separate, exact-targeted, and explicitly
  authorized.
- **DFR-046:** Release notes identify data/schema, integration, security, and behavior
  changes.

## 10. Public Build and Review Pipeline

Assemble the release from an allowlist. Do not copy the private skill tree and subtract
known-sensitive files.

Required pipeline stages:

1. validate root `AGENTS.md` routing, skill, UI metadata, plugin manifest, marketplace
   metadata when present, and schemas;
2. run unit, adapter-contract, offline integration, Desktop interaction, security, privacy,
   and portability tests;
3. build Polygon golden examples only from their public source manifest;
4. scan the release tree and intended Git history for secrets, private identifiers, absolute
   paths, internal domains, and prohibited patterns;
5. run semantic review for private facts that survive renamed identifiers;
6. perform dependency license/IP and quotation review;
7. install on a clean second computer/profile;
8. exercise update and uninstall preservation;
9. produce a test report and artifact digest;
10. obtain exact-digest public-release approval;
11. tag and publish only after all applicable gates pass.

## 11. Portability Requirements

- Support the operating systems explicitly listed in the release compatibility matrix.
- Use no private submodule, symlink outside the package, or local absolute path.
- Resolve references correctly in a source checkout, standalone skill load, and installed
  plugin wrapper.
- Work with a read-only plugin directory.
- Keep user data outside plugin caches.
- Avoid assuming a particular shell for the Desktop experience.
- Verify fresh-process discovery after install and update.
- Provide actionable diagnostics when the installed Codex version is unsupported.

Headless portability is not a v1 release criterion. The package must, however, keep
controller and persisted data independent of Desktop conversation identifiers.

## 12. Implementation Checklist

- [x] Use one canonical skill-first repository with a thin plugin wrapper and no separate
      starter repository.
- [ ] Approve GitHub repository and license.
- [ ] Add root `AGENTS.md` that routes every build task to the governing PRDs and tests.
- [ ] Create and validate plugin manifest.
- [ ] Package the approved skill, controller, schemas, and v1 web/GitHub/local/synthetic
      adapters.
- [ ] Add Slack as an optional separately mapped integration.
- [ ] Build the fictional synthetic pack.
- [ ] Build Polygon golden examples from approved public sources in order: Chain, Payments,
      Wallets.
- [ ] Create golden source manifest and exact-digest approval record.
- [ ] Create the adopter mapping template and checklist.
- [ ] Document internal names, channels, systems, permissions, and existing-data mapping.
- [ ] Add Desktop installation, quickstart, update, uninstall, and troubleshooting docs.
- [ ] Declare headless and scheduled execution deferred.
- [ ] Validate all references from source-repo, standalone-skill, and installed-plugin
      layouts.
- [ ] Run public secrets, privacy, semantic-leak, and license/IP review.
- [ ] Run clean second-computer install and fresh-process discovery.
- [ ] Test update and uninstall data preservation.
- [ ] Produce artifact digest and release test report.
- [ ] Obtain public-release approval before GitHub release or marketplace submission.

## 13. Acceptance

This PRD is satisfied when:

1. AT-001–009, AT-010–015, AT-070–076, AT-090–095, AT-100–106, and applicable
   performance tests pass;
2. standalone-skill and plugin-wrapper paths both load the canonical skill on a clean second
   computer, and the plugin path runs the synthetic quickstart;
3. Chain, Payments, and Wallets golden packs pass provenance, generalization, privacy, and
   exact-digest approval gates in that sequence;
4. the adopter mapping checklist covers every required internal replacement category;
5. update and uninstall preserve adopter data;
6. the public artifact and intended release history contain no prohibited private material;
7. public capability claims include web, GitHub, synthetic, and local files, describe Slack
   as optional, and exclude headless/scheduled support;
8. root `AGENTS.md` reliably makes Codex consult the PRD suite during build tasks without
   over-triggering the runtime skill;
9. publication is approved separately under the governing repository process.

## 14. Open Decisions

1. Public repository location and release license confirmation.
2. GitHub-only v1 versus simultaneous marketplace submission.
3. Supported Desktop operating systems and minimum Codex version.
4. Whether optional Slack wiring ships inside the wrapper or as a companion plugin.
5. Who approves the Chain, Payments, and Wallets golden packs.
6. Whether public releases include prebuilt artifacts, source-only installation, or both.

## 15. Official Codex References

- [Build skills](https://learn.chatgpt.com/docs/build-skills) — skills are the reusable
  workflow authoring format and can be used standalone.
- [Package your plugin](https://developers.openai.com/plugins/build/plugins) — plugins add a
  stable install identity and can bundle skills with connector/MCP mappings.
