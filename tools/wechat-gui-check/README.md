# WeChat GUI Check

English | [中文](./README.zh-CN.md)

Config-driven WeChat DevTools GUI smoke harness for runtime and interaction checks that do not show up in CLI `preview`.

## Current Status

Public beta extraction. The harness now ships with a bundled fixture miniapp plus two repo-owned sample configs, keeps its default repo-owned dependency surface small by loading `miniprogram-automator` only from an explicit runtime install, supports automated dry-run checks against a copied project root outside the repository, and now has one documented external forward-test on a public miniapp repo. Broader cross-repo validation is still pending. See `../../docs/gui-check-forward-test.md`.

## What It Does

- launch WeChat DevTools automation mode through the official CLI
- connect through `miniprogram-automator`
- open configured routes from JSON config
- perform a small number of taps, waits, or page-method actions
- collect runtime exceptions and console events
- emit a machine-readable `report.json`
- capture screenshots as best-effort evidence

## Files

- `check.js`: main runner
- `lib/check-helpers.js`: shared helpers
- `examples/sample.route-config.json`: example route config
- `examples/sample.rich.route-config.json`: richer fixture config with mixed action types
- `examples/sample-report.json`: example output shape
- `examples/sample.session-error.json`: example fatal session-blocker output shape

## Install

```powershell
cd tools/wechat-gui-check
npm ci
```

Install the runtime automation dependency in one of these places before running GUI checks:

```powershell
cd <project-root>
npm install --no-save miniprogram-automator
```

Or:

```powershell
cd tools/wechat-gui-check
npm install --no-save miniprogram-automator
```

## Run

Use the bundled fixture and sample config:

```powershell
cd tools/wechat-gui-check
npm run check -- --route home
```

The default run uses `examples/fixture-miniapp` as the project root and `examples/sample.route-config.json` as the route config.

Use the richer bundled sample when you want the fixture to exercise `wait`, `tap`, and `callMethod` in one route:

```powershell
cd tools/wechat-gui-check
npm run check:fixture:rich:dry-run
```

Use your own miniapp project:

```powershell
cd tools/wechat-gui-check
npm run check -- --config .\my-routes.json --project-path <project-root> --route home --route tasks
```

`<project-root>` must point to a WeChat Mini Program project root that contains `project.config.json`. The checker validates that root before it launches DevTools automation and, by default, tries to load `miniprogram-automator` from that project first.

If your automator install lives elsewhere, pass it explicitly:

```powershell
cd tools/wechat-gui-check
npm run check -- --project-path <project-root> --automator-module-path C:\path\to\miniprogram-automator
```

Validate an external miniapp path without launching DevTools:

```powershell
cd tools/wechat-gui-check
npm run check -- --project-path <project-root> --route home --dry-run
```

`--dry-run` confirms that the route config, selected routes, and resolved miniapp root are valid. It also reports whether the local machine can see a usable DevTools CLI path and a `miniprogram-automator` runtime install, but it does not launch automation.

## Route Config Shape

Each route spec can include:

- `key`
- `route`
- `expectedPath`
- `primarySelector`
- `titleSelector`
- `settleMs`
- `dataFields`
- `actions`

Supported action types:

- `wait`
- `tap`
- `callMethod`

See `examples/sample.route-config.json` for the baseline multi-route fixture example and `examples/sample.rich.route-config.json` for a mixed-action route that exercises `wait`, `tap`, and `callMethod` against the bundled fixture.

## Bundled Fixture

The repository includes a minimal public demo project under `examples/fixture-miniapp/` with:

- a valid `project.config.json`
- a small `home` page with `.page-shell`, `.page-title`, `.btn-primary`, and a stable `applyScenario` page method for `callMethod` samples
- a small `tasks` page with `.filter-tab` interactions

This keeps the sample config reproducible and gives contributors a safe baseline when changing the harness.

## Output Shape

```text
.tmp/gui-check/<timestamp>/
|-- report.json
|-- report.partial.json
`-- *.png
```

`--dry-run` prints a JSON preflight summary to stdout instead of creating a run directory.

Current report schema highlights:

- `reportSchemaVersion`: current report shape version
- `summary.failureClassCounts`: failure counts grouped by classification code
- `summary.warningClassCounts`: warning counts grouped by classification code
- `pages[].failureCodes` / `pages[].warningCodes`: unique classification codes for a route
- `pages[].failureDetails` / `pages[].warningDetails`: structured issue entries with `code` and `message`

## Troubleshooting

- `Unable to load miniprogram-automator`: install it with `npm install --no-save miniprogram-automator` in the target miniapp project or in `tools/wechat-gui-check`, or pass `--automator-module-path` to an existing install.
- `登录用户不是该小程序的开发者`: this is a host/account AppID authorization blocker from WeChat DevTools. For public forward-tests, use a disposable local copy and swap the real upstream AppID for `touristappid` or another testing AppID you control before running `cli auto`.
- `screenshot unavailable: miniProgram.screenshot is not a function`: screenshot support varies across `miniprogram-automator` builds. The report classifies this as `screenshot_capability_missing`. Treat screenshot capture as best-effort evidence and rely on route/path/selector data when the rest of the run succeeds.
- screenshot capture timeout: the report classifies this as `screenshot_timeout`; rerun only if the screenshot itself matters, not as a default sign of repo failure.

## Notes

- screenshots are best-effort and may fail without invalidating the full run
- backend-dependent routes should be documented in the route config, not hidden in code
- start with one route before expanding to multiple routes
- the richer bundled sample exists to keep `wait` and `callMethod` coverage public and reproducible even before a second real-repo sample is documented
- the default repo install no longer carries `miniprogram-automator`'s transitive image stack; that runtime dependency is now user-supplied at execution time
- a Windows host run against a copied fixture project outside the repository completed successfully for the `home` route, but screenshot capture still timed out in that live run
- one external public-repo forward-test is now documented in `../../docs/gui-check-forward-test.md`
- for a second public-repo sample on a collaborator machine, use `../../docs/gui-check-collaborator-forward-test.md`
- this package is intentionally beta until that upstream dependency story is cleaner

## Remaining Work

- expand forward-testing beyond the first documented public miniapp repo
- add sample config for a real public demo repo
- revisit whether the current user-supplied runtime model should evolve into a cleaner adapter only after broader cross-machine evidence is collected
