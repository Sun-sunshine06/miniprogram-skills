# Center Hub Playbook

## Problem Signals

Consider a hub refactor when several of these appear together:

- users must remember multiple unrelated tabs to finish one workflow
- a former `profile` or `me` page has turned into a navigation dumping ground
- pending work and settings are both important, but neither has a clear home
- integrations, reminders, and personal state all compete for top-level space
- the same destination is linked from several tabs because ownership is unclear

## Audit Before Moving Routes

Build a simple audit table before changing navigation:

- current entry point
- user intent
- usage frequency
- whether the flow needs a detailed page
- likely future owner inside the hub

Useful ownership buckets:

- pending or review work
- integrations or data sources
- reminders or notifications
- personal settings or preferences
- service status or environment state

## Hub Structure Pattern

The hub should answer two questions quickly:

1. what needs attention now
2. where do I manage supporting settings

Recommended pattern:

- keep the hub as one top-level tab
- give it internal sections or tabs with explicit ownership
- keep summaries on the hub
- keep detailed pages behind the summary rows

Good examples of hub-owned summaries:

- pending count
- unread or unreviewed count
- connection status
- reminder status
- service mode or sync status

## Migration Checklist

1. Freeze the new top-level tab list.
2. Decide the hub name and its internal sections.
3. Map every old top-level destination to:
   - stays top-level
   - moves into hub summary
   - survives as detailed child page
4. Update deep links and button destinations.
5. Keep old detailed pages alive until the new hub navigation is proven.
6. Update route docs, smoke checks, and screenshots after the move.

## Anti-Patterns

- replacing many tabs with one huge undifferentiated page
- mixing high-frequency handling and low-frequency settings in one scrolling block without section boundaries
- deleting detailed pages just because the hub now exists
- moving routes based on component reuse instead of user ownership
- using the hub to hide problems that really need clearer state or copy
