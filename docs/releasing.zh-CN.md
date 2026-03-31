# Releasing

[English](./releasing.md) | 中文

在发布 tag 或仓库版本前，可以先过一遍这个简短清单。

## 发布前检查

1. 运行 `pwsh -File scripts/check.ps1 -IncludeAudit` 或 `powershell.exe -File scripts/check.ps1 -IncludeAudit`
2. 确认 `tools/wechat-gui-check/node_modules` 和 `.tmp/` 没有被暂存
3. 确认 release note 仍然符合当前范围和已知限制

## 发布时建议的表述

针对 `v0.3.0` 这个版本，建议把仓库描述为：

- 一个四个公开 skill 都已经补齐示例提示词和验证记录的可复用 skill 仓库
- 一个本地校验入口和 CI 校验流已经基本统一的贡献友好型仓库
- 一个面向 GUI 冒烟检查工具的 public beta，并且现在已经带有更丰富的仓库内 sample 和一条外部公开仓库 forward-test 记录
- 一个默认安装不会自带上游 GUI 图像依赖链，但真实 GUI 自动化仍依赖用户自行提供运行时安装的仓库
- 一个已经进入 `v0.3` 证据补强阶段的仓库，接下来的重点是协作者宿主机验证和 routing transcript，而不是把这些作为当前发版阻塞项

## 发布后

1. 在对应 tag 上创建 GitHub Release
2. 以 `docs/release-v0.3.0.md` 为基础整理发布说明，并同步回 `CHANGELOG.md`
3. 建一个 follow-up issue，用于跟进协作者宿主机上的 GUI harness forward-test 和 routing-eval 证据
4. 再建一个 follow-up issue，用于在拿到更完整的 `v0.3` 证据后决定是否保留当前用户自带 `miniprogram-automator` 的运行时模式
