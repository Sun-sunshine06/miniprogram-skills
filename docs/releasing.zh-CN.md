# Releasing

[English](./releasing.md) | 中文

在发布 tag 或第一次公开发布仓库前，可以先过一遍这个简短清单。

## 发布前检查

1. 运行 `pwsh -File scripts/check.ps1 -IncludeAudit` 或 `powershell.exe -File scripts/check.ps1 -IncludeAudit`
2. 确认 `tools/wechat-gui-check/node_modules` 和 `.tmp/` 没有被暂存
3. 确认 release note 仍然符合当前范围和已知限制

## 发布时建议的表述

针对当前的 `v0.1.0-public-beta`，建议把仓库描述为：

- 一个文档优先的可复用 skill 仓库
- 一个面向 GUI 冒烟检查工具的 public beta
- 一个默认安装不会自带上游 GUI 图像依赖链，但真实 GUI 自动化仍依赖用户自行提供运行时安装的仓库

## 发布后

1. 在对应 tag 上创建 GitHub Release
2. 把 `CHANGELOG.md` 里的 `v0.1.0-public-beta` 说明粘贴进去
3. 建一个 follow-up issue，用于跟进 GUI harness 在非源仓库小程序上的 forward test
4. 再建一个 follow-up issue，用于决定是否保留当前用户自带 `miniprogram-automator` 的运行时模式
