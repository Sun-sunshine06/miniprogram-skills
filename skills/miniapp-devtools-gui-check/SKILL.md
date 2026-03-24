---
name: miniapp-devtools-gui-check
description: Use host-side WeChat DevTools automation to inspect GUI-only runtime and interaction failures that do not show up in CLI `preview`. Trigger when page entry, taps, or websocket-based DevTools automation are needed to separate repo bugs from IDE session problems or remaining visual-only issues. 中文：当 CLI `preview` 看不出问题，而你需要通过页面进入、点击操作或基于 websocket 的 DevTools 自动化来区分仓库缺陷、IDE 会话问题和纯视觉问题时使用。
---

# Miniapp Devtools Gui Check

## Overview

Use this skill when CLI `preview` is not enough and the user needs GUI-side runtime evidence. Prefer it for smoke coverage, not for full visual regression.

## Quick Start

1. Read `references/gui-check-playbook.md`.
2. Confirm the run will happen on the real host, not inside a restricted sandbox.
3. Start with one route or one user flow, not the full app.
4. Run the local GUI checker if the repo provides one.
5. Inspect the generated report before claiming success or failure.

## Core Rules

- Treat the host environment as part of the system under test.
- Prefer narrow smoke checks over "all routes at once" until the session is stable.
- Trust runtime exceptions, console events, page path, and selector presence more than screenshots.
- Treat screenshots as best-effort evidence, not the primary signal.
- Keep the checker config-driven so route specs, backend prerequisites, and output locations are explicit.
- Separate repo bugs, DevTools session problems, and remaining visual-only questions.

## Output Format

When answering, keep the result operational:

1. which route or flow was checked
2. whether automation really connected
3. what runtime evidence was collected
4. whether the issue is in repo code, session state, or still needs manual visual confirmation
5. the next command or user action

## Resources

- `references/gui-check-playbook.md`: host prerequisites, failure classification, and reporting guidance
- `../../tools/wechat-gui-check/README.md`: current extraction target for the public harness
- `references/example-prompts.md`: reusable trigger examples and evaluation notes
