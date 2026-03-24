# WeChat GUI Check

[English](./README.md) | 中文

一套配置驱动的微信开发者工具 GUI 冒烟检查工具，用来检查那些在 CLI `preview` 中看不出来的运行时和交互问题。

## 当前状态

目前是 public beta 抽离版本。仓库自带一个 fixture 小程序示例，默认依赖面也尽量保持轻量：`miniprogram-automator` 不再随仓库默认安装，而是从显式指定的运行时安装位置加载。现在已经支持对仓库外复制出来的小程序根目录做 dry-run 预检，但在独立公开小程序仓库上的完整 forward test 还没做完。

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
- `examples/sample.route-config.json`: 示例路由配置
- `examples/sample-report.json`: 示例输出结构

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

使用你自己的小程序项目：

```powershell
cd tools/wechat-gui-check
npm run check -- --config .\my-routes.json --project-path <project-root> --route home --route tasks
```

`<project-root>` 必须指向一个包含 `project.config.json` 的微信小程序项目根目录。工具会在拉起 DevTools 自动化之前先校验这个目录，并默认优先从该项目里寻找 `miniprogram-automator`。

如果 automator 安装在别的地方，可以显式传入：

```powershell
cd tools/wechat-gui-check
npm run check -- --project-path <project-root> --automator-module-path C:\path\to\miniprogram-automator
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

具体示例见 `examples/sample.route-config.json`。

## 仓库自带 Fixture

仓库在 `examples/fixture-miniapp/` 下提供了一个最小可公开演示的小程序：

- 含有有效的 `project.config.json`
- 含有一个带 `.page-shell`、`.page-title` 和 `.btn-primary` 的 `home` 页面
- 含有一个包含 `.filter-tab` 交互的 `tasks` 页面

这让 sample config 可以稳定复现，也给后续维护工具的贡献者提供了一个安全基线。

## 输出目录结构

```text
.tmp/gui-check/<timestamp>/
|-- report.json
|-- report.partial.json
`-- *.png
```

`--dry-run` 不会创建运行目录，而是把 JSON 形式的预检摘要直接输出到 stdout。

## 说明

- 截图是 best-effort 的，失败不一定代表整次检查失败
- 依赖后端的页面前提应写在 route config 里，不要藏在代码中
- 先从单一路由开始，稳定后再扩展到多路由
- 仓库默认安装现在不再携带 `miniprogram-automator` 的上游图像依赖链；这个依赖改成由用户在执行时自行提供
- 已经有一次在 Windows 宿主机上针对仓库外复制 fixture 项目的成功运行记录；截图在那次运行中曾发生超时，因此目前仍应把截图视为辅助证据
- 在上游依赖方案更稳定之前，这个包会继续保持 beta 状态

## 剩余工作

- 在独立公开小程序仓库上完成完整 forward test
- 补一个真实公开 demo repo 的 sample config
- 决定是否继续保留当前用户自带 `miniprogram-automator` 的运行时模式，还是改成更干净的长期适配方案
