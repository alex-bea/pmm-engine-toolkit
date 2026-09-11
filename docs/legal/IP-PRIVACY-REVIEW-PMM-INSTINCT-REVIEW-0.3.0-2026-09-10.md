---
doc_type: DOC
normative: false
requires:
  - ../../plugins/pmm-instinct-review/skills/pmm-instinct-review/references/DOC-product-requirements.md
  - ../STD-evidence-privacy-v1.0.md
status: Draft
version: "0.3.0"
owner: toolkit-maintainers
consumers:
  - public toolkit maintainers
change_control: Pull request review
---

# PMM Instinct Review `0.3.0` IP and privacy review

## Scope and decision

This Draft review covers the proposed native Claude additions under
`plugins/pmm-instinct-review/`, the retained Codex and portable package, and their direct
tests, catalog/export registration, release note, and legal/security evidence. It supports
candidate review only. Local privacy, provenance, scanning, structural, and test checks are
complete, and the hosted pull-request checks pass. A real Claude lifecycle smoke test and
project-owner Gate B review remain pending; this document does not approve merge or publication.

## Public-safe construction assessment

- The proposed runtime, installer, documentation, schemas, templates, tests, and fictional
  examples are project-authored generic artifacts for this public repository.
- Private behavior informed functional requirements, but no private source file, transcript,
  audit, suggestion, instinct, output, identifier, route table, machine path, configuration, or
  alias map is authorized for inclusion.
- The Northstar Reports Claude lifecycle is independently authored fiction. Its entities,
  dates, IDs, paths, language, and relationships are synthetic; any web or email values must
  use reserved `.invalid` domains.
- The native Claude implementation is an independently reviewed public implementation, not a
  public copy of private evidence, hooks, installer state, or destination mappings.
- Codex and portable behavior remain covered by the historical `0.2.0` evidence, but that
  historical evidence does not approve the additive `0.3.0` boundary.

## Data flow and retention boundary

Installation does not enable capture. First enablement requires explicit privacy
acknowledgment. Native Codex and Claude capture use separate user-owned state roots and keep
only bounded, redacted conversation roles from eligible main-thread sessions. System and
developer instructions, reasoning, tool calls and results, patches, world state, and
compaction payloads are excluded from normalized evidence. Local state also records the
session/job identifiers, timestamps, content digests, paths, and project-directory metadata
needed for idempotence, routing, review, and recovery. Claude also writes a short-lived local
capture request containing the session ID, native transcript path, project directory, and
timestamp, but no conversation text; a detached worker removes it after processing.

Extraction submits normalized evidence to the configured runtime provider: OpenAI for Codex
or the configured Anthropic model through Anthropic's API or a supported cloud provider for
Claude. The public package has no hosted PMM service or telemetry, but the provider may process
that evidence under the adopter's account terms and settings. The Claude worker's `--bare`
invocation does not reuse ordinary subscription login or keychain state. Review decisions
delete only the normalized evidence; audit, suggestion, queue, instinct, sanitized log, and
promotion records remain local until the adopter removes them. Native session history is not
modified.

Promotion requires a separate human approval bound to the exact preview and target state.
Local delivery may change only the approved result. Governed delivery creates a local review
patch and does not mutate the governed destination. The package does not approve, merge, or
publish automatically.

## Required verification

The frozen candidate passed the complete package publicizer scan, repository public-safety and
skill-pack validators, a zero-finding full-tree Gitleaks scan, 243 public unit tests, the 57-test
Codex/portable regression suite, the 79-test public Claude suite, the 84-test mirrored private
Claude suite, fictional cross-file tests, a 61-document strict audit, and GitHub Actions
validation. The approved-manifest comparison is exact at 57 paths: 36 additions and 21
modifications, with no missing, extra, or action-mismatched path. The generated IP inventory is
exact at 443 rows for 443 artifacts. The exact-slice private-term scan produced matches only in
content already present on the current base; diff review confirmed that candidate-added content
introduced none. Agent-assisted privacy and narrative review found no remaining
actionable P0, P1, or P2 issue.

The destination-machine Claude smoke test was not run because this host has no `claude`
executable. Hosted CodeQL, dependency review, governance, and Python 3.10–3.14 checks pass.
Project-owner narrative review remains pending at Gate B. The missing native smoke and owner
approval prevent a release-readiness or merge claim, but do not invalidate the completed
candidate evidence.

## Residual risk

Automated redaction and pattern scanning cannot prove that every sensitive or narratively
identifying detail is absent. User transcripts and imported candidates may contain sensitive
content, and the configured provider receives normalized evidence during extraction. A local
user or process with write access can alter or bypass user-controlled hooks. These risks are
bounded, not eliminated, through disabled-by-default capture, explicit acknowledgment,
conversation-only minimization, bounds and redaction, isolated state, tool-disabled extraction,
exact-digest human approvals, governed review delivery, no bundled private routes, and final
human review.
