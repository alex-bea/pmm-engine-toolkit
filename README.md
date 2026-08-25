# PMM Engine Toolkit

A portable, public-safe PMM operating toolkit for planning work, producing evidence-bound
marketing artifacts, synthesizing signals, and maintaining repository hygiene:

- **26 agent skills** — the complete approved v1 set across planning, execution,
  intelligence, drafting, signal operations, and repository hygiene.
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

## Skill authoring

The included [skill catalog](docs/SKILL-CATALOG.md), [skill-structure standard](docs/STD-skill-structure-v1.0.md),
and [format templates](docs/templates/) are the public reference set for extending this
toolkit without copying private operating context.

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
