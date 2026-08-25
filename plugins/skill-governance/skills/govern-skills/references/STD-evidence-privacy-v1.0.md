---
doc_type: STD
normative: true
requires: []
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Codex users
  - skill authors
change_control: Pull request review
---

# Evidence and Privacy Standard

## Rules

1. Use only user-supplied, repository-local, public, or explicitly approved sources.
2. Attribute material claims to a source and represent absent decision-critical facts as
   `[Missing]`.
3. Never embed credentials, account IDs, private channel IDs, customer data, personal data,
   or private profiles in a reusable skill package.
4. Create person-specific output only from consented inputs and only for the stated use.
5. Use synthetic organizations and people in examples.
6. Keep external connectors optional. Retrieval permission does not grant permission to
   publish, message, schedule, or mutate external state.
7. Require an owner-approved source and qualified review for legal, financial, health,
   security, compliance, availability, or other high-stakes claims.
8. Preserve uncertainty and conflicting evidence instead of forcing a conclusion.

## Evidence labels

- `Verified` — directly supported by a cited source.
- `Reported` — present in supplied material but not independently validated.
- `Inference` — analysis derived from cited observations.
- `[Missing]` — decision-critical information is absent.
