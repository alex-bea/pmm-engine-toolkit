# Pre-Read Sharpener Setup Receipt

> Blank adopter template. Write the completed receipt to the confirmed adopter-owned receipt
> destination outside the installed skill package. Never record credentials or unnecessary
> sensitive locator values.

## Identity

- **Skill slug:** pre-read-sharpener
- **Installed package path:** `{installed-skill-directory}`
- **Package revision or digest:** `{package-revision-or-digest}`
- **Runtime:** `{compatible-agent-runtime}`
- **Test timestamp:** `{ISO-8601-timestamp}`
- **Configuration path:** `{adopter-owned-configuration-path}`
- **Configuration digest:** `{sha256-of-completed-configuration}`

## Mapping readiness

| ID | Kind | Required | Status | Evidence or limitation |
|---|---|---|---|---|
| `{source-or-destination-id}` | `{source or destination}` | `{yes or no}` | `{pass, fail, skipped, or unavailable}` | `{safe evidence without secrets or sensitive locator values}` |

## Installation and permission checks

| Check | Status | Evidence or limitation |
|---|---|---|
| Package closure and sole RUN | `{pass, fail, skipped, or unavailable}` | `{result}` |
| Package-relative links | `{pass, fail, skipped, or unavailable}` | `{result}` |
| Compatible agent runtime | `{pass, fail, skipped, or unavailable}` | `{result}` |
| Required source read access | `{pass, fail, skipped, or unavailable}` | `{result}` |
| Required local destination write access | `{pass, fail, skipped, or unavailable}` | `{result}` |
| External writes suppressed | `{pass, fail, skipped, or unavailable}` | `{result}` |

## Fixture execution

- **Fixture:** `examples/fixtures/setup-smoke-test.md`
- **Method:** `{compatible-agent-procedure}`
- **Expected artifacts:** `{expected-files}`
- **Actual artifacts:** `{actual-files-or-none}`
- **Output validation:** `{pass, fail, skipped, or unavailable plus evidence}`
- **Collision or update validation:** `{pass, fail, skipped, unavailable, or not applicable plus reason}`
- **Skipped live checks:** `{explicit-list-or-none}`

## Files created

- `{adopter-owned-or-temporary-path}`

## Result

- **Residual limitations:** `{explicit-list-or-none}`
- **Overall status:** `{ready, ready-with-optional-limitations, or blocked}`
- **Normal execution entrypoint:** `references/RUN-pre-read-sharpener-setup-workflow.md`, section `## 10. Normal execution`
- **Next repair action:** `{none-or-specific-action}`

This receipt is stale when the package revision or digest, required mapping, dependency set,
or configuration digest changes. Re-run the affected checks before normal execution.
