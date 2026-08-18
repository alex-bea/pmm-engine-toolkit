# Evidence and Privacy Standard v1.0

## Rules

1. Use only user-supplied, repository-local, or explicitly approved sources.
2. Attribute material claims to a source; represent missing facts as `[Missing]`.
3. Never embed credentials, account IDs, private channel IDs, customer data, or personal
   profiles in a skill package.
4. Create person-specific output only from consented inputs and only for the stated use.
5. Use synthetic organizations and people in examples.
6. Keep external connectors optional. A connector may retrieve evidence, but may not
   publish, message, schedule, or mutate external state without explicit approval.
7. Treat legal, financial, health, security, compliance, and availability claims as
   requiring an owner-approved source and qualified review.

## Evidence labels

- `Verified` — directly supported by a cited source.
- `Reported` — present in supplied material but not independently validated.
- `Inference` — analysis derived from multiple cited observations.
- `[Missing]` — decision-critical information is absent.
