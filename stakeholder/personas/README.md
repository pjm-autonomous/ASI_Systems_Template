---
artifact-type: persona
tier: stakeholder
---

# Personas

- [What belongs here](#what-belongs-here)
- [What does not belong here](#what-does-not-belong-here)
- [How many is normal](#how-many-is-normal)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

If this repo does not declare the `stakeholder` tier, this directory should not
exist here. Personas are authored once, at the level that owns stakeholder and
market defined needs, and everything below traces up to them across repo
boundaries.

One Markdown file per persona, named `<role-or-team>.md` — kebab-case, **no
prefix**; personas are the one artifact type without one. Start from
`templates/persona.md`, and read the worked persona under `example/` before
authoring your first.

## What belongs here

A persona is a **stakeholder who interacts with the system across its
lifecycle** — not a feature, not a team internal to the organisation building the
system.

Personas are usually the first artifacts authored on a new project, because every
use case traces up to at least one (`parent-personas` in
`stakeholder/use-cases/uc-*.md`), and everything below a use case traces up
through it. A persona is where "traces upstream to a customer-defined need" bottoms
out.

Each persona declares a `class`. The authoritative value list is the
`persona-class` enum in `standard/artifact-schema.yaml`; what each one means:

| Class | Interacts with the system… |
| --- | --- |
| `developer-integrator` | at **build time** — API consumers, framework integrators, tooling users. They build *on top of* the system. |
| `runtime-operator` | at **run time**, as a person — commands, state transitions, telemetry, manual overrides. |
| `external-system` | at **run time**, as software acting for people — command-and-control systems, fleet managers, mission planners. |

The distinction that matters is *when* and *as what*, not seniority or job title.

## What does not belong here

- **The team building the system is not a persona.** It is the implicit author of
  everything in this repo. A builder-side actor may appear in a use case table as
  a supporting actor without having its own persona file.
- **Not one persona per person or per customer.** Personas are roles and classes
  of stakeholder, not named individuals or accounts.
- **Not a persona per variant.** "Senior operator" versus "operator" is usually a
  note inside one persona, not a second file.

## How many is normal

Most projects settle between three and six active personas. If you are authoring
a tenth, check first whether it is a variant of an existing one.

## Maturity

Personas start at `M1`. A state at or above `M2` requires a dated promotion
record in `_registry/` — see `standard/decisions.md` D-40 … D-43. Because
everything traces up to a persona, a persona that is wrong is expensive to
correct later; it is worth getting these to `M2` before authoring far below them.
