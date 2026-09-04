---
doc_type: STD
normative: true
requires:
  - STD-skill-structure-v1.0.md
  - STD-governance-document-metadata-v1.0.md
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Codex users
  - skill maintainers
change_control: Pull request review
---

# AI Skill Governance Standard

## Purpose and authority

Keep skill packages consistent, reviewable, safe, portable, and independently installable.
This standard owns skill registration, lifecycle, ownership, activation, deprecation,
approval boundaries, and truthful enforcement claims. The skill-structure standard owns the
files inside a skill package. The runtime-enforcement standard owns technical controls across
harnesses.

## Registry

Every governed skill must have exactly one entry in
`.agents/governance/skill-registry.yaml`. The registry is the source of truth for:

- `name`: the lowercase kebab-case skill name;
- `folder`: the repository-relative package path;
- `version`: the governed contract version;
- `owner`: one accountable person or role;
- `status`: `draft`, `active`, `deprecated`, or `archived`; and
- `replacement`: the successor skill name when status is `deprecated`.

An unregistered folder is not an active governed skill. Generated catalogs are views and
must never override the registry.

## Lifecycle

| Status | Meaning | Execution rule |
|---|---|---|
| `draft` | Being built or evaluated | Manual testing only with user authorization |
| `active` | Registered, tested, and supported | May be used for authorized work |
| `deprecated` | Replaced or being retired | Do not use for new work; name a replacement |
| `archived` | Removed from live skill roots | Retain only for history or migration |

Activate a skill only after its package validates, deterministic scripts pass tests, a
synthetic end-to-end example has been exercised, and the owner approves activation.

## Change rules

- Review changes to behavior, inputs, outputs, permissions, dependencies, or references.
- Increment the governed version when the contract changes materially.
- Treat removed fields, removed steps, renamed interfaces, and incompatible output changes
  as breaking changes.
- Keep source material traceable. Mark missing facts instead of inventing them.
- Never silently add, remove, or weaken an approval gate.
- Preserve old versions or provide a migration path when compatibility breaks.

## Agent authority

An agent may inspect files and produce an advisory audit without approval. It must show the
intended paths and changes, then obtain explicit approval before initializing governance,
applying fixes, changing lifecycle state, publishing, performing an external write, or
taking a destructive action. Approval for one action does not authorize a broader action.

Conversational approval is sufficient only for the scoped local write the user controls.
Approval that authorizes a protected workflow transition or publication must be established
by the configured external authority and bind the authorized human, reviewed revision,
artifact path, artifact digest, decision, and time. A caller-supplied name or well-formed URL
is evidence to verify, not proof.

Scheduled workers may collect declared staging evidence. They may not create approval,
advance a human-review gate, enter a publish-ready stage, or publish.

## Enforcement claims

Classify every material rule as `instruction-only`, `static-validator`, `runtime-guard`,
`capability-boundary`, or `external-authority`. Never claim that a rule is enforced merely
because a model loaded it, a validator passed, or one hook can be bypassed through another
available tool.

Claude Code and Codex adapters use one shared policy decision. Strong enforcement also
requires protected policy and state, restricted shell and network routes, independent
approval verification, and publisher credentials unavailable to the agent. See
`STD-runtime-enforcement-v1.0.md`.

## Privacy and IP

- Never commit credentials, private URLs, internal identifiers, personal data, customer
  data, or unlicensed third-party content.
- Use generic templates in reusable packages and synthetic examples.
- Provide sensitive context only at runtime from an authorized user.
- Do not impersonate a person or use a voice profile without consent.

## Validation

Before release, confirm registry and folder agreement, required files, dependency closure,
metadata, lifecycle state, synthetic examples, tests, and public-safety rules. When runtime
controls are included, also test harness parity, scheduled restrictions, stale digests,
forged approval, verifier outage, direct publisher calls, and alternate paths. Advisory
findings are the default for local adoption. Blocking CI and runtime enforcement are
separate explicit opt-ins.
