# Example Prompts

Use these prompts to validate whether the skill routes to actionable queue design instead of top-level architecture or copy-only cleanup.

## Prompt 1

**User prompt**

```text
This pending queue makes users open a detail page for every item just to approve, ignore, or import it. Redesign the queue cards so common actions happen in place and refresh safely afterward.
```

**Expected answer structure**

1. queue states and actions
2. card interaction contract
3. refresh and side-effect chain
4. files or components to change first

**Evaluation notes**

- The answer should move common actions onto the list card.
- The answer should define a stable refresh chain after mutation.
- The answer should not widen into a full navigation rewrite.

## Prompt 2

**User prompt**

```text
I already have a queue page, but every state invents different buttons and the card tap keeps colliding with inline actions. Standardize the action surface and the mutation flow.
```

**Expected answer structure**

1. queue states and actions
2. card interaction contract
3. refresh and side-effect chain
4. files or components to change first

**Evaluation notes**

- The answer should normalize state-specific actions instead of adding more ad hoc buttons.
- The answer should clearly separate card navigation from inline mutation.

## Do Not Use This Skill When

```text
The queue actions are acceptable, but the page reads like internal documentation. I mainly want shorter labels, shorter empty states, and more user-facing copy.
```

Use `miniapp-user-facing-copy-trim` instead, because the interaction model is acceptable and the main problem is on-page wording.
