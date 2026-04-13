# Releasing

English | [中文](./releasing.zh-CN.md)

Use this short checklist before publishing a tag or repository release.

## Pre-Release Checks

1. run `pwsh -File scripts/check.ps1 -IncludeAudit` or `powershell.exe -File scripts/check.ps1 -IncludeAudit`
2. confirm `tools/wechat-gui-check/node_modules` and `.tmp/` are not staged
3. confirm the release note still matches the current scope and known limitations

## Release Framing

For the `v0.4.0` release, describe the repository as:

- a reusable skill repository whose four public skills now have a machine-readable catalog entry, replayable routing fixtures, example prompts, and recorded validation evidence
- a contributor-friendly repository with one shared local validation flow covering skills, docs, JSON, the skill catalog, routing fixtures, and tool preflight behavior
- a public beta for the GUI smoke harness that still keeps scope honest while carrying one documented external forward-test
- a repository whose default install avoids the upstream GUI image-stack dependency chain, while live automation still depends on a user-supplied runtime install
- a repository that has established the catalog-and-routing baseline in `v0.4.0`, where collaborator-host validation and transcript-backed routing evidence are the next confidence work rather than current release blockers

## After Publishing

1. create the GitHub release from the matching tag
2. use `docs/release-v0.4.0-draft.md` as the release-note baseline and keep `CHANGELOG.md` aligned with the final wording
3. open one follow-up issue for collaborator-host forward-testing and routing-eval evidence
4. open one follow-up issue for deciding whether to keep or replace the current user-supplied `miniprogram-automator` runtime model after broader post-`v0.4.0` evidence arrives
