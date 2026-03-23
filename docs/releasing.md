# Releasing

Use this short checklist before publishing a tag or first public repository release.

## Pre-Release Checks

1. run `python scripts/validate_skills.py skills`
2. run `node --check tools/wechat-gui-check/check.js`
3. run `node --check tools/wechat-gui-check/lib/check-helpers.js`
4. run `npm ci --ignore-scripts` inside `tools/wechat-gui-check`
5. run `npm audit --omit=dev` inside `tools/wechat-gui-check`
6. confirm `tools/wechat-gui-check/node_modules` and `.tmp/` are not staged
7. confirm the release note still matches the current scope and known limitations

## Release Framing

For the current `v0.1.0-public-beta` release, describe the repository as:

- a docs-first reusable skill repository
- a public beta for the GUI smoke harness
- a repository with known but isolated upstream dependency findings in the optional GUI tool

## After Publishing

1. create the GitHub release from the matching tag
2. paste the `v0.1.0-public-beta` notes from `CHANGELOG.md`
3. open one follow-up issue for forward-testing the GUI harness on a non-source miniapp repo
4. open one follow-up issue for replacing or isolating the current `miniprogram-automator` image stack
