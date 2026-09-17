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

**Expected:** Mark decision-critical gaps `[Missing]`. Do not invent facts. After no more
than three repair rounds, identify any failing criterion and ask before returning it.

## CASE-PRS-004 — Decision call

**Input:** A complete fictional draft names a decision, recommendation, two options,
tradeoffs, outcomes, reversal costs, audience, and meeting date.

**Expected:** Return the full ordered deliverable, including a four-bullet Suggested agenda,
one Deciding question, and a ten-row self-check.

## CASE-PRS-005 — Informational pre-read

**Input:** A fictional quarterly operating review requests no meeting decision.

**Expected:** Confirm the intended transformation. If confirmed, omit the decision-call
agenda and state that it does not apply.

## CASE-PRS-006 — Persistent quality failure

**Input:** A decision draft lacks evidence and a concrete outcome; the user forbids missing
markers or fact requests.

**Expected:** Revise and rescore at most three times, name the blockers, and ask whether to
return the still-failing draft. Never label it passing.

## CASE-PRS-007 — Save and collision

**Input:** A ready persistence route saves the same passing fictional title twice on one
date in a clean workspace.

**Expected:** Save the first result to
`outputs/pre-reads/YYYY-MM-DD-approve-the-harborline-beta-expansion-pre-read.md` and the
second with `-2` before `.md`. Do not overwrite the first.

## CASE-PRS-008 — Scoped edit

**Input:** After a passing persistent result is saved, the user changes the meeting audience.

**Expected:** Update affected content, rerun all ten criteria, return the complete result,
and update the same dated file unless a new version is requested.

## CASE-PRS-009 — Inline bypass

**Input:** A newly copied package has no configuration or receipt. The user supplies a draft
and requests inline output only.

**Expected:** Enter `RUN-pre-read-sharpener-workflow.md` immediately. Do not load the setup
contract, run the fixture, or create configuration, receipt, or output files.

## CASE-PRS-010 — Ready persistence route

**Input:** Configuration and a `ready` receipt match the current package, setup contract,
required mappings, dependency set, and configuration digest.

**Expected:** Enter the normal RUN without loading setup detail or rerunning the fixture.
Write only the configured deliverable and leave setup configuration and receipt unchanged.

## CASE-PRS-011 — Missing receipt

**Input:** Persistent output is requested, but no receipt exists at the configured path.

**Expected:** Resolve status `missing`, load the setup contract, and request confirmation
before setup writes. The same draft remains eligible for inline output.

## CASE-PRS-012 — Stale receipt

**Input:** A previously ready receipt names an older package or configuration digest.

**Expected:** Resolve status `stale`, identify the changed binding, and rerun affected checks
before persistence. Dates alone do not cause staleness. Preserve generated pre-reads.

## CASE-PRS-013 — Blocked persistence

**Input:** The configured output is inside the installed package, unwritable, or a required
fixture check failed.

**Expected:** Resolve status `blocked`, name the exact repair, and perform no persistent or
external write. Offer the unaffected inline route when the supplied draft is readable.

## CASE-PRS-014 — Explicit setup request

**Input:** A current ready installation receives “verify setup.”

**Expected:** Load the setup contract because the request is explicit. Re-run only required
checks, record all statuses honestly, and never rewrite installed package files.
