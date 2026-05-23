# Conventions

English | [中文](./conventions.zh-CN.md)

## Repository Goal

Write skills that can be used across multiple WeChat Mini Program repositories, not just one source project.

## Skill Folder Shape

Every public skill should keep this minimum structure:

```text
skill-name/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
`-- references/
```

## SKILL.md YAML Frontmatter

All SKILL.md files use YAML frontmatter with the following fields:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier, lowercase with hyphens |
| `description` | Yes | Skill description for auto-trigger detection |
| `tools` | No | Claude Code tools available to this skill |
| `slash_command` | No | Manual trigger command, format: `/skill-name` |

Example:

```yaml
---
name: my-skill
description: Description of when to use this skill.
tools:
  - Bash
  - Read
  - Edit
slash_command: /my-skill
---
```

Codex ignores `tools` and `slash_command` fields and continues using `agents/openai.yaml`.

## Writing Rules

- Keep `SKILL.md` short and procedural.
- Move detailed reasoning, checklists, and examples into `references/`.
- Use placeholders such as `<project-root>`, `<cli-path>`, and `<miniapp-root>` instead of absolute local paths.
- Keep repo-specific evidence out of the core skill body.
- Write the trigger conditions in the YAML `description`, not only in the markdown body.
- Prefer operational output formats over long narrative output formats.

## Publicization Rules

- Remove or replace product names that are not needed for the workflow.
- Remove storage keys unless they are part of the public contract.
- Replace specific route names with representative examples.
- Separate normative claims from repo-specific observations.
- Mark draft-only tools clearly when the harness has not been extracted yet.

## Validation Rules

- Run the skill validator on every skill folder after major edits.
- Keep `manifests/skill-catalog.json` aligned with the current public skill surface, host requirements, and evidence state.
- Keep `agents/openai.yaml` aligned with `SKILL.md`.
- Add or update the matching `evals/routing/` fixture coverage when a public skill boundary changes.
- Add or update the matching `evals/routing-replays/` transcript records when a committed routing fixture or output contract changes.
- Forward-test on realistic prompts before calling a skill public-ready.

## Non-Goals

- Do not turn this repo into a full miniapp template app.
- Do not mix product roadmaps with reusable skill content.
- Do not keep undocumented project-local assumptions in public skill files.
