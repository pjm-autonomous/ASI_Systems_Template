---
name: requirement
description: EARS requirement formatter — converts a plain-language behavior description into a properly formatted EARS statement. Utility only; creates no files.
---

# Skill: requirement

EARS Requirement Formatter — converts plain-language behavior descriptions into properly formatted EARS requirement statements. Does not create files; to author a requirement artifact, use `/product-requirement` or `/system-requirement` (both apply these same rules).

## Instructions

When invoked:

1. Ask the user for a plain-language description of what the system must do (or use the description they already provided).
2. Identify the appropriate EARS keyword:
   - **When** — event-driven response (`When <trigger>, the system shall <response>.`)
   - **While** — state-driven behavior (`While <state>, the system shall <behavior>.`)
   - **If** — conditional action (`If <condition>, the system shall <action>.`)
   - **Where** — feature inclusion (`Where <feature is included>, the system shall <capability>.`)
   - Ubiquitous (no keyword) — an unconditional property (`The system shall <capability>.`)
3. Output a formatted EARS statement.
4. If the trigger type is ambiguous, ask the user which keyword fits best before formatting.
5. If the description bundles several behaviors, propose splitting it into one EARS statement per behavior.
6. If the user wants to revise, iterate on the statement until they are satisfied.

## Quality checks

Flag (and offer to fix) these while formatting:

- Vague verbs — "handle", "support", "manage", "process" without a measurable outcome
- Unbounded quantities — "quickly", "reliably", "as needed" instead of numbers with units
- Hidden compound requirements — "and" joining two independently testable behaviors
- Passive voice hiding the responsible component — say which part of the system shall act

## Output format

Present the EARS statement as a plain quoted block — no file is created.

## EARS format reference

| Keyword | Pattern | Use when |
|---|---|---|
| When | `When <trigger>, the system shall <response>.` | A discrete event occurs |
| While | `While <state>, the system shall <behavior>.` | A continuous state holds |
| If | `If <condition>, the system shall <action>.` | A condition may or may not be true |
| Where | `Where <feature is included>, the system shall <capability>.` | A feature is optionally present |
| (none) | `The system shall <capability>.` | The behavior is unconditional |
