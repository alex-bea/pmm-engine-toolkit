# Public Export Manifest

## Approved v1 boundary

This local fresh-history repository contains the 25 standalone skills and one draft Codex
plugin listed in `SKILL-CATALOG.md`, Diffguard Lite, shared public standards, reusable
templates, synthetic examples, and tests.
The root governance set covers contributions, conduct, project decisions, security,
support, privacy, licensing, and independent setup.

It also contains the `skill-governance` Codex plugin, its public marketplace entry, and three
self-contained governance skills that can be installed independently from GitHub.

The repository also contains a complete, agent-neutral competitive-intelligence starter kit
under `skills/comp-intel/`: a working analyst method, fillable source/registry/positioning/
tracker templates, a guided first-run procedure, review gates, a full-depth fictional
embedded-wallet example with one completed counterpart for every human-readable template,
and an optional deterministic controller. The example is a non-reversible structural mirror:
it retains reusable analytical depth but contains no real entity, fact, URL, or alias map. The
setup procedure starts with adopter and
competitor homepages, keeps unverified source candidates outside the canonical source map,
requires adopter-positioning approval before comparison, and permits an explicitly limited
baseline. An earlier Draft Codex migration suite under `product-requirements/comp-intel/` is
retained as non-binding design history.

The `marketing-brief` package preserves the full PMM Engine template-fill method: the
canonical seven-section template and limits, detailed source precedence and field ownership,
generic Tier 1–3 launch guidance, multi-launch and edit behavior, and a complete fictional
source packet with its finished brief. It is stateless and directly installable; private
examples were used only to calibrate structure and depth and are not part of the export.

## Package contract

Every skill includes:

- `SKILL.md` with public trigger metadata and operating instructions;
- `agents/openai.yaml` with user-facing metadata;
- at least one workflow runbook under `references/`;
- `assets/output-template.md` plus any required config/schema templates;
- `examples/EX-synthetic.md` containing fictional data; and
- local scripts when the workflow has deterministic validation or transformation logic.

The repository validator enforces this contract and checks declared local dependencies.

Plugin governance skills additionally include the canonical standards they enforce,
deterministic initializer/audit/fix scripts, installable schemas and templates, and generic
examples with optional PMM profiles. The document audit is read-only and validates only
opted-in Markdown structure and local paths. CI verifies mirrored standards against `docs/`.

The `plugins/pmm-instinct-review/` `0.2.0` Draft release candidate additionally contains a
Codex plugin manifest, marketplace registration, plugin-relative hooks, a bundled skill, a
standard-library Python runtime, explicit Codex and isolated portable review adapters, an
extractor prompt and schema, complete public state/output templates, governed product and
operator documents, focused tests, and a full fictional lifecycle. Codex capture stays
disabled until explicit consent. Portable mode requires an explicit adopter-owned root,
supports candidate import and review only, and never reads native agent stores or promotes
instructions. The package has no dependency on a private registry or repository. The retired
standalone `skills/pmm-instinct-review/` package is represented by the plugin's explicit
candidate-file import command.

## Generalization rules applied

- Existing safe templates were retained, including the PM Prioritizer framework and format.
- Company positioning, customer and employee references, personal profiles, account IDs,
  service-specific configuration, and real operating examples were not copied.
- Integration-dependent workflows now expose config templates and review-first adapter
  boundaries. No connector is required to use the local workflow.
- Global workflows were converted from private runtime state to explicit local input paths.
- Examples use fictional organizations and people and must never be treated as evidence.
- No private chats, native Codex history, runtime configuration, audits, instincts, or
  normalized transcripts are part of the public export.
- PMM Instinct Review examples use the fictional Northstar Reports scenario and `.invalid`
  domains. No private-to-fictional crosswalk, private route table, Claude desktop capture
  tooling, private hook, mutable adopter state, or real session example is exported.
- Competitive-intelligence adopters must map their own internal names, channels, company
  systems, permissions, existing intelligence data, reviewers, and output destinations. The
  package provides blank templates, source-verification and content-access gates, and a fully
  fictional worked example; no live mapping is included or inferred.

## Verification

Run:

```bash
python3 scripts/governance/validate_skill_pack.py
python3 -m unittest discover -s tests
```

Public CI is defined by SHA-pinned, least-privilege workflows under `.github/workflows/`;
its security properties and required checks are documented in [`CI.md`](CI.md).

The repository is licensed under Apache-2.0. The independent all-ref and tracked-tree
secrets scan is recorded in [`security/SECRET-AUDIT-2026-08-18.md`](security/SECRET-AUDIT-2026-08-18.md).
The per-artifact provenance and redistribution review is recorded in
[`legal/IP-RIGHTS-REVIEW-2026-08-18.md`](legal/IP-RIGHTS-REVIEW-2026-08-18.md). Before
creating a public remote, confirm repository name and ownership. Then apply and verify the
versioned branch, Actions, CodeQL, dependency, secret-scanning, and vulnerability-reporting
baseline in
[`security/GITHUB-SECURITY-CONTROLS.md`](security/GITHUB-SECURITY-CONTROLS.md).

The current starter-kit candidate has a Draft
[IP and privacy review](legal/IP-PRIVACY-REVIEW-COMP-INTEL-FRAMEWORK-2026-09-03.md). The
[sanitized example set has its own Draft review](legal/IP-PRIVACY-REVIEW-COMP-INTEL-SANITIZED-EXAMPLE-2026-09-03.md). The
[earlier requirements-suite review](legal/IP-PRIVACY-REVIEW-COMP-INTEL-PRDS-2026-08-28.md)
remains design history. The public starter kit contains only project-authored generic
structures and fictional examples. Live source corpora, adopter mappings, and private outputs
remain outside the public boundary.

The PMM Instinct Review `0.2.0` candidate has separate Draft
[privacy](legal/IP-PRIVACY-REVIEW-PMM-INSTINCT-REVIEW-0.2.0-2026-09-04.md),
[rights](legal/IP-RIGHTS-REVIEW-PMM-INSTINCT-REVIEW-0.2.0-2026-09-04.md), and
[secret-audit](security/SECRET-AUDIT-PMM-INSTINCT-REVIEW-2026-09-04.md) evidence. Those
documents describe a candidate for review, not an approved release.
