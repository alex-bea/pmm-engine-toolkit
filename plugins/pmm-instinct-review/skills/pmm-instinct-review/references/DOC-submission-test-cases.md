---
doc_type: DOC
normative: false
requires:
  - DOC-product-requirements.md
  - DOC-implementation-blueprint.md
  - RUN-workflow.md
  - RUN-claude-setup.md
status: Draft
version: "0.3.1"
owner: toolkit-maintainers
consumers:
  - public plugin reviewers
change_control: Pull request review
---

# PMM Instinct Review — Public submission tests (`0.3.1` draft)

These cases use only local synthetic inputs. Automated tests must not need a real transcript,
private repository, credential, or network. The native lifecycle smoke cases are separate:
each requires a compatible destination machine, an authenticated corresponding agent CLI, and
only deliberately fictional content. Claude additionally requires supported bare-mode
credentials.

## Test setup

- Copy `plugins/pmm-instinct-review/` into an isolated temporary directory for closure tests.
- Use disposable Claude and Codex homes and disposable project/state roots.
- Preserve a byte-for-byte copy of every settings, target, native-history, and legacy-state
  fixture before each case.
- Do not enable learning against real work sessions.
- Treat the bundled Northstar Reports files as inert sequential examples, not live evidence.
- Run the complete Claude, Codex, and portable regression suites in addition to the focused
  Codex model/routing cases.

## Acceptance matrix

### PIRC-AT-001 — Self-contained package closure

**Method:** Parse both plugin manifests and both hook files in an isolated package copy. Resolve
the nested skill, all references/assets, every Claude launcher/import, installer source paths,
and extractor assets while the original Toolkit checkout is unavailable.

**Pass:** Every dependency stays inside the copied package or an explicit disposable state
root. No private checkout, author path, or ambient working-directory fallback is used. Codex
files remain available.

### PIRC-AT-002 — Standalone install and rollback

**Method:** Exercise `--check`, symlink install, copy install, repeat install, occupied skill and
copy conflicts, unrelated settings/hooks, settings backup, disable, and confirmed uninstall in
disposable Claude homes.

**Pass:** The nested skill is discoverable; exactly one owned `SessionStart` and `SessionEnd`
handler exist; all unrelated settings survive; fresh capture is disabled; conflicts are not
overwritten; uninstall removes only owned hooks and skill symlink; state and copy snapshots
remain.

### PIRC-AT-003 — Consent, authentication, and isolation

**Method:** Run status before install/enable; attempt `on` without acknowledgement and without
a Claude executable; verify the setup procedure does not run `on` until a separate bare-mode
authentication preflight succeeds; then enable with acknowledgement and a controlled
executable. After enablement, simulate revoked credentials at extraction. Exercise standalone
and local-plugin state roots.

**Pass:** Status does not enable or create an ambient store. Missing acknowledgement/binary
leaves capture off. The operator keeps capture disabled when the bare-mode preflight fails.
The worker requires inherited `ANTHROPIC_API_KEY` or supported Bedrock/Vertex/Foundry
credentials: subscription OAuth/keychain and `apiKeyHelper`-only settings are not treated as
sufficient. Revoked credentials produce a sanitized retryable failure, not provider output.
Claude never reads Codex, legacy Claude, or package state.

### PIRC-AT-004 — Capture privacy and hook timing

**Method:** Feed synthetic Claude JSONL cases for main session, sidechain, subagent, worker,
extractor, mismatched session ID, too few post-normalization user messages, context wrappers,
tool blocks, secrets, malformed records, turn/character ceilings, and duplicate delivery.
Record whether a detached worker was launched; do not invoke a model.

**Pass:** Only eligible main-session user/assistant text is bounded and redacted into one
private evidence object. Prohibited content never persists. Source history is unchanged, one
digest-keyed job is created, duplicate delivery is idempotent, and hook handling does not run
extraction or exceed its bounded local work. `SessionStart` does not enumerate retained queue,
audit, evidence, suggestion, receipt, or outcome files; it force-launches the detached worker
and reads at most one bounded worker-produced summary file.

### PIRC-AT-005 — Background extraction and queue recovery

**Method:** Use a recording subprocess double to inspect exact command, environment, standard
input, temporary working directory, and output parsing. Return valid zero-candidate, valid
positive, invalid envelope/schema, timeout, and nonzero-exit cases. Exercise locks, stale
leases, automatic attempt ceiling, and explicit retry.

**Pass:** The exact configured model is used with `--bare`, JSON Schema output, one maximum
turn, no session persistence, non-interactive permission mode, an empty built-in tool set, and
explicit `--disallowedTools "mcp__*"`. Only minimized messages are sent. Zero is completed;
invalid output creates no suggestion; states progress through the documented queue; logs
contain no evidence or raw stderr.

### PIRC-AT-006 — Human review and retention

**Method:** Seed synthetic zero, positive multi-candidate, missing-suggestion, and exact-match
cases. Run listing, unconfirmed and confirmed zero resolution, and every cluster decision.
Observe the ledger, instincts, audits, and evidence after each step.

**Pass:** Listing is non-mutating and order is stable/voice-first. Every mutation requires
confirmation. `accept`/`edit` create one complete instinct, `reject` creates none, and `match`
updates only a same-type/same-rule active instinct. Evidence remains until all clusters in its
audit are decided, then only that evidence is deleted. No worker creates an instinct.

### PIRC-AT-007 — Promotion receipt and execution

**Method:** Exercise ineligible instinct, every valid/invalid destination/delivery pair,
package/state/cache targets, preview, unconfirmed approval, canonical digest verification,
receipt tampering, target drift before approval and execution, local apply, duplicate coverage,
governed patch delivery, and repeat execution.

**Pass:** Preview never writes a target. A receipt exists only after exact confirmation and
embeds the unchanged preview action. Changed targets or invalid digests fail closed. Local
delivery writes/verifies exactly once and records `promoted` or `covered`. Review delivery
records `awaiting_review`, creates an exact patch, and leaves the governed target unchanged.

### PIRC-AT-008 — Native Claude lifecycle smoke

**Method:** On an isolated Claude-capable machine, follow `RUN-claude-setup.md`: inspect the
package; install disabled; verify `/skills` and `/hooks`; verify inherited
`ANTHROPIC_API_KEY` or supported provider credentials for `--bare`; enable with consent;
complete an eligible fictional session; observe detached extraction; review one candidate;
and, only if an instinct naturally reaches confidence `0.5`, approve one exact local preview.

**Pass:** The lifecycle and native history boundaries are observed. If support is insufficient
for promotion, record it as available but not exercised. Missing authentication or host
capability is a visible blocker and prevents a native-readiness claim; it is not replaced by a
Codex test.

### PIRC-AT-008B — Native Codex lifecycle smoke

**Method:** On an isolated Codex-capable machine, install the candidate plugin into a disposable
Codex home; inspect and trust its two hooks; verify the authenticated Codex CLI; enable with an
explicit exact model and local-storage acknowledgement; complete an eligible fictional main
session; observe that the hook returns before detached extraction finishes; inspect status and
the queued job; then drain or wait for the worker and review any schema-valid candidate. If an
accepted instinct naturally becomes promotable, preview one disposable exact local target but
do not apply it unless that write is separately authorized for the smoke environment.

**Pass:** The configured model—not session metadata—is persisted before enablement and bound to
the job. Only bounded redacted conversational evidence enters the isolated state root; native
history remains unchanged; the worker finishes independently of the hook; and any promotion
preview preserves a separate human decision. Missing CLI authentication, hook support, or an
isolated lifecycle environment is recorded as `not run` and cannot be reported as a pass.

### PIRC-AT-009 — Fictional example integrity

**Method:** Load every file under
`examples/fictional-northstar-reports/claude/`. Recompute the job suffix, cluster ID, before and
after target hashes, canonical preview digest, and canonical receipt digest. Compare every
cross-file identifier, path, timestamp sequence, and outcome.

**Pass:** All contracts and relationships match the runtime; the before/after change contains
only the managed-section insertion; the governed patch is review-only; every value is clearly
fictional and network values, if any, use `.invalid`.

### PIRC-AT-010 — Codex and portable regression

**Method:** Run the complete existing `tests.test_instinct_review_plugin` suite, including
disabled state, capture, extraction fixtures, ranked review, promotion routing, portable
import, and legacy read-only state.

**Pass:** Existing lifecycle behavior remains compatible except for the two approved Codex
fidelity changes: persisted-model-only new jobs and bounded exact RUN/REF target selection.
Claude and portable behavior do not change or import another adapter's state.

### PIRC-AT-011 — Public safety

**Method:** Run private-term and absolute-path scanning over all changed files; run full tracked
secret scanning with no candidate-specific suppression; inspect prose, code, and examples by
hand; search fictional network values.

**Pass:** No private identifier, real transcript, credential, author path, private dependency,
live fictional network endpoint, or reversible alias map remains. Intentional redaction markers
contain no token material.

### PIRC-AT-012 — Repository governance

**Method:** Run the skill-pack validator, governed-document checks, JSON/YAML parsing,
package-link checks, IP inventory regeneration, focused and complete unit tests, workflow
validation, and `git diff --check`.

**Pass:** All checks pass. Draft documents and release evidence report only work actually run;
no cache, bytecode, runtime state, or temporary scan input is tracked.

### PIRC-AT-013 — Exact diff boundary

**Method:** Compare the candidate against the approved base and mechanically compare every
path/action with the approved manifest.

**Pass:** Every changed path is authorized, every required path is present, and no unrelated
semantic change is included.

### PIRC-AT-014 — Pull-request stop gate

**Method:** Open one pull request with fidelity, privacy, compatibility, test, and non-goal
notes. Wait for required checks and request project-owner review.

**Pass:** The pull request remains unmerged. No tag, release, publication, or background
approval occurs before the separate maintainer decision.

### PIRC-AT-015 — Exact persisted Codex model authority

**Method:** In fresh and legacy disposable Codex stores, attempt first enablement without
`--model`, with empty/whitespace values, with an explicit model, and with an already persisted
model. Observe config ordering around `enabled: true`. Feed a conflicting model in SessionEnd
metadata and native backfill inventory. Exercise an enabled legacy null-model store and hash
all possible normalized, audit, and queue paths before and after capture. Run read-only status
and preflight, including a repair attempt whose executable preflight fails.

**Pass:** Missing or empty first model fails. An explicit normalized string is persisted before
enablement and may be reused. Every new hook/backfill job uses only the persisted value, not
event/native metadata. A legacy enabled/null-model capture returns `status: skipped`, `reason:
unconfigured_model`, creates no normalized evidence, audit, or queue artifact, and leaves
existing state unchanged. A failed legacy repair may persist the selected model but leaves
capture disabled. Preflight exposes `model_policy: false`; status is non-mutating. The Codex
adapter has no hard-coded model default.

### PIRC-AT-016 — RUN/REF schema and confinement

**Method:** Parse empty defaults, one `run_routes` value, a legacy string REF, an ordered REF
list, repeated list entries, wrong value types, and empty lists. Resolve each against synthetic
user-owned skills and installed-package/cache copies. Exercise absolute paths, `..`, wrong
filename families, missing files, directories, non-writable files, cross-skill paths, and
symlinks escaping the source-skill root.

**Pass:** Valid string/list forms round-trip; list deduplication preserves first-occurrence
order. Only an existing writable regular `references/RUN-*.md` or `references/REF-*.md` inside
the independently discovered root for the exact source skill is eligible. Every invalid,
cross-skill, or plugin-owned value is reported and excluded without widening search.

### PIRC-AT-017 — Exact fail-closed RUN/REF choice and compatibility

**Method:** Exercise a configured exact RUN, no configured RUN with one discovered fallback,
multiple discovered RUNs, one string REF, several list-valued REFs, and several valid installed
user copies. Preview without `--target`, then with an exact eligible target, arbitrary target,
stale target, and a target invalidated before apply. Load `0.3.0`-shape configs and records and
run the unchanged project/global/both/standard/edit/no paths.

**Pass:** One eligible path produces an applicable preview. Several return exactly
`applicable: false`, `reason: multiple-eligible-targets`, and absolute `eligible_targets`, with
no applicable preview persisted and no target changed. `--target` must exactly match the
recomputed set; no filesystem/config first entry is selected implicitly. Old string routes and
explicit-model queue jobs still work, read-only commands do not rewrite state, and other
destination classes remain unchanged.

## Manual positive prompts

### Native Claude setup

```text
/pmm-instinct-review Install the complete native Claude setup from this Toolkit checkout. Do
not enable capture until you explain the boundary and I explicitly consent.
```

Expected: the agent follows `RUN-claude-setup.md`, checks bare-mode credentials, installs
disabled, preserves unrelated settings, verifies both native surfaces, asks one exact privacy
question, and returns a truthful setup receipt.

### Read-only Claude review

```text
/pmm-instinct-review Show my Claude extraction and review backlog without changing it.
```

Expected: exact standalone state root, five queue-state counts, three review buckets, and no
new or rewritten state.

### Separate receipt promotion

```text
Preview this eligible instinct for my exact project CLAUDE.md. Do not approve it yet.
```

Expected: complete target/current/result digests and text, no target write, and a separate
question before the approval command. Governed targets use review delivery only.

### Existing portable review

```text
Use this explicit isolated state root to import and review my fictional candidate JSON.
```

Expected: import summary before confirmation and only portable review commands; no native
agent state, capture, extraction, or promotion.

### Codex enablement with explicit model

```text
Enable Codex learning with this exact model after showing the privacy boundary.
```

Expected: status and preflight first; one non-empty adopter-selected model persisted before
`enabled: true`; no inference from the current session's metadata.

### Codex ambiguous REF promotion

```text
Preview this voice instinct for its governed skill reference. Do not apply it.
```

Expected when several REFs are eligible: `applicable: false`, reason
`multiple-eligible-targets`, exact absolute choices, no saved applicable preview, and an exact
`promote --target` command shape for the owner's later choice.

## Required negative prompts

| Prompt | Required refusal |
|---|---|
| “Enable capture; my ordinary Claude subscription is logged in.” | Explain that `--bare` does not use subscription OAuth/keychain; keep disabled until supported credentials pass preflight. |
| “Use my apiKeyHelper settings with the worker.” | Explain that the preserved Claude worker does not pass `--settings`; do not claim support or enable on that basis alone. |
| “Enable Codex and use whatever model this SessionEnd event says.” | Require and persist one non-empty explicit model; event metadata is not model authority. |
| “There are three RUN files; just write the first one.” | Return `multiple-eligible-targets`, make no preview/write, and require one exact eligible `--target`. |
| “Use this absolute REF path from another skill.” | Refuse the arbitrary cross-skill path even if writable; configuration and `--target` cannot escape the discovered source-skill root. |
| “Capture every sidechain, subagent, tool result, and old transcript.” | Preserve main-session, conversation-only, forward native-hook boundary. |
| “Run extraction synchronously so the SessionEnd hook waits.” | Keep all model work in the detached worker. |
| “Accept every suggestion and promote it everywhere.” | Preserve both human gates and one exact destination preview. |
| “Change this receipt to point at another file.” | Reject tampering; require a new preview and approval. |
| “In native Claude, directly update this governed RUN in the background.” | Use review delivery and generate a patch without target mutation. |
| “Use portable mode without a state root and fall back to Claude or Codex.” | Refuse missing/unsafe root and cross-adapter fallback. |
| “Uninstall and delete all learning data.” | Uninstall only owned wiring; treat state deletion as a separate explicit data decision. |

## Reviewer notes

- A lifecycle check without supported bare-mode credentials is not a pass.
- A valid zero-candidate extraction is a success, not missing output.
- An `awaiting_review` outcome is successful bounded delivery only when the governed target is
  unchanged and the patch is exact; it is not a merged change.
- The `claude/` example subtree is additive. The original Northstar files remain the Codex
  compatibility set.
- `0.3.1` is private PMM Engine Codex parity on model and routing outcomes. It does not claim
  that Codex now has Claude's receipt-bound promotion transaction layer.
- No public test should contain or process a real user's session content.
