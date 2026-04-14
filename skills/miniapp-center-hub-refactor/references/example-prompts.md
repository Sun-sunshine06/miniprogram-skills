# Example Prompts

Use these prompts to validate whether the skill routes to architecture work instead of copy-only or card-level interaction work.

## Prompt 1

**User prompt**

```text
This miniapp started with `home / tasks / profile`, but now inbox work, integrations, and settings are scattered across too many tabs. Refactor the top-level information architecture into a clearer center without turning everything into one long page.
```

**Expected answer structure**

1. current navigation problem
2. proposed hub structure
3. page ownership and migration map
4. migration order

**Evaluation notes**

- The answer should focus on top-level ownership and internal hub sections.
- The answer should keep detailed pages when they still have real flow value.
- The answer should not collapse into copy editing only.

## Prompt 2

**User prompt**

```text
Users cannot tell where to process pending items versus where to change reminders and connections. Redesign the navigation so both live under one obvious hub, but keep the detailed pages independent.
```

**Expected answer structure**

1. current navigation problem
2. proposed hub structure
3. page ownership and migration map
4. migration order

**Evaluation notes**

- The answer should explicitly separate high-frequency handling from low-frequency settings.
- The answer should present a migration map from old entries to new destinations.

## Do Not Use This Skill When

```text
The structure is fine, but page titles, banners, and button text still read like internal documentation. Keep the navigation and trim the on-page copy instead.
```

Use `miniapp-user-facing-copy-trim` instead, because the blocker is on-page wording rather than top-level navigation.
