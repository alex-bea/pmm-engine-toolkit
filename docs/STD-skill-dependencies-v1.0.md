# Skill Dependency Closure Standard v1.0

A public skill package is complete when:

1. `SKILL.md` has only `name` and `description` in YAML frontmatter.
2. `agents/openai.yaml` contains display metadata and a prompt naming the skill.
3. Every path named by `SKILL.md` exists in the repository.
4. The package contains a runbook, reusable output or config asset, and synthetic example.
5. Any deterministic behavior is implemented in `scripts/` and covered by a local test.
6. Required shared standards are committed under `docs/` and linked explicitly.
7. Optional services are described as adapters; no private configuration is committed.
8. Placeholder files, private examples, local absolute paths, and secrets are absent.

Run `python3 scripts/governance/validate_skill_pack.py` before release.
