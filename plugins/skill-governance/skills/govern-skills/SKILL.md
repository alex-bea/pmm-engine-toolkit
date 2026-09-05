---
name: govern-skills
description: Audit and safely repair portable skill governance, manage lifecycle records, or harden approval-gated workflows for Claude Code and Codex with shared policy decisions, pre-tool hooks, protected CI, external approval verification, and credential-isolated publishing. Use when a user asks to govern a repository, standardize skills, inspect enforcement gaps, install governance, or design non-bypassable workflow gates.
---

# Govern Skills

## Overview

Establish a repository-owned skill-governance contract and state the enforcement level of
every material rule. Keep audits read-only by default. Treat loaded instructions as guidance,
not as a security boundary.

For an install, setup, configuration, activation, adoption, or rollout request, read
`references/REF-governance-adoption-guide-v1.0.md` and guide the user through its discovery,
readiness, and scoped-approval sequence before any repository write.

## Workflow

1. Resolve the repository, read its instructions, inspect Git status, locate skill roots,
   and discover existing governance, hook, sandbox, CI, approval, and publishing surfaces.
2. Read `references/RUN-govern-skills-workflow-v1.0.md` and follow the selected `audit`,
   `repair`, `lifecycle`, `enforcement`, or adoption mode. Adoption mode is governed by
   `references/REF-governance-adoption-guide-v1.0.md`.
3. Run the deterministic audit before proposing a change:

   ```bash
   python3 scripts/govern_skills.py audit --repo <repository>
   ```

4. Classify every relevant rule as `instruction-only`, `static-validator`,
   `runtime-guard`, `capability-boundary`, or `external-authority`. Never use an
   unqualified claim that a rule is enforced.
5. For initialization or repair, run a dry-run and show the exact paths. Add
   `--with-ci` or `--with-enforcement` only when the user explicitly chooses those layers:

   ```bash
   python3 scripts/govern_skills.py initialize --repo <repository> --dry-run
   python3 scripts/govern_skills.py fix --repo <repository> --dry-run
   ```

6. Wait for explicit approval, repeat the same command with `--apply`, and re-run the audit
   and relevant behavioral tests.

## Enforcement contract

- Claude Code and Codex adapters call the same `scripts/governance_policy.py` decision core.
- Invalid or unavailable policy, run state, digest, verifier, or publisher state denies a
  sensitive action.
- The digest-bound source policy selects the external verifier. It establishes human
  identity, reviewed revision, decision, timing, artifact path, and digest; the caller
  cannot substitute a verifier, name, or link as proof.
- Scheduled workers may collect declared staging evidence but cannot approve, advance a
  human gate, become publish-ready, or publish.
- Publication is available only through `scripts/publisher_guard.py`; the external adapter,
  not the agent or skill package, holds credentials.
- Strong guarantees require hook and policy files outside agent-writable paths, restricted
  alternate shell and network routes, protected CI, and isolated credentials.

Read `references/STD-runtime-enforcement-v1.0.md` before designing or activating runtime
controls. Read the evidence/privacy standard before handling private inputs or external
services.

## Write boundaries

- Never overwrite a differing managed file.
- Never infer lifecycle state, ownership, approval, or publication authority.
- Keep adopter-owned source policies, state, verifier configuration, publisher
  configuration, and credentials outside the installed skill package.
- Direct installation without a verified active hook remains useful for audit and planning
  but must report the runtime guard as inactive or `policy-enabled-hook-unverified`.

## Failure handling

Stop when a managed target conflicts, metadata cannot be parsed, external authority cannot
be verified, or a sensitive action cannot be evaluated. Do not bypass a failed control with
another tool, shell command, network route, or direct file mutation.
