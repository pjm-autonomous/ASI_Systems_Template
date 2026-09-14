---
name: use-case
description: Create or update a use case artifact in stakeholder/use-cases/<feature>/. Use when the user wants to capture a specific need a persona has of the system.
---

# Skill: use-case

Create or update a use case artifact in `stakeholder/use-cases/<feature>/`.

## Create flow

Ask the user for:

- Use case title (short description for the filename)
- Parent persona filename(s) (e.g. `remote-operator.md`) — one or more; each must exist in `stakeholder/personas/` (if not, direct the user to `/persona` first)
- Primary actor filename(s) — typically the same as the parent persona(s); one or more
- Feature bucket — kebab-case directory name. Suggest the best fit from existing buckets under `stakeholder/use-cases/`; create a new bucket only when no existing one fits
- A brief summary of the need or scenario

Then create `stakeholder/use-cases/<feature>/uc-<name>.md` from `templates/use-case.md`:

1. Populate YAML frontmatter:
   - `id`: filename without the `.md` extension
   - `title`: human-readable title
   - `primary-actors`: YAML list of persona filenames including `.md`, no directory path (singleton list is fine)
   - `parent-personas`: YAML list of persona filenames including `.md`, no directory path (singleton list is fine)
2. Fill the plain Markdown table rows: **ID**, **Primary Actors**, **Parent Personas**
3. Fill the sections:
   - **Description** — what need the persona has of the system, from the summary
   - **Preconditions** — `TBD` if unknown
   - **Main Flow** — numbered interaction sequence with the system; `TBD` if unknown
   - **Alternate / Exception Flows** — `TBD` if unknown
   - **Postconditions** — `TBD` if unknown
   - **Notes** — anything that doesn't fit above; omit or `TBD` if none
4. Optionally add a `## Flow Diagram` section with a Mermaid flowchart of the main/alternate flows — follow the **Mermaid conventions** in `.claude/skills/architecture/SKILL.md` (the single source for this repo's Mermaid conventions)
frontmatter (D-46). A skill writing rows into it reintroduces the hand
maintenance that produced a 316-row, 0-populated matrix. The parent
reference you set in frontmatter is what puts this artifact in the matrix.

Finish by running `python tools/validate.py` from the repo root and fixing anything it reports.

## Update flow

If the use case already exists:

1. Locate it under `stakeholder/use-cases/` and read it
2. Ask the user what needs to change
3. Apply only the requested changes — do not regenerate the whole file
4. Re-run `python tools/validate.py`

## Conventions

- Filename: `uc-<short-description>.md` in kebab-case
- Tables are plain Markdown, never HTML `<table>` markup
- Examples: `uc-geofence-breach-alert.md`, `uc-low-battery-return-to-dock.md`, `uc-all-stop-broadcast.md`
