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
- 保持 `agents/openai.yaml` 和 `SKILL.md` 一致。
- 在称某个 skill 已经 public-ready 之前，先用真实提示词做 forward test。

## 非目标

- 不要把这个仓库做成完整的小程序模板工程。
- 不要把产品 roadmap 和可复用 skill 内容混在一起。
- 不要在公开文件里保留没有文档说明的项目私有假设。
