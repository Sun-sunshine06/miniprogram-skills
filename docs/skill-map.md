# Skill Map

## Active Public Skills

| Skill | Purpose | Current Shape | Public Readiness |
| --- | --- | --- | --- |
| `miniapp-official-scaffold-alignment` | Validate scaffold correctness before feature work begins. | `SKILL.md` + baseline reference | medium |
| `miniapp-devtools-recovery` | Recover repos after wrong-root imports or DevTools template drift. | `SKILL.md` + recovery checklist | medium |
| `miniapp-devtools-cli-repair` | Use the official DevTools CLI as the primary diagnostic path. | `SKILL.md` + CLI playbook | high |
| `miniapp-devtools-gui-check` | Catch runtime and interaction failures that do not surface in `preview`. | `SKILL.md` + GUI playbook + public beta tool | high |

## Planned Skills

These are promising, but still more product-bound than the first public batch:

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
