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

The governance job also validates the Codex plugin manifest and hooks, marketplace entry,
all three installable skills, mirrored standards, dry-run behavior, advisory exit behavior,
strict exit behavior, approval-gated writes, shared policy decisions, harness-payload parity,
scheduled restrictions, stale-digest denial, external-verifier failures, and publisher
isolation. Document audits remain opt-in and advisory; no document-specific workflow is
installed into adopting repositories.

For PMM Instinct Review `0.3.1`, governance separately validates the Codex and Claude
manifests, runtime-specific hook variables, bundle-root Claude scripts and extractor assets,
the detailed Claude setup runbook, and the complete fictional Claude lifecycle. Focused tests
cover Codex persisted-model enablement, legacy null-model no-artifact skips, hook/backfill model
binding, safe RUN/REF route parsing and confinement, fail-closed target choice, standalone
Claude installation without a marketplace, disabled-by-default capture, evidence
minimization and redaction, bounded extraction and retries, explicit review decisions,
digest-bound promotion receipts, target-drift rejection, governed patch delivery, background
worker isolation, uninstall scope, and complete Claude/Codex/portable regressions.

The `0.3.1` claim is parity with the private PMM Engine Codex model/routing outcomes. CI must
not describe Codex as having Claude's immutable receipt-bound promotion transaction layer.
Candidate-specific local results are recorded in the Draft release evidence from commands
actually run. Hosted pull-request results remain pending until the candidate branch is pushed
and the checks complete.

The real Claude and Codex lifecycle smoke tests are environment-dependent and are not replaced
by fictional fixtures or mocked process tests. Release evidence must record the corresponding
case as `not run` when a compatible authenticated CLI or isolated lifecycle environment is
unavailable; an unavailable check cannot be reported as a pass. The bounded procedures and
pass criteria are PIRC-AT-008 and PIRC-AT-008B in the submission test cases.

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
- Governance negative tests assert that denied file mutations and publisher calls did not
  occur. CI receives no approval-verifier or publisher credential.

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
