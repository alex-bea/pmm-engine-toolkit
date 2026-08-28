# PMM skill governance example

This fictional PMM repository keeps reusable skills under `.agents/skills/` and registers
them in `.agents/governance/skill-registry.yaml`.

```json
{
  "version": "1.0",
  "skills": [
    {
      "name": "launch-brief",
      "folder": ".agents/skills/launch-brief",
      "version": "1.0.0",
      "owner": "product-marketing",
      "status": "active",
      "replacement": null
    }
  ]
}
```

The `launch-brief` skill requires approved inputs, labels unsupported facts `[Missing]`,
produces a draft before publication, and keeps external publishing behind an explicit
approval gate.
