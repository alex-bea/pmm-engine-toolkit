---
doc_type: REF
normative: true
requires:
  - RUN-govern-skills-workflow-v1.0.md
  - STD-ai-skill-governance-prd-v1.0.md
  - STD-governance-document-metadata-v1.0.md
  - STD-runtime-enforcement-v1.0.md
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Claude Code users
  - Codex users
  - repository administrators
  - new adopters
change_control: Project owner approval
---

# Governance Adoption Guide

## 0. Purpose

Guide a new adopter through governance setup in conversation. This file is the setup
experience: it tells Claude Code or Codex what to inspect, what gaps to explain, which exact
changes to propose, where approval is required, and how to prove the selected enforcement
layers are active. It is not an interactive installer and does not replace deterministic
audit, initialization, policy, or hook code.

The guide is fail-closed for claims. An agent may report only the controls it can verify. It
must never convert an installation request, chat response, caller-supplied identity, or
syntactically valid approval reference into proof of external authority.

## 1. Enter Adoption Mode

Use this guide when the user asks to install, set up, configure, activate, adopt, or roll out
skill governance.

Before asking setup questions:

1. Resolve the repository root and read every applicable instruction file.
2. Inspect Git status and preserve unrelated work.
3. Detect the available skill roots, canonical registry, governed documents, existing CI,
   Claude Code settings, Codex hooks or plugins, workflow state, publisher paths, and
   approval references.
4. Run the repository-owned read-only governance audit when available.
5. Identify schema or convention conflicts between the adopter repository and the packaged
   defaults. Do not propose initialization until these compatibility findings are explicit.
6. Infer which harnesses are present from evidence. Ask the user only about material scope
   or authority decisions that inspection cannot resolve.

Do not write, initialize, enable, trust, or publish during this phase.

## 2. Explain the Enforcement Model

Tell the adopter that governance is evaluated as five independent layers:

| Layer | Ready only when |
|---|---|
| `instruction-only` | The controlling documents are discoverable and loaded by the relevant harness. |
| `static-validator` | Deterministic checks cover the selected rules and are required before merge or release. |
| `runtime-guard` | The harness has loaded the shared pre-action policy adapter and fail-closed behavior is verified. |
| `capability-boundary` | The agent cannot rewrite policy, bypass hooks through another tool or network route, or access publisher credentials. |
| `external-authority` | A protected service independently verifies approval or performs the governed publication. |

Do not imply that selecting one layer activates another. A repository-local hook is a
runtime guard, not a capability boundary. A passing validator is not human approval.

## 3. Produce the Setup Readiness Report

Present one row for every relevant layer and every compatibility blocker:

| Layer or blocker | Current state | Evidence | Gap | Proposed action | Approval authority | Verification |
|---|---|---|---|---|---|---|

Use only these current-state values:

- `ready` — directly verified for the named scope;
- `configured-inactive` — installed but deliberately disabled or not trusted;
- `missing` — no qualifying implementation or configuration exists;
- `blocked` — a conflict, failed check, or unresolved authority prevents progress;
- `not-applicable` — the governed side effect is explicitly outside the approved scope.

The report must cover, when applicable:

- canonical registry and skill-manifest compatibility;
- governed-document metadata and dependency checks;
- exact Claude Code and Codex hook sources and their trust state;
- policy and executable write protection;
- direct file-write, shell, network, MCP, and alternate publisher paths;
- source-policy and workflow-run schemas;
- approval system of record and authorized identities;
- external verifier location and health;
- publisher adapter, credentials, and audit receipts;
- CI workflow installation and required-check or branch-protection state; and
- the negative tests needed to prove denied side effects do not occur.

Label assumptions and unobservable external state. Do not collapse an unknown into `ready`.

## 4. Resolve Only Material Decisions

After presenting discovered facts, ask the adopter to decide only what cannot be derived:

1. Which repositories and workflows are in scope?
2. Which harnesses must be covered: Claude Code, Codex, or both?
3. Which rules must block locally, in CI, at runtime, or through an external capability
   boundary?
4. What protected system is the approval source of truth, and who is authorized there?
5. Is external publication in scope? If not, record the publisher layer as
   `not-applicable` and keep it disabled.
6. Who can perform administrator-only hook, filesystem, network, credential, and branch
   protection changes?

Do not choose identities, lifecycle states, publisher destinations, or bypass permissions
for the user. One answer does not authorize a broader layer or a different target.

## 5. Prepare the Exact Installation Plan

Run the deterministic initializer in dry-run mode with only the layers the adopter selected.
When supported, use the equivalent of:

```bash
python3 <skill>/scripts/govern_skills.py initialize --repo <repository> --dry-run
python3 <skill>/scripts/govern_skills.py initialize --repo <repository> --with-ci --with-enforcement --dry-run
```

Present:

- every file to add, update, leave unchanged, or treat as a conflict;
- the exact commands that would perform the write;
- the repository and branch or checkout affected;
- compatibility decisions and files intentionally excluded;
- controls that will remain inactive after installation;
- the applicable approval system of record; and
- an artifact or diff digest when the governing process requires one.

Stop before `--apply`. Obtain approval for the exact plan through the repository's
configured change-control authority. If approval cannot be verified as required, keep the
plan pending. Never overwrite a differing managed file.

## 6. Apply Repository-Local Installation

After valid scoped approval:

1. Re-run the same deterministic command with `--apply`.
2. Confirm that applied paths are a subset of the approved plan.
3. Re-run the audit and static validators.
4. Report conflicts and remaining inactive layers.
5. Do not enable external publication or claim runtime activation.

Repository-local installation normally ends as `configured-inactive` for runtime controls.
That is a successful installation state, not enforcement readiness.

## 7. Guide Administrator Activation

For each selected harness, show the administrator the exact evidence and action required:

1. Install or enable the Claude Code and Codex pre-action adapters from an
   administrator-controlled source.
2. Establish any required hook hash trust or managed configuration.
3. Move or mount policy, hook, verifier, publisher, audit, and credential surfaces outside
   agent-writable paths.
4. Restrict alternate shell commands, direct state mutation, unmanaged network routes,
   ungoverned connector tools, and second publisher paths.
5. Configure the external approval verifier from the digest-bound source policy.
6. Configure a publisher only when publication is in scope; keep its credential unavailable
   to the ordinary agent.
7. Make relevant CI checks and branch protections required.

Each administrator change requires its own configured authority when it was not part of the
approved repository plan. The guiding agent may provide exact snippets and verification
commands, but it may not use the user's credentials to create the human approval event or
assert that an external harness loaded a hook without evidence.

## 8. Verify Before Declaring Readiness

Run the positive and negative checks relevant to the approved scope. At minimum, verify:

- Claude Code and Codex normalize the same sensitive request to the same decision;
- malformed state, missing artifacts, and stale digests deny before mutation;
- direct file edits and alternate shell commands cannot bypass protected transitions;
- scheduled execution cannot approve, cross a human gate, become publish-ready, or publish;
- forged references, wrong reviewers, wrong revisions, wrong digests, and verifier outages
  leave approval pending;
- direct publishers, unapproved adapters, missing credentials, and alternate network routes
  do not cause an external side effect; and
- required CI and branch protection reject an unapproved governed change.

For every negative test, verify that the sentinel file, mock operation, merge, message, or
publication did not occur. Record unavailable checks as `not run`; never describe them as
passing.

## 9. Report the Final State

End with the updated setup-readiness table and exactly one overall status:

- `ready` — every selected layer is directly verified for the named scope;
- `installed-inactive` — repository assets are installed, but one or more activation layers
  remain disabled or unverified; or
- `blocked` — a conflict, failed check, missing authority, or absent external boundary
  prevents safe activation.

State the precise scope of `ready`. A layer may be `not-applicable` only when its side effect
was explicitly excluded. List the next human or administrator action for every non-ready
row. Do not use an unqualified statement that governance is enforced.

## 10. Stop Conditions

Stop and keep the affected layer inactive when:

- a canonical registry or manifest conflicts with the packaged defaults;
- the proposed paths or digest differ from the approved plan;
- hook trust or administrator control cannot be verified;
- policy, verifier, publisher, state, audit, or credential files remain agent-writable when
  a strong boundary is required;
- an alternate tool or network path can still cause the governed side effect;
- approval authority, identity, revision, artifact path, digest, or timing is unverified;
- a required negative test fails or was not run; or
- the publisher is missing, unapproved, or holds no valid credential.
