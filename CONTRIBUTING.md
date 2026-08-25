# Contributing

Thank you for helping improve PMM Engine Toolkit. Contributions should make the toolkit
more reusable without introducing private operating context.

## Before contributing

- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Do not submit credentials, personal data, customer information, private links, internal
  identifiers, or third-party material without redistribution permission.
- Keep examples fictional and label unsupported facts `[Missing]`.
- Report vulnerabilities through [SECURITY.md](SECURITY.md), not a public issue.

## Local setup

Use Git and Python 3.10 or newer:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r requirements-build.lock
.venv/bin/python -m pip install --require-hashes --no-build-isolation -r requirements.lock
```

Run the complete validation suite before opening a pull request:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/governance/validate_github_actions.py
.venv/bin/python scripts/governance/validate_skill_pack.py
.venv/bin/python scripts/governance/configure_github_security.py \
  --repo example/pmm-engine-toolkit --plan
```

## Change requirements

- Keep pull requests focused and explain the user problem and behavioral change.
- Add or update tests for code and deterministic workflow changes.
- Preserve the public package contract in `docs/STD-skill-dependencies-v1.0.md`.
- Keep `SKILL.md` concise; move detailed knowledge into `references/` and reusable output
  material into `assets/`.
- Keep canonical standards and their installable plugin mirrors byte-for-byte identical.
- Preserve advisory-by-default audits, explicit apply gates, and non-overwrite behavior.
- Update the skill catalog or governance documentation when the public interface changes.
- Never weaken privacy, approval-gate, dependency, or secrets checks merely to make a test pass.

## Review and acceptance

Maintainers may request changes for correctness, safety, scope, documentation, or long-term
maintenance cost. A contribution is not accepted until it is reviewed and merged. See
[GOVERNANCE.md](GOVERNANCE.md) for decision-making and release authority.

Unless explicitly marked otherwise, intentional contributions are submitted under the
[Apache License 2.0](LICENSE), consistent with section 5 of that license.
