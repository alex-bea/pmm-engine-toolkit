# Instinct-review release-candidate secrets audit — 2026-08-25

## Result

Passed locally. Gitleaks 8.30.1 reported zero findings in both the complete reachable Git
history and the final release-candidate working tree, including the plugin's product,
implementation, and public-review documentation.

## Method and scope

- Built-in Gitleaks rules; no custom configuration, baseline, ignore file, or allowlist.
- `gitleaks:allow` comment suppression disabled.
- Findings fully redacted in command output and reports.
- All reachable refs: 13 commits and approximately 592 KB were scanned.
- Release-candidate tree: every file in the working release candidate was scanned, including
  plugin, documentation, tests, marketplace, and governance files (approximately 1.07 MB).

## Evidence

| Pass | Report | Findings |
| --- | --- | ---: |
| All refs and reachable commits | [`gitleaks-all-refs-2026-08-25.json`](gitleaks-all-refs-2026-08-25.json) | 0 |
| Release-candidate tree | [`gitleaks-tracked-tree-2026-08-25.json`](gitleaks-tracked-tree-2026-08-25.json) | 0 |

The committed reports contain empty JSON arrays. Re-run both scans after any change to the
published tree; an unchanged empty report is the expected result.

## Limitations and release gate

Signature and entropy scanning is evidence, not proof, that sensitive values are absent.
CodeQL and dependency review run on the public pull request. Publication still requires an
approved IP review and pull request, and GitHub secret scanning and push protection should
remain enabled.
