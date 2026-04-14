---
name: miniapp-devtools-cli-repair
description: Diagnose WeChat DevTools failures through the official CLI instead of relying only on GUI screenshots. Use when Codex needs to run `open`, `preview`, or related commands, discover the live service port, classify whether a failure is CLI-visible, host-side, or outside preview scope, and apply or suggest only safe repo-level fixes.
---

# Miniapp Devtools Cli Repair

## Overview

Use this skill when the user needs CLI-visible evidence from WeChat DevTools. Treat the official CLI as the primary observability surface for compile and preview failures.

## Quick Start

1. Read `references/cli-repair-playbook.md`.
2. Confirm the official DevTools CLI exists and can print help.
3. Use `open` to establish IDE connectivity and the live service port.
4. Use `preview` as the primary mini program compile check.
5. Classify the result as:
   - CLI-visible and auto-fixable
   - CLI-visible but not safe to auto-fix
   - host or account blocker
   - outside preview scope and better handled by GUI or service-level debugging

## Core Rules

- Prefer the official WeChat DevTools CLI over screenshots for first-pass diagnosis.
- Treat CLI output, exit code, process state, and local logs as primary evidence.
- For miniapp compile diagnosis, prefer `preview` over `engine build`.
- Use `open` first when the live service port is unknown or the current IDE session is suspect.
- Auto-fix only repository-scoped problems such as root-path drift, page-path mismatch, or small syntax issues surfaced with exact locations.
- If `preview` is already green or the remaining blocker is a page-side `request:fail`, do not keep grinding CLI repair; move to GUI/runtime or service debugging.
- Do not claim full coverage when the error exists only in GUI-only panels, runtime requests, or compile-mode menus.

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
3. what was changed or what further evidence is still needed
4. the next command or user action

## Resources

- `references/cli-repair-playbook.md`: command ladder, timeout handling, and fix boundaries
- `references/example-prompts.md`: reusable trigger examples and evaluation notes
