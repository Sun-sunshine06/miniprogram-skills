---
name: miniapp-official-scaffold-alignment
description: Validate or design a WeChat Mini Program scaffold, repository layout, or TypeScript setup against official platform rules. Use when Codex needs to review `project.config.json`, `app.json`, `miniprogramRoot`, page or component file sets, or the initial repo skeleton before feature work begins.
---

# Miniapp Official Scaffold Alignment

## Overview

Use this skill when scaffold correctness is the blocker. Validate the repository shape before changing pages, components, or build settings.

## Quick Start

1. Read `references/official-scaffold-baseline.md`.
2. Identify the repository root and the miniapp code root.
3. Check `project.config.json`, `app.json`, page paths, component file sets, and TypeScript assumptions.
4. Report what is already valid, what is incomplete or risky, and the smallest next scaffold decision.

## Core Rules

- Use only official WeChat documentation for normative claims.
- Prefer the smallest runnable scaffold that matches the project shape.
- Distinguish repository root from miniapp code root.
- If the repo authors in TypeScript, make the compiler-plugin path explicit.
- Require matching path-and-name file quartets for pages and components.
- Write "not yet specified" instead of inventing missing spec details.

## Review Checklist

- Does `project.config.json` point at the intended miniapp code root?
- Does `app.json.pages` match real page folders?
- Does every page have matching logic, structure, style, and config files?
- Do custom components declare `component: true` and have matching file sets?
- Is TypeScript support explicit rather than implied?
- Does the repo layout leave room for sibling folders such as `docs/`, backend code, or tooling?

## Output Format

When answering, keep the result short and action-oriented:

1. officially valid parts
2. missing or risky parts
3. recommended scaffold decision
4. first edit to make

## Resources

- `references/official-scaffold-baseline.md`: official rule summary and practical implications
- `references/example-prompts.md`: reusable trigger examples and evaluation notes
