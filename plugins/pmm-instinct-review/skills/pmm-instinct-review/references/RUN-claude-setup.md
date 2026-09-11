---
doc_type: RUN
normative: true
requires:
  - DOC-product-requirements.md
  - DOC-implementation-blueprint.md
status: Draft
version: "0.3.1"
owner: toolkit-maintainers
consumers:
  - Claude Code adopters
  - plugin operators
  - public toolkit maintainers
change_control: Pull request review
---

# PMM Instinct Review — Native Claude setup (`0.3.1` package; `0.3.0` Claude behavior)

This is the binding setup procedure for adopting native Claude Code session capture,
background extraction, human review, and receipt-bound promotion from a self-contained PMM
Engine Toolkit checkout. It does not require a Claude marketplace or a private repository.

Complete setup ends with a truthful receipt. Installation alone is not consent, an extracted
candidate is not an approved instinct, and an approved instinct is not promotion approval.

## 0. Safety boundary

Before changing the destination machine, explain these facts in plain language:

- The installer makes the nested `pmm-instinct-review` skill discoverable as a personal
  Claude skill and adds one narrowly owned `SessionStart` and one `SessionEnd` handler to the
  user's Claude settings.
- A fresh installation is disabled. A valid receipt-owned upgrade preserves the current
  state and reports it truthfully. Capture starts for a new state root only after the user
  explicitly acknowledges local storage and Claude model processing.
- Eligible main-session user/assistant text is minimized, redacted, bounded, and stored under
  `~/.claude/pmm-instinct-review-data/`. Native transcript files are read-only.
- System/developer context, reasoning, tools, tool results, patches, world state, subagents,
  sidechains, and this package's extractor/worker sessions are excluded.
- `SessionEnd` only checks consent, spools a small metadata request, and launches a fully
  detached worker. It does not scan the transcript or wait for a model call. The worker
  normalizes bounded evidence and invokes the authenticated Claude Code CLI with no tools, no
  session persistence, one maximum turn, and a strict output schema.
- Pattern-based redaction cannot guarantee removal of every secret type. Do not put secrets
  into test sessions, and do not enable capture where policy forbids local transcript-derived
  storage or this additional Claude invocation.
- The worker may suggest zero to five patterns. It cannot create an instinct or approval.
- Candidate acceptance and promotion approval are separate human decisions. Promotion
  approval is bound to exact target and content digests. A worker may execute that immutable
  receipt; it may not approve, retarget, merge, or publish.
- Claude, Codex, and portable stores remain separate. This setup never imports from or falls
  back to `~/.codex/` or an older Claude review directory.

Stop if the user does not understand this boundary, the device policy is unknown, or local
capture is prohibited. It is valid to install with capture left disabled.

## 1. Preconditions

Verify all of the following on the destination machine:

1. The Toolkit checkout is from the intended public source and its revision is known.
2. Python 3.10 or newer is available as `python3`.
3. Claude Code 2.1.205 or newer is installed for the user who will run the hooks. The worker
   requires `--bare`, `--json-schema`, `--max-turns`, `--no-session-persistence`,
   `--permission-mode`, `--tools`, and `--disallowedTools`. Because `claude --help` does not
   list every supported flag, the successful Section 1.1 request—not help output—is the
   authoritative feature check.
4. The hook/worker environment has one authentication path supported by this preserved bare
   extractor: an inherited `ANTHROPIC_API_KEY`, or supported Amazon Bedrock, Google Vertex AI,
   or Microsoft Foundry provider credentials. An ordinary Claude subscription login/keychain
   alone is not used by `--bare`. This release also does not pass `--settings`, so an
   `apiKeyHelper` configured only in Claude settings is not consumed.
5. The user can read and update `~/.claude/settings.json` and
   `~/.claude/skills/`, or those paths do not yet exist.
6. The package directory is:

   ```text
   <toolkit-root>/plugins/pmm-instinct-review/
   ```

7. The package contains these required surfaces:

   ```text
   .claude-plugin/plugin.json
   hooks/claude-hooks.json
   scripts/pmm_instinct_claude.py
   scripts/claude_instinct_capture.py
   scripts/claude_instinct_hook.py
   scripts/claude_instinct_worker.py
   scripts/claude_instinct_review.py
   scripts/claude_instinct_promote.py
   scripts/install_claude_instinct_review.py
   assets/claude-config-template.json
   assets/claude-extractor-prompt.md
   assets/claude-extractor-schema.json
   skills/pmm-instinct-review/SKILL.md
   skills/pmm-instinct-review/references/RUN-claude-setup.md
   ```

Read this package README, the nested `SKILL.md`, and this RUN before install. Stop if any
launcher imports from outside this package, embeds an author-specific path, or requires a
private repository. Do not repair a partial package by pointing it to another checkout.

### 1.1 Verify bare-mode authentication safely

First record `claude --version`. You may inspect `claude --help`, but absence there does not
prove a flag is unsupported because the help output is not exhaustive. The actual request below
is the authoritative feature and authentication check.

Do not display, log, copy, or test-print credential values. Check that the intended provider
environment is available to non-interactive child processes, then run one harmless bare-mode
request using the same model and safety flags as the worker:

```bash
claude --bare -p 'Return an object whose ready field is true and include no other fields.' \
  --output-format json \
  --json-schema '{"type":"object","properties":{"ready":{"type":"boolean"}},"required":["ready"],"additionalProperties":false}' \
  --model sonnet \
  --max-turns 1 \
  --no-session-persistence \
  --permission-mode dontAsk \
  --tools "" \
  --disallowedTools "mcp__*"
```

Require exit code zero and `structured_output.ready: true` in the JSON response. The empty tool
set disables built-in tools, and the explicit MCP wildcard denies MCP tools. If a different
model will be configured, use that exact model in the preflight. A successful
ordinary interactive Claude session is not this check: `--bare` does not consume subscription
OAuth/keychain state. Do not claim that settings-only `apiKeyHelper` support exists in this
release. If the request reports missing authentication, provider configuration, entitlement,
or model access, leave capture disabled and resolve that account/provider issue outside this
skill. Never place credentials in this package, state files, command arguments, examples, or
diagnostic output.

## 2. Choose an installation mode

Run all commands in Sections 2–10 from the package directory unless a command says otherwise.

| Mode | Use when | Active code | Update behavior |
|---|---|---|---|
| `symlink` (recommended for a trusted checkout) | The Toolkit checkout will remain at a stable path | The checkout itself | Validated checkout updates become active immediately |
| `copy` | The user wants a pinned local snapshot | `~/.claude/pmm-instinct-review/` | Remains unchanged until an explicit replacement procedure |

Both modes create a personal-skill symlink at
`~/.claude/skills/pmm-instinct-review`. In the public nested layout it points to
`skills/pmm-instinct-review/` inside the active bundle. Both use
`~/.claude/pmm-instinct-review-data/` for mutable state.

The installer refuses an occupied install or skill destination. Do not overwrite a different
skill, copy, symlink, or user-edited directory. Report its exact path and let the user decide
how to preserve or relocate it.

## 3. Inspect, then install disabled

First inspect without writing:

```bash
python3 scripts/install_claude_instinct_review.py --check
```

Record the returned personal-skill path, whether it already exists, owned-hook count, settings
path, state root, and whether state already exists. A clean machine normally reports no skill,
zero owned handlers, and no state.

Install in the selected mode:

```bash
# Live Toolkit checkout
python3 scripts/install_claude_instinct_review.py --install --mode symlink

# Or pinned snapshot
python3 scripts/install_claude_instinct_review.py --install --mode copy
```

For a fresh state root, the installer must:

- resolve its package root and nested skill without an ambient working-directory fallback;
- preserve all unrelated keys and handlers in `~/.claude/settings.json`;
- remove only stale handlers owned by this package before adding the current two;
- create a timestamped settings backup when settings change;
- install exactly one `SessionStart` and one `SessionEnd` command handler;
- create the explicit state root and disabled default `config.json`;
- record an installation receipt under the state root; and
- leave `enabled: false` and `privacy_acknowledged_at: null`.

Save the command's JSON receipt. Do not describe installation as capture enablement.
If an unowned state root already contains enablement or acknowledgement, installation must
stop without adding hooks. A valid receipt-owned upgrade preserves existing config and records
the observed capture and acknowledgement values in the new receipt.

## 4. Verify skill discovery and native hooks

Restart Claude Code so personal skill and settings changes are loaded. Then:

1. Open `/skills` and verify `pmm-instinct-review` is present.
2. Invoke `/pmm-instinct-review` or ask Claude to show PMM Instinct Review status.
3. Open `/hooks` and inspect both package-owned handlers.
4. Verify `SessionStart` matches `startup|resume|clear|compact`, uses a five-second timeout,
   and passes the explicit state root to `claude_instinct_hook.py`.
5. Verify `SessionEnd` uses the same active bundle and state root with a five-second timeout.
6. Confirm every pre-existing unrelated setting and hook is still present.
7. Confirm no MCP server, network publisher, scheduled approval, or hidden marketplace entry
   was added.

Run the check again:

```bash
python3 scripts/install_claude_instinct_review.py --check
```

The expected installed state is one personal skill, two owned hook handlers,
`receipt_valid: true`, `skill_target_valid: true`, `bundle_valid: true`,
`installation_valid: true`, and
`ambiguous_hook_handlers: 0`. `skill_target_valid` proves that the personal-skill symlink still
resolves to the exact active skill named by the receipt; `installation_valid` additionally binds
that target to a complete fixed runtime surface and the complete owned-hook set with no
ambiguous handler. Any false value, other owned-hook count, invalid or missing receipt,
ambiguous handler, broken or retargeted skill symlink, or unresolved package file blocks
enablement. The schema-2 installation receipt is
ownership authority: missing or tampered `state/installation.json` also blocks update and
uninstall rather than guessing ownership.

The optional plugin manifest is for local validation/development only. When supported by the
installed Claude Code version, maintainers may additionally run:

```bash
claude plugin validate .
claude --plugin-dir .
```

Do not substitute optional plugin loading for checking the standalone personal skill and user
hooks. The plugin's `SessionEnd` handler is asynchronous: a plugin-provided timeout does not
raise Claude Code's shared 1.5-second SessionEnd budget. Claude can cancel async hooks when a
non-interactive `claude -p` process tears down, so the standalone user-settings installation is
the supported path when those sessions must be captured.

## 5. Inspect disabled runtime status

Status is read-only and requires an explicit state root:

```bash
python3 scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data status
```

Before consent, verify:

- `enabled` is `false`;
- `privacy_acknowledged` is `false`;
- `state_root` is exactly the standalone state root;
- `queue` has no unexpected work;
- `extraction_available` is `true` because the prompt and schema are bundled;
- `promotion_automation_available` and `human_approval_required` are `true`; and
- `claude_binary` identifies the intended executable, or is `null` and blocks enablement.

Also require the Section 1.1 bare-mode request to pass in the same shell/environment that will
launch Claude Code. Binary discovery does not prove model authentication.

Status must not read or create state in `~/.codex/`, the Toolkit checkout, a plugin cache, or
another Claude directory.

## 6. Ask for privacy consent and enable only on an exact yes

After completing the trust inspection and successful bare-mode authentication preflight, ask
one decision:

```text
Enable private session capture now? If enabled, bounded and redacted user/assistant text
from eligible Claude Code sessions will be stored under
~/.claude/pmm-instinct-review-data/ and sent to your authenticated Claude Code CLI for
background pattern extraction. yes / no
```

- If the answer is `no`, ambiguous, or absent, leave capture disabled and finish with an
  installed-but-inactive receipt.
- Do not infer consent from cloning the Toolkit, installing hooks, approving a public package,
  or enabling a different runtime.
- On `yes`, run:

  ```bash
  python3 scripts/claude_instinct_capture.py \
    --state-root ~/.claude/pmm-instinct-review-data \
    on --acknowledge-privacy
  ```

To choose a different supported extraction model or explicit Claude executable, append
`--model MODEL` or `--claude-binary /absolute/path/to/claude` to that command. The runtime
uses that exact model and never silently substitutes another.

If Claude Code or its supported bare-mode credential environment cannot be resolved,
enablement must remain off. Report that blocker; do not hand-edit configuration to bypass it.

Run status again and require `enabled: true`, `privacy_acknowledged: true`, the intended
model/executable, and the expected state root before testing capture.

## 7. Run a privacy-safe native lifecycle smoke check

Use an intentionally fictional, non-sensitive main Claude Code session. It must contain at
least five user messages after normalization. Include one durable, harmless preference that
can plausibly generate a candidate; do not use real customer, employer, financial, health,
credential, or unpublished product information.

1. Start a new main session after enablement.
2. Send at least five genuine user messages and receive normal assistant responses.
3. End the session normally so native `SessionEnd` runs.
4. Verify the hook returns promptly. A model call, long wait, or transcript text in hook output
   is a failed smoke check.
5. Start or resume Claude Code. `SessionStart` must only validate the fixed store layout,
   force-launch the detached worker, and optionally read one bounded prior status snapshot;
   the worker performs recovery and retained-store scans.
6. Run status and inspect the explicit state root.

The immediate `SessionEnd` artifact is one metadata-only request under `capture-inbox/`.
The detached worker consumes it and creates one audit, one evidence object, and one `queued`
job keyed by Claude runtime, session ID, transcript SHA-256, and schema version. The evidence
must contain only bounded redacted user/assistant text. The native source transcript must be
byte-for-byte unchanged. Re-delivering the same hook payload must return the existing valid
request or job rather than create a duplicate. A retryable capture failure retains its request;
an invalid file occupying the derived job identity is not reported as successful capture.

The detached worker should move the job through `processing` to `completed`, or to visible
`retryable`/`failed` state. `completed` requires a schema-valid suggestion file; zero
candidates is a valid success. No suggestion file may be inferred from invalid output.

If pending work remains, run one explicit drain:

```bash
python3 scripts/claude_instinct_worker.py \
  --state-root ~/.claude/pmm-instinct-review-data --drain
```

If a job reaches `failed`, inspect only its sanitized state and log. Never paste the native
transcript or raw model stderr into a diagnostic report. After fixing the underlying issue,
requeue all failed jobs—or one exact job—and let the detached worker run:

```bash
python3 scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data retry

python3 scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data retry --job JOB_ID
```

Automatic retries stop at the configured attempt ceiling. A stale `processing` lease may be
recovered to `retryable`; a lock never grants review or promotion authority.

## 8. Review extracted suggestions

List the backlog without mutation:

```bash
python3 scripts/claude_instinct_review.py \
  --state-root ~/.claude/pmm-instinct-review-data list-priority
```

Keep the three buckets separate:

1. zero-candidate audits;
2. positive clusters, grouped by exact type and normalized rule; and
3. audits missing a suggestion file.

Present one positive cluster at a time with what happened, user feedback, proposed future
behavior, why it matters, support count, source skills/cwds, and cluster ID. Do not introduce a
destination at this gate. Accept only the user's explicit decision:

```bash
# Accept
python3 scripts/claude_instinct_review.py \
  --state-root ~/.claude/pmm-instinct-review-data review \
  --cluster CLUSTER_ID --decision accept --confirm

# Reject
python3 scripts/claude_instinct_review.py \
  --state-root ~/.claude/pmm-instinct-review-data review \
  --cluster CLUSTER_ID --decision reject --confirm

# Edit requires an exact edited rule; an edited rationale is optional
python3 scripts/claude_instinct_review.py \
  --state-root ~/.claude/pmm-instinct-review-data review \
  --cluster CLUSTER_ID --decision edit --edited-rule "ONE ATOMIC RULE" \
  --edited-rationale "EVIDENCE-BOUND RATIONALE" --confirm

# Match requires an existing active instinct of the same type and normalized rule
python3 scripts/claude_instinct_review.py \
  --state-root ~/.claude/pmm-instinct-review-data review \
  --cluster CLUSTER_ID --decision match --confirm
```

Use `--strong-correction` or `--contradicted` only when the user explicitly confirms that
fact. Resolve zero-candidate audits only after one explicit confirmation:

```bash
python3 scripts/claude_instinct_review.py \
  --state-root ~/.claude/pmm-instinct-review-data resolve-zero --confirm
```

The worker must never perform these commands. Evidence is deleted only after every cluster
occurrence in its audit has an exact job/result/audit-bound ledger decision; audits,
suggestions, instincts, and sanitized state remain. If an older or malformed review ledger is
present, review and cleanup fail closed until the operator repairs or archives that ledger.

## 9. Preview and approve promotion separately

Only an `active` instinct with confidence at least `0.5` is eligible. A single observation
normally produces confidence `0.3`; do not manufacture support, edit state by hand, or weaken
the threshold just to complete setup. If no eligible instinct exists, record promotion as
available but not exercised.

Select exactly one destination class and delivery pair:

| Destination | Required target | Delivery |
|---|---|---|
| `global` | Exactly `~/.claude/CLAUDE.md` | `local` |
| `project` | Exact project `CLAUDE.md` | `local` |
| `skill` | Exact governed `RUN-*.md` or `REF-*.md` | `review` |
| `standard` | Exact governed `STD-*.md` | `review` |

Installed packages, plugin caches, and runtime state are never valid targets. Generate a
preview without writing the destination:

```bash
python3 scripts/claude_instinct_promote.py \
  --state-root ~/.claude/pmm-instinct-review-data preview \
  --instinct INSTINCT_ID \
  --target /absolute/project/CLAUDE.md \
  --destination-class project \
  --delivery local
```

Show the user every bound value: instinct, source-guidance SHA-256, destination class, delivery
mode, exact target, current target SHA-256, rule, rationale, managed section, insertion,
complete resulting text, resulting SHA-256, duplicate state, and preview digest. The preview
must not change the target.

Ask whether to approve that exact digest. An edit, changed target, ambiguous answer, or changed
destination cancels the approval and requires a new preview. On an explicit exact approval:

```bash
python3 scripts/claude_instinct_promote.py \
  --state-root ~/.claude/pmm-instinct-review-data approve \
  --preview-digest PREVIEW_SHA256 --confirm
```

This command rechecks the preview and current target, writes an immutable receipt, and launches
the detached executor. It is not permission to approve another preview or target.

Inspect execution status:

```bash
python3 scripts/claude_instinct_promote.py \
  --state-root ~/.claude/pmm-instinct-review-data status
```

`approved` counts only valid immutable receipts; `promoted`, `covered`, `awaiting_review`,
`failed`, and `pending_execution` partition those valid receipts. `invalid` reports malformed
receipt files and is always an operator blocker.

If an approved receipt remains pending, an operator may run:

```bash
python3 scripts/claude_instinct_promote.py \
  --state-root ~/.claude/pmm-instinct-review-data execute
```

Local execution atomically writes exactly the approved result, verifies its digest, and records
`promoted` or duplicate `covered`. Any target drift produces `failed`; make a new preview rather
than modifying a receipt. Repeated approval of the same unchanged preview returns the same
receipt. If execution is interrupted after the exact target write but before its outcome is
saved, the next execution verifies the approved resulting digest, records the outcome, and does
not rewrite the target. Only a valid outcome bound to that receipt's target and result suppresses
repeat execution.

For `skill` or `standard` review delivery, the executor writes a unified diff under
`promotion-changesets/`, records `awaiting_review`, and leaves the governed target unchanged.
Take the patch through that repository's normal branch, approval, and pull-request process.
The receipt is never merge or publication authority.

## 10. Produce the setup receipt

Finish with the structure in `../assets/output-template.md`. At minimum record:

- Toolkit checkout and revision;
- symlink or copy mode;
- active bundle and personal-skill paths;
- package-closure result;
- settings path and backup, if any;
- installation receipt schema/digest, `receipt_valid`, `skill_target_valid`, `bundle_valid`,
  `installation_valid`, and ambiguous-handler count;
- `/skills` discovery and both `/hooks` results;
- explicit privacy decision and current capture state;
- exact Claude-owned state root and extractor model;
- native lifecycle smoke result, including queue/extraction outcome;
- review and promotion availability, and whether either was actually exercised;
- any blocker or unsupported host capability; and
- exact update, disable, and uninstall instructions.

Do not claim release validation when the authenticated native lifecycle was not run. A missing
Claude executable, failed hook, unresolved package file, or unverified extraction must stay
visible as a blocker.

## 11. Routine operation

- Use status and `list-priority` for read-only inspection.
- `off` stops new capture. `SessionStart` may still launch the worker, which can recover already
  queued extraction work and execute already approved receipts; inspect or drain retained state
  explicitly.
- Review positive clusters intentionally; never treat a schedule or worker as confirmation.
- Retry failed extraction only after inspecting the sanitized failure.
- Periodically inspect retained audits, suggestions, instincts, receipts, outcomes, and data
  policy. Delete normalized evidence only through the review retention path.
- Reverse promoted guidance through the destination's normal owner/governance process; do not
  rewrite an old receipt.

## 12. Disable and uninstall

Disable future capture while preserving all state:

```bash
python3 scripts/claude_instinct_capture.py \
  --state-root ~/.claude/pmm-instinct-review-data off
```

Then remove only the personal-skill symlink and two owned settings handlers:

```bash
python3 scripts/install_claude_instinct_review.py --uninstall --confirm
```

The uninstaller backs up changed settings, preserves unrelated settings and hooks, and leaves
`~/.claude/pmm-instinct-review-data/` intact. It refuses to delete a non-symlink skill target.
It also leaves a copy-mode snapshot intact. Remove either state or a snapshot only as a
separate, explicit local data-management action after deciding what must be retained.

## 13. Update safely

### Symlink mode

1. Disable capture.
2. Validate and update the Toolkit checkout using the repository's normal version-control
   workflow.
3. Re-run `--check`, then `--install --mode symlink` to refresh the two owned handlers without
   duplicating them.
4. Restart Claude Code; inspect `/skills` and `/hooks` again.
5. Review release/privacy changes, then obtain fresh consent before re-enabling if the capture
   boundary changed.

Do not pull unreviewed code into a live symlink while hooks are enabled.
If the installation receipt is missing or invalid, do not reinstall over the state or edit
hooks by inference; preserve the state and reconcile ownership manually first.

### Copy mode

A copy is pinned and the installer will not overwrite it:

1. Disable capture from the active snapshot.
2. Run its `--uninstall --confirm` to remove owned hooks and the personal-skill symlink while
   preserving state and the old snapshot.
3. Move the old `~/.claude/pmm-instinct-review/` snapshot to a clearly named backup location;
   do not delete it until the replacement passes.
4. From the validated new Toolkit package, run `--install --mode copy`.
5. Restart Claude Code and repeat Sections 4–7.
6. Preserve the same explicit state root; do not migrate or merge Codex state.
7. Remove the old snapshot only after the user confirms the replacement and retention needs.

## 14. Failure handling

- **Claude CLI missing or unsupported:** leave capture disabled; install or update Claude Code.
- **Bare-mode authentication missing:** leave capture disabled. Configure an inherited
  `ANTHROPIC_API_KEY` or supported Bedrock/Vertex/Foundry provider credentials. Subscription
  OAuth/keychain and settings-only `apiKeyHelper` do not authenticate this worker.
- **Partial package or broken nested skill:** stop and restore a complete Toolkit package.
- **Occupied install destination:** preserve it and ask the user to resolve the conflict.
- **Invalid settings JSON or hook collection type:** stop without rewriting settings.
- **Hook error or no eligible job:** the lifecycle hook returns without disrupting Claude and
  may be silent. Inspect status, `capture-inbox/`, queue state, and sanitized logs for the
  stable reason; do not broaden capture.
- **Invalid installation receipt or ambiguous owned hook:** preserve settings/state and stop;
  do not upgrade or uninstall by guessed ownership.
- **Invalid capture request:** record only a sanitized error, remove the invalid request, and do
  not report the session as queued.
- **Occupied job identity:** retain the invalid job file for recovery, retain the capture request
  while it remains retryable, inspect only sanitized logs/metadata, and do not report the
  session as queued.
- **Invalid extractor output:** create no suggestion; retain visible retry state.
- **Transcript/evidence leakage into logs:** disable capture and treat validation as failed.
- **Duplicate job:** preserve the first digest-keyed record; do not create another.
- **Review without confirmation:** make no ledger or instinct change.
- **Preview or receipt mismatch/target drift:** make no new target change; create a new preview.
- **Interrupted exact target write:** rerun the executor; it must recognize the approved
  resulting digest and complete the outcome without rewriting.
- **Governed patch awaiting review:** leave the target untouched and use its normal review path.
- **Cross-runtime or package-cache write:** disable capture, preserve sanitized diagnostics, and
  treat setup as failed.

At every failure, report what is unavailable. A skipped or substituted stage is not a pass.
