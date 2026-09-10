# Northstar Reports: fictional native Claude lifecycle

This directory is an independently authored, entirely fictional `0.3.0` example. It does not
rename or reproduce a real transcript. Northstar Reports, its release-summary workflow, all
identifiers, and every `/fictional/...` path exist only for documentation.

The directory combines documentary snapshots from different points in one lifecycle; it is
not a claim that every file coexists in terminal state. In particular, `evidence.json` is the
pre-review snapshot that the runtime deletes after the audit becomes `processed: true`.

## Lifecycle trace

1. [`installation-receipt.json`](installation-receipt.json) shows a symlink install with
   capture disabled and state preservation. The installer flow also adds the two owned hooks.
   [`config.json`](config.json) is a later snapshot after the fictional user explicitly
   acknowledges privacy and enables capture.
2. [`evidence.json`](evidence.json) contains five bounded fictional user turns and only
   user/assistant text. It shows one bearer-credential redaction as
   `Bearer [REDACTED TOKEN]`. A synthetic tool-result block
   in the imagined source transcript is intentionally absent. The native transcript itself is
   not distributed.
3. [`audit.md`](audit.md), [`queue.json`](queue.json), and
   [`suggestions.md`](suggestions.md) share job
   `nsr-claude-003-1bc3012bf455`. The job is completed after one detached attempt and
   produces one `voice` candidate.
4. [`review-decisions.json`](review-decisions.json) records an explicit `accept` decision for
   cluster `voice-a4e8533d9f91`. Its three occurrence records bind each fictional observation
   to its session, derived job, transcript, suggestion result, and pre-processing audit digests;
   only the final minimized evidence snapshot is included.
5. [`instinct.md`](instinct.md) shows the resulting confidence-eligible instinct and its later
   terminal `promoted` state.
6. [`promotion-preview.json`](promotion-preview.json) binds the exact project target, current
   target digest, insertion, full resulting text, and resulting digest. The separately
   confirmed [`promotion-receipt.json`](promotion-receipt.json) embeds that unchanged action.
7. [`CLAUDE-before.md`](CLAUDE-before.md) and [`CLAUDE-after.md`](CLAUDE-after.md) differ only
   by the approved managed-section insertion. [`promotion-outcome.json`](promotion-outcome.json)
   records the verified local result, and [`status.json`](status.json) shows no pending receipt.
8. [`governed-changeset.patch`](governed-changeset.patch) demonstrates an alternative
   review-only skill destination. It is not part of the local receipt chain above: the
   governed target would remain unchanged until its repository's normal review applies the
   patch.

## Digest relationships

- transcript SHA-256: `f336906c23e0049113dab5aaa79d041229c5d739777f241e13a7308129139dd3`
- before-target SHA-256: `ca33778bfedda98944ad7f877183af0128981181763208b19c01aff072ef314f`
- resulting-target SHA-256: `1257bbef10aeffdd0734b1504f70fc4dac86de99974a8595b058ef6ddcf170f7`
- preview digest: `d6a4d71ee14b8e6e1c3f803fc0d902c1baa11a64122549a76185570c9695d282`
- receipt digest: `0b7a0bf8541354eb18d8dbc646244dc8e41fe9244ad14581c41a760cafbd1720`

The job suffix derives from runtime, session ID, transcript digest, and schema version. The
preview and receipt digests use canonical key-sorted compact JSON over their unsigned payloads.
