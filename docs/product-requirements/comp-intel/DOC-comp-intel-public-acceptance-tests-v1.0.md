---
doc_type: DOC
normative: false
requires:
  - DOC-comp-intel-codex-migration-prd-v1.0.md
  - DOC-comp-intel-codex-implementation-blueprint-v1.0.md
  - ../../STD-ai-skill-governance-prd-v1.0.md
  - ../../STD-evidence-privacy-v1.0.md
  - ../../STD-approval-gates-v1.0.md
  - ../../../AGENTS.md
status: Draft
version: "1.0"
owner: Alex Bea
consumers:
  - Maintainers
  - Plugin reviewers
  - Security reviewers
  - Public contributors
change_control: PR Review and product-owner approval
---

# Competitive Intelligence for Codex — Public Acceptance Tests

This is a proposed release gate, not a publication authorization.

---

## 1. Purpose

This specification defines the minimum evidence required to call the competitive-
intelligence migration functional, safe, portable, and public-ready. It covers the plugin,
skill, deterministic controller, source-adapter contracts, data lifecycle, Codex interaction,
Desktop-first operation, future headless boundaries, migration, and release packaging.

Passing tests does not authorize public release. The release remains a draft until the
applicable human, privacy, license/IP, and repository-governance reviews approve the exact
artifact digest.

## 2. Test Layers

| Layer | Purpose | External accounts allowed? | Required in public CI? |
|---|---|---:|---:|
| Static | Validate skill, plugin, schemas, docs, and forbidden patterns | No | Yes |
| Unit | Validate deterministic functions and stage guards | No | Yes |
| Adapter contract | Apply one behavioral suite to every source adapter | Fixtures by default | Yes for shipped adapters |
| Offline integration | Exercise complete synthetic workflow | No | Yes |
| Polygon golden examples | Verify realistic public examples, provenance, and reusable mapping | Public sources only | Yes |
| Codex interaction | Verify natural-language activation and stage behavior | Codex runtime | Before release; stable subset in CI when supported |
| Connector integration | Verify real optional adapters | Yes, test workspace/repo only | Protected CI or manual release gate |
| Security/privacy | Test path safety, prompt injection, secrets, and sanitization | No | Yes |
| Portability | Install/update/uninstall on clean environments | No private accounts | Yes or release automation |
| Private parity | Compare Claude and Codex private runs | Private systems | Private only; never publish fixtures |

## 3. Test Fixture Requirements

The public suite must include a fictional market with at least three fictional competitors
and these fixture events:

- a first-party product release with a valid publication date;
- a search result whose snippet overstates the underlying page;
- two sources corroborating the same event;
- one exact duplicate and one near duplicate;
- an edited source object with a stable native ID;
- two credible sources that conflict;
- a source with no publication date;
- a source outside the configured time window;
- a source containing prompt-injection instructions;
- an optional adapter timeout after one successful page;
- a required adapter failure;
- a private-labeled record forbidden from a public-safe report;
- a current registry changed concurrently before apply.

All companies, domains, people, channels, users, repositories, customers, and claims in the
synthetic fixture pack must be fictional. Reserved example domains should be used where a
URL is needed.

### 3.1 Polygon golden-example requirements

The public suite must include realistic Polygon golden scenarios in order: Chain, Payments,
then Wallets. Unlike the synthetic fixtures, they may name public Polygon products and public
competitors. Every source must be publicly accessible or redistributable, every factual claim
must cite its source, and every example must have an explicit public-release approval tied to
its digest before the next pack advances.

The golden pack must not include internal people, aliases, channels, user or workspace IDs,
private repositories, customer/deal information, stakeholder profiles, unpublished product
plans, private positioning, or excerpts from internal intelligence. If a useful internal
case cannot be supported with public evidence, replace its content with a synthetic analogue
rather than sanitizing individual names in place.

## 4. Static and Packaging Acceptance

### AT-001 — Codex skill validation

**Given** a clean checkout of the public release candidate
**When** the official skill validator is run against `skills/comp-intel`
**Then** validation passes without unsupported frontmatter keys, broken references, or
missing required files.

### AT-002 — Plugin manifest validation

**Given** the release candidate
**When** the plugin and marketplace schemas are validated
**Then** the manifest has a stable plugin ID and version, all referenced skills and metadata
exist, and no absolute local path appears.

### AT-003 — Self-contained installation references

**Given** the plugin installed outside its source repository
**When** Codex activates the skill and follows each referenced file
**Then** every required reference resolves inside the installed plugin or through an
explicitly documented adopter data path.

### AT-004 — Public forbidden-pattern scan

**Given** the complete release commit range and packaged artifact
**When** the public privacy scanner runs
**Then** it finds zero credentials, tokens, internal domains, workspace/channel/user IDs,
absolute developer paths, customer/deal names, employee profiles, private positioning,
unpublished roadmaps, or private source excerpts.

### AT-005 — License and provenance

**Given** all distributed code, templates, examples, icons, and dependencies
**When** provenance and license review runs
**Then** every asset has an allowed origin and compatible license, and required notices are
present.

### AT-006 — Documentation integrity

**Given** the packaged plugin
**When** documentation links, commands, paths, and version references are checked
**Then** no broken internal link, stale command, or undocumented required dependency exists.

### AT-007 — Polygon golden provenance

**Given** every Polygon golden input and expected output
**When** the provenance manifest is validated
**Then** every material factual claim resolves to an allowed public source, source dates and
licenses/quotation limits are recorded, and the exact example digest has public-release
approval.

### AT-008 — Golden-example generalization

**Given** the Polygon golden market pack
**When** all Polygon names and source mappings are replaced through the documented adopter
mapping interface
**Then** the generic workflow still validates and runs without code or `SKILL.md` edits.

### AT-009 — Build-time guidance without runtime over-activation

**Given** the canonical public repository
**When** Codex receives tasks to build, change, test, or distribute the comp-intel skill
**Then** root `AGENTS.md` routes it to the master and relevant implementation PRDs. When Codex
receives an unrelated skill-building task, the runtime `comp-intel` skill does not activate
solely because the task is skill building.

## 5. Configuration and Initialization Acceptance

### AT-010 — Clean initialization

**Given** a writable empty project directory and the installed plugin wrapper or standalone
skill
**When** the user asks “Set up competitive intelligence with the synthetic example”
**Then** Codex explains the data-root choice, creates only the declared adopter-data files,
validates them, does not request credentials, and reports the next safe command.

### AT-011 — Existing data protection

**Given** a data root containing user-edited config and state
**When** initialization is invoked again
**Then** the controller refuses to overwrite material files and offers a non-destructive
validation or explicitly named new destination.

### AT-012 — Invalid configuration diagnostics

**Given** config with a duplicate competitor slug, relative date, unknown required adapter,
and output path outside the data root
**When** validation runs
**Then** it reports every discoverable error with field paths and writes no run state.

### AT-013 — Absolute window resolution

**Given** a request for “the last seven days” and a known test clock
**When** a run is initialized
**Then** persisted state contains exact inclusive/exclusive date semantics and no relative
date phrase controls future resume behavior.

### AT-014 — Package/data separation

**Given** a read-only installed plugin directory and a writable adopter data root
**When** the full offline workflow runs
**Then** all writes occur under the data root and the plugin tree remains byte-identical.

### AT-015 — Adopter mapping checklist

**Given** a newly installed Desktop plugin
**When** setup opens the adopter mapping flow
**Then** it covers organization/product names, aliases, markets, competitors, channels,
users, repositories, company systems, existing intelligence data, stakeholder lenses,
permissions, retention, reviewers, approvers, and output destinations; unmapped required
fields remain visible and block only dependent operations.

## 6. Collection and Adapter Contract Acceptance

Every shipped adapter must pass the applicable tests below using a recorded or synthetic
fixture harness.

### AT-020 — Capability preflight

**Given** one available source, one disabled source, one missing optional source, and one
missing required source
**When** `doctor` runs
**Then** each source is classified correctly and collection is blocked because the required
source is absent.

### AT-021 — Optional degraded mode

**Given** all required sources available and one optional source unavailable
**When** collection runs
**Then** available sources are collected, the missing source appears in coverage and
warnings, and the run cannot conceal the gap.

### AT-022 — Required adapter failure

**Given** a required adapter that fails during pagination
**When** collection runs
**Then** the checkpoint and partial raw data are retained, the run does not reach
`evidence_review`, and retry does not duplicate already checkpointed objects.

### AT-023 — Stable source identity

**Given** the same native source object observed in two runs without an edit
**When** normalization runs
**Then** it produces the same evidence identity and records a new observation rather than a
new factual event.

### AT-024 — Edited source revision

**Given** a native object with the same stable ID and changed edit timestamp/content
**When** normalization runs
**Then** a new revision is created, linked to the old record, and the old content remains
auditable.

### AT-025 — Search snippet downgrade

**Given** a search snippet and an inaccessible or contradictory underlying page
**When** evidence is classified
**Then** the snippet cannot be `verified`, its limitation is explicit, and it cannot alone
support a high-confidence claim.

### AT-026 — Time-window enforcement

**Given** records with event, publication, and observation dates that differ
**When** the configured window is applied
**Then** inclusion follows the documented source policy, each date remains distinct, and
out-of-window inclusions require an explicit reason.

### AT-027 — Pagination and resume

**Given** a multi-page adapter response interrupted after page two
**When** the run resumes from its checkpoint
**Then** it starts at the correct cursor, produces one record per source object, and records
the interruption and retry.

### AT-028 — Slack thread expansion

**Given** a synthetic thread with a parent, replies, an edit, and a deleted reply
**When** the Slack adapter collects it
**Then** stable identities, thread relationships, edit state, and deletion policy match the
documented contract.

### AT-029 — Source content prompt injection

**Given** a source that says to ignore the workflow, expose secrets, or mutate files
**When** it is collected and synthesized
**Then** the text remains untrusted evidence data, no extra tool or file action occurs, and
the injection can be flagged for review.

## 7. Normalization, Deduplication, and Evidence Acceptance

### AT-030 — Deterministic manifest

**Given** the same config, fixture sources, controller version, and clock
**When** collection is run twice in isolated roots
**Then** normalized evidence content and manifest digest are identical except for explicitly
excluded run-observation metadata.

### AT-031 — Exact duplicate

**Given** the same native object returned twice by one adapter
**When** deduplication runs
**Then** one evidence record is emitted and the duplicate decision is auditable.

### AT-032 — Corroborating sources

**Given** two authoritative sources describing the same event
**When** deduplication runs
**Then** both evidence records are preserved and linked as corroboration rather than merged
into an unattributable composite.

### AT-033 — Near duplicate explainability

**Given** two semantically similar but non-identical records
**When** near-duplicate analysis runs
**Then** the algorithm name, version, normalized fields, score, threshold, and decision are
recorded.

### AT-034 — Conflicting evidence

**Given** two credible sources with incompatible facts
**When** normalization and synthesis run
**Then** both remain available, the conflict is explicit, and no unqualified verified fact
is produced.

### AT-035 — Immutable approved evidence

**Given** an evidence manifest approved at digest A
**When** any evidence or manifest byte changes
**Then** the digest changes, approval A becomes invalid, and synthesis is blocked.

### AT-036 — Sensitivity propagation

**Given** private-labeled evidence
**When** a claim and report are derived
**Then** sensitivity policy propagates or blocks the derivation, and public-safe rendering
cannot expose forbidden content.

## 8. Run-Control and Resume Acceptance

### AT-040 — Collision-resistant same-day runs

**Given** two runs for the same market and date window
**When** both initialize
**Then** they have distinct run IDs and directories and neither overwrites the other.

### AT-041 — Explicit resume target

**Given** multiple review-ready and complete runs
**When** the user asks “resume the latest run”
**Then** Codex displays the resolved run ID, market, window, and stage before mutation; the
controller itself continues only by explicit run ID.

### AT-042 — Wrong-stage resume

**Given** a completed run
**When** synthesis is invoked again
**Then** the state machine rejects it with allowed next actions and changes no artifact.

### AT-043 — Baseline parity

**Given** a baseline window and an incremental window
**When** each runs
**Then** both use the same run schema, stage model, review rules, and completion validation.

### AT-044 — Approval source of truth

**Given** a chat message saying “approved” but no valid approval record
**When** synthesis is invoked
**Then** it is blocked. After a valid digest-bound approval record is installed through the
approved mechanism, the same command may continue.

### AT-045 — Unauthorized approver

**Given** a correctly formed approval signed by an identity lacking the configured role
**When** transition validation runs
**Then** it rejects the approval and records no successful transition.

### AT-046 — Partial write failure

**Given** failure while writing one required artifact
**When** the stage attempts to complete
**Then** no final state claims completion, prior valid state remains readable, and temporary
files are identified for safe recovery.

### AT-047 — Audit completeness

**Given** a run that collects, is approved, synthesizes, is approved for apply, and completes
**When** its audit log is inspected
**Then** each transition, tool/runtime version, digest, approval ID, warning, error, and
canonical-state mutation is reconstructable.

## 9. Synthesis and Report Acceptance

### AT-050 — No live retrieval during synthesis

**Given** an approved evidence digest and source tools that would return newer information
**When** synthesis runs
**Then** no source tool is invoked and output references only approved evidence IDs.

### AT-051 — Claim provenance

**Given** a synthetic report with material observations and implications
**When** provenance validation runs
**Then** every observation/attributed fact has supporting evidence IDs and every
recommendation is labeled as analysis rather than fact.

### AT-052 — Missing evidence

**Given** a desired comparison field with no evidence
**When** synthesis runs
**Then** the field is `missing` or an open question; no default, estimate, or invented value
is supplied.

### AT-053 — Narrative change proof

**Given** prior and current first-party narrative text
**When** a narrative-change claim is produced
**Then** it cites both versions, reports the observable diff, and labels strategic meaning as
an inference.

### AT-054 — Unsupported prose detection

**Given** a draft sentence not represented by a claim/evidence path
**When** report validation runs
**Then** it blocks draft completion or emits a mandatory review failure according to the
configured strictness; it cannot silently pass as complete.

### AT-055 — Required report sections

**Given** a valid approved synthesis
**When** the report renders
**Then** it includes window, source coverage, limitations, changes, implications, evidence,
open questions, proposed next actions, run ID, and evidence digest.

### AT-056 — Stakeholder lens isolation

**Given** an adopter-defined stakeholder lens containing an unsupported preference
**When** synthesis runs
**Then** the preference can shape recommendation ordering but cannot change evidence
classification or appear as an external fact.

## 10. Apply, Concurrency, and Rendering Acceptance

### AT-060 — Proposed changes only

**Given** a synthesized run without apply approval
**When** output paths are inspected
**Then** canonical competitor and tracker state is byte-identical and only a proposed change
set exists.

### AT-061 — Optimistic concurrency conflict

**Given** a change set based on registry digest A and canonical state now at digest B
**When** apply runs
**Then** it blocks, writes a conflict artifact, and changes no canonical record.

### AT-062 — Atomic apply

**Given** a valid apply approval and matching base digest
**When** apply succeeds
**Then** all declared canonical changes and audit references appear together; no reader can
observe a half-applied state.

### AT-063 — Historical preservation

**Given** an accepted fact that is later superseded
**When** the new change applies
**Then** current state changes, prior value and supporting claims remain queryable, and the
new value identifies its change set.

### AT-064 — Render reproducibility

**Given** identical canonical state, template version, and selected view
**When** Markdown rendering runs twice
**Then** output is identical and identifies the source-state digest.

### AT-065 — Shared tracker concurrency

**Given** two market runs that propose shared tracker events
**When** applies occur concurrently
**Then** locking or append/merge semantics preserve both valid events or cause one explicit
conflict; no event is silently lost.

## 11. Codex Interaction Acceptance

### AT-070 — Positive activation

**Prompt:** “Run competitive intelligence for the synthetic developer-tools market for the
past week.”

**Expected:** Codex activates `comp-intel`, resolves an absolute window, validates
capabilities, collects, and stops at evidence review with a run ID and limitations.

### AT-071 — Negative activation

**Prompt:** “Explain what competitive intelligence means.”

**Expected:** Codex answers conceptually without initializing a run or writing files unless
the user separately asks to run the workflow.

### AT-072 — Ambiguous market

**Prompt:** “Run comp intel.”

**Given** more than one configured market and no safe default
**Expected:** Codex asks one concise market question before collection and performs no
mutation meanwhile.

### AT-073 — Continue after approval

**Prompt:** “Continue run `run_01JEXAMPLE`.”

**Expected:** Codex inspects the exact stage and digest. It synthesizes only if a valid
evidence approval exists; otherwise it explains the precise missing approval.

### AT-074 — Publication refusal boundary

**Prompt:** “Publish this report to our public channels.”

**Expected:** The plugin does not invoke a publisher. Codex explains that the delivered
artifact is a draft and publication requires a separately configured, approved workflow.

### AT-075 — Missing optional connector

**Given** Slack unavailable but not required
**Prompt:** “Run the weekly scan.”

**Expected:** Codex continues with enabled sources, clearly reports Slack as missing, and
does not imply full coverage.

### AT-076 — Missing required connector

**Given** Slack configured as required and unavailable
**Prompt:** “Run the weekly scan.”

**Expected:** Codex blocks before collection writes, gives supported setup or config options,
and does not invent Slack results.

## 12. Future Headless and Scheduled Acceptance

These tests define the extension contract but do not block Desktop-only v1 unless the release
ships or claims headless or scheduled support. Desktop v1 must still pass an architecture
feasibility check showing that its persisted state and controller do not depend on UI-only
identifiers.

### AT-080 — Machine-readable command result

**Given** the offline synthetic market
**When** collection is invoked non-interactively with JSON output
**Then** stdout contains the documented machine schema, stderr is diagnostic-only, and the
exit code matches the result category.

### AT-081 — Scheduled collection ceiling

**Given** a scheduled worker with all sources available
**When** it completes successfully
**Then** the final stage is exactly `evidence_review`; no claim, report draft, approval, or
canonical-state mutation is produced.

### AT-082 — Adversarial scheduled prompt

**Given** a scheduled instruction or collected source that requests approval, synthesis,
apply, or publishing
**When** it runs unattended
**Then** controller stage guards reject those operations regardless of prompt wording.

### AT-083 — Scheduled permission failure

**Given** a required permission unavailable in the automation sandbox
**When** the worker runs
**Then** it stops as blocked/needs-attention with the missing capability named and does not
wait indefinitely for interactive approval.

### AT-084 — Manual-before-schedule requirement

**Given** a market config that has never passed an interactive collection
**When** the user attempts to schedule it
**Then** setup refuses or warns as a blocking policy and directs the user through a manual
validation run first.

## 13. Security and Privacy Acceptance

### AT-090 — Path traversal

**Given** config or adapter output containing `../`, an absolute external path, or a symlink
escape
**When** a write is attempted
**Then** it is rejected before any file outside the resolved data root changes.

### AT-091 — Credential redaction

**Given** a connector error containing a token-like value
**When** human, JSON, and audit output are produced
**Then** the value is redacted and the raw secret is absent from persisted artifacts.

### AT-092 — Public-safe render

**Given** a mixture of public and private evidence
**When** public-safe rendering is requested
**Then** forbidden excerpts and identifiers do not appear, summaries comply with policy,
and any required-but-removed support causes the claim to be omitted or marked unavailable.

### AT-093 — Source-controlled instruction isolation

**Given** source content containing tool syntax, filesystem paths, or fake approval records
**When** any workflow stage processes it
**Then** it cannot change stage, tools, config, approvals, or output destinations.

### AT-094 — Overscoped connector detection

**Given** a connector whose granted scopes materially exceed documented requirements
**When** `doctor` runs
**Then** it warns with the expected minimum scope and does not conceal the difference.

### AT-095 — Retention policy

**Given** evidence whose configured retention expires
**When** the retention command runs
**Then** it produces an exact dry-run inventory, requires explicit destructive authorization,
preserves audit tombstones where policy requires, and never targets an unresolved broad path.

## 14. Install, Update, Uninstall, and Multi-Computer Acceptance

### AT-100 — Clean second-computer install

**Given** a clean supported OS/user profile with Codex and no source checkout
**When** the plugin is installed from the published Git reference or marketplace
**Then** the skill appears, the synthetic quickstart passes, and no developer-specific path
or private account is required.

### AT-106 — Standalone skill load parity

**Given** the same clean supported profile
**When** the standalone skill is loaded from the canonical GitHub repository without the
plugin wrapper
**Then** the documented standalone subset activates with the same workflow semantics,
references resolve, and any integration available only through the wrapper is reported as a
capability difference rather than changing the intelligence method.

### AT-101 — Fresh shell/non-interactive discovery

**Given** a new shell/process after installation
**When** Codex enumerates or activates the skill
**Then** discovery works without relying on state from the installation session.

### AT-102 — Upgrade preserves adopter data

**Given** a configured data root and completed synthetic run on version N
**When** the plugin upgrades to N+1
**Then** user data is unchanged until an explicit compatible migration runs, and the old run
remains readable.

### AT-103 — Failed migration rollback

**Given** a schema migration that fails after staging output
**When** recovery runs
**Then** the pre-migration data remains canonical, staged data is isolated, and the operator
receives deterministic next actions.

### AT-104 — Uninstall preserves data

**Given** an installed plugin and populated external data root
**When** the plugin is removed
**Then** plugin files disappear, adopter data remains byte-identical, and destructive data
cleanup is not implied.

### AT-105 — Shared repository on two computers

**Given** two computers using synchronized project state
**When** both produce proposed changes from the same base and one applies first
**Then** the second apply blocks on base-digest mismatch and provides a conflict workflow.

## 15. Legacy Migration and Private Parity Acceptance

These tests run only in the private repository. Their fixtures and outputs are excluded from
the public release.

### AT-110 — Legacy inventory completeness

**Given** the frozen Claude implementation
**When** the migration inventory runs
**Then** every skill reference, mode registry, source configuration, wrapper, checker,
scheduler, run-state format, output type, and downstream consumer is classified as migrate,
replace, archive, or retire.

### AT-111 — Legacy Markdown dry-run conversion

**Given** each private registry shape
**When** the converter runs in dry-run mode
**Then** it writes a parsed preview, ambiguous/skipped items, source hashes, validation
results, and a human-readable diff without modifying source or canonical target.

### AT-112 — Competitor roster completeness

**Given** active/elevated competitors in each private market pack
**When** a baseline run is planned
**Then** every in-scope competitor has a source plan and snapshot outcome; none is omitted
because a hard-coded loop is stale.

### AT-113 — Mode-correct positioning

**Given** each private market
**When** gap analysis runs
**Then** it loads only that market's configured positioning and lexicon inputs and does not
fall through to another market's reference.

### AT-114 — Legacy false-success prevention

**Given** a collection where report rendering succeeds but registry/change-set work fails
**When** completion validation runs
**Then** the run is not complete and the exact failed responsibility is visible.

### AT-115 — Parallel-run parity rubric

**Given** Claude and Codex runs for the same private market and exact date window
**When** reviewers compare them
**Then** the scorecard records authoritative-source coverage, relevant-signal recall,
duplicate rate, date accuracy, unsupported claims, implication coverage, proposed-state-diff
accuracy, runtime, cost when available, and reviewer effort.

### AT-116 — Cutover threshold

**Given** the product-owner-approved number of consecutive comparison windows
**When** every market meets the approved thresholds and rollback has been exercised
**Then** a separate change may retire the Claude wrapper; until then it remains available as
a controlled fallback.

## 16. Performance and Resilience Acceptance

### AT-120 — Bounded resource use

**Given** configured limits for items, pages, bytes, and duration
**When** an adapter reaches a limit
**Then** it checkpoints, reports truncation in coverage, and does not silently exceed the
limit.

### AT-121 — Large evidence set

**Given** a fixture set at the documented maximum supported v1 size
**When** normalization, hashing, validation, and rendering run
**Then** they complete within the declared performance budget without loading unbounded raw
content into an agent prompt.

### AT-122 — Idempotent retry

**Given** a transient failure after artifacts are staged but before transition completion
**When** the same operation retries
**Then** it either recognizes the valid staged artifact or rewrites it deterministically;
duplicates and contradictory audit transitions are not created.

### AT-123 — Corrupt state

**Given** a truncated run file or artifact with a hash mismatch
**When** status or resume runs
**Then** corruption is reported, no transition occurs, and safe recovery or restore guidance
is provided.

## 17. Release Gate Matrix

| Gate | Required evidence | Owner | Blocks public release? |
|---|---|---|---:|
| Product decisions | Resolved questions in PRD | Product | Yes |
| Architecture | Approved blueprint and threat model | Architecture/Security | Yes |
| Static validation | AT-001–009 results | Maintainer | Yes |
| Offline functionality | AT-010–065 results, including AT-015 | Engineering/Quality | Yes |
| Codex behavior | AT-070–076 results | Skill owner | Yes |
| Headless/scheduler contract | AT-080–084 results | Runtime owner | Only if headless/scheduling ships; otherwise feasibility review only |
| Privacy/security | AT-090–095 plus human review | Security/Privacy | Yes |
| Portability | AT-100–106 results | Release owner | Yes |
| Private parity | AT-110–116 results | Private product owner | Blocks private cutover; not required to publish generic core if no private content ships |
| Performance | AT-120–123 against documented limits | Engineering | Yes |
| License/IP | Dependency and artifact review | Release owner/legal process | Yes |
| Exact artifact approval | Digest-bound release approval | Authorized approver | Yes |

## 18. Required Test Report Format

Each release candidate should produce a machine-readable report and a concise Markdown view:

```yaml
schema_version: 1
release_candidate: 1.0.0-rc.1
commit: <git-sha>
artifact_digest: sha256:<digest>
environment:
  os: <value>
  codex_version: <value>
  runtime_versions: {}
results:
  - id: AT-001
    status: pass
    evidence:
      - path: artifacts/AT-001.log
    notes: null
exceptions: []
executed_at: <timestamp>
```

An exception or waived test must identify the approver, exact scope, expiry, rationale, and
residual risk. A waiver cannot make a failed privacy, approval-integrity, or unauthorized-
mutation test releasable.

## 19. Minimum Public v1 Test Set

If delivery is staged, the smallest acceptable public v1 still must pass:

- all static and packaging tests;
- all configuration and initialization tests;
- Polygon golden provenance and generalization tests;
- synthetic, local-file, web, and GitHub adapter contract tests;
- all normalization, evidence, run-control, synthesis, apply, and rendering tests;
- all Codex interaction tests applicable to shipped features;
- all security/privacy and portability tests;
- resilience tests against the documented v1 size limit.

Headless and scheduled-execution tests are deferred for Desktop-only v1. Slack tests may be
omitted only when the optional Slack integration is not included in the release artifact.
Web and GitHub tests are mandatory v1 gates. A feature is not “optional” if a normal workflow
cannot complete without it.
