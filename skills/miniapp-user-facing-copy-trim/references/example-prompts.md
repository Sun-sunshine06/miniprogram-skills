# Example Prompts

Use these prompts to validate whether the skill routes to copy simplification instead of architecture or queue-action work.

## Prompt 1

**User prompt**

```text
The miniapp pages read like internal documentation. Trim the on-page text, keep only action-first labels and short status summaries, and move implementation-heavy explanation out of the main surfaces.
```

**Expected answer structure**

1. high-friction copy to cut
2. replacement labels and summaries
3. what to move out of the page
4. copy validation pass

**Evaluation notes**

- The answer should simplify wording without inventing an unrelated layout rewrite.
- The answer should explicitly separate what stays on-page from what moves elsewhere.

## Prompt 2

**User prompt**

```text
The navigation is acceptable, but the settings page is full of long sentences, mixed Chinese and English labels, and implementation-heavy warnings. Rewrite the copy so the page feels shorter and clearer.
```

**Expected answer structure**

1. high-friction copy to cut
2. replacement labels and summaries
3. what to move out of the page
4. copy validation pass

**Evaluation notes**

- The answer should improve wording at label, banner, and empty-state level.
- The answer should not turn into a full information-architecture refactor.

## Do Not Use This Skill When

```text
The labels are fine, but users still do not know where inbox work lives versus where reminders and integrations live. I need a hub redesign, not just shorter text.
```

Use `miniapp-center-hub-refactor` instead, because the blocker is navigation ownership rather than page copy.
