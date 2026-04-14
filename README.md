# Miniprogram Skills

[![Validate](https://github.com/Sun-sunshine06/miniprogram-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Sun-sunshine06/miniprogram-skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/github/license/Sun-sunshine06/miniprogram-skills)](https://github.com/Sun-sunshine06/miniprogram-skills/blob/main/LICENSE)

Reusable Codex skills and playbooks for WeChat Mini Program development, DevTools diagnosis, and scaffold validation.

English | [中文](./README.zh-CN.md)

## Status

This repository is now tagged as `v0.4.0`. The public surface has expanded from four DevTools-and-scaffold skills to six reusable miniapp skills: the original four infrastructure skills remain, and two new public-draft skills now cover hub-style information architecture refactors and user-facing copy trimming. The GUI checker remains a beta utility and now records `trace.log` alongside `report.json` so launcher-stage DevTools hangs can be diagnosed without private source-repo context.

The `v0.4.0` baseline additionally includes a machine-readable public skill catalog plus replayable routing-eval fixtures so future reviews can compare declared skill boundaries against committed evidence assets.

The current `main` branch also carries transcript-backed local routing replays for the committed prompt pack plus repo-owned negative-path fixtures for scaffold, recovery, and GUI/session failure review, while installed-skill and collaborator-host routing evidence are still pending.

## Why This Exists

- WeChat Mini Program setup and DevTools failures repeat across projects.
- CLI-visible failures and GUI-only failures need different workflows.
- Wrong-root imports, stale compile settings, and TypeScript recognition drift are common.
- These patterns are more reusable than any one product repo.

## Current Public Scope

| Skill | Purpose | Status |
| --- | --- | --- |
| `miniapp-official-scaffold-alignment` | Validate or design an officially valid miniapp scaffold. | public draft |
| `miniapp-devtools-recovery` | Recover a repo after wrong-root import, template residue, or compile drift. | public draft |
| `miniapp-devtools-cli-repair` | Diagnose DevTools through the official CLI and classify safe repo-level fixes. | public draft |
| `miniapp-devtools-gui-check` | Run or design host-side GUI smoke checks for runtime-only failures. | public beta tool |
| `miniapp-center-hub-refactor` | Reorganize a growing miniapp into a clearer center or hub with stable ownership. | public draft |
| `miniapp-user-facing-copy-trim` | Shorten verbose miniapp copy into clearer action-first labels and summaries. | public draft |

## Repository Layout

```text
.
|-- docs/
|   |-- conventions.md
|   |-- extraction-checklist.md
|   |-- public-roadmap.md
|   `-- skill-map.md
|-- evals/
|   `-- routing/
|-- manifests/
|   `-- skill-catalog.json
|-- schemas/
|   |-- routing-eval-case.schema.json
|   `-- skill-catalog.schema.json
|-- skills/
|   |-- miniapp-devtools-cli-repair/
|   |-- miniapp-devtools-gui-check/
|   |-- miniapp-devtools-recovery/
|   |-- miniapp-center-hub-refactor/
|   |-- miniapp-user-facing-copy-trim/
|   `-- miniapp-official-scaffold-alignment/
`-- tools/
    `-- wechat-gui-check/
```

## What This Repo Is

- A reusable skill and playbook repo.
- A public extraction target for high-value miniapp workflows.
- A home for patterns that should survive beyond one product codebase.

## What This Repo Is Not Yet

- A complete GUI automation product.
- A full miniapp boilerplate repo.
- A generic home for every business-flow skill from the source project.
- A fully self-contained GUI automation stack; the optional GUI automation flow still depends on a user-supplied `miniprogram-automator` install when you actually run it, even though the repo now includes a dry-run preflight for external project roots.

## Release Direction

1. Treat `v0.4.0` as the stable catalog-and-routing baseline for the extracted skill set and GUI harness.
2. Broaden forward-test and routing evidence across more hosts and repo shapes.
3. Add more negative-path validation for recovery, scaffold, and GUI/session failures.
4. Keep the public boundary clean while forward-testing the newer structure and copy skills on more repo shapes.

## Local Validation

Run the shared local validation flow before opening a PR:

```powershell
pwsh -File scripts/check.ps1
powershell.exe -File scripts/check.ps1
```

This command expects `python`, `node`, and `npm` on `PATH`. It installs the tool dependencies with `npm ci --ignore-scripts`, validates public skills, validates the machine-readable skill catalog, validates both routing fixtures and routing replay transcripts, validates the committed negative-path fixtures, checks markdown links plus bilingual doc cross-links, validates repository JSON, checks tool syntax, and runs the external-project dry-run smoke checks against a copied fixture for both bundled sample configs.

## Immediate Next Steps

- record one collaborator-host forward-test on a public repo with a different scaffold shape
- broaden recovery and success-path CLI public-repo evidence, and add installed-skill or host-routed transcripts beyond the current local replay pack
- add cross-repo forward-testing for the newer hub and copy skills

See [CHANGELOG.md](./CHANGELOG.md), [docs/release-v0.1.0-public-beta.md](./docs/release-v0.1.0-public-beta.md), [docs/release-v0.3.0.md](./docs/release-v0.3.0.md), [docs/release-v0.4.0-draft.md](./docs/release-v0.4.0-draft.md), [docs/releasing.md](./docs/releasing.md), [docs/skill-map.md](./docs/skill-map.md), [docs/skill-map.zh-CN.md](./docs/skill-map.zh-CN.md), [docs/public-roadmap.md](./docs/public-roadmap.md), [docs/v0.2-execution-checklist.md](./docs/v0.2-execution-checklist.md), [docs/skill-validation-log.md](./docs/skill-validation-log.md), [docs/routing-eval-log.md](./docs/routing-eval-log.md), [docs/skill-review-checklist.md](./docs/skill-review-checklist.md), [docs/gui-check-forward-test.md](./docs/gui-check-forward-test.md), [docs/gui-check-collaborator-forward-test.md](./docs/gui-check-collaborator-forward-test.md), [docs/runtime-model-decision.md](./docs/runtime-model-decision.md), [docs/extraction-checklist.md](./docs/extraction-checklist.md), [docs/license-decision.md](./docs/license-decision.md), and [CONTRIBUTING.md](./CONTRIBUTING.md) for the detailed release plan.

