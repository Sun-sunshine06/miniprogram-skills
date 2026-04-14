# Routing Eval Log

This log records observed routing outcomes against the committed prompt pack under `evals/routing/`.

Evidence source preference remains:

1. installed-skill transcripts from a local skill directory
2. replayable eval runs where the prompt and answer are both captured
3. curated maintainer notes when the first two are not yet available

As of 2026-04-14, the repository still does not include a live installed-skill router or transcript capture flow. It now does include committed replay transcripts under `evals/routing-replays/` for all 7 positive fixtures and the 5 adjacent boundary prompts. These entries are stronger than the earlier curated notes because the prompt and answer are both captured, but they are still local replay evidence rather than live installed-skill routing.

Current status:

- positive fixtures with a replay transcript: 7 / 7
- boundary fixtures with a replay transcript: 5 / 5
- installed-skill transcripts recorded: 0
- replay transcripts recorded: 12
- collaborator-host routing runs recorded: 0

## 2026-04-14 - `miniapp-center-hub-refactor`

**Prompt fixture**

- `evals/routing/positive/miniapp-center-hub-refactor.json`

**Expected routing**

- use `miniapp-center-hub-refactor`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 4 required output sections in the expected order
- the answer stays on top-level ownership and migration order instead of collapsing into queue actions or copy cleanup

**Evidence source**

- replay transcript captured at `evals/routing-replays/miniapp-center-hub-refactor.json`

## 2026-04-14 - `miniapp-review-queue-actions`

**Prompt fixture**

- `evals/routing/positive/miniapp-review-queue-actions.json`

**Expected routing**

- use `miniapp-review-queue-actions`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 4 required output sections in the expected order
- the answer stays on queue-state actions and refresh flow instead of widening into navigation redesign

**Evidence source**

- replay transcript captured at `evals/routing-replays/miniapp-review-queue-actions.json`

## 2026-04-14 - `miniapp-user-facing-copy-trim`

**Prompt fixture**

- `evals/routing/positive/miniapp-user-facing-copy-trim.json`

**Expected routing**

- use `miniapp-user-facing-copy-trim`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 4 required output sections in the expected order
- the answer stays on trimming user-facing copy and does not over-claim architectural refactoring

**Evidence source**

- replay transcript captured at `evals/routing-replays/miniapp-user-facing-copy-trim.json`

## 2026-04-13 - `miniapp-official-scaffold-alignment`

**Prompt fixture**

- `evals/routing/positive/miniapp-official-scaffold-alignment.json`

**Expected routing**

- use `miniapp-official-scaffold-alignment`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 4 required output sections in the expected order
- the answer stays on pre-import scaffold validity and does not drift into recovery or DevTools troubleshooting

**Evidence source**

- replay transcript captured at `evals/routing-replays/miniapp-official-scaffold-alignment.json`

**Notes**

- the prompt still anchors clearly on official scaffold validity before feature work begins
- no wording change is needed at this stage

## 2026-04-13 - `miniapp-devtools-recovery`

**Prompt fixture**

- `evals/routing/positive/miniapp-devtools-recovery.json`

**Expected routing**

- use `miniapp-devtools-recovery`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 4 required recovery sections in the expected order
- the answer stays on post-import cleanup and tells the user what to restore, delete, and change in DevTools

**Evidence source**

- replay transcript captured at `evals/routing-replays/miniapp-devtools-recovery.json`

**Notes**

- the prompt remains clearly post-import and post-drift, which keeps it on the recovery side rather than the scaffold-review side
- no wording change is needed at this stage

## 2026-04-13 - `miniapp-devtools-cli-repair`

**Prompt fixture**

- `evals/routing/positive/miniapp-devtools-cli-repair.json`

**Expected routing**

- use `miniapp-devtools-cli-repair`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 4 required CLI-repair sections in the expected order
- the answer keeps the official CLI as the primary evidence surface and does not overclaim GUI-only coverage

**Evidence source**

- replay transcript captured at `evals/routing-replays/miniapp-devtools-cli-repair.json`

**Notes**

- the prompt still clearly asks for CLI-visible evidence, live-port recovery, and narrow repo-safe fixes
- no wording change is needed at this stage

## 2026-04-13 - `miniapp-devtools-gui-check`

**Prompt fixture**

- `evals/routing/positive/miniapp-devtools-gui-check.json`

**Expected routing**

- use `miniapp-devtools-gui-check`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 5 required GUI-check sections in the expected order
- the answer stays on narrow host-side runtime evidence and keeps screenshots as best-effort rather than the primary signal

**Evidence source**

- replay transcript captured at `evals/routing-replays/miniapp-devtools-gui-check.json`

**Notes**

- the prompt still clearly says CLI `preview` already succeeds and asks for GUI/runtime evidence instead of another compile pass
- no wording change is needed at this stage

## 2026-04-13 - Boundary `miniapp-devtools-gui-check` over `miniapp-devtools-cli-repair`

**Prompt fixture**

- `evals/routing/boundaries/gui-check-over-cli-repair.json`

**Expected routing**

- use `miniapp-devtools-gui-check`
- do not route to `miniapp-devtools-cli-repair`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 5 GUI-check output sections in the expected order
- the answer explicitly treats the already-green `preview` result as a reason to avoid another CLI-first compile pass

**Evidence source**

- replay transcript captured at `evals/routing-replays/gui-check-over-cli-repair.json`

**Notes**

- the strongest routing signal remains that `preview` is already green and the user explicitly asks for runtime evidence instead of another compile check
- this is still the highest-confusion adjacent boundary and remains a strong candidate for the first live installed-skill transcript

## 2026-04-14 - Boundary `miniapp-center-hub-refactor` over `miniapp-review-queue-actions`

**Prompt fixture**

- `evals/routing/boundaries/miniapp-center-hub-refactor-over-miniapp-review-queue-actions.json`

**Expected routing**

- use `miniapp-center-hub-refactor`
- do not route to `miniapp-review-queue-actions`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 4 hub-refactor sections in the expected order
- the answer treats queue-card changes as secondary until top-level ownership is fixed

**Evidence source**

- replay transcript captured at `evals/routing-replays/miniapp-center-hub-refactor-over-miniapp-review-queue-actions.json`

## 2026-04-14 - Boundary `miniapp-center-hub-refactor` over `miniapp-user-facing-copy-trim`

**Prompt fixture**

- `evals/routing/boundaries/miniapp-center-hub-refactor-over-miniapp-user-facing-copy-trim.json`

**Expected routing**

- use `miniapp-center-hub-refactor`
- do not route to `miniapp-user-facing-copy-trim`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 4 hub-refactor sections in the expected order
- the answer treats wording drift as secondary because the stronger signal is broken ownership across top-level destinations

**Evidence source**

- replay transcript captured at `evals/routing-replays/miniapp-center-hub-refactor-over-miniapp-user-facing-copy-trim.json`

## 2026-04-14 - Boundary `miniapp-review-queue-actions` over `miniapp-user-facing-copy-trim`

**Prompt fixture**

- `evals/routing/boundaries/miniapp-review-queue-actions-over-miniapp-user-facing-copy-trim.json`

**Expected routing**

- use `miniapp-review-queue-actions`
- do not route to `miniapp-user-facing-copy-trim`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 4 queue-action sections in the expected order
- the answer keeps the boundary on card-level action design and refresh flow rather than drifting into label-only cleanup

**Evidence source**

- replay transcript captured at `evals/routing-replays/miniapp-review-queue-actions-over-miniapp-user-facing-copy-trim.json`

## 2026-04-13 - Boundary `miniapp-official-scaffold-alignment` over `miniapp-devtools-recovery`

**Prompt fixture**

- `evals/routing/boundaries/scaffold-alignment-over-recovery.json`

**Expected routing**

- use `miniapp-official-scaffold-alignment`
- do not route to `miniapp-devtools-recovery`

**Observed routing**

- selected correctly

**Observed answer shape**

- the replay answer preserves all 4 scaffold-review output sections in the expected order
- the answer stays on pre-import validity and does not start prescribing cleanup steps for a drift event that has not happened yet

**Evidence source**

- replay transcript captured at `evals/routing-replays/scaffold-alignment-over-recovery.json`

**Notes**

- the prompt still explicitly says DevTools import has not happened yet, which keeps it in pre-import scaffold review rather than cleanup/recovery
- no wording change is needed at this stage
