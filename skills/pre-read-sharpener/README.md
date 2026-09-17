# Pre-Read Sharpener Starter Guide

## What this skill does

`pre-read-sharpener` turns one existing executive pre-read into a shorter,
decision-oriented document. It returns a direct editorial review, specific cuts, a
constrained rewrite, and, for a decision call, a compact meeting agenda.

The skill uses only the draft you supply. It does not research missing facts, combine
unrelated documents, invent evidence, or create a pre-read from scratch.

## What to provide

Paste, attach, or identify one pre-read that the agent is authorized to read. A useful draft
normally contains:

1. the audience for the decision;
2. the single decision the meeting should produce;
3. the recommended option;
4. the material alternatives and tradeoffs;
5. evidence supporting the recommendation; and
6. what changes if the recommendation is approved.

Missing decision-critical information is marked `[Missing]`. The skill never fills a gap
from general knowledge or the fictional example.

## Normal use

Choose one output route:

- **Inline:** The result is returned in the response. No installation setup, configuration,
  or receipt is required.
- **Persistent local output:** The result is also written beneath the configured
  `outputs/pre-reads/` destination. This route requires a current `ready` receipt.

Normal editorial work follows
[`references/RUN-pre-read-sharpener-workflow.md`](references/RUN-pre-read-sharpener-workflow.md).
A ready persistence route enters that RUN without loading setup detail or rerunning the
fixture.

## Setup

Setup is conditional because the package uses the `local-persistence` profile. Run setup
only when you explicitly want to configure, verify, diagnose, or repair the installation,
or when persistent output reports `missing`, `stale`, or `blocked` readiness.

Detailed setup rules are in
[`references/REF-pre-read-sharpener-setup-contract.md`](references/REF-pre-read-sharpener-setup-contract.md).
Copy the blank schemas to adopter-owned paths outside the installed package:

```text
{authorized-workspace}/.pmm-skills/pre-read-sharpener/setup-config.yaml
{authorized-workspace}/.pmm-skills/pre-read-sharpener/setup-receipt.yaml
```

Use [`assets/setup-config.yaml`](assets/setup-config.yaml) for source and output destination
mapping and [`assets/setup-receipt.yaml`](assets/setup-receipt.yaml) for readiness evidence.
Never edit those installed templates in place.

Setup verifies package closure and links, confirms local input/output paths and permissions,
and runs the bundled
[`fictional setup smoke test`](examples/fixtures/setup-smoke-test.md) in a separate temporary
workspace. The test disables publishing, messaging, notifications, scheduling, approval
creation, network mutation, and production writes. It must leave the copied installation
unchanged.

Receipt states mean:

- `ready`: persistent output may enter the normal RUN directly;
- `missing`: no receipt exists at the stable path;
- `stale`: a bound package, setup-contract, mapping, dependency, or configuration digest
  changed; and
- `blocked`: a required current check failed or is unavailable.

Dates are audit evidence and do not make a receipt stale. Reconfigure only affected checks,
show differences before changing an existing file, preserve generated pre-reads, and never
delete or rewrite the installed package to mark setup complete.

## How normal execution works

1. **Accept the draft:** Stop and request it when no draft is supplied. Confirm intent when
   the source is clearly not a pre-read.
2. **Diagnose:** Identify the audience, decision, recommendation, tradeoffs, outcome, logic
   gaps, repetition, hedging, and throat-clearing.
3. **Review and rewrite:** Return a blunt review, biggest issues, specific cuts, and the
   rewritten pre-read using the fixed template.
4. **Prepare the meeting:** For a decision call, add a four-item agenda and one deciding
   question.
5. **Self-check:** Score all ten decision-ready criteria. Revise failures up to three times;
   ask before returning a result that still fails.
6. **Persist when configured:** Return every result inline. On a ready persistence route,
   also save the same content beneath the configured `outputs/pre-reads/` directory.

## What you receive

The tightened rewrite follows
[`assets/output-template.md`](assets/output-template.md). It surfaces the audience,
decision, recommendation, three-point summary, options, tradeoffs, reversal cost, concrete
outcome, and any blocking questions. The rewrite is at most 600 words.

The full deliverable also contains:

- a blunt PM review of at most 150 words;
- three to six concise issues;
- line-specific cut recommendations;
- a decision-call agenda when applicable; and
- a ten-row pass/fail self-check.

## Persistent artifact

The default configured pattern is:

```text
outputs/pre-reads/YYYY-MM-DD-<slug>-pre-read.md
```

The slug comes from the rewrite title, then the input title, then the first eight input
words. A same-day collision uses `-2`, `-3`, and later numeric suffixes rather than
overwriting. A later edit updates the same dated file unless you request a new version.

If the configured destination becomes unwritable, the skill still returns the complete
inline result and reports the persistence failure. It does not choose another path.

## Invocation

In Claude Code, Codex, or another compatible agent, ask:

```text
Use $pre-read-sharpener to tighten this draft around the decision.
```

Then provide the draft and say whether you want inline-only or persistent local output.

## Fictional example

The example is entirely fictional and is not evidence for a real company or product:

1. Read the fictional
   [`source draft`](examples/fictional-rollout-decision/source-draft.md).
2. Compare it with the
   [`review and rewrite`](examples/fictional-rollout-decision/review-and-rewrite.md).
3. Use the [`behavior cases`](examples/fixtures/behavior-cases.md) to understand editorial
   and routing edge cases.
4. Use the [`setup smoke test`](examples/fixtures/setup-smoke-test.md) only when verifying
   persistent local output.

## Package map

| File | Purpose |
|---|---|
| `SKILL.md` | Trigger, boundaries, conditional router, and output contract |
| `references/RUN-pre-read-sharpener-workflow.md` | Sole normal editorial workflow |
| `references/REF-pre-read-sharpener-setup-contract.md` | Conditionally loaded setup, mappings, test, receipt, and repair rules |
| `references/REF-decision-ready-criteria.md` | Four anchors and ten binary quality tests |
| `references/REF-evidence-and-privacy.md` | Source, privacy, untrusted-input, and write safeguards |
| `assets/output-template.md` | Canonical tightened-rewrite template |
| `assets/setup-config.yaml` | Blank adopter-owned source and destination configuration schema |
| `assets/setup-receipt.yaml` | Blank setup-readiness receipt schema |
| `examples/EX-synthetic.md` | Fictional example index and interpretation guidance |
| `examples/fictional-rollout-decision/` | Complete fictional source and output pair |
| `examples/fixtures/behavior-cases.md` | Compact editorial and routing edge cases |
| `examples/fixtures/setup-smoke-test.md` | Complete fictional conditional-setup test |

## Limits

- No research, browsing, retrieval, or fact-checking.
- No invented facts, metrics, dates, people, claims, options, or consensus.
- No synthesis across multiple source documents.
- No from-scratch pre-read generation.
- No external publishing, messaging, scheduling, or service mutation.
- No adopter configuration, receipt, draft, or generated output is stored inside the
  installed package.

The public template is faithful to the written golden workflow. No qualifying real private
completed output was available; the worked example is independently fictional and should be
used only as formatting and behavior guidance.
