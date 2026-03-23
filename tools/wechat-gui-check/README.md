# WeChat GUI Check

Config-driven WeChat DevTools GUI smoke harness for runtime and interaction checks that do not show up in CLI `preview`.

## Current Status

Public beta extraction. The harness now ships with a bundled fixture miniapp so the sample config is runnable without access to a private source repository, but it still needs forward-testing on more than one real miniapp repository.

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

`<project-root>` must point to a WeChat Mini Program project root that contains `project.config.json`. The checker now validates that root before it launches DevTools automation.

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

## Notes

- screenshots are best-effort and may fail without invalidating the full run
- backend-dependent routes should be documented in the route config, not hidden in code
- start with one route before expanding to multiple routes
- the current audit findings are isolated to `miniprogram-automator`'s transitive image stack, not to the direct `pngjs` integration in this repo
- this package is intentionally beta until that upstream dependency story is cleaner

## Remaining Work

- forward-test on additional miniapp repos
- add sample config for a real public demo repo
- replace or isolate the current `miniprogram-automator` image stack so the remaining moderate audit findings disappear
