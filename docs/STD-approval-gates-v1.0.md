# Approval Gates Standard v1.0

## Gate levels

| Level | Action | Default |
|---|---|---|
| Read | Inspect local or user-approved sources | Proceed |
| Draft | Create a local proposal or artifact | Proceed |
| Local write | Update files in the repository | Show intended paths first when destructive |
| External write | Post, message, schedule, publish, or mutate a service | Require explicit approval |
| Destructive | Delete, overwrite, force-push, or remove worktrees | Require target-specific approval and a clean-state check |

Approval for one gate does not imply approval for a higher gate. Generated monitors and
automations must default to dry-run or review-first operation.
