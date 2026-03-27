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

Current status on 2026-03-27:

- completed:
  - example prompts for all four public skills
  - recorded validation passes for all four active skills
  - upgraded skill validator with stronger content checks
  - added a shared local validation entry point and aligned CI around it
  - added markdown link hygiene plus bilingual doc cross-link checks to the shared validation flow
  - expanded repository validation from selected samples to repo-wide JSON validity checks
  - recorded one documented external forward-test on a public miniapp repo for `tools/wechat-gui-check`
  - updated GUI checker docs with clearer forward-test and troubleshooting guidance
- in progress:
  - broader cross-repo forward-testing beyond the first public-repo evidence point
  - collaborator-host forward-testing to validate cross-machine behavior
- next:
  - add one more public repo forward-test with a different scaffold shape on a collaborator machine
  - review whether the bundled sample route config should grow into a second public sample that covers more than one route or action type
  - draft the `v0.2.0` release note once the remaining evidence is stable

Exit criteria:

- runnable local harness exists
- report format is documented
- route spec configuration is externalized
- one sample result artifact is documented
- the harness has been exercised on at least one real miniapp repo outside the source project

## v0.3 Forward-Tested Skills

Goal:

- confirm that the skills generalize across more than one repo

Entry conditions from current progress:

- internal fixture-based validation evidence now exists for all active skills
- the next gating step is an external public repo forward-test rather than more docs-only evidence

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
