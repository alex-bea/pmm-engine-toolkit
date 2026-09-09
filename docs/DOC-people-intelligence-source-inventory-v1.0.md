---
doc_type: DOC
normative: false
requires: []
status: Draft
version: "1.0"
owner: toolkit-maintainers
consumers:
  - people-intelligence maintainers
  - privacy reviewers
change_control: Pull request review
---

# People Intelligence Public Source Inventory

This public inventory records the safe implementation boundary for the `people-intelligence` package. It describes the public candidate, not private source content or a path to private systems.

| Public artifact or interface | Public role | Disposition | Requirement IDs | Verification |
|---|---|---|---|---|
| `skills/people-intelligence/SKILL.md` | Concise public entrypoint and mode boundary | rewrite-generic | PI-REQ-001, PI-REQ-002, PI-REQ-009 | Focused package test |
| `references/RUN-workflow.md` | Bounded, adapter-neutral workflow | rewrite-generic | PI-REQ-002, PI-REQ-003, PI-REQ-005 through PI-REQ-008 | Focused workflow test |
| `references/REF-evidence-privacy.md` | Package-local consent, evidence, retention, and correction guidance | add | PI-REQ-002, PI-REQ-005, PI-REQ-010 | Focused privacy test |
| `assets/` templates | Blank reusable input, output, source-map, and writing-prompt structures | replace-with-template-or-schema | PI-REQ-004, PI-REQ-007, PI-REQ-010 | Template test |
| `examples/fictional-team-coordination/` | Complete independently invented source-to-output scenario | rewrite-generic | PI-REQ-006, PI-REQ-011 | Source-support and reserved-URL test |
| Authorized adopter evidence | Optional input interface | interface-only | PI-REQ-002, PI-REQ-004, PI-REQ-010 | Safe-degradation test |
| Adopter state and output destinations | Optional baseline and local destination interface | interface-only | PI-REQ-004, PI-REQ-006, PI-REQ-010 | No-automatic-write test |
| Public catalog, test, privacy review, and IP inventory | Public governance and release records | interface-only | PI-REQ-009, PI-REQ-012 | Repository validation |

The golden implementation informed workflow structure, templates, constraints, and depth only. No private output, populated source configuration, organization-specific system, personal profile, identifier, message, or mapping is included in this public candidate.
