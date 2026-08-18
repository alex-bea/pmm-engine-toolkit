# PMM Engine Toolkit

A small, portable subset of PMM Engine for planning disciplined work and keeping code
changes understandable:

- **PM Prioritizer** — an agent skill for reducing build plans to a coherent MVP, with
  explicit deferred and declined scope.
- **Diffguard Lite** — a local Git-diff analyzer for Python and JavaScript complexity,
  file size, churn, and test health.
- **Writing workflows** — guidance review, marketing briefs, sales one-pagers, product
  pages, executive pre-reads, strategic narratives, professional habits, and consented
  LinkedIn ghostwriting.

This repository deliberately contains no customer data, operating outputs, product-source
registries, runtime configuration, integrations, or private Git history.

The writing skills intentionally use generic templates. Supply your own approved claims
guide, positioning, examples, legal review, and consented voice profile rather than relying
on embedded company, customer, or individual data.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest tests/test_diffguard_lite.py
```

Run Diffguard Lite against a Git base ref:

```bash
.venv/bin/python scripts/governance/diffguard_lite.py --base origin/main
```

The PM Prioritizer skill is self-contained under `skills/pm-prioritizer/`. Load its
`SKILL.md` together with its listed reference files in an agent runtime that supports
repository-local skills.

## Skill authoring

The included [skill catalog](docs/SKILL-CATALOG.md), [skill-structure standard](docs/STD-skill-structure-v1.0.md),
and [format templates](docs/templates/) are the public reference set for extending this
toolkit without copying private operating context.

## Security and contributions

See [SECURITY.md](SECURITY.md) for vulnerability reporting and
[CONTRIBUTING.md](CONTRIBUTING.md) for contribution expectations.

## License

This staging repository is intentionally not licensed for public release until its owner
selects and records the appropriate license.
