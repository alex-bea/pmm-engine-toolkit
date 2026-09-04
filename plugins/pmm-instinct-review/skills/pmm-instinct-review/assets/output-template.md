# PMM Instinct Review output templates

## Read-only status receipt

- **Adapter:** `codex|portable`
- **Capture supported:** `true|false`
- **Enabled:** `true|false`
- **Store:** [adopter-owned path]
- **Queue:** queued/running/succeeded/failed counts
- **Backlog:** pending, zero-candidate, positive-cluster, missing-suggestion, unresolved counts
- **Instincts:** active, promotion candidates, stale
- **Priority snapshot:** [path; existence is not implied]
- **Capture preflight:** checks or explicit non-applicability

## Backlog bucket summary

- **Zero-candidate audits:** [count and audit IDs]
- **Positive clusters:** [count, impact tiers, areas, match states]
- **Missing suggestions:** [count and audit IDs]
- **Unresolved normalized evidence:** [count]

## Instinct review candidate

- **What happened:**
- **Your feedback:**
- **Proposed future behavior:**
- **Why it matters:**
- **Support/source:** support count, source skills, source repositories/cwds
- **First/last seen:**
- **Exact match state:** `new|exact`
- **Decision:** `accept|reject|edit|match`

Destination routing is intentionally excluded from this candidate-to-instinct decision.

## Installation or enablement receipt

- **Adapter:**
- **Capture supported:**
- **State root:**
- **Enabled:**
- **Privacy acknowledgment:**
- **Preflight:**
- **State preserved on disable/removal:**

## Promotion preview (separate gate)

- **Instinct ID:**
- **Destination class selected by the owner:**
- **Exact target paths:**
- **Managed section:** `## PMM Instinct Review — Promoted Guidance`
- **Insertion:**
- **Duplicate state per target:**
- **Preview signature persisted:**
- **Second confirmation:**
- **Terminal outcome:** `promoted|covered`
