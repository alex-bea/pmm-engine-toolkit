---
doc_type: DOC
normative: false
requires:
  - ../DOC-govern-skills-product-requirements-v1.0.md
  - ../legal/IP-PRIVACY-REVIEW-GOVERN-SKILLS-2026-09-15.md
status: Draft
version: "1.0"
owner: toolkit-maintainers
consumers:
  - governance adopters
  - public toolkit maintainers
change_control: Pull request review
---

# Govern Skills standalone `1.0` — draft release notes

Status: locally verified implementation candidate. These notes describe an unmerged,
unreleased change and do not authorize installation into production workflows, merge,
tagging, marketplace action, or a GitHub release.

## New standalone copy pattern

- Added a self-contained `skills/govern-skills/` package that can be read directly by
  Claude Code, Codex, or another capable local coding agent.
- Added a copy-paste prompt that starts with read-only repository inspection, adapts to
  existing conventions, presents an exact file plan, and does not require a plugin.
- Explained the separate roles of `SKILL`, `RUN`, `STD`, `REF`, templates, examples,
  scripts, shared policy decisions, harness adapters, and capability boundaries.
- Added one setup-and-execution RUN with source and destination mapping, adopter-owned
  configuration, a safe fictional fixture, setup-receipt staleness, and normal audit,
  repair, create/update, lifecycle, and enforcement modes.
- Added eight package-local public standards, three blank templates, one output template,
  and a complete independently fictional Acorn Studio mapping and receipt.

## Optional plugin maintenance

- Updated the existing `skill-governance` plugin to `0.3.1` Draft.
- Added one `pretooluse.py` entrypoint with explicit Claude Code or Codex harness selection.
- Retained both existing adapters and the one shared policy decision, preserving direct
  callers and policy outcomes.
- Kept the plugin optional and runtime enforcement inactive unless separately configured
  and activated.

## Compatibility and limits

The standalone package does not replace the plugin package, and the plugin is not a runtime
dependency of the standalone workflow. Existing public standards remain canonical and are
mirrored inside the standalone package for direct-copy closure.

Documents-only adoption is an `instruction-only` layer. It can be ready for that named
scope without a registry, CI, hook, capability boundary, external authority, or publisher,
but it must not be described as generally enforced.

## Verification status

| Check | Candidate result |
|---|---|
| Setup contract and isolated fictional fixture | Pass; exactly three expected temporary files were created. |
| Focused standalone and plugin tests | Pass: 27 tests. |
| Complete repository unit suite | Pass: 285 tests. |
| Skill-pack and Skill Creator validation | Pass: 26 standalone skills, two plugins, and a valid copied package. |
| Governed-document audit | Pass: 83 governed Markdown documents, no findings. |
| GitHub Actions validator and read-only security plan | Pass; no external mutation. |
| Public-candidate privacy scan | Pass with the run-private denylist. |
| IP inventory | Pass: 486 artifacts and repeatable SHA-256. |
| Exact approved-manifest comparison | Pass: 38 of 38 paths, no extra path. |
| Hosted pull-request checks | Pending. |
| Project-owner exact-revision review | Pending. |

An unavailable, skipped, stale, or failing required check blocks release readiness. This
Draft does not authorize merge or release.
