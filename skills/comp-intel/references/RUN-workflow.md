# Desktop workflow

The controller owns all transitions. Run commands from the installed skill directory.

## 1. Initialize and inspect

```text
python3 scripts/comp_intel.py init --data-root <explicit-path>
python3 scripts/comp_intel.py doctor --data-root <explicit-path> --market <market-id> --json
```

Initialization refuses a non-empty destination. Doctor distinguishes available, disabled,
missing optional, and missing required sources. A missing required source blocks collection
before a run is created.

## 2. Collect

```text
python3 scripts/comp_intel.py collect --data-root <explicit-path> --market <market-id> --from <YYYY-MM-DD> --to <YYYY-MM-DD> --json
```

The start is inclusive and the end is exclusive. Collection preserves raw candidates,
normalizes and deduplicates attributable evidence, records coverage, creates an immutable
manifest, and stops at `evidence_review`.

## 3. Review and approve evidence

Inspect `reviews/evidence-review.md`, the evidence JSONL, coverage, rejections, duplicates,
conflicts, and limitations. Copy the generated approval template outside the run, replace
its reviewer fields through the configured approval process, then install it:

```text
python3 scripts/comp_intel.py approve-evidence --data-root <explicit-path> --run-id <run-id> --approval-file <reviewed-file>
```

Changing any manifest byte invalidates the approval.

## 4. Submit bounded synthesis

Create a synthesis package that conforms to `assets/schemas/synthesis-package.schema.json`.
Every material claim cites evidence from the approved manifest. The package includes the
current registry digest and only proposed changes.

```text
python3 scripts/comp_intel.py submit-synthesis --data-root <explicit-path> --run-id <run-id> --package-file <package-file>
```

The controller validates provenance, confidence, sensitivity, public-safe selection,
change targets, and digests. It renders a draft and stops at `draft_review`.

## 5. Review and apply

Review claims, limitations, the one-or-two-signal executive layer, capability or narrative
changes, and proposed battlecard-gap, narrative, or win/loss tracker events. Install a
separate change-set approval and apply:

```text
python3 scripts/comp_intel.py approve-apply --data-root <explicit-path> --run-id <run-id> --approval-file <reviewed-file>
python3 scripts/comp_intel.py apply --data-root <explicit-path> --run-id <run-id> --json
```

Apply uses a market lock and the expected base-state digest. A stale proposal blocks without
changing canonical state. Apply does not publish or send the report.
