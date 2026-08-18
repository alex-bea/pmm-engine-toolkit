# Project Governance

## Roles

- **Project owner:** `alex-bea`, responsible for repository administration, releases,
  security decisions, and appointing maintainers.
- **Maintainers:** contributors granted review or merge authority for defined areas.
- **Contributors:** anyone proposing issues, documentation, code, skills, or reviews.

Repository permissions, not contribution volume, determine maintainer authority.

## Decision-making

Routine changes are decided through pull-request review. Maintainers prefer evidence,
backward compatibility, safety, and a small maintainable surface. Material changes to the
public skill inventory, license, governance, security model, or compatibility policy require
project-owner approval and should remain open long enough for meaningful review.

The project owner is the final decision-maker when consensus is not reached. Decisions may
be revisited when new evidence appears.

## Releases

Only the project owner or an authorized maintainer may create releases. A release must pass
the repository test suite, skill-pack validation, security checks, documentation review,
and the applicable release checklist. Security fixes may use an abbreviated private review
before coordinated disclosure.

## Maintainer changes

The project owner may appoint or remove maintainers based on sustained, trustworthy
contributions and the project's needs. Maintainers must follow the Code of Conduct, protect
confidential reports, disclose relevant conflicts of interest, and use least privilege.

Changes to this governance document use the same material-change review process described
above.
