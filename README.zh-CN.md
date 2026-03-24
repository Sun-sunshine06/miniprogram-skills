# Miniprogram Skills

[English](./README.md) | 中文

面向微信小程序开发、开发者工具诊断与脚手架校验的可复用 Codex skills 与操作手册。

## 当前状态

这个仓库已经适合以“文档优先”的方式公开发布。当前四个核心 skill 都可以复用，每个 active skill 都已经补齐示例提示词并至少记录过一次验证；`wechat-gui-check` 则以 beta 工具的形式提供，并附带了一个公开可运行的示例小程序。

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

## 仓库结构

```text
.
|-- docs/
|   |-- conventions.md
|   |-- public-roadmap.md
|   |-- skill-map.md
|   `-- skill-map.zh-CN.md
|-- skills/
|   |-- miniapp-devtools-cli-repair/
|   |-- miniapp-devtools-gui-check/
|   |-- miniapp-devtools-recovery/
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

1. 保持 `v0` 以文档优先、易于审阅为主。
2. 继续打磨 `tools/wechat-gui-check` 这套抽离出来的 GUI 冒烟检查工具。
3. 增加一个或多个用于 forward test 的样例仓库或夹具。
4. 只有在公开边界足够干净后，再从 DevTools 技能扩展到更高层的小程序工作流技能。

## 当前下一步

- 增加 `docs/skill-review-checklist.md`，让 PR 评审有一个统一而简短的标准。
- 增加一个单命令的本地校验入口，方便贡献者在提交前自检。
- 在独立的公开小程序仓库上做一次完整 forward test。
- 继续评估当前用户自带 `miniprogram-automator` 的运行时模式是否要保留。

## 推荐阅读

- [README.md](./README.md): 英文总览
- [docs/skill-map.zh-CN.md](./docs/skill-map.zh-CN.md): 中文 skill 总览
- [docs/public-roadmap.md](./docs/public-roadmap.md): 公开路线图
- [docs/v0.2-execution-checklist.md](./docs/v0.2-execution-checklist.md): v0.2 执行清单
- [docs/skill-validation-log.md](./docs/skill-validation-log.md): 当前验证记录
