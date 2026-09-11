---
doc_type: DOC
normative: false
requires:
  - IP-PRIVACY-REVIEW-PMM-INSTINCT-REVIEW-0.3.1-2026-09-11.md
status: Draft
version: "0.3.1"
owner: toolkit-maintainers
consumers:
  - public toolkit maintainers
change_control: Pull request review
---

# PMM Instinct Review `0.3.1` rights review

## Scope

This Draft covers the bounded public Codex model/routing parity candidate and its direct
documentation, configuration, fictional example, tests, validator, release, legal, and security
records. Exact inventory regeneration, dependency/license review, and independent final-diff
review are complete. Hosted checks passed on PR #17 for implementation commit `90d5177`;
project-owner Gate B review remains pending. This record is not approval to merge, tag,
release, or publish.

## Preliminary provenance assessment

The candidate is represented as project-authored implementation, tests, documentation,
schemas, templates, and independently fictional examples for this Apache-2.0 repository.
Private implementation experience supplies behavioral requirements only. No private source
file, transcript, state, populated registry, route value, model default, output, identifier,
machine path, or one-to-one fictionalization map is authorized for redistribution.

The public `run_routes` and `voice_ref_routes` values are empty templates. Northstar Reports
uses its existing fictional model token and newly authored fictional route strings solely to
demonstrate shape. Codex,
Claude Code, OpenAI, and Anthropic are nominative interoperability/provider references; no
affiliation or endorsement is claimed.

## Redistribution basis

Project-authored candidate artifacts are intended to be offered under the repository's
Apache-2.0 license. `LICENSE`, `NOTICE`, and `THIRD_PARTY_NOTICES.md` are outside this change
and remain unchanged. The final generated IP inventory must include exactly one complete row
for each repository artifact, including all five new `0.3.1` evidence paths, before this review
can be finalized.

## Exclusions

The candidate excludes private repositories and histories, real user sessions, organization
or customer facts, credentials, live internal URLs, private route tables, machine-specific
paths, mutable adopter state, private default models, and third-party implementation code or
substantive prose.

## Verification status

- Exact approved-manifest comparison: pass; 29 modifications and five additions, no extra path.
- IP inventory regeneration and exact-set comparison: pass; 448 artifacts and identical repeat generation.
- Private-term, developer-path, and independent narrative review: pass; no remaining actionable finding.
- Tracked-tree secret scan: pass; Gitleaks 8.30.1 found zero findings.
- Dependency and license-delta review: pass; dependency manifests, locks, workflows, license,
  notice, and third-party notice are unchanged, and changed runtime imports remain standard
  library or package-local.
- Hosted checks: pass on PR #17 at `90d5177` for CodeQL, dependency review, governance, and
  Python 3.10–3.14.
- Project-owner final-diff review: pending.

Any new dependency, changed provenance, or candidate edit requires these checks and this Draft
record to be refreshed. A pending or unavailable check cannot support a redistribution or
release-readiness claim.
