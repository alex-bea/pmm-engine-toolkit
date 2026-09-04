---
doc_type: DOC
normative: false
requires:
  - ../legal/IP-PRIVACY-REVIEW-PMM-INSTINCT-REVIEW-0.2.0-2026-09-04.md
  - gitleaks-tracked-tree-pmm-instinct-review-2026-09-04.json
status: Draft
version: "0.2.0"
owner: toolkit-maintainers
consumers:
  - public toolkit maintainers
change_control: Pull request review
---

# PMM Instinct Review `0.2.0` secret and private-term audit

## Result

Passed locally on 2026-09-04. Gitleaks 8.30.1 reported zero findings in the full release-
candidate working tree. The PMM Skill Publicizer scanner reported `CLEAN` for the complete
`plugins/pmm-instinct-review/` candidate with the run-specific private denylist.

## Method and scope

- Gitleaks built-in rules, no baseline or custom allowlist, `gitleaks:allow` suppression
  disabled, 100 percent redaction, approximately 2.92 MB scanned.
- Publicizer secret, credential, private-key, user-path, fictional-example URL, unfinished-
  placeholder, and case-insensitive denylist checks over the full plugin package.
- Manual review of the other manifest-authorized code, test, catalog, export, release, legal,
  and security changes against the same denylist.
- The existing public project name “PMM Engine” is an adjudicated nominative public reference
  in repository-level catalog/export prose, not a private entity leak. No other denylist term
  appears in the changed candidate.
- The denylist itself remains outside the public repository and is not committed.

## Evidence

| Check | Result | Evidence |
|---|---|---|
| Full working-tree secret scan | 0 findings | [`gitleaks-tracked-tree-pmm-instinct-review-2026-09-04.json`](gitleaks-tracked-tree-pmm-instinct-review-2026-09-04.json) |
| Plugin private-denylist scan | CLEAN | Local command receipt; denylist retained outside the repository |
| Fictional URL review | All example web/email values use `.invalid` | Northstar Reports example set |
| Human narrative review | No unadjudicated private phrase, fact bundle, path, ID, route, or alias map | Final manifest diff review |

## Limitations and gate

Pattern and entropy scans are evidence, not proof that sensitive data is absent. The pull
request still requires hosted checks and owner review. Re-run the scans if any candidate file
changes; this Draft audit does not authorize merge or release.
