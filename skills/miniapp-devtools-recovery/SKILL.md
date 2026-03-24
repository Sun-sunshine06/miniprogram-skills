---
name: miniapp-devtools-recovery
description: Recover a WeChat Mini Program repository after wrong-root import, DevTools template residue, stale compile conditions, or TypeScript-recognition drift. Use when Codex needs to restore the intended repo shape, remove generated clutter, or tell the user exactly what to fix inside DevTools.
---

# Miniapp Devtools Recovery

## Overview

Use this skill when DevTools has polluted the repository or started compiling the wrong thing. Keep the cleanup minimal and restore tracked files before deleting residue.

## Quick Start

1. Read `references/devtools-recovery-checklist.md`.
2. Inspect `git status`, repository root, `project.config.json`, `project.private.config.json`, and `app.json`.
3. Decide whether the problem is wrong import root, template residue, stale compile condition, or TypeScript-recognition drift.
4. Restore tracked files first, then delete only the generated residue.
5. Tell the user exactly which directory to import and which compile mode to use.

## Core Rules

- Treat repository root and miniapp code root as separate concerns.
- Prefer restoring tracked files from version control before deleting generated clutter.
- Keep `project.private.config.json` local-only; do not rely on it for shared project truth.
- Remove generated template pages or helpers unless the app explicitly depends on them.
- If DevTools complains about missing `.js` files while the repo authors in `.ts`, verify TypeScript recognition before rewriting the app to JavaScript.
- If DevTools tries to start from a page not listed in `app.json`, suspect a stale custom compile condition first.

## Output Format

When answering, keep the result short and operational:

1. what DevTools changed
2. what should remain in the repo
3. what to delete or restore
4. what the user must change in DevTools

## Resources

- `references/devtools-recovery-checklist.md`: cleanup rules and error-to-cause mapping
- `references/example-prompts.md`: reusable trigger examples and evaluation notes
