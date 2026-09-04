# Governed workflow rules

These instructions define repository policy. They are not, by themselves, a security
boundary. Enable the repository's validated hooks, protected CI, capability restrictions,
external approval verifier, and publisher guard before describing runtime governance as
active.

For each schema-version-2 workflow run:

1. Validate the run before preparing or changing its next stage.
2. Treat the configured external authority as the only source of human approval.
3. Keep every approval bound to the exact reviewed revision, artifact path, and SHA-256
   digest.
4. Allow scheduled workers to collect only declared staging evidence and stop at
   `evidence_review`.
5. Deny scheduled approval creation, human-gate transitions, `publish_ready`, and
   publication.
6. Publish only through the approved publisher guard after it re-verifies state, approval,
   and digest.
7. Keep policy, verifier configuration, publisher configuration, and credentials outside
   agent-writable paths or mount them read-only.
