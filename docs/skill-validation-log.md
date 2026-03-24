# Skill Validation Log

This log records prompt-level and host-side validation passes for public skills.

Current status:

- `miniapp-devtools-cli-repair`: one host-side validation recorded
- `miniapp-devtools-gui-check`: one host-side validation recorded
- `miniapp-devtools-recovery`: one host-side validation recorded
- `miniapp-official-scaffold-alignment`: one local scaffold validation recorded

## 2026-03-24 - `miniapp-devtools-gui-check`

**Prompt used**

```text
`preview` already succeeds, but the home page still goes blank sometimes. Run a minimal WeChat DevTools GUI smoke check and verify only whether the home page opens correctly and whether any runtime exceptions appear.
```

**Expected behavior**

- run one narrow route instead of a whole-app sweep
- connect to the real host-side WeChat DevTools automation session
- capture route path, selector, action, runtime exception, and console evidence
- separate repo/runtime results from screenshot-only limitations

**Observed behavior**

- Host environment was valid:
  - WeChat DevTools CLI existed at `D:\微信web开发者工具\cli.bat`
  - `cli.bat islogin` returned `{"login":true}`
  - `miniprogram-automator` was installed locally for execution
- Command run:

```powershell
cd tools/wechat-gui-check
npm run check -- --route home --cli-path "D:\微信web开发者工具\cli.bat"
```

- Result:
  - route `home` finished with `ok=true`
  - final path was `pages/home/index`
  - primary selector existed
  - title text was `Fixture Home`
  - tap action on `.btn-primary` succeeded
  - no console events were recorded
  - no exception events were recorded
- Artifact:
  - report saved at `tools/wechat-gui-check/examples/fixture-miniapp/.tmp/gui-check/2026-03-24T13-54-20-815Z/report.json`

**Gaps / follow-up**

- Screenshot capture still timed out after 30000ms, so screenshots remain best-effort evidence rather than a success requirement.
- During the host-side run, DevTools rewrote the fixture `project.config.json` by adding `setting.minifyWXML`; the tracked file was restored afterward, so fixture runs currently have a config-drift side effect worth guarding against.
- This validates the bundled fixture on a real host, but it does not yet satisfy the external public repo forward-test goal.

## 2026-03-24 - `miniapp-devtools-cli-repair`

**Prompt used**

```text
I can already open WeChat DevTools, but I do not know the current live port and I am not sure whether the session is stale. Re-establish connectivity through the official CLI, then determine whether this repo fails `preview` because of `project.config.json` or page-path problems.
```

**Expected behavior**

- use the official DevTools CLI as the primary evidence source
- establish IDE connectivity and a live port before diagnosing `preview`
- classify whether the failure is repo-scoped and safe to auto-fix
- avoid inventing GUI/runtime conclusions from CLI-only evidence

**Observed behavior**

- CLI availability was confirmed with `cli.bat --help`.
- IDE connectivity was re-established with:

```powershell
& "D:\微信web开发者工具\cli.bat" open --project "D:\openproject\miniprogram_skills\tools\wechat-gui-check\examples\fixture-miniapp" --port 47567
```

- `open` succeeded and confirmed the IDE HTTP server at `http://127.0.0.1:47567`.
- `preview` was then run with QR/info outputs requested:

```powershell
& "D:\微信web开发者工具\cli.bat" preview --project "D:\openproject\miniprogram_skills\tools\wechat-gui-check\examples\fixture-miniapp" --port 47567 --qr-format base64 --qr-output "D:\openproject\miniprogram_skills\.tmp\cli-preview\fixture.qr.txt" --info-output "D:\openproject\miniprogram_skills\.tmp\cli-preview\fixture.info.json"
```

- `preview` failed with code `10` and the message `AppID 不合法,invalid appid`.
- The failure was not a page-path or scaffold-shape error. It was classified as a preview credential/AppID limitation of the fixture project, so no repo auto-fix was applied.

**Gaps / follow-up**

- This validates that the CLI repair flow can recover the live port and surface a real preview failure on host.
- A future pass should use a public repo or fixture with a preview-acceptable AppID so the success path is also recorded.

## 2026-03-24 - `miniapp-devtools-recovery`

**Prompt used**

```text
After WeChat DevTools ran, it modified `project.config.json` in this copied miniapp. Follow the recovery workflow, decide whether that change belongs in shared repo state, restore the project to its intended shape, and explain what to watch for in DevTools next time.
```

**Expected behavior**

- detect that the changed file is shared project config rather than disposable local state
- describe the intended repo shape and keep cleanup minimal
- restore the tracked/shared config before deleting anything else
- tell the user what belongs in DevTools local state versus repo state

**Observed behavior**

- A disposable copy of the bundled fixture was created at `D:\openproject\miniprogram_skills\.tmp\recovery-fixture-copy-20260324`.
- Host-side GUI automation was run against that copy:

```powershell
cd tools/wechat-gui-check
npm run check -- --config examples/sample.route-config.json --project-path "D:\openproject\miniprogram_skills\.tmp\recovery-fixture-copy-20260324" --route home --cli-path "D:\微信web开发者工具\cli.bat" --automator-module-path "D:\openproject\miniprogram_skills\tools\wechat-gui-check\node_modules"
```

- The live run succeeded and produced a screenshot plus a report, but DevTools rewrote `project.config.json` by adding `setting.minifyWXML`.
- The recovery decision was:
  - keep the copied repo root and page files
  - treat the added `minifyWXML` field as host-side config drift, not shared repo truth
  - restore `project.config.json` from the known-good fixture source
- After restoration, `git diff --no-index` between the source fixture config and the copied config returned no diff.

**Gaps / follow-up**

- This validates the "restore shared config first" part of the recovery flow on a real host-side side effect.
- A future recovery pass should also exercise wrong-root import residue or stale compile-condition drift, not only config rewrite drift.

## 2026-03-24 - `miniapp-official-scaffold-alignment`

**Prompt used**

```text
Review this fixture project against official WeChat Mini Program scaffold rules. Verify that `project.config.json.miniprogramRoot`, `app.json.pages`, and the page file sets are consistent, and call out anything incomplete.
```

**Expected behavior**

- identify the repository root and the miniapp code root
- verify that `app.json.pages` maps to real page folders
- verify that each listed page has matching logic, structure, style, and config files
- call out missing TypeScript or component details only when they are actually ambiguous

**Observed behavior**

- The fixture project root inspected was `tools/wechat-gui-check/examples/fixture-miniapp`.
- `project.config.json` was valid for a repo-root miniapp:
  - `compileType` was `miniprogram`
  - `miniprogramRoot` was `.`
- `app.json.pages` listed:
  - `pages/home/index`
  - `pages/tasks/index`
- Both listed pages existed on disk and each had the full file quartet:
  - `.js`
  - `.json`
  - `.wxml`
  - `.wxss`
- No TypeScript ambiguity was present because the fixture authors in JavaScript.
- No custom component mismatch was found because the fixture does not define reusable component folders in this sample.

**Gaps / follow-up**

- This validates the skill on a clean, minimal scaffold that passes the core checks.
- A future pass should include a deliberately incomplete scaffold sample so the "missing or risky parts" branch is also exercised.
