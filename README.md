# PMM Engine Toolkit

A portable, public-safe PMM operating toolkit for planning work, producing evidence-bound
marketing artifacts, synthesizing signals, and maintaining repository hygiene:

- **26 agent skills** — the complete approved v1 set across planning, execution,
  intelligence, drafting, signal operations, and repository hygiene.
- **Diffguard Lite** — a local Git-diff analyzer for Python and JavaScript complexity,
  file size, churn, and test health.
- **Standards and templates** — public skill structure, evidence/privacy, approval-gate,
  tracker, and dependency-closure rules with reusable formats and synthetic examples.

This repository deliberately contains no customer data, operating outputs, private source
registries, account identifiers, credentials, or private Git history. Integrations are
represented by local config templates and adapter contracts only.

The writing skills intentionally use generic templates. Supply your own approved claims
guide, positioning, examples, legal review, and consented voice profile rather than relying
on embedded company, customer, or individual data.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests
```

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

## Security and contributions

See [SECURITY.md](SECURITY.md) for vulnerability reporting and
[CONTRIBUTING.md](CONTRIBUTING.md) for contribution expectations.

## License

This staging repository is intentionally not licensed for public release until its owner
selects and records the appropriate license.
