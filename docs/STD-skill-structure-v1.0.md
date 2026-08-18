# Skill Structure Standard

## Required package shape

Every skill lives in `skills/<slug>/` and contains a `SKILL.md` file. A skill may also
contain `references/`, `templates/`, `examples/`, and executable helpers when those files
are necessary to perform the workflow.

## `SKILL.md` contract

The file must contain:

1. YAML frontmatter with `name`, `version`, `description`, and every referenced local file.
2. A role statement that says what the skill does and does not do.
3. Trigger phrases or clear invocation conditions.
4. Required inputs and the behavior for missing inputs.
5. Output format, evidence rules, and approval gates.

## Reference rules

- Keep reusable knowledge, templates, and workflows in local reference files.
- Every path declared in frontmatter must exist within the package.
- Do not embed credentials, personal data, customer data, unpublished plans, or private
  service identifiers in a skill or reference file.
- A template must use placeholders for organization, product, people, and customer details.

## Quality bar

A skill is complete when a new contributor can run it using only its declared references
and user-supplied approved inputs.
