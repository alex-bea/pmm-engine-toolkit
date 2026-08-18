# Security Policy

## Supported versions

The latest commit on the default branch and the latest tagged release receive security
fixes. Older releases are supported only when a maintainer explicitly says otherwise.

## Reporting a vulnerability

Do not disclose a suspected vulnerability in a public issue, discussion, or pull request.
Use the repository's private security-advisory reporting channel.

Private vulnerability reporting is a required launch control and is verified alongside
secret scanning, push protection, dependency alerts, and CodeQL. See
[`docs/security/GITHUB-SECURITY-CONTROLS.md`](docs/security/GITHUB-SECURITY-CONTROLS.md).

Include:

- the affected version or commit;
- a minimal reproduction or proof of concept;
- expected and observed behavior;
- impact and realistic attack conditions; and
- any known mitigation or evidence of active exploitation.

Maintainers will acknowledge and triage reports on a best-effort basis, coordinate a fix
and disclosure plan when appropriate, and credit reporters who request attribution.

## Security scope

Treat exposed credentials, unsafe generated automation, dependency compromise, arbitrary
code execution, private-data leakage, internal URLs, and bypasses of review or approval
gates as security issues. General support requests belong in the channel described by
[SUPPORT.md](SUPPORT.md).

This toolkit should not require credentials or private-service access. Optional connectors
must be configured locally and should use least-privilege access.
