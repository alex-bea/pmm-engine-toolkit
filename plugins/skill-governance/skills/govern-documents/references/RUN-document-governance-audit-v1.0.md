---
doc_type: RUN
normative: true
requires:
  - STD-governance-document-metadata-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-approval-gates-v1.0.md
status: Active
version: "1.0"
owner: toolkit-maintainers
consumers:
  - document reviewers
  - Codex users
change_control: Pull request review
---

# Document Governance Audit Runbook

## Purpose

Use this runbook to inspect the mechanical integrity of opted-in governed Markdown. It
is an advisory review by default and does not change the target repository.

## Eligibility

Only Markdown files with a YAML-frontmatter `doc_type` are in scope. `SKILL.md` files
and ordinary Markdown remain outside this audit so repositories can adopt document
governance incrementally.

## Command

```bash
python3 scripts/govern_documents.py audit --repo <repository>
```

Add `--format json` for a machine-readable result. Add `--strict` only when the caller
has requested a blocking check; it returns nonzero when findings exist. Without
`--strict`, findings are reported and the command exits successfully.

## Review sequence

1. Confirm that the target repository and its local instructions are the intended scope.
2. Run the advisory audit and group findings by document.
3. Confirm whether each structural finding is deliberate or needs correction by the
   responsible document owner.
4. For documents intended for decisions or external sharing, separately review source
   authority, explicit assumptions, caveats, and approval requirements.
5. Re-run the audit after approved edits. Do not use audit output as evidence that a
   claim is true or content is approved for publication.

## Checks

The audit checks required metadata, recognized type and status values, declared
`requires` paths relative to the document, and local Markdown links. It does not follow
network links and it never creates, rewrites, or infers metadata.
