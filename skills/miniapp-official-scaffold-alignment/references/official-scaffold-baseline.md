# Official Scaffold Baseline

## Purpose

Use this file as the baseline when checking a WeChat Mini Program scaffold against official documentation.

## Official Source Areas

- directory structure
- global and page config
- code composition
- custom components
- TypeScript support
- project config

## Baseline Rules

### 1. App Root Files

- the miniapp code root contains the app entry files
- the app uses `app.js`, `app.json`, and optional `app.wxss`
- a TypeScript project can author `app.ts`, but that still depends on the DevTools compiler path

### 2. Page File Set

- each page uses matching path-and-name files
- the usual authoring set is logic, structure, style, and optional page config
- `app.json.pages` must list the page paths that actually exist

### 3. Component File Set

- a reusable component uses matching files for logic, structure, style, and config
- the component config must set `"component": true`
- components are registered through `usingComponents`

### 4. Project Config Responsibilities

- `project.config.json` stores DevTools project settings
- `miniprogramRoot` chooses the miniapp code root relative to the repository root
- this matters when the repository root also contains docs, tools, or backend code

### 5. TypeScript Constraint

- TypeScript is an authoring convenience, not the underlying package format
- if a project authors in `.ts`, the compiler-plugin path must be explicit
- same-name `.ts` and `.js` files need careful handling to avoid ambiguity

## Practical Implications

- a spec that mentions `app.ts` but not TypeScript setup is incomplete
- a spec that lists page folders without the matching file set is incomplete
- a repo with sibling folders often needs repo-root DevTools config plus a dedicated miniapp code root
