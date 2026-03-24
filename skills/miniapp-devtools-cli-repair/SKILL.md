---
name: miniapp-devtools-cli-repair
description: Diagnose WeChat DevTools failures through the official CLI instead of relying only on GUI screenshots. Use when Codex needs to run `open`, `preview`, or related commands, discover the live service port, classify whether a failure is CLI-visible, and apply or suggest safe repo-level fixes. 中文：当你需要通过微信开发者工具官方 CLI 运行 `open`、`preview` 等命令，确定 live port、判断问题是否可在 CLI 中复现，并执行或建议安全的仓库级修复时使用。
---

# Miniapp Devtools Cli Repair

## Overview

Use this skill when the user needs CLI-visible evidence from WeChat DevTools. Treat the official CLI as the primary observability surface for compile and preview failures.

## Quick Start

1. Read `references/cli-repair-playbook.md`.
2. Confirm the official DevTools CLI exists and can print help.
3. Use `open` to establish IDE connectivity and the live service port.
4. Use `preview` as the primary mini program compile check.
5. Classify the result as CLI-visible and auto-fixable, CLI-visible but not safe to auto-fix, or GUI-only.

## Core Rules

- Prefer the official WeChat DevTools CLI over screenshots for first-pass diagnosis.
- Treat CLI output, exit code, process state, and local logs as primary evidence.
- For miniapp compile diagnosis, prefer `preview` over `engine build`.
- Use `open` first when the live service port is unknown or the current IDE session is suspect.
- Auto-fix only repository-scoped problems such as root-path drift, page-path mismatch, or small syntax issues surfaced with exact locations.
- Do not claim full coverage when the error exists only in GUI-only panels or compile-mode menus.

## Auto-Fix Boundary

Apply fixes automatically only when they are coherent and local to the repo:

- repair `project.config.json`
- repair `tsconfig.json`
- repair `app.json`
- delete wrong-root residue
- restore tracked files
- replace a pinpointed unsupported syntax form with an equivalent narrow fix

Do not auto-fix without explicit user direction when the change would alter app strategy, publish state, backend settings, or broad syntax across the repo.

## Output Format

When answering, keep the result operational:

1. what the CLI exposed
2. whether the issue is auto-fixable
3. what was changed or what screenshot is still needed
4. the next command or user action

## Resources

- `references/cli-repair-playbook.md`: command ladder, timeout handling, and fix boundaries
- `references/example-prompts.md`: reusable trigger examples and evaluation notes
