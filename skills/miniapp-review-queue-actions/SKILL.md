---
name: miniapp-review-queue-actions
description: Design or refactor a WeChat Mini Program review, pending, inbox, approval, or candidate queue so common actions happen directly on list cards instead of forcing a detail-page detour. Use when Codex needs to define queue states, card-level primary and secondary actions, confirm dangerous actions, or set the refresh chain after a queue mutation.
---

# Miniapp Review Queue Actions

## Overview

Use this skill when users are spending too many taps just to perform common queue actions. The goal is to make the queue itself actionable while still preserving a detailed page for richer context when needed.

## Quick Start

1. Read `references/queue-actions-playbook.md`.
2. List the queue states and the top one to three actions users perform most often.
3. Keep one primary action per state and treat destructive actions explicitly.
4. Define the mutation and refresh chain in the service layer before changing button layout.
5. If the request is really about top-level navigation, use `miniapp-center-hub-refactor` instead.

## Core Rules

- Let each queue state expose one primary action and a small set of secondary actions.
- Keep card tap for detail or context, but do not require it for the most frequent actions.
- Keep mutation logic in a service or page method layer; the card surface should dispatch intent, not invent business state.
- Prevent action taps from also triggering card navigation.
- Show enough context on the card to support action confidence:
  - status badge
  - short reason or classification
  - latest update or receive time
  - short content preview when useful
- Use loading or acting state per item so users know which card is mutating.
- Keep the refresh order stable:
  - mutate queue state
  - run any downstream recalculation only if needed
  - reload the queue snapshot
  - show toast or inline status
- Dangerous or irreversible actions need clear labeling and, when appropriate, confirmation.

## Output Format

1. queue states and actions
2. card interaction contract
3. refresh and side-effect chain
4. files or components to change first

## Resources

- `references/queue-actions-playbook.md`: state matrix, action surface, and refresh-chain guidance
- `references/example-prompts.md`: reusable trigger and non-trigger prompts
