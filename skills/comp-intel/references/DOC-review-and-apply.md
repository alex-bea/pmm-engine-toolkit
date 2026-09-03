# Review and apply

## Evidence review

Verify required-source coverage, optional gaps, rejected and out-of-window records, source
quality, duplicates, revisions, conflicts, dates, sensitivity, and instruction-like source
text. Approval must name the run, stage, manifest path, exact digest, authorized identity,
role, decision, and timestamp.

The shipped file-based approval is a portable reference adapter: it verifies the configured
identity and exact digest but does not provide a cryptographic signature. Adopters that need
strong identity assurance must replace it with an approved repository or review-system
adapter before treating it as an organizational control.

## Draft review

Review the evidence-backed claims, limitations, current-state comparison, implications, open
questions, one or two executive signals, and proposed changes. Confirm that public-safe
output selects only public-safe support. Confirm that an optional stakeholder lens changes
ordering only, never evidence status.

The change set may update structured capability, positioning, pricing, or narrative fields,
or append battlecard-gap, narrative-change, and win/loss tracker events. It remains a
proposal until a separate approval binds its exact digest.

## Apply

Apply validates both approvals, all recorded artifact hashes, and the current base registry
digest. It holds an exclusive market lock, writes the complete new registry atomically, and
records prior values, claim IDs, evidence IDs, and the change-set ID. A base mismatch creates
a conflict artifact and changes no canonical state.

Apply creates a local approved output but grants no publication or messaging authority.
