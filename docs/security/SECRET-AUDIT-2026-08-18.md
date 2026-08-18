# Independent Secrets and Credential Audit — 2026-08-18

## Result

Passed. Gitleaks reported zero findings in both the complete Git history and the
tracked release tree.

## Scope

- Repository state: `refs/heads/codex/public-v1-toolkit` at
  `6ce08b729f49bb93f74b7b84f6d4e37cb790a4c8` before this evidence was added.
- History: every commit reachable from every local ref, using `git log --all` semantics.
- History volume: 6 commits and approximately 173 KB scanned.
- Release tree: the exact tracked files exported from `HEAD` with `git archive`.
- Release-tree volume: approximately 163 KB scanned.
- Local ignored or untracked files, including `.venv`, were outside the release tree
  and are not publication content.

## Method

- Scanner: Gitleaks 8.30.1.
- Rules: the scanner's built-in default rule set.
- Suppression controls: no custom configuration, baseline, ignore file, or allowlist.
- Inline `gitleaks:allow` directives were explicitly disabled as suppressions with
  `--ignore-gitleaks-allow`.
- Reports were generated as fully redacted JSON.

Commands, run from the repository root:

```bash
gitleaks git --no-banner --no-color --redact --ignore-gitleaks-allow \
  --report-format json --report-path history.json --log-opts=--all .
gitleaks dir --no-banner --no-color --redact --ignore-gitleaks-allow \
  --report-format json --report-path tracked-tree.json <tracked-tree-snapshot>
```

## Evidence

| Pass | Report | Findings | SHA-256 |
| --- | --- | ---: | --- |
| All refs and reachable commits | [`gitleaks-history-2026-08-18.json`](gitleaks-history-2026-08-18.json) | 0 | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |
| Tracked release tree | [`gitleaks-tracked-tree-2026-08-18.json`](gitleaks-tracked-tree-2026-08-18.json) | 0 | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |

The identical checksums are expected: each zero-finding JSON report contains an empty
array.

## Limitations and publication gate

This signature and entropy scan is evidence, not proof, that no sensitive value exists.
Publication still requires the separate IP-rights review and final release verification.
GitHub secret scanning and push protection should also be enabled when the public remote
is created.

