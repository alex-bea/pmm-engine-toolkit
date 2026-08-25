# Codex Skill Governance Plugin

The `skill-governance` plugin installs three self-contained Codex skills:

- `govern-skills` initializes and audits skill structure, metadata, registry entries,
  lifecycle, dependency closure, evidence quality, and approval gates.
- `govern-work-tracker` initializes and audits a lightweight roadmap, epic, and task
  tracker under `state/work/`.
- `govern-documents` audits opted-in Markdown document metadata, declared dependencies,
  and local links without changing the repository.

Audits are read-only and advisory by default. Initializers and fixes show a dry-run plan
and require explicit approval before they use `--apply`. Blocking CI is optional.

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

## Governance sources

The repository copies its canonical standards into the installable skill packages for
offline and direct-install use. Repository tests enforce byte-for-byte parity between those
copies. PMM-specific examples remain under each skill's `assets/examples/pmm-engine/`
directory and do not alter the generic core.
