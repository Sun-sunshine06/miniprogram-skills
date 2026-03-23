# Public Roadmap

## v0 Draft

Goal:

- establish the repository direction
- define the first public skill batch
- strip obvious source-repo coupling

Exit criteria:

- top-level README exists
- skill map exists
- four core DevTools/scaffold skills have usable `SKILL.md` files
- each skill has at least one reusable reference file

## v0.1 Docs-First Release

Goal:

- publish a documentation-only release that is honest about scope

Exit criteria:

- license selected
- repository metadata finalized
- all draft language reviewed
- one example prompt per skill added in references if needed

## v0.2 Tool Extraction

Goal:

- harden the extracted host-side GUI smoke harness in `tools/wechat-gui-check`

Exit criteria:

- runnable local harness exists
- report format is documented
- route spec configuration is externalized
- one sample result artifact is documented
- the harness has been exercised on at least one real miniapp repo outside the source project

## v0.3 Forward-Tested Skills

Goal:

- confirm that the skills generalize across more than one repo

Exit criteria:

- each active skill is tested through realistic prompts
- at least one non-source miniapp repo is used for evaluation
- repo-specific wording is removed where it blocks reuse

## Later Expansion

Consider expanding into:

- local backend bridge patterns
- design-system evolution patterns
- higher-level business-flow skills

Only expand after the public boundary stays clean and the first batch proves useful.
