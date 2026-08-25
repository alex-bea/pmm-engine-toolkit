# Continuous Integration

## Required checks

The public repository runs these checks on pull requests:

- `Tests (Python 3.10)` through `Tests (Python 3.14)`;
- `Governance`; and
- `CodeQL`; and
- `Dependency review` when dependency or workflow files change.

The repository-settings gate requires the five test jobs, governance, and CodeQL before
merge. Dependency review runs when dependency, workflow, or plugin files change. It is not
configured as an always-required check because GitHub will leave it absent on unrelated pull
requests.

## Security properties

- Default workflow permissions are read-only and no job references repository secrets.
- CodeQL alone receives `security-events: write`, narrowly scoped to uploading analyses.
- Every external action is pinned to a full 40-character commit SHA with its release tag in
  a comment for auditability.
- Checkout credentials are not persisted beyond the checkout step.
- Jobs run on the fixed `ubuntu-24.04` hosted-runner label and have explicit timeouts.
- Superseded runs are cancelled through per-ref concurrency groups.
- Pull requests use the `pull_request` event; `pull_request_target` is prohibited.
- Build tooling is installed from `requirements-build.lock` with hashes and binary-only
  mode. Runtime packages are hash-locked and built without isolated dependency downloads.

## Updating dependencies

Dependabot proposes grouped weekly updates for Python packages and GitHub Actions. Review
action updates by checking the upstream release and verifying the new full commit SHA.

After changing a source manifest, regenerate both universal lock files as applicable:

```bash
uv pip compile requirements.txt --universal --python-version 3.10 \
  --generate-hashes --output-file requirements.lock
uv pip compile requirements-build.txt --universal --python-version 3.10 \
  --generate-hashes --output-file requirements-build.lock
```

Then run the local parity checks:

```bash
.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r requirements-build.lock
.venv/bin/python -m pip install --require-hashes --no-build-isolation -r requirements.lock
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/governance/validate_github_actions.py
.venv/bin/python scripts/governance/validate_skill_pack.py
.venv/bin/python scripts/governance/build_ip_inventory.py
git diff --exit-code -- docs/legal/IP-INVENTORY.csv
actionlint
zizmor .
```

Repository-level branch protection, secret scanning, push protection, and Actions policy
settings are declared and automated in
[`security/GITHUB-SECURITY-CONTROLS.md`](security/GITHUB-SECURITY-CONTROLS.md).
