# Codex Skill Governance Plugin

The `skill-governance` plugin installs three self-contained Codex skills:

- `govern-skills` initializes and audits skill structure, metadata, registry entries,
  lifecycle, dependency closure, evidence quality, and approval gates. It can also install
  an inactive cross-harness control plane for separately approved activation.
- `govern-work-tracker` initializes and audits a lightweight roadmap, epic, and task
  tracker under `state/work/`.
- `govern-documents` audits opted-in Markdown document metadata, declared dependencies,
  and local links without changing the repository.

Audits are read-only and advisory by default. Initializers and fixes show a dry-run plan
and require explicit approval before they use `--apply`. Blocking CI and runtime governance
are separate opt-ins.

## Install as a Codex plugin

Add this GitHub repository as a marketplace and install the plugin:

```bash
codex plugin marketplace add alex-bea/pmm-engine-toolkit --ref main
codex plugin add skill-governance@pmm-engine-toolkit
```

Start a new Codex task after installation so the new skills are available. To refresh a Git
marketplace after a release, run `codex plugin marketplace upgrade pmm-engine-toolkit` and
reinstall the plugin.

## Install individual skills from GitHub

Use Codex's built-in Skill Installer when only one workflow is needed:

```text
Use $skill-installer to install:
https://github.com/alex-bea/pmm-engine-toolkit/tree/main/plugins/skill-governance/skills/govern-skills
```

```text
Use $skill-installer to install:
https://github.com/alex-bea/pmm-engine-toolkit/tree/main/plugins/skill-governance/skills/govern-work-tracker
```

```text
Use $skill-installer to install:
https://github.com/alex-bea/pmm-engine-toolkit/tree/main/plugins/skill-governance/skills/govern-documents
```

Each directory carries all of the references, scripts, templates, schemas, and examples
needed for that skill's workflow.

## Adopt governance in a repository

Ask Codex to use `$govern-skills` to audit the repository. The skill will run a read-only
audit before proposing initialization. After reviewing and approving the dry-run, the
initializer creates:

```text
.agents/governance/
├── bin/
├── manifest.yaml
├── schemas/
├── skill-registry.yaml
├── standards/
└── templates/
```

The manifest records the governance-pack version and SHA-256 hash of each managed file.
Audits report local modifications but never silently replace them.

To add the tracker, ask Codex to use `$govern-work-tracker` to initialize `state/work/`.
Roadmap, epic, and task templates are installed without inventing actual project work.

For document governance, adopt the global baseline and opt in only the documents that need
it. `$govern-documents` then audits metadata and local paths without inferring or rewriting
anything. See [Codex Document Governance](CODEX-DOCUMENT-GOVERNANCE.md) for the adoption
sequence and the limits of automation.

## Command contract

The skill and work-tracker scripts support the same review-first pattern:

```bash
python3 <skill>/scripts/govern_skills.py audit --repo .
python3 <skill>/scripts/govern_skills.py initialize --repo . --dry-run
python3 <skill>/scripts/govern_skills.py initialize --repo . --with-enforcement --dry-run
python3 <skill>/scripts/govern_skills.py fix --repo . --dry-run

python3 <skill>/scripts/govern_work_tracker.py audit --repo .
python3 <skill>/scripts/govern_work_tracker.py initialize --repo . --dry-run
python3 <skill>/scripts/govern_work_tracker.py fix --repo . --dry-run
```

The document audit is intentionally audit-only:

```bash
python3 <skill>/scripts/govern_documents.py audit --repo .
python3 <skill>/scripts/govern_documents.py audit --repo . --format json
python3 <skill>/scripts/govern_documents.py audit --repo . --strict
```

Replace `--dry-run` with `--apply` only after reviewing the proposed paths. Use
`audit --format json` for machine-readable findings. Use `audit --strict` to return nonzero
when any finding exists. Document checks are not installed into CI by this plugin release;
adopters can use the strict command when they choose to add a future gate.

## Optional blocking CI

The skill-governance initializer accepts `--with-ci`. This installs
`.github/workflows/skill-governance.yml`, which runs the repository-owned audit scripts in
strict mode. Omit this flag to keep checks advisory and local.

## Optional runtime governance

`--with-enforcement` installs a shared policy decision, run-control command, Claude Code and
Codex adapters, approval-verifier contract, and publisher guard under
`.agents/governance/bin/`. It also creates `.agents/governance/enforcement.yaml` with
`enabled: false`. The installer never edits an existing policy file.

Runtime activation is an administrator operation, not an agent convenience flag:

1. Review the installed hashes and templates.
2. Install the Claude Code PreToolUse snippet from
   `.agents/governance/templates/claude-settings.json` when Claude is in scope. The Codex
   plugin exposes its plugin-relative PreToolUse hook automatically, but Codex skips a
   non-managed hook until the user reviews and trusts its exact hash with `/hooks`; a direct
   skill install does not expose a plugin hook.
3. Move or mount enabled policy and hook configuration outside agent-writable paths.
4. Restrict alternate shell commands, direct network routes, ungoverned connector tools,
   direct run-state writes, and publisher credentials.
5. Configure an external approval verifier. Its executable and configuration must be
   absolute and outside the repository. The command is a single executable; requests arrive
   on standard input rather than through repository-controlled command arguments.
6. Configure an approved external publisher only when publication is required. The
   publisher executable, not the agent or repository, holds credentials.
7. Run the negative test matrix before enabling the policy.

The two harness adapters normalize their tool payloads and call the same
`governance_policy.py`; they do not carry separate rules. Only exact direct invocations of
the packaged control scripts receive controlled-command status. Compound shell commands,
pipelines, redirections, and wrapper-name smuggling remain untrusted.

These activation and payload rules follow the official
[Codex Hooks documentation](https://learn.chatgpt.com/docs/hooks). For centrally enforced
Codex deployments, install the hook through managed configuration, pin hooks on, and exclude
unmanaged hook sources according to that documentation.

The Claude snippet follows the official
[Claude Code Hooks reference](https://code.claude.com/docs/en/hooks), resolves the installed
script through `$CLAUDE_PROJECT_DIR`, and blocks with exit code 2. For organization-wide
Claude enforcement, distribute the same hook and permission restrictions through managed
policy settings so repository or user settings cannot disable them.

## What “enforced” means

The audit reports five layers independently:

- `instruction-only` — a model-readable rule;
- `static-validator` — a deterministic local or CI check;
- `runtime-guard` — a pre-tool policy decision;
- `capability-boundary` — filesystem, network, tool, or credential access is unavailable;
- `external-authority` — a protected service verifies human approval or performs
  publication.

Do not treat instructions or a hook alone as a non-bypassable boundary. A machine owner can
disable a hook or widen capabilities. Strong enforcement requires protected configuration,
restricted bypass paths, independently verified digest-bound approval, protected CI, and
publisher credentials outside the agent's capability set.

The repository audit cannot observe whether an external harness actually loaded a hook. An
enabled policy therefore reports `policy-enabled-hook-unverified` until hook activation is
established in the administrator-controlled harness.

## Approval-gated runs

`governance_control.py` maintains schema-version-2 run state under `state/runs/`. Approval is
valid only when the verifier selected by the digest-bound source policy confirms the
authorized person, approved decision, review time, reviewed revision, artifact path, and
SHA-256 digest. The caller cannot choose a different verifier. The publisher guard
re-validates all of those fields immediately before use and requires the publisher response
to echo the exact run, operation, artifact, digest, and approval reference.

Scheduled runs may enter collection, register declared staging evidence, and stop at
`evidence_review`. They cannot create approval, advance a human-review gate, enter
`publish_ready`, or publish. Missing or invalid verifier and publisher configuration fails
closed for the actions that depend on it; read-only audit remains available.

## Governance sources

The repository copies its canonical standards into the installable skill packages for
offline and direct-install use. Repository tests enforce byte-for-byte parity between those
copies. PMM-specific examples remain under each skill's `assets/examples/pmm-engine/`
directory and do not alter the generic core.
