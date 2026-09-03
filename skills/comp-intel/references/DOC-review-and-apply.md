# Review and apply

The default document workflow has two human review gates. Teams using the optional controller
bind the same gates to artifact digests.

## Gate 1: evidence review

Review the exact evidence log and coverage summary before synthesis. Verify:

- market, mode, and absolute window;
- required and optional source coverage;
- accepted, rejected, out-of-window, duplicate, revised, and conflicting records;
- source quality, dates, confidence, and limitations;
- sensitive or non-public evidence; and
- any source text that could be mistaken for an instruction.

Record reviewer, date, decision, evidence-log path, and a version identifier or digest when
available. If the evidence set changes, the review no longer covers it.

## Gate 2: draft and change review

Review the briefing and proposed changes together. Confirm:

- every material statement cites reviewed evidence;
- facts, attributed reports, inferences, recommendations, and unknowns are distinct;
- narrative shifts show comparable prior and current language;
- positioning gaps meet the verified, relevant, in-scope, non-duplicate test;
- the executive layer contains at most two actionable signals;
- optional stakeholder context changed priority only, not factual status;
- public-safe output contains only public-safe support;
- stable registry facts remain intact;
- each proposed field change shows its prior value; and
- unconfirmed win/loss signals remain unconfirmed.

The reviewer may approve all changes, approve a named subset, request revision, or reject the
proposal. Record the exact scope of approval.

## Apply locally

After approval:

1. verify the registry has not changed since the proposal was prepared;
2. save a recoverable copy or rely on version control;
3. update only approved fields;
4. append approved tracker rows and the registry update log;
5. preserve claim-to-evidence references;
6. save the approved local briefing; and
7. report files changed, counts, conflicts, skipped changes, and remaining actions.

If the base registry changed, stop and rebuild the proposal against current state. Do not
silently overwrite concurrent work.

Local approval does not authorize external publication, messages, CRM changes, or edits to a
separately managed battlecard repository.

## Optional controller commands

The file-based approval adapter verifies configured identity and exact digest but is not a
cryptographic signature. Organizations needing strong identity assurance should replace it
with their approved repository or review system.

```text
python3 <skill-directory>/scripts/comp_intel.py approve-evidence --data-root <path> --run-id <run-id> --approval-file <reviewed-file>
python3 <skill-directory>/scripts/comp_intel.py submit-synthesis --data-root <path> --run-id <run-id> --package-file <package-file>
python3 <skill-directory>/scripts/comp_intel.py approve-apply --data-root <path> --run-id <run-id> --approval-file <reviewed-file>
python3 <skill-directory>/scripts/comp_intel.py apply --data-root <path> --run-id <run-id> --json
```

The controller validates approvals, artifact hashes, provenance, sensitivity, and the current
base-registry digest. It uses a market lock, writes the complete new registry atomically, and
creates a conflict artifact rather than overwriting a changed base.
