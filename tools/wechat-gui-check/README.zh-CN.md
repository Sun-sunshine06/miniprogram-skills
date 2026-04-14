# WeChat GUI Check

[English](./README.md) | 中文

一套配置驱动的微信开发者工具 GUI 冒烟检查工具，用来检查那些在 CLI `preview` 中看不出来的运行时和交互问题。

## 当前状态

目前是 public beta 抽离版本。仓库自带一个 fixture 小程序示例和两份仓库内 sample 配置，默认依赖面也尽量保持轻量：`miniprogram-automator` 不再随仓库默认安装，而是从显式指定的运行时安装位置加载。现在已经支持对仓库外复制出来的小程序根目录做 dry-run 预检，也已经补了一次面向公开小程序仓库的外部 forward-test 记录；更广泛的跨仓库验证仍在继续。详见 `../../docs/gui-check-forward-test.md`。

## 它能做什么

- 通过官方 CLI 拉起微信开发者工具自动化模式
- 通过 `miniprogram-automator` 建立连接
- 按 JSON 配置打开指定路由
- 执行少量点击、等待或页面方法调用
- 收集运行时异常和 console 事件
- 输出机器可读的 `report.json`
- 以 best-effort 方式截图留证

## 关键文件

- `check.js`: 主运行入口
- `lib/check-helpers.js`: 公共辅助函数
- `examples/sample.route-config.json`: 基础示例路由配置
- `examples/sample.rich.route-config.json`: 覆盖混合 action 类型的 richer 示例配置
- `examples/sample-report.json`: 示例输出结构
- `examples/sample.session-error.json`: fatal session-blocker 的示例输出结构

## 安装

```powershell
cd tools/wechat-gui-check
npm ci
```

在真正运行 GUI 检查之前，还需要把运行时自动化依赖安装在下面任一位置：

```powershell
cd <project-root>
npm install --no-save miniprogram-automator
```

或者：

```powershell
cd tools/wechat-gui-check
npm install --no-save miniprogram-automator
```

## 运行方式

使用仓库自带 fixture 和示例配置：

```powershell
cd tools/wechat-gui-check
npm run check -- --route home
```

默认会把 `examples/fixture-miniapp` 作为项目根目录，把 `examples/sample.route-config.json` 作为路由配置。

如果你想用仓库自带 fixture 顺手覆盖 `wait`、`tap` 和 `callMethod` 三类 action，可以直接跑 richer sample：

```powershell
cd tools/wechat-gui-check
npm run check:fixture:rich:dry-run
```

使用你自己的小程序项目：

```powershell
cd tools/wechat-gui-check
npm run check -- --config .\my-routes.json --project-path <project-root> --route home --route tasks
```

`<project-root>` 必须指向一个包含 `project.config.json` 的微信小程序项目根目录。工具会在拉起 DevTools 自动化之前先校验这个目录，并默认优先从该项目里寻找 `miniprogram-automator`。

如果 automator 安装在别的地方，可以显式传入：

```powershell
cd tools/wechat-gui-check
npm run check -- --project-path <project-root> --automator-module-path <automator-install-root>
```

如果你只想做预检，不真正启动 DevTools：

```powershell
cd tools/wechat-gui-check
npm run check -- --project-path <project-root> --route home --dry-run
```

`--dry-run` 会确认路由配置、选中的 routes、解析出来的小程序根目录是否有效，也会汇报当前机器是否能找到可用的 DevTools CLI 和 `miniprogram-automator` 运行时安装，但不会真正启动自动化会话。

## 路由配置结构

每个 route spec 可以包含：

- `key`
- `route`
- `expectedPath`
- `primarySelector`
- `titleSelector`
- `settleMs`
- `dataFields`
- `actions`

支持的 action 类型：

- `wait`
- `tap`
- `callMethod`

基础多 route 示例见 `examples/sample.route-config.json`；如果要看同一条 route 里串联 `wait`、`tap`、`callMethod` 的写法，见 `examples/sample.rich.route-config.json`。

## 仓库自带 Fixture

仓库在 `examples/fixture-miniapp/` 下提供了一个最小可公开演示的小程序：

- 含有有效的 `project.config.json`
- 含有一个带 `.page-shell`、`.page-title`、`.btn-primary` 和稳定 `applyScenario` page method 的 `home` 页面
- 含有一个包含 `.filter-tab` 交互的 `tasks` 页面

这让 sample config 可以稳定复现，也给后续维护工具的贡献者提供了一个安全基线。

## 输出目录结构

```text
.tmp/gui-check/<timestamp>/
|-- report.json
|-- report.partial.json
|-- trace.log
`-- *.png
```

`--dry-run` 不会创建运行目录，而是把 JSON 形式的预检摘要直接输出到 stdout。

如果运行目录已经生成但没有 `report.json`，先看同目录下的 `trace.log`。它会记录当前卡在 DevTools launcher、websocket 连接、app runtime ready 还是具体 route 执行阶段。

## 排障提示

- `Unable to load miniprogram-automator`：在目标小程序项目里或 `tools/wechat-gui-check` 目录里运行 `npm install --no-save miniprogram-automator`，或者用 `--automator-module-path` 显式指向一个现成安装。
- `登录用户不是该小程序的开发者`：这是 WeChat DevTools 的宿主机账号 / AppID 授权阻塞，不是仓库运行时错误。做公开仓库 forward-test 时，建议先复制一个一次性本地副本，再把真实上游 `appid` 换成 `touristappid` 或你自己可控的测试 `appid`，之后再运行 `cli auto`。
- `screenshot unavailable: miniProgram.screenshot is not a function`：不同 `miniprogram-automator` 版本暴露的截图能力并不完全一致。报告里现在会把这类情况归类为 `screenshot_capability_missing`。当前应把截图视为 best-effort 证据；如果路由、路径和 selector 检查都通过，优先以这些结果为准。
- 截图超时：报告里会归类为 `screenshot_timeout`；除非截图本身就是你要核验的重点，否则不要默认把它当成仓库失败。
- 运行目录存在但没生成 `report.json`：先检查 `trace.log`。如果最后一条仍停在 DevTools 启动或 websocket 连接阶段，优先把它当成宿主机 / 会话问题，而不是仓库代码问题。

## 说明

- 截图是 best-effort 的，失败不一定代表整次检查失败
- 依赖后端的页面前提应写在 route config 里，不要藏在代码中
- 先从单一路由开始，稳定后再扩展到多路由
- richer sample 的存在，是为了在第二个真实公开仓库 sample 还没补齐前，先把 `wait` 和 `callMethod` 的公开可复现覆盖保留下来
- 仓库默认安装现在不再携带 `miniprogram-automator` 的上游图像依赖链；这个依赖改成由用户在执行时自行提供
- 已经有一次在 Windows 宿主机上针对仓库外复制 fixture 项目的成功运行记录；截图在那次运行中曾发生超时，因此目前仍应把截图视为辅助证据
- 现在也已经记录了一次面向公开仓库的 external forward-test，详见 `../../docs/gui-check-forward-test.md`
- 如果第二个公开仓库样本准备交给协作者宿主机执行，直接使用 `../../docs/gui-check-collaborator-forward-test.md`
- 现在 launcher 还带有一个 `cli auto` 超时兜底：如果 DevTools 仍在后台继续启动，工具会继续尝试连 websocket，并把这个决策写进 `trace.log`
- 在上游依赖方案更稳定之前，这个包会继续保持 beta 状态

## 剩余工作

- 把 forward-test 从首个公开小程序仓库扩展到更多仓库样本
- 补一个真实公开 demo repo 的 sample config
- 只有在拿到更多跨机器证据后，再复审当前用户自带 `miniprogram-automator` 的运行时模式是否要演进成更干净的长期适配方案
