# Instinct-review release-candidate secrets audit — 2026-08-25

## Result

Passed locally. Gitleaks 8.30.1 reported zero findings in both the complete reachable Git
history and the release-candidate working tree containing the new plugin artifacts.

## Method and scope

- Built-in Gitleaks rules; no custom configuration, baseline, ignore file, or allowlist.
- `gitleaks:allow` comment suppression disabled.
- Findings fully redacted in command output and reports.
- All refs after the implementation commit: the complete reachable branch history was scanned.
- Release-candidate tree: every file in the working release candidate was scanned, including
  plugin, documentation, test, marketplace, and governance files.

## Evidence

| Pass | Report | Findings |
| --- | --- | ---: |
| All refs and reachable commits | [`gitleaks-all-refs-2026-08-25.json`](gitleaks-all-refs-2026-08-25.json) | 0 |
| Release-candidate tree | [`gitleaks-tracked-tree-2026-08-25.json`](gitleaks-tracked-tree-2026-08-25.json) | 0 |

The committed reports contain empty JSON arrays. The all-ref scan will be repeated after the
implementation commit; an unchanged empty report is the expected result.

## Limitations and release gate

Signature and entropy scanning is evidence, not proof, that sensitive values are absent.
CodeQL and dependency review run on the public pull request. Publication still requires an
approved IP review and pull request, and GitHub secret scanning and push protection should
remain enabled.
