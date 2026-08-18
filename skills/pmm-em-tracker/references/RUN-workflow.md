# Tracker workflow

1. Read the tracker and validate its schema before reasoning about status.
2. Resolve the exact roadmap, epic, or task requested; never guess an ambiguous ID.
3. Draft the smallest state transition and explain any dependency or WIP effect.
4. Obtain approval when the request did not already authorize the local write.
5. Apply the change, validate again, and render a concise summary.

Allowed task transitions are `icebox -> todo -> active -> done`; `blocked` may interrupt
`todo` or `active` and must include a reason. Reopening a task requires a stated reason.
