# Pre-Read Sharpener Workflow

## Purpose

Tighten one supplied executive pre-read into a direct review and a decision-ready rewrite.
Operate only on the source the user provides. Do not research, retrieve, combine other
documents, fact-check, or invent facts. Mark missing decision-critical information
`[Missing]`.

## Step 0 — Accept input

Accept a pasted draft, attached text, or an authorized local path to one pre-read.

If no draft is provided, ask: “Paste, attach, or identify the pre-read draft you want me to
sharpen.” Stop without creating an output.

If the input is clearly not an executive or leadership pre-read, explain the mismatch and
ask the user to confirm the intended transformation. Do not proceed or save a file until the
user confirms.

## Step 1 — Load package rules silently

Read, in order:

1. `../assets/output-template.md` for the exact rewrite structure and limits;
2. `REF-decision-ready-criteria.md` for the binary quality gate; and
3. `REF-evidence-and-privacy.md` for source, privacy, and write boundaries.

Use the fictional example only for format and depth. Never use it as evidence. Do not print
this loading step.

## Step 2 — Diagnose silently

Identify and record:

1. the single decision the meeting should produce;
2. the audience, using named roles rather than a generic group;
3. the one recommended option;
4. what the recommendation gives up and what rejection gives up;
5. the cost to reverse each option when the source provides it;
6. the concrete outcome if the meeting says yes;
7. any decision-blocking open question;
8. clarity gaps, logic gaps, and repetition; and
9. hedges, consultant language, throat-clearing, passive constructions, and abstract claims
   that should be cut.

If the source omits a decision-critical item, record `[Missing]`. Do not infer or invent it.

## Step 3 — Produce the review and rewrite

Return the following components in this exact order.

### 3.1 Blunt PM review

Write one paragraph of at most 150 words. State what the draft is trying to accomplish,
where it fails, and the single biggest issue. Be direct without becoming insulting.

### 3.2 Biggest issues

Write three to six bullets. Each bullet is at most 20 words and covers one clarity, logic,
evidence, tradeoff, or repetition problem.

### 3.3 Specific cuts

For each cut, quote or briefly paraphrase the relevant source line, then give a cut or move
instruction of at most ten words. Use five to fifteen cuts when the source length supports
that range; use fewer only when the draft does not contain five distinct cut candidates.

### 3.4 Tightened rewrite

Fill `../assets/output-template.md` exactly. Use only supplied facts. Keep the complete
rewrite at most 600 words and preserve the source's material constraints and uncertainty.

### 3.5 Suggested agenda

When the source is for a decision call, add:

- exactly four agenda bullets, each at most ten words; and
- one sentence labeled `Deciding question` that names the single question the meeting must
  answer.

When the document is informational rather than decision-oriented, omit the agenda and state
before the rewrite that the decision-call agenda does not apply. If the document type was
unclear at intake, obtain confirmation in Step 0 before using this path.

## Step 4 — Run the decision-ready self-check

Score only the tightened rewrite from Step 3.4 against every line of
`REF-decision-ready-criteria.md`. Append this table after the rewrite and applicable agenda:

| Criterion | Pass / Fail | Why |
|---|---|---|

Every row is binary. Partial credit is a failure.

If any row fails:

1. revise the rewrite without adding unsupported facts;
2. rescore all ten criteria;
3. repeat for no more than three revision rounds; and
4. if any row still fails after round three, name each blocking criterion and the exact
   source gap, then ask whether the user wants the failing draft returned anyway.

Do not silently return a failing rewrite or label a missing fact as passing. The quality gate
does not authorize invention. When the source is too thin, `[Missing]` and an honest failure
are preferable to fabricated specificity.

## Step 5 — Persist a passing deliverable

After every criterion passes, write the complete Step 3 and Step 4 result to:

```text
outputs/pre-reads/YYYY-MM-DD-<slug>-pre-read.md
```

The path is relative to the user's authorized workspace, never the installed skill package.
Create `outputs/pre-reads/` when absent.

Derive the lowercase kebab-case slug from no more than eight words, in this order:

1. the first H1 in the tightened rewrite;
2. the first H1 in the input draft; or
3. the first eight words of the input draft.

If the path already exists for that date and slug, append `-2`, `-3`, or the next available
integer before `.md`. Never overwrite an existing same-day result during initial execution.

If the authorized workspace is not writable, return the passing inline deliverable and
report the persistence failure. Do not silently choose another destination.

## Step 6 — Return

Put the written path on the first line, then return the same complete content inline. Add no
introductory preamble or task list.

## Edit handling

When the user requests an edit after a result:

1. change the requested content and any fields that must change for consistency;
2. preserve the canonical rewrite structure unless the user explicitly changes the
   template;
3. rerun the full ten-criterion self-check;
4. surface any new failure and follow the three-round limit;
5. update the same dated file unless the user explicitly requests a new version; and
6. return the complete revised deliverable, not only the edited fragment.

## Error handling

| Situation | Action |
|---|---|
| No draft | Ask for the draft and stop without writing. |
| Input is clearly not a pre-read | Confirm intent before rewriting or writing. |
| Source is too thin | Fill supported fields, mark decision-critical gaps `[Missing]`, and apply the quality gate honestly. |
| Research or fact-checking requested | Explain that this skill uses only the supplied draft. |
| User asks to invent or assume facts | Decline and request source support. |
| User asks to skip the self-check | Explain that the binary gate is part of the skill contract. |
| A criterion still fails after three rounds | Name the blocker and ask before returning the failing draft. |
| Output directory is absent | Create it in the authorized workspace. |
| Initial output path exists | Use the next numeric suffix; do not overwrite. |
| Workspace is not writable | Return inline and report the persistence failure; do not write elsewhere. |
| External save or publication requested | Treat it as a separate target-specific request; this workflow does not authorize it. |
