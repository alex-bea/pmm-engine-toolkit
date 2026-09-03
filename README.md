# PMM Engine Toolkit

A portable, public-safe PMM operating toolkit for planning work, producing evidence-bound
marketing artifacts, synthesizing signals, and maintaining repository hygiene:

- **25 standalone agent skills** — the approved v1 set across planning, execution,
  intelligence, drafting, signal operations, and repository hygiene.
- **PMM Instinct Review plugin (draft)** — an installable, human-gated Codex improvement
  loop for local capture, extraction, review, promotion, and cleanup.
- **Diffguard Lite** — a local Git-diff analyzer for Python and JavaScript complexity,
  file size, churn, and test health.
- **Standards and templates** — public skill structure, evidence/privacy, approval-gate,
  tracker, and dependency-closure rules with reusable formats and synthetic examples.
- **Codex governance plugin** — approval-gated initialization, advisory audits, safe
  mechanical fixes, optional blocking CI for skills and work, and opt-in document audits.

This repository deliberately contains no customer data, operating outputs, private source
registries, account identifiers, credentials, or private Git history. Integrations are
represented by local config templates and adapter contracts only.

The writing skills intentionally use generic templates. Supply your own approved claims
guide, positioning, examples, legal review, and consented voice profile rather than relying
on embedded company, customer, or individual data.

## Quick start

Requirements: Git and Python 3.10 or newer.

```bash
git clone <repository-url>
cd pmm-engine-toolkit
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r requirements-build.lock
.venv/bin/python -m pip install --require-hashes --no-build-isolation -r requirements.lock
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/governance/validate_skill_pack.py
```

The `requirements*.txt` files are human-maintained source manifests. Their corresponding
lock files provide the hash-verified installation used by CI and recommended for local
setup. Build tooling is installed first so the one source-only runtime package can build
without fetching undeclared build dependencies.

Run Diffguard Lite against a Git base ref:

```bash
.venv/bin/python scripts/governance/diffguard_lite.py --base origin/main
```

Each skill is self-contained under `skills/<name>/` except for explicitly linked shared
standards in `docs/`. Run `python3 scripts/governance/validate_skill_pack.py` to verify
the selected inventory, required resources, local links, frontmatter, and public-safety
guardrails.

## PMM Instinct Review plugin (draft)

The plugin is a release candidate pending pull-request approval. Installation does not
enable chat capture. After installation, review and trust both hooks with `/hooks`, confirm
your employer permits local transcript-derived storage and a second Codex model invocation,
then explicitly enable learning through `$pmm-instinct-review`.

```bash
codex plugin marketplace add alex-bea/pmm-engine-toolkit --ref main
codex plugin add pmm-instinct-review@pmm-engine-toolkit
```

If `codex` is not on `PATH` on macOS, use either installed app binary:

```bash
"/Applications/ChatGPT.app/Contents/Resources/codex" plugin marketplace add alex-bea/pmm-engine-toolkit --ref main
"/Applications/ChatGPT.app/Contents/Resources/codex" plugin add pmm-instinct-review@pmm-engine-toolkit
```

The equivalent Codex app binary path is
`/Applications/Codex.app/Contents/Resources/codex`.

Enabling creates user-owned state under `~/.codex/instinct-review/`. The plugin has no
telemetry or hosted PMM service, and it never changes native Codex history. Removing the
plugin leaves captured state in place. See the
[operator guide](plugins/pmm-instinct-review/README.md) and [privacy policy](PRIVACY.md)
before enabling it on a work device.

## Skill authoring

The included [skill catalog](docs/SKILL-CATALOG.md), [skill-structure standard](docs/STD-skill-structure-v1.0.md),
and [format templates](docs/templates/) are the public reference set for extending this
toolkit without copying private operating context.

The [competitive-intelligence starter kit](skills/comp-intel/README.md) publishes the reusable
framework of a mature working practice: source mapping, collection logic, evidence standards,
competitor registries, positioning and narrative analysis, gap trackers, executive briefing,
review gates, and a complete fictional example. Copy the skill into Claude Code, Codex, or
another compatible agent environment, fill the adopter-owned templates, and use the guided
workflow with whatever source access you authorize.

The document-led workflow is the default. An optional standard-library controller adds
synthetic/local-file adapters, deterministic evidence manifests, digest-bound review records,
and guarded local-state apply for teams that need machine-enforced controls:

```bash
python3 skills/comp-intel/scripts/comp_intel.py init --data-root ./comp-intel-data
python3 skills/comp-intel/scripts/comp_intel.py doctor --data-root ./comp-intel-data --market synthetic-devtools
python3 skills/comp-intel/scripts/comp_intel.py collect --data-root ./comp-intel-data --market synthetic-devtools --from 2026-08-18 --to 2026-08-26
```

Every controller collection intentionally stops at evidence review; later controller steps
require two digest-bound review records. The guided workflow does not require bundled web,
repository, or communication adapters: adopters use the source tools already available in
their agent environment and record the resulting evidence using the shipped contract.

The earlier [Codex migration requirements](docs/product-requirements/comp-intel/README.md) are
retained as non-binding design history.

See the [public export manifest](docs/PUBLIC-EXPORT-MANIFEST.md) for the exact package
contract, generalization rules, and pre-publication gates.

## Codex governance plugin

Install the public marketplace and plugin:

```bash
codex plugin marketplace add alex-bea/pmm-engine-toolkit --ref main
codex plugin add skill-governance@pmm-engine-toolkit
```

The three plugin skills can also be installed independently from their GitHub directories
with Codex's built-in `$skill-installer`. See the complete
[installation and adoption guide](docs/CODEX-GOVERNANCE-PLUGIN.md), including the
[document-governance baseline](docs/CODEX-DOCUMENT-GOVERNANCE.md).

## Community and governance

- [Contributing](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Project governance](GOVERNANCE.md)
- [Security policy](SECURITY.md)
- [Support policy](SUPPORT.md)
- [Privacy policy](PRIVACY.md)
- [Continuous integration](docs/CI.md)

## License

Copyright 2026 Alexander Bea.

Licensed under the [Apache License 2.0](LICENSE).
See the repository [notice](NOTICE), [third-party notices](THIRD_PARTY_NOTICES.md), and
[IP-rights review](docs/legal/IP-RIGHTS-REVIEW-2026-08-18.md) for attribution and
redistribution details. Third-party product names are used nominatively; no affiliation or
endorsement is claimed.
