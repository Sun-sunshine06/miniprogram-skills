# DevTools GUI Check Playbook

## Why This Exists

CLI `preview` and GUI smoke checks solve different problems.

CLI is good for:

- syntax or compile failures
- page path drift
- project config drift
- upload-path diagnostics

GUI automation is needed for:

- errors that appear only after a page opens
- errors that appear only after a real tap
- state drift that does not break `preview`
- smoke-level blank-page suspicion

## Host Prerequisites

Run this flow only when all of these are true:

- the command runs on the real host
- WeChat DevTools is installed and logged in
- no blocking IDE dialog is still open
- the repo has a known project root and route targets

If automation keeps failing after a previous manual session, fully quit DevTools and rerun.

## Command Ladder

### Step 1: Start Narrow

Run one route first:

```powershell
cd tools/wechat-gui-check
npm run check -- --route home
```

### Step 2: Expand Only After One Route Is Stable

Use multiple routes only after a single route can connect and report consistently.

### Step 3: Read The Report Before Claiming Success

Inspect:

```text
.tmp/gui-check/<timestamp>/report.json
```

Focus on:

- `ok`
- `failures`
- `warnings`
- route path
- selector presence
- action result
- console events
- exception events

If `report.json` is missing but the run directory exists, inspect:

```text
.tmp/gui-check/<timestamp>/trace.log
```

Use the last recorded stage to decide whether the blocker is:

- DevTools launcher startup
- websocket connection
- app runtime readiness
- route-level action or selector failure

## Failure Classification

### Automation Does Not Connect

Typical meaning:

- DevTools reused an old session
- a blocking dialog is still open
- the websocket endpoint never became available
- the launcher never exited cleanly and the harness had to continue in background mode

Action:

1. clear dialogs
2. fully quit DevTools
3. rerun the same narrow check

If `trace.log` never gets past launcher or websocket stages, keep the diagnosis on host or session state first.

### Runtime Exceptions Or Severe Console Errors Appear

Typical meaning:

- the page loads but throws after initialization
- a real interaction triggers bad state or a bad handler

Action:

1. inspect the route-specific action
2. inspect page data and report fields
3. patch the repo
4. rerun the same route

### Page Shows `request:fail` Or Localhost Refusal

Typical meaning:

- the route opened correctly
- compile succeeded
- a local backend or service dependency is unavailable

Action:

1. keep the GUI report as runtime evidence
2. do not misclassify it as a DevTools launcher problem
3. verify the local service or runtime dependency outside the GUI harness

### Action Is Skipped Because A Selector Is Missing

Typical meaning:

- the UI changed
- the page opened in an unexpected state
- the smoke harness is stale

Action:

1. confirm the expected selector
2. decide whether the checker or the app regressed
3. rerun after patching the correct side

## Success Criteria

Claim a route check is successful only when all of these are true:

1. automation connected
2. the current page path matches the expected page
3. the primary selector exists
4. no new runtime exceptions were recorded
5. the route-specific action either succeeded or was intentionally absent
6. report output was written
