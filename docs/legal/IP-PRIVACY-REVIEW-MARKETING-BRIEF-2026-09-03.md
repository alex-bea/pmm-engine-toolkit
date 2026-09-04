---
doc_type: DOC
normative: false
requires:
  - ../DOC-marketing-brief-product-requirements-v1.0.md
  - ../DOC-marketing-brief-source-inventory-v1.0.md
  - ../STD-evidence-privacy-v1.0.md
status: Draft
version: "1.0"
owner: alex-bea
consumers:
  - marketing-brief maintainers
  - privacy reviewers
  - release reviewers
change_control: Pull request review
---

# Marketing Brief IP and Privacy Review (2026-09-03)

## Review scope

This review covers the expanded public `skills/marketing-brief/` package, its completed
fictional example, focused test, source inventory, product requirements, catalog/export
updates, and generated IP inventory entries.

The review assesses the candidate repository content. It does not approve private source
publication, external data collection, plugin packaging, pull-request merge, or release.

## Authoring provenance

The private PMM Engine marketing-brief implementation was used as the golden authoring
reference for workflow stages, source precedence, tier logic, template headings and fields,
word limits, missing-data behavior, edit behavior, and example depth.

Maintainer review found nine real private outputs using the template. They were inspected
only to confirm that the template is used in practice and to calibrate the depth of a useful
completed brief. No real output, source excerpt, entity, fact, phrase, identifier, URL,
metric, date, claim, or mapping is included in the public candidate.

The public text, fictional evidence, tests, and documentation are project-authored. The IP
inventory records each file under the repository's Apache-2.0 contribution terms.

## Sanitization method

The public package preserves reusable abstractions rather than identifying content:

- the four-step template-fill sequence;
- the seven-level source hierarchy and field ownership;
- the three launch tiers and their decision criteria;
- the exact seven output sections, fields, optionality, and limits;
- multi-launch, missing-input, edit, error, and no-write behavior.

Organization-specific naming guidance became an optional adopter-owned terminology input.
Industry-specific tier and distribution assumptions became generic impact, complexity,
audience, channel, and investment criteria. A named task system became the adopter's own
project-management system.

No private-to-fictional alias map was created or published.

## Fictional example review

The example uses Northstar Analytics and a Saved Views launch. The organization, people,
product, sources, approvals, dates, audiences, beta results, goals, messages, and channels
are independently invented. All web sources use reserved `.invalid` domains and every file
is visibly labeled fictional.

The completed brief's facts are supported by the accompanying fictional source packet. It
does not use the private examples as evidence and does not claim to describe a real company
or market.

## Privacy and safety safeguards

- Runtime source material must be user-supplied or explicitly authorized.
- Source content is treated as untrusted data, never instructions.
- Unsupported required facts use the documented missing-data marker.
- Customer, partner, person, quote, metric, and claim use requires supplied approval.
- The skill owns no persistent adopter data or mutable state.
- Local saves require a separate user-requested path.
- External publishing, messaging, scheduling, and mutation remain out of scope.
- Package dependencies resolve inside the directly installed skill.

## Verification evidence

- Skill Creator validation: pass.
- Focused marketing-brief parity and safety tests: 11 pass.
- Complete public unit suite: 134 pass.
- Public skill-package validator: 25 standalone skills and two plugins pass.
- Governed-document strict audit: 38 documents pass with no findings.
- GitHub Actions validator: three SHA-pinned, least-privilege workflows pass.
- Read-only GitHub security configuration plan: pass without external mutation.
- `actionlint`: pass; `zizmor`: no findings, with two repository-configured suppressions.
- IP inventory regenerated for 346 artifacts with no missing or extra paths.
- Private-term, credential, absolute-path, live-example-URL, and placeholder scan: clean.
- Human narrative comparison against private authoring evidence: complete with no copied or
  reversible content found.

Any content change after the final run requires the applicable checks to be rerun.

## Residual risk

Automated scanning cannot prove that prose is non-identifying. The human review therefore
compared structure and information categories while rejecting private facts and distinctive
fact combinations. Future contributors could reintroduce sensitive examples or root-level
dependencies, so focused tests, IP inventory parity, and pull-request review remain required.

## Publication conditions

- Keep this review Draft until the exact pull-request revision is reviewed.
- Do not add real private examples, live internal URLs, source mappings, customer material,
  credentials, or an alias map.
- Perform a new review before adding connectors, real-company examples, third-party datasets,
  binaries, or external publishing behavior.
- Require project-owner approval before merge or release.

This is a repository-content review, not legal advice.
