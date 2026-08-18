---
name: slack-monitor-scaffolder
description: Generate a review-first Slack channel monitoring configuration and prompt. Use when the user asks to scaffold a channel monitor or signal digest; require an approved connector and never post, react, or message automatically.
---

# Slack Monitor Scaffolder

1. Read `docs/STD-approval-gates-v1.0.md` and `docs/STD-evidence-privacy-v1.0.md`.
2. Follow `references/RUN-workflow.md`.
3. Fill `assets/config-template.yaml` and use `assets/output-template.md` for the digest.
4. Use `examples/EX-synthetic.md` only as a fictional configuration.

Store no channel IDs in the package. Default generated monitors to dry-run and local output.
