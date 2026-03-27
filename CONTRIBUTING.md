# Contributing

English | [中文](./CONTRIBUTING.zh-CN.md)

## Goal

Keep this repository focused on reusable WeChat Mini Program skills and supporting tooling, not on one product repo's private implementation details.

## Before Opening A Change

- confirm that the workflow is reusable across more than one miniapp repo
- remove absolute local paths unless they are examples with placeholders
- remove product-specific storage keys from core instructions
- keep source-repo baselines out of `SKILL.md`

## Collaboration Workflow

- keep `validate` green before merging into `main`
- use a pull request when the change would benefit from review history or discussion
- small maintainer-only updates may be pushed directly when they stay within the current branch protection rules
- keep pull-request branches up to date with `main` when GitHub reports them as behind

## Local Validation

Run the shared validation command before opening a PR:

```powershell
pwsh -File scripts/check.ps1
powershell.exe -File scripts/check.ps1
```

This command expects `python`, `node`, and `npm` on `PATH`. It installs `tools/wechat-gui-check` dependencies with `npm ci --ignore-scripts`, validates public skills, checks markdown links plus bilingual doc cross-links, validates repository JSON plus tool syntax, and runs the external-project dry-run smoke check against a copied fixture.

## Skill Changes

For changes under `skills/`:

1. update `SKILL.md`
2. update `references/` if the workflow details changed
3. verify `agents/openai.yaml` still matches the skill
4. run `pwsh -File scripts/check.ps1` or `powershell.exe -File scripts/check.ps1`, or at minimum rerun the skill validator while iterating on skill-only changes

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
- the documented collaboration flow still matches the current repository rules
- skill-review feedback can be grounded in `docs/skill-review-checklist.md` when the PR touches `skills/`
