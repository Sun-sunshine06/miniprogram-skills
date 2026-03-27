# GUI Check Forward Test

This document records the first external forward-test for `tools/wechat-gui-check` on a public miniapp repository outside this repository.

## Host Environment

- Date: 2026-03-25
- OS: Microsoft Windows 11 Home China, `10.0.26200`
- Node.js: `v24.11.0`
- WeChat DevTools CLI path: `D:\微信web开发者工具\cli.bat`
- WeChat DevTools app version: `1.03.0`
- `miniprogram-automator`: `0.5.9`

## Repo Screening Notes

### Attempt 1 - `wechat-miniprogram/miniprogram-demo`

Repo:

- https://github.com/wechat-miniprogram/miniprogram-demo

What worked:

- the repo cloned cleanly
- `project.config.json` resolved a valid `miniprogramRoot`
- `wechat-gui-check --dry-run` successfully recognized the project root and route selection

What blocked live automation:

- `cli auto` failed with `登录用户不是该小程序的开发者`
- this was an AppID/account-authorization blocker from the host environment, not a repo runtime error

Why the run was not used as the primary evidence:

- the current logged-in DevTools account is not an authorized developer for the upstream real AppID
- that makes the exact upstream checkout unsuitable as the first generally reproducible public forward-test on this host

### Selected Forward-Test Target - `ecomfe/echarts-for-weixin`

Repo:

- https://github.com/ecomfe/echarts-for-weixin

Why this repo was selected:

- the root scaffold is simple and public
- the default home page is lightweight and does not depend on a private backend
- the route surface is small enough for a narrow GUI smoke route

## Local Test Preparation

The public repo was cloned into a disposable local copy:

- `D:\openproject\miniprogram_skills\.tmp\forward-test-echarts-for-weixin`

To avoid the same AppID authorization blocker as the first candidate, the disposable local copy changed only this field before the live run:

- `project.config.json.appid`: changed from the upstream real AppID to `touristappid`

This override was test-only host preparation for DevTools automation and was not treated as shared repo truth.

The live run used an explicit automator install path because this tool supports user-supplied runtime installs:

- `D:\openproject\miniprogram_skills\.tmp\forward-test-miniprogram-demo\node_modules`

Temporary route config used for the run:

```json
{
  "projectPath": "<project-root>",
  "outputRoot": "<project-root>/.tmp/gui-check",
  "routes": [
    {
      "key": "charts-home",
      "route": "/pages/index/index",
      "expectedPath": "pages/index/index",
      "primarySelector": ".panel",
      "settleMs": 2200,
      "dataFields": [
        "charts.0.id",
        "charts.0.name",
        "chartsWithoutImg.0.id"
      ],
      "actions": [
        {
          "type": "wait",
          "waitMs": 800,
          "required": false
        }
      ]
    }
  ]
}
```

## Dry-Run Result

Command:

```powershell
node tools/wechat-gui-check/check.js --config .tmp/forward-test-echarts-for-weixin.route-config.json --project-path .tmp/forward-test-echarts-for-weixin --route charts-home --dry-run --automator-module-path .tmp/forward-test-miniprogram-demo/node_modules
```

Observed result:

- `ok: true`
- `mode: dry-run`
- `readyForAutomation: true`
- `project.projectConfigPath` resolved correctly
- `project.miniprogramRoot` resolved to `.`
- selected route `charts-home` matched the intended homepage route

## Live-Run Result

Command:

```powershell
node tools/wechat-gui-check/check.js --config .tmp/forward-test-echarts-for-weixin.route-config.json --project-path .tmp/forward-test-echarts-for-weixin --route charts-home --automator-module-path .tmp/forward-test-miniprogram-demo/node_modules --port 9422
```

Observed behavior:

- route key `charts-home` finished with `ok: true`
- final path was `pages/index/index`
- primary selector `.panel` existed
- selected page data captured:
  - `charts.0.id = bar`
  - `charts.0.name = 柱状图`
  - `chartsWithoutImg.0.id = lazyLoad`
- no console events were recorded
- no exception events were recorded

Artifact:

- `D:\openproject\miniprogram_skills\.tmp\forward-test-echarts-for-weixin\.tmp\gui-check\2026-03-25T07-41-28-011Z\report.json`

## Report Summary

From the generated `report.json`:

- `summary.total = 1`
- `summary.passed = 1`
- `summary.failed = 0`
- `summary.warningPages = 1`
- `summary.failureClassCounts = {}`
- `summary.warningClassCounts.screenshot_capability_missing = 1`

The only warning was:

- `screenshot unavailable: miniProgram.screenshot is not a function`

## What This Validates

- `wechat-gui-check` can validate a public miniapp repo outside the bundled fixture
- the project-root and route-spec model generalized to a second repository shape
- route path, selector existence, page data capture, and report generation all worked on the external repo

## Blockers And Follow-Up

- Real AppIDs on public repos may still block `cli auto` when the current DevTools account is not an authorized developer. That should be classified as a host/account blocker, not a repo-runtime failure.
- Screenshot support depends on the runtime `miniprogram-automator` build. In this run, route verification succeeded but screenshot capture was unavailable because the installed automator did not expose `miniProgram.screenshot`.
- Treat this warning as `screenshot_capability_missing` rather than a DevTools session failure; the route/path/selector evidence remains the primary result.
- This is the first external public-repo forward-test, not the final confidence bar. A second public repo with a different scaffold shape would strengthen `v0.3`.

## Next Evidence Point

The next forward-test should preferably run on a collaborator host rather than the original maintainer machine so the repository collects cross-machine evidence instead of only more same-host confirmation.

Use `docs/gui-check-collaborator-forward-test.md` as the handoff runbook for that second sample.
