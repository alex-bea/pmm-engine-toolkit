---
doc_type: DOC
normative: false
requires:
  - DOC-comp-intel-source-inventory-v1.0.md
  - product-requirements/comp-intel/DOC-comp-intel-codex-migration-prd-v1.0.md
  - STD-approval-gates-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-skill-dependencies-v1.0.md
  - STD-skill-structure-v1.0.md
status: Superseded
version: "1.0"
owner: alex-bea
consumers:
  - comp-intel implementers
  - product reviewers
  - security reviewers
  - public adopters
change_control: Pull request review and project-owner approval
---

# Competitive Intelligence Skill Expansion Product Requirements (v1.0)

This earlier product-requirements draft is retained as decision history. It is superseded by
the [current Codex product-requirements suite](product-requirements/comp-intel/README.md),
which incorporates later product-owner decisions about public golden examples, integration
scope, migration, and distribution. Do not implement from this document where it conflicts
with that suite. Neither document authorizes implementation, source collection, private
cutover, or external publication without its stated approvals.

## 0. Document purpose and companion authority map

This PRD recorded an earlier product direction for the public `comp-intel` expansion. The
current suite now owns the proposed outcomes, scope, product requirements, quality bar,
approval gates, and release acceptance. This document remains useful only as a trace of the
prior analysis and narrower alternative.

| Artifact | Role | Authority |
|---|---|---|
| This PRD | Superseded product alternative and decision history | Non-normative; must not override the current suite |
| `product-requirements/comp-intel/README.md` and linked suite | Current proposed product outcomes, architecture, implementation slices and acceptance | Advisory while `Draft`; binding only after the suite's stated approvals |
| `DOC-comp-intel-source-inventory-v1.0.md` | Bounded source closure and publication dispositions | Advisory design evidence; remains non-normative |
| Future `skills/comp-intel/references/RUN-comp-intel-workflow-v1.0.md` | Exact operator stages, stop conditions and approval procedure | Binding execution contract when implemented, reviewed and Active |
| Future analysis, source-adapter and registry references | Detailed semantic and interface contracts | Authority declared by each governed document's metadata; cannot override this PRD |
| Future schemas, templates and deterministic controller | Machine-enforced data and transition contracts | Implementation of this PRD; schema versions and tests govern compatibility |
| Implementation pull requests and test reports | Build history and verification evidence | Evidence only; they do not change product scope without a PRD revision |

## 1. Superseded decision summary

Expand the existing public `skills/comp-intel` package in place into a self-contained,
review-gated competitive-intelligence workflow for interactive Codex use. Keep `comp-intel`
as the skill name and preserve its current invocation language. Do not create a duplicate
skill, plugin, marketplace entry, hosted service, or bundled organization-specific market.

The product will help an adopter configure a market, collect attributable evidence from
approved sources, review an immutable evidence set, synthesize claims from that exact set,
review proposed state changes, and apply approved changes to adopter-owned local state.
Installed files remain reusable and immutable; all live configuration, evidence, approvals,
registries, trackers and reports live under an adopter-controlled data root.

The package and examples are generic and fictional. Real companies, people, channels,
customers, deals, source mappings, positioning, profiles and historical intelligence are not
part of the distribution.

## 2. Problem and current state

The current public package is safe and discoverable, but it is a thin six-file prompt scaffold.
It can summarize supplied signals, yet it does not define:

- initialization or a safe mutable-data boundary;
- market-pack and registry contracts;
- source capability discovery or adapter failure behavior;
- normalized evidence, claim, run-state or proposed-change records;
- deterministic deduplication, time-window or conflict handling;
- evidence-digest review, draft review or canonical-state application gates;
- collision-resistant resume behavior;
- update, rollback, retention or concurrency behavior; or
- an offline end-to-end acceptance case.

The private source workflow demonstrates useful jobs—collection, monitoring, positioning
snapshots, gap detection, executive synthesis and durable competitive state—but couples them
to one organization, private sources, mutable Markdown, implicit approvals and a legacy host
runtime. The [source inventory](DOC-comp-intel-source-inventory-v1.0.md) defines which concepts
may be generalized and which material must remain private or excluded.

## 3. Users and jobs to be done

| User | Job |
|---|---|
| Competitive analyst | Collect a bounded evidence window, distinguish verified observations from reports and inference, and resume without recollecting sources. |
| Product marketer | Turn approved evidence into implications, positioning gaps and recommended actions without introducing unsupported claims. |
| Reviewer | Inspect the exact evidence and proposed changes, understand limitations, and approve or reject a digest rather than an ambiguous draft. |
| Adopter/operator | Configure markets, sources, permissions, storage and reviewers without editing installed package files. |
| Maintainer/security reviewer | Prove that the distributed package is self-contained, generic, fictional, least-privilege and free of private state. |
| Downstream consumer | Read approved claims or rendered views while retaining evidence status, dates and limitations. |

## 4. Goals and non-goals

### 4.1 Goals

- Preserve the strongest reusable analysis behavior while removing organization coupling.
- Make a direct installation of `skills/comp-intel/` complete without repository-root runtime
  dependencies.
- Separate collection, evidence review, synthesis, draft review and local application.
- Make claims traceable to normalized evidence with explicit uncertainty and conflict.
- Keep mutable data outside the installed package and preserve it across package updates.
- Support an offline fictional quickstart and deterministic acceptance suite.
- Give optional integrations honest capability, permission and degraded-mode behavior.

### 4.2 Non-goals

- Bundling a real competitor registry, positioning, person profile, source map, customer record,
  call-derived intelligence, prior run, or public-company golden pack.
- Creating a dedicated plugin, marketplace listing, hosted service or separate repository.
- Supporting unattended, scheduled or headless execution in v1.
- Sending messages, publishing reports, changing external systems or creating automations.
- Owning connector authentication or installing global runtime configuration.
- Importing private historical runs or cutting over an existing private deployment.
- Rebuilding downstream copywriting, battlecard or signal-scanning skills.

## 5. Success measures

These are release measures, not claims about current product performance. Every target must be
demonstrated with synthetic or repository-governance evidence before public release.

| Outcome | Measure | v1 release target | Guardrail |
|---|---|---|---|
| Portable direct installation | Share of runtime paths and declared package dependencies resolved from a direct `skills/comp-intel/` install | 100% | Repository-root or private-path fallback is a release blocker |
| Trustworthy outputs | Share of material rendered statements linked to eligible evidence or explicitly labeled `[Missing]` | 100% | A fluent unsupported statement counts as failure, not partial success |
| Gate integrity | Unauthorized synthesis, canonical-state apply or external-write successes in the acceptance corpus | Zero | Any bypass blocks release and further apply testing until reviewed |
| Honest degraded operation | Enabled adapters with explicit capability, coverage and terminal status in the run manifest | 100% | A failed source may not disappear from coverage or silently fall back |
| Deterministic operability | Repeated fixture runs with identical normalized digests and rendered outputs; offline synthetic controller duration | 100% identical; no more than 30 seconds per supported CI runtime, excluding model and external-service time | Performance work may not weaken evidence, approval or privacy controls |
| Data safety | Private-data findings in package/history scans; update or uninstall tests that preserve adopter-owned data | Zero findings; 100% preservation tests pass | Any credential, private identifier or unintended data deletion blocks release |

## 6. Required user experience

### 6.1 Setup

1. Inspect for an existing configuration and data root without writing.
2. If absent, show the exact files and directories that initialization would create.
3. Default the mutable data root to `.comp-intel/` in the adopter's current repository; allow
   an explicit external directory override.
4. Reject a data root inside the installed skill/package and never overwrite differing files.
5. Validate at least one market pack and one enabled source before a live run.
6. Offer the offline fictional fixture without requiring any external account.

Initialization requires explicit local-write approval. If `.comp-intel/` is repository-local,
the initializer proposes a matching ignore rule but does not edit `.gitignore` without separate
approval.

### 6.2 Run stages

```text
configure -> collect -> normalize -> evidence_review -> synthesize
          -> draft_review -> apply_approved -> complete
```

- **Configure:** Resolve market, absolute time window, enabled sources, data root and reviewer
  policy. Ambiguity that changes scope must be resolved before collection.
- **Collect:** Read only approved sources and write run-local staging records. Collection cannot
  update canonical registries or trackers.
- **Normalize:** Validate source identity, dates, labels, confidence, sensitivity and duplicates;
  calculate the evidence-manifest digest.
- **Evidence review:** Stop. Present coverage, conflicts, failures and the exact digest. No
  synthesis occurs until that digest has a valid approval record.
- **Synthesize:** Use only the approved evidence manifest. Live retrieval is prohibited.
- **Draft review:** Present the briefing, claims and proposed change set. Do not mutate canonical
  competitive state.
- **Apply approved:** Validate a separate apply approval, evidence digest, draft digest and base
  registry digest; apply atomically or write nothing.
- **Complete:** Record artifacts, versions, approvals and final digests. External publication or
  messaging remains outside the product.

### 6.3 Resume and failure behavior

- Resume requires an exact run ID. A convenience command may suggest the latest eligible run but
  must display and confirm its market, window and stage before proceeding.
- Same-day runs use collision-resistant IDs and never overwrite one another.
- Missing optional sources produce explicit partial coverage. Missing required sources stop the
  run before evidence review.
- Partial collection, validation, synthesis or apply failures are recorded as failures; artifact
  existence alone cannot mark a stage successful.
- A corrupt or unsupported state version stops with recovery guidance. It is never repaired
  silently.

## 7. Functional requirements

### 7.1 Package and compatibility

- **CI-PKG-001:** Expand `skills/comp-intel` in place. No duplicate package or plugin may define
  competing workflow semantics.
- **CI-PKG-002:** `SKILL.md` contains exactly `name` and `description` in frontmatter and remains
  a concise router to task-specific, skill-local resources.
- **CI-PKG-003:** A direct skill installation is self-contained. Runtime instructions must not
  require repository-root standards, private paths or another skill.
- **CI-PKG-004:** Preserve the `$comp-intel` name, existing positive invocation concepts and
  accurate `agents/openai.yaml` metadata. Add negative activation cases for unrelated research
  and generic skill-authoring requests.

### 7.2 Configuration and adopter-owned data

- **CI-CFG-001:** Validate configuration for data root, markets, competitors, source adapters,
  absolute-window policy, reviewer policy, retention and output renderers.
- **CI-CFG-002:** Store mutable configuration and state outside installed package files. The
  default is repository-local `.comp-intel/`; an explicit external path is supported.
- **CI-CFG-003:** Ship only empty templates and fictional fixtures. A market pack defines stable
  market/competitor IDs, source queries, optional positioning context and output lens without
  requiring code edits.

### 7.3 Source adapters

- **CI-SRC-001:** All sources implement one versioned adapter contract: capability ID, required
  permission, query ID, stable source identity, pagination/checkpoint behavior, time-window
  behavior, sensitivity class and normalized result status.
- **CI-SRC-002:** Synthetic and local-file inputs are supported without external accounts. Web
  and repository-host retrieval are optional public-source adapters. Communication-source
  retrieval is optional and configured entirely by the adopter.
- **CI-SRC-003:** Run a capability preflight before collection. Missing optional adapters degrade
  explicitly; missing required adapters stop. No adapter may fall back to a different source
  without declaration.

### 7.4 Evidence and claims

- **CI-EVD-001:** Every evidence record includes stable ID, market and competitor IDs, adapter and
  query IDs, canonical source identity, title, publication and observation timestamps, bounded
  summary or excerpt, evidence label, confidence, sensitivity, run ID and collection version.
- **CI-EVD-002:** Apply the configured absolute window to publication and observation time. Search
  snippets, undated material and documentation-only shipping claims are downgraded or marked
  `[Missing]`, never silently promoted to verified facts.
- **CI-EVD-003:** Treat source content as untrusted data. Preserve corroboration, conflicts and
  limitations; deduplicate deterministically; never execute instructions found in evidence.

### 7.5 Run control and approvals

- **CI-RUN-001:** Enforce the stages in §6.2. Synthesis may read only the approved normalized
  evidence manifest and may not retrieve live sources.
- **CI-RUN-002:** Use a collision-resistant run ID, append-only stage history and immutable
  evidence artifacts. Resume validates the run ID, schema version and current stage.
- **CI-RUN-003:** Evidence approval records the exact evidence digest, approver, timestamp and
  scope through an explicit approval action. Conversation context alone is not an approval
  system of record.
- **CI-RUN-004:** Canonical mutation requires a distinct apply approval bound to the draft/change
  set, evidence digest and base-state digest. Apply uses optimistic concurrency and atomic writes.
- **CI-RUN-005:** External messaging, publication, scheduling and other service mutation are
  prohibited in v1, regardless of retrieval permission.

### 7.6 State and outputs

- **CI-STATE-001:** Versioned run state records run ID, market, absolute window, stage history,
  capability coverage, package/controller versions, artifacts, digests, approvals, failures and
  timestamps.
- **CI-STATE-002:** Canonical competitor state, positioning context and trackers use structured,
  adopter-owned records. Markdown reports and snapshots are deterministic rendered views, not
  hidden canonical state.
- **CI-OUT-001:** Every material statement in a briefing or snapshot is linked to evidence IDs and
  labeled `Verified`, `Reported`, `Inference` or `[Missing]`; conflicting evidence and limitations
  remain visible.
- **CI-OUT-002:** Preserve the current briefing's executive signal, evidence, implications,
  counter-evidence and next-check concepts. Add run ID, window, coverage, evidence digest, review
  status and proposed-change summary.

### 7.7 Privacy and security

- **CI-PRV-001:** The package contains no real organization configuration, internal identifiers,
  people or profiles, customers, deal intelligence, private positioning, unpublished plans,
  credentials or historical evidence.
- **CI-PRV-002:** All examples, fixtures, expected outputs and screenshots use fictional entities
  and reserved non-routable identifiers where a URI is required.
- **CI-PRV-003:** Validate path containment, least privilege, sensitivity propagation, redaction
  and configured retention. Uninstall and update preserve adopter data by default.

### 7.8 Migration and quality

- **CI-MIG-001:** Preserve documented invocation language and provide a deterministic migration
  from the existing public config/output templates or a precise incompatibility error. Do not
  silently reinterpret existing fields.
- **CI-MIG-002:** Public v1 starts with clean adopter state. Private registries, historical runs,
  prior internal PRDs and legacy state-backfill behavior are not imported or published.
- **CI-QA-001:** Deterministic or fragile behavior lives in `scripts/` and has unit, schema,
  transition, failure, privacy and synthetic end-to-end tests.
- **CI-QA-002:** Release requires the governed-document audit, skill-pack validator, complete test
  suite, GitHub Actions validator, local-link check, IP inventory reconciliation and applicable
  security review to pass without weakening a control.

## 8. Non-functional requirements

- **CI-NFR-001 — Privacy:** Minimize collected and persisted data, apply configured sensitivity
  and retention, and prevent real identities, private mappings or evidence from entering the
  distributed package or synthetic corpus.
- **CI-NFR-002 — Security:** Treat all retrieved and local-file content as untrusted, validate
  path containment, use least-privilege adapters, keep credentials outside artifacts, and refuse
  instructions embedded in evidence.
- **CI-NFR-003 — Reliability:** Make collection checkpoints, normalization, resume and apply
  idempotent where applicable; use deterministic digests, atomic writes, optimistic concurrency
  and explicit terminal failure records.
- **CI-NFR-004 — Performance:** Complete the offline synthetic controller path within 30 seconds
  on each supported CI runtime, excluding model and external-service latency; expose stage
  durations and bound adapter pagination, item counts and excerpt sizes.
- **CI-NFR-005 — Explainability:** Before each approval, show source coverage, limitations,
  conflicts, relevant digests, proposed operations and the effect of accepting or rejecting.
- **CI-NFR-006 — Maintainability:** Version machine-readable contracts, keep deterministic logic
  in tested helpers, keep runtime instructions concise, and require explicit migrations for
  incompatible schema or package changes.
- **CI-NFR-007 — Portability and compatibility:** Support direct installation without private or
  repository-root dependencies, preserve documented invocation language and validate upgrades
  from every supported public schema version.
- **CI-NFR-008 — Resource and cost control:** Apply configured source, page, item, excerpt and
  retry limits; resume from approved checkpoints instead of recollecting; do not introduce a
  hosted service or mandatory paid integration in v1.

## 9. Data contracts

The implementation may use JSON or YAML, but the machine-readable schemas and field semantics
are normative. Rendered Markdown is never the only representation of mutable state.

### 9.1 Evidence record

Required fields:

- `schema_version`, `evidence_id`, `run_id`, `market_id`, `competitor_id`;
- `adapter_id`, `adapter_version`, `query_id`, `canonical_source_id`;
- `title`, `published_at`, `observed_at`, `summary`, optional bounded `excerpt`;
- `label`, `confidence`, `sensitivity`, `retention_class`;
- `corroborates[]`, `conflicts_with[]`, `limitations[]`; and
- a content digest.

### 9.2 Claim record

Required fields:

- `schema_version`, `claim_id`, `run_id`, `market_id`, `competitor_id`;
- `claim_type`, `text`, `evidence_ids[]`, `confidence`, `limitations[]`;
- `review_status`; and
- a claim digest.

No claim can be `Verified` without at least one eligible evidence ID.

### 9.3 Proposed change set

Required fields:

- `schema_version`, `change_set_id`, `run_id`, `market_id`;
- `base_state_digest`, `evidence_digest`, `draft_digest`;
- typed proposed operations, target IDs and supporting claim IDs;
- `status`; and
- review/apply approval references.

### 9.4 Run state

Required fields:

- `schema_version`, `run_id`, package and controller versions;
- market, absolute window and capability-preflight result;
- append-only stages with start/end timestamps and result status;
- artifacts and their digests;
- evidence and draft approvals;
- error ledger and retry metadata; and
- final status.

## 10. Target package architecture

Later implementation PRs will converge on this package shape:

```text
skills/comp-intel/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── RUN-comp-intel-workflow-v1.0.md
│   ├── DOC-comp-intel-analysis-contract-v1.0.md
│   ├── REF-comp-intel-source-adapter-contract-v1.0.md
│   └── REF-comp-intel-registry-schema-v1.0.md
├── assets/
│   ├── config-template.yaml
│   ├── market-pack-template.yaml
│   ├── policy-map-template.yaml
│   ├── stakeholder-lens-template.yaml
│   ├── positioning-context-template.md
│   ├── output-template.md
│   ├── evidence-record.schema.json
│   ├── claim-record.schema.json
│   ├── change-set.schema.json
│   └── run-state.schema.json
├── examples/EX-synthetic.md
├── scripts/
│   ├── comp_intel.py
│   └── validate_comp_intel.py
└── tests/
    └── fixtures/
```

The old `references/RUN-workflow.md` is replaced only in the same implementation change that
updates `SKILL.md` and tests. Repository-root standards remain contributor governance; runtime
instructions contain the required operational rules locally so direct installation stays closed.

## 11. Compatibility and lifecycle

- The skill name and `$comp-intel` invocation remain stable.
- Existing public config fields (`scope`, `market`, `competitors`, `sources`, confidence
  threshold) receive an explicit migration mapping in the implementation.
- Existing output headings remain available in the richer rendered report.
- Installed package files are treated as versioned code. Adopter data is never written there.
- Update performs schema preflight and backup before migration; failure leaves prior data intact.
- Uninstall removes only installed package files unless the user separately chooses a specific
  adopter-data path for removal.
- Breaking contract changes require a major package/schema version and a documented migration.

## 12. Rollout plan and implementation slices

| Phase | Scope | Exit evidence |
|---|---|---|
| 0 — Requirements baseline | Land this PRD, source inventory, catalog discoverability and legal inventory without runtime changes | Strict document audit, local-link validation, IP reconciliation, project-owner approval of the exact PRD revision and activation as normative |
| 1 — Package contracts | Update the router and metadata; add the runbook, analysis/source/registry references, templates and schemas | CI-AT-001, CI-AT-002, CI-AT-009, CI-AT-010, CI-AT-014 and direct-install review pass |
| 2 — Offline controller | Implement initialization, synthetic/local-file collection, normalization, state, approvals, rendering and local apply | CI-AT-003, CI-AT-004, CI-AT-006–009 and CI-AT-013 pass on every supported CI runtime |
| 3 — Optional public adapters | Add web and repository-host adapters; keep communication-source retrieval separately configured and optional | CI-AT-005–007, privacy review and adapter failure/limit tests pass |
| 4 — Release verification | Exercise clean install, update, uninstall, compatibility, refusal, privacy, IP, security and complete CI acceptance | CI-AT-001–014 pass; success measures meet their targets; all stop conditions are clear; project-owner release approval is recorded |

Each phase is a focused pull request. A phase cannot claim behavior or exit evidence owned by a
later phase, and failure of an exit condition stops advancement.

## 13. Acceptance tests and requirement traceability

| ID | Requirements verified | Scenario | Pass condition |
|---|---|---|---|
| CI-AT-001 | CI-PKG-001, CI-MIG-002, CI-PRV-001, CI-QA-002 | Inventory closure | Every functional seed reference has an inventory row or an explicit interface/pattern boundary; no copied-content path is publishable. |
| CI-AT-002 | CI-PKG-001–003, CI-CFG-002, CI-NFR-006–007 | Direct installation | A clean direct install resolves every runtime path inside `skills/comp-intel/`. |
| CI-AT-003 | CI-CFG-001–003, CI-SRC-002, CI-RUN-001–004, CI-STATE-001–002, CI-OUT-001–002, CI-NFR-003–005, CI-NFR-008 | Offline quickstart | Fictional fixture completes configure through approved local apply without an external account, repeats with identical digests and output, and meets the offline duration target. |
| CI-AT-004 | CI-SRC-001–002, CI-EVD-001–003, CI-NFR-001–002 | Local-file evidence | Approved local input normalizes into stable evidence records with correct dates, labels and sensitivity. |
| CI-AT-005 | CI-SRC-001–003, CI-STATE-001, CI-OUT-002, CI-NFR-004, CI-NFR-008 | Optional adapter absent | Missing optional adapter produces explicit partial coverage; missing required adapter stops before collection. Adapter limits and stage timing remain visible. |
| CI-AT-006 | CI-EVD-003, CI-RUN-001–003, CI-NFR-002, CI-NFR-005 | Evidence review gate | Synthesis refuses absent, unauthorized or wrong-digest approval and performs no live retrieval after approval. |
| CI-AT-007 | CI-EVD-001–003, CI-OUT-001–002, CI-NFR-005 | Claim provenance | Every material rendered claim resolves to eligible evidence; missing or conflicting support stays visible. |
| CI-AT-008 | CI-RUN-004, CI-STATE-001–002, CI-NFR-003 | Apply safety | Wrong base digest or partial-write failure leaves canonical state unchanged. |
| CI-AT-009 | CI-CFG-002, CI-PRV-003, CI-NFR-002–003 | Data-root safety | Initialization rejects package-contained and escaping paths and never overwrites differing files. |
| CI-AT-010 | CI-CFG-003, CI-PRV-001–003, CI-MIG-002, CI-NFR-001–002 | Public privacy | Package and intended history contain no prohibited real configuration, identities, people, deals, positioning, credentials or private evidence. |
| CI-AT-011 | CI-PKG-004, CI-MIG-001, CI-NFR-006–007 | Compatibility | Existing invocation language and supported config/output concepts migrate deterministically or fail with precise guidance. |
| CI-AT-012 | CI-RUN-005, CI-PRV-003, CI-NFR-002, CI-NFR-008 | External-write refusal | Requests to message, publish, schedule or mutate a service are refused as out of v1 scope. |
| CI-AT-013 | CI-RUN-002, CI-STATE-001, CI-NFR-003 | Same-day and resume | Multiple same-day runs do not collide; exact-run resume validates stage and schema without recollecting approved inputs. |
| CI-AT-014 | CI-QA-001–002, CI-NFR-006–007 | Document and package governance | Metadata, links, dependency closure, IP inventory, tests and validators all pass. |

Every requirement in §§7–8 appears in at least one acceptance row. Implementation pull requests
must preserve this mapping and name the automated or review evidence used for each applicable ID.

## 14. Risks, mitigations and stop conditions

| Risk | Mitigation | Stop condition |
|---|---|---|
| Private or identifying material enters a public artifact or Git history | Synthetic-only fixtures, bounded inventory dispositions, staged review, privacy scans and IP reconciliation | Any real private identity, mapping, evidence, credential or restricted positioning blocks release until removed from the branch and intended history |
| Unsupported or stale claims appear authoritative | Absolute windows, evidence labels, source dates, conflicts, limitations and claim-to-evidence validation | Any material claim without eligible evidence or `[Missing]` status stops report approval |
| Retrieved content attempts to redirect the workflow | Treat evidence as untrusted data, isolate normalization and prohibit instruction execution from source content | Any evidence-originated instruction changes scope, tools, approvals or writes; stop the run and record the source as unsafe |
| Adapter failure silently narrows coverage | Capability preflight, explicit required/optional policy and coverage manifest | A required adapter fails, or any enabled adapter lacks a terminal coverage status |
| Concurrent or partial apply corrupts adopter state | Digest-bound approval, optimistic concurrency, backups and atomic replacement | Base digest mismatch, write failure or unverifiable rollback leaves canonical state untouched and stops apply |
| Package update or uninstall loses adopter data | Separate data root, schema preflight, migration backup and path-scoped removal | A preservation or rollback test fails; block the release or migration |
| Review burden encourages approval shortcuts | Bounded evidence summaries, visible conflicts, separate evidence/apply decisions and resumable review | Approval cannot be bound to the exact digest or a reviewer cannot inspect the proposed effect |
| Scope expands into external mutation or hosted operation | Explicit v1 non-goals, adapter read boundaries and external-write refusal tests | Any implementation can publish, message, schedule or mutate a service through the v1 workflow |

## 15. Release gates and approval

This PRD begins as `Draft` and `normative: false`. Project-owner approval must apply to the
exact pull-request revision after all review findings are resolved. Before merge as the binding
implementation contract:

1. change `status` to `Active` and `normative` to `true` in that approved revision;
2. rerun document, package, test, link, IP and security validation; and
3. retain pull-request review as the approval record.

Approval of this PRD authorizes only the later implementation work described here. It does not
approve a public release, live source collection, external messaging, publication, scheduling,
or migration of private state.

## 16. Assumptions and fixed defaults

- The canonical public source remains this repository and the existing `skills/comp-intel` path.
- Interactive Codex is the supported v1 runtime; headless and scheduled operation are deferred.
- The default mutable data root is `.comp-intel/` in the adopter repository, with an explicit
  external-path override.
- Synthetic and local-file inputs form the offline baseline. All external adapters are optional
  unless an adopter marks one required for a market.
- The public distribution remains generic and fictional; there is no bundled real-market pack.
- Prior private design documents inform this specification but are not dependencies, references
  or distributable content.
- Downstream integrations consume versioned approved outputs; their implementation remains out
  of scope.

## 17. Change control and review cadence

- Changes to product scope, requirement semantics, approval gates, data contracts, supported
  adapters, privacy boundaries, compatibility or release targets require project-owner approval,
  pull-request review and a version change when the contract is materially different.
- Each implementation phase must review this PRD's traceability table and record affected
  requirement and acceptance IDs in its pull request.
- Review this PRD after each implementation phase, before every public release, after any privacy
  or approval-control incident, and at least once per minor release while the skill is Active.
- A validator change cannot silently weaken a written requirement. Update the PRD and validation
  evidence together when intended behavior changes.
- Changes to future companion documents cannot override this PRD; conflicting documents stop the
  implementation until the project owner approves a reconciled revision.

## 18. Changelog

| Date | Version | Author | Summary |
|---|---|---|---|
| 2026-08-28 | 1.0 | alex-bea / Codex | Initial public expansion PRD: generic staged workflow, bounded dependency closure, measurable success targets, non-functional requirements, requirement-to-test traceability, rollout exit evidence, risk controls and governed approval lifecycle. |
