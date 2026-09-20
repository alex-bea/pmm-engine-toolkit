# Public Export Manifest

## Approved v1 boundary

This local fresh-history repository contains the 26 standalone skills and one draft
dual-runtime agent plugin listed in `SKILL-CATALOG.md`, Diffguard Lite, shared public standards, reusable
templates, synthetic examples, and tests.
The root governance set covers contributions, conduct, project decisions, security,
support, privacy, licensing, and independent setup.

It also contains the `skill-governance` Codex plugin, its public marketplace entry, and three
self-contained governance skills that can be installed independently from GitHub.

The standalone `skills/govern-skills/` package is the primary low-friction governance
adoption path. A user can give the package to a capable local coding agent and ask it to
inspect a repository, adapt the `SKILL`/`RUN`/`STD`/`REF` pattern to existing conventions,
show an exact file plan, run a synthetic isolated setup, and leave an adopter-owned receipt.
It requires no plugin. Documents are the default layer; registries, validators, CI, hooks,
capability restrictions, external authority, and publishers remain explicit opt-ins.

The repository also contains a complete, agent-neutral competitive-intelligence starter kit
under `skills/comp-intel/`: a working analyst method, fillable source/registry/positioning/
tracker templates, one normal RUN, a conditional `configured-sources` setup contract,
adopter-owned setup configuration and readiness receipt schemas, review gates, a full-depth fictional
embedded-wallet example with one completed counterpart for every human-readable template,
and an optional deterministic controller. The example is a non-reversible structural mirror:
it retains reusable analytical depth but contains no real entity, fact, URL, or alias map. The
setup route uses `ready`, `missing`, `stale`, and `blocked` states; a matching ready receipt
enters normal execution without loading setup detail. The isolated fictional smoke test has no
live source or external side effect. Setup starts with adopter and
competitor homepages, keeps unverified source candidates outside the canonical source map,
requires adopter-positioning approval before comparison, and permits an explicitly limited
baseline. An earlier Draft Codex migration suite under `product-requirements/comp-intel/` is
retained as non-binding design history.

The `marketing-brief` package preserves the full PMM Engine template-fill method: the
canonical seven-section template and limits, detailed source precedence and field ownership,
generic Tier 1–3 launch guidance, multi-launch and edit behavior, and a complete fictional
source packet with its finished brief. It is stateless and directly installable; private
examples were used only to calibrate structure and depth and are not part of the export.

The `pre-read-sharpener` package preserves the complete decision-editing method: supplied-
draft intake, silent diagnosis, blunt review, issue list, line-specific cuts, one constrained
rewrite, an optional decision-call agenda, a ten-line binary quality gate, a three-round
repair ceiling, and collision-safe local persistence. It includes the canonical rewrite
template, package-local evidence and privacy rules, and one independently fictional source
and completed output pair. No qualifying real private completed output was available, and no
private example, source content, registry state, or generated pre-read is part of the export.
Its sole RUN is normal editorial execution. Inline work needs no setup. Optional local
persistence conditionally loads a separate setup contract, maps the adopter's supplied-draft
mode and local output/configuration/receipt destinations, checks local permissions, runs a
bundled fictional fixture in an isolated temporary workspace, and records readiness in an
adopter-owned YAML receipt. A current ready receipt routes directly to normal execution;
missing, stale, or blocked persistence routes to setup. Blank YAML templates and fictional
evidence contain no private defaults, and setup never rewrites the installed package. The
skill has no connector, secret, network, publisher, scheduler, notification, or external
approval dependency.

## Package contract

Every skill includes:

- `SKILL.md` with public trigger metadata and operating instructions;
- `agents/openai.yaml` with user-facing metadata;
- at least one workflow runbook under `references/`;
- `assets/output-template.md` plus any required config/schema templates;
- `examples/EX-synthetic.md` containing fictional data; and
- local scripts when the workflow has deterministic validation or transformation logic.

The repository validator enforces this contract and checks declared local dependencies.

Plugin governance skills additionally include the canonical standards they enforce,
deterministic initializer/audit/fix scripts, installable schemas and templates, and generic
examples with optional PMM profiles. The document audit is read-only and validates only
opted-in Markdown structure and local paths. CI verifies mirrored standards against `docs/`.

The plugin's `govern-skills` package also includes a shared runtime policy decision, thin Claude Code
and Codex PreToolUse adapters, schema-version-2 run control, an external approval-verifier
contract, and a publisher guard. Runtime installation is opt-in and inactive by default.
External verifier and publisher implementations, credentials, enabled adopter policy,
mutable run state, and protected audit records are not part of the public package.

The plugin hook registrations use one `pretooluse.py` entrypoint with an explicit harness
argument. It delegates to the retained Claude Code and Codex normalizers, which preserves
one shared policy decision and direct-adapter compatibility without making the plugin a
standalone-package dependency.

The `plugins/pmm-instinct-review/` `0.3.1` Draft release candidate contains
separate Codex and Claude manifests, marketplace registration for Codex, runtime-specific
plugin-relative hooks, a bundled skill, standard-library Python runtimes, and an isolated
portable review adapter. The Claude surface includes a no-marketplace standalone installer,
bundle-root capture/review/worker commands, an extractor prompt and schema, a detailed setup
runbook, and a complete fictional lifecycle. Native capture stays disabled until explicit
consent. Claude extraction is detached, exact-model, schema-bound, retry-limited, and
tool-disabled. Its background promotion worker acts only on a separate exact-digest human
approval receipt; governed destinations produce review patches rather than direct writes.
Portable mode still requires an explicit adopter-owned root, supports candidate import and
review only, and never reads native agent stores or promotes instructions. The package has no
dependency on a private registry or repository. The retired standalone
`skills/pmm-instinct-review/` package is represented by the plugin's explicit candidate-file
import command.

The `0.3.1` parity slice adds no private registry or model default. Codex first enablement
requires one adopter-selected persisted model, and new capture/backfill jobs use only it.
Adopter-owned `run_routes` name one safe relative RUN; `voice_ref_routes` retains its string
form and may contain an ordered list of safe relative REFs. Route resolution is confined to
independently discovered user-owned skill roots. Multiple eligible targets produce no
applicable preview until the owner supplies one exact `promote --target` choice. Native Claude
and portable behavior remain unchanged; Codex does not inherit Claude's receipt-bound
transaction layer.

Mutable runtime data is never stored inside the installed package. Codex uses its existing
user-owned state root, Claude uses a separate explicit state root, and portable mode requires
an adopter-selected isolated root. Installation receipts, normalized evidence, queue records,
suggestions, review decisions, instincts, promotion previews and receipts, outcomes, logs, and
governed changesets remain local adopter state and are not public export artifacts. The
similarly named files under `examples/` are independently fictional contract fixtures.

## Generalization rules applied

- Existing safe templates were retained, including the PM Prioritizer framework and format.
- Company positioning, customer and employee references, personal profiles, account IDs,
  service-specific configuration, and real operating examples were not copied.
- Integration-dependent workflows now expose config templates and review-first adapter
  boundaries. No connector is required to use the local workflow.
- Global workflows were converted from private runtime state to explicit local input paths.
- Examples use fictional organizations and people and must never be treated as evidence.
- No private chats, native Codex history, runtime configuration, audits, instincts, or
  normalized transcripts are part of the public export.
- No private skill registry, harness permission list, run state, approval event, publisher
  endpoint, credential, or real governance output is part of the runtime-governance export.
- The cross-harness example is independently fictional and uses reserved `.invalid`
  domains; it is not an anonymized private run.
- PMM Instinct Review examples use the fictional Northstar Reports scenario and `.invalid`
  domains. No private-to-fictional crosswalk, private route table, private hook or installer,
  mutable adopter state, machine configuration, or real Codex or Claude session example is
  exported. The published native Claude implementation is independently reviewed generic
  runtime code, not a copy of private evidence or configuration.
- The public Codex model identifier and route values are supplied by each adopter. The
  fictional model/RUN/REF values demonstrate only schema shape and are not defaults, private
  aliases, or evidence about a current installation.
- Competitive-intelligence adopters must map their own internal names, channels, company
  systems, permissions, existing intelligence data, reviewers, and output destinations. The
  package provides blank templates, source-verification and content-access gates, and a fully
  fictional worked example; no live mapping is included or inferred.

## Verification

Run:

```bash
python3 scripts/governance/validate_skill_pack.py
python3 -m unittest discover -s tests
```

Public CI is defined by SHA-pinned, least-privilege workflows under `.github/workflows/`;
its security properties and required checks are documented in [`CI.md`](CI.md).

The repository is licensed under Apache-2.0. The independent all-ref and tracked-tree
secrets scan is recorded in [`security/SECRET-AUDIT-2026-08-18.md`](security/SECRET-AUDIT-2026-08-18.md).
The per-artifact provenance and redistribution review is recorded in
[`legal/IP-RIGHTS-REVIEW-2026-08-18.md`](legal/IP-RIGHTS-REVIEW-2026-08-18.md). Before
creating a public remote, confirm repository name and ownership. Then apply and verify the
versioned branch, Actions, CodeQL, dependency, secret-scanning, and vulnerability-reporting
baseline in
[`security/GITHUB-SECURITY-CONTROLS.md`](security/GITHUB-SECURITY-CONTROLS.md).

The current starter-kit candidate has a Draft
[IP and privacy review](legal/IP-PRIVACY-REVIEW-COMP-INTEL-FRAMEWORK-2026-09-03.md). The
[sanitized example set has its own Draft review](legal/IP-PRIVACY-REVIEW-COMP-INTEL-SANITIZED-EXAMPLE-2026-09-03.md). The
[earlier requirements-suite review](legal/IP-PRIVACY-REVIEW-COMP-INTEL-PRDS-2026-08-28.md)
remains design history. The public starter kit contains only project-authored generic
structures and fictional examples. Live source corpora, adopter mappings, and private outputs
remain outside the public boundary.

The PMM Instinct Review `0.3.1` candidate has separate Draft
[privacy](legal/IP-PRIVACY-REVIEW-PMM-INSTINCT-REVIEW-0.3.1-2026-09-11.md),
[rights](legal/IP-RIGHTS-REVIEW-PMM-INSTINCT-REVIEW-0.3.1-2026-09-11.md), and
[secret-audit](security/SECRET-AUDIT-PMM-INSTINCT-REVIEW-2026-09-11.md) records. Their
80-test Codex/portable suite, 79-test Claude suite, 266-test complete suite, exact 34-path
manifest comparison, 448-artifact inventory regeneration, publicizer scan, and zero-finding
Gitleaks report are complete. PR #17 passed CodeQL, dependency review, governance, and Python
3.10–3.14 checks for implementation commit `90d5177`. The native Codex lifecycle smoke was not
run in this workspace, and project-owner Gate B review remains pending. The candidate is not
merge- or release-ready.

The earlier PMM Instinct Review `0.3.0` candidate retains separate Draft
[privacy](legal/IP-PRIVACY-REVIEW-PMM-INSTINCT-REVIEW-0.3.0-2026-09-10.md),
[rights](legal/IP-RIGHTS-REVIEW-PMM-INSTINCT-REVIEW-0.3.0-2026-09-10.md), and
[secret-audit](security/SECRET-AUDIT-PMM-INSTINCT-REVIEW-2026-09-10.md) records. These
documents describe a locally frozen candidate for review. The complete automated local suite,
strict document audit, exact 57-path manifest comparison, 443-artifact IP inventory, publicizer
scan with unchanged-match adjudication, zero-finding Gitleaks scan, and hosted pull-request
checks are complete. The real Claude lifecycle smoke test and project-owner Gate B review remain
pending, so `0.3.0` was not independently merge- or release-ready. Its completed checks are
historical evidence only and do not approve `0.3.1`.

The earlier PMM Instinct Review `0.2.0` candidate retains its separate Draft
[privacy](legal/IP-PRIVACY-REVIEW-PMM-INSTINCT-REVIEW-0.2.0-2026-09-04.md),
[rights](legal/IP-RIGHTS-REVIEW-PMM-INSTINCT-REVIEW-0.2.0-2026-09-04.md), and
[secret-audit](security/SECRET-AUDIT-PMM-INSTINCT-REVIEW-2026-09-04.md) evidence. Those
documents remain historical evidence for that narrower Codex/portable candidate, not an
approval of `0.3.0`, `0.3.1`, or an approved release.
