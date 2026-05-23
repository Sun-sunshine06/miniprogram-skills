# Conventions

[English](./conventions.md) | 中文

## 仓库目标

编写可以跨多个微信小程序仓库复用的 skills，而不是只服务于某一个源项目。

## Skill 目录的最小结构

每个公开 skill 至少应保持下面这个结构：

```text
skill-name/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
`-- references/
```

## SKILL.md YAML 前置元数据

所有 SKILL.md 文件使用 YAML 前置元数据（frontmatter），包含以下字段：

| 字段 | 是否必须 | 说明 |
|------|----------|------|
| `name` | 是 | Skill 标识符，小写字母加连字符 |
| `description` | 是 | Skill 描述，用于自动触发检测 |
| `tools` | 否 | Claude Code 可用的工具列表 |
| `slash_command` | 否 | 手动触发命令，格式：`/skill-name` |

示例：

```yaml
---
name: my-skill
description: Description of when to use this skill.
tools:
  - Bash
  - Read
  - Edit
slash_command: /my-skill
---
```

Codex 会忽略 `tools` 和 `slash_command` 字段，继续使用 `agents/openai.yaml`。

## 编写规则

- `SKILL.md` 保持简短、偏流程化。
- 详细推理、检查清单和示例放到 `references/`。
- 用 `<project-root>`、`<cli-path>`、`<miniapp-root>` 这类占位符，不要直接写本地绝对路径。
- 仓库特有证据不要放进 skill 主体。
- 触发条件要写进 YAML 的 `description`，不要只写在 markdown 正文里。
- 优先使用可执行、可操作的输出格式，不要写成长篇叙事。

## 公开化规则

- 删除或替换对工作流不是必须的产品名。
- 如果 storage key 不是公开契约的一部分，就不要保留。
- 具体路由名改成更有代表性的公开示例。
- 把规范性结论和仓库特有观察分开。
- 如果工具还没有真正抽离成熟，要明确标记成 draft 或 beta。

## 校验规则

- 每次对 skill 做较大修改后，都运行 skill validator。
- 保持 `manifests/skill-catalog.json` 与当前公开 skill 边界、宿主依赖和证据状态一致。
- 保持 `agents/openai.yaml` 和 `SKILL.md` 一致。
- 如果公开 skill 的路由边界变了，就同步补或更新对应的 `evals/routing/` fixtures。
- 如果 committed routing fixture 或输出契约变了，也要同步补或更新对应的 `evals/routing-replays/` transcript 记录。
- 在称某个 skill 已经 public-ready 之前，先用真实提示词做 forward test。

## 非目标

- 不要把这个仓库做成完整的小程序模板工程。
- 不要把产品 roadmap 和可复用 skill 内容混在一起。
- 不要在公开文件里保留没有文档说明的项目私有假设。
