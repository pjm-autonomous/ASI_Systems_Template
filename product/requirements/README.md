# Product Requirements

Grouped by feature bucket: `product/requirements/<feature>/req-<description>.md`. Start from `templates/product-requirement.md`. See `example/product/requirements/low-battery-return-to-dock/req-autonomous-return-to-dock.md` for a worked sample.

## What Belongs Here

A product requirement is a stakeholder-facing statement of what the system shall do to satisfy a use case — EARS-formatted, prioritized, with acceptance criteria. It traces up to `parent-use-cases` and down to system requirements, architecture diagrams, ICDs, and/or data specifications as needed (not every product requirement needs all four — a purely internal behavior might only need a system requirement, for instance).

Product requirements describe stakeholder-observable behavior — "when X happens, the system shall Y" — not implementation. If you're naming a specific component, service, or algorithm, that content probably belongs in a system requirement instead (`system/requirements/<feature>/`), which is where allocation to a component/subsystem happens.

## Priority Field

Every product requirement carries a `priority`: `Critical`, `High`, `Medium`, or `Low`. There is no separate "safety requirement" category in this template — a safety-bearing requirement is a normal product requirement with `priority: Critical`, cross-referenced from the relevant `extensions/safety/` document once that category is authored. See `reference/standards-framework.md` for the standards (ISO 26262, ISO 13849-1/IEC 62061, IEC 60204-1, ISO 21448/SOTIF, ISO 3691-4, ISO 10218) that typically drive `Critical` priority on an autonomous-systems project.

## EARS Format Reference

- **When**: `When <trigger>, the system shall <response>.`
- **While**: `While <state>, the system shall <behavior>.`
- **If**: `If <condition>, the system shall <action>.`
- **Where**: `Where <feature is included>, the system shall <capability>.`

`ISO/IEC/IEEE 29148` (see `reference/standards-framework.md`) is the standard behind why EARS-style phrasing matters — it's one way of satisfying that standard's "unambiguous and singular" requirement characteristics.
