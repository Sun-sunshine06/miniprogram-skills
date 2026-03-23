# Contributing

## Goal

Keep this repository focused on reusable WeChat Mini Program skills and supporting tooling, not on one product repo's private implementation details.

## Before Opening A Change

- confirm that the workflow is reusable across more than one miniapp repo
- remove absolute local paths unless they are examples with placeholders
- remove product-specific storage keys from core instructions
- keep source-repo baselines out of `SKILL.md`

## Skill Changes

For changes under `skills/`:

1. update `SKILL.md`
2. update `references/` if the workflow details changed
3. verify `agents/openai.yaml` still matches the skill
4. run the skill validator

## Tool Changes

For changes under `tools/`:

- prefer config-driven behavior over hardcoded app routes
- document new flags or output fields
- keep sample configs and sample reports current
- note repo-specific prerequisites explicitly instead of hiding them in code

## Review Standard

Accept changes only when:

- the public boundary is cleaner, not dirtier
- the repo becomes easier to reuse
- the docs and tool behavior still match
