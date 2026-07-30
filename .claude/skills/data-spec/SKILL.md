---
name: data-spec
description: Create or update a data specification in system/data/<feature>/. Use when the user wants to define an entity, schema, ownership, lifecycle, or retention policy.
---

# Skill: data-spec

Create or update a data specification artifact in `system/data/<feature>/`.

A data specification defines one entity (or a tightly coupled group of entities): its schema, who owns the source of truth, its relationships, and its lifecycle/retention rules.

## Create flow

Ask the user for:

- Spec title (short description for the filename, usually named after the entity, e.g. `dock-reservation-schema`)
- Parent product requirement filename (e.g. `req-autonomous-return-to-dock.md`) — **required**; must exist under `product/requirements/` (if not, direct the user to `/product-requirement` first)
- Owner — the component/subsystem that is the source of truth for this entity
- A brief description of the entity and its key fields, if known

Locate the parent product requirement under `product/requirements/`. The feature bucket is the directory the parent lives in — reuse it for the new spec. If the parent cannot be located, ask the user for the correct filename rather than guessing.

Then:

1. Create `system/data/<feature>/data-<short-description>.md` from `templates/data-specification.md`. Create the feature directory if it doesn't exist.
2. Populate YAML frontmatter:
   - `id`: filename without the `.md` extension
   - `title`: human-readable title
   - `parent-product-requirement`: parent filename including `.md`, no directory path
3. Fill the plain Markdown table rows: **Owner (source of truth)**, **Parent Product Requirement**
4. Fill the sections — `TBD` for anything unknown rather than deleting the heading:
   - **Entity Definition** — what the entity represents, in a sentence or two
   - **Schema** — plain Markdown table with Field / Type / Constraints / Description columns
   - **Relationships** — links to other entities (reference other `data-*.md` filenames where they exist)
   - **Lifecycle** — create / update / delete rules
   - **Storage & Retention** — storage type (cache/db/blob/ledger/etc.), retention and archival policy
   - **Validation Rules** — invariants beyond per-field constraints
5. Update `traceability/TRACEABILITY.md`: fill the Data Spec cell on the row containing the parent product requirement. Link relative to `traceability/`: `[data-<name>.md](../system/data/<feature>/data-<name>.md)`. If the requirement has multiple data specs, duplicate the row.

Finish by running `python tools/validate.py` from the repo root and fixing anything it reports.

## Update flow

If the data spec already exists:

1. Locate it under `system/data/` and read it
2. Ask the user what needs to change
3. Apply only the requested changes — do not regenerate the whole file
4. Re-run `python tools/validate.py`

## Conventions

- Filename: `data-<short-description>.md` in kebab-case
- Tables are plain Markdown, never HTML `<table>` markup
- Examples: `data-geofence-zone-schema.md`, `data-dock-reservation-schema.md`
