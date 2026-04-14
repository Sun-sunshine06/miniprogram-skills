---
name: miniapp-devtools-gui-check
description: Use host-side WeChat DevTools automation to inspect GUI-only runtime and interaction failures that do not show up in CLI `preview`. Trigger when page entry, taps, websocket-based DevTools automation, or run-directory evidence such as `report.json` and `trace.log` are needed to separate repo bugs from IDE session problems, local service blockers, or remaining visual-only issues.
---

# Miniapp Devtools Gui Check

## Overview

Use this skill when CLI `preview` is not enough and the user needs GUI-side runtime evidence. Prefer it for smoke coverage, not for full visual regression.

## Quick Start

1. Read `references/gui-check-playbook.md`.
2. Confirm the run will happen on the real host, not inside a restricted sandbox.
3. Start with one route or one user flow, not the full app.
4. Run the local GUI checker if the repo provides one.
5. Inspect the generated `report.json` before claiming success or failure.
6. If `report.json` is missing, inspect `trace.log` in the same run directory before blaming repo code.

## Core Rules

- Treat the host environment as part of the system under test.
- Prefer narrow smoke checks over "all routes at once" until the session is stable.
- Trust runtime exceptions, console events, page path, and selector presence more than screenshots.
- Treat screenshots as best-effort evidence, not the primary signal.
- Keep the checker config-driven so route specs, backend prerequisites, and output locations are explicit.
- If the run directory contains `trace.log` but no `report.json`, classify the failure by stage first:
  - launcher or websocket stage usually means DevTools session or host setup
  - page stage usually means route-level runtime or state issues
- Separate repo bugs, DevTools session problems, local service blockers, and remaining visual-only questions.

## Output Format

When answering, keep the result operational:

1. which route or flow was checked
2. whether automation really connected
3. what runtime evidence was collected
4. whether the issue is in repo code, session state, a local service dependency, or still needs manual visual confirmation
5. the next command or user action

## Resources

- `references/gui-check-playbook.md`: host prerequisites, failure classification, and reporting guidance
- `../../tools/wechat-gui-check/README.md`: current extraction target for the public harness
- `references/example-prompts.md`: reusable trigger examples and evaluation notes
