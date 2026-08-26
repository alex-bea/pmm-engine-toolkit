# PMM Instinct Review for Codex (draft)

This plugin implements a local, human-gated improvement loop:

```text
eligible completed session -> redacted normalized copy -> queued extraction
-> explicit review -> approved instinct -> separate promotion approval -> cleanup
```

It targets macOS Codex and Python 3.11 or newer. The release remains a draft until its
pull request is approved.

## Privacy and consent

Installation does not enable capture. Enabling creates local transcript-derived state and
runs a second Codex model invocation for each eligible session. Confirm that your employer's
policy permits both actions before enabling on a work device.

The plugin has no telemetry or hosted PMM service. It never changes native Codex history.
It stores redacted user/assistant text temporarily under `~/.codex/instinct-review/` and
deletes that normalized copy after review resolution. Plugin removal preserves this user-owned
directory.

For the complete product and implementation contract, see the bundled
[product requirements](skills/pmm-instinct-review/references/DOC-product-requirements.md),
[implementation blueprint](skills/pmm-instinct-review/references/DOC-implementation-blueprint.md),
and [public submission test cases](skills/pmm-instinct-review/references/DOC-submission-test-cases.md).

## Install from the toolkit marketplace

```bash
codex plugin marketplace add alex-bea/pmm-engine-toolkit --ref main
codex plugin add pmm-instinct-review@pmm-engine-toolkit
```

When `codex` is not on `PATH`, use the ChatGPT app-bundled executable:

```bash
"/Applications/ChatGPT.app/Contents/Resources/codex" plugin marketplace add alex-bea/pmm-engine-toolkit --ref main
"/Applications/ChatGPT.app/Contents/Resources/codex" plugin add pmm-instinct-review@pmm-engine-toolkit
```

For the standalone Codex app, replace the executable with
`/Applications/Codex.app/Contents/Resources/codex`.

Open `/hooks` in Codex and separately inspect and trust the plugin's `SessionStart` and
`SessionEnd` hooks. Then ask:

```text
Use $pmm-instinct-review to enable continuous learning. I acknowledge local chat storage.
```

The first enablement records a timestamp in the local configuration. If Python, Codex, the
extractor schema, or a model policy cannot be resolved, enablement fails without turning
capture on.

## Operator requests

Use `$pmm-instinct-review` with any of these requests:

- `continuous learning status`, `continuous learning on`, or `continuous learning off`;
- `dry-run the five-session backfill` or `apply the five-session backfill`;
- `drain the extraction queue` or `retry failed extraction`;
- `clean up processed transcripts`;
- `list priority suggestions`, `resolve the zero-candidate bucket`, or `review Codex instincts`;
- `preview promotion for <instinct-id>`, select `project`, `global`, `both`, `run`, `ref`, or
  `standard`, then inspect the exact destination before the separate confirmation; or
- `import candidates from <local-json-path>` for the retired standalone workflow.

The deterministic entrypoint in a source checkout is:

```bash
python3 plugins/pmm-instinct-review/skills/pmm-instinct-review/scripts/instinct_review.py --help
```

Each review card leads with what happened, the user's feedback, proposed future behavior, and
why it matters; it does not include routing. `accept`, `reject`, `edit`, or `match` is required.
Promotion is unavailable below confidence `0.5` and always requires a destination-selection
preview followed by a matching apply confirmation. Exact duplicates are recorded as covered,
not inserted. New rules are written under `## PMM Instinct Review — Promoted Guidance`.

Voice-to-REF promotion is opt-in: add an explicit relative path under `voice_ref_routes` in
the user-owned `~/.codex/instinct-review/config.json`, for example
`{"voice_ref_routes":{"my-skill":"references/REF-voice.md"}}`. The destination must
already exist, be writable, and sit outside the plugin cache; the plugin never guesses it.

## Controlled smoke test

1. Confirm status reports `enabled: false` and that an ordinary session creates no audit.
2. Trust both hooks in `/hooks`.
3. Enable learning with the privacy acknowledgment.
4. Complete a main task with at least five user turns. Include a durable correction such as
   "For future reports, lead with the decision, not the chronology."
5. End the task, then check status. Expect one audit and one queued, succeeded, or visibly
   retryable failed extraction job.
6. Start or resume a task. If extraction produced a positive candidate, the start hook adds one
   pending-review notice per task.
7. Review the cluster. Confirm the native session remains and its normalized copy is removed.

A valid zero-candidate extraction is possible when the model finds no durable behavioral signal.
The Codex hook runner currently caps command hooks at three seconds, so `SessionEnd` only captures
and launches a detached worker; it never waits for model extraction.

## Rollback and recovery

Ask `$pmm-instinct-review` to turn continuous learning off before uninstalling. Remove the
plugin through Codex's plugin interface. No uninstall action deletes
`~/.codex/instinct-review/`; reinstalling the plugin allows its next start hook or a manual
queue drain to recover retryable jobs. Delete that state only as a separate, explicit local
data-management action.

## Runtime state

```text
~/.codex/instinct-review/
├── config.json
├── sessions/
├── queue/
├── instincts/
├── logs/
└── state/
```

Operational logs contain timestamps, states, candidate counts, and sanitized errors only.
They never contain transcript text.
