# Skill Validation Log

This log records prompt-level and host-side validation passes for public skills.

Current status:

- `miniapp-devtools-cli-repair`: two host-side validations recorded, plus one external public-repo auth/session blocker sample
- `miniapp-devtools-gui-check`: one host-side validation recorded, plus one session-blocker failure-shape sample
- `miniapp-devtools-recovery`: one host-side validation recorded, plus one wrong-root residue fixture review and one external public-repo-derived recovery sample
- `miniapp-official-scaffold-alignment`: one local scaffold validation recorded, plus one deliberately broken scaffold fixture review and one external public-repo scaffold review
- `miniapp-center-hub-refactor`: one routing-backed draft extraction review recorded
- `miniapp-review-queue-actions`: one routing-backed draft extraction review recorded
- `miniapp-user-facing-copy-trim`: one routing-backed draft extraction review recorded

## 2026-04-14 - `miniapp-center-hub-refactor` routing-backed draft extraction

**Prompt used**

```text
This miniapp started with `home / tasks / profile`, but now pending work, integrations, and settings are scattered across too many tabs. Refactor the top-level information architecture into a clearer center without turning everything into one long page.
```

**Expected behavior**

- recognize an information-architecture problem instead of a copy-only or queue-card problem
- propose a hub structure that separates pending-work flow from lower-frequency settings
- keep detailed pages when they still own meaningful form or state flow

**Observed behavior**

- The extracted skill stays on top-level navigation ownership and does not drift into card-level button design.
- The output contract is operational:
  - current navigation problem
  - proposed hub structure
  - page ownership and migration map
  - migration order
- No source-repo route names, storage keys, or absolute paths were kept in the public skill body or references.

**Gaps / follow-up**

- This is routing-backed draft evidence, not yet a cross-repo forward-test.
- A future pass should validate the same workflow on a second miniapp repository with a different tab shape.

## 2026-04-14 - `miniapp-review-queue-actions` routing-backed draft extraction

**Prompt used**

```text
This pending queue makes users open a detail page for every item just to approve, ignore, or import it. Redesign the queue cards so common actions happen in place and refresh safely afterward.
```

**Expected behavior**

- keep the work on queue states, inline actions, and refresh chains
- preserve detail-page navigation as a secondary path instead of the only path
- expose a reusable mutation-and-reload sequence

**Observed behavior**

- The extracted skill stays on actionable queue design and does not widen into a full navigation rewrite.
- The public contract stays reusable across approval, import, and review queues rather than one product's exact data model.
- The references keep the state matrix, card contract, and side-effect chain separate from any app-specific terminology.

**Gaps / follow-up**

- This is routing-backed draft evidence, not yet a second-repo implementation sample.
- A future pass should validate the pattern on a queue that is not task-import specific.

## 2026-04-14 - `miniapp-user-facing-copy-trim` routing-backed draft extraction

**Prompt used**

```text
The miniapp pages read like internal documentation. Trim the on-page text, keep only action-first labels and short status summaries, and move implementation-heavy explanation out of the main surfaces.
```

**Expected behavior**

- keep the task on wording and surface density rather than broader architecture change
- separate what stays on-page from what should move to help or detail surfaces
- keep bilingual guidance reusable instead of repo-bound

**Observed behavior**

- The extracted skill stays on copy trimming and does not pretend to solve deeper navigation drift by itself.
- The output contract remains operational:
  - high-friction copy to cut
  - replacement labels and summaries
  - what to move out of the page
  - copy validation pass
- The public references keep proper nouns and bilingual usage as generic guidance instead of one app's vocabulary list.

**Gaps / follow-up**

- This is routing-backed draft evidence, not yet a cross-repo forward-test.
- A future pass should validate the skill on a second miniapp with more bilingual or integration-heavy copy.

## 2026-04-13 - `miniapp-devtools-cli-repair` external public-repo auth/session blocker

**Prompt used**

```text
Use the official WeChat DevTools CLI on this public miniapp repo, re-establish the live IDE port if needed, and determine whether any failure is a repo-scoped preview problem or a host/session blocker that should not trigger repo edits.
```

**Expected behavior**

- treat the official CLI as the primary evidence source
- recover or reuse the live IDE port before classifying `preview`
- distinguish repo-local preview failures from AppID, login, or DevTools session blockers
- avoid inventing repo fixes when the CLI failure is clearly host-side

**Observed behavior**

- The public repo cloned was `https://github.com/ecomfe/echarts-for-weixin` into `.tmp/external-echarts-for-weixin`.
- Initial CLI state on this host was inconsistent:
  - one `cli.bat islogin` pass returned `{"login":true}` and exposed an IDE server on `http://127.0.0.1:30590`
  - asking `open` or `preview` to use a new port returned `IDE server has started on http://127.0.0.1:30590 and must be restarted on port 47611 first`
- Retrying `open` and `preview` against the live port `30590` then returned `需要重新登录 (code 10)` instead of a repo-local compile or page-path error.
- A later captured retry under `.tmp/external-cli-echarts/` showed the instability more clearly:
  - `islogin.txt` ended with `{"login":false}`
  - `open.txt` and `preview.txt` both ended with `#initialize-error: wait IDE port timeout`
  - no QR or info output files were produced
- The observed failure was therefore classified as a host/session authentication problem on the external repo, not a repo-scoped auto-fix candidate.

**Gaps / follow-up**

- This records a real external public-repo CLI blocker, but it is still a failure-path sample rather than a success-path preview run.
- A future pass should add one public repo where `open` and `preview` succeed cleanly so the success branch is documented too.

**Post-login retest on 2026-04-13**

- After a fresh `cli.bat login` scan, `cli.bat islogin` returned `{"login":true}` on port `40318`, so the host-side login/session blocker was cleared.
- Retesting the upstream repo still failed for the expected reason:
  - `open` / `preview` on the unmodified upstream checkout returned `登录用户不是该小程序的开发者`
- Retesting a disposable public-repo copy with a test-only AppID override narrowed the remaining blocker further:
  - the copy was `D:\openproject\skills\miniprogram_skills\.tmp\external-echarts-for-weixin-previewable`
  - `project.config.json.appid` was changed from the upstream real AppID to `touristappid`
  - `open` then succeeded on port `40318`
  - `preview` still failed with `AppID 不合法, invalid appid`
- This means the remaining gap is no longer basic CLI connectivity or login. The missing ingredient for a true success-path public-repo preview sample is a preview-acceptable testing AppID controlled by the current account, not another repo-local fix.

## 2026-04-13 - `miniapp-devtools-cli-repair` local host-side preview success

**Prompt used**

```text
Use the official WeChat DevTools CLI on a project owned by the current logged-in account, recover or reuse the live IDE port, and confirm the full `open` + `preview` success path with output artifacts.
```

**Expected behavior**

- reuse a live CLI port instead of forcing a new one when the IDE is already serving
- prove that `open` succeeds before claiming preview success
- prove preview success with both CLI output and generated artifacts
- keep the result narrowly on CLI-visible evidence instead of GUI/runtime claims

**Observed behavior**

- A locally available project from the DevTools project list was selected:
  - `D:\微信web开发者工具\MpWechatProject\miniprogram-1`
  - `project.config.json.appid = wx4b466a75420cb9ab`
- `cli.bat islogin` had already returned `{"login":true}` and the IDE HTTP server was live on `http://127.0.0.1:40318`.
- Running:

```powershell
& "D:\微信web开发者工具\cli.bat" open --project "D:\微信web开发者工具\MpWechatProject\miniprogram-1" --port 40318
& "D:\微信web开发者工具\cli.bat" preview --project "D:\微信web开发者工具\MpWechatProject\miniprogram-1" --port 40318 --qr-format base64 --qr-output "D:\openproject\skills\miniprogram_skills\.tmp\local-cli-success\miniprogram-1.qr.txt" --info-output "D:\openproject\skills\miniprogram_skills\.tmp\local-cli-success\miniprogram-1.info.json"
```

- produced:
  - `open` success
  - `preview` success
  - one QR output artifact at `.tmp/local-cli-success/miniprogram-1.qr.txt`
  - one info artifact at `.tmp/local-cli-success/miniprogram-1.info.json`
- The info artifact recorded a successful package summary:
  - `size.total = 4661`
  - one package entry with name `TOTAL`

**Gaps / follow-up**

- This proves the CLI repair success path on a real host-owned project, but it is not a public-repo sample.
- The remaining evidence gap for this skill is now specifically a public-repo success-path preview sample with a preview-acceptable testing AppID.

## 2026-04-13 - `miniapp-devtools-gui-check` session blocker sample

**Prompt used**

```text
CLI `preview` is already green, but the GUI checker never gets a ready DevTools session and exits before the route can open. Classify whether this is repo runtime, host setup, or DevTools session state, and tell me what evidence is still missing.
```

**Expected behavior**

- do not pretend that a route-level runtime result was collected when automation never became ready
- classify the failure as a DevTools session or environment blocker rather than a repo runtime regression
- keep the answer operational and tell the user what host-side evidence is still needed

**Observed behavior**

- Reviewed the committed failure sample at `tools/wechat-gui-check/examples/sample.session-error.json`.
- The sample records:
  - `ok: false`
  - `classification: devtools_session_error`
  - `error: cli auto exited because DevTools did not become ready before timeout`
- This is the intended negative-path shape for a session blocker:
  - automation did not connect cleanly
  - no route/path/selector/runtime conclusion should be claimed yet
  - the next step should stay on host/session recovery rather than repo-runtime blame

**Gaps / follow-up**

- This is a repo-owned failure-shape sample, not a second live host-side run.
- A future pass should capture one real host-side session blocker artifact so the same classification is proven outside the sample JSON.

## 2026-04-13 - `miniapp-devtools-recovery` external public-repo-derived sample

**Prompt used**

```text
This public miniapp repo was copied into a disposable local directory and then polluted with a generated page plus a stale local compile condition. Follow the recovery workflow, remove only the residue, and prove the repo returns to its intended shape.
```

**Expected behavior**

- keep the upstream public repo shape as the source of truth
- identify the generated residue as local-only pollution rather than shared repo state
- remove the stale compile condition and generated page with minimal cleanup
- confirm the disposable copy matches the original public repo again after recovery

**Observed behavior**

- The upstream public repo used was `https://github.com/ecomfe/echarts-for-weixin`, cloned into `.tmp/external-echarts-for-weixin`.
- A disposable copy was created at `.tmp/external-echarts-for-weixin-recovery`.
- The disposable copy was intentionally polluted with:
  - `pages/generated/index.{js,json,wxml,wxss}`
  - `project.private.config.json` containing a stale compile condition for `pages/generated/index`
- Before cleanup, `git diff --no-index --stat` between the upstream clone and the disposable copy showed exactly those 5 residue files.
- Recovery then removed only:
  - `project.private.config.json`
  - `pages/generated/`
- After cleanup, `git diff --no-index --exit-code .tmp/external-echarts-for-weixin .tmp/external-echarts-for-weixin-recovery` returned success, confirming the disposable copy matched the public-repo source again.

**Gaps / follow-up**

- This is a public-repo-derived disposable-copy sample, not a live DevTools-side mutation captured from a real import mistake.
- A future pass should add one host-created wrong-root or compile-condition drift artifact on a second repo shape.

## 2026-04-13 - `miniapp-devtools-recovery` wrong-root residue fixture

**Prompt used**

```text
After importing this repo the wrong way, DevTools left root-level template pages behind and the local compile target now points at the wrong start page. Restore the intended repo shape, keep only the real miniapp root, and tell me what to clear in DevTools.
```

**Expected behavior**

- detect that the intended miniapp root lives under a subfolder instead of the repo root
- keep the real shared miniapp tree
- remove generated wrong-root residue and stale compile-condition drift
- tell the user what belongs in local DevTools state rather than shared repo state

**Observed behavior**

- Reviewed the committed fixture at `evals/negative-fixtures/recovery-wrong-root-residue`.
- The fixture intentionally shows:
  - `project.config.json.miniprogramRoot = "miniprogram"`
  - the intended app under `miniprogram/pages/home/index`
  - a root-level `pages/index/` quartet that acts as wrong-root residue
  - `project.private.config.json` carrying a stale compile condition for `pages/index/index`
- This exercises the recovery branch that should keep the `miniprogram/` tree, delete the root residue, and clear the stale local compile condition.

**Gaps / follow-up**

- This is a repo-owned negative fixture, not a live DevTools mutation captured on a second repo shape.
- A future pass should add one host-side residue example beyond config rewrite drift.

## 2026-04-13 - `miniapp-official-scaffold-alignment` broken scaffold fixture

**Prompt used**

```text
Review this planned miniapp scaffold before import. Tell me what is officially valid, what is incomplete, and what the first corrective edit should be if one page listed in `app.json` is missing part of its required file quartet.
```

**Expected behavior**

- identify the repository root and the miniapp code root
- verify that `app.json.pages` maps to real page folders
- catch the missing file-quartet member instead of calling the scaffold valid
- recommend the smallest correction before feature work begins

**Observed behavior**

- Reviewed the committed fixture at `evals/negative-fixtures/scaffold-missing-page-style`.
- The fixture intentionally shows:
  - a valid repo-root `project.config.json` with `miniprogramRoot = "."`
  - `app.json.pages` listing `pages/missing/index`
  - a complete file quartet for `pages/home/index`
  - a deliberately incomplete file set for `pages/missing/index`, where `index.wxss` is absent
- This exercises the scaffold branch that should mark the scaffold as incomplete and recommend restoring the missing page file before feature work starts.

**Gaps / follow-up**

- This is a repo-owned negative fixture, not a public-repo review artifact.
- A future pass could add a TypeScript-specific negative scaffold sample so the TS/plugin branch is exercised too.

## 2026-04-13 - `miniapp-official-scaffold-alignment` external public-repo review

**Prompt used**

```text
Review this public WeChat Mini Program repo against the official scaffold rules before feature changes. Verify the effective miniapp root, the `app.json.pages` list, and whether the repo keeps complete page/component file sets.
```

**Expected behavior**

- identify the repository root and the miniapp code root
- verify that `app.json.pages` maps to real page folders
- verify that each page has matching logic, structure, style, and config files
- call out component-shape or TypeScript ambiguity only when it is actually present

**Observed behavior**

- The public repo reviewed was `https://github.com/ecomfe/echarts-for-weixin`, cloned into `.tmp/external-echarts-for-weixin`.
- `project.config.json` was valid for a repo-root miniapp:
  - `compileType` was `miniprogram`
  - `miniprogramRoot` was absent, so the effective miniapp root resolved to `.`
- `app.json.pages` listed 25 routes under `pages/**/index`.
- A scripted page-quartet check confirmed that all 25 listed pages had matching:
  - `.js`
  - `.json`
  - `.wxml`
  - `.wxss`
- The shared `ec-canvas` component folder also had the expected component quartet:
  - `ec-canvas.js`
  - `ec-canvas.json`
  - `ec-canvas.wxml`
  - `ec-canvas.wxss`
- No immediate scaffold mismatch was found for this external public repo shape.

**Gaps / follow-up**

- This is a JavaScript repo-root sample, so it does not yet exercise a nested `miniprogramRoot` or TypeScript-first scaffold.
- A future pass should add one external public repo with a non-root code folder or explicit TS tooling so those branches are covered too.

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
