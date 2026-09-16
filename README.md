# PMM Engine Toolkit

A portable, public-safe PMM operating toolkit for planning work, producing evidence-bound
marketing artifacts, synthesizing signals, and maintaining repository hygiene:

- **26 standalone agent skills** — the approved v1 set across planning, execution,
  intelligence, drafting, signal operations, and repository hygiene.
- **PMM Instinct Review plugin (`0.3.1` draft)** — a self-contained, human-gated
  improvement loop with native local capture and background extraction for Codex and
  Claude Code, plus explicit portable candidate review.
- **Diffguard Lite** — a local Git-diff analyzer for Python and JavaScript complexity,
  file size, churn, and test health.
- **Standards and templates** — public skill structure, evidence/privacy, approval-gate,
  tracker, and dependency-closure rules with reusable formats and synthetic examples.
- **Govern Skills copy pattern** — a self-contained, documents-first package that a local
  coding agent can inspect and adapt without installing a plugin.
- **Skill governance plugin** — approval-gated initialization, advisory audits, safe
  mechanical fixes, optional blocking CI, and optional Claude Code/Codex runtime guards
  backed by external approval and publisher boundaries.

This repository deliberately contains no customer data, operating outputs, private source
registries, account identifiers, credentials, or private Git history. Integrations are
represented by local config templates and adapter contracts only.

The writing skills intentionally use generic templates. Supply your own approved claims
guide, positioning, examples, legal review, and consented voice profile rather than relying
on embedded company, customer, or individual data.

## Quick start

Requirements: Git and Python 3.10 or newer.

```bash
git clone https://github.com/alex-bea/pmm-engine-toolkit.git
cd pmm-engine-toolkit
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r requirements-build.lock
.venv/bin/python -m pip install --require-hashes --no-build-isolation -r requirements.lock
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/governance/validate_skill_pack.py
```

The `requirements*.txt` files are human-maintained source manifests. Their corresponding
lock files provide the hash-verified installation used by CI and recommended for local
setup. Build tooling is installed first so the one source-only runtime package can build
without fetching undeclared build dependencies.

These commands validate the complete Toolkit source tree, so they are the right starting
point for contributors and people changing a package. To evaluate one standalone workflow,
start with its catalog entry and package documentation instead.

## Choose a starting point

| If you want to… | Start here |
| --- | --- |
| Find a workflow for a PMM job | Browse the [skill catalog](docs/SKILL-CATALOG.md), then read the selected package's `SKILL.md` and any package README. |
| Use one standalone skill | Copy its complete `skills/<name>/` directory into a compatible agent environment, keeping its subdirectories together. The [competitive-intelligence starter kit](skills/comp-intel/README.md) shows the pattern. |
| Evaluate the PMM Instinct Review candidate | Read the evaluation notice and setup guidance in the next section before installing or enabling anything. |
| Copy a governance pattern into a repository | Give your local agent the [standalone Govern Skills package](skills/govern-skills/README.md) and use its copy prompt. No plugin is required. |
| Add optional governance automation | After documents-first adoption, evaluate the [Codex governance plugin](docs/CODEX-GOVERNANCE-PLUGIN.md) for validators, hooks, and advanced controls. |
| Contribute a change | Follow [CONTRIBUTING.md](CONTRIBUTING.md) and the [continuous-integration guide](docs/CI.md). |

Run Diffguard Lite against a Git base ref:

```bash
.venv/bin/python scripts/governance/diffguard_lite.py --base origin/main
```

Each skill is self-contained under `skills/<name>/` except for explicitly linked shared
standards in `docs/`. Run `python3 scripts/governance/validate_skill_pack.py` to verify
the selected inventory, required resources, local links, frontmatter, and public-safety
guardrails.

## PMM Instinct Review plugin (`0.3.1` draft)

> **Draft / evaluation only.** The `0.3.1` local Codex model/routing checks and security scans
> are complete, and the hosted checks passed on PR #17 for implementation commit `90d5177`.
> The native Codex lifecycle smoke was not run, and project-owner Gate B review remains
> pending. Do not treat `0.3.1` as a production-ready release. The completed `0.3.0` evidence
> remains historical and does not approve this candidate.

The plugin supports two independent native runtimes: the existing Codex plugin and a standalone
Claude Code bundle. Fresh installation does not enable chat capture in either runtime. Before
enabling capture, inspect the relevant hooks, confirm that local transcript-derived storage and
a second model invocation are allowed on the machine, and explicitly acknowledge the privacy
boundary through `$pmm-instinct-review` in Codex or `/pmm-instinct-review` in Claude Code.
Codex also requires one non-empty adopter-selected extractor model to be persisted before
capture becomes enabled; event metadata is not a model fallback.

Install for Codex through the public marketplace:

```bash
codex plugin marketplace add alex-bea/pmm-engine-toolkit --ref main
codex plugin add pmm-instinct-review@pmm-engine-toolkit
```

After installation, inspect status and enable Codex capture only with an exact model (or reuse
one already persisted in the user-owned store):

```bash
python3 plugins/pmm-instinct-review/skills/pmm-instinct-review/scripts/instinct_review.py status
python3 plugins/pmm-instinct-review/skills/pmm-instinct-review/scripts/instinct_review.py \
  on --acknowledge-local-chat-storage --model <exact-model>
```

Adopters may configure safe relative `run_routes` and string-or-list `voice_ref_routes` in
their own Codex state. If several validated RUN or REF files remain, the preview returns exact
`eligible_targets` and requires `promote --target`; it never chooses the first file.

If `codex` is not on `PATH` on macOS, use either installed app binary:

```bash
"/Applications/ChatGPT.app/Contents/Resources/codex" plugin marketplace add alex-bea/pmm-engine-toolkit --ref main
"/Applications/ChatGPT.app/Contents/Resources/codex" plugin add pmm-instinct-review@pmm-engine-toolkit
```

The equivalent Codex app binary path is
`/Applications/Codex.app/Contents/Resources/codex`.

For Claude Code, clone or copy this repository to the destination machine and begin with the
non-mutating installer preflight. Before any installation or enablement, confirm that the
machine can use the required authenticated Claude CLI or supported provider credentials and
that its local-storage and model-processing policies permit evaluation.

```bash
python3 plugins/pmm-instinct-review/scripts/install_claude_instinct_review.py \
  --check
```

If the preflight is acceptable and you choose to evaluate the candidate, install one mode.
Copy mode leaves a durable bundle under the user's Claude directory; neither mode requires a
Claude marketplace:

```bash
python3 plugins/pmm-instinct-review/scripts/install_claude_instinct_review.py \
  --install --mode symlink
# Or create a pinned copy:
python3 plugins/pmm-instinct-review/scripts/install_claude_instinct_review.py \
  --install --mode copy
```

The installer adds only the `pmm-instinct-review` personal skill and its owned
`SessionStart` and `SessionEnd` handlers, preserving unrelated Claude settings. Native state
is isolated by runtime: Codex uses `~/.codex/instinct-review/`, while Claude uses
`~/.claude/pmm-instinct-review-data/`. Disabling or uninstalling preserves that user-owned
state. The package has no telemetry or hosted PMM service and never changes native session
history.

Read the [operator guide](plugins/pmm-instinct-review/README.md), the
[detailed Claude setup runbook](plugins/pmm-instinct-review/skills/pmm-instinct-review/references/RUN-claude-setup.md),
and the [privacy policy](PRIVACY.md) before enabling it on a work device. A local-plugin
Claude launch is also available for temporary evaluation; it is separate from the persistent
standalone installation described above.

## Skill authoring

The included [skill catalog](docs/SKILL-CATALOG.md), [skill-structure standard](docs/STD-skill-structure-v1.0.md),
and [format templates](docs/templates/) are the public reference set for extending this
toolkit without copying private operating context.

The [competitive-intelligence starter kit](skills/comp-intel/README.md) publishes the reusable
framework of a mature working practice: source mapping, collection logic, evidence standards,
competitor registries, positioning and narrative analysis, gap trackers, executive briefing,
review gates, and a complete fictional example. Its guided first run turns a product website
and competitor homepages into a verified source map, reviewed adopter positioning, and a
clearly scoped baseline with about 30 minutes of PMM input. Copy the skill into Claude Code,
Codex, or another compatible agent environment and use the sources you authorize. See the
[first-run onboarding procedure](skills/comp-intel/references/RUN-onboarding.md).

The document-led workflow is the default. An optional standard-library controller adds
synthetic/local-file adapters, deterministic evidence manifests, digest-bound review records,
and guarded local-state apply for teams that need machine-enforced controls:

```bash
python3 skills/comp-intel/scripts/comp_intel.py init --data-root ./comp-intel-data
python3 skills/comp-intel/scripts/comp_intel.py doctor --data-root ./comp-intel-data --market synthetic-devtools
python3 skills/comp-intel/scripts/comp_intel.py collect --data-root ./comp-intel-data --market synthetic-devtools --from 2026-08-18 --to 2026-08-26
```

Every controller collection intentionally stops at evidence review; later controller steps
require two digest-bound review records. The guided workflow does not require bundled web,
repository, or communication adapters: adopters use the source tools already available in
their agent environment and record the resulting evidence using the shipped contract.

The earlier [Codex migration requirements](docs/product-requirements/comp-intel/README.md) are
retained as non-binding design history.

To copy the repository's skill-governance architecture without installing anything, open the
[Govern Skills package](skills/govern-skills/README.md) and give its prompt to Claude Code,
Codex, or another capable local coding agent. The agent first inventories the target
repository, adapts the `SKILL`/`RUN`/`STD`/`REF` pattern to existing conventions, proposes
exact files, and runs a fictional isolated setup test. Documents are the default scope;
registries, validators, CI, hooks, capability restrictions, external approval, and
publishers remain separate optional layers.

See the [public export manifest](docs/PUBLIC-EXPORT-MANIFEST.md) for the exact package
contract, generalization rules, and pre-publication gates.

## Optional Codex governance plugin

The standalone [Govern Skills copy pattern](skills/govern-skills/README.md) is the simplest
adoption path. The plugin is optional advanced tooling for repositories that also want its
initializer, audits, work tracker, or separately activated runtime guard.

Install the public marketplace and plugin:

```bash
codex plugin marketplace add alex-bea/pmm-engine-toolkit --ref main
codex plugin add skill-governance@pmm-engine-toolkit
```

The three plugin skills can also be installed independently from their GitHub directories
with Codex's built-in `$skill-installer`. See the complete
[installation and adoption guide](docs/CODEX-GOVERNANCE-PLUGIN.md), including the
[document-governance baseline](docs/CODEX-DOCUMENT-GOVERNANCE.md).

Runtime controls install disabled and are separate from the advisory audit. A hook alone is
not a complete security boundary: strong enforcement also requires administrator-protected
policy, restricted shell/network and tool paths, independently verified digest-bound human
approval, protected CI, and publisher credentials unavailable to the agent.

## Community and governance

- [Contributing](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Project governance](GOVERNANCE.md)
- [Security policy](SECURITY.md)
- [Support policy](SUPPORT.md)
- [Privacy policy](PRIVACY.md)
- [Continuous integration](docs/CI.md)

## License

Copyright 2026 Alexander Bea.

Licensed under the [Apache License 2.0](LICENSE).
See the repository [notice](NOTICE), [third-party notices](THIRD_PARTY_NOTICES.md), and
[IP-rights review](docs/legal/IP-RIGHTS-REVIEW-2026-08-18.md) for attribution and
redistribution details. Third-party product names are used nominatively; no affiliation or
endorsement is claimed.
