# GUI Check Collaborator Forward Test

Use this runbook when the next `tools/wechat-gui-check` public-repo forward-test should be executed on a collaborator's machine instead of the maintainer host.

## Goal

Collect a second public-repo evidence point that helps answer two questions:

- does `wechat-gui-check` still work on a different Windows host with a different DevTools install and account state?
- if it fails, is the failure a host/account/setup issue or a repo/runtime issue?

## What The Collaborator Should Return

Please ask the collaborator to return these artifacts together:

- one host environment JSON captured with `scripts/collect_gui_check_env.ps1`
- the exact route config JSON used for the test
- the dry-run JSON output
- the final `report.json` from the live run, if any
- a short note describing whether the target repo was used as-is or from a disposable local copy
- a short note describing any temporary AppID override or host-side workaround

## Recommended Candidate Repo

Prefer a public miniapp repo that:

- has a simple homepage route
- does not need private backend state to render the first screen
- can be validated with one narrow route and zero or one non-required action
- is different in scaffold shape from the first recorded public-repo pass

If the repo uses a real upstream AppID and `cli auto` blocks with a developer-authorization error, switch to a disposable local copy and document the test-only AppID override.

## Step 1 - Clone A Disposable Copy

Ask the collaborator to clone the public repo into a disposable local directory outside this repository.

Example:

```powershell
git clone --depth 1 <public-repo-url> D:\tmp\miniapp-forward-test-2
```

If they expect to edit `project.config.json.appid`, do it only in that disposable copy.

## Step 2 - Capture Host Environment

From this repository root, run:

```powershell
pwsh -File scripts/collect_gui_check_env.ps1 -OutputPath .tmp/gui-check-host-env-collaborator.json
powershell.exe -File scripts/collect_gui_check_env.ps1 -OutputPath .tmp/gui-check-host-env-collaborator.json
```

If the live run will use a shared automator install, include it:

```powershell
pwsh -File scripts/collect_gui_check_env.ps1 -OutputPath .tmp/gui-check-host-env-collaborator.json -AutomatorModulePath <path-to-node_modules> -ProjectPath <target-project-root>
powershell.exe -File scripts/collect_gui_check_env.ps1 -OutputPath .tmp/gui-check-host-env-collaborator.json -AutomatorModulePath <path-to-node_modules> -ProjectPath <target-project-root>
```

## Step 3 - Create A Narrow Route Config

Use one narrow route first. A good starting template is:

```json
{
  "projectPath": "<project-root>",
  "outputRoot": "<project-root>/.tmp/gui-check",
  "routes": [
    {
      "key": "home",
      "route": "/pages/index/index",
      "expectedPath": "pages/index/index",
      "primarySelector": ".page",
      "settleMs": 2200,
      "dataFields": [
        "loading",
        "errorMessage"
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

Adjust only what is needed for the target repo:

- `route`
- `expectedPath`
- `primarySelector`
- `dataFields`
- optional narrow action

## Step 4 - Run Dry-Run First

From this repository root:

```powershell
node tools/wechat-gui-check/check.js --config <route-config-path> --project-path <target-project-root> --route <route-key> --dry-run --automator-module-path <path-to-node_modules> > .tmp/gui-check-preflight-collaborator.json
```

Record whether:

- `ok` is `true`
- `readyForAutomation` is `true`
- `project.projectConfigPath` and `project.miniprogramRoot` look correct

If dry-run already fails, stop there and return the dry-run JSON plus a short note.

## Step 5 - Run Live Automation

If dry-run is ready, run:

```powershell
node tools/wechat-gui-check/check.js --config <route-config-path> --project-path <target-project-root> --route <route-key> --automator-module-path <path-to-node_modules> --port 9420
```

Use a different port if `9420` is already occupied on that machine.

## Step 6 - Return The Artifacts

Please collect and send back:

- `.tmp/gui-check-host-env-collaborator.json`
- `.tmp/gui-check-preflight-collaborator.json`
- `<route-config-path>`
- `<target-project-root>/.tmp/gui-check/<timestamp>/report.json`
- any screenshots generated in the same run directory

## How To Classify Common Outcomes

- `登录用户不是该小程序的开发者`: host/account/AppID blocker, not a repo runtime regression
- `Unable to load miniprogram-automator`: host dependency/setup blocker
- `projectPath must point to ... project.config.json`: wrong project root
- `failureCodes` include `selector_assertion_error`: likely route config mismatch or real UI drift
- `failureCodes` include `repo_runtime_error`: likely repo behavior/runtime issue
- `warningClassCounts` include only `screenshot_capability_missing` or `screenshot_timeout`: treat the route/path/selector evidence as primary and screenshot as best-effort

## Minimum Notes To Include In The Write-Up

Please include these facts even if the run fails:

- public repo URL
- whether the run used the upstream repo directly or a disposable local copy
- whether `project.config.json.appid` was changed for the test
- whether dry-run passed
- whether live-run passed
- the top-level `classification` or `summary.failureClassCounts` / `summary.warningClassCounts`

## Repository Follow-Up

Once the collaborator returns the artifacts:

1. summarize the result in `docs/gui-check-forward-test.md`
2. compare it against the first public-repo evidence point
3. decide whether the result strengthens cross-machine confidence or exposes a host-specific blocker worth documenting
