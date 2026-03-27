# Changelog

All notable changes to this repository will be documented in this file.

## Unreleased

- added a Chinese entry README and a Chinese skill map to improve first-run usability for Chinese-speaking miniapp developers
- added Chinese contributor, conventions, releasing, and `wechat-gui-check` user docs for human-facing repository guidance
- added `references/example-prompts.md` for all four public skills and linked them from each `SKILL.md`
- added `docs/skill-review-checklist.md` so skill-focused PRs can be reviewed against a short shared rubric
- added `scripts/check.ps1` as the shared local validation entry point and aligned README, release docs, and CI around it
- added `scripts/validate_docs.py` so shared validation now checks markdown links and bilingual document cross-links
- upgraded `scripts/validate_skills.py` to check required sections, `references/`, `agents/openai.yaml` interface fields, meaningful descriptions, and optional example-prompt presence
- updated CI and release checks to enforce `python scripts/validate_skills.py skills --require-example-prompts`
- expanded JSON validation from selected examples to all repo-owned `.json` files outside generated/vendor directories
- added `docs/skill-validation-log.md` with recorded validation passes for all four active skills
- added `docs/gui-check-forward-test.md` with the first documented external public-repo forward-test for `wechat-gui-check`, including an AppID-authorization blocker note from a screened candidate repo
- added `docs/gui-check-collaborator-forward-test.md` plus `scripts/collect_gui_check_env.ps1` so the second public-repo sample can be run on a collaborator machine with standardized evidence capture
- recorded real host-side validation runs for `miniapp-devtools-gui-check`, `miniapp-devtools-cli-repair`, and `miniapp-devtools-recovery`, plus a scaffold validation pass for `miniapp-official-scaffold-alignment`
- moved `tools/wechat-gui-check` to a user-supplied `miniprogram-automator` runtime model so the default repo install and lockfile no longer carry the upstream image-stack dependency chain
- added a `--dry-run` preflight mode and CI coverage for exercising `wechat-gui-check` against a copied miniapp project outside the repository
- fixed the default Windows DevTools CLI path probe for common Chinese-language install directories
- improved `wechat-gui-check` cleanup and README troubleshooting guidance after the first public-repo forward-test
- refined GUI screenshot warnings so unsupported screenshot APIs classify as `screenshot_capability_missing` instead of the broader `devtools_session_error`
- recorded one successful Windows host run against a copied external fixture project, with screenshot capture still treated as best-effort
- added `examples/sample.rich.route-config.json` plus fixture and dry-run coverage updates so the bundled public sample surface now exercises `wait`, `tap`, and `callMethod`
- drafted `docs/release-v0.2.0-draft.md` so the current v0.2 release story is ready without reconstructing context from recent commits

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
