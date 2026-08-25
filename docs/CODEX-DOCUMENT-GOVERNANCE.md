---
doc_type: DOC
normative: false
requires:
  - STD-governance-document-metadata-v1.0.md
  - STD-evidence-privacy-v1.0.md
  - STD-approval-gates-v1.0.md
status: Active
version: "1.0"
owner: toolkit-maintainers
consumers:
  - Codex users
  - document maintainers
change_control: Pull request review
---

# Codex Document Governance

This guide provides a small, opt-in baseline for documents that will be reused, inform a
decision, or be shared outside their working context. It is intentionally narrower than
governing every Markdown file or conversation.

## Instruction precedence

Place durable personal defaults in `~/.codex/AGENTS.md`. Codex reads that global guidance
for each task, then applies repository and nested `AGENTS.md` files for the current work.
The more specific repository instruction can narrow or supersede the global default. Keep
project-specific policy, owners, and approval paths in the repository rather than in the
global file.

## Copyable global baseline

Add a version of this neutral baseline to `~/.codex/AGENTS.md`:

```md
# Document governance baseline

Apply these rules to final, reusable, decision-making, or externally shareable documents.
Defer to applicable repository and nested AGENTS.md instructions when they are more
specific.

- Prefer authoritative sources; identify the source when it materially supports a claim.
- State material assumptions, missing facts, and uncertainty explicitly.
- Preserve material caveats and constraints when summarizing or revising source material.
- Keep external-publication material as a draft until the applicable review or approval
  process is complete.
- Use relevant local review workflows when the repository provides them.
```

This baseline does not require a particular vendor, review tool, or document template.

## Adoption path

1. Add the global baseline and start a new Codex task so it is loaded.
2. In a repository that wants mechanical checks, opt individual documents in by adding
   the YAML metadata defined by the [metadata standard](STD-governance-document-metadata-v1.0.md).
   Markdown without `doc_type` remains untouched by the audit.
3. Install the `skill-governance` plugin and ask Codex to use `$govern-documents`, or run
   `python3 scripts/govern_documents.py audit --repo <path>` from the installed skill.
4. Treat findings as an advisory review. Use `--format json` for automation and `--strict`
   only when an adopter deliberately wants a blocking check.

The included [governed-document template](../plugins/skill-governance/skills/govern-documents/assets/templates/governed-document.md)
is a starting point, not a required repository-wide migration.

## What automation can and cannot decide

The audit checks opted-in document metadata, declared `requires` paths, and local Markdown
links. It does not decide whether claims are true, sources are authoritative, caveats are
adequate, a document suits its audience, or content is approved for publication. Those
questions remain a responsible human or agent review, following any repository policy.

For plugin installation and the complementary skill and work-tracker workflows, see the
[Codex Skill Governance Plugin guide](CODEX-GOVERNANCE-PLUGIN.md).
