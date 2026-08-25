---
doc_type: STD
normative: true
requires:
  - STD-skill-structure-v1.0.md
status: Active
version: "1.0"
owner: alex-bea
consumers:
  - Codex users
  - skill authors
change_control: Pull request review
---

# Skill Primitives and Authoring Quality Standard

Keep each reusable concern in one place so a workflow does not duplicate or contradict
itself.

| Primitive | Purpose | Typical location |
|---|---|---|
| Workflow | Ordered execution, stop conditions, and approvals | `references/RUN-*.md` |
| Knowledge | Stable rules, schemas, and source precedence | `references/REF-*.md` |
| Template | Required output shape and placeholders | `assets/` or `references/BP-*.md` |
| Example | Illustrative, non-sensitive input and output | `examples/EX-*.md` |
| Script | Deterministic validation or transformation | `scripts/` |

## Quality contract

Every workflow must name its inputs, outputs, evidence requirements, approval gates,
failure modes, and stop conditions. Side-effectful steps must say whether they are
idempotent, conditionally idempotent, or non-idempotent and must verify the resulting
state after a write.

Templates define shape, not hidden policy. Examples illustrate behavior but are never
evidence. Knowledge references own stable rules. Scripts must not silently invent semantic
content, weaken checks, or broaden the authorized write scope.

## Testing

Test deterministic scripts in isolation and exercise at least one representative end-to-end
workflow with synthetic inputs. Include negative cases for malformed metadata, missing
dependencies, unauthorized writes, ambiguous inputs, and repeated execution. Prefer
property or matrix tests when a primitive is reused across multiple skills.
