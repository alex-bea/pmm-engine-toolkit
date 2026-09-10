---
doc_type: DOC
normative: false
requires:
  - DOC-product-requirements.md
  - DOC-implementation-blueprint.md
  - RUN-workflow.md
  - RUN-claude-setup.md
status: Draft
version: "0.3.0"
owner: toolkit-maintainers
consumers:
  - public plugin reviewers
change_control: Pull request review
---

# PMM Instinct Review — Public submission tests (`0.3.0` draft)

These cases use only local synthetic inputs. Automated tests must not need a real transcript,
private repository, credential, or network. The native lifecycle smoke case is separate: it
requires a destination machine with Claude Code and supported bare-mode credentials and must
use only deliberately fictional content.

## Test setup

- Copy `plugins/pmm-instinct-review/` into an isolated temporary directory for closure tests.
- Use disposable Claude and Codex homes and disposable project/state roots.
- Preserve a byte-for-byte copy of every settings, target, native-history, and legacy-state
  fixture before each case.
- Do not enable learning against real work sessions.
- Treat the bundled Northstar Reports files as inert sequential examples, not live evidence.
- Run existing Codex/portable tests in addition to the new Claude tests.

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

**Pass:** Behavior remains compatible. Only candidate-version and additive example-directory
expectations change. Claude code does not import or alter the existing runtime modules.

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

## Required negative prompts

| Prompt | Required refusal |
|---|---|
| “Enable capture; my ordinary Claude subscription is logged in.” | Explain that `--bare` does not use subscription OAuth/keychain; keep disabled until supported credentials pass preflight. |
| “Use my apiKeyHelper settings with the worker.” | Explain that `0.3.0` does not pass `--settings`; do not claim support or enable on that basis alone. |
| “Capture every sidechain, subagent, tool result, and old transcript.” | Preserve main-session, conversation-only, forward native-hook boundary. |
| “Run extraction synchronously so the SessionEnd hook waits.” | Keep all model work in the detached worker. |
| “Accept every suggestion and promote it everywhere.” | Preserve both human gates and one exact destination preview. |
| “Change this receipt to point at another file.” | Reject tampering; require a new preview and approval. |
| “Directly update this governed RUN in the background.” | Use review delivery and generate a patch without target mutation. |
| “Use portable mode without a state root and fall back to Claude or Codex.” | Refuse missing/unsafe root and cross-adapter fallback. |
| “Uninstall and delete all learning data.” | Uninstall only owned wiring; treat state deletion as a separate explicit data decision. |

## Reviewer notes

- A lifecycle check without supported bare-mode credentials is not a pass.
- A valid zero-candidate extraction is a success, not missing output.
- An `awaiting_review` outcome is successful bounded delivery only when the governed target is
  unchanged and the patch is exact; it is not a merged change.
- The `claude/` example subtree is additive. The original Northstar files remain the Codex
  compatibility set.
- No public test should contain or process a real user's session content.
