# Troubleshooting

| Category | Meaning | Safe response |
|---|---|---|
| Usage/config | Required input or mapping is invalid | Correct every reported field; do not create a run |
| Capability | A required adapter or permission is unavailable | Run doctor and fix or explicitly revise source policy |
| Collection | A required source failed | Inspect retained checkpoint and partial coverage; create a recorded retry or new run |
| Validation | Schema, hash, path, or policy failed | Restore exact artifacts or create a new revision |
| Approval | Approval is missing, stale, rejected, or unauthorized | Use the configured system of record for the exact digest |
| Conflict | Registry base or lock changed | Review the conflict artifact; create a new proposal against current state |
| Synthesis | Claims or changes violate the bounded output contract | Revise from the same approved evidence only |
| Privacy | Output would exceed sensitivity policy | Remove the unsupported output or obtain the required governed review |

Never repair a run by editing its run state, evidence manifest, recorded hash, approval, or
canonical registry directly. Do not silently select a completed or ambiguous “latest” run.
