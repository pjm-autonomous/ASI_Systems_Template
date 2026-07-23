> **⚠️ TODO — pending review.** This file was generalized from `prak-v-model`'s `CLAUDE.md` as a first pass and has not yet had a dedicated review. Treat it as a working draft; see `TODO.md`.

# Project Context for AI Assistants

Artifact repository for [PROJECT NAME] — replace this line with a one-paragraph description of the product/system this repo covers.

## Artifact Hierarchy

```
Personas → Use Cases → Product Requirements → { System Requirements, Architecture Diagrams, ICDs, Data Specifications }
```

- **Personas** — who interacts with the system and what they do across its lifecycle
- **Use Cases** — a specific need a persona has of the system
- **Product Requirements** — stakeholder-facing statements of what the system shall do to satisfy a use case
- **System Requirements** — engineering decomposition of a product requirement, allocated to a component or subsystem
- **Architecture Diagrams** — Mermaid diagrams (structure, behavior, deployment) describing a product requirement
- **Interface Control Documents (ICDs)** — contracts between components, subsystems, or external systems
- **Data Specifications** — entity/schema definitions, ownership, and retention rules
- **Architecture Decision Records (ADRs)** — cross-cutting; capture why a significant design choice was made

## Directory Structure

| Directory | Contains |
|---|---|
| `product/personas/` | Persona Markdown files |
| `product/use-cases/<feature>/` | Use case Markdown files, grouped by feature bucket |
| `product/requirements/<feature>/` | Product requirement Markdown files, grouped by feature |
| `system/requirements/<feature>/` | System requirement Markdown files |
| `system/architecture/<feature>/` | Architecture diagram Markdown files (Mermaid) |
| `system/data/<feature>/` | Data specification Markdown files |
| `system/deployment/<feature>/` | Deployment architecture Markdown files |
| `system/interfaces/<feature>/` | Interface control document Markdown files |
| `system/decisions/` | Architecture decision records (not feature-bucketed — sequential) |
| `templates/` | Canonical blank templates for each artifact type |
| `example/` | One fictional feature worked end-to-end, for reference |
| `extensions/` | Stub folders for safety, coding, testing, QA/CM, change/risk, metrics documentation |
| `reference/` | Condensed BKM document-set and standards-framework reference material |

Feature buckets are kebab-case directories chosen by the author. Reuse an existing bucket when content fits; create a new one only when no existing bucket is a good fit.

## Naming Conventions

| Artifact | Pattern | Example |
|---|---|---|
| Persona | `<role-or-team>.md` | `remote-operator.md` |
| Use case | `uc-<description>.md` | `uc-geofence-breach-alert.md` |
| Product requirement | `req-<description>.md` | `req-geofence-alert-latency.md` |
| System requirement | `sysreq-<description>.md` | `sysreq-geofence-check-interval.md` |
| Architecture diagram | `arch-<description>.md` | `arch-geofence-alert-flow.md` |
| Data specification | `data-<description>.md` | `data-geofence-zone-schema.md` |
| Deployment architecture | `deploy-<description>.md` | `deploy-geofence-service-topology.md` |
| Interface control document | `icd-<description>.md` | `icd-geofence-alert-api.md` |
| Architecture decision record | `adr-NNNN-<description>.md` | `adr-0001-geofence-service-boundary.md` |

All names use kebab-case. Cross-references in frontmatter use the filename only (no directory prefix).

## Table Format

All artifact tables use **plain Markdown table syntax** (not HTML `<table>` markup). Keep column content short — wrap long prose into the paragraph below the table rather than cramming it into a cell.

## Frontmatter Requirements

Every artifact file must open with YAML frontmatter (`---` delimited) containing at minimum:

| Artifact | Required fields |
|---|---|
| Persona | `id`, `title`, `class` |
| Use case | `id`, `title`, `primary-actors`, `parent-personas` |
| Product requirement | `id`, `title`, `parent-use-cases`, `priority` |
| System requirement | `id`, `title`, `parent-product-requirement`, `allocation`, `priority` |
| Architecture diagram | `id`, `title`, `parent-product-requirement`, `diagram-type` |
| ICD | `id`, `title`, `parent-product-requirement`, `owning-component`, `consumers` |
| Data specification | `id`, `title`, `parent-product-requirement` |
| Deployment architecture | `id`, `title`, `scope` |
| ADR | `id`, `title`, `status`, `date` |

`tools/validate.py` enforces filename pattern, required frontmatter fields, and that cross-reference fields point to files that actually exist.

## Diagram Format

Architecture diagrams use Mermaid inside a fenced ` ```mermaid ` block, accompanied by a short Markdown table with Purpose, Scope, and Notes. One diagram per file so each file maps to a single reviewable unit.

## Extension Folders

`extensions/` holds stub documents for the parts of the SE lifecycle that aren't authored at project kickoff: safety, coding, testing, QA/CM, change/risk, and metrics. Each stub explains what a complete document looks like (per `reference/bkm-document-set.md`) and is replaced with real content when the project reaches that maturity point — do not delete the stub structure even if a category isn't needed yet; note the decision to defer it instead.

## Traceability

`traceability/TRACEABILITY.md` — Markdown matrix linking each persona to its use cases, product requirements, system requirements, architecture diagrams, ICDs, and data specifications via relative links. Update it whenever you add or change an artifact.

`traceability/STANDARDS-MAPPING.md` — tracks which cross-industry standards apply to this project and current coverage. Seeded from `reference/standards-framework.md`.
