---
name: miniapp-center-hub-refactor
description: Refactor a growing WeChat Mini Program whose top-level navigation has become scattered across tabs such as home, profile, inbox, integrations, or settings into a clearer hub or center structure. Use when Codex needs to regroup top-level tabs, separate high-frequency action flows from low-frequency settings, define internal hub sections, or migrate detailed pages without collapsing everything into one long page.
---

# Miniapp Center Hub Refactor

## Overview

Use this skill when the real problem is information architecture, not just styling or labels. Reach for it when users no longer know where to handle pending work, where to manage settings, or which tab owns integrations and personal state.

## Quick Start

1. Read `references/center-hub-playbook.md`.
2. Audit the current top-level tabs, repeated entry points, and detailed pages before moving any routes.
3. Separate high-frequency action flow from low-frequency settings flow.
4. Keep the hub as an aggregator and keep detailed pages for flows that still need their own state, forms, or validation.
5. If the request is only about shortening page text, use `miniapp-user-facing-copy-trim` instead.

## Core Rules

- Start from user questions, not from the current file tree:
  - what do I need to handle now
  - where do I manage settings or integrations
- Reduce top-level tabs only when the replacement entry remains obvious.
- Give the hub internal sections with stable ownership, such as `inbox`, `settings`, or `status`, instead of turning the hub into one unstructured long page.
- Promote summaries and next actions on the hub; demote long explanation and rarely used detail.
- Keep detailed pages when the flow has its own form state, validation, filters, or multi-step interaction.
- Move pages by ownership, not by which old page linked to them.
- Define a migration map from old entry point to new hub location before deleting or hiding old navigation.
- Update top-level navigation, route docs, and smoke checks together so structure changes stay reviewable.

## Output Format

1. current navigation problem
2. proposed hub structure
3. page ownership and migration map
4. migration order

## Resources

- `references/center-hub-playbook.md`: audit checklist, section design rules, and migration guidance
- `references/example-prompts.md`: reusable trigger and non-trigger prompts
