# DevTools Recovery Checklist

## Standard Repo Shape

Use these as the default expectations unless the project spec says otherwise:

- the repository root is the directory imported into WeChat DevTools
- the miniapp code may live in a dedicated folder such as `miniprogram/`
- shared project config lives in `project.config.json`
- local-only DevTools state may live in `project.private.config.json`

## Keep

- tracked app entry files
- tracked pages and components
- shared config files
- docs, tests, and tools that belong to the repository contract

## Common Residue To Delete

Delete only when DevTools generated them and the app does not depend on them:

- nested code roots created by wrong-root import
- template pages such as `pages/index/` or `pages/logs/`
- generated helper files from the starter template
- extra `project.config.json`, `tsconfig.json`, or package files created in the wrong directory

## Restore First

If DevTools overwrote tracked files, restore them before further cleanup:

- `app.json`
- app entry logic file
- global style file
- tracked page or component files replaced by template output

## Error Mapping

### Missing page `.js` file while the repo uses TypeScript

Likely cause:

- DevTools is not recognizing the project as a TypeScript miniapp.

Check:

- correct import root
- `project.config.json`
- `miniprogramRoot`
- compiler-plugin settings
- `tsconfig.json`

### Startup page is not defined in `app.json`

Likely cause:

- DevTools is still using a stale custom compile condition.

Check:

- current compile mode in the toolbar
- `project.config.json.condition`
- `project.private.config.json`

## Import Workflow

1. Close the polluted project in DevTools.
2. Re-import the intended repository root.
3. Do not create a new template project on top of an existing repo.
4. Clear compile cache if the old project shape was different.
5. Verify that normal compile mode or a real startup page is selected.
