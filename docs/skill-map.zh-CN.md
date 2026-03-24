# Skill Map

[English](./skill-map.md) | 中文

## 当前公开 Skills

| Skill | 用途 | 当前形态 | 公开成熟度 |
| --- | --- | --- | --- |
| `miniapp-official-scaffold-alignment` | 在功能开发开始前验证脚手架是否正确。 | `SKILL.md` + 官方基线参考文档 | medium |
| `miniapp-devtools-recovery` | 在错误导入根目录或 DevTools 模板污染后恢复仓库。 | `SKILL.md` + 恢复检查清单 | medium |
| `miniapp-devtools-cli-repair` | 把官方 DevTools CLI 作为主诊断路径。 | `SKILL.md` + CLI playbook | high |
| `miniapp-devtools-gui-check` | 捕捉 `preview` 暴露不出来的运行时和交互故障。 | `SKILL.md` + GUI playbook + public beta tool | high |

## 计划中的 Skills

这些方向有价值，但当前仍然和具体产品实现绑定得更紧，所以没有进入第一批公开范围：

| Skill | 用途 | 暂未纳入原因 |
| --- | --- | --- |
| `miniprogram-local-backend-bridge` | 让小程序连接本地后端并带有降级路径。 | 仍依赖具体本地后端契约和运行时选择 |
| `miniapp-design-system-evolution` | 演进一个可复用的小程序设计系统。 | 仍依赖仓库特定的视觉案例与资产 |
| `miniprogram-task-center-scaffold` | 构建一个支持写入和刷新流的任务中心页面。 | 仍绑定某个应用的数据模型和页面契约 |

## 晋升为公开 Skill 的标准

- 不依赖某个源仓库的上下文也能理解。
- 核心说明里不包含绝对路径、私有路由名或业务专用存储键。
- 触发条件描述稳定明确。
- 至少有一份可复用的参考文档解释流程。
- 能在另一个小程序仓库上通过 forward test。
