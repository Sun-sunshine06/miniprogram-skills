# Releasing

English | [中文](./releasing.zh-CN.md)

Use this short checklist before publishing a tag or repository release.

## Pre-Release Checks

1. run `pwsh -File scripts/check.ps1 -IncludeAudit` or `powershell.exe -File scripts/check.ps1 -IncludeAudit`
2. confirm `tools/wechat-gui-check/node_modules` and `.tmp/` are not staged
3. confirm the release note still matches the current scope and known limitations

## Release Framing

For the `v0.3.0` release, describe the repository as:

- a reusable skill repository whose four public skills now ship with example prompts and recorded validation evidence
- a contributor-friendly repository with one shared local validation flow and matching CI coverage
- a public beta for the GUI smoke harness, now with richer bundled samples and one documented external forward-test
- a repository whose default install avoids the upstream GUI image-stack dependency chain, while live automation still depends on a user-supplied runtime install
- a repository entering the evidence-heavy part of `v0.3`, where collaborator-host validation and routing transcripts are the next confidence work rather than current release blockers

## After Publishing

1. create the GitHub release from the matching tag
2. use `docs/release-v0.3.0.md` as the release-note baseline and keep `CHANGELOG.md` aligned with the final wording
3. open one follow-up issue for collaborator-host forward-testing and routing-eval evidence
4. open one follow-up issue for deciding whether to keep or replace the current user-supplied `miniprogram-automator` runtime model after broader `v0.3` evidence arrives
