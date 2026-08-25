# Codex instinct-review workflow

## 1. Status and enablement

Run `python3 <skill-dir>/scripts/instinct_review.py status`. Installation is not consent to
capture. Before enabling, disclose that eligible chats will be normalized into local transient
files and analyzed by a second ephemeral Codex invocation. Confirm that the user's organization
permits this on the device, then run `on --acknowledge-local-chat-storage`.

## 2. Capture and extraction

`SessionEnd` captures only enabled main-thread sessions with at least five user messages. The
hook writes an audit, redacted normalized JSONL, and queue record atomically, starts a detached
worker, and returns. It excludes developer/system messages, reasoning, tools, results, patches,
world state, compaction payloads, and context-only wrappers.

The worker uses the configured model or the exact model recorded by the hook. It never falls
back. Extraction is ephemeral, ignores user configuration and rules, uses a read-only sandbox,
and validates a strict schema. Zero candidates is success.

## 3. Backlog review

Run `list-priority`. Review zero-candidate audits separately and present each positive cluster's
type, rule, evidence, context, support, repositories, and default destination. Accept only an
explicit `accept`, `reject`, `edit`, or `match` decision. Mutating review commands require
`--confirm`. Use `resolve-zero --confirm` only after explicitly confirming the zero-candidate
bucket. When one audit contains multiple candidates, keep its normalized transcript until every
candidate cluster from that audit has a recorded decision.

Accepting creates one runtime-owned instinct. Rejecting creates none. Matching increments the
exact active instinct. Any resolved review marks its audits processed and deletes only their
normalized transcript copies.

## 4. Promotion

Only active instincts with confidence at least 0.5 are eligible. Preview first. Project guidance
targets the nearest repository `AGENTS.md`; general guidance targets `~/.codex/AGENTS.md`;
`both` targets both. A skill destination is allowed only for one exact writable user/project
skill outside plugin cache.

Show exact paths, insertion text, and duplicate state. Apply only after a second explicit
confirmation. Record destinations in the instinct file. Never write Claude state.

## 5. Retention and rollback

Use `cleanup` to retry deletion of normalized transcripts for already processed audits. `off`
stops new capture but preserves all state. Removing the plugin also preserves
`~/.codex/instinct-review/` and native Codex history.
