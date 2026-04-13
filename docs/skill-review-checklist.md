# Skill Review Checklist

Use this short checklist during PR review for changes under `skills/`.

## Review Questions

- Is the trigger clear from the skill description, including when the skill should not be used?
- Can a new reader execute the workflow from `## Quick Start` without hidden repo knowledge?
- Is the expected output format concrete enough that reviewers can tell what a good answer should look like?
- Does the change avoid repo-specific leakage such as private product names, absolute local paths, storage keys, or one-off route names?
- Do the `references/` files add real operational value instead of repeating the `SKILL.md` body?
- Do the example prompts cover both a realistic use case and at least one clear non-use case?
- If the skill is public-facing, does `manifests/skill-catalog.json` still reflect the current boundary and evidence state?
- If the routing boundary changed, is the matching `evals/routing/` fixture coverage updated too?
- If the routing prompt or output contract changed, do the matching `evals/routing-replays/` transcript records still validate?

## Accept If

- most review answers are "yes" without needing maintainer-only context
- any remaining draft-only limits are stated explicitly
- catalog and routing fixture updates land with the skill change when the public boundary moved
- routing replay transcript updates land with the change when prompt wording or output structure moved
- review comments can point to one checklist item instead of vague "make it more reusable" feedback
