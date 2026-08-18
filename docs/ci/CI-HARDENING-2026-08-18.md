# Public CI Hardening Evidence — 2026-08-18

## Result

Passed locally. The public-release candidate contains two least-privilege workflows and a
weekly dependency-update configuration. No workflow requires a private secret or a
write-capable token.

## Controls implemented

- `actions/checkout` v7.0.1, `actions/setup-python` v7.0.0, and
  `actions/dependency-review-action` v5.0.0 are pinned to reviewed 40-character commit
  SHAs.
- Repository permissions are limited to `contents: read`; persisted checkout credentials
  and `pull_request_target` are prohibited.
- Test jobs cover Python 3.10 through 3.14 on the fixed `ubuntu-24.04` runner label.
- Every job has a timeout, and concurrency groups cancel superseded runs.
- Runtime and build packages are version- and hash-locked. Build tooling is installed
  before the source-only dependency is built with isolated dependency downloads disabled.
- Dependency review blocks newly introduced high- or critical-severity vulnerabilities.
- Dependabot groups weekly Python and GitHub Actions updates and applies explicit release
  cooldowns; security updates are not delayed by those version-update cooldowns.
- The workflow-policy validator rejects unreviewed or mutable actions, write permissions,
  secret references, unsafe event triggers, untrusted event interpolation in shell steps,
  missing timeouts, and persisted checkout credentials.

## Local verification

| Check | Result |
| --- | --- |
| actionlint 1.7.12 | Passed with zero findings |
| zizmor 1.24.1 | Passed with zero findings |
| Clean Python 3.11.14 lockfile install | Passed |
| Clean Python 3.14.5 lockfile install | Passed |
| Full unit suite | 32 tests passed in both clean environments |
| Workflow-policy validator | 2 workflows passed |
| Public package validator | 26 skills and dependencies passed |
| Gitleaks 8.30.1 candidate-tree scan | Zero findings |
| ScanCode Toolkit 32.5.0 candidate-tree scan | Zero scan errors; expected license references only |

## Remaining online verification

The staging repository has no public remote, so GitHub-hosted jobs cannot run yet. After
the repository is created, confirm that all matrix jobs execute successfully and configure
the required checks listed in [`../CI.md`](../CI.md). Branch protection, Actions policy,
secret scanning, and push protection belong to the next GitHub security-controls gate.

