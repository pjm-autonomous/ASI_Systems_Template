---
name: system-requirement
description: Create or update a system requirement in system/requirements/<feature>/, enforcing EARS format, a parent product requirement, and a component allocation.
---

# Skill: system-requirement

Create or update a system requirement artifact in `system/requirements/<feature>/`.

System requirements are the engineering decomposition of a product requirement — allocated to a component or subsystem, with measurable acceptance criteria. They use the same EARS format as product requirements but live under `system/` to keep the layers separated.

## Create flow

Ask the user for:

- Requirement title (short description for the filename)
- Parent product requirement filename (e.g. `req-geofence-alert-latency.md`) — **required**; must exist under `product/requirements/` (if not, direct the user to `/product-requirement` first)
- Parent use case filename(s) — optional; only if the system requirement also traces directly to use case(s)
- Allocation — the component or subsystem this requirement is assigned to (e.g. `geofence-service`, `safety-monitor`, `battery-manager`)
- Priority — `Critical`, `High`, `Medium`, or `Low`
- A brief description of what the component must do

Locate the parent product requirement under `product/requirements/`. The feature bucket is the directory the parent lives in — reuse it for the new system requirement. If the parent cannot be located, ask the user for the correct filename rather than guessing.

Then:

1. Format the description as an EARS statement (reference below).
2. Create `system/requirements/<feature>/sysreq-<short-description>.md` from `templates/system-requirement.md`. Create the feature directory if it doesn't exist.
3. Populate YAML frontmatter:
   - `id`: filename without the `.md` extension
   - `title`: human-readable title
   - `parent-product-requirement`: parent filename including `.md`, no directory path
   - `parent-use-cases`: YAML list of use case filenames if provided; **delete the field entirely if not applicable** — an empty list fails validation
   - `allocation`: component or subsystem
   - `priority`: as provided
4. Fill the plain Markdown table rows: **ID**, **Parent Product Requirement**, **Parent Use Cases** (comma-separated, or `n/a`), **Allocation**, **Priority**
5. Fill the sections:
   - **Requirement Statement** — the EARS-formatted statement, quantified where possible (thresholds, intervals, latencies)
   - **Rationale** — `TBD` if unknown
   - **Acceptance Criteria** — measurable; `TBD` if unknown
6. Update `traceability/TRACEABILITY.md`: fill the System Requirement cell on the row containing the parent product requirement. Link relative to `traceability/`: `[sysreq-<name>.md](../system/requirements/<feature>/sysreq-<name>.md)`. If the product requirement decomposes into multiple system requirements, duplicate the row per additional child.

Finish by running `python tools/validate.py` from the repo root and fixing anything it reports.

## Update flow

If the system requirement already exists:

1. Locate it under `system/requirements/` and read it
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

- Filename: `sysreq-<short-description>.md` in kebab-case
- Tables are plain Markdown, never HTML `<table>` markup
- Examples: `sysreq-geofence-check-interval.md`, `sysreq-battery-threshold-monitor.md`, `sysreq-dock-availability-check.md`
