# Skill Review Checklist

Use this short checklist during PR review for changes under `skills/`.

## Review Questions

- Is the trigger clear from the skill description, including when the skill should not be used?
- Can a new reader execute the workflow from `## Quick Start` without hidden repo knowledge?
- Is the expected output format concrete enough that reviewers can tell what a good answer should look like?
- Does the change avoid repo-specific leakage such as private product names, absolute local paths, storage keys, or one-off route names?
- Do the `references/` files add real operational value instead of repeating the `SKILL.md` body?
- Do the example prompts cover both a realistic use case and at least one clear non-use case?

## Accept If

- most review answers are "yes" without needing maintainer-only context
- any remaining draft-only limits are stated explicitly
- review comments can point to one checklist item instead of vague "make it more reusable" feedback
