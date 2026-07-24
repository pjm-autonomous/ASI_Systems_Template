# Data Specifications

Grouped by feature bucket: `system/data/<feature>/data-<description>.md`. Start from `templates/data-specification.md`. See `example/system/data/low-battery-return-to-dock/data-dock-reservation-schema.md` for a worked sample.

## What Belongs Here

A data specification defines one entity: its schema (fields, types, constraints), relationships to other entities, lifecycle (create/update/delete rules), storage/retention policy, and validation rules. It traces up to a `parent-product-requirement` — usually the same one a related ICD or system requirement traces to, since a data spec typically exists to back an interface or a stateful behavior.

One file per entity, not one file per feature bucket — if a feature bucket introduces three related entities, that's three `data-*.md` files, cross-referenced from each other's "Relationships" section.

## Ownership

Every data specification names an owner — the single component that is the source of truth for that entity (the "Owner (source of truth)" table row). If two components both claim ownership of the same conceptual entity, that's a design problem worth an ADR (`system/decisions/`), not something to resolve by picking one arbitrarily in the data spec.

## Retention and Compliance

If a project has data-retention, privacy, or export-control obligations, the "Storage & Retention" section is where those get made concrete per entity — not left as a general policy statement elsewhere. Cross-reference `extensions/qa-cm/configuration-management-plan.md` once authored if retention ties into configuration baselines.
