---
artifact-type: architecture
tier: architecture
---

# Architecture

- [What belongs here](#what-belongs-here)
- [Architecture has no parent requirement](#architecture-has-no-parent-requirement)
- [Diagram types](#diagram-types)
- [One diagram per file](#one-diagram-per-file)
- [Diagram format](#diagram-format)
- [When to add an ADR instead, or as well](#when-to-add-an-adr-instead-or-as-well)
- [Keeping diagrams from going stale](#keeping-diagrams-from-going-stale)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `architecture/arch-<description>.md`, optionally grouped into a
feature-bucket directory. Start from `templates/architecture-diagram.md`.

## What belongs here

**Architecture exists at every level** (D-09), and at each one it shows **the
entities of the level below and how they relate** — L0's architecture shows the
L1 systems, L1's shows the L2 systems, L2's shows its own sub-systems and
components.

Architecture and interfaces are **one responsibility seen from two sides**. A
level owns the boundaries between the entities below it (`interfaces/`), and it
owns the architecture those boundaries are drawn on. Neither stands without the
other: an interface defined with no architecture saying what the parties are is
ungrounded, and an architecture with no interfaces is a picture rather than a
contract.

That pairing is why architecture carries no flag in `repo-standard.yaml`. It is
core at every level, not an optional packet — a flag you cannot set to false is
not a packet (D-52).

## Architecture has no parent requirement

An architecture artifact has **no `parent-*` field**, deliberately.

A diagram is not a decomposition of one requirement; it is the context several
requirements are written against. Forcing it to name a single parent would either
be a lie or would silently privilege one requirement over the others the diagram
serves.

Relate a diagram to requirements through its Notes row and through the entities
it names, which should match the `allocation` values used in requirements at this
level.

## Diagram types

`diagram-type` is required. The authoritative value list is the `diagram-type`
enum in [`standard/artifact-schema.yaml`](../standard/artifact-schema.yaml); what
each is for:

| Value | Use for |
| --- | --- |
| `context` | what sits outside this level's boundary and what crosses it |
| `structure` | how the entities one level down are arranged and connected |
| `behavior` | what the system does over time, without fixing a message order |
| `sequence` | a specific interaction, in order, between named parties |
| `state` | lifecycle-driven behaviour — modes, transitions, and their triggers |
| `deployment` | where things run, and on what |

## One diagram per file

One diagram per file, so each file is a single reviewable unit and diffs stay
meaningful. Resist combining several views into one file — a structure view and a
sequence view of the same feature are two files, not two sections.

Each file carries a short Purpose / Scope / Notes table alongside the diagram.

## Diagram format

The source format is declared per repo in `repo-standard.yaml`
(`conventions.diagram-format`, D-33):

- **`mermaid`** renders natively in GitHub, so a diagram is readable in a pull
  request with no build step.
- **`puml`** is more expressive but needs a render step to be readable in review.

`ISO/IEC/IEEE 42010` is the standard behind the viewpoint-per-file structure. It
specifies the *structure* an architecture description needs, not a notation — see
`reference/standards-framework.md`.

## When to add an ADR instead, or as well

If a diagram is capturing a **decision** — why this boundary, why this data flow
rather than an alternative — the rationale belongs in an ADR at the relevant
tier (`<tier>/decisions/adr-NNNN-<description>.md`), referenced from the diagram's
Notes row.

A diagram shows what the architecture *is*. An ADR records why it is that and not
something else. Trying to argue the decision inside the diagram file produces a
document that is bad at both jobs.

## Keeping diagrams from going stale

**A diagram that no longer matches the system is worse than no diagram** — it is
believed, and it is wrong.

When a requirement or an interface changes in a way that affects a diagram,
update the diagram in the same pull request. Diagram updates that become separate
backlog items do not get done.

## Maturity

Architecture artifacts start at `M1`. A state at or above `M2` requires a dated
promotion record in `_registry/` — see
[`standard/decisions.md`](../standard/decisions.md) D-40 … D-43.

Because interfaces are defined against architecture, an architecture artifact
should not lag the interfaces that depend on it — if `interfaces/` is being
promoted and this is not, the boundary is being baselined against a picture
nobody has reviewed.
