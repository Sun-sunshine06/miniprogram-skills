# Conventions

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
- Keep `agents/openai.yaml` aligned with `SKILL.md`.
- Forward-test on realistic prompts before calling a skill public-ready.

## Non-Goals

- Do not turn this repo into a full miniapp template app.
- Do not mix product roadmaps with reusable skill content.
- Do not keep undocumented project-local assumptions in public skill files.
