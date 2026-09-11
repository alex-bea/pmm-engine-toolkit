---
doc_type: RUN
normative: true
requires:
  - REF-evidence-privacy.md
status: Active
version: "1.0"
owner: toolkit-maintainers
consumers:
  - Codex users
  - Claude Code users
change_control: Pull request review
---

# Stakeholder Brief Workflow

## 0. Purpose and boundary

Turn authorized, professionally relevant observations into a concise stakeholder brief and a communication-preparation prompt. This workflow is not a personality assessment, employment evaluation, surveillance mechanism, or external-system integration. Do not collect evidence, discover accounts, or read external systems without the user's explicit authorization.

## 1. Confirm the request

Before analysis, establish all of the following:

- subject name or role and a clear way to distinguish them from similarly named people;
- stated professional purpose and intended audience;
- authority or consent basis for each proposed evidence source;
- requested mode: standalone, delta, or relational;
- whether the user wants a conversational draft or an explicitly named local output path.

If the subject is ambiguous, stop and ask the user to choose. If authority, professional purpose, or allowed evidence is missing, stop and ask for it. Do not substitute an account search, public-profile scrape, or guessed identity.

## 2. Assemble a bounded evidence corpus

Use a 14-day lookback by default unless the user supplies a different bounded window. Record the window and all limitations in the brief.

When the authorized source supports it, distinguish:

- **subject-originated** observations, such as a statement, update, decision, or reply from the subject; and
- **subject-directed** observations, such as a request, question, or response directed to the subject.

Use the supplied evidence only. An optional adapter may retrieve evidence in the adopter's environment, but it is not a package dependency and must honor the adopter's permissions. For a large corpus, begin with no more than about 60 observations in each direction. If fewer than 10 subject-originated observations are available, report the count and ask whether the user wants to proceed with thin signal. Subject-directed material does not satisfy that floor.

Record source, date, direction when known, relevant context, permitted use, and contradictions in `assets/evidence-corpus-template.md` or an equivalent user-supplied record. Do not place evidence, identifiers, credentials, or access details in this package.

## 3. Select revealing context

Choose up to 10 high-value observations for context review. Prioritize items that show a stated decision, recommendation, tradeoff, commitment, blocker, disagreement, clarification, response to a request, or change in scope. If direct-conversation context is authorized, include up to five additional relevant conversation contexts that are not already in the selected slate. The total cap is 15 contexts.

Read only the supplied or authorized context. If context cannot be accessed, note the limitation and continue with the evidence that remains. Do not invent a thread, infer missing replies, or present absence as proof of a trait.

## 4. Load optional context

### Optional long-form notes

Use optional long-form notes only when the adopter supplies an approved source map and the relevant material. Keep at most three recent dated note sources in the default window. Use the notes to identify explicit asks, stated priorities, and discrepancies with the primary corpus. If notes are unavailable or cannot be read, omit this section and say so.

### Delta mode

Use delta mode only when the user supplies a prior brief or comparable authorized baseline. Compare new priorities, resolved or dropped topics, evidence volume or urgency, and relationship activity. If no baseline is supplied, omit the section and state that no comparison was made.

### Relational mode

Use relational mode only when the user supplies an authorized reference-person brief or evidence set. Identify work intersections, relevant differences, and communication framing grounded in both source sets. Do not infer private affinity, conflict, hierarchy, or sensitive relationship information. If the reference material is absent, offer standalone mode instead.

## 5. Analyze and render the stakeholder brief

Use `assets/output-template.md`. Every material claim needs a source and date and one of these labels:

- **Verified**: directly supported by a cited, reliable source.
- **Reported**: contained in supplied material but not independently validated.
- **Inference**: a cautious analysis derived from cited observations.
- **[Missing]**: a decision-critical fact is absent.

Require at least two independent observations before describing a recurring professional pattern, collaboration preference, capacity signal, or relationship pattern. Preserve disagreements and contradictory evidence. Do not turn a writing style, workload note, or one interaction into a personality claim.

For relationships, list at most five people only when the evidence establishes a professional interaction. Describe the observed topic and a working state such as active, waiting on a decision, or blocked by an explicitly cited dependency. Do not infer emotional states or private relationships.

Include optional long-form-note, delta, and relational sections only when their inputs are present. Explain every omitted section in the uncertainties and corrections area.

## 6. Produce the writing-preparation prompt

Use `assets/writing-prompt-template.md`. Populate it from cited observations only. It should help the user frame a professional message; it must not imitate a person's voice, claim to know their private preferences, or conceal uncertainty. Include the relational framing only in relational mode.

## 7. Deliver, correct, and save

Return the brief and writing-preparation prompt in the conversation by default. State how the subject or authorized owner can correct or request deletion of an output. A local save requires an explicit user-selected path and confirmation immediately before writing. Never publish, send, schedule, or otherwise mutate an external system.

## Error handling

| Situation | Action |
|---|---|
| Subject is ambiguous | Stop and ask the user to identify the subject or role. |
| Source authority or professional purpose is absent | Stop and request the missing authorization context. |
| Fewer than 10 subject-originated observations | Report the count, explain thin-signal risk, and ask whether to proceed. |
| Subject-directed observations are absent | Record the absence and continue; do not infer a relationship pattern from it. |
| Optional notes cannot be read | Omit the notes section and record the limitation. |
| Prior brief is absent in delta mode | Offer standalone mode or ask the user to supply a baseline. |
| Reference brief is absent in relational mode | Offer standalone mode or ask the user to supply authorized reference material. |
| Sources conflict | Preserve both views, label the conflict, and avoid a forced conclusion. |
| User asks for an external action | Explain that the skill can prepare a draft only; request separate authorization and use an appropriate tool if one is available. |
