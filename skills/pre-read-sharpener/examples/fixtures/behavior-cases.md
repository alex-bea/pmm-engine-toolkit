# Fictional Pre-Read Sharpener Behavior Cases

> **Fictional test fixture:** Every organization, person, product, date, and result below is
> invented. These cases define contract behavior; they are not evidence for real work.

## CASE-PRS-001 — No draft

**Input:** “Use the pre-read sharpener.” No draft follows.

**Expected:** Ask the user to paste, attach, or identify the pre-read. Stop before diagnosis,
file creation, or external action.

## CASE-PRS-002 — Wrong document type

**Input:** A three-line social post promoting a fictional product, with no decision meeting
or pre-read structure.

**Expected:** Explain that the input is not clearly a pre-read and ask the user to confirm
the intended transformation. Do not rewrite or save it yet.

## CASE-PRS-003 — Missing decision facts

**Input:** A fictional draft recommends expanding a pilot but supplies no audience, timing,
alternative, reversal cost, or success measure.

**Expected:** Use the documented missing-data marker for decision-critical gaps. Do not
invent facts to make the specificity criterion pass. After no more than three repair rounds,
identify any criterion that remains failing and ask before returning a failing draft.

## CASE-PRS-004 — Decision call

**Input:** A complete fictional draft names a decision, recommendation, two options,
tradeoffs, outcomes, reversal costs, audience, and meeting date.

**Expected:** Return the full ordered deliverable, including a four-bullet Suggested agenda,
one Deciding question, and a ten-row self-check.

## CASE-PRS-005 — Informational pre-read

**Input:** A fictional quarterly operating review summarizes results and requests no meeting
decision.

**Expected:** Confirm that the user wants sharpening despite the non-decision format. If
confirmed, omit the decision-call agenda and state that the agenda does not apply.

## CASE-PRS-006 — Persistent quality failure

**Input:** A decision draft provides a recommendation but no evidence or concrete outcome;
the user forbids marking missing data or requesting facts.

**Expected:** Revise and rescore at most three times. Then name the blocking criteria and ask
whether to return the still-failing draft. Never label it passing.

## CASE-PRS-007 — Save and collision

**Input:** A passing fictional rewrite titled “Approve the Harborline Beta Expansion” is run
twice on the same date in a clean temporary workspace.

**Expected:** Save the first result to
`outputs/pre-reads/YYYY-MM-DD-approve-the-harborline-beta-expansion-pre-read.md`. Save the
second to the same stem with `-2` before `.md`. Do not overwrite the first artifact.

## CASE-PRS-008 — Scoped edit

**Input:** After a passing result is saved, the user changes the meeting audience and asks
for the update.

**Expected:** Update the Audience field and any directly affected language, rerun all ten
criteria, return the full revised deliverable, and update the same dated file unless the user
requests a new version.

## CASE-PRS-009 — First-run setup

**Input:** A newly copied package has no setup mapping or receipt. The user asks to sharpen a
real draft.

**Expected:** Run the setup sections first. Verify the complete package, present exact
adopter-owned configuration, receipt, test, and output paths, require confirmation before
local setup writes, execute the fictional fixture in an isolated workspace, and create a
receipt before processing the real draft.

## CASE-PRS-010 — Unsafe destination

**Input:** The proposed configuration or output destination is inside the installed skill
package, is ambiguous, or is not writable.

**Expected:** Mark setup `blocked`, identify the unsafe destination, and ask the adopter to
confirm a safe path outside the package. Do not silently select another directory and do not
run the real draft.

## CASE-PRS-011 — Stale setup receipt

**Input:** A previously ready receipt names an older package digest or a different required
destination mapping.

**Expected:** Treat the receipt as stale, identify the changed package or mapping field, and
repeat the affected installation, mapping, permission, and fixture checks before normal
execution. Preserve existing generated pre-reads.

## CASE-PRS-012 — Repair after fixture failure

**Input:** Package closure passes, but the isolated fixture cannot write its receipt or the
compatible agent cannot complete the expected pre-read.

**Expected:** Keep overall readiness `blocked`. Record the failure as failed or unavailable,
name the exact repair action, preserve diagnostic evidence, and never convert static
inspection into a passed end-to-end test.
