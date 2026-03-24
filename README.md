# Miniprogram Skills

[![Validate](https://github.com/Sun-sunshine06/miniprogram-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Sun-sunshine06/miniprogram-skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/github/license/Sun-sunshine06/miniprogram-skills)](https://github.com/Sun-sunshine06/miniprogram-skills/blob/main/LICENSE)

Reusable Codex skills and playbooks for WeChat Mini Program development, DevTools diagnosis, and scaffold validation.

## Status

This repository is suitable for a public docs-first release. The four core skills are reusable today, each active skill now has example prompts plus at least one recorded validation pass, and the GUI checker ships as a beta utility with a bundled demo miniapp instead of assuming access to a private source repo.

## Why This Exists

- WeChat Mini Program setup and DevTools failures repeat across projects.
- CLI-visible failures and GUI-only failures need different workflows.
- Wrong-root imports, stale compile settings, and TypeScript recognition drift are common.
- These patterns are more reusable than any one product repo.

## Initial Public Scope

| Skill | Purpose | Status |
| --- | --- | --- |
| `miniapp-official-scaffold-alignment` | Validate or design an officially valid miniapp scaffold. | public draft |
| `miniapp-devtools-recovery` | Recover a repo after wrong-root import, template residue, or compile drift. | public draft |
| `miniapp-devtools-cli-repair` | Diagnose DevTools through the official CLI and classify safe repo-level fixes. | public draft |
| `miniapp-devtools-gui-check` | Run or design host-side GUI smoke checks for runtime-only failures. | public beta tool |

## Repository Layout

```text
.
|-- docs/
|   |-- conventions.md
|   |-- extraction-checklist.md
|   |-- public-roadmap.md
|   `-- skill-map.md
|-- skills/
|   |-- miniapp-devtools-cli-repair/
|   |-- miniapp-devtools-gui-check/
|   |-- miniapp-devtools-recovery/
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

1. Keep `v0` documentation-first and easy to review.
2. Harden the extracted GUI smoke harness in `tools/wechat-gui-check`.
3. Add one or more sample repos or fixtures for forward-testing.
4. Expand from DevTools skills into broader miniapp workflow skills only after the public boundary is clean.

## Immediate Next Steps

- Add `docs/skill-review-checklist.md` so PR review can use a short shared rubric.
- Add a single local validation entry point for contributors.
- Forward-test the full GUI harness on an independent public miniapp repo now that all four active skills have recorded validation passes and host-side evidence exists.
- Decide whether to keep the current user-supplied `miniprogram-automator` runtime model or replace it with a cleaner long-term adapter.

See [CHANGELOG.md](./CHANGELOG.md), [docs/release-v0.1.0-public-beta.md](./docs/release-v0.1.0-public-beta.md), [docs/releasing.md](./docs/releasing.md), [docs/skill-map.md](./docs/skill-map.md), [docs/public-roadmap.md](./docs/public-roadmap.md), [docs/v0.2-execution-checklist.md](./docs/v0.2-execution-checklist.md), [docs/skill-validation-log.md](./docs/skill-validation-log.md), [docs/extraction-checklist.md](./docs/extraction-checklist.md), [docs/license-decision.md](./docs/license-decision.md), and [CONTRIBUTING.md](./CONTRIBUTING.md) for the detailed draft plan.

