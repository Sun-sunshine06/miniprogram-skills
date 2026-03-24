# Example Prompts

Use these prompts to validate whether the skill is used before feature work when scaffold correctness is the blocker.

## Prompt 1

**User prompt**

```text
我准备新建一个微信小程序仓库，根目录里还会放 `docs/` 和一些脚本。请你按官方规则帮我设计一个最小可运行的目录结构，并说明 `project.config.json` 里的 `miniprogramRoot` 应该怎么定。
```

**Expected answer structure**

1. which parts of the proposed scaffold are already officially valid
2. which parts are still missing or risky
3. the recommended scaffold decision, especially repo root versus miniapp code root
4. the first edit or file set to create

**Evaluation notes**

- The answer should distinguish repository root from miniapp code root.
- Official claims should stay within documented platform rules.
- The answer should prefer the smallest runnable scaffold instead of adding speculative folders.

## Prompt 2

**User prompt**

```text
帮我检查这个小程序目录：`app.json` 里列了两个页面，但其中一个页面只有 `.wxml` 和 `.wxss`，另一个页面是 `.ts` 写的却没看到明确的 TypeScript 配置。请你判断哪些地方已经合法，哪些地方还缺。
```

**Expected answer structure**

1. officially valid parts of the current scaffold
2. missing page or component file sets and any TypeScript ambiguity
3. the smallest scaffold decision needed to remove the ambiguity
4. the first concrete edit to make

**Evaluation notes**

- The answer should require matching file sets for pages and components.
- The answer should call out incomplete TypeScript setup rather than assuming it works.
- The answer should say "not yet specified" where the spec is incomplete.

## Do Not Use This Skill When

```text
我已经确定脚手架合法了，现在是微信开发者工具导入错目录后污染了仓库，想恢复干净。
```

Use `miniapp-devtools-recovery` instead, because the scaffold is no longer the question; the problem is cleanup and DevTools state recovery.
