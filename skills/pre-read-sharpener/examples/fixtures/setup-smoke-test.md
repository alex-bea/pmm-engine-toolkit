# Fictional Pre-Read Sharpener Setup Smoke Test

> **Fictional setup fixture:** Every path, digest, timestamp, mapping, and result below is
> invented for a non-destructive local test. The Harborline source and output are bundled
> synthetic examples. Nothing in this file is a default for a real installation.

## Scenario

An adopter has copied the complete `pre-read-sharpener` package to
`test-install/pre-read-sharpener/`. The adopter wants to verify the package before supplying
a real draft. A compatible local agent may read the copied package and write only beneath a
new `test-workspace/` directory. Network access and every external mutation are disabled.

## Source mapping

| Source ID | Purpose | Kind | Locator | Authorization method | Data class | Required | Read check |
|---|---|---|---|---|---|---|---|
| PRS-SRC-DRAFT | Normal pre-read input mode after setup | paste or authorized local file | User supplies one draft per run. | user-supplied content or local filesystem authorization | adopter-owned, potentially confidential | yes for normal execution | Deferred during the smoke test; confirm no retrieval fallback is configured. |
| PRS-SRC-FIXTURE | Smoke-test input | package-local file | `examples/fictional-rollout-decision/source-draft.md` | local filesystem read access | synthetic | yes for setup test | File resolves inside the copied package and starts with a fictional-source label. |
| PRS-SRC-EXTERNAL | External evidence or retrieval | none | none | none | none | no | No connector, browser, or secondary source is available. |

## Output destinations

| Destination ID | Artifact | Location | Write mode | Visibility | Retention | External approval | Required | Write check |
|---|---|---|---|---|---|---|---|---|
| PRS-DST-OUTPUT | Fictional pre-read results | `test-workspace/outputs/pre-reads/` | create with numeric collision suffixes | private synthetic | test duration | no | yes | Parent is outside the copied package, empty at start, and writable. |
| PRS-DST-CONFIG | Completed fictional setup mapping | `test-workspace/.pre-read-sharpener/setup.md` | create | private synthetic | test duration | no | yes | Parent is outside the copied package and writable. |
| PRS-DST-RECEIPT | Fictional setup receipt | `test-workspace/.pre-read-sharpener/receipts/setup-receipt.md` | create | private synthetic | test duration | no | yes | Parent is outside the copied package and writable. |
| PRS-DST-TEST | All smoke-test artifacts | `test-workspace/` | create | private synthetic | test duration | no | yes | Directory is new, isolated, writable, and not a production root. |
| PRS-DST-EXTERNAL | Publication, messages, notifications, schedules, or approvals | none | forbidden | none | none | separate approval and adapter would be required | no | No external destination or callable publisher exists. |

## Configuration

- **Installed package path:** `test-install/pre-read-sharpener/`
- **Package revision or digest:** `sha256:1111111111111111111111111111111111111111111111111111111111111111`
- **Compatible agent runtime:** `fictional-compatible-local-agent`
- **Timezone for dated filenames:** `UTC`
- **Configuration path:** `test-workspace/.pre-read-sharpener/setup.md`
- **Configuration digest:** `sha256:2222222222222222222222222222222222222222222222222222222222222222`
- **Generated pre-read retention:** test duration
- **Setup-record retention:** test duration
- **Publishing enabled:** no
- **Messaging or notifications enabled:** no
- **Scheduling enabled:** no
- **External approval creation enabled:** no
- **Production-state writes enabled:** no

## Test procedure

1. Copy only the candidate skill directory to `test-install/pre-read-sharpener/`.
2. Verify the package contains one RUN file named
   `RUN-pre-read-sharpener-setup-workflow.md` and every required local resource resolves.
3. Write this fictional mapping to `test-workspace/.pre-read-sharpener/setup.md`.
4. Read only `examples/fictional-rollout-decision/source-draft.md` from the copied package.
5. Run section `## 10. Normal execution` with the fictional source.
6. Save the passing result under `test-workspace/outputs/pre-reads/` using the execution
   date and the slug `approve-the-four-week-guided-import-expansion`.
7. Repeat the initial save once to verify the second file receives the `-2` suffix and the
   first file is unchanged.
8. Validate the output structure and source discipline against the bundled template,
   criteria, and completed fictional example. Prose need not be byte-identical.
9. Write the receipt shown below to the fictional receipt destination.

## Expected artifacts and invariants

- `test-workspace/.pre-read-sharpener/setup.md` exists outside the installed package.
- `test-workspace/outputs/pre-reads/{execution-date}-approve-the-four-week-guided-import-expansion-pre-read.md`
  contains the full ordered deliverable and ten passing criteria.
- The repeated save creates the same stem with `-2.md` and does not alter the first file.
- `test-workspace/.pre-read-sharpener/receipts/setup-receipt.md` records the test and overall
  readiness.
- Every output fact traces to the bundled fictional source.
- The installed package is unchanged.
- No production source, output, configuration, receipt, network service, publisher,
  notification, schedule, message, or approval is read or mutated.

## Fictional completed setup receipt

### Identity

- **Skill slug:** pre-read-sharpener
- **Installed package path:** `test-install/pre-read-sharpener/`
- **Package revision or digest:** `sha256:1111111111111111111111111111111111111111111111111111111111111111`
- **Runtime:** `fictional-compatible-local-agent`
- **Test timestamp:** `2026-10-02T09:00:00Z`
- **Configuration path:** `test-workspace/.pre-read-sharpener/setup.md`
- **Configuration digest:** `sha256:2222222222222222222222222222222222222222222222222222222222222222`

### Mapping readiness

| ID | Kind | Required | Status | Evidence or limitation |
|---|---|---|---|---|
| PRS-SRC-DRAFT | source | yes for normal execution | pass | User-supplied paste or authorized local-file mode is configured; no locator is stored in this receipt. |
| PRS-SRC-FIXTURE | source | yes for setup test | pass | Bundled fictional source resolved from the copied package. |
| PRS-SRC-EXTERNAL | source | no | skipped | No external source exists; skipped by design. |
| PRS-DST-OUTPUT | destination | yes | pass | Temporary output root was writable and collision-safe. |
| PRS-DST-CONFIG | destination | yes | pass | Fictional mapping was written outside the package. |
| PRS-DST-RECEIPT | destination | yes | pass | Receipt parent was writable outside the package. |
| PRS-DST-TEST | destination | yes for setup test | pass | A new isolated temporary workspace was used. |
| PRS-DST-EXTERNAL | destination | no | skipped | External mutation was disabled and no adapter existed. |

### Installation and permission checks

| Check | Status | Evidence or limitation |
|---|---|---|
| Package closure and sole RUN | pass | One setup-workflow RUN and every required file resolved. |
| Package-relative links | pass | All required package-local links resolved from the copied package. |
| Compatible agent runtime | pass | The fictional fixture completed through the documented local procedure. |
| Required source read access | pass | Only the bundled fictional source was read. |
| Required local destination write access | pass | Config, output, and receipt paths were writable. |
| External writes suppressed | pass | Publishing, messages, notifications, schedules, approvals, and production writes remained disabled. |

### Fixture execution

- **Fixture:** `examples/fixtures/setup-smoke-test.md`
- **Method:** copied-package compatible-agent execution
- **Expected artifacts:** setup mapping, two collision-safe fictional pre-reads, and setup receipt
- **Actual artifacts:** setup mapping, two collision-safe fictional pre-reads, and setup receipt
- **Output validation:** pass; full ordered deliverable, canonical rewrite, agenda, and ten passing criteria were present
- **Collision validation:** pass; the second initial save used `-2.md` and preserved the first file
- **Skipped live checks:** external source and external destination checks, both optional and absent by design

### Files created

- `test-workspace/.pre-read-sharpener/setup.md`
- `test-workspace/outputs/pre-reads/{execution-date}-approve-the-four-week-guided-import-expansion-pre-read.md`
- `test-workspace/outputs/pre-reads/{execution-date}-approve-the-four-week-guided-import-expansion-pre-read-2.md`
- `test-workspace/.pre-read-sharpener/receipts/setup-receipt.md`

### Result

- **Residual limitations:** none for required local operation
- **Overall status:** ready
- **Normal execution entrypoint:** `references/RUN-pre-read-sharpener-setup-workflow.md`, section `## 10. Normal execution`
- **Next repair action:** none

This completed receipt is fictional schema evidence, not proof of a real installation.
