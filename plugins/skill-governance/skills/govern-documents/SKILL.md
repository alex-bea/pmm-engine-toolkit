---
name: govern-documents
description: Audit opted-in governed Markdown documents for metadata, declared dependencies, and local-link integrity. Use when a user asks to audit document governance, validate governed Markdown, check document metadata, or run a document-governance review. The audit is read-only and advisory unless the user explicitly requests strict validation.
---

# Govern Documents

Audit only repository Markdown that opts in with `doc_type` YAML frontmatter. Keep the
audit read-only: report structural findings, then let the document owner decide whether
and how to correct them.

## Workflow

1. Resolve the target repository and read any applicable repository instructions.
2. Read `references/STD-governance-document-metadata-v1.0.md`,
   `references/STD-evidence-privacy-v1.0.md`, and
   `references/STD-approval-gates-v1.0.md` before interpreting findings.
3. Run `python3 scripts/govern_documents.py audit --repo <repository>`.
4. Use `--format json` only when a machine-readable result is useful. Use `--strict`
   only for an explicitly requested release or CI gate; the normal audit is advisory.
5. Separate mechanical findings from review-required work. Metadata, declared
   dependencies, and local links can be checked mechanically. Claim truth, source
   authority, caveats, publication approval, and audience suitability require human or
   agent review.

For the detailed command contract and review order, read
`references/RUN-document-governance-audit-v1.0.md`. Start a new governed document from
`assets/templates/governed-document.md` when the repository has adopted this standard.

## Boundaries

- A document is governed only when its YAML frontmatter declares `doc_type`.
- Ordinary Markdown and every `SKILL.md` are intentionally ignored.
- The audit validates structure and local paths; it does not judge factual claims or
  remote URLs.
- Never add frontmatter, select an owner, infer a status, rewrite a document, or publish
  content as part of this audit.
