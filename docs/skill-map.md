# Skill Map

English | [中文](./skill-map.zh-CN.md)

## Active Public Skills

| Skill | Purpose | Current Shape | Public Readiness |
| --- | --- | --- | --- |
| `miniapp-official-scaffold-alignment` | Validate scaffold correctness before feature work begins. | `SKILL.md` + baseline reference | medium |
| `miniapp-devtools-recovery` | Recover repos after wrong-root imports or DevTools template drift. | `SKILL.md` + recovery checklist | medium |
| `miniapp-devtools-cli-repair` | Use the official DevTools CLI as the primary diagnostic path. | `SKILL.md` + CLI playbook | high |
| `miniapp-devtools-gui-check` | Catch runtime and interaction failures that do not surface in `preview`. | `SKILL.md` + GUI playbook + public beta tool | high |
| `miniapp-center-hub-refactor` | Reorganize a growing miniapp into a clearer hub with stable section ownership. | `SKILL.md` + hub playbook | medium |
| `miniapp-user-facing-copy-trim` | Shorten verbose miniapp copy into clearer action-first UI text. | `SKILL.md` + copy-trim playbook | medium |

## Platform Compatibility

All skills support both Codex and Claude Code:

- **Codex**: Reads `name` and `description` from SKILL.md, uses `agents/openai.yaml` for platform config
- **Claude Code**: Reads all SKILL.md fields including optional `tools` and `slash_command`

### Slash Commands

Each skill can be triggered manually in Claude Code using its slash command:

| Skill | Slash Command |
|-------|---------------|
| `miniapp-official-scaffold-alignment` | `/miniapp-official-scaffold-alignment` |
| `miniapp-devtools-recovery` | `/miniapp-devtools-recovery` |
| `miniapp-devtools-cli-repair` | `/miniapp-devtools-cli-repair` |
| `miniapp-devtools-gui-check` | `/miniapp-devtools-gui-check` |
| `miniapp-center-hub-refactor` | `/miniapp-center-hub-refactor` |
| `miniapp-user-facing-copy-trim` | `/miniapp-user-facing-copy-trim` |

## Planned Skills

These are promising, but still more product-bound than the current public batch:

| Skill | Purpose | Reason Not Included Yet |
| --- | --- | --- |
| `miniprogram-local-backend-bridge` | Connect a miniapp to a local backend with fallback behavior. | still tied to local backend contract and app runtime choices |
| `miniapp-design-system-evolution` | Evolve a reusable miniapp design system. | still depends on repo-specific visual case studies |
| `miniprogram-task-center-scaffold` | Build a writable task center with refresh flow. | still bound to one app's data model and page contracts |

## Criteria For Promotion To Public

- The skill can be understood without one source repo's context.
- The skill avoids absolute paths, app-specific storage keys, and private route names in the core instructions.
- The skill has a stable trigger description.
- The skill has at least one reference file that explains the workflow in reusable terms.
- The skill can survive forward-testing on a different miniapp repo.
