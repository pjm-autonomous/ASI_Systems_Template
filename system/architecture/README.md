# Architecture Diagrams

Grouped by feature bucket: `system/architecture/<feature>/arch-<description>.md`. One Mermaid diagram per file. Start from `templates/architecture-diagram.md`. See `example/system/architecture/low-battery-return-to-dock/arch-dock-return-flow.md` for a worked sample.

## What Belongs Here

Each file is one diagram (`diagram-type`: `component`, `sequence`, `state`, `deployment`, or `use-case`) tracing to exactly one `parent-product-requirement`, accompanied by a short Purpose/Scope/Notes table. One diagram per file keeps each file mapped to a single reviewable unit and keeps diffs meaningful — resist the urge to combine several views into one file.

Diagram notation is intentionally not prescribed beyond Mermaid — sequence diagrams for interaction flows, state diagrams for lifecycle-driven behavior, flowcharts for component/data relationships, and so on. `ISO/IEC/IEEE 42010` (see `reference/standards-framework.md`) is the standard behind this template's viewpoint-per-file structure; it specifies the *structure* an architecture description needs, not a specific notation.

## When to Add an ADR Instead (or Also)

If a diagram is capturing a decision — *why* this component boundary, *why* this data flow instead of an alternative — put the rationale in `system/decisions/adr-NNNN-<description>.md` and reference it from the diagram's Notes row, rather than trying to justify the decision in the diagram file itself. The example feature does exactly this: `arch-dock-return-flow.md` references `adr-0001-centralize-dock-reservation-in-fleet-service.md` for the reasoning behind the architecture shown.

## Keeping Diagrams From Going Stale

A diagram that no longer matches the system is worse than no diagram. When a system requirement or ICD changes in a way that affects a diagram, update the diagram in the same PR — don't let diagram updates become a separate backlog item.
