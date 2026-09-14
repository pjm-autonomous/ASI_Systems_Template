---
artifact-type: data-specification
tier: system
---

# Data Specifications

- [What belongs here](#what-belongs-here)
- [One file per entity](#one-file-per-entity)
- [Ownership](#ownership)
- [Relationship to interfaces](#relationship-to-interfaces)
- [Retention and compliance](#retention-and-compliance)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `system/data/data-<description>.md`, optionally grouped into a
feature-bucket directory. Start from `templates/data-specification.md`.

Data specifications are valid at the **system** and **subsystem** tiers. An
entity no other subsystem can see belongs at `subsystem/data/`.

## What belongs here

A data specification defines **one entity**: its schema (fields, types,
constraints), its relationships to other entities, its lifecycle (create, update,
delete rules), its storage and retention policy, and its validation rules.

A data specification carries **no parent requirement**. It is a definition that
several requirements and interfaces refer to, not a decomposition of any one of
them — the same reasoning that leaves architecture without a parent. Relate it
through the entities it names and the interfaces that carry it.

## One file per entity

One file per entity, not one per feature. If a feature introduces three related
entities, that is three `data-*.md` files, cross-referenced from each other's
Relationships section.

The test is whether the two things have independent lifecycles. Two entities
always created and deleted together are usually one entity with a nested
structure.

## Ownership

Every data specification names an owner — **the single component that is the source of truth** for that entity.

If two components both claim ownership of the same conceptual entity, that is a
design problem, not a documentation problem. Resolve it in an ADR
(`<tier>/decisions/`) rather than by picking one arbitrarily here. A data
specification that records a contested ownership as settled makes the conflict
harder to find later, not easier.

## Relationship to interfaces

A data specification usually exists because an interface carries the entity, or a
requirement makes it stateful.

Keep the schema here and **reference** it from the interface's Data Schema
section rather than restating it. Two copies of a schema drift, and the interface
copy is the one consumers build against — so the drift surfaces as a production
incompatibility rather than a documentation inconsistency.

## Retention and compliance

Where a project has data-retention, privacy or export-control obligations, the
Storage and Retention section is where they become **concrete per entity**, not a
general policy statement filed elsewhere.

Cross-reference `extensions/qa-cm/configuration-management-plan.md` once
authored, if retention ties into configuration baselines.

## Maturity

Data specifications start at `M1`. A state at or above `M2` requires a dated
promotion record in `_registry/` — see
[`standard/decisions.md`](../../standard/decisions.md) D-40 … D-43.
