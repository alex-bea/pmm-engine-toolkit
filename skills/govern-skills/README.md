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

| Primitive | Job | Typical update point |
|---|---|---|
| `SKILL.md` | Discovery, routing, and durable boundaries | Change when the job or trigger changes. |
| `RUN-*.md` | Ordered normal workflow | Insert or change an operating step here. |
| `STD-*.md` | Stable rules shared across decisions | Change only when the rule itself changes. |
| `REF-*.md` | Focused setup or mode guidance | Add knowledge without bloating the entrypoint. |
| Templates | Blank structures copied and adapted | Change when an artifact contract changes. |
| Examples | Fictional completed demonstrations | Change when users need clearer depth or edge cases. |
| Scripts | Optional deterministic checks or transforms | Add only when repeatable mechanics justify code. |
| Policy decision | One shared allow/deny judgment | Keep rule logic out of harness-specific adapters. |
| Harness adapter | Translate one tool's payload | Change when a harness interface changes. |
| Capability boundary | Make an action unavailable | Configure outside agent-writable scope. |

Versioned governance documents are intentionally small and retained. Their filenames make
dependencies, authority, and safe insertion points visible to both people and agents.

## Setup

The setup profile is `local-persistence`. It stores a completed configuration and a compact
readiness receipt in the adopter's authorized workspace, outside the installed package.
Unless an existing compatible convention governs those files, use:

- `.agents/govern-skills/setup-config.yaml` for the completed mapping; and
- `.agents/govern-skills/setup-receipt.yaml` for the current readiness record.

For explicit setup, install, configure, verify, diagnose, or repair requests—and whenever
the receipt is missing, stale, or blocked—follow the
[`setup contract`](references/REF-govern-skills-setup-contract.md). Begin with the blank
[`setup configuration`](assets/setup-config.yaml) and
[`setup receipt`](assets/setup-receipt.yaml). Run the
[`fictional smoke test`](examples/fixtures/setup-smoke-test.md) in an isolated temporary
directory and compare the generated state with the fictional
[`configuration`](examples/fixtures/setup-config.yaml) and
[`receipt`](examples/fixtures/setup-receipt.yaml).

A receipt is `ready` only for its named scope. It is stale when the package revision or
digest, setup-contract version, required mapping, selected enforcement layer, dependency
set, or configuration digest changes. Dates are audit evidence only; there is no
time-to-live. Repair only the affected scope, rerun its checks, and write a new receipt.

The YAML receipt is the stable machine-readable readiness record. The existing
[`detailed receipt template`](assets/output-template.md) and fictional Markdown receipt are
optional human-readable evidence reports, not substitutes for the YAML readiness record.

## Normal use

With a matching `ready` receipt, follow the sole normal
[`governance workflow`](references/RUN-govern-skills-workflow-v1.1.md). Normal audit or
maintenance work should not load the setup contract. The usual sequence is:

1. inspect the repository and controlling instructions;
2. choose one governance mode;
3. load only the relevant standards;
4. report evidence and an exact proposed boundary;
5. obtain scoped approval before writes; and
6. run focused verification and report limitations.

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

- `references/RUN-govern-skills-workflow-v1.1.md` — normal governance work.
- `references/REF-govern-skills-setup-contract.md` — setup, readiness, safe test, receipt,
  and repair contract.
- `references/REF-governance-adoption-guide-v1.0.md` — inspect-first adoption method.
- `references/STD-*.md` — eight reusable public governance standards.
- `assets/setup-config.yaml` and `assets/setup-receipt.yaml` — blank setup-state contracts.
- `assets/templates/` — blank repository instruction, skill, and governance templates.
- `assets/output-template.md` — optional detailed human-readable receipt.
- `examples/fixtures/` — complete fictional mapping, setup state, smoke test, and receipt.

Adopted files belong to the adopter repository. Mutable configuration, state, outputs, and
receipts stay outside the installed package.
