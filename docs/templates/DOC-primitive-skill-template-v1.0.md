# Primitive Skill Template

Use this small shape when a skill performs one bounded, deterministic action.

```markdown
---
name: <slug>
version: 1.0.0
description: <one bounded outcome>
references: []
---

# <Name>

## Input
## Procedure
## Output
## Safety constraints
```

Do not add external data collection, publication, or hidden dependencies without declaring
them and adding an explicit approval gate.
