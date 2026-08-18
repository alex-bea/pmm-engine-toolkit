# Skill Primitives Standard

Skills are composed from four primitives. Keep each primitive in one place so the workflow
does not duplicate or contradict itself.

| Primitive | Purpose | Typical location |
| --- | --- | --- |
| Workflow | Ordered execution and approval steps | `references/RUN-*.md` |
| Knowledge | Stable facts, rules, or source precedence | `references/REF-*.md` |
| Template | Required output shape and placeholders | `references/BP-*.md` or `templates/` |
| Example | Illustrative, non-sensitive input/output | `examples/EX-*.md` |

Workflows may reference the other primitives, but templates must not become hidden policy
documents and examples must not be treated as facts.
