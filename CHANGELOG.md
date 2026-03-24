# Changelog

All notable changes to this repository will be documented in this file.

## Unreleased

- added a Chinese entry README and a Chinese skill map to improve first-run usability for Chinese-speaking miniapp developers
- added Chinese contributor, conventions, releasing, and `wechat-gui-check` user docs for human-facing repository guidance
- added `references/example-prompts.md` for all four public skills and linked them from each `SKILL.md`
- upgraded `scripts/validate_skills.py` to check required sections, `references/`, `agents/openai.yaml` interface fields, meaningful descriptions, and optional example-prompt presence
- updated CI and release checks to enforce `python scripts/validate_skills.py skills --require-example-prompts`
- added `docs/skill-validation-log.md` with recorded validation passes for all four active skills
- recorded real host-side validation runs for `miniapp-devtools-gui-check`, `miniapp-devtools-cli-repair`, and `miniapp-devtools-recovery`, plus a scaffold validation pass for `miniapp-official-scaffold-alignment`
- moved `tools/wechat-gui-check` to a user-supplied `miniprogram-automator` runtime model so the default repo install and lockfile no longer carry the upstream image-stack dependency chain
- added a `--dry-run` preflight mode and CI coverage for exercising `wechat-gui-check` against a copied miniapp project outside the repository
- fixed the default Windows DevTools CLI path probe for common Chinese-language install directories
- recorded one successful Windows host run against a copied external fixture project, with screenshot capture still treated as best-effort

## v0.1.0-public-beta

Initial public release for the reusable WeChat Mini Program skills set and the first beta extraction of `tools/wechat-gui-check`.

Highlights:

- ships four reusable Codex skills for scaffold alignment, DevTools recovery, CLI diagnosis, and GUI-only smoke checks
- includes a bundled public fixture miniapp so the GUI checker sample config is runnable without a private source repository
- adds validation and repository conventions suitable for public collaboration
- keeps the public boundary explicit by treating the GUI harness as beta rather than pretending the dependency story is fully finished

Known limitations:

- live GUI automation still depends on a user-supplied `miniprogram-automator` runtime install, and that host-side dependency may continue to inherit upstream audit findings
- the full GUI harness still needs forward-testing on more than one non-source miniapp repository
- the repository is documentation-first and is not yet a full GUI automation product or full miniapp boilerplate
