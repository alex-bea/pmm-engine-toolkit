---
doc_type: RUN
normative: true
requires:
  - STD-ai-skill-governance-prd-v1.0.md
  - STD-approval-gates-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-runtime-enforcement-v1.0.md
  - STD-skill-dependencies-v1.0.md
  - STD-skill-primitives-v1.0.md
  - STD-skill-structure-v1.0.md
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Claude Code users
  - Codex users
  - skill maintainers
change_control: Project owner approval
---

# Govern Skills Workflow

## 1. Select a mode

- **Audit:** inspect and report without writing.
- **Repair:** propose the smallest mechanical correction, obtain approval, apply it, and
  re-run the responsible checks.
- **Lifecycle:** update skill identity, ownership, version, status, replacement, or path
  through the canonical registry.
- **Enforcement:** turn a binding rule into a shared policy decision, harness guard, CI gate,
  capability restriction, or independently verified authority.

## 2. Preflight

1. Resolve the repository root and read every applicable instruction file.
2. Inspect Git status and preserve unrelated work.
3. Locate the skill roots, registry, managed-file manifest, schemas, CI, hooks, and external
   adapter configuration.
4. Run `scripts/govern_skills.py audit --repo <repository>`.
5. State which controls are currently active and which are only documented.

Stop before writing if the repository, target skill, owner decision, or external authority
cannot be resolved.

## 3. Audit mode

Classify findings as blocking validator errors, advisory drift, semantic owner decisions,
or written rules without complete technical enforcement. A passing audit does not prove
factual quality, human approval, runtime compliance, or publication authority. Use
`audit --strict` only when a blocking local or CI result is intended.

## 4. Repair and lifecycle modes

1. Reproduce the finding with its deterministic validator.
2. Identify the canonical standard and registry field that own the behavior.
3. Run `fix --dry-run`, optionally selecting one finding.
4. Show exact paths and distinguish creates, updates, unchanged files, conflicts, and
   semantic decisions.
5. Obtain explicit approval for the displayed change.
6. Apply only that change and re-run focused and cross-file checks.

New registry entries begin as `draft`, version `0.1.0`, owner `unassigned`. Do not activate,
deprecate, archive, choose an owner, or invent a replacement without the owner's decision.

## 5. Enforcement mode

1. Read `STD-runtime-enforcement-v1.0.md`.
2. Inventory every tool and alternate path that can cause the governed side effect.
3. Define one normalized decision request and stable reason codes.
4. Put policy in `scripts/governance_policy.py`; keep Claude and Codex adapters thin.
5. Deny direct mutation of governed run state and protected policy paths.
6. Require external verification for human approval and re-verify immediately before
   publication.
7. Reject scheduled approval, human-gate transition, publish-ready transition, and
   publication.
8. Keep credentials in the external publisher implementation, never in the repository,
   hook payload, state file, or model context.
9. Add positive and negative tests. Every negative side-effect test asserts that the effect
   did not occur.

Use `initialize --with-enforcement --dry-run` to display the repository-local installation.
Activation still requires an administrator to protect the policy, install the applicable
harness hook, restrict bypass capabilities, and configure external adapters.

## 6. Verification

Run the relevant subset of:

- advisory and strict skill audits;
- schema and governed-document validation;
- registry and managed-manifest consistency;
- shared policy decision tests;
- Claude and Codex payload fixtures;
- scheduled-run, stale-digest, forged-approval, verifier-outage, direct-publisher, network,
  alternate-shell, and direct-file-mutation negative tests;
- protected CI checks from a clean checkout.

Report checks not run as `not run`. Never reinterpret a validator defect as a change to the
written standard.

## 7. Approval and stop conditions

Audit reports and dry-runs may proceed without write approval. Repository writes, lifecycle
decisions, managed hook changes, CI requirements, external adapter changes, and publisher
boundaries require explicit scoped approval. Approval binds the exact artifact digest or
diff. Material change invalidates it.

Stop and deny when policy evaluation fails, approval cannot be independently verified, the
artifact digest is stale, a scheduled worker requests authority, the publisher is missing or
unapproved, a managed target differs, or a requested action would exceed the displayed
boundary.
