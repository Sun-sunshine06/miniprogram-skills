# v0.4.0 Draft Release Notes

## Summary

`v0.4.0` is the first release candidate that treats public skill boundaries as machine-readable repository assets instead of only human-written docs.

The main changes are a committed skill catalog, a replayable routing-eval prompt pack, dedicated validators for both, and an initial routing evidence log that records the current review status honestly as curated maintainer replay notes while live installed-skill transcripts are still pending.

## What Improved For Skill Consumers

- the four public skills now have one machine-readable catalog entry each in `manifests/skill-catalog.json`
- host requirements such as official CLI dependence, GUI automation, and user-supplied `miniprogram-automator` are now explicit repo-owned data instead of only prose
- adjacent routing priorities such as GUI-over-CLI and scaffold-over-recovery are now committed review surface rather than implied maintainer knowledge
- the routing prompt pack under `evals/routing/` makes the intended skill boundaries replayable without reconstructing prompts from roadmap prose

## What Improved For Contributors

- shared validation now checks skill structure, docs hygiene, repo JSON, routing fixtures, and catalog consistency in one flow
- `docs/routing-eval-log.md` gives reviewers a single place to compare prompt fixtures, intended routing, and the current strength of the recorded evidence
- the review checklist and conventions now explicitly require catalog and routing-fixture updates when public skill boundaries move
- `docs/public-roadmap.md` now separates the catalog-and-routing baseline from the later transcript-heavy maturity step

## What This Release Still Does Not Claim

- it does not claim that live installed-skill routing has already been proven across all four public skills
- it does not claim that collaborator-host routing evidence is complete
- it does not change the GUI harness status from beta
- it does not remove the current user-supplied `miniprogram-automator` runtime model for live GUI automation

## Recommended Release Framing

Describe `v0.4.0` as:

- a machine-readable public-boundary release for the four extracted miniapp skills
- a contributor-facing hardening release that makes routing expectations replayable and reviewable
- an evidence-structuring release, not the final live-transcript proof point
- a release that keeps the GUI tool beta while making its surrounding skill-selection story clearer

## Suggested Release Notes Copy

`miniprogram_skills v0.4.0` turns the repository's public skill boundary into committed, validated assets. The release adds a machine-readable skill catalog, a replayable routing-eval prompt pack, dedicated validators for both, and an initial routing log that records current outcomes honestly as curated maintainer replay notes while live transcript-backed evidence is still being gathered. The four public skills keep the same scope, the GUI harness remains beta, and the next maturity step is to replace these initial notes with installed-skill or replayable transcript evidence plus broader collaborator-host validation.
