# Example Prompts

Use these prompts to validate whether the skill is triggered only after CLI evidence stops being enough.

## Prompt 1

**User prompt**

```text
`preview` 已经通过了，但首页进来还是偶发白屏。请你用微信开发者工具自动化做一个最小 GUI smoke check，只看首页有没有正常进入、有没有报运行时异常。
```

**Expected answer structure**

1. which route or flow was checked
2. whether automation really connected to DevTools
3. what runtime evidence was collected from the report
4. whether the failure belongs to repo code, DevTools session state, a local service dependency, or still needs manual visual confirmation
5. the next command or user action

**Evaluation notes**

- The answer should start with one route, not a whole-app sweep.
- Runtime exceptions, page path, selectors, and report fields should outrank screenshot commentary.
- The answer should separate host/session failure from repo failure.

## Prompt 2

**User prompt**

```text
我想把 `tools/wechat-gui-check` 跑在一个外部小程序项目上，先不要真启动 DevTools，先帮我做 dry-run 预检，确认 route config、project root 和 automator 依赖是不是都准备好了。
```

**Expected answer structure**

1. which project root and routes were validated
2. whether dry-run succeeded and what it proved
3. whether DevTools CLI and `miniprogram-automator` were discoverable
4. any blocker that prevents a later live automation run
5. the next command to move from dry-run to live-run

**Evaluation notes**

- The answer should describe `--dry-run` as preflight only, not as runtime proof.
- Missing automator should be classified as an environment/setup issue.
- The answer should stay config-driven and explicit about the selected route keys.

## Do Not Use This Skill When

```text
我还没确定这个仓库的 `miniprogramRoot`、`app.json.pages` 和页面文件集是不是官方合法，先帮我做脚手架体检。
```

Use `miniapp-official-scaffold-alignment` instead, because the blocker is scaffold validity rather than GUI-only runtime evidence.
