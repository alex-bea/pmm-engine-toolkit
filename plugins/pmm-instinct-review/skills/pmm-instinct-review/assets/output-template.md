# PMM Instinct Review output templates

Use the section that matches the active runtime. Omit inapplicable fields rather than
pretending an unavailable stage succeeded. Paths belong to the adopter; never copy a
fictional example path into live state.

## Read-only status receipt

- **Runtime/adapter:** `claude|codex|portable`
- **Capture supported:** `true|false`
- **Enabled:** `true|false`
- **Privacy acknowledged:** `true|false|not applicable`
- **State root:** [exact adopter-owned path]
- **Extractor model:** [exact configured model or not applicable]
- **Model policy:** `true|false|not applicable`
- **Extractor executable:** [resolved path, unavailable, or not applicable]
- **Queue:** [state counts for the selected runtime]
- **Backlog:** [zero-candidate, positive-cluster, and missing-suggestion counts]
- **Promotion:** [approved, pending execution, promoted, covered, awaiting review, failed, invalid]
- **Extraction available:** `true|false`
- **Approval-bound promotion available:** `true|false`
- **Human approval required:** `true`
- **Notes/blockers:** [only observed facts]

For a legacy Codex store that is enabled but has no persisted model, report
`model_policy: false` and the exact remediation `on --model <exact-model>`. A skipped capture reports
`status: skipped` and `reason: unconfigured_model`; it must not claim that evidence, an audit,
or a queue record was created.

## Claude standalone setup receipt

- **Toolkit checkout/revision:** [path and revision when known]
- **Installation mode:** `symlink|copy`
- **Active bundle:** [exact path]
- **Personal skill:** [exact path and discovery result]
- **Package closure:** [manifest, skill, hooks, scripts, assets, references]
- **Settings file:** [exact path]
- **Settings backup:** [path or not created]
- **Installation receipt:** [schema, digest, `receipt_valid`, `skill_target_valid`,
  `bundle_valid`, `installation_valid`, ambiguous-handler count]
- **Owned hooks:** `SessionStart` [status], `SessionEnd` [status]
- **Unrelated settings preserved:** `true|false`
- **Privacy decision:** `enabled|declined|not yet decided`
- **Capture enabled:** `true|false`
- **Claude-owned state root:** [exact path]
- **Extractor model:** [exact configured model]
- **Lifecycle smoke check:** `passed|failed|not run`, with observed result
- **Extraction available:** `true|false`
- **Receipt-bound promotion execution available:** `true|false`
- **State preserved on disable/uninstall:** `true`
- **Update/disable/uninstall:** [exact next commands]

Do not say the setup passed unless `/skills`, `/hooks`, an eligible fictional session, and
detached extraction were checked on the destination Claude machine.

## Backlog bucket summary

- **Zero-candidate audits:** [count and audit paths or IDs]
- **Positive clusters:** [count; each cluster's type, support, skill/cwd breadth, priority]
- **Missing suggestions:** [count and audit paths or IDs]

## Instinct review candidate

- **What happened:** [evidence-bound situation]
- **User feedback:** [short redacted evidence]
- **Proposed future behavior:** [one atomic rule]
- **Why it matters:** [evidence-bound consequence, maximum 300 characters]
- **Support/source:** [session count, source skills, source repositories/cwds]
- **Exact match state:** `new|exact`
- **Decision:** `accept|reject|edit|match`
- **Confirmation:** [explicit user confirmation]

Destination routing is intentionally excluded from this candidate-to-instinct decision.

## Claude promotion preview

- **Instinct ID:**
- **Source-guidance SHA-256:**
- **Destination class:** `global|project|skill|standard`
- **Delivery:** `local|review`
- **Exact target path:**
- **Current target SHA-256:**
- **Rule:**
- **Why it matters:**
- **Managed section:** `## PMM Instinct Review — Promoted Guidance`
- **Exact insertion:**
- **Exact resulting text:**
- **Resulting SHA-256:**
- **Duplicate:** `true|false`
- **Preview digest:**
- **Separate confirmation required:** `true`

## Claude promotion approval receipt

- **Preview digest:**
- **Approved at:**
- **Approved action:** [the unchanged unsigned preview payload]
- **Receipt digest:**
- **Receipt path:** [shown by the command; not part of the immutable receipt payload]

Approval is valid only when the target still has the previewed digest and the canonical
preview digest verifies. Editing any bound value requires a new preview and approval.

## Claude promotion outcome

- **Receipt digest:**
- **Status:** `promoted|covered|awaiting_review|failed`
- **Target path:**
- **Resulting SHA-256:** [local delivery]
- **Changeset path:** [governed review delivery]
- **Completed/created/failed at:**
- **Sanitized error:** [failed only]
- **Bookkeeping warning:** [optional; target applied but instinct metadata update failed]

`awaiting_review` means the target was not changed. The generated patch must go through the
destination repository's normal review and approval process.

## Codex ambiguous RUN/REF selection

- **Applicable:** `false`
- **Reason:** `multiple-eligible-targets`
- **Destination:** `run|ref`
- **Eligible targets:** [ordered exact absolute paths validated for the source skill]
- **Target changed:** `false`
- **Applicable preview persisted:** `false`
- **Next command:** repeat `promote` with the same instinct and destination plus
  `--target <exact-eligible-path>`

Do not render the first path as a recommendation. An eligible target is a bounded choice, not
authorization to apply it.

## Codex applicable promotion preview

- **Applicable:** `true`
- **Instinct ID:**
- **Destination:** `project|global|both|run|ref|standard`
- **Exact target path(s):**
- **Rule:**
- **Why it matters:**
- **Managed section:** `## PMM Instinct Review — Promoted Guidance`
- **Exact insertion:**
- **Duplicate:** `true|false` for each target
- **Separate confirmation required:** `true`

RUN or REF preview with `--target` is applicable only when that exact absolute path remains in
the recomputed eligible set. Apply still requires the same arguments, a matching saved preview,
`--apply`, and `--confirm`.
