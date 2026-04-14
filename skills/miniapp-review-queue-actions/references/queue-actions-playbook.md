# Review Queue Actions Playbook

## State And Action Matrix

Define queue states first. For each state, capture:

- entry condition
- primary action
- secondary actions
- whether confirmation is required
- whether a downstream recalculation or sync should run

Typical state examples:

- needs review
- ready to import or approve
- update acknowledged but not synced
- ignored or dismissed

## Card Contract

A useful queue card usually contains:

- short title
- state badge
- short secondary line, such as type or timestamp
- optional reason or classification note
- optional preview body
- action row

Keep the contract stable:

- card tap opens detail or fuller context
- action buttons perform direct mutations
- loading state is item-scoped
- dangerous actions are visually distinct

## Refresh Chain

Recommended sequence after a card action:

1. mark the item as acting
2. call the queue mutation
3. run downstream recomputation only when the product requires it
4. reload queue data from the source of truth
5. clear the acting state
6. surface a toast, banner, or inline result

If the mutation fails:

- clear the acting state
- keep the user on the same queue
- surface a short actionable error

## Anti-Patterns

- forcing a detail-page detour for every approval or import
- letting button taps also trigger card navigation
- putting too many equal-weight actions on one card
- hiding irreversible actions behind vague labels
- duplicating mutation logic across several queue pages
