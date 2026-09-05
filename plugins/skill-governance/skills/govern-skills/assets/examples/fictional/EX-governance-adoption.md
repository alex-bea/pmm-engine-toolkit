# Fictional cross-harness governance adoption

Everything in this example is fictional and non-operational. Cedar Harbor Software uses
reserved `.invalid` domains, a test-only approval response, and a disabled publisher
adapter to exercise the complete public template set.

## 1. Governed skill

```yaml
---
name: release-note
description: Draft a sourced release note and stop for verified review before publication.
---
```

```yaml
interface:
  display_name: "Release Note"
  short_description: "Draft a governed software release note"
  default_prompt: "Use $release-note to draft an evidence-bound release note."
```

The registry stores lifecycle metadata outside `SKILL.md`:

```json
{
  "version": "1.0",
  "skills": [
    {
      "name": "release-note",
      "folder": ".agents/skills/release-note",
      "version": "1.0.0",
      "owner": "release-maintainer",
      "status": "active",
      "replacement": null
    }
  ]
}
```

## 2. Repository instructions

The fictional repository adopts the `AGENTS.md` template. Its key instruction says that a
schema-version-2 run must validate before every stage and that only the external verifier
can establish approval. The team separately protects the policy and adapter configuration
with managed filesystem permissions. The instruction improves agent behavior; the managed
configuration supplies the security boundary.

## 3. Source policy

```json
{
  "schema_version": 1,
  "policy_id": "cedar-release-policy",
  "status": "active",
  "approval_authority": {
    "authority_id": "cedar-review-service",
    "verifier_config": "/etc/governance/cedar-approval-verifier.json"
  },
  "allowed_sources": [
    {
      "id": "fictional-release-evidence",
      "adapter": "local-read-only-files",
      "description": "Fictional evidence committed under examples/evidence/."
    }
  ]
}
```

The configured verifier is an administrator-managed executable outside the repository. A
test response may name `reviewer-7`, revision `rev-42`, artifact digest
`aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`, and
`https://code.example.invalid/reviews/42`. These values are invented and confer no real
authority.

## 4. Runtime enforcement policy

The initializer writes a disabled policy first. An administrator reviews it, moves or mounts
the policy read-only, and then enables it:

```json
{
  "schema_version": 1,
  "enabled": true,
  "mode": "enforce",
  "execution_mode": "interactive",
  "run_state_globs": ["state/runs/*.yaml", "state/runs/**/*.yaml"],
  "protected_path_globs": [
    ".agents/governance/**",
    ".claude/settings*.json",
    ".codex/**"
  ],
  "publisher_tool_globs": ["mcp__*publish*", "*publisher*", "*send_message*"]
}
```

With this file writable by the agent, the control is only a runtime guard. With the policy,
hook, network policy, and credentials outside agent control, the effective boundary also
includes capability restrictions and external authority.

## 5. Claude Code adapter

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit|MultiEdit|NotebookEdit|mcp__.*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.agents/governance/bin/claude_pretooluse.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

## 6. Codex adapter

The installed plugin registers `hooks/hooks.json`. The hook is repository-scoped: if the
current repository has no enabled enforcement policy, it returns an inactive-layer result
and does not claim runtime protection. Both adapters normalize their payloads and call the
same `governance_policy.py` decision function.

## 7. Workflow run

After initialization and collection, the fictional run has this shape:

```json
{
  "schema_version": 2,
  "workflow_id": "release-note",
  "run_id": "cedar-release-001",
  "stage": "evidence_review",
  "runtime": {"execution_mode": "interactive"},
  "source_policy": {
    "path": ".agents/governance/source-policy.yaml",
    "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
  },
  "artifacts": {
    "evidence": {
      "path": "staging/cedar-release-evidence.md",
      "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "disposition": "staging"
    }
  },
  "approvals": {},
  "transition_history": [
    {"from": "initialized", "to": "collection"},
    {"from": "collection", "to": "evidence_review"}
  ]
}
```

The example hashes are structurally valid placeholders. A real run always computes them
from the current files.

## 8. CI

The repository opts into `skill-governance-ci.yml`. CI audits governed skill structure,
validates run state, runs the negative policy matrix, and verifies that canonical standards
match their installable mirrors. CI has read-only repository permission and receives no
publisher credential.

## 9. Publisher boundary

The committed template remains disabled:

```json
{
  "schema_version": 1,
  "adapter_id": "cedar-release-publisher",
  "enabled": false,
  "approved": false,
  "command": ["/usr/local/libexec/cedar-governed-publisher"],
  "allowed_operations": ["publish-approved-artifact"],
  "timeout_seconds": 30
}
```

An administrator stores the enabled configuration outside the repository. Only the
external executable receives publication credentials.

## 10. Stale-digest denial

The fictional reviewer approves digest `aaaaaaaa…` at revision `rev-42`. A later edit
changes the staged artifact. The next validation reports the artifact as stale;
`can-publish` denies the run, and the publisher executable is never invoked. The adapters
record only decision metadata such as `GOV_PUBLISHER_GUARD_REQUIRED`; they do not retain the
prompt, content body, full command, or credential material.

## 11. Fictional setup-readiness report

This test-only report shows what the guiding agent would return before Cedar Harbor's
administrator completes activation. It does not describe a real repository or confer any
authority.

| Layer or blocker | Current state | Evidence | Gap | Proposed action | Approval authority | Verification |
|---|---|---|---|---|---|---|
| Registry compatibility | `ready` | The first fictional audit found an older schema; the approved migration now validates. | None after the recorded migration. | Preserve the migrated schema and re-audit after upgrades. | Cedar Harbor repository owner | Current audit reports no schema conflict. |
| `instruction-only` | `ready` | Fictional `AGENTS.md` is present and named in both harness setup records. | None for the named repository scope. | Preserve the instruction and confirm loading after upgrades. | Cedar Harbor repository owner | Both test harnesses report the same controlling instruction. |
| `static-validator` | `configured-inactive` | The CI workflow is installed but not a required check. | A merge can bypass it. | Make the governance check required. | Cedar Harbor repository administrator | A synthetic noncompliant change cannot merge. |
| `runtime-guard` | `configured-inactive` | The shared policy and both adapters are installed with enforcement disabled. | Hook trust and active fail-closed behavior are unverified. | Administrator enables managed hooks after resolving the registry blocker. | Cedar Harbor repository administrator | Both adapters deny the same stale-digest request before mutation. |
| `capability-boundary` | `missing` | No fictional managed filesystem or network policy is evidenced. | The agent could alter policy or reach an alternate publisher. | Protect policy and executables, restrict alternate tools and network routes, and isolate credentials. | Cedar Harbor platform administrator | Negative tests prove direct file, shell, connector, and network bypasses cause no side effect. |
| `external-authority` | `missing` | Only the reserved `code.example.invalid` test response exists. | No protected verifier establishes a real approval identity or decision. | Configure and health-check an administrator-controlled verifier. | Cedar Harbor security administrator | Forged, stale, wrong-reviewer, and outage cases remain pending. |
| Publisher | `not-applicable` | Publication is excluded from this fictional adoption scope. | None while publication remains excluded. | Keep the publisher disabled and credentials absent. | Cedar Harbor repository owner | Direct and alternate publication tests produce no message or external side effect. |

Overall status: `installed-inactive`. The compatibility blocker is resolved and repository
assets are installed, but the static gate, runtime guard, capability boundary, and external
authority are not yet verified as ready.
