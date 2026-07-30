---
name: product-requirement
description: Create or update a product requirement in product/requirements/<feature>/, enforcing EARS format and a parent use case. Use when the user wants to capture a stakeholder-facing obligation.
---

# Skill: product-requirement

Create or update a product requirement artifact in `product/requirements/<feature>/`.

## Create flow

Ask the user for:

- Requirement title (short description for the filename)
- Parent use case filename(s) (e.g. `uc-geofence-breach-alert.md`) — **required**, one or more; each must exist under `product/use-cases/` (if not, direct the user to `/use-case` first)
- Priority — `Critical`, `High`, `Medium`, or `Low`
- A brief description of what the system must do

Locate each parent use case under `product/use-cases/`. The feature bucket is the directory the parent lives in — reuse it for a single-parent requirement. If the requirement has multiple parent use cases from different buckets, place it in a shared bucket (e.g. `<domain>-common/`) rather than under any single parent's bucket. If a parent cannot be located, ask the user for the correct filename rather than guessing.

Then:

1. Format the description as an EARS statement (reference below). If it doesn't fit any EARS pattern cleanly, iterate with the user via the `/requirement` utility rules before writing the file.
2. Create `product/requirements/<feature>/req-<short-description>.md` from `templates/product-requirement.md`. Create the feature directory if it doesn't exist.
3. Populate YAML frontmatter:
   - `id`: filename without the `.md` extension
   - `title`: human-readable title
   - `parent-use-cases`: YAML list of parent use case filenames including `.md`, no directory path (singleton list is fine)
   - `priority`: as provided
4. Fill the plain Markdown table rows: **ID**, **Parent Use Cases** (comma-separated filenames), **Priority**
5. Fill the sections:
   - **Requirement Statement** — the EARS-formatted statement
   - **Rationale** — `TBD` if unknown
   - **Acceptance Criteria** — `TBD` if unknown
6. Update `traceability/TRACEABILITY.md`: for each parent use case, fill the Product Requirement cell on the row containing that use case, or append a new row. Link relative to `traceability/`: `[req-<name>.md](../product/requirements/<feature>/req-<name>.md)`. A multi-parent requirement appears on multiple rows.

Finish by running `python tools/validate.py` from the repo root and fixing anything it reports.

## Update flow

If the requirement already exists:

1. Locate it under `product/requirements/` and read it
2. Ask the user what needs to change
3. Apply only the requested changes — do not regenerate the whole file
4. If the Requirement Statement changed, verify it is still valid EARS format
5. Re-run `python tools/validate.py`

## EARS format reference

| Keyword | Pattern | Use when |
|---|---|---|
| When | `When <trigger>, the system shall <response>.` | A discrete event occurs |
| While | `While <state>, the system shall <behavior>.` | A continuous state holds |
| If | `If <condition>, the system shall <action>.` | A condition may or may not be true |
| Where | `Where <feature is included>, the system shall <capability>.` | A feature is optionally present |

## Conventions

- Filename: `req-<short-description>.md` in kebab-case
- Tables are plain Markdown, never HTML `<table>` markup
- Examples: `req-geofence-alert-latency.md`, `req-autonomous-return-to-dock.md`, `req-all-stop.md`
