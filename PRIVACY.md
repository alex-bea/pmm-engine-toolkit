# Privacy

## Repository behavior

The repository does not include analytics, telemetry, hosted services, remote collection, or
default-on data collection. Its scripts otherwise read only explicit inputs and write only to
requested local destinations. The opt-in PMM Instinct Review exception below uses local native
lifecycle hooks after separate consent; it is disabled at installation.

## PMM Instinct Review plugin

Installing the plugin does not enable capture. First enablement requires explicit
acknowledgment of local chat-derived storage. The Codex and Claude runtimes use separate,
user-owned roots: `~/.codex/instinct-review/` and
`~/.claude/pmm-instinct-review-data/`, respectively. When enabled, each native runtime
captures eligible main-thread sessions with at least five user messages. It keeps only
bounded, redacted user and assistant conversation text in a normalized transient copy; it
also records local session/job identifiers, timestamps, content digests, state paths, and
project-directory metadata needed for routing and review. Claude briefly spools a local
metadata-only capture request containing its native transcript path before a detached worker
normalizes the read-only transcript; the request contains no conversation text and is removed
after success, ineligibility, its retry ceiling, or contract-invalid input has been recorded in
a sanitized log. It excludes system and developer instructions, reasoning, tool calls and
results, patches, world state, and compaction payloads.

Codex additionally stores the adopter-selected exact extractor-model identifier and optional
relative `run_routes` / `voice_ref_routes` values in its local config. These values are used as
configuration, not transmitted as telemetry. New Codex capture and backfill jobs obtain model
authority only from the persisted config; a model name present in session metadata cannot
supply or override it. A legacy enabled store with no configured model skips capture before
creating normalized evidence, an audit, or a queue record.

Route values may reveal adopter-owned skill and document names to local users or processes that
can read the state root. Resolution exposes only validated eligible absolute paths needed for
an explicit human choice. Configuration cannot authorize absolute paths, parent traversal,
cross-skill destinations, plugin/cache files, or symlink escapes. The runtime does not read or
send target document contents merely to enumerate an ambiguous RUN/REF choice.

Extraction performs a second, ephemeral invocation of the configured native model with no
session persistence requested. Native Claude extraction disables built-in and MCP tools.
Codex extraction runs in a read-only sandbox and its prompt prohibits tool use, but the Codex
runtime does not claim that tools are technically unavailable. Codex extraction is processed
by the applicable OpenAI service. Claude extraction uses the configured Anthropic model
through the Anthropic API or a supported cloud provider such as Amazon Bedrock, Google Vertex
AI, or Microsoft Foundry. Those providers may process the normalized input under the user's
account agreement and settings. The Claude worker's isolated `--bare` invocation does not
reuse an ordinary subscription login or keychain. The plugin has no telemetry and sends
nothing to a hosted PMM service. Users must confirm employer policy and provider configuration
before enabling this workflow on a work device.

After every candidate cluster in an audit has a recorded human decision, or after separate
confirmation resolves a zero-candidate audit, the runtime deletes only the normalized copy.
Audits, suggestions, approved instincts, sanitized operational logs, and queue metadata remain
local until the user removes them. Native Codex and Claude session histories are never
modified. Disabling or uninstalling the package preserves the applicable state root so queued
work can recover after reinstallation.

Claude promotion is a separate data flow. A human must approve the exact target, existing
content digest, proposed result, and preview digest before a background worker may execute a
local update. If a destination is classified for governed review, the worker writes a local
patch for review and does not mutate the governed target. The runtime does not approve,
merge, publish, or send that patch automatically.

## User responsibility

Do not place credentials, personal data, customer information, private communications,
internal URLs, or confidential business material in committed configuration, examples,
issues, pull requests, or test fixtures. Store connector credentials outside the repository
and grant the minimum access required.

Generated artifacts may reproduce information from their inputs. Review and redact outputs
before committing, sharing, or publishing them. Synthetic examples in this repository are
formatting references, not real people, customers, or claims.

## Skill governance runtime controls

The optional governance hooks inspect the current tool name and only the arguments needed to
classify a path, command, transition, or publication attempt. Structured decisions contain
the result, reason code, harness, action class, enforcement class, and explanation. They do
not retain prompts, content bodies, full tool arguments, cookies, authorization headers,
credentials, or private artifact content.

Runtime enforcement is disabled by default. Adopters own enabled policy, workflow run state,
external verifier configuration, publisher configuration, service-side approval evidence,
and publisher receipts. Store those outside agent-writable and publicly committed paths.
The toolkit does not operate a hosted verifier or publisher and receives no data from those
adopter-configured services.

## External services

Optional connectors, Git hosting, package registries, and other external services operate
under their own privacy terms. This project does not control their collection or retention.

Report accidental exposure through [SECURITY.md](SECURITY.md). Do not repeat exposed data
in a public issue.
