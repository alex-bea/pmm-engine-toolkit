# Support

## Where to ask

- Use a GitHub issue for reproducible bugs and concrete documentation defects.
- Use a GitHub discussion, when enabled, for usage questions and design proposals.
- Use a pull request for a tested, scoped improvement.
- Follow [SECURITY.md](SECURITY.md) for vulnerabilities and
  [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for conduct concerns.

Before filing a request, search existing issues and reproduce the problem from the latest
default branch or release. Include your operating system, Python version, exact command,
minimal input, expected behavior, observed behavior, and relevant output with secrets and
personal information removed.

For `pmm-instinct-review`, include the output of `continuous learning status`, the queue state,
the operating-system and Python versions, and whether Codex was resolved from `PATH`, ChatGPT,
or the Codex app. Never attach native or normalized transcripts, audit evidence, tokens, or
employer-confidential content. A failed model job is intentionally retryable; use
`retry failed extraction` after correcting the reported model or executable issue.

Hook trust is controlled by Codex. Open `/hooks` after installation and review the distinct
`SessionStart` and `SessionEnd` entries. Installation, hook trust, and learning enablement are
three separate steps.

## Support boundary

This is a community-maintained open-source project with no guaranteed response or service
level. Maintainers may close requests that are unreproducible, unsafe, out of scope,
duplicative, or dependent on private integrations. Commercial implementation, legal
review, and organization-specific configuration are not included.
