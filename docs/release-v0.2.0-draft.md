# v0.2.0 Draft Release Notes

## Summary

`v0.2.0` moves `miniprogram_skills` from a docs-first public beta toward a more validated and repeatable public toolkit.

The four public skills now ship with reusable prompt examples plus recorded validation evidence, contributors get a shared local check flow mirrored by CI, and `tools/wechat-gui-check` now has clearer failure classification, richer bundled samples, and one documented forward-test on a public miniapp repository outside this repo.

## What Improved For Skill Consumers

- every public skill now includes `references/example-prompts.md`
- every active skill now has at least one recorded validation pass in `docs/skill-validation-log.md`
- shared validation now catches more repo-local leakage, including absolute home-directory paths and `~/.codex` assumptions
- `wechat-gui-check` now ships with a bundled fixture miniapp plus two public sample route configs for reproducible smoke checks

## What Improved For Contributors

- one shared validation entry point is now documented: `powershell.exe -File scripts/check.ps1`
- CI now mirrors the shared validation flow across skill metadata, example prompts, docs hygiene, repo JSON, and GUI dry-run smoke coverage
- `docs/skill-review-checklist.md` makes skill-focused PR expectations explicit
- `docs/gui-check-forward-test.md`, `docs/gui-check-collaborator-forward-test.md`, and `scripts/collect_gui_check_env.ps1` make host-side evidence collection more repeatable

## Still Intentionally Beta

- live GUI automation still depends on a user-supplied `miniprogram-automator` runtime install
- only one external public-repo forward-test is recorded so far, so broader cross-machine evidence is still pending
- screenshot capture remains best-effort evidence rather than the main release gate
- this repository still focuses on DevTools and scaffold workflows, not a full GUI automation product or generic business-flow skill set

## Likely v0.3 Focus

- add more external forward-tests, especially on collaborator hosts and on repos with different scaffold shapes
- revisit the runtime model only if broader cross-machine evidence shows the current user-supplied approach is no longer the right tradeoff
- continue proving that the public skills generalize cleanly across more than one repo shape
- only expand into higher-level miniapp workflow skills after the public boundary remains clean under that broader testing

## Suggested Release Notes Copy

`miniprogram_skills v0.2.0` strengthens the repository's public boundary and contributor workflow. All four public skills now include reusable example prompts and recorded validation evidence, the shared validation flow now checks skills, docs, JSON, and GUI dry-run behavior in one command, and `wechat-gui-check` now has clearer failure classification, richer bundled samples, and a documented forward-test on a public miniapp repo. The GUI harness remains beta because live automation still depends on a user-supplied `miniprogram-automator` install and broader cross-machine evidence is still in progress.
