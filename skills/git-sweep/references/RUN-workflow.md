# Git sweep workflow

1. Resolve the repository and inspect `git status`, branches, and worktrees read-only.
2. Classify each non-current worktree as protected, dirty, unmerged, merged-and-clean,
   detached-and-clean, or unknown.
3. Show exact paths and reasons for cleanup candidates.
4. Require explicit approval for each removal set.
5. Recheck status immediately before removal; abort if classification changed.
6. Remove only approved clean candidates, prune metadata separately, and report results.

Never delete a current, main, locked, dirty, or unmerged worktree.
