# Govern Skills: copy the pattern, not the plugin

This standalone package is a model-readable governance kit. Give it to Claude Code,
Codex, or another capable local coding agent and ask the agent to reproduce the useful
pattern inside your repository. No plugin, marketplace install, hosted service, or bundled
runtime is required.

Start with this prompt:

```text
Read skills/govern-skills/README.md and every package file it routes you to. Inspect this
repository and recreate the governance pattern here, adapted to the conventions that
already exist. Begin with a read-only inventory, a setup-readiness report, and an exact
proposed file plan. Do not install a plugin or add hooks, CI, registries, runtime
enforcement, external approval services, or publishers unless I separately approve those
layers. Preserve unrelated work and stop before every unapproved write.
```

If you are reading the package at a public URL rather than in the target repository, tell
the agent to use that URL as its read-only reference and substitute the target repository's
actual root during inspection.

## Why the files are separated

The package makes each maintenance concern easy to find:

| Primitive | Job | Typical update point |
|---|---|---|
| `SKILL.md` | Discovery, routing, and durable boundaries | Change when the job or trigger changes. |
| `RUN-*.md` | Ordered setup and operating workflow | Insert or change a workflow step here. |
| `STD-*.md` | Stable rules shared across decisions | Change only when the rule itself changes. |
| `REF-*.md` | Detailed guidance needed in one mode | Add knowledge without bloating the entrypoint. |
| Templates | Blank structures copied and adapted | Change when an artifact contract changes. |
| Examples | Fictional completed demonstrations | Change when users need clearer depth or edge cases. |
| Scripts | Optional deterministic checks or transforms | Add only when repeatable mechanics justify code. |
| Policy decision | One shared allow/deny judgment | Keep rule logic out of harness-specific adapters. |
| Harness adapter | Translate one tool's payload | Change when a harness interface changes. |
| Capability boundary | Make an action unavailable | Configure outside agent-writable scope. |

Versioned governance documents are intentionally small and retained. Their filenames make
dependencies, authority, and safe insertion points visible to both people and agents.

## Default adoption path

1. Read [`SKILL.md`](SKILL.md), then follow the sole
   [setup and execution workflow](references/RUN-govern-skills-setup-workflow-v1.0.md).
2. Inspect the adopter repository before proposing changes.
3. Reuse compatible local naming, metadata, and directory conventions.
4. Start with documents, templates, and examples only.
5. Show an exact file plan and obtain scoped approval before writing.
6. Run the bundled fictional fixture in an isolated temporary directory.
7. Save the completed mapping, configuration, and setup receipt outside this package.

The package-local standards are deliberately duplicated so a copy of this one directory is
self-contained. The fictional mapping and receipt demonstrate shape only; they are not
defaults or evidence about a real installation.

## Optional layers

Documents can make a repository understandable without making it non-bypassable. Add these
layers only when the adopter selects and authorizes them:

- `instruction-only`: model-readable rules and workflows;
- `static-validator`: deterministic local or CI checks;
- `runtime-guard`: a pre-action hook that can deny a covered request;
- `capability-boundary`: filesystem, network, tool, or credential restrictions; and
- `external-authority`: a protected service that independently verifies approval or
  performs a governed side effect.

One layer never proves another. The existing `skill-governance` plugin in this repository
is optional advanced tooling; it is not required for this copy-and-adapt workflow.

## Package map

- `references/RUN-govern-skills-setup-workflow-v1.0.md` — setup, safe test, receipt, and
  normal governance work.
- `references/REF-governance-adoption-guide-v1.0.md` — inspect-first adoption method and
  readiness reporting.
- `references/STD-*.md` — eight reusable public governance standards.
- `assets/templates/` — blank repository instruction, skill, and configuration templates.
- `assets/output-template.md` — setup-receipt template.
- `examples/fixtures/` — complete fictional mapping and receipt.

Adopted files belong to the adopter repository. Mutable configuration, state, outputs, and
receipts stay outside the installed package.
