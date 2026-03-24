# Releasing

English | [中文](./releasing.zh-CN.md)

Use this short checklist before publishing a tag or first public repository release.

## Pre-Release Checks

1. run `python scripts/validate_skills.py skills --require-example-prompts`
2. run `node --check tools/wechat-gui-check/check.js`
3. run `node --check tools/wechat-gui-check/lib/check-helpers.js`
4. run `node --check tools/wechat-gui-check/lib/load-automator.js`
5. run `npm ci --ignore-scripts` inside `tools/wechat-gui-check`
6. run one external-project dry run by copying `tools/wechat-gui-check/examples/fixture-miniapp` outside the repo and calling `node tools/wechat-gui-check/check.js --config tools/wechat-gui-check/examples/sample.route-config.json --project-path <copied-fixture-path> --route home --dry-run`
7. run `npm audit --omit=dev --package-lock-only` inside `tools/wechat-gui-check`
8. confirm `tools/wechat-gui-check/node_modules` and `.tmp/` are not staged
9. confirm the release note still matches the current scope and known limitations

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
