# PMM Instinct Review plugin IP-rights review — 2026-08-25

Status: draft pending pull-request approval.

## Result

The plugin release candidate is suitable for inclusion under the toolkit's Apache-2.0 license,
subject to pull-request approval. Every release-candidate artifact is included in
[`IP-INVENTORY.csv`](IP-INVENTORY.csv) with provenance, third-party-content classification,
redistribution basis, and an `include` disposition.

## Review basis

- The plugin runtime, hooks, schemas, documentation, product requirements, implementation
  blueprint, submission test cases, synthetic examples, tests, marketplace record, and
  governance changes are project-authored in the public fresh-history repository.
- No private chats, audits, instincts, configuration, runtime state, private repository files,
  or private Git history were copied into the release candidate.
- The implementation uses Python's standard library only and vendors no package source,
  model output, binary, dataset, transcript, or media asset.
- GitHub, Codex, OpenAI, ChatGPT, macOS, and Python appear only as nominative compatibility or
  installation references. No logos, screenshots, slogans, or product collateral are included.
- Public documentation links to the toolkit repository and official Codex documentation; linked
  content is not embedded.
- The previous ScanCode 32.5.0 baseline remains documented in
  [`IP-RIGHTS-REVIEW-2026-08-18.md`](IP-RIGHTS-REVIEW-2026-08-18.md). The new text-only source
  artifacts were reviewed through the regenerated path-by-path inventory and manual attribution
  review; ScanCode was not installed in this checkout and was not rerun locally.

## Migration disposition

The retired standalone `skills/pmm-instinct-review/` package was project-authored under the same
repository license. Its explicit-candidate behavior was reimplemented inside the plugin; no
private runtime implementation or private test fixture was copied into the public tree.

## Publication conditions

- Keep the release marked draft until pull-request review approves publication.
- Keep `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md`, and the generated IP inventory with the
  source distribution.
- Regenerate the inventory whenever release-candidate paths change.
- Require a fresh rights review for externally sourced examples, quotations, images, binaries,
  datasets, or vendored code.

This is a repository-content review, not legal advice.
