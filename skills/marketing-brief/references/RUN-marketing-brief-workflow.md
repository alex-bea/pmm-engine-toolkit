# Marketing Brief Workflow

## Purpose

Fill the canonical marketing brief from source material supplied or explicitly authorized by
the user. This is a template-fill workflow. Do not conduct research, synthesize unsupported
strategy, or invent facts. Use `[Missing]` for unsupported required information.

## Step 0 — Accept input

Accept any combination of:

- final PRDs or approved product specifications;
- approved launch plans or campaign briefs;
- approved product, PMM, or go-to-market strategy;
- approved messaging or positioning;
- launch-tier guidance;
- customer, partner, or sales notes tied to the launch;
- meeting notes, brainstorm documents, or chat summaries;
- optional adopter-approved terminology guidance.

If no source material is provided, ask the user to paste, attach, or identify the launch
material and stop. Do not search for it.

Scan the input for distinct launches. If more than one is present, tell the user how many
separate launches you found and process each independently through this workflow.

## Step 1 — Load the package rules silently

Read, in order:

1. `../assets/output-template.md` for the exact section order, fields, limits, and writing
   rules;
2. `REF-source-priority.md` for source ownership and conflict resolution;
3. `REF-launch-tiers.md` for tier classification;
4. `REF-evidence-and-privacy.md` for evidence and privacy boundaries.

Do not print the loading step.

## Step 2 — Analyze the supplied material silently

### 2.1 Separate launches

Keep different launches separate even when they share a product, audience, date, or campaign.
Never combine unrelated changes to make a source set look complete.

### 2.2 Classify the launch tier

Use `REF-launch-tiers.md`:

- Tier 1 for a market-expanding or business-critical launch with broad audience impact,
  high complexity, or major investment;
- Tier 2 for a meaningful feature, segment expansion, or awareness launch with moderate
  complexity and several channels;
- Tier 3 for a small update or visibility moment with low complexity and one or two channels.

Use an explicitly approved tier when the source provides one. Otherwise apply the framework.
If classification remains ambiguous, default to Tier 2.

### 2.3 Resolve source conflicts

Apply `REF-source-priority.md` field by field. Do not merge conflicting claims. Use the
highest-priority source that directly owns the field. If the hierarchy does not resolve a
required fact, write `[Missing]`.

### 2.4 Identify missing fields

Check every field in `../assets/output-template.md`. Use only facts supplied for that launch.
Mark unsupported required fields `[Missing]`. Omit an optional field only when the template
allows it. Do not fill a gap through general knowledge or the fictional example.

## Step 3 — Fill the template

Follow the exact seven-section order and all limits in `../assets/output-template.md`.

### Section 1 — Brief Info

- Keep each field to eight words or fewer.
- Write a launch name of six words or fewer that describes the user outcome, not the
  implementation mechanism.
- Keep strategy and messaging out of this section.

### Section 2 — Launch Summary

- Use no more than 50 words in two or three sentences.
- State what users experience differently, who is affected, and what changed.

### Section 3 — Audience and Problem

- Keep primary and secondary audiences to five words each.
- Keep Core Problem and Why Now to 18 words each.
- Name one core problem and keep each line distinct.

### Section 4 — Launch Scope and Value

- Keep Scope to 20 words and Customer Value to 18 words.
- Keep each proof point to 10 words.
- Use facts, focus on this launch, and write value in customer language.

### Section 5 — Messaging

- Keep the topline message to 15 words.
- Keep each support point to 10 words and the CTA to eight words.
- Keep support points distinct and do not repeat proof points word for word.

### Section 6 — Distribution

- Name channel categories, not tasks.
- Keep detailed execution in the adopter's project-management system.

### Section 7 — Success

- Use one to three measurable goals tied to this launch.
- Keep each goal to 10 words.

Apply optional adopter-approved terminology exactly. Otherwise use plain, generic language.

## Step 4 — Return output

Return the final brief only. Do not add a preamble, commentary, task list, or execution
checklist. Return separate complete briefs with clear separators when the input contains
multiple launches.

Do not save a file unless the user separately asks for and authorizes a local path. Never
publish, message, schedule, or mutate an external system.

## Edit handling

When the user requests an edit:

1. change only the requested content unless consistency requires a clearly related update;
2. preserve the canonical structure unless the user explicitly asks to change the template;
3. recheck all field and section limits; and
4. return the full updated brief, not only the edited fragment.

## Error handling

| Situation | Action |
|---|---|
| No source material | Ask for a PRD, launch document, or notes and stop. |
| Material is too vague to fill most fields | Fill supported fields and mark unsupported required fields `[Missing]`. |
| Sources conflict | Apply field ownership and priority; never blend conflicting claims. |
| A required conflict remains unresolved | Use `[Missing]` and preserve the uncertainty. |
| Multiple launches appear in one input | Report the count and create one brief per launch. |
| User asks for web research or retrieval | Explain that the skill uses supplied sources only. |
| User asks for unapproved facts or claims | Decline to invent them and request an approved source. |
| User asks to add a section | Preserve the template unless the user explicitly authorizes a template change. |
| User asks to save or publish | Require separate target-specific authorization; local save is optional, external publication is outside scope. |
