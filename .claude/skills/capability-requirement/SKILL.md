---
name: capability-requirement
description: Create or update a capability requirement in product/requirements/<feature>/, enforcing EARS format and a parent use case. Use when the user wants to capture a stakeholder-facing obligation.
---

# Skill: capability-requirement

Create or update a capability requirement artifact in `product/requirements/<feature>/`.

## Create flow

Ask the user for:

- Requirement title (short description for the filename)
- Parent use case filename(s) (e.g. `uc-geofence-breach-alert.md`) — **required**, one or more; each must exist under `stakeholder/use-cases/` (if not, direct the user to `/use-case` first)
- Priority — the authoritative values are the `priority` enum in
  `standard/artifact-schema.yaml` (MoSCoW). Do not offer a value list from
  memory; read the schema.
- A brief description of what the system must do

Locate each parent use case under `stakeholder/use-cases/`. The feature bucket is the directory the parent lives in — reuse it for a single-parent requirement. If the requirement has multiple parent use cases from different buckets, place it in a shared bucket (e.g. `<domain>-common/`) rather than under any single parent's bucket. If a parent cannot be located, ask the user for the correct filename rather than guessing.

Then:

1. Format the description as an EARS statement (reference below). If it doesn't fit any EARS pattern cleanly, iterate with the user via the `/requirement` utility rules before writing the file.
2. Create `product/requirements/<feature>/capreq-<short-description>.md` from `templates/capability-requirement.md`. Create the feature directory if it doesn't exist.
3. Populate YAML frontmatter:
   - `id`: filename without the `.md` extension
   - `title`: human-readable title
   - `parent-product-requirements`: YAML list of parent **product requirement**
     filenames including `.md`, no directory path. These live in the **L0 repo** —
     the reference is shape-checked locally and verified upstream against that
     repo's published `artifact-index.json`, so it cannot be confirmed here (singleton list is fine)
   - `priority`: as provided
4. Fill the plain Markdown table rows: **ID**, **Parent Use Cases** (comma-separated filenames), **Priority**
5. Fill the sections:
   - **Requirement Statement** — the EARS-formatted statement
   - **Rationale** — `TBD` if unknown
   - **Acceptance Criteria** — `TBD` if unknown
frontmatter (D-46). A skill writing rows into it reintroduces the hand
maintenance that produced a 316-row, 0-populated matrix. The parent
reference you set in frontmatter is what puts this artifact in the matrix.

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

- Filename: `capreq-<short-description>.md` in kebab-case
- Tables are plain Markdown, never HTML `<table>` markup
- Examples: `capreq-geofence-alert-latency.md`, `capreq-autonomous-return-to-dock.md`, `capreq-all-stop.md`
