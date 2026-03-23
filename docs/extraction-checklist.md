# Extraction Checklist

Use this checklist when moving content from a product repo into this public repository.

## Remove Tight Coupling

- replace absolute paths with placeholders
- replace product names when they are not required
- remove project-local storage keys from core instructions
- remove route names that only make sense in one app
- move source-repo baselines into examples or omit them

## Keep The Reusable Core

- keep workflow boundaries
- keep failure classifications
- keep safe auto-fix rules
- keep validation and reporting patterns
- keep the minimal command ladder

## Rewrite For Public Use

- explain when to use the skill in the YAML description
- explain what not to use the skill for
- prefer generic repo terms such as `repo root` and `miniapp code root`
- keep the body operational and concise

## Before Calling It Public-Ready

- validate the skill folder
- read the skill from scratch and check whether it still depends on hidden context
- confirm that a new reader could execute the workflow without the source repo
- record any remaining draft-only areas openly
