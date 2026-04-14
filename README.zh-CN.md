# Miniprogram Skills

[English](./README.md) | 中文

面向微信小程序开发、开发者工具诊断与脚手架校验的可复用 Codex skills 与操作手册。

## 当前状态

这个仓库现在已经打上 `v0.4.0` 标签。当前公开范围已经从 4 个 DevTools / scaffold 类 skill 扩展到 7 个可复用 miniapp skill：原有 4 个基础设施 skill 继续保留，另外新增了 3 个 public draft，分别覆盖中心化信息架构重排、待处理队列卡片直达动作，以及用户导向文案收束。`wechat-gui-check` 仍以 beta 工具的形式提供，而且现在除了 `report.json` 之外还会写出 `trace.log`，方便定位 DevTools 宿主侧启动卡住这类问题。

`v0.4.0` 基线还额外纳入了一份机器可读的公开 skill catalog，以及一组可重放的 routing-eval fixtures，方便后续把“声明出来的边界”和“实际记录下来的证据”对齐审查。

当前 `main` 分支还补上了针对这组 committed prompt pack 的 transcript-backed 本地 routing replay 记录，以及面向 scaffold、recovery、GUI/session 失败复核的 repo-owned 负路径样本，不过 installed-skill 和协作者宿主机上的 routing 证据仍然待补。

## 为什么会有这个仓库

- 微信小程序初始化、导入和 DevTools 故障会在不同项目里重复出现。
- 只能在 CLI 里看到的问题，和只能在 GUI 里看到的问题，需要不同的处理流程。
- 错误导入根目录、编译条件残留、TypeScript 识别漂移都很常见。
- 这些模式本身比任何单一业务仓库都更值得沉淀。

## 当前公开范围

| Skill | 用途 | 状态 |
| --- | --- | --- |
| `miniapp-official-scaffold-alignment` | 在开始功能开发前检查或设计符合官方规则的小程序脚手架。 | public draft |
| `miniapp-devtools-recovery` | 在错误导入、模板残留或编译漂移之后恢复仓库。 | public draft |
| `miniapp-devtools-cli-repair` | 通过官方 CLI 诊断 DevTools 问题，并判断哪些仓库级修复是安全的。 | public draft |
| `miniapp-devtools-gui-check` | 对 `preview` 看不到的运行时或交互问题做宿主机 GUI 冒烟检查。 | public beta tool |
| `miniapp-center-hub-refactor` | 把功能增长后变得分散的小程序重排成更清晰的中心 / hub 结构。 | public draft |
| `miniapp-review-queue-actions` | 让待处理 / 审核队列在卡片层直接完成常用动作。 | public draft |
| `miniapp-user-facing-copy-trim` | 把冗长页面文案收成更短、更面向用户的标签与状态摘要。 | public draft |

## 仓库结构

```text
.
|-- docs/
|   |-- conventions.md
|   |-- public-roadmap.md
|   |-- skill-map.md
|   `-- skill-map.zh-CN.md
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
|   |-- miniapp-review-queue-actions/
|   |-- miniapp-user-facing-copy-trim/
|   `-- miniapp-official-scaffold-alignment/
`-- tools/
    `-- wechat-gui-check/
```

## 这个仓库是什么

- 一个可复用的 skill 与 playbook 仓库。
- 一个面向公开抽离的小程序高价值工作流沉淀点。
- 一个希望脱离单一业务代码库后依然能成立的模式集合。

## 这个仓库目前还不是什么

- 不是一个完整的 GUI 自动化产品。
- 不是一个完整的小程序 boilerplate 仓库。
- 不是所有业务流技能的总仓库。
- 不是完全自包含的 GUI 自动化栈；真实 GUI 自动化运行时仍然依赖用户自行提供 `miniprogram-automator`。

## 发布方向

1. 把 `v0.4.0` 视为当前抽离 skill 集合和 GUI harness 的 catalog 与 routing 稳定基线。
2. 继续补强更多宿主机和更多仓库形态下的 forward-test 与 routing 证据。
3. 为 recovery、scaffold 和 GUI/session 失败场景增加更多负路径验证。
4. 在继续扩大公开范围之前，先保持这些公开边界干净，并补强新工作流类 skill 的跨仓库 forward-test。

## 本地校验

在提交 PR 前，先运行这条统一的本地校验命令：

```powershell
pwsh -File scripts/check.ps1
powershell.exe -File scripts/check.ps1
```

这条命令要求 `python`、`node` 和 `npm` 已经在 `PATH` 里。它会自动执行 `npm ci --ignore-scripts` 安装工具依赖，校验公开 skill，校验机器可读的 skill catalog，同时校验 routing-eval fixtures、routing replay transcripts 和已提交的负路径样本，检查 markdown 链接和双语文档互链，校验仓库里的 JSON 文件，检查工具语法，并对复制出来的 fixture 针对两份仓库自带 sample 配置分别运行 external-project dry-run smoke check。

## 当前下一步

- 在不同脚手架形态的公开仓库上补一条协作者宿主机 forward-test 记录。
- 继续补 recovery 和 success-path CLI 的公开仓库证据，并在当前本地 replay pack 之外继续补 installed-skill 或 host-routed transcript。
- 为新的中心重排、队列动作、文案收束 skill 增加跨仓库 forward-test 证据。

## 推荐阅读

- [README.md](./README.md): 英文总览
- [docs/skill-map.zh-CN.md](./docs/skill-map.zh-CN.md): 中文 skill 总览
- [CONTRIBUTING.zh-CN.md](./CONTRIBUTING.zh-CN.md): 中文贡献说明
- [docs/conventions.zh-CN.md](./docs/conventions.zh-CN.md): 中文编写约定
- [docs/releasing.zh-CN.md](./docs/releasing.zh-CN.md): 中文发布清单
- [docs/release-v0.3.0.md](./docs/release-v0.3.0.md): `v0.3.0` 发布说明
- [docs/runtime-model-decision.md](./docs/runtime-model-decision.md): GUI 运行时模型决策记录
- [tools/wechat-gui-check/README.zh-CN.md](./tools/wechat-gui-check/README.zh-CN.md): GUI 工具中文使用说明
- [docs/public-roadmap.md](./docs/public-roadmap.md): 公开路线图
- [docs/v0.2-execution-checklist.md](./docs/v0.2-execution-checklist.md): 当前 `v0.3.0` 基线对应的历史 v0.2 执行清单
- [docs/skill-validation-log.md](./docs/skill-validation-log.md): 当前验证记录
- [docs/routing-eval-plan.md](./docs/routing-eval-plan.md): 下一阶段最小 routing-eval / transcript 方案
- [docs/routing-eval-log.md](./docs/routing-eval-log.md): 当前 routing prompt pack 的首轮观察记录
- [docs/skill-review-checklist.md](./docs/skill-review-checklist.md): skill 评审短清单
- [docs/release-v0.4.0-draft.md](./docs/release-v0.4.0-draft.md): `v0.4.0` 发布说明草稿
- [docs/gui-check-forward-test.md](./docs/gui-check-forward-test.md): GUI 工具外部 forward-test 记录
- [docs/gui-check-collaborator-forward-test.md](./docs/gui-check-collaborator-forward-test.md): 第二个公开样本给协作者执行的 runbook
