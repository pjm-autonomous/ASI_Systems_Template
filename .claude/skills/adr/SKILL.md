---
name: adr
description: Create or update an architecture decision record in system/decisions/, auto-incrementing the adr-NNNN number. Use when a significant design choice needs its rationale recorded.
---

# Skill: adr

Create or update an architecture decision record (ADR) in `system/decisions/`.

ADRs are cross-cutting — they record why a significant design choice was made and can span multiple artifacts, so they are numbered sequentially rather than grouped into feature buckets, and they do not appear in the traceability matrix.

## Create flow

Ask the user for:

- Decision title (short description for the filename, e.g. `centralize-dock-reservation-in-fleet-service`)
- Status — `proposed` or `accepted` (new ADRs are never born `superseded`/`obsolete`)
- The context: what problem or decision point is being faced
- The options considered and the decision made, if already settled (a `proposed` ADR may have options but no decision yet)

Determine the next ADR number: list `system/decisions/adr-*.md`, take the highest `NNNN`, and add 1 (zero-padded to 4 digits, starting at `0001` if none exist).

Then:

1. Create `system/decisions/adr-NNNN-<short-description>.md` from `templates/adr.md`.
2. Populate YAML frontmatter:
   - `id`: filename without the `.md` extension (e.g. `adr-0001-centralize-dock-reservation-in-fleet-service`)
   - `title`: human-readable title
   - `status`: one of `proposed` / `accepted` / `superseded` / `obsolete`
   - `date`: today's date, `YYYY-MM-DD` (get it from the environment; do not guess)
3. Fill the sections — `TBD` for anything unknown rather than deleting the heading:
   - **Context** — the problem or decision point, and the forces at play
   - **Options Considered** — plain Markdown table, one row per option with its tradeoffs
   - **Decision** — the chosen option, stated plainly (or `TBD` while `proposed`)
   - **Rationale** — why this option won
   - **Implications / Follow-ups** — consequences, migrations, revisit conditions

Finish by running `python tools/validate.py` from the repo root and fixing anything it reports.

## Update flow

If the ADR already exists:

1. Locate it under `system/decisions/` and read it
2. Ask the user what needs to change
3. Apply only the requested changes — do not regenerate the whole file
4. Re-run `python tools/validate.py`

Status transitions:

- `proposed` → `accepted` once the decision is made — fill in Decision and Rationale at the same time
- When a new ADR replaces an old one, set the old ADR's status to `superseded` and note the superseding ADR's filename in its **Implications / Follow-ups**; never rewrite the old ADR's decision text
- `obsolete` is for decisions overtaken by events with no direct replacement — note why

ADR numbers are never reused, and an ADR's number never changes.

## Conventions

- Filename: `adr-NNNN-<short-description>.md` — four-digit zero-padded number, kebab-case description
- Tables are plain Markdown, never HTML `<table>` markup
- Examples: `adr-0001-geofence-service-boundary.md`, `adr-0001-centralize-dock-reservation-in-fleet-service.md`
