---
doc_type: DOC
normative: false
requires:
  - ../DOC-govern-skills-product-requirements-v1.0.md
  - ../DOC-govern-skills-source-inventory-v1.0.md
  - ../STD-evidence-privacy-v1.0.md
status: Draft
version: "1.0"
owner: alex-bea
consumers:
  - govern-skills maintainers
  - privacy reviewers
  - release reviewers
change_control: Pull request review
---

# Govern Skills Standalone Package IP and Privacy Review (2026-09-15)

## Review scope

This review covers the new public `skills/govern-skills/` copy-pattern package, focused
tests and discovery records, and the compatible `0.3.1` maintenance update to the optional
`skill-governance` plugin's PreToolUse entrypoint.

It does not authorize a plugin installation, hook activation, CI or branch-protection
change, external approval event, publisher, merge, or release.

## Authoring provenance

A private golden implementation was used to identify reusable document roles, workflow
order, lifecycle and approval boundaries, enforcement classifications, and maintenance
insertion points. Private standards, populated registries, operating outputs, review
history, and test fixtures are not distributed.

The standalone package mirrors eight already-public standards byte for byte. Its README,
entrypoint, setup workflow, adoption guide, templates, and tests are newly authored generic
public material. The Acorn Studio example is independently fictional; its organization,
repository, paths, contact, and receipt do not map to a real source.

The optional plugin maintenance retains the existing Claude Code and Codex normalizers and
shared policy. The new entrypoint only selects a harness and delegates; it adds no policy,
approval, publisher, or credential behavior.

## Public changes and sanitization

- No private absolute path, account or channel identifier, customer or deal fact, real
  operating output, approval record, private quotation, or alias map is included.
- Fictional web and contact values use the reserved `.invalid` domain.
- The blank configuration contains no adopter identity, repository path, integration
  locator, or credential value.
- Completed mappings, configuration, mutable state, outputs, and receipts are required to
  remain outside the installed package.
- The documents-only path is primary. Optional validators, registries, hooks, CI,
  capability restrictions, external authority, and publishers remain separate layers.
- The package never represents synthetic evidence or static validation as proof of a live
  installation or non-bypassable enforcement.

## Verification evidence

| Check | Candidate result |
|---|---|
| Review-package approval | Pass: owner recorded against unchanged digest `9f306dbddf0ba65937d6462c406070b24484399e6bf8837e18e5f20a0bc1b3d3`. |
| Setup-contract validator | Pass: one `setup-workflow` RUN, required mappings, safety terms, fixture, and receipt states validated. |
| Isolated compatible-agent fixture | Pass: a copied package created exactly the three expected temporary files; the installed package and production paths remained unchanged. |
| Focused standalone and plugin suites | Pass: 27 tests. |
| Complete public unit suite | Pass: 285 tests. |
| Public skill-pack validator | Pass: 26 standalone skills and two plugins. |
| Governed-document audit | Pass: 83 governed Markdown documents, no findings. |
| Skill Creator validation | Pass for the source and isolated copied package. |
| GitHub Actions validator | Pass: three SHA-pinned, least-privilege workflows. |
| Read-only GitHub security plan | Pass without external mutation. |
| Standard-mirror and package-link checks | Pass in the focused suite. |
| Private denylist and public-candidate scan | Pass: no finding across the exact approved candidate paths. |
| IP inventory | Pass: 486 artifacts; repeat generation produced SHA-256 `f3e201c1fc959c5954c3d9913325c289dc8fc47cf29d36a1a440de192b263215`. |
| Approved-manifest comparison | Pass: 38 changed paths exactly match the approved manifest. |
| Hosted pull-request checks | Pending until the candidate is pushed. |
| Project-owner exact-revision review | Pending. |

The compatible-agent fixture used only the bundled fictional mapping and a temporary local
destination. It did not install a plugin, activate a hook, alter CI, create an approval,
send a message, schedule work, publish, or touch production state.

## Residual risk

A model-readable workflow cannot guarantee that every model will follow it. Automated
scanning cannot prove prose is non-identifying. Repository-local hooks can be disabled or
bypassed when policy and capabilities remain agent-writable. Strong enforcement requires
administrator protection, restricted alternate paths, independently verified authority,
and isolated credentials.

## Publication conditions

- Keep this document Draft until the exact pull-request revision is reviewed.
- Keep private source evidence and the run-specific denylist outside the public repository.
- Require project-owner review before merge, tagging, marketplace action, or release.
- Re-run affected verification after any material package, policy, fixture, or public-
  boundary change.

This is a repository-content review, not legal advice.
