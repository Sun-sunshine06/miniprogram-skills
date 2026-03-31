# Routing Eval Plan

This document describes the smallest useful routing-eval / transcript evidence pack for `miniprogram_skills`.

The goal is not to build a large telemetry system during the current early `v0.3` stage. The goal is to collect enough clean evidence that future audits can say the public skill boundaries were tested in real agent routing conditions, not only in repository-owned validation flows.

The prompt pack described below is now mirrored under `evals/routing/` as machine-readable fixtures. The next step is to record observed routing outcomes against those committed prompts instead of keeping the plan as prose only.

## Why This Is Not A Current P0

As of 2026-03-31:

- the repository has just been tagged `v0.3.0` and is only starting the evidence-heavy part of `v0.3`
- `tools/wechat-gui-check` is still explicitly beta and host-dependent
- the public roadmap does not claim that all 4 skills are already proven in live installed-skill routing

Because of that, missing routing transcripts are a next-stage confidence gap, not a contradiction of the current public story.

## Goal

Add a small, reviewable evidence set that proves:

1. each public skill can be selected from a realistic user prompt
2. each adjacent skill pair has at least one clear non-use prompt
3. the resulting answer shape matches the intended workflow boundary

## Minimal Evidence Pack

For each of the 4 public skills, add:

1. one installed-skill transcript or replayable routing-eval prompt where the skill should be selected
2. one short outcome note:
   - selected correctly
   - partially selected / mixed boundary
   - not selected
3. one follow-up note on what wording or structure changed, if any

For each adjacent skill boundary, add one non-use case:

- `miniapp-devtools-cli-repair` vs `miniapp-devtools-gui-check`
- `miniapp-devtools-recovery` vs `miniapp-official-scaffold-alignment`

## Recommended Format

Create one small evidence doc or log section with entries like:

```markdown
## 2026-04-xx - `miniapp-devtools-gui-check`

**Prompt**
`preview` already succeeds, but tapping a button still blanks the page. Run a minimal GUI-side smoke check and tell me whether this is repo code or DevTools session state.

**Expected routing**
- use `miniapp-devtools-gui-check`
- do not route to `miniapp-devtools-cli-repair`

**Observed routing**
- {selected / partially selected / not selected}

**Observed answer shape**
- {did it produce the expected output format?}

**Notes**
- {boundary confusion, wording update, or no change needed}
```

## Suggested Execution Order

1. start with the 4 positive prompts, one per public skill
2. then add the 2 adjacent non-use prompts
3. only after those 6 samples are stable, decide whether more routing coverage is worth the maintenance cost

## Prompt Set

### Positive Prompt 1 - `miniapp-official-scaffold-alignment`

```text
I am starting a new WeChat Mini Program repo. Before feature work begins, review the intended `project.config.json`, `app.json`, `miniprogramRoot`, and page file layout against official platform rules and tell me the smallest valid scaffold decision.
```

### Positive Prompt 2 - `miniapp-devtools-recovery`

```text
After importing this repo into WeChat DevTools the wrong way, the project gained template residue and the start page drifted. Restore the intended repo shape, tell me what should be reverted, and tell me what to change in DevTools.
```

### Positive Prompt 3 - `miniapp-devtools-cli-repair`

```text
WeChat DevTools `preview` is failing and I only trust CLI-visible evidence right now. Re-establish the live port through the official CLI, determine whether this is a repo-level issue, and only apply a safe fix if the failure is clearly local to the repo.
```

### Positive Prompt 4 - `miniapp-devtools-gui-check`

```text
CLI `preview` already succeeds, but the page still blanks only after entering the route and tapping one button. Run a narrow host-side GUI smoke check and separate repo runtime failures from DevTools session problems.
```

### Boundary Prompt 1 - GUI check should win over CLI repair

```text
`preview` is already green, but tapping the home-page CTA intermittently opens a blank page. I need runtime evidence, not another compile check.
```

### Boundary Prompt 2 - Scaffold alignment should win over recovery

```text
I have not imported this repo into DevTools yet. I just want to know whether the planned `miniprogramRoot`, `app.json.pages`, and file quartets form an officially valid starting scaffold.
```

## Evidence Source Preference

Prefer, in order:

1. installed-skill transcripts from a local skill directory
2. replayable eval runs where the prompt and answer are both captured
3. curated maintainer notes only if the first two are not yet available

## Exit Criteria

This plan is "good enough" when:

- all 4 public skills have one positive routing sample
- both adjacent-skill boundaries have one non-use sample
- the evidence is easy to re-check during future public-release reviews
