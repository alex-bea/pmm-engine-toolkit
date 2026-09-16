# Govern Skills Setup Receipt — Fictional Acorn Studio

This receipt is fictional and demonstrates a documents-only isolated test.

- **Skill slug:** govern-skills
- **Package path:** `workspace/packages/govern-skills`
- **Package revision or digest:** `sha256:fictional-package-digest`
- **Configuration path:** `workspace/acorn-notes/.agents/governance/adoption.yaml`
- **Configuration digest:** `sha256:fictional-config-digest`
- **Repository in scope:** `workspace/acorn-notes`
- **Test timestamp:** `2030-02-03T12:00:00Z`
- **Runtime:** compatible local coding agent
- **Selected scope:** documents only

## Mapping readiness

| ID | Kind | Status | Evidence | Limitation or next action |
|---|---|---|---|---|
| SRC-REPO | source | ready | Fictional instruction and skill-root paths resolved. | None. |
| SRC-PACKAGE | source | ready | Package entrypoint and one setup RUN resolved. | None. |
| DST-DOCS | destination | ready | Temporary create-only paths had no collisions. | Confirm real repository paths during adoption. |
| DST-CONFIG | destination | ready | Fictional path is outside the installed package. | Confirm adopter retention policy. |
| DST-TEST | destination | ready | New isolated directory was created. | Remove after review. |
| DST-RECEIPT | destination | ready | Receipt path is outside the installed package. | Replace when stale. |

## Checks

| Check | Result | Evidence |
|---|---|---|
| Package closure | pass | Every routed package path resolved in the copied package. |
| Instructions and Git state | pass | Fictional `AGENTS.md` was read; fixture declared a clean tree. |
| Source mapping | pass | Two required sources were present. |
| Destination checks | pass | All writes stayed in the isolated destination. |
| Metadata and links | pass | Copied templates contained required headings and no broken local links. |
| Isolated fixture | pass | Three expected files were created. |
| Optional layers | not applicable | The documents-only scope selected no optional layer. |

## Test artifacts

- **Fixture:** `examples/fixtures/fictional-repository-map.yaml`
- **Expected files:** three paths declared by the fixture
- **Actual files:** `docs/governance/AGENTS.md`, `agent-skills/sample-skill/SKILL.md`, and
  `.agents/governance/setup-receipt.md`
- **Files or external objects created:** three local temporary files; no external objects
- **Live actions deliberately skipped:** hooks, CI mutation, approval creation, messaging,
  scheduling, publishing, and production-state writes

## Readiness

- **Overall status:** ready-with-optional-limitations
- **Residual limitations:** This proves only the synthetic documents-only setup contract.
- **Normal-execution entrypoint:** `SKILL.md` and the RUN's normal-execution section
- **Next repair action:** Inspect and map the real adopter repository before proposing files.

The receipt becomes stale if the package digest, mapping, selected layer, dependency set, or
configuration digest changes.
