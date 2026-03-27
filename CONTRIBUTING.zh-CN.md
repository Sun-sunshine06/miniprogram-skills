# Contributing

[English](./CONTRIBUTING.md) | 中文

## 目标

让这个仓库始终聚焦在可复用的微信小程序 skills 和配套工具上，而不是某一个产品仓库里的私有实现细节。

## 提交改动前

- 确认这个工作流可以复用于不止一个小程序仓库。
- 删除绝对本地路径，除非它们只是带占位符的示例。
- 从核心说明中移除产品专用的 storage key。
- 不要把源仓库特有的基线直接塞进 `SKILL.md`。

## 协作流程

- 合并到 `main` 前，尽量保证 `validate` 是绿色的。
- 如果改动需要评审历史或讨论记录，优先走 Pull Request。
- 如果是小范围的维护者更新，并且仍符合当前分支保护规则，可以直接 push。
- 当 GitHub 提示分支落后于 `main` 时，记得及时同步。

## 本地校验

在提交 PR 前，先运行统一的本地校验命令：

```powershell
pwsh -File scripts/check.ps1
powershell.exe -File scripts/check.ps1
```

这条命令要求 `python`、`node` 和 `npm` 已经在 `PATH` 里。它会在 `tools/wechat-gui-check` 目录执行 `npm ci --ignore-scripts` 安装依赖，校验公开 skill，检查 markdown 链接和双语文档互链，校验仓库里的 JSON 文件，检查工具语法，并对复制出来的 fixture 运行 external-project dry-run smoke check。

## 修改 Skills 时

如果改动位于 `skills/` 下：

1. 更新 `SKILL.md`
2. 如果工作流细节变了，同步更新 `references/`
3. 确认 `agents/openai.yaml` 仍然和 skill 对齐
4. 运行 `pwsh -File scripts/check.ps1` 或 `powershell.exe -File scripts/check.ps1`；如果只是迭代 skill 文案，至少要重新跑一遍 skill validator

## 修改 Tools 时

如果改动位于 `tools/` 下：

- 优先做成配置驱动，而不是把应用路由写死在代码里。
- 新增 flag 或输出字段时同步写进文档。
- 保持 sample config 和 sample report 是最新的。
- 如果某些前提依赖是仓库特有的，要明确写在文档里，不要藏在代码逻辑中。

## 评审标准

只有在下面这些条件成立时，才应该接受改动：

- 公开边界比之前更干净，而不是更脏
- 仓库变得更容易复用
- 文档和工具行为仍然一致
- 文档里的协作流程仍然符合当前仓库规则
- 如果 PR 涉及 `skills/`，评审意见最好能落到 `docs/skill-review-checklist.md` 里的具体检查项
