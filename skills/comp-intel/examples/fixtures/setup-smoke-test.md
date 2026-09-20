# Fictional Comp Intel Setup Smoke Test

> **Fictional fixture:** Every market, identity, path, mapping, source, digest, and output in
> this test is invented. The fixture is not a live default and does not authorize organization
> source access.

## Scenario

Install a copied `comp-intel` package under `test-install/skills/comp-intel/` and create a
separate empty `test-workspace/`. Configure the bundled `synthetic-devtools` market using only
the synthetic and local JSON fixtures shipped in the package. Stop collection at
`evidence_review`; do not create an evidence approval or apply registry changes.

The completed fictional setup files are:

- `examples/fixtures/setup-config.yaml`
- `examples/fixtures/setup-receipt.yaml`

## Isolation requirements

- The copied install root and test workspace are different directories.
- Neither path is a production repository, production data root, or private authoring source.
- The controller data root begins empty.
- Live web, communication, repository-host, CRM, publication, messaging, notifications,
  scheduling, approval creation, and production writes are disabled.
- Only the temporary workspace may receive writes.

## Source mapping

| Source ID | Purpose | Kind | Locator | Authorization method | Data class | Required | Read check |
|---|---|---|---|---|---|---|---|
| CI-TEST-SYNTHETIC | Deterministic public-source simulation | local fixture | copied data root `fixtures/synthetic-source.json` | bundled fictional fixture | synthetic | yes | JSON contains a `pages` array. |
| CI-TEST-LOCAL | Adopter-local evidence simulation | local fixture | copied data root `local/local-source.json` | isolated test filesystem | synthetic | no | File is contained by the configured data root. |
| CI-TEST-LIVE | Prove live integrations are off | none | none | not configured | synthetic | no | No live adapter or credential is present. |

## Output destinations

| Destination ID | Artifact | Location | Write mode | Visibility | Retention | External approval | Required | Write check |
|---|---|---|---|---|---|---|---|---|
| CI-TEST-SETUP | Fictional setup state | `test-workspace/.pmm-skills/comp-intel/` | create | private synthetic | test duration | no | Path is outside the package. |
| CI-TEST-DATA | Controller state and evidence-review artifacts | `test-workspace/.comp-intel/` | create | private synthetic | test duration | no | Path begins empty and is outside the package. |
| CI-TEST-EXTERNAL | Publication or message | none | external publish | external | none | yes | Fail closed; no adapter or authorization exists. |

## Procedure

1. Copy the complete package to the fictional install root and record a recursive package
   digest or clean diff.
2. Create the separate empty test workspace.
3. Copy the fictional setup config into
   `test-workspace/.pmm-skills/comp-intel/setup-config.yaml` and replace only its fictional
   install/workspace paths and calculated digests.
4. From the copied package, initialize the test controller data root:

   ```text
   python3 test-install/skills/comp-intel/scripts/comp_intel.py init \
     --data-root test-workspace/.comp-intel --json
   ```

5. Validate and probe the bundled market:

   ```text
   python3 test-install/skills/comp-intel/scripts/validate_comp_intel.py \
     --data-root test-workspace/.comp-intel --market synthetic-devtools

   python3 test-install/skills/comp-intel/scripts/comp_intel.py doctor \
     --data-root test-workspace/.comp-intel --market synthetic-devtools --json
   ```

6. Collect the fictional absolute window and stop at evidence review:

   ```text
   python3 test-install/skills/comp-intel/scripts/comp_intel.py collect \
     --data-root test-workspace/.comp-intel \
     --market synthetic-devtools \
     --from 2026-08-18 --to 2026-08-26 \
     --observed-at 2026-08-26T12:00:00Z \
     --run-id run_setup_smoke --json
   ```

7. Confirm the run stage is `evidence_review`, the evidence manifest and coverage exist, and
   no approval or applied registry change exists.
8. Write the fictional receipt only after package closure, mappings, reviewer policy,
   destination safety, validation, and smoke-test checks pass.
9. Compare the copied package with the recorded digest or diff. It must be unchanged.

## Routing cases

| Case | Fixture change | Expected status | Expected route |
|---|---|---|---|
| CI-ROUTE-READY | Configuration and receipt identities match; required checks are true. | `ready` | Enter `references/RUN-workflow.md`; do not load detailed setup or rerun this fixture. |
| CI-ROUTE-MISSING | Remove the receipt or a required mapping. | `missing` | Load the setup contract and stop before live collection. |
| CI-ROUTE-STALE | Change configuration revision or package/configuration digest without replacing the receipt. | `stale` | Load repair guidance; preserve existing controller data. |
| CI-ROUTE-BLOCKED | Make a required fixture unreadable or move a required destination inside the package. | `blocked` | Report the failed check; do not collect or write production state. |

Changing only `installed_at` or `verified_at` does not make a matching receipt stale.

## Expected artifacts

- `test-workspace/.pmm-skills/comp-intel/setup-config.yaml`
- `test-workspace/.pmm-skills/comp-intel/setup-receipt.yaml`
- `test-workspace/.comp-intel/config.json`
- `test-workspace/.comp-intel/markets/synthetic-devtools.json`
- `test-workspace/.comp-intel/runs/run_setup_smoke/run.json`
- `test-workspace/.comp-intel/runs/run_setup_smoke/collection/evidence-manifest.json`
- `test-workspace/.comp-intel/runs/run_setup_smoke/reviews/evidence-review.md`

No evidence approval, synthesis package, applied registry mutation, published report, message,
notification, schedule, external approval, or production artifact is expected.

## Pass conditions

- Package resources and all package-relative links resolve.
- Exactly one normal RUN exists and the setup contract is a REF.
- Required fictional sources and local destinations validate.
- Collection stops at `evidence_review` with explicit coverage and limitations.
- All four routing cases match the contract.
- The copied installed package is unchanged.
- No external side effect or production-state write occurs.
