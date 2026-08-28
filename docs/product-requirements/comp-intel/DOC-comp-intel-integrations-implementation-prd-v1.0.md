---
doc_type: DOC
normative: false
requires:
  - DOC-comp-intel-codex-migration-prd-v1.0.md
  - DOC-comp-intel-codex-implementation-blueprint-v1.0.md
  - DOC-comp-intel-public-acceptance-tests-v1.0.md
  - DOC-comp-intel-codex-skill-implementation-prd-v1.0.md
  - ../../STD-evidence-privacy-v1.0.md
  - ../../STD-approval-gates-v1.0.md
status: Draft
version: "1.0"
owner: Alex Bea
consumers:
  - Integration implementers
  - Security reviewers
  - Skill implementers
  - Test engineers
change_control: PR Review and product-owner approval
---

# Comp Intel Integrations Implementation PRD

## 1. Outcome

Provide a connector-neutral integration layer that lets the Codex Desktop skill collect
competitive evidence from configured public and private sources without embedding one
company's workspace IDs, repository names, credentials, or tool implementation identifiers.

The public v1 product ships support for synthetic fixtures, local files, web research, and
GitHub. Slack is an additional optional integration. Each integration follows the same
adapter contract, capability preflight, evidence schema, error model, checkpoint model, and
privacy controls.

## 2. Scope and Release Boundary

### 2.1 Shipped v1 integrations

- Synthetic fixture adapter for deterministic offline tests.
- Local-file adapter for explicitly allowed paths.
- Web search and page retrieval through the supported Codex capability.
- GitHub through an installed Codex plugin/connector, neutral MCP mapping, or approved
  read-only local tool.
- Codex Desktop capability discovery and connection-status presentation.

“Shipped” means the public product implements and tests the adapter. A market may still mark
web or GitHub optional, disabled, or required according to its source policy.

### 2.2 Optional Slack integration

- Slack through an installed Codex plugin/connector or neutral MCP mapping.
- Slack is disabled until the adopter maps its own workspace, channels, users, queries,
  privacy policy, and minimum permissions.
- Slack absence must not break synthetic, local, web, GitHub, or public Polygon workflows.

### 2.3 Out of scope

- Bundling credentials or private connector configuration.
- Automatically installing third-party connectors.
- Writing to Slack, GitHub, CRM, email, or publication systems.
- Using internal company systems without an adopter mapping.
- Real-time streaming surveillance.
- Headless authentication and unattended connector refresh in v1.

## 3. Adapter Contract

Every adapter declares:

- stable adapter ID and version;
- source classes it can produce;
- required configuration and connection type;
- supported capability probes;
- cursor/checkpoint format;
- rate-limit and retry behavior;
- stable source-identity strategy;
- private/public sensitivity defaults;
- raw-content retention behavior;
- error categories;
- minimum permissions.

Conceptual interface:

```python
class SourceAdapter(Protocol):
    adapter_id: str
    version: str

    def probe(self, config: SourceConfig) -> CapabilityResult: ...
    def collect(self, request: CollectionRequest) -> Iterable[RawCandidate]: ...
    def checkpoint(self) -> AdapterCheckpoint: ...
```

Adapters read configured sources and return normalized candidates. They cannot approve runs,
synthesize claims, mutate canonical competitor state, send messages, or publish.

## 4. Desktop Connection Experience

### 4.1 Capability preflight

Before a run starts, Desktop displays:

| State | Meaning | Run behavior |
|---|---|---|
| Available | Connection and minimum permissions validate | Collect |
| Disabled | Adopter intentionally disabled source | Exclude and report |
| Missing optional | Source is configured optional but unavailable | Continue with coverage warning |
| Missing required | Source is required but unavailable | Block before collection |
| Overscoped | Granted permissions exceed documented minimum | Warn and require policy decision if configured |
| Degraded | Connection works but a capability such as thread expansion is unavailable | Follow source policy or block |

Connection setup must use Codex's supported installation/connection experience. The skill
must never ask the user to paste a token into chat or commit a secret to configuration.

### 4.2 Adopter source mapping

The setup checklist requires users to map their own:

- workspace and organization names;
- channel and user aliases to stable connector identifiers;
- GitHub organizations, repositories, branches, releases, issues, and labels;
- company document systems and allowed roots;
- web domains, official source types, and domain allow/deny policy;
- search terms, competitor aliases, product names, and languages;
- required/optional status by market;
- retention and sensitivity policy;
- minimum connector permissions.

Polygon mappings in the golden pack must use public sources only. Internal Polygon channel,
user, repository, or system identifiers cannot appear in the public package.

## 5. Integration Requirements

### 5.1 Synthetic adapter

- **IFR-001:** Ship with the public package and require no account or network.
- **IFR-002:** Support pagination, duplicates, edits, conflicts, missing dates, prompt
  injection, timeouts, and required failures through fixtures.
- **IFR-003:** Produce deterministic evidence and manifest digests under a fixed test clock.
- **IFR-004:** Use only fictional entities and reserved example domains.

### 5.2 Local-file adapter

- **IFR-010:** Read only from explicitly allowed roots.
- **IFR-011:** Reject absolute-path escape, traversal, and symlink escape.
- **IFR-012:** Record relative path, content hash, observed timestamp, media type, parser
  version, and sensitivity.
- **IFR-013:** Enforce configured file-count, byte, and format limits.
- **IFR-014:** Treat file contents as untrusted source data.
- **IFR-015:** Make unsupported or corrupt files visible in coverage.

### 5.3 Web adapter

- **IFR-020:** Separate search discovery from source-page retrieval.
- **IFR-021:** Preserve canonical URL, source title, publication date when known, observation
  date, query, and retrieval outcome.
- **IFR-022:** Never classify a search snippet alone as verified.
- **IFR-023:** Prefer first-party public sources under the configured source policy.
- **IFR-024:** Validate time-window inclusion using documented date semantics.
- **IFR-025:** Honor domain allow/deny policy and record redirects.
- **IFR-026:** Respect quotation, redistribution, robots/access, and source-retention limits.
- **IFR-027:** Make inaccessible or dynamically incomplete pages explicit rather than
  reconstructing missing content.

### 5.4 Slack adapter

- **IFR-030:** Use stable workspace/message IDs and edit timestamps without exposing them in
  public examples.
- **IFR-031:** Support pagination, thread expansion, reply relationships, edits, deletions,
  cursor resume, and rate-limit checkpointing.
- **IFR-032:** Record channel and author display data only according to sensitivity policy.
- **IFR-033:** Scope searches to mapped channels and terms; no implicit workspace-wide scan.
- **IFR-034:** Distinguish original statements, quoted external claims, reactions, and
  analyst interpretation.
- **IFR-035:** Default all real Slack evidence to private unless the adopter explicitly sets
  a stricter organization policy.
- **IFR-036:** Require read-only minimum permissions and document the exact scope.

### 5.5 GitHub adapter

- **IFR-040:** Normalize repository, release, tag, commit, pull request, issue, comment, and
  publication timestamps.
- **IFR-041:** Record repository visibility and prevent private content from entering a
  public-safe render.
- **IFR-042:** Use immutable SHAs or native IDs when available.
- **IFR-043:** Distinguish shipped releases from roadmap issues, proposals, open pull
  requests, and forks.
- **IFR-044:** Apply configured authority rules for first-party versus third-party
  repositories and comments.
- **IFR-045:** Use read-only minimum permissions.

## 6. Normalization and Evidence Handoff

All adapters produce `RawCandidate` objects with:

- adapter/source identity;
- canonical source reference;
- native object/version identity;
- title and raw or summarized content reference;
- event, publication, modification, and observation times where available;
- query and collection checkpoint;
- authority and sensitivity hints;
- collection errors or truncation flags.

The shared normalizer—not the adapter—assigns evidence schema fields, source-quality labels,
deduplication relationships, retention outcomes, and manifest hashes. This prevents Slack,
web, or GitHub-specific logic from changing the claim model.

## 7. Failure, Retry, and Coverage

- Required adapter probe failure blocks before run collection.
- Required adapter collection failure prevents `evidence_review`.
- Optional failure produces a coverage warning and `needs_attention` when policy requires.
- Retry resumes from an immutable checkpoint and cannot duplicate accepted source objects.
- Rate-limit exhaustion records the next safe retry time when known.
- Partial raw data is retained according to policy but cannot masquerade as complete
  coverage.
- Connector implementation details may appear in diagnostics, but user-facing output uses
  stable adapter names and actionable setup guidance.

## 8. Security and Privacy

- Store secrets only in the supported connector/platform secret mechanism.
- Redact token-like values from human, JSON, log, and audit output.
- Prevent source content from changing config, tools, approvals, paths, or stages.
- Enforce minimum permissions and warn when granted scopes exceed them.
- Carry source sensitivity into evidence, claims, reports, and public-safe renders.
- Keep public Polygon examples limited to public web or public GitHub evidence unless another
  source is explicitly approved for redistribution.
- Do not publish screenshots or copied internal UI data as configuration examples.

## 9. Desktop-First and Headless Extension

Version 1 probes and invokes integrations through Codex Desktop. The adapter protocol must
not depend on a Desktop conversation ID. Configuration stores logical adapter IDs and source
mappings, not ephemeral UI connection handles.

A future headless adapter may provide a different authentication and invocation bridge, but
must implement the same probe, collection, checkpoint, evidence, error, and sensitivity
contracts. Headless support is not accepted by merely making the Desktop command callable
from a shell; its permission and unattended-failure behavior requires a separate release.

## 10. Implementation Checklist

- [x] Set v1 integrations to web, GitHub, synthetic fixtures, and local files; keep Slack
      optional.
- [ ] Define the adapter protocol and JSON Schemas.
- [ ] Implement shared capability and error models.
- [ ] Build the synthetic adapter and contract harness first.
- [ ] Build the local-file adapter and path-security tests.
- [ ] Map Codex Desktop connection discovery to logical adapter IDs.
- [ ] Implement web and GitHub as shipped adapters.
- [ ] Implement Slack as an independently enableable optional adapter.
- [ ] Document minimum permissions and overscope behavior.
- [ ] Add the adopter mapping schema for channels, users, repos, systems, domains, aliases,
      retention, and sensitivity.
- [ ] Add pagination, checkpoint, edit, deletion, duplicate, conflict, and rate-limit tests.
- [ ] Add prompt-injection and secret-redaction tests.
- [ ] Ensure Polygon golden examples contain no internal connector mapping.
- [ ] Verify optional adapter removal does not break the base skill.
- [ ] Record the future headless adapter seam without advertising support.

## 11. Acceptance

This PRD is satisfied when:

1. every shipped adapter passes AT-020–029 and its source-specific requirements;
2. synthetic, local-file, web, and GitHub adapters pass their applicable public and protected
   test suites;
3. the Desktop skill reports capability states and degraded coverage correctly;
4. no connector identifier, secret, or organization mapping is embedded in workflow prose;
5. Polygon golden examples pass public-source and privacy review;
6. a connector can be replaced behind the logical adapter ID without changing evidence,
   claim, or run schemas;
7. Slack is accurately described as optional and the base workflow passes without it;
8. the headless feasibility review confirms a new runtime bridge can reuse the adapter
   contract.

## 12. Open Decisions

1. Whether optional Slack wiring lives in the thin plugin wrapper or a companion plugin.
2. Whether web collection is controller-owned or a bounded Codex tool step returning the
   same adapter schema.
3. Whether GitHub's default bridge is the installed connector, neutral MCP, or an approved
   read-only local tool.
4. Whether connector overscope is a warning or blocking policy by default.
5. Which private company systems, beyond Slack and GitHub, require an adapter in the private
   migration but remain outside the public v1 package.
