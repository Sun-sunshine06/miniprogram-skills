# Miniprogram Skills - Reusable Codex & Claude Code Skills for WeChat Mini Program Development

[![Validate](https://github.com/Sun-sunshine06/miniprogram-skills/actions/workflows/production.yml/badge.svg)](https://github.com/Sun-sunshine06/miniprogram-skills/actions/workflows/production.yml)
[![License: MIT](https://img.shields.io/github/license/Sun-sunshine06/miniprogram-skills)](https://github.com/Sun-sunshine06/miniprogram-skills/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Sun-sunshine06/miniprogram-skills?style=social)](https://github.com/Sun-sunshine06/miniprogram-skills/stargazers)

**English** | [中文](./README.zh-CN.md)

> Reusable AI coding skills for WeChat Mini Program development, DevTools diagnosis, scaffold validation, and miniapp architecture optimization. Works with Codex and Claude Code.

## What is Miniprogram Skills?

**Miniprogram Skills** is an open-source AI coding skill library specifically designed for WeChat Mini Program development. It provides **6 reusable skills** that help developers diagnose DevTools issues, validate project scaffolds, optimize miniapp architecture, and improve user-facing copy.

The project supports **2 AI coding platforms** (Codex and Claude Code) and includes complete **bilingual documentation** in English and Chinese.

### Key Statistics

| Metric | Value |
|--------|-------|
| Reusable Skills | 6 |
| AI Platforms Supported | 2 (Codex, Claude Code) |
| GitHub Topics | 13 |
| Documentation Languages | 2 (English, Chinese) |
| Evaluation Fixtures | 10+ |
| Machine-Readable Catalog | 1 (JSON) |

## Why This Exists

Based on [WeChat Mini Program Official Documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/) and [WeChat DevTools Documentation](https://developers.weixin.qq.com/miniprogram/dev/devtools/), common issues include:

- WeChat Mini Program setup and DevTools failures repeat across projects
- CLI-visible failures and GUI-only failures need different workflows
- Wrong-root imports, stale compile settings, and TypeScript recognition drift are common
- These patterns are more reusable than any one product repo

## Features

- **6 Reusable Skills** - Covering scaffold validation, DevTools recovery, CLI diagnosis, GUI checks, architecture refactoring, and copy optimization
- **Dual Platform Support** - Works with both Codex and Claude Code
- **TypeScript Ready** - Full TypeScript support for miniapp development
- **Bilingual Documentation** - Complete English and Chinese documentation
- **Machine-Readable Catalog** - JSON-based skill catalog for automation
- **Routing Evaluation** - Replayable fixtures for skill boundary testing

## Current Public Skills

| Skill | Purpose | Status |
| --- | --- | --- |
| `miniapp-official-scaffold-alignment` | Validate or design an officially valid miniapp scaffold | public draft |
| `miniapp-devtools-recovery` | Recover a repo after wrong-root import, template residue, or compile drift | public draft |
| `miniapp-devtools-cli-repair` | Diagnose DevTools through the official CLI and classify safe repo-level fixes | public draft |
| `miniapp-devtools-gui-check` | Run or design host-side GUI smoke checks for runtime-only failures | public beta tool |
| `miniapp-center-hub-refactor` | Reorganize a growing miniapp into a clearer center or hub with stable ownership | public draft |
| `miniapp-user-facing-copy-trim` | Shorten verbose miniapp copy into clearer action-first labels and summaries | public draft |

## Use Case Scenarios

| Scenario | Recommended Skill | Description |
|----------|------------------|-------------|
| DevTools shows errors | `miniapp-devtools-cli-repair` | Diagnose CLI-visible failures through official CLI |
| Wrong root import | `miniapp-devtools-recovery` | Recover from wrong-root imports or template residue |
| Scaffold validation | `miniapp-official-scaffold-alignment` | Validate project structure against official guidelines |
| GUI runtime issues | `miniapp-devtools-gui-check` | Check GUI-only runtime failures |
| Navigation reorganization | `miniapp-center-hub-refactor` | Reorganize scattered tabs into hub structure |
| Verbose UI copy | `miniapp-user-facing-copy-trim` | Simplify user-facing text |

## Quick Start

### For Codex Users

Skills are automatically loaded from the `skills/` directory. Each skill has an `agents/openai.yaml` configuration file.

### For Claude Code Users

Skills can be triggered in two ways:

1. **Auto-trigger**: Claude Code automatically invokes skills based on the `description` field
2. **Manual trigger**: Use slash commands like `/miniapp-devtools-recovery`

### Installation

```bash
# Clone the repository
git clone https://github.com/Sun-sunshine06/miniprogram-skills.git

# Navigate to the project
cd miniprogram-skills

# Run validation
pwsh -File scripts/check.ps1
```

## Repository Layout

```text
.
├── docs/                           # Documentation
│   ├── conventions.md              # Writing conventions
│   ├── public-roadmap.md           # Development roadmap
│   └── skill-map.md               # Skill overview
├── evals/                          # Evaluation fixtures
│   ├── routing/                    # Routing test cases
│   └── routing-replays/           # Replay transcripts
├── manifests/                      # Machine-readable catalogs
│   └── skill-catalog.json         # Public skill catalog
├── schemas/                        # JSON schemas
├── skills/                         # Skill definitions
│   ├── miniapp-devtools-cli-repair/
│   ├── miniapp-devtools-gui-check/
│   ├── miniapp-devtools-recovery/
│   ├── miniapp-center-hub-refactor/
│   ├── miniapp-user-facing-copy-trim/
│   └── miniapp-official-scaffold-alignment/
└── tools/                          # Utilities
    └── wechat-gui-check/          # GUI smoke checker
```

## Platform Compatibility

All skills support both Codex and Claude Code:

- **Codex**: Reads `name` and `description` from SKILL.md, uses `agents/openai.yaml` for platform config
- **Claude Code**: Reads all SKILL.md fields including optional `tools` and `slash_command`

### Slash Commands

Each skill can be triggered manually in Claude Code using its slash command:

| Skill | Slash Command |
|-------|---------------|
| `miniapp-official-scaffold-alignment` | `/miniapp-official-scaffold-alignment` |
| `miniapp-devtools-recovery` | `/miniapp-devtools-recovery` |
| `miniapp-devtools-cli-repair` | `/miniapp-devtools-cli-repair` |
| `miniapp-devtools-gui-check` | `/miniapp-devtools-gui-check` |
| `miniapp-center-hub-refactor` | `/miniapp-center-hub-refactor` |
| `miniapp-user-facing-copy-trim` | `/miniapp-user-facing-copy-trim` |

## Frequently Asked Questions (FAQ)

### What is Miniprogram Skills used for?

Miniprogram Skills is an open-source AI coding skill library for WeChat Mini Program development. It provides reusable skills for diagnosing DevTools issues, validating project scaffolds, optimizing miniapp architecture, and improving user-facing copy.

### How do I use these skills with Claude Code?

You can use skills in Claude Code in two ways:
1. **Auto-trigger**: Claude Code automatically invokes skills based on the `description` field in SKILL.md
2. **Manual trigger**: Use slash commands like `/miniapp-devtools-recovery` or `/miniapp-official-scaffold-alignment`

### Which AI coding platforms are supported?

Miniprogram Skills supports **2 AI coding platforms**:
- **Codex** (OpenAI) - Uses `agents/openai.yaml` configuration
- **Claude Code** (Anthropic) - Uses SKILL.md frontmatter with `tools` and `slash_command` fields

### What types of issues can these skills diagnose?

The skills can diagnose:
- **CLI-visible failures**: Compile errors, preview issues, service port problems
- **GUI-only runtime issues**: Page load failures, interaction problems, WebSocket issues
- **Project structure issues**: Wrong root imports, template residue, TypeScript recognition drift
- **Architecture problems**: Scattered navigation, verbose UI copy

### Is this project actively maintained?

Yes, the project is actively maintained with regular updates. The current version is `v0.4.0` with 6 public skills and comprehensive evaluation fixtures.

### How do I contribute to this project?

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines. The project welcomes contributions including new skills, bug fixes, documentation improvements, and forward-testing on different miniapp repos.

## Local Validation

Run the shared local validation flow before opening a PR:

```powershell
pwsh -File scripts/check.ps1
```

This command validates:
- Public skills structure and metadata
- Machine-readable skill catalog
- Routing fixtures and replay transcripts
- Negative-path fixtures
- Markdown links and bilingual cross-links
- Repository JSON validity
- Tool syntax
- External-project dry-run smoke checks

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Links

- [Documentation](./docs/)
- [Skill Map](./docs/skill-map.md)
- [Public Roadmap](./docs/public-roadmap.md)
- [Release Notes](./docs/release-v0.4.0-draft.md)
- [Changelog](./CHANGELOG.md)
