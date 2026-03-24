# Example Prompts

Use these prompts to validate whether the skill focuses on repository cleanup after DevTools drift.

## Prompt 1

**User prompt**

```text
我把一个已有小程序仓库错误地当成新项目导入到微信开发者工具里了，现在仓库里多出了模板页、额外的配置文件，而且启动页也不对。请你帮我判断哪些该删、哪些该还原，并告诉我 DevTools 里要怎么重新导入。
```

**Expected answer structure**

1. what DevTools likely changed in the repo
2. what should remain as the intended tracked project shape
3. what to restore first and what generated residue to delete
4. what the user must change in DevTools after cleanup

**Evaluation notes**

- The answer should restore tracked files before deleting generated clutter.
- The answer should distinguish repository root from miniapp code root.
- The answer should tell the user the correct import behavior inside DevTools.

## Prompt 2

**User prompt**

```text
这个仓库明明是 TypeScript 小程序，但 DevTools 一直提示缺少某个页面的 `.js` 文件。我怀疑是导入方式或者编译模式漂移了，请你按恢复流程排查，不要直接把项目改回 JavaScript。
```

**Expected answer structure**

1. the most likely recovery class, such as wrong-root import or TypeScript-recognition drift
2. which repo files and DevTools settings should be inspected first
3. what to restore, delete, or leave untouched
4. the exact DevTools-side correction the user should make

**Evaluation notes**

- The answer should check TypeScript recognition before rewriting source files.
- The answer should treat `project.private.config.json` as local state, not shared truth.
- The answer should keep cleanup minimal and explain why each deletion is safe.

## Do Not Use This Skill When

```text
我想确认一个全新仓库的页面结构、组件文件集和 `project.config.json` 设计是不是符合微信官方规则。
```

Use `miniapp-official-scaffold-alignment` instead, because this is a scaffold design/validation task rather than a recovery task after DevTools pollution.
