# Runtime Model Decision

## Selected Default

For the current `v0.2` release window, `tools/wechat-gui-check` should keep the current user-supplied `miniprogram-automator` runtime model.

That means:

- the repository default install does not bundle `miniprogram-automator`
- live GUI automation loads `miniprogram-automator` at execution time from an explicit path, the target miniapp project, or a manual local install under `tools/wechat-gui-check`
- dry-run, config validation, reporting, and bundled samples remain repo-owned and reproducible without pretending that host-side GUI automation is fully portable

## Why Keep This Model

- it keeps the default repository dependency surface small and public-review friendly
- it avoids pulling the upstream automation image-stack dependency chain into the default lockfile
- it matches the real host-side nature of WeChat DevTools automation, which already depends on local DevTools state, account state, and AppID authorization
- it lets contributors point at a project-local or explicitly managed runtime install instead of forcing one repo-owned version onto every host
- it keeps the repository honest about what CI can and cannot verify

## Alternatives Considered

### Bundle `miniprogram-automator` as a normal dependency

Pros:

- the setup story is simpler for first-time users
- maintainers get a more standardized default runtime version
- docs can look more "one command and go"

Cons:

- the repository lockfile and default install become heavier again
- upstream audit noise and transitive dependency churn move back into the repo
- it suggests a level of host portability that the DevTools + account + AppID stack still does not actually provide
- it conflicts with the current public-boundary goal of the extraction

### Publish or split a dedicated adapter package

Pros:

- long-term architecture is cleaner
- the main repo could define a stable harness/report contract while isolating the messy upstream runtime dependency
- it creates a clearer path if the project later supports more than one automation backend

Cons:

- it adds packaging, versioning, and interface-design overhead too early
- the current repo still needs more cross-machine evidence before that abstraction is justified
- it would slow down the current release path without reducing today's main uncertainty

### Reduce the tool to dry-run only

Pros:

- easiest model to support in CI and public docs
- avoids the most fragile host-side behavior

Cons:

- removes the main reason this harness exists, which is catching runtime and interaction problems that CLI `preview` and preflight checks do not surface
- weakens the value of `miniapp-devtools-gui-check`

## Similar Decisions Around This Tool

This runtime choice belongs to a broader family of boundary decisions:

- keep live GUI automation on real hosts, but keep CI limited to dry-run and static validation
- treat screenshot capture as best-effort evidence instead of a hard success gate
- document collaborator-host forward-testing explicitly instead of pretending the maintainer host alone proves portability
- keep route behavior and backend assumptions in config/docs instead of hiding them in repo-specific code

All of these decisions make the same tradeoff: less fake convenience, more honest portability.

## Project-Specific Tradeoff Summary

For this repository today, the current runtime model is:

- better for public extraction, because it keeps the repo boundary clean
- better for maintenance, because it avoids owning an unstable upstream runtime by default
- worse for first-run convenience, because contributors must still install or point to `miniprogram-automator`
- worse for exact reproducibility, because host-side runtime versions can differ

That trade is acceptable right now because the repository is still a reusable skill/tooling repo with a beta GUI harness, not a polished end-user automation product.

## Revisit Trigger

Revisit this decision only if one of these changes:

- collaborator-host forward-tests show that the current model is confusing or unreliable even with the improved docs
- contributors repeatedly fail on runtime setup in ways that a repo-owned adapter would clearly solve
- the project decides to invest in a stronger long-term harness product instead of a lightweight extracted beta utility

Until then, the recommended path is:

1. keep the current user-supplied runtime model for `v0.2`
2. collect broader cross-machine forward-test evidence
3. reconsider an adapter-style design only after that evidence shows it would materially help
