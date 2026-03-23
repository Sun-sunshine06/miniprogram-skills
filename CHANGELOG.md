# Changelog

All notable changes to this repository will be documented in this file.

## v0.1.0-public-beta

Initial public release for the reusable WeChat Mini Program skills set and the first beta extraction of `tools/wechat-gui-check`.

Highlights:

- ships four reusable Codex skills for scaffold alignment, DevTools recovery, CLI diagnosis, and GUI-only smoke checks
- includes a bundled public fixture miniapp so the GUI checker sample config is runnable without a private source repository
- adds validation and repository conventions suitable for public collaboration
- keeps the public boundary explicit by treating the GUI harness as beta rather than pretending the dependency story is fully finished

Known limitations:

- `tools/wechat-gui-check` still inherits five moderate audit findings through the upstream `miniprogram-automator` image stack
- the GUI harness still needs forward-testing on more than one non-source miniapp repository
- the repository is documentation-first and is not yet a full GUI automation product or full miniapp boilerplate
