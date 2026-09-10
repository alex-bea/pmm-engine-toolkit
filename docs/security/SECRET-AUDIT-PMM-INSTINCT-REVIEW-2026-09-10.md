---
doc_type: DOC
normative: false
requires:
  - ../legal/IP-PRIVACY-REVIEW-PMM-INSTINCT-REVIEW-0.3.0-2026-09-10.md
  - gitleaks-tracked-tree-pmm-instinct-review-2026-09-10.json
status: Draft
version: "0.3.0"
owner: toolkit-maintainers
consumers:
  - public toolkit maintainers
change_control: Pull request review
---

# PMM Instinct Review `0.3.0` secret and private-term audit

## Status

Clean local automated and agent-assisted review of the frozen `0.3.0` candidate. No
candidate-introduced secret, credential, private term, developer path, live fictional URL, or private
identifier was found. Final project-owner narrative review remains part of pull-request Gate B;
this Draft is evidence for review, not approval to merge or release.

## Method and scope

- Gitleaks `8.30.1` scanned a snapshot of the complete release-candidate tree using built-in
  rules, no candidate-specific baseline or allowlist, disabled inline suppression, and full
  redaction.
- The PMM Skill Publicizer scanner checked its secret, credential, private-key, user-path,
  fictional-example URL, unfinished-placeholder, and run-specific private-term checks across
  the complete plugin package and every other manifest-authorized change.
- The review validated that fictional web and email values use reserved `.invalid` domains and
  that no absolute developer path, live account identifier, real session content, machine
  configuration, route, or private-to-fictional crosswalk is present.
- Native Claude hook commands, installer receipts, evidence, queue data, promotion receipts,
  and changesets were reviewed for synthetic-only values and safe relative paths.
- Agent-assisted narrative and security review covered the exact 57-path candidate. The
  run-specific private denylist remained outside the public repository. Project-owner review
  remains pending at Gate B.

## Evidence status

| Check | Result | Evidence |
|---|---|---|
| Full candidate-tree secret scan | Pass: zero findings | Generated Gitleaks report: [`gitleaks-tracked-tree-pmm-instinct-review-2026-09-10.json`](gitleaks-tracked-tree-pmm-instinct-review-2026-09-10.json) |
| Complete plugin publicizer scan | Pass: zero findings | Complete self-contained `plugins/pmm-instinct-review/` package scanned with the external run-specific denylist |
| Exact 57-path private-term review | Pass after adjudication | Five scanner matches appeared only in pre-existing unchanged content in three modified files; zero matches occurred in candidate-added content |
| Absolute developer-path review | Pass: zero findings | Publicizer path rules plus exact-diff review |
| Fictional URL and identifier review | Pass: zero findings | Northstar Reports Claude fixtures use synthetic identifiers and reserved `.invalid` values |
| Agent-assisted narrative and security review | Pass: no actionable P0, P1, or P2 findings remain | Exact manifest diff, hook boundary, state confinement, promotion authority, installer, and fixture review |
| Project-owner narrative review | Pending | Pull-request Gate B; not represented as complete by this Draft |

## Limitations and gate

Pattern and entropy scans are evidence, not proof that sensitive data is absent. Re-run every
check after any candidate change. The scan covers the repository candidate, not adopter state,
credentials, transcripts, or the destination machine. A missing, stale, skipped, or failing
result blocks a clean audit and release-readiness claim. This Draft does not authorize merge or
release.
