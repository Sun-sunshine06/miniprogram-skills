# WeChat GUI Check

Config-driven WeChat DevTools GUI smoke harness for runtime and interaction checks that do not show up in CLI `preview`.

## Current Status

Public beta extraction. The harness now ships with a bundled fixture miniapp, keeps its default repo-owned dependency surface small by loading `miniprogram-automator` only from an explicit runtime install, and now supports automated dry-run checks against a copied project root outside the repository. Full forward-testing on an independent public miniapp repository is still pending.

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
- `examples/sample-report.json`: example output shape

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

See `examples/sample.route-config.json`.

## Bundled Fixture

The repository includes a minimal public demo project under `examples/fixture-miniapp/` with:

- a valid `project.config.json`
- a small `home` page with `.page-shell`, `.page-title`, and `.btn-primary`
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

## Notes

- screenshots are best-effort and may fail without invalidating the full run
- backend-dependent routes should be documented in the route config, not hidden in code
- start with one route before expanding to multiple routes
- the default repo install no longer carries `miniprogram-automator`'s transitive image stack; that runtime dependency is now user-supplied at execution time
- a Windows host run against a copied fixture project outside the repository completed successfully for the `home` route, but screenshot capture still timed out in that live run
- this package is intentionally beta until that upstream dependency story is cleaner

## Remaining Work

- forward-test the full automation flow on an independent public miniapp repo
- add sample config for a real public demo repo
- decide whether to keep the current user-supplied runtime model or replace `miniprogram-automator` with a cleaner long-term adapter
