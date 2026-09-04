---
doc_type: STD
normative: true
requires:
  - STD-approval-gates-v1.0.md
  - STD-skill-dependencies-v1.0.md
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Claude Code users
  - Codex users
  - governance maintainers
change_control: Project owner approval
---

# Runtime Enforcement Standard

## Enforcement classes

Every material governance rule has one explicit current class:

| Class | Meaning |
|---|---|
| `instruction-only` | The model can read the rule, but no independent check or block exists. |
| `static-validator` | Deterministic code detects violations before merge or release. |
| `runtime-guard` | A pre-action hook or policy decision can deny an attempted operation. |
| `capability-boundary` | Filesystem, network, credential, or tool policy makes the prohibited operation unavailable. |
| `external-authority` | A protected service establishes identity, review, approval, or publication independently of the agent. |

Do not describe a repository as governed without naming the active classes. A hook installed
in an agent-writable location is a runtime guard, not a complete capability boundary.

## Shared policy decision

Claude Code and Codex adapters must normalize their payloads and call the same deterministic
policy function. A decision request contains only the fields required to decide: harness,
execution mode, tool, operation, normalized target paths, current stage, artifact digest, and
verified authority status. The result is `allow`, `deny`, or `require-human` with a stable
reason code and explanation.

Policy logic belongs in `governance_policy.py`. Harness adapters translate payloads and exit
according to their supported hook contract; they do not reimplement policy. Missing,
malformed, stale, ambiguous, or unverifiable input denies a sensitive action. Read-only audit
may remain available when optional adapters are absent.

Only an exact, direct invocation of the packaged control or publisher script is treated as a
controlled command. A compound shell command, redirection, pipeline, command substitution,
or wrapper name embedded in another command is untrusted and must not inherit that status.

## Protected surfaces

For a strong boundary, install or mount these surfaces outside agent-writable paths:

- enabled policy and hook configuration;
- policy and control executables;
- approval-verifier configuration;
- publisher configuration and executable;
- protected approval or publication audit records; and
- credentials.

Also restrict alternate shell commands, direct network access, ungoverned connector tools,
direct run-state writes, and any second publisher path. Repository instructions and hooks
cannot compensate for a credential already available to the agent.

## Run-state contract

A governed run records a schema version, workflow and run identifiers, execution mode,
ordered stage, source-policy digest, staged artifact paths and SHA-256 digests, verified
approval records, and transition history. Direct edits to run state are denied when the
runtime guard is active. Controlled transitions validate the current files before writing the
next state.

Changing a staged artifact invalidates its approval. A syntactically valid link, caller name,
chat statement, or repository field is evidence to verify, not proof of human authority.

## Approval authority

The verifier is a single absolute external executable configured outside the repository. The
control plane sends its request on standard input, so repository-controlled script arguments
cannot be inserted into the trusted command. The verifier confirms all of the following in
one response:

- the configured authority identity;
- an authorized human approver;
- an approved decision and approval time;
- the exact approval reference and reviewed revision; and
- the exact artifact path and digest.

The control plane compares every returned value with the requested gate and current artifact.
Verifier failure, timeout, malformed output, unauthorized identity, wrong revision, or wrong
digest leaves the gate pending.

The verifier configuration is derived from the digest-bound source policy. A caller cannot
substitute a different verifier, and the verified authority identifier must match that policy.

## Scheduled execution

A scheduled worker may initialize a scheduled run, enter collection, register only declared
staging evidence during collection, and stop at `evidence_review`. It cannot create approval,
advance a human-review gate, enter `publish_ready`, or publish. Well-formed state never
overrides this restriction.

## Publication

Only the publisher guard may invoke an approved external publisher. Immediately before the
operation it validates the run, confirms interactive mode and `publish_ready`, recomputes
artifact digests, and re-verifies external approval. The configured command names one absolute
external executable and receives the request on standard input. That publisher holds
the publication credential and returns a result bound to the run, operation, artifact, digest,
and approval reference. The repository may retain only a minimal receipt without credential
material.

Direct publisher tools, unapproved adapters, missing credentials, verifier failure, or an
alternate network route deny. Protected network and tool policy must make those bypass paths
unavailable when a non-bypassable guarantee is required.

## Minimal logging

Runtime decisions may record timestamp, result, stable reason code, harness, action class,
run identifier, and non-sensitive receipt identifiers. Do not store prompts, content bodies,
full tool arguments, cookies, authorization headers, credentials, or private artifact
content.

## Activation and health reporting

Installation creates an inactive policy. Activation is a separate administrator action after
hook trust, protected paths, external adapters, network restrictions, and credentials have
been reviewed. Audits report each layer independently. A missing hook or external adapter is
reported as inactive and denies only actions that require it; it must never be represented as
active enforcement.

A repository audit can observe that the policy is enabled but cannot prove that an external
harness loaded the hook. It therefore reports `policy-enabled-hook-unverified` until that
activation is established outside the repository.

## Required negative tests

Test direct file mutation, alternate shell commands, scheduled approval, scheduled transition,
stale digests, forged approval references, wrong reviewer or revision, verifier outage,
direct publisher calls, unapproved adapters, network bypass, malformed hook payloads, and
repeated installation. Each negative side-effect test proves that the sentinel file, mock
service, or publisher call did not occur.
