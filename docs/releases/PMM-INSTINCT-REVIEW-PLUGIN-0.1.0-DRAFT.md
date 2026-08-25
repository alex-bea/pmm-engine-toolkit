# PMM Instinct Review plugin 0.1.0 — draft release notes

Status: release candidate pending pull-request approval.

## Added

- A marketplace-installable Codex plugin with `SessionStart` and `SessionEnd` hooks resolved
  through `${PLUGIN_ROOT}`.
- Disabled-by-default, acknowledged local capture for eligible main-thread sessions.
- Stable redacted transcript normalization, model-pinned ephemeral extraction, an atomic
  recoverable queue, and three-attempt retry handling.
- Explicit cluster review, runtime-owned instincts, confidence-gated project/global/skill
  promotion previews, normalized duplicate checks, and a second approval gate.
- Five-session calibration backfill, processed-transcript cleanup, status and queue commands,
  and compatibility import for explicit candidate JSON.
- Public product requirements, a maintainer implementation blueprint, and five positive plus
  three negative reviewer test cases that use only local, synthetic inputs.

## Changed

- The standalone `pmm-instinct-review` skill is retired from the public skill inventory. Its
  manual candidate review capability now ships inside the plugin.
- The public catalog contains 25 standalone skills plus one installable plugin.

## Privacy and compatibility

- Installation does not enable capture.
- Enabling creates local transcript-derived state and each extraction invokes Codex a second
  time. Employer policy must permit both on a work device.
- No telemetry or hosted PMM service is included; native Codex history is never modified.
- Target support is macOS, Codex, and Python 3.11 or newer. Other runtimes and Windows are not
  included in this release.
