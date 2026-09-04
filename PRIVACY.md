# Privacy

## Repository behavior

The repository does not include analytics, telemetry, hosted services, or automatic data
collection. Its local scripts read only the files and Git repository state explicitly
provided to them and write only to requested local destinations.

## PMM Instinct Review plugin

Installing the plugin does not enable capture. First enablement requires explicit
acknowledgment of local chat-derived storage. When enabled, the plugin creates user-owned
state under `~/.codex/instinct-review/` from eligible main-thread sessions with at least five
user messages. It keeps only redacted user and assistant text in a normalized transient copy;
it excludes system and developer instructions, reasoning, tool calls and results, patches,
world state, and compaction payloads.

Extraction performs a second, ephemeral Codex model invocation in a read-only sandbox. The
plugin has no telemetry and sends nothing to a hosted PMM service. The applicable Codex model
service may still process the normalized input under the user's OpenAI agreement and settings.
Users must confirm employer policy before enabling this workflow on a work device.

Approval or rejection deletes only the normalized copy. Audits, suggestions, approved
instincts, sanitized operational logs, and queue metadata remain local until the user removes
them. Native Codex session history is never modified. Disabling or uninstalling the plugin
preserves `~/.codex/instinct-review/` so queued work can recover after reinstallation.

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
