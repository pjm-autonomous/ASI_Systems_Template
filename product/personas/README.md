# Personas

One Markdown file per persona, named `<role-or-team>.md` (kebab-case, no prefix — personas are the one artifact type without one). Start from `templates/persona.md`. See `example/product/personas/fleet-operator.md` for a worked sample.

## What Belongs Here

A persona is a stakeholder who interacts with the system across its lifecycle — not a feature, not a team internal to the org building the system. Every use case must trace up to at least one persona (`parent-personas` in `product/use-cases/*/uc-*.md` frontmatter), so personas are usually the first artifacts authored on a new project.

Each persona must declare a `class` in its frontmatter, one of:

- **`developer-integrator`** — teams that build on top of the system: API consumers, framework integrators, build-time tooling users.
- **`runtime-operator`** — people who interact with system behavior at runtime: commands, state transitions, telemetry, manual overrides.
- **`external-system`** — other software systems that interface with this system at runtime on behalf of humans: command-and-control systems, fleet managers, mission planners.

## What Doesn't Belong Here

- The team that builds the system itself is not a persona (it's the implicit author of everything in this repo). If a builder-side actor needs to appear in a use case table as a supporting actor, that's fine — it just doesn't get its own persona file.
- Don't create a persona per individual person or per company — personas are roles/classes of stakeholder, not named individuals or accounts.

## How Many Personas Is Normal

Most projects settle on somewhere between 3 and 6 active personas. If you're authoring a 10th persona, check whether it's actually a variant of an existing one (e.g., "senior operator" vs. "operator") before creating a new file — variants are usually better captured as a note inside the existing persona than as a new class.
