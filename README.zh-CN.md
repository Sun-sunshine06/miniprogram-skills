# Miniprogram Skills - 微信小程序开发可复用 Codex 与 Claude Code 技能集

[![Validate](https://github.com/Sun-sunshine06/miniprogram-skills/actions/workflows/production.yml/badge.svg)](https://github.com/Sun-sunshine06/miniprogram-skills/actions/workflows/production.yml)
[![License: MIT](https://img.shields.io/github/license/Sun-sunshine06/miniprogram-skills)](https://github.com/Sun-sunshine06/miniprogram-skills/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Sun-sunshine06/miniprogram-skills?style=social)](https://github.com/Sun-sunshine06/miniprogram-skills/stargazers)

[English](./README.md) | **中文**

> 面向微信小程序开发、DevTools 诊断、脚手架校验与小程序架构优化的可复用 AI 编码技能集。支持 Codex 和 Claude Code。

## 什么是 Miniprogram Skills？

**Miniprogram Skills** 是一个专门为微信小程序开发设计的开源 AI 编码技能库。它提供 **6 个可复用技能**，帮助开发者诊断 DevTools 问题、验证项目脚手架、优化小程序架构和改进用户界面文案。

该项目支持 **2 个 AI 编码平台**（Codex 和 Claude Code），并提供完整的**中英文双语文档**。

### 项目数据

| 指标 | 数值 |
|------|------|
| 可复用技能 | 6 个 |
| 支持的 AI 平台 | 2 个（Codex、Claude Code） |
| GitHub 标签 | 13 个 |
| 文档语言 | 2 种（英文、中文） |
| 评估 Fixtures | 10+ 个 |
| 机器可读目录 | 1 个（JSON） |

## 为什么会有这个仓库

基于[微信小程序官方开发文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)和[微信开发者工具文档](https://developers.weixin.qq.com/miniprogram/dev/devtools/)，常见问题包括：

- 微信小程序初始化、导入和 DevTools 故障会在不同项目里重复出现
- 只能在 CLI 里看到的问题，和只能在 GUI 里看到的问题，需要不同的处理流程
- 错误导入根目录、编译条件残留、TypeScript 识别漂移都很常见
- 这些模式本身比任何单一业务仓库都更值得沉淀

## 功能特性

- **6 个可复用技能** - 覆盖脚手架校验、DevTools 恢复、CLI 诊断、GUI 检查、架构重构和文案优化
- **双平台支持** - 同时支持 Codex 和 Claude Code
- **TypeScript 支持** - 完整的小程序 TypeScript 开发支持
- **双语文档** - 完整的中英文文档
- **机器可读目录** - 基于 JSON 的技能目录，支持自动化
- **路由评估** - 可重放的 fixtures 用于技能边界测试

## 当前公开技能

| 技能 | 用途 | 状态 |
| --- | --- | --- |
| `miniapp-official-scaffold-alignment` | 在开始功能开发前检查或设计符合官方规则的小程序脚手架 | public draft |
| `miniapp-devtools-recovery` | 在错误导入、模板残留或编译漂移之后恢复仓库 | public draft |
| `miniapp-devtools-cli-repair` | 通过官方 CLI 诊断 DevTools 问题，并判断哪些仓库级修复是安全的 | public draft |
| `miniapp-devtools-gui-check` | 对 `preview` 看不到的运行时或交互问题做宿主机 GUI 冒烟检查 | public beta tool |
| `miniapp-center-hub-refactor` | 把功能增长后变得分散的小程序重排成更清晰的中心 / hub 结构 | public draft |
| `miniapp-user-facing-copy-trim` | 把冗长页面文案收成更短、更面向用户的标签与状态摘要 | public draft |

## 使用场景

| 场景 | 推荐技能 | 说明 |
|------|---------|------|
| DevTools 报错 | `miniapp-devtools-cli-repair` | 通过官方 CLI 诊断 CLI 可见的故障 |
| 错误导入根目录 | `miniapp-devtools-recovery` | 从错误导入或模板残留中恢复 |
| 脚手架校验 | `miniapp-official-scaffold-alignment` | 验证项目结构是否符合官方指南 |
| GUI 运行时问题 | `miniapp-devtools-gui-check` | 检查仅 GUI 可见的运行时故障 |
| 导航重组 | `miniapp-center-hub-refactor` | 将分散的标签重组为 hub 结构 |
| 冗长 UI 文案 | `miniapp-user-facing-copy-trim` | 简化用户界面文案 |

## 快速开始

### Codex 用户

技能会自动从 `skills/` 目录加载。每个技能都有一个 `agents/openai.yaml` 配置文件。

### Claude Code 用户

技能可以通过两种方式触发：

1. **自动触发**：Claude Code 根据 `description` 字段自动调用技能
2. **手动触发**：使用斜杠命令，如 `/miniapp-devtools-recovery` 或 `/miniapp-official-scaffold-alignment`

### 安装

```bash
# 克隆仓库
git clone https://github.com/Sun-sunshine06/miniprogram-skills.git

# 进入项目目录
cd miniprogram-skills

# 运行验证
pwsh -File scripts/check.ps1
```

## 仓库结构

```text
.
├── docs/                           # 文档
│   ├── conventions.md              # 编写约定
│   ├── public-roadmap.md           # 开发路线图
│   └── skill-map.md               # 技能概览
├── evals/                          # 评估 fixtures
│   ├── routing/                    # 路由测试用例
│   └── routing-replays/           # 重放 transcripts
├── manifests/                      # 机器可读目录
│   └── skill-catalog.json         # 公开技能目录
├── schemas/                        # JSON schemas
├── skills/                         # 技能定义
│   ├── miniapp-devtools-cli-repair/
│   ├── miniapp-devtools-gui-check/
│   ├── miniapp-devtools-recovery/
│   ├── miniapp-center-hub-refactor/
│   ├── miniapp-user-facing-copy-trim/
│   └── miniapp-official-scaffold-alignment/
└── tools/                          # 工具
    └── wechat-gui-check/          # GUI 冒烟检查器
```

## 平台兼容性

所有技能同时支持 Codex 和 Claude Code：

- **Codex**：从 SKILL.md 读取 `name` 和 `description`，使用 `agents/openai.yaml` 进行平台配置
- **Claude Code**：读取 SKILL.md 的所有字段，包括可选的 `tools` 和 `slash_command`

### 斜杠命令

每个技能都可以在 Claude Code 中使用斜杠命令手动触发：

| 技能 | 斜杠命令 |
|------|----------|
| `miniapp-official-scaffold-alignment` | `/miniapp-official-scaffold-alignment` |
| `miniapp-devtools-recovery` | `/miniapp-devtools-recovery` |
| `miniapp-devtools-cli-repair` | `/miniapp-devtools-cli-repair` |
| `miniapp-devtools-gui-check` | `/miniapp-devtools-gui-check` |
| `miniapp-center-hub-refactor` | `/miniapp-center-hub-refactor` |
| `miniapp-user-facing-copy-trim` | `/miniapp-user-facing-copy-trim` |

## 常见问题 (FAQ)

### 这个仓库是做什么的？

Miniprogram Skills 是一个面向微信小程序开发的开源 AI 编码技能库。它提供可复用的技能，用于诊断 DevTools 问题、验证项目脚手架、优化小程序架构和改进用户界面文案。

### 如何在 Claude Code 中使用这些技能？

在 Claude Code 中使用技能有两种方式：
1. **自动触发**：Claude Code 根据 SKILL.md 中的 `description` 字段自动调用技能
2. **手动触发**：使用斜杠命令，如 `/miniapp-devtools-recovery` 或 `/miniapp-official-scaffold-alignment`

### 支持哪些 AI 编码平台？

Miniprogram Skills 支持 **2 个 AI 编码平台**：
- **Codex**（OpenAI）- 使用 `agents/openai.yaml` 配置
- **Claude Code**（Anthropic）- 使用 SKILL.md 的 `tools` 和 `slash_command` 字段

### 这些技能可以诊断哪些类型的问题？

技能可以诊断：
- **CLI 可见的故障**：编译错误、预览问题、服务端口问题
- **仅 GUI 可见的运行时问题**：页面加载失败、交互问题、WebSocket 问题
- **项目结构问题**：错误导入根目录、模板残留、TypeScript 识别漂移
- **架构问题**：分散的导航、冗长的 UI 文案

### 这个项目是否在积极维护？

是的，该项目在积极维护并定期更新。当前版本是 `v0.4.0`，包含 6 个公开技能和全面的评估 fixtures。

### 如何为这个项目做贡献？

请参阅 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解贡献指南。该项目欢迎各种贡献，包括新技能、错误修复、文档改进和在不同小程序仓库上的 forward-testing。

## 本地校验

在提交 PR 前，先运行这条统一的本地校验命令：

```powershell
pwsh -File scripts/check.ps1
```

这条命令会验证：
- 公开技能结构和元数据
- 机器可读技能目录
- 路由 fixtures 和 replay transcripts
- 负路径样本
- Markdown 链接和双语文档互链
- 仓库 JSON 文件有效性
- 工具语法
- 外部项目 dry-run 冒烟检查

## 贡献

请参阅 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解贡献指南。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](./LICENSE) 文件。

## 相关链接

- [文档](./docs/)
- [技能地图](./docs/skill-map.zh-CN.md)
- [公开路线图](./docs/public-roadmap.md)
- [发布说明](./docs/release-v0.4.0-draft.md)
- [更新日志](./CHANGELOG.md)
