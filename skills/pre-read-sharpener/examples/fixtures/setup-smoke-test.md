# Fictional Pre-Read Sharpener Conditional Setup Test

> **Fictional setup fixture:** Every path, digest, timestamp, mapping, and result below is
> invented for a non-destructive local test. The Harborline source and output are bundled
> synthetic examples. Nothing in this file is a default for a real installation.

## Scenario

An adopter copied the complete package to `test-install/pre-read-sharpener/` and uses a
separate `test-workspace/`. A compatible local agent may read the copy and write only below
the fictional workspace. Network access and every external mutation are disabled.

The test verifies both supported normal routes:

- inline work bypasses setup and creates no local file; and
- persistent work uses a current receipt, writes collision-safe outputs, and does not rerun
  setup or mutate configuration, receipt, or installed package files.

## Fictional completed configuration

```yaml
schema_version: 1
skill_slug: "pre-read-sharpener"
setup_profile: "local-persistence"
package:
  path: "test-install/pre-read-sharpener"
  revision: "fictional-candidate-revision"
  digest: "sha256:1111111111111111111111111111111111111111111111111111111111111111"
sources:
  - id: "PRS-SRC-DRAFT"
    kind: "paste-or-authorized-local-file"
    locator: "per-run-input"
    authorization_method: "user-supplied-content-or-local-filesystem"
    required: true
  - id: "PRS-SRC-FIXTURE"
    kind: "package-local-file"
    locator: "examples/fictional-rollout-decision/source-draft.md"
    authorization_method: "local-filesystem-read"
    required_for_setup_test: true
destinations:
  - id: "PRS-DST-OUTPUT"
    location: "test-workspace/outputs/pre-reads"
    write_mode: "create-or-update-known-edit"
    required_for_persistence: true
  - id: "PRS-DST-CONFIG"
    location: "test-workspace/.pmm-skills/pre-read-sharpener/setup-config.yaml"
    write_mode: "create-or-confirmed-update"
    required_for_persistence: true
  - id: "PRS-DST-RECEIPT"
    location: "test-workspace/.pmm-skills/pre-read-sharpener/setup-receipt.yaml"
    write_mode: "create-or-confirmed-replace"
    required_for_persistence: true
  - id: "PRS-DST-TEST"
    location: "test-workspace"
    write_mode: "create-test-artifacts"
    required_for_setup_test: true
timezone: "UTC"
retention: "test-duration"
receipt_path: "test-workspace/.pmm-skills/pre-read-sharpener/setup-receipt.yaml"
configuration_revision: "fictional-revision-1"
```

## Source mapping

| Source ID | Purpose | Kind | Locator | Authorization method | Data class | Required | Read check |
|---|---|---|---|---|---|---|---|
| PRS-SRC-DRAFT | Normal input mode | paste or authorized local file | one per-run input | user-supplied content or local filesystem | adopter-owned, potentially confidential | yes for normal work | No retrieval fallback is configured. |
| PRS-SRC-FIXTURE | Test input | package-local file | `examples/fictional-rollout-decision/source-draft.md` | local filesystem read | synthetic | yes for test | File resolves inside the copy and is labeled fictional. |
| PRS-SRC-EXTERNAL | External evidence | none | none | none | none | no | No connector, browser, or secondary source exists. |

## Output destinations

| Destination ID | Artifact | Location | Write mode | Visibility | Retention | External approval | Required | Write check |
|---|---|---|---|---|---|---|---|---|
| PRS-DST-INLINE | Complete result | current response | inline | conversation | test duration | no | yes | No local or external write occurs. |
| PRS-DST-OUTPUT | Fictional pre-reads | `test-workspace/outputs/pre-reads/` | create with numeric collision suffixes | private synthetic | test duration | no | for persistence | Parent is outside the copy and writable. |
| PRS-DST-CONFIG | Fictional configuration | `test-workspace/.pmm-skills/pre-read-sharpener/setup-config.yaml` | create | private synthetic | test duration | no | for persistence | Parent is outside the copy and writable. |
| PRS-DST-RECEIPT | Fictional receipt | `test-workspace/.pmm-skills/pre-read-sharpener/setup-receipt.yaml` | create | private synthetic | test duration | no | for persistence | Parent is outside the copy and writable. |
| PRS-DST-TEST | Test artifacts | `test-workspace/` | create | private synthetic | test duration | no | yes for test | Directory is new and not a production root. |
| PRS-DST-EXTERNAL | Publishing, messaging, notifications, scheduling, or approvals | none | forbidden | none | none | separate approval and adapter required | no | No external destination or publisher exists. |

## Test procedure

1. Copy only the candidate package to `test-install/pre-read-sharpener/` and hash every
   copied file.
2. Confirm there is one RUN named `RUN-pre-read-sharpener-workflow.md`, the separate setup
   contract exists, and every required package-relative resource resolves.
3. Run the bundled fictional source on the `inline` route. Confirm a complete ordered
   result with ten passing criteria and no configuration, receipt, or output file.
4. Copy `assets/setup-config.yaml` to the fictional configuration path and fill it with the
   values above.
5. Read only `examples/fictional-rollout-decision/source-draft.md` and write the complete
   fictional review under `test-workspace/outputs/pre-reads/` using the execution date and
   slug `approve-the-four-week-guided-import-expansion`.
6. Repeat the initial persistent save once. Confirm the second file uses `-2.md` and the
   first file remains unchanged.
7. Validate the result against the bundled template, criteria, and fictional completed
   example. Prose need not be byte-identical, but every factual statement must trace to the
   fictional source.
8. Write the completed receipt below. Snapshot configuration and receipt digests.
9. Run one more persistent request through the `ready` route. Confirm it enters the normal
   RUN without loading setup detail or rerunning this fixture and does not change setup
   configuration or receipt files.
10. Exercise routing probes: absent receipt is `missing`; changed package or configuration
    digest is `stale`; a failed required write or fixture check is `blocked`.
11. Re-hash the copied package and confirm it is unchanged.

## Expected artifacts and invariants

- `test-workspace/.pmm-skills/pre-read-sharpener/setup-config.yaml`
- `test-workspace/.pmm-skills/pre-read-sharpener/setup-receipt.yaml`
- `test-workspace/outputs/pre-reads/{execution-date}-approve-the-four-week-guided-import-expansion-pre-read.md`
- `test-workspace/outputs/pre-reads/{execution-date}-approve-the-four-week-guided-import-expansion-pre-read-2.md`
- a full ordered deliverable with ten passing criteria;
- a `ready` route that leaves configuration and receipt content unchanged;
- correct `missing`, `stale`, and `blocked` routing results;
- identical installed-package hashes before and after, proving the installed package is unchanged; and
- no production source, output, configuration, receipt, network service, publisher,
  notification, schedule, message, or approval read or mutation.

## Fictional completed receipt

```yaml
schema_version: 1
skill_slug: "pre-read-sharpener"
status: "ready"
installed_at: "2026-10-02T09:00:00Z"
verified_at: "2026-10-02T09:05:00Z"
package_revision: "fictional-candidate-revision"
package_digest: "sha256:1111111111111111111111111111111111111111111111111111111111111111"
setup_contract_version: "1.0"
configuration_path: "test-workspace/.pmm-skills/pre-read-sharpener/setup-config.yaml"
configuration_digest: "sha256:2222222222222222222222222222222222222222222222222222222222222222"
checks:
  package_closure: "passed"
  source_mapping: "passed"
  destination_mapping: "passed"
  local_permissions: "passed"
  fictional_fixture: "passed"
  package_unchanged: "passed"
limitations: []
normal_entrypoint: "references/RUN-pre-read-sharpener-workflow.md"
next_repair_action: "none"
```

This receipt is fictional schema evidence, not proof of a real installation. Conditional
routing is instruction-only because the package has no mandatory dispatcher.
