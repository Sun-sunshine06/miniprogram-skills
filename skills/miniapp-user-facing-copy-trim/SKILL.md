---
name: miniapp-user-facing-copy-trim
description: Simplify on-page WeChat Mini Program copy so main surfaces become shorter, more action-first, and more user-facing. Use when Codex needs to trim verbose labels, mixed implementation detail, over-explained settings, or long empty-state and status text without changing the underlying business flow.
---

# Miniapp User Facing Copy Trim

## Overview

Use this skill when the structure and interaction model are mostly acceptable, but the page sounds like internal documentation instead of a product surface. The goal is to keep only the copy users need in the moment.

## Quick Start

1. Read `references/copy-trim-playbook.md`.
2. Inventory the longest labels, subtitles, empty states, banners, and toasts on the target surfaces.
3. Classify each text block as keep, shorten, move, or delete.
4. Replace explanation-heavy paragraphs with concise labels, summaries, and status text.
5. If the real blocker is page ownership or navigation, use `miniapp-center-hub-refactor` instead.

## Core Rules

- Main surfaces should answer:
  - what can I do here
  - what is the current state
  - what is blocking me
- Prefer one strong label plus one short supporting line over a paragraph.
- Remove implementation detail from user copy unless the user must act on it directly.
- Keep terminology consistent across page titles, section labels, buttons, banners, and toasts.
- Prefer concrete verbs over abstract management nouns.
- Keep mixed-language copy intentional:
  - preserve proper nouns or official platform names when needed
  - avoid mixing two languages inside the same short label unless the product requires it
- Move maintainer explanation, technical caveats, and long rationale into docs, help surfaces, or detailed pages.
- Validate copy at small-surface level: tab text, title, button, chip, empty state, error banner, and toast.

## Output Format

1. high-friction copy to cut
2. replacement labels and summaries
3. what to move out of the page
4. copy validation pass

## Resources

- `references/copy-trim-playbook.md`: rewrite patterns, bilingual guidance, and review checklist
- `references/example-prompts.md`: reusable trigger and non-trigger prompts
