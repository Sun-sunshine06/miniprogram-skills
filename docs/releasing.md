# Releasing

English | [中文](./releasing.zh-CN.md)

Use this short checklist before publishing a tag or first public repository release.

## Pre-Release Checks

1. run `pwsh -File scripts/check.ps1 -IncludeAudit` or `powershell.exe -File scripts/check.ps1 -IncludeAudit`
2. confirm `tools/wechat-gui-check/node_modules` and `.tmp/` are not staged
3. confirm the release note still matches the current scope and known limitations

## Release Framing

For the current `v0.1.0-public-beta` release, describe the repository as:

- a docs-first reusable skill repository
- a public beta for the GUI smoke harness
- a repository whose default install avoids the upstream GUI image-stack dependency chain, while live automation still depends on a user-supplied runtime install

## After Publishing

1. create the GitHub release from the matching tag
2. paste the `v0.1.0-public-beta` notes from `CHANGELOG.md`
3. open one follow-up issue for forward-testing the GUI harness on a non-source miniapp repo
4. open one follow-up issue for deciding whether to keep or replace the current user-supplied `miniprogram-automator` runtime model
