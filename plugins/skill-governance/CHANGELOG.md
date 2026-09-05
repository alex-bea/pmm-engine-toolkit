# Skill Governance Plugin Changelog

## 0.3.0 — Draft

- Added an agent-facing adoption guide that makes Claude Code and Codex inspect first,
  report setup readiness, obtain scoped approval, and verify activation before claiming
  governance is ready.
- Rebuilt `govern-skills` from the private golden implementation while keeping its public
  core generic and directly installable.
- Added one shared policy decision for Claude Code and Codex PreToolUse adapters.
- Added schema-version-2 run control, digest-bound artifacts, independently verified human
  approval, scheduled-run restrictions, and a credential-isolated publisher guard.
- Bound verifier selection to the source policy, constrained trusted wrappers to exact
  single-command invocations, and bound publisher receipts to the requested run and digest.
- Kept audits advisory, initialization dry-run first, blocking CI and runtime controls
  opt-in, and conflicting managed files non-overwritable.
- Added complete generic templates, schemas, a fictional adoption example, negative tests,
  privacy disclosure, and explicit enforcement-class reporting.

This release does not provide a hosted approval service, credential store, or publisher.
Runtime hooks alone are not a complete security boundary; strong enforcement requires
administrator-protected configuration and capability restrictions.
