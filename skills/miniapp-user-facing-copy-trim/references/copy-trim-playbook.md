# User Facing Copy Trim Playbook

## Copy Triage

For each text block, decide whether it should be:

- kept as-is
- shortened
- moved to a lower-emphasis help surface
- deleted entirely

Good candidates for trimming:

- section subtitles that repeat the title
- empty states that explain implementation instead of next action
- settings rows that contain long backend or integration rationale
- banners that repeat information already visible in chips or badges

## Rewrite Patterns

Prefer these conversions:

- paragraph -> title + short summary
- management noun -> action verb
- implementation phrase -> user-facing state phrase
- repeated warning text -> one concise blocker line

Examples of better direction:

- "connection management" -> "connect account"
- "manual import entry" -> "import manually"
- "synchronization status configuration" -> "sync status"

## Bilingual Guidance

- Keep official product or platform names when users will see them elsewhere.
- Choose one primary language for a short label whenever possible.
- Use a second language only when it improves recognition instead of adding noise.
- Keep English technical nouns out of the main page unless they are part of the user's actual task.

## Surface Checklist

Run the review across these surfaces:

- tab text
- page title
- section label
- button
- status chip
- empty state
- error banner
- toast

## Anti-Patterns

- using the page as a maintainer manual
- repeating the same explanation in subtitle, row detail, and banner text
- exposing backend, storage, or implementation words that the user cannot act on
- shortening copy so aggressively that the current state becomes ambiguous
