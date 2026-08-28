# Codex instinct-review workflow

Read `DOC-product-requirements.md` for product scope and approval gates and
`DOC-implementation-blueprint.md` before changing behavior. This runbook owns the exact
operator procedure.

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

Run `list-priority`. Present one positive candidate at a time with what happened, the user's
feedback, proposed future behavior, why it matters, and concise support/source details. Do not
show a destination or routing metadata at this candidate-to-instinct gate. Accept only an
explicit `accept`, `reject`, `edit`, or `match` decision; an edit can include an amended
rationale. Mutating review commands require `--confirm`. Use `resolve-zero --confirm` only
after explicitly confirming the zero-candidate bucket. When one audit contains multiple
candidates, keep its normalized transcript until every candidate cluster from that audit has a
recorded decision.

Accepting creates one runtime-owned instinct. Rejecting creates none. Matching increments the
exact active instinct. Any resolved review marks its audits processed and deletes only their
normalized transcript copies.

## 4. Promotion

Only active instincts with confidence at least 0.5 are eligible. First choose a destination
class, then preview that exact target. Project guidance targets the nearest repository
`AGENTS.md`; general guidance targets `~/.codex/AGENTS.md`; `both` targets both. A single
named skill can target its exact writable registered RUN document. A voice rule can target an
explicitly configured writable REF mapping; an unmapped route remains unresolved. A pattern
with at least three source skills can target an owner-selected writable `STD-*.md` inside a
supporting repository. Never write a plugin-cache skill.

Configure a voice mapping only in the user-owned `voice_ref_routes` object in
`~/.codex/instinct-review/config.json`. Each value is a relative path within the named skill,
such as `"references/REF-voice.md"`; absolute paths and parent-directory traversal are refused.

The destination preview is recorded locally. Show exact paths, insertion text, and duplicate
state, then apply only with a matching second explicit confirmation. Append new rules under
`## PMM Instinct Review — Promoted Guidance`; stage all selected writes before replacing any
target. If a target already covers the rule, record it as covered without a duplicate write.
Record the final file and managed section in the instinct file. Never write Claude state.

## 5. Retention and rollback

Use `cleanup` to retry deletion of normalized transcripts for already processed audits. `off`
stops new capture but preserves all state. Removing the plugin also preserves
`~/.codex/instinct-review/` and native Codex history.
