# Skill Optimization Report
**Date**: 2026-03-30
**Scope**: all 4 public skills under `miniprogram_skills/skills/`
**Evidence**:
- current repository state on `main`
- `python scripts/validate_skills.py skills --require-example-prompts --check-portability` passed on 2026-03-30
- `docs/skill-validation-log.md` with 4 recorded validation entries
- 8 historical Codex sessions from 2026-03-23 through 2026-03-27 whose shell workdirs included `miniprogram_skills`
- `docs/skill-review-checklist.md`, `docs/conventions*.md`, `scripts/check.ps1`, and `docs/public-roadmap.md`
**Confidence**:
- static quality: high
- workflow completion: medium
- trigger rate / user reaction / undertrigger: low
**Release stage**: docs-first public beta / `v0.2` tool-extraction stage

## Scope Notes

This repository already has strong docs-first quality controls, but the available historical sessions are mostly maintainer sessions about building and publishing the repository, not clean end-user sessions where these 4 skills were loaded from an installed skill directory and routed live by the agent.

That means this report can confidently score:

- static quality
- progressive disclosure / token economics
- existence of validation evidence
- cross-skill boundary design

It cannot confidently score:

- real trigger rate
- post-invocation user reaction
- true undertrigger frequency

Those dimensions are still included below, but several are marked `N/A` or low-confidence on purpose.

## Overview

| Skill | Trigger | Reaction | Completion | Static | Undertrigger | Token | Score |
|-------|---------|----------|------------|--------|--------------|-------|-------|
| `miniapp-devtools-cli-repair` | N/A | N/A | strong | strong | N/A | strong | 4/5 |
| `miniapp-devtools-gui-check` | N/A | N/A | strong | strong | N/A | strong | 4/5 |
| `miniapp-devtools-recovery` | N/A | N/A | strong | strong | N/A | strong | 4/5 |
| `miniapp-official-scaffold-alignment` | N/A | N/A | strong | strong | N/A | strong | 4/5 |

Scoring note:

- every skill is capped at `4/5` in this audit, because a `5/5` rating would require strong live-routing and user-reaction evidence that the repository does not yet have

## P0 Fixes

None from the current evidence set.

Severity calibration note:

- As of 2026-03-30, this repository still presents itself as docs-first and beta-oriented, and its public roadmap does not claim that live agent routing quality is already proven.
- Because of that, the missing routing-eval / transcript evidence is best treated as the top `P1` for the next maturity step, not as an immediate `P0` contradiction of the current public story.

## P1 Improvements

1. Add real routing evidence for the public skills. The 8 historical Codex sessions tied to `miniprogram_skills` are overwhelmingly repository-construction sessions rather than installed-skill consumption, so trigger rate, user reaction, and undertrigger cannot be validated with confidence. Record at least one installed-skill transcript or structured routing eval per public skill before claiming the public descriptions are proven in live agent use.
2. Add negative-path validation coverage. The current validation log proves that each skill can succeed once, but it does not yet cover a deliberately wrong scaffold, wrong-root import residue, or a GUI-session/setup failure with the same level of repeatable evidence.
3. Add a small routing matrix for adjacent skills. The descriptions and example prompts already do most of this work, but `miniapp-devtools-cli-repair` vs `miniapp-devtools-gui-check` and `miniapp-devtools-recovery` vs `miniapp-official-scaffold-alignment` are close enough that a repo-owned boundary matrix would make future edits safer.

## P2 Optional Optimizations

1. Trim 20-40 characters from each frontmatter description so the last disambiguating phrase is less likely to be truncated in agent skill lists.
2. Split "repo-authoring evidence" from "installed-skill usage evidence" in the validation log so future audits do not need to reconstruct that distinction from session history.

## Milestone Fit

- current-milestone blockers:
  - none identified beyond the repository's already-declared beta and host-side limits
- next-milestone evidence work:
  - add routing-eval / transcript-backed evidence for the 4 public skills
  - expand negative-path skill validations

## Repository-Level Findings

### Strengths

- The repository is already unusually strong on static hygiene. All 4 public skills passed the current validator, each skill has `references/`, `agents/openai.yaml`, example prompts, and a concise `SKILL.md`.
- Progressive disclosure is healthy. The 4 public skill bodies are about 251-317 words each, while detail lives in `references/`.
- Cross-skill boundaries are not only in descriptions; they are reinforced by "Do Not Use This Skill When" examples in every public skill.
- The repo has a real contributor workflow: validator, docs checks, JSON checks, tool syntax checks, and external-project dry-run smoke coverage are all wired into `scripts/check.ps1`.

### Constraints

- The strongest evidence is still repository-owned and maintainer-curated.
- `miniapp-devtools-gui-check` and `miniapp-devtools-cli-repair` depend on host-side WeChat DevTools behavior, so successful dry-run and docs evidence do not fully replace live routing evidence.
- The repository's public story is intentionally honest about host-only limits, which is good engineering hygiene but means some dimensions stay unproven until more collaborator or consumer sessions exist.

## Per-Skill Diagnostics

### `miniapp-devtools-cli-repair`

#### 4.1 Trigger Rate

`N/A — insufficient live routing evidence`

- No clean installed-skill transcript set was found for this public repo.
- Historical `miniprogram_skills` sessions mostly discuss repository extraction, docs, or roadmap work rather than asking the agent to diagnose a live DevTools CLI failure through the installed skill.

#### 4.2 User Reaction

`N/A — insufficient live invocation evidence`

- The available evidence does not show repeated real user turns immediately after live invocation of this public skill.

#### 4.3 Workflow Completion

`strong`

- `docs/skill-validation-log.md` records one host-side validation pass where the workflow reached the intended end state:
  - established connectivity with `open`
  - surfaced a real `preview` failure
  - classified the result as an AppID / credential limit rather than a repo auto-fix case
- This is good evidence that the workflow itself is coherent, even if it is not yet broad usage telemetry.

#### 4.4 Static Quality

`strong`

- Frontmatter is valid and meaningful.
- The description is action-oriented and clearly framed around the CLI path.
- The body is concise, references are present, and `agents/openai.yaml` aligns with the skill.
- Minor note: the description includes some action detail (`open`, `preview`, live port, safe repo-level fixes). In this repository that detail appears to function as boundary disambiguation rather than harmful workflow leakage.

#### 4.5a Overtrigger

`no concrete overtrigger evidence found`

- The example prompts include a clear non-use case that redirects GUI/runtime issues to `miniapp-devtools-gui-check`.
- Confidence is low because there is not enough live routing data.

#### 4.5b Undertrigger

`N/A — insufficient live routing evidence`

- I did not find a clean end-user message corpus for this public repo where CLI-repair-capable requests repeatedly appeared without the skill being used.
- Risk level is still moderate because this skill shares DevTools vocabulary with `miniapp-devtools-gui-check`.

#### 4.6 Cross-Skill Conflicts

`moderate but controlled`

- Strongest overlap is with `miniapp-devtools-gui-check`; both mention WeChat DevTools failures.
- Current mitigation is good:
  - CLI repair centers `open` / `preview` and CLI-visible evidence
  - GUI check centers runtime/interaction issues after CLI evidence stops being enough

#### 4.7 Environment Consistency

`pass with intentional host prerequisites`

- Repo-owned references exist.
- Host requirements are real but documented: official DevTools CLI availability and a valid host session.
- No broken repo-local references were found.

#### 4.8 Token Economics

`strong`

- Body size is about 317 words.
- The skill uses references instead of embedding the whole playbook in `SKILL.md`.
- This is a good size for a high-value operational skill.

### `miniapp-devtools-gui-check`

#### 4.1 Trigger Rate

`N/A — insufficient live routing evidence`

- There is strong tool validation evidence, but not enough installed-skill routing evidence for this public skill.

#### 4.2 User Reaction

`N/A — insufficient live invocation evidence`

- Available records show maintainer validation and documentation, not repeated user follow-up after public skill invocation.

#### 4.3 Workflow Completion

`strong`

- `docs/skill-validation-log.md` records a host-side validation pass that:
  - ran one narrow route
  - connected to host-side DevTools automation
  - collected route, selector, tap, console, and exception evidence
  - treated screenshot timeouts as best-effort limitations rather than false failure
- The external forward-test docs reinforce that this workflow is not only theoretical.

#### 4.4 Static Quality

`strong`

- The description is explicit about GUI-only runtime and interaction failures that do not show up in CLI `preview`.
- The body is concise, config-driven, and points to both the playbook and the extracted harness docs.
- Minor note: because this skill borders closely on CLI repair, the description should keep its "GUI-only after CLI is insufficient" signal very early and very sharp.

#### 4.5a Overtrigger

`no concrete overtrigger evidence found`

- The non-use example correctly redirects scaffold-validation work to `miniapp-official-scaffold-alignment`.
- Confidence is low without more real routing telemetry.

#### 4.5b Undertrigger

`N/A — insufficient live routing evidence`

- Historical repository sessions discuss GUI automation as a project direction, but that is not the same as finding end-user GUI-only bug reports that the public skill failed to catch.

#### 4.6 Cross-Skill Conflicts

`moderate but controlled`

- Primary overlap is with `miniapp-devtools-cli-repair`.
- Current separation is healthy:
  - CLI repair owns compile / preview / live-port evidence
  - GUI check owns runtime, interaction, and host-session smoke checks after preview is not enough

#### 4.7 Environment Consistency

`pass with explicit host dependency boundary`

- Repo references exist.
- `tools/wechat-gui-check` is real, documented, and validated by `scripts/check.ps1`.
- The user-supplied `miniprogram-automator` runtime dependency is an intentional host-side prerequisite, not a broken reference.

#### 4.8 Token Economics

`strong`

- Body size is about 251 words.
- Most detail lives in `references/gui-check-playbook.md` and the extracted tool README.
- Good progressive-disclosure behavior for a host-heavy skill.

### `miniapp-devtools-recovery`

#### 4.1 Trigger Rate

`N/A — insufficient live routing evidence`

- No robust installed-skill transcript sample is available for this public skill.

#### 4.2 User Reaction

`N/A — insufficient live invocation evidence`

- Historical evidence is mostly repository-maintainer work, not user follow-up after live recovery guidance.

#### 4.3 Workflow Completion

`strong`

- The validation log shows one real host-side scenario where DevTools rewrote `project.config.json`, and the recovery flow:
  - identified the drift as host-side config noise
  - restored shared config first
  - verified the restored file matched the known-good source

#### 4.4 Static Quality

`strong`

- The description is concrete and bounded around wrong-root import, template residue, compile-condition drift, and TypeScript recognition drift.
- The body stays concise and action-oriented.
- The skill does a good job of separating repo truth from local-only DevTools state.

#### 4.5a Overtrigger

`no concrete overtrigger evidence found`

- The non-use case correctly redirects greenfield scaffold design work to `miniapp-official-scaffold-alignment`.

#### 4.5b Undertrigger

`N/A — insufficient live routing evidence`

- No direct user-task corpus was available where recovery-type problems repeatedly appeared without the skill being invoked.
- Boundary risk still exists because this skill and scaffold alignment both mention `project.config.json`, root structure, and page/file consistency.

#### 4.6 Cross-Skill Conflicts

`moderate but controlled`

- Strongest overlap is with `miniapp-official-scaffold-alignment`.
- Current mitigation is solid:
  - recovery owns polluted or drifted repos
  - scaffold alignment owns greenfield or baseline-validity questions

#### 4.7 Environment Consistency

`pass`

- Repo references exist and point to repo-owned docs.
- No broken relative references were found.

#### 4.8 Token Economics

`strong`

- Body size is about 251 words.
- Detailed cleanup logic is kept in `references/devtools-recovery-checklist.md`.
- This is a healthy balance between routing clarity and token cost.

### `miniapp-official-scaffold-alignment`

#### 4.1 Trigger Rate

`N/A — insufficient live routing evidence`

- This skill has the clearest static trigger boundary, but the public repo still lacks enough clean installed-skill usage history to measure real routing frequency.

#### 4.2 User Reaction

`N/A — insufficient live invocation evidence`

- No solid post-invocation follow-up corpus was available for this public skill.

#### 4.3 Workflow Completion

`strong`

- The validation log records a clean scaffold review pass that:
  - identified repo root and miniapp root
  - checked `project.config.json.miniprogramRoot`
  - checked `app.json.pages`
  - verified page file quartets on disk
- This is good workflow evidence for the skill's intended output.

#### 4.4 Static Quality

`strong`

- This is the cleanest frontmatter boundary of the 4 public skills.
- It clearly anchors itself in official platform rules and avoids inventing missing spec details.
- The skill is compact and well supported by a dedicated official-baseline reference.

#### 4.5a Overtrigger

`no concrete overtrigger evidence found`

- The non-use example correctly redirects polluted-repo cleanup problems to recovery.

#### 4.5b Undertrigger

`N/A — insufficient live routing evidence`

- No trustworthy live transcript corpus was available to show repeated scaffold-review requests going elsewhere.

#### 4.6 Cross-Skill Conflicts

`low to moderate`

- Closest neighbor is `miniapp-devtools-recovery`.
- Current distinction is already good because scaffold alignment is framed as a baseline-validity or design task, not a cleanup task.

#### 4.7 Environment Consistency

`pass`

- Repo references exist.
- This skill has the least host-dependency surface of the 4 public skills.

#### 4.8 Token Economics

`strong`

- Body size is about 253 words.
- The skill is compact and uses references correctly.
- This is a strong example of progressive disclosure.

## Audit Conclusion

`miniprogram_skills` is already a strong public skill repository in static quality, contributor workflow, and validation discipline. The biggest remaining gap is not wording quality or progressive disclosure; it is the lack of clean live-routing evidence that proves these public descriptions are already selecting the right skill in real agent sessions.

In other words:

- the repository looks publication-ready from a docs and structure perspective
- the workflows look validated enough to be useful
- the remaining work is mostly about routing proof, negative-path evidence, and broader external consumption
