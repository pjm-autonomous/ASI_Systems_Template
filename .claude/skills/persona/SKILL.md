---
name: persona
description: Create or update a persona artifact in product/personas/. Use when the user wants to add a stakeholder, actor, or persona to the artifact tree.
---

# Skill: persona

Create or update a persona artifact in `product/personas/`.

## Persona classes

Every persona is exactly one of:

- **developer-integrator** — teams building on or integrating with the system; they interact at API, framework, or build-time boundaries
- **runtime-operator** — people interacting with the system at runtime (commands, monitoring, telemetry, interventions)
- **external-system** — software systems interfacing with the system at runtime on behalf of human operators or other systems (C2 systems, fleet managers, ERP/MES, planners)

The team building this repo's system is never a persona — personas are stakeholders *of* the system, not its authors.

## Create flow

Ask the user for:

1. Persona name → becomes the kebab-case filename (e.g. `remote-operator`)
2. Class — `developer-integrator`, `runtime-operator`, or `external-system`
3. One or two sentences on who they are and what they need from the system

Then create `product/personas/<name>.md` from `templates/persona.md`:

- Populate YAML frontmatter: `id` from the filename (no `.md`), `title` human-readable, `class` from the answer above
- **Summary** — 1–2 sentences from the user's description
- **Class** — restate the class and, in one clause, why it fits
- **Responsibilities / Goals** — what this persona is trying to accomplish; for developer-integrators name the APIs/framework surface they touch, for runtime-operators the behaviors/commands/telemetry they consume or trigger, for external-systems the runtime interfaces they use
- **Boundaries** — what this persona does NOT own or control; use `TBD` if unknown rather than leaving the section empty

Add a new row to `traceability/TRACEABILITY.md` with the Persona cell filled and the remaining columns empty. Link relative to `traceability/`: `[<name>.md](../product/personas/<name>.md)`.

Finish by running `python tools/validate.py` from the repo root and fixing anything it reports.

## Update flow

If `product/personas/<name>.md` already exists:

1. Read the file
2. Ask the user what needs to change (summary, class, responsibilities, boundaries)
3. Apply only the requested changes — do not regenerate the whole file
4. Re-run `python tools/validate.py`

## Conventions

- Filename: `<role-or-team>.md` in kebab-case — no `persona-` prefix
- Tables (if any) are plain Markdown, never HTML `<table>` markup
- Examples: `remote-operator.md`, `fleet-operator.md`, `mission-controller.md`, `perception-dev-team.md`
