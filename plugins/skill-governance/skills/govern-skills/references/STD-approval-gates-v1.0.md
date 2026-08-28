---
doc_type: STD
normative: true
requires: []
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Codex users
  - skill authors
change_control: Pull request review
---

# Approval Gates Standard

| Level | Action | Default |
|---|---|---|
| Read | Inspect local or user-approved sources | Proceed |
| Draft | Create a local proposal, audit, or dry-run | Proceed |
| Local write | Create or modify repository files | Show exact paths and request approval |
| External write | Post, message, schedule, publish, or mutate a service | Require explicit approval |
| Destructive | Delete, overwrite, force-push, or remove work | Require target-specific approval and a clean-state check |

Approval for one level or target does not imply approval for another. Initializers and fix
workflows must inspect first, show a deterministic plan, and require an explicit `--apply`
or equivalent user confirmation before writing. Existing differing files must never be
silently overwritten. Generated monitors and automations default to dry-run or review-first
operation.
