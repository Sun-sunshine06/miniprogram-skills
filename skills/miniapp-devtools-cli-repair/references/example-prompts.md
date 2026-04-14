# Example Prompts

Use these prompts to validate whether the skill is triggered at the right time and whether the response stays operational.

## Prompt 1

**User prompt**

```text
微信开发者工具里预览一直失败，但我只有命令行和这个小程序仓库。请你优先用 DevTools CLI 看看 `preview` 到底报了什么，能修就直接修，不能修就告诉我还缺什么证据。
```

**Expected answer structure**

1. what CLI command was used and what it exposed
2. whether the failure is repository-scoped and safe to auto-fix
3. what changed in the repo or what further evidence is still needed
4. the exact next command or remaining evidence needed

**Evaluation notes**

- The answer should prefer the official DevTools CLI over guessing from symptoms.
- The answer should classify whether the problem is CLI-visible, safe to patch, or still GUI-only.
- The answer should not claim runtime-page validation if only `preview` evidence exists.

## Prompt 2

**User prompt**

```text
我已经能打开微信开发者工具，但不知道当前 live port 是多少，也不确定是不是会话脏了。请你用官方 CLI 重新建立连接，再判断这个仓库是不是因为 `project.config.json` 或页面路径问题导致无法 preview。
```

**Expected answer structure**

1. how IDE connectivity and the live port were established
2. the preview result and the exact file or config area involved
3. whether a narrow repo fix was applied or why the issue falls outside preview scope
4. the rerun command that proves the fix or the limit of CLI evidence

**Evaluation notes**

- The answer should use `open` before `preview` when the live port is unknown.
- Safe fixes should stay local to repo structure or config files.
- If the CLI path is exhausted, the answer should explicitly ask for GUI evidence instead of inventing conclusions.

## Do Not Use This Skill When

```text
我已经能正常 `preview`，但是页面点按钮后才白屏，想知道是不是运行时状态或者某个点击事件炸了。
```

Use `miniapp-devtools-gui-check` instead, because this is a GUI/runtime question rather than a CLI-visible compile or preview problem.
