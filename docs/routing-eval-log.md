# Routing Eval Log

This log records observed routing outcomes against the committed prompt pack under `evals/routing/`.

Evidence source preference remains:

1. installed-skill transcripts from a local skill directory
2. replayable eval runs where the prompt and answer are both captured
3. curated maintainer notes when the first two are not yet available

As of 2026-03-31, the repository still does not include a live installed-skill router or transcript capture flow. Because of that, the entries below are explicitly recorded as **curated maintainer replay notes** against the committed fixtures and current public skill contracts. They are useful review evidence, but they are not a substitute for future live transcript-backed routing evidence.

Current status:

- positive fixtures with an initial observed outcome note: 4 / 4
- boundary fixtures with an initial observed outcome note: 2 / 2
- installed-skill transcripts recorded: 0
- collaborator-host routing runs recorded: 0

## 2026-03-31 - `miniapp-official-scaffold-alignment`

**Prompt fixture**

- `evals/routing/positive/miniapp-official-scaffold-alignment.json`

**Expected routing**

- use `miniapp-official-scaffold-alignment`

**Observed routing**

- selected correctly

**Observed answer shape**

- live answer shape not captured yet
- committed fixture sections still match the documented output contract in `skills/miniapp-official-scaffold-alignment/SKILL.md`

**Evidence source**

- curated maintainer replay note against the committed fixture and current skill contract

**Notes**

- the prompt clearly anchors on official scaffold validity before any DevTools import or recovery event
- no wording change is needed at this stage

## 2026-03-31 - `miniapp-devtools-recovery`

**Prompt fixture**

- `evals/routing/positive/miniapp-devtools-recovery.json`

**Expected routing**

- use `miniapp-devtools-recovery`

**Observed routing**

- selected correctly

**Observed answer shape**

- live answer shape not captured yet
- committed fixture sections still match the documented output contract in `skills/miniapp-devtools-recovery/SKILL.md`

**Evidence source**

- curated maintainer replay note against the committed fixture and current skill contract

**Notes**

- the prompt is clearly post-import and post-drift, which keeps it on the recovery side rather than the scaffold-review side
- no wording change is needed at this stage

## 2026-03-31 - `miniapp-devtools-cli-repair`

**Prompt fixture**

- `evals/routing/positive/miniapp-devtools-cli-repair.json`

**Expected routing**

- use `miniapp-devtools-cli-repair`

**Observed routing**

- selected correctly

**Observed answer shape**

- live answer shape not captured yet
- committed fixture sections still match the documented output contract in `skills/miniapp-devtools-cli-repair/SKILL.md`

**Evidence source**

- curated maintainer replay note against the committed fixture and current skill contract

**Notes**

- the prompt explicitly asks for CLI-visible evidence, live-port recovery, and safe repo-local fixes
- no wording change is needed at this stage

## 2026-03-31 - `miniapp-devtools-gui-check`

**Prompt fixture**

- `evals/routing/positive/miniapp-devtools-gui-check.json`

**Expected routing**

- use `miniapp-devtools-gui-check`

**Observed routing**

- selected correctly

**Observed answer shape**

- live answer shape not captured yet
- committed fixture sections still match the documented output contract in `skills/miniapp-devtools-gui-check/SKILL.md`

**Evidence source**

- curated maintainer replay note against the committed fixture and current skill contract

**Notes**

- the prompt clearly says CLI `preview` already succeeds and asks for runtime-only GUI evidence
- no wording change is needed at this stage

## 2026-03-31 - Boundary `miniapp-devtools-gui-check` over `miniapp-devtools-cli-repair`

**Prompt fixture**

- `evals/routing/boundaries/gui-check-over-cli-repair.json`

**Expected routing**

- use `miniapp-devtools-gui-check`
- do not route to `miniapp-devtools-cli-repair`

**Observed routing**

- selected correctly

**Observed answer shape**

- live answer shape not captured yet
- committed fixture sections still match the documented output contract in `skills/miniapp-devtools-gui-check/SKILL.md`

**Evidence source**

- curated maintainer replay note against the committed fixture and current skill contract

**Notes**

- the strongest routing signal is that `preview` is already green and the user explicitly asks for runtime evidence instead of another compile check
- this remains the highest-confusion adjacent boundary and should be prioritized for the first live transcript-backed run

## 2026-03-31 - Boundary `miniapp-official-scaffold-alignment` over `miniapp-devtools-recovery`

**Prompt fixture**

- `evals/routing/boundaries/scaffold-alignment-over-recovery.json`

**Expected routing**

- use `miniapp-official-scaffold-alignment`
- do not route to `miniapp-devtools-recovery`

**Observed routing**

- selected correctly

**Observed answer shape**

- live answer shape not captured yet
- committed fixture sections still match the documented output contract in `skills/miniapp-official-scaffold-alignment/SKILL.md`

**Evidence source**

- curated maintainer replay note against the committed fixture and current skill contract

**Notes**

- the prompt explicitly says DevTools import has not happened yet, which keeps it in pre-import scaffold review rather than cleanup/recovery
- no wording change is needed at this stage
