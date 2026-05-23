# Claude Code Adapter Design

Date: 2026-05-24

## Overview

This document describes the design for adapting miniprogram-skills to support both Codex and Claude Code in a single repository using dual-compatible YAML frontmatter.

## Current State

### Codex Format

Each skill currently has:
- `SKILL.md` with YAML frontmatter (`name`, `description`)
- `agents/openai.yaml` for Codex-specific configuration
- `references/` directory with supporting documents

Example `SKILL.md` frontmatter:
```yaml
---
name: miniapp-devtools-recovery
description: Recover a WeChat Mini Program repository...
---
```

Example `agents/openai.yaml`:
```yaml
interface:
  display_name: "Miniapp DevTools Recovery"
  short_description: "Recover a WeChat miniapp after import or template drift."
  default_prompt: "Use $miniapp-devtools-recovery to repair WeChat DevTools..."
```

### Target State

Support both Codex and Claude Code without breaking existing functionality.

## Design Decisions

### Decision 1: Minimal Frontmatter Extension

**Choice**: Extend existing `SKILL.md` frontmatter with optional fields

**Rationale**:
- Minimal changes to existing files
- Forward compatible with existing Codex users
- Single source of truth for skill metadata

### Decision 2: Standard YAML Format

**Choice**: Use standard YAML with underscore naming convention

**Rationale**:
- Consistent with existing `name` and `description` fields
- Easy to parse for both platforms
- No special syntax required

### Decision 3: Optional Tools Field

**Choice**: `tools` field is optional

**Rationale**:
- Not all skills need explicit tool references
- Claude Code can use default tool set when not specified
- Reduces boilerplate for simple skills

### Decision 4: Skill Name as Slash Command

**Choice**: Use full skill name for slash command (e.g., `/miniapp-devtools-recovery`)

**Rationale**:
- Consistent with skill naming convention
- Avoids namespace conflicts
- Self-documenting

## Proposed Format

### YAML Frontmatter

```yaml
---
name: miniapp-devtools-recovery
description: Recover a WeChat Mini Program repository after wrong-root import, DevTools template residue, stale compile conditions, or TypeScript-recognition drift. Use when Codex needs to restore the intended repo shape, remove generated clutter, or tell the user exactly what to fix inside DevTools.
tools:
  - Bash
  - Read
  - Edit
  - Glob
  - Grep
slash_command: /miniapp-devtools-recovery
---
```

### Field Specification

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Skill identifier, lowercase with hyphens |
| `description` | Yes | string | Skill description for auto-trigger detection |
| `tools` | No | list[string] | Claude Code tools available to this skill |
| `slash_command` | No | string | Manual trigger command, format: `/skill-name` |

### Platform Behavior

#### Codex
- Reads `name` and `description` from `SKILL.md`
- Ignores `tools` and `slash_command` fields
- Continues using `agents/openai.yaml` for platform-specific config

#### Claude Code
- Reads all fields from `SKILL.md`
- Uses `description` for auto-trigger detection
- Uses `tools` to limit available tools (if specified)
- Registers `slash_command` for manual triggering

## Implementation Plan

### Phase 1: Update SKILL.md Files

For each of the 6 skills, add optional fields to YAML frontmatter:

1. `miniapp-official-scaffold-alignment`
2. `miniapp-devtools-recovery`
3. `miniapp-devtools-cli-repair`
4. `miniapp-devtools-gui-check`
5. `miniapp-center-hub-refactor`
6. `miniapp-user-facing-copy-trim`

### Phase 2: Documentation

Update documentation to explain:
- Dual-compatible format
- How Codex reads the skills
- How Claude Code reads the skills
- How to add new skills

### Phase 3: Validation

- Verify existing Codex functionality unchanged
- Test Claude Code skill loading
- Validate slash command registration

## Backward Compatibility

- Existing `agents/openai.yaml` files remain unchanged
- Codex continues to work without modification
- New fields are optional, so existing SKILL.md files without them still work

## Future Considerations

- If Claude Code adoption grows, consider adding `agents/claude.yaml` for platform-specific config
- Monitor for conflicts between Codex and Claude Code tool requirements
- Consider adding `auto_trigger` boolean field if default behavior needs override
