# GitHub Security Controls

This document is the launch baseline for the public repository. The desired state lives in
[`config/github-security-controls.json`](../../config/github-security-controls.json), and
[`configure_github_security.py`](../../scripts/governance/configure_github_security.py)
plans, applies, and verifies it through the GitHub REST API.

## Required state

| Control | Required setting |
| --- | --- |
| Repository | Public, with `main` as the default branch |
| Merge policy | Squash only; auto-merge and update-branch enabled; merged branches deleted |
| Default branch | Pull request required; one approval; stale approvals dismissed; last push approved by someone else; review threads resolved |
| History | Linear history; branch deletion and force pushes blocked |
| Required checks | Five Python versions, governance, and CodeQL |
| Ruleset bypass | None |
| Actions allowlist | GitHub-owned actions only, with full-SHA pinning enforced |
| Workflow permissions | Read-only by default; workflows cannot approve pull requests |
| Code scanning | CodeQL advanced workflow on pushes, pull requests, weekly schedule, and manual runs |
| Dependency security | Dependency graph and alerts enabled; Dependabot security updates enabled |
| Secret protection | Secret scanning and push protection enabled |
| Vulnerability intake | Private vulnerability reporting enabled |

The CodeQL workflow is the only workflow granted a write permission, limited to
`security-events: write` so it can upload analysis results. All other workflow permissions
remain read-only.

## Launch procedure

The script defaults to an offline plan and does not contact or mutate GitHub:

```bash
python3 scripts/governance/configure_github_security.py \
  --repo OWNER/REPOSITORY --plan
```

After the fresh-history repository has been created as public, the default branch is
`main`, and administrator authentication is available through GitHub CLI, apply the
controls:

```bash
python3 scripts/governance/configure_github_security.py \
  --repo OWNER/REPOSITORY --apply
```

Run the CodeQL workflow once on `main`, then verify both the settings and the presence of
an uploaded code-scanning analysis:

```bash
python3 scripts/governance/configure_github_security.py \
  --repo OWNER/REPOSITORY --verify
```

Application is intentionally refused unless the target repository is already public and
uses `main` as its default branch. The ruleset is created or updated by its stable name, so
re-running `--apply` is idempotent. Verification fails closed on drift or missing CodeQL
results.

## Required-check note

`Dependency review` runs only when dependency manifests, lock files, plugin files,
Dependabot configuration, or workflows change. It must not be an always-required check:
GitHub would leave that check absent on unrelated pull requests. The always-required list is
encoded in the ruleset policy.

## Evidence to retain

After launch, retain the successful `--verify` output with the release evidence. Also
confirm in the GitHub Security view that CodeQL, secret scanning, push protection,
Dependabot alerts, and private vulnerability reporting are visible and enabled. A settings
change is not complete until verification passes.
