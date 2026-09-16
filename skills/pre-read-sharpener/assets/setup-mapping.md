# Pre-Read Sharpener Setup Mapping

> Blank adopter template. Copy this file to a confirmed path such as
> `{authorized-workspace}/.pre-read-sharpener/setup.md` and complete the copy. Do not store
> adopter configuration or source locators inside the installed skill package.

## Package

- **Installed package path:** `{installed-skill-directory}`
- **Package revision or digest:** `{package-revision-or-digest}`
- **Compatible agent runtime:** `{runtime-name-and-version-if-available}`
- **Timezone for dated filenames:** `{IANA-timezone}`
- **Configuration retention:** `{adopter-selected-retention}`
- **Generated pre-read retention:** `{adopter-selected-retention}`

## Source mapping

| Source ID | Purpose | Kind | Locator | Authorization method | Data class | Required | Read check |
|---|---|---|---|---|---|---|---|
| PRS-SRC-DRAFT | One pre-read for normal execution | `{paste, attachment, or authorized local file}` | `{literal-input or adopter-confirmed path}` | `{user-supplied content or local filesystem authorization}` | `{adopter-selected classification}` | yes | Confirm one non-empty, readable pre-read and no retrieval fallback. |
| PRS-SRC-FIXTURE | Bundled setup-test input | package-local file | `examples/fictional-rollout-decision/source-draft.md` | local filesystem read access | synthetic | yes for setup test | Resolve inside the package and confirm the fictional-source label. |
| PRS-SRC-EXTERNAL | External evidence or retrieval | none | none | none | none | no | Confirm no connector or undeclared fallback is configured. |

## Output destinations

| Destination ID | Artifact | Location | Write mode | Visibility | Retention | External approval | Required | Write check |
|---|---|---|---|---|---|---|---|---|
| PRS-DST-OUTPUT | Passing pre-read deliverables | `{authorized-workspace}/outputs/pre-reads/` | create; update only a known artifact for an explicit edit | `{private or team}` | `{adopter-selected}` | no external approval; local path confirmation required | yes | Confirm the parent is outside the package and writable; preserve initial collisions with numeric suffixes. |
| PRS-DST-CONFIG | This completed mapping | `{authorized-workspace}/.pre-read-sharpener/setup.md` | create or explicitly update | private | while setup is active | no external approval; local path confirmation required | yes | Confirm the parent is outside the package and do not overwrite an unknown differing file. |
| PRS-DST-RECEIPT | Setup readiness receipt | `{authorized-workspace}/.pre-read-sharpener/receipts/setup-receipt.md` | create or replace after a confirmed setup rerun | private | with active configuration | no external approval; local path confirmation required | yes | Confirm the parent is outside the package and writable. |
| PRS-DST-TEST | Isolated setup-test artifacts | `{new-temporary-workspace}` | create; optionally remove after review | private synthetic | test duration unless retained | no | Confirm the directory is empty, writable, outside the package, and not a production root. |
| PRS-DST-EXTERNAL | Publication, message, notification, schedule, or external approval | none | forbidden by this workflow | none | none | separate target-specific approval and adapter required | no | Confirm no external destination or callable publisher is configured. |

## Permissions and boundaries

- **Package read mechanism:** `{authorization-mechanism}`
- **Draft read mechanism:** `{authorization-mechanism}`
- **Local write mechanism:** `{authorization-mechanism}`
- **Credential values stored:** no
- **Publishing enabled:** no
- **Messaging or notifications enabled:** no
- **Scheduling enabled:** no
- **External approval creation enabled:** no
- **Production-state writes during setup test:** no

## Test configuration

- **Fixture:** `examples/fixtures/setup-smoke-test.md`
- **Input:** `examples/fictional-rollout-decision/source-draft.md`
- **Expected content shape:** `examples/fictional-rollout-decision/review-and-rewrite.md`
- **Temporary destination:** `{new-temporary-workspace}`
- **Collision check:** `{enabled or disabled with reason}`
- **Receipt destination:** `{new-temporary-workspace}/.pre-read-sharpener/receipts/setup-receipt.md`

## Confirmation

- **Confirmed by:** `{adopter-or-authorized-operator}`
- **Confirmed at:** `{ISO-8601-timestamp}`
- **Configuration digest:** `{sha256-of-completed-mapping}`

Any change to a required mapping, package revision, dependency set, or configuration digest
makes the prior setup receipt stale.
