---
name: git-sweep
description: Inspect Git branches and worktrees, classify safe cleanup candidates, and optionally remove only merged clean worktrees after explicit approval. Use for repository cleanup or worktree hygiene; never delete dirty or unmerged work.
---

# Git Sweep

1. Read `docs/STD-approval-gates-v1.0.md` and `references/RUN-workflow.md`.
2. Run `scripts/worktree_hygiene.py --repo <path>` without `--apply` to inspect.
3. Render the proposal with `assets/output-template.md`.
4. Use `examples/EX-synthetic.md` only as synthetic output.
5. Run with `--apply` only after target-specific approval.

Skip dirty, locked, main, current, and unmerged worktrees. Pruning is separate from deleting worktrees.
