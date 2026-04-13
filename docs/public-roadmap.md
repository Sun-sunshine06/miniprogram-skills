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

Status on 2026-03-31:

- completed and rolled into the `v0.3.0` tag:
  - example prompts for all four public skills
  - recorded validation passes for all four active skills
  - upgraded skill validator with stronger content checks
  - added a shared local validation entry point and aligned CI around it
  - added markdown link hygiene plus bilingual doc cross-link checks to the shared validation flow
  - expanded repository validation from selected samples to repo-wide JSON validity checks
  - recorded one documented external forward-test on a public miniapp repo for `tools/wechat-gui-check`
  - updated GUI checker docs with clearer forward-test and troubleshooting guidance
  - added a second bundled sample config that exercises `wait`, `tap`, and `callMethod` against the public fixture miniapp
  - documented the current runtime-model decision to keep `miniprogram-automator` user-supplied in the release baseline

This work was originally tracked as a standalone `v0.2` cycle, but it was ultimately released as part of `v0.3.0` instead of a separate `v0.2.0` tag.

Exit criteria:

- runnable local harness exists
- report format is documented
- route spec configuration is externalized
- one sample result artifact is documented
- bundled fixture samples cover both multi-route tap flows and richer mixed-action flows
- the harness has been exercised on at least one real miniapp repo outside the source project

## v0.3 Forward-Tested Skills

Goal:

- confirm that the skills generalize across more than one repo

Current status on 2026-04-13:

- starting point:
  - the `v0.3.0` tag now captures the completed tool-extraction baseline
  - internal fixture-based validation evidence exists for all active skills
  - one external public-repo forward-test exists for `tools/wechat-gui-check`
  - a replayable routing prompt pack plus a machine-readable skill catalog now exist
  - replayable prompt-and-answer routing transcripts now exist for all 4 positive fixtures and the 2 adjacent boundary prompts
  - repo-owned negative-path fixtures now exist for a broken scaffold, wrong-root recovery residue, and a GUI session blocker sample
  - non-GUI public-repo evidence now exists for scaffold review, CLI auth/session blocker classification, and a recovery sample derived from `ecomfe/echarts-for-weixin`
- in progress:
  - collaborator-host forward-testing to validate cross-machine behavior
  - broadening external evidence beyond the current GUI-focused public forward-test into more success-path and recovery-path repo shapes
  - extending the current negative-path pack into more live host-side and external-repo observations
- next:
  - add one collaborator-host public-repo forward-test with a different scaffold shape
  - add at least one success-path CLI public-repo run beyond the current auth/session blocker sample
  - add at least one live host-side negative sample beyond the current repo-owned fixture pack

Exit criteria:

- each active skill is tested through realistic prompts
- at least two non-source miniapp repos or host environments contribute evidence, with at least one collaborator-host run
- adjacent-skill boundaries have reviewable routing evidence
- repo-specific wording is removed where it blocks reuse

## v0.4 Catalog And Routing Baseline

Goal:

- make the public skill surface machine-readable and replayable before claiming a broader maturity jump

Current status on 2026-04-13:

- `manifests/skill-catalog.json` records the current public skill surface, host requirements, evidence state, and adjacent routing priorities
- `evals/routing/` now contains replayable positive and boundary prompt fixtures for the four public skills
- `evals/routing-replays/` now contains transcript-backed local replay records for every committed routing case
- `docs/routing-eval-log.md` records the current routing outcomes against those replay transcripts instead of only curated maintainer notes
- shared validation checks the catalog, the routing fixture pack, and the routing replay pack on every run

Still missing:

- installed-skill or host-routed transcript capture beyond the current local replay pack
- collaborator-host evidence for another repo or host shape beyond the first external forward-test

Exit criteria:

- the machine-readable catalog stays aligned with live public skill folders and review docs
- each public skill has replayable positive coverage and each adjacent high-confusion pair has a committed boundary prompt
- at least one installed-skill or replayable transcript-backed routing result is recorded against the committed prompt pack

## Later Expansion

Consider expanding into:

- local backend bridge patterns
- design-system evolution patterns
- higher-level business-flow skills

Only expand after the public boundary stays clean and the first batch proves useful.
