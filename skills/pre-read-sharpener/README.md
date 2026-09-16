# Pre-Read Sharpener Starter Guide

## What this skill does

`pre-read-sharpener` turns an existing executive pre-read into a shorter,
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

## First-run setup

The package's sole RUN file is a setup-and-execution wizard. On first use, after a package
change, or when configuration changes, it:

1. verifies the complete installed package and package-relative links;
2. maps whether real drafts arrive by paste, attachment, or authorized local path;
3. confirms the output, configuration, receipt, and temporary test destinations;
4. checks local read and write permissions without storing credential values;
5. runs the bundled fictional fixture in an isolated temporary workspace; and
6. writes a setup receipt with readiness, evidence, limitations, and the normal entrypoint.

Copy [`assets/setup-mapping.md`](assets/setup-mapping.md) to an adopter-owned path such as
`{authorized-workspace}/.pre-read-sharpener/setup.md`. Write the receipt from
[`assets/setup-receipt.md`](assets/setup-receipt.md) under the same adopter-owned workspace.
Never put configuration, receipts, drafts, test results, or generated pre-reads inside the
installed skill package.

Setup uses no connector, network service, secret, publisher, scheduler, or fixed model. The
smoke test disables publishing, messages, notifications, scheduling, approval creation, and
production writes. A passing setup authorizes only the confirmed local workflow.

## How it works

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
6. **Save:** Return the complete result inline and save the same content under the current
   workspace's `outputs/pre-reads/` directory.

The complete setup and operating procedure is in
[`references/RUN-pre-read-sharpener-setup-workflow.md`](references/RUN-pre-read-sharpener-setup-workflow.md).

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

## Saved artifact

The default local path is:

```text
outputs/pre-reads/YYYY-MM-DD-<slug>-pre-read.md
```

The slug comes from the rewrite title, then the input title, then the first eight input
words. A same-day collision uses `-2`, `-3`, and later numeric suffixes rather than
overwriting. A later edit updates the same dated file unless you request a new version.

The path is relative to your authorized working directory, not the installed skill package.
No external service is contacted or modified.

Recommended setup state paths are:

```text
.pre-read-sharpener/setup.md
.pre-read-sharpener/receipts/setup-receipt.md
```

These paths are also relative to the authorized workspace. A receipt becomes stale after a
package revision, required mapping, dependency set, or configuration digest changes.

## Invocation

In Claude Code, Codex, or another compatible agent, ask:

```text
Use $pre-read-sharpener to tighten this draft around the decision.
```

Then provide the draft.

## Fictional example

The example is entirely fictional and is not evidence for a real company or product:

1. Read the fictional
   [`source draft`](examples/fictional-rollout-decision/source-draft.md).
2. Compare it with the
   [`review and rewrite`](examples/fictional-rollout-decision/review-and-rewrite.md).
3. Use the [`behavior cases`](examples/fixtures/behavior-cases.md) to understand edge-case
   handling.
4. Run the fictional
   [`setup smoke test`](examples/fixtures/setup-smoke-test.md) in a temporary workspace before
   supplying a real draft.

## Package map

| File | Purpose |
|---|---|
| `SKILL.md` | Trigger, boundaries, runtime routing, and output contract |
| `references/RUN-pre-read-sharpener-setup-workflow.md` | Installation checks, mappings, safe test, receipt, repair, and complete normal execution |
| `references/REF-decision-ready-criteria.md` | Four anchors and ten binary quality tests |
| `references/REF-evidence-and-privacy.md` | Source, privacy, untrusted-input, and write safeguards |
| `assets/output-template.md` | Canonical tightened-rewrite template |
| `assets/setup-mapping.md` | Blank adopter-owned source, destination, configuration, and permission schema |
| `assets/setup-receipt.md` | Blank setup-readiness receipt and staleness contract |
| `examples/EX-synthetic.md` | Fictional example index and interpretation guidance |
| `examples/fictional-rollout-decision/` | Complete fictional source and output pair |
| `examples/fixtures/behavior-cases.md` | Compact edge-case evaluation inputs and expectations |
| `examples/fixtures/setup-smoke-test.md` | Complete fictional setup map, isolated test procedure, expected artifacts, and receipt |

## Limits

- No research, browsing, retrieval, or fact-checking.
- No invented facts, metrics, dates, people, claims, options, or consensus.
- No synthesis across multiple source documents.
- No from-scratch pre-read generation.
- No external publishing, messaging, scheduling, or service mutation.
- No adopter draft or generated output is stored inside the installed package.

The public template is faithful to the written golden workflow. No qualifying real private
completed output was available; the worked example is independently fictional and should be
used only as formatting and behavior guidance.
