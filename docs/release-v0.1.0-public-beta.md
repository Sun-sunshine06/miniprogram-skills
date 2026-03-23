# v0.1.0-public-beta

## Summary

This is the first public release of `miniprogram_skills`.

The repository starts as a docs-first extraction of reusable WeChat Mini Program skills, with one beta utility under `tools/wechat-gui-check` for GUI-only smoke checks that do not surface in CLI `preview`.

## Included In This Release

- `miniapp-official-scaffold-alignment`
- `miniapp-devtools-recovery`
- `miniapp-devtools-cli-repair`
- `miniapp-devtools-gui-check`
- the `wechat-gui-check` beta harness
- a bundled public fixture miniapp for the harness sample config

## Why This Release Is Public-Ready

- the core skills are reusable without one product repository's hidden context
- the GUI harness now ships with a public demo project instead of assuming a private repo
- the repository has license, contribution, security, validation, issue-template, and PR-template coverage

## Known Limitations

- the GUI harness remains beta
- `tools/wechat-gui-check` still inherits a small remaining set of moderate audit findings through `miniprogram-automator` and its transitive image stack
- the harness still needs broader forward-testing outside the source environment

## Recommended Release Notes Copy

Public beta release for reusable WeChat Mini Program Codex skills and an initial GUI smoke harness. This version focuses on scaffold validation, DevTools recovery, CLI-first diagnosis, and GUI-only runtime checks. The repository is ready for public collaboration, while the optional GUI harness remains beta because of known upstream dependency findings and limited forward-testing coverage.
