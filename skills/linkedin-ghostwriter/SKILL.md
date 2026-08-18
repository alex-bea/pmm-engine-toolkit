---
name: linkedin-ghostwriter
version: 1.0.0
description: Draft a LinkedIn post from approved source material and a consented voice profile; never publish or invent claims.
references:
  - path: references/RUN-linkedin-ghostwriter-workflow.md
    role: runbook
  - path: references/REF-voice-profile-template.md
    role: template
---

# LinkedIn Ghostwriter

## Role

Draft posts in a named person's voice only when the user supplies a consented voice profile
and source material. This skill drafts; it does not search for a person, collect examples,
or post to LinkedIn.

## Triggers

- "draft a LinkedIn post"
- "ghostwrite a LinkedIn post"
- "write a post in this voice"

## Output

Provide one draft, a source-evidence note for material claims, and any `[Missing]` facts.
Do not invent quotes, metrics, customer names, endorsements, or positions.

Follow `references/RUN-linkedin-ghostwriter-workflow.md`.
