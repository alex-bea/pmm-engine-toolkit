---
doc_type: DOC
normative: false
requires:
  - ../../plugins/pmm-instinct-review/skills/pmm-instinct-review/references/DOC-product-requirements.md
  - ../STD-evidence-privacy-v1.0.md
status: Draft
version: "0.3.1"
owner: toolkit-maintainers
consumers:
  - public toolkit maintainers
change_control: Pull request review
---

# PMM Instinct Review `0.3.1` IP and privacy review

## Scope and preliminary decision

This Draft covers the proposed Codex persisted-model and RUN/REF routing parity changes, the
unchanged public Claude and portable boundaries, fictional configuration updates, and direct
documentation, tests, validation, release, provenance, and security evidence. It supports
candidate review only. Required local automated scans and independent final-diff review are
complete. Hosted checks passed on PR #17 for implementation commit `90d5177`; project-owner
Gate B review remains pending. This record does not approve merge or publication.

The fidelity reference is the private PMM Engine Codex implementation. The public result uses
generic adopter-owned configuration. No private model choice, capability registry, route value,
repository alias, state, transcript, output, or reversible private-to-fictional mapping is
authorized. The change does not claim parity with the private Claude promotion transaction
architecture.

## Data flow and retention boundary

Codex config stores one adopter-supplied extractor-model identifier and optional relative
`run_routes` and `voice_ref_routes` values under the existing user-owned state root. The model
identifier is persisted before enablement and is the sole authority for new capture/backfill
jobs. A model identifier in session or native-history metadata cannot supply or override it.
An enabled legacy store with no model returns `skipped` / `unconfigured_model` before creating
normalized evidence, an audit, or a queue record.

Route values may expose adopter-owned skill/document names to local users or processes with
state-root access. The resolver confines them to independently discovered user-owned roots for
the exact source skill and does not use them to widen filesystem discovery. An ambiguous choice
may return exact absolute eligible paths to the local operator. It does not send those paths to
a hosted PMM service or read target contents merely to enumerate choices.

Eligible Codex evidence still follows the existing local capture, minimization, redaction,
provider-processing, retention, and deletion boundary described in `PRIVACY.md`. Native Codex
history and every Claude store remain read-only and isolated from this change.

## Safety controls

- The Codex adapter contains no default model and its public route maps are empty.
- Absolute paths, parent traversal, wrong filename families, missing/directories/non-writable
  targets, cross-skill paths, plugin/cache-owned targets, and symlink escapes are ineligible.
- Multiple eligible RUN/REF paths produce no applicable preview or target change. The owner
  must provide an exact `--target` from the recomputed set.
- Apply retains the existing separate human confirmation and recomputes route eligibility.
- Existing string REF routes and explicit-model queue jobs remain compatible without a
  destructive state migration.
- Native Claude and portable behavior remain unchanged and isolated.

## Public-safe construction assessment

The proposed contracts, runtime changes, tests, and evidence are project-authored generic
artifacts for this public repository. The Northstar Reports configuration remains independently
authored fiction; its model and route strings illustrate schemas and are not live targets,
private aliases, or Codex defaults. Nominative Codex, Claude Code, OpenAI, and Anthropic
references describe interoperability and provider processing only.

## Verification status

| Review | Status |
|---|---|
| Exact changed-path and approved-manifest comparison | Pass: exactly 29 modifications and five additions |
| Publicizer private-term and developer-path scan | Pass: exact changed set clean with external run-specific denylist |
| Targeted absolute-path and route-value review | Pass: no private path or live route; examples are fictional relative values |
| Full tracked-tree Gitleaks scan | Pass: Gitleaks 8.30.1, zero findings; adjacent generated JSON is `[]` |
| IP inventory regeneration and exact-set comparison | Pass: 448 artifacts; repeat generation identical |
| Focused and complete automated tests | Pass: 80 Codex/portable, 79 Claude, and 266 complete tests |
| Independent privacy and narrative review | Pass: no remaining actionable finding |
| Native Codex lifecycle smoke | Not run: no separately authorized isolated hook lifecycle and adopter-selected smoke model were used |
| Hosted pull-request checks | Pass on PR #17 at `90d5177`: CodeQL, dependency review, governance, and Python 3.10–3.14 |
| Project-owner review | Pending |

Results must be entered only from the exact final candidate. An unavailable check is `not run`,
not a pass, and keeps the release Draft.

## Residual risk

Pattern redaction and secret/private-term scans cannot prove that all sensitive or narratively
identifying input is absent. Adopter-supplied model and route strings can themselves reveal
internal naming. A user with local write access can alter configuration, hooks, or targets. A
wrong but syntactically valid route inside the correct skill root can still reflect an adopter
configuration mistake. These risks are bounded through explicit model choice, no Codex adapter
default, local owner-only state where supported, root/family/file validation, exact ambiguity
choice, two human gates, no private bundled mapping, and final review; they are not eliminated.
