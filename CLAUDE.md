# Project Context for AI Assistants

Artifact repository for **[PROJECT NAME]** — replace this line with a one-paragraph description of the product/system this repo covers. If you're reading this in `template-repo` itself rather than an instantiated project, see `README.md` first — this file assumes the template has already been used to create a real project.

This file is written for Claude (or another AI assistant) working in this repo. A human contributor should read `README.md` and `CONTRIBUTING.md` first; this file adds machine-actionable detail on top of those.

## What This Repo Is

A traceability chain of SA/SE artifacts — personas, use cases, requirements, architecture, interfaces, data, deployment, and decisions — plus extension points for the rest of the SE lifecycle (safety, coding, testing, QA/CM, change/risk, metrics) that get filled in as the project matures. See `README.md` for the full directory tree and `reference/bkm-document-set.md` for what a mature version of each extension category looks like.

## Artifact Hierarchy

```text
Personas
  └─ Use Cases
       └─ Product Requirements
            ├─ System Requirements
            ├─ Architecture Diagrams
            ├─ Interface Control Documents (ICDs)
            └─ Data Specifications
```

Architecture Decision Records (`system/decisions/`) and deployment architecture (`system/deployment/`) are cross-cutting — they document rationale and topology that can span multiple artifacts in the hierarchy above, rather than being a child of exactly one.

| Layer | Description | Directory |
| --- | --- | --- |
| Personas | Stakeholders who interact with the system across its lifecycle | `product/personas/` |
| Use Cases | A specific need a persona has of the system | `product/use-cases/<feature>/` |
| Product Requirements | Stakeholder-facing obligations that satisfy a use case | `product/requirements/<feature>/` |
| System Requirements | Engineering decomposition of a product requirement, allocated to a component/subsystem | `system/requirements/<feature>/` |
| Architecture Diagrams | Mermaid diagrams (structure, behavior, deployment) tracing to a product requirement | `system/architecture/<feature>/` |
| Data Specifications | Entity/schema definitions, ownership, retention | `system/data/<feature>/` |
| Deployment Architecture | Nodes, environments, networking | `system/deployment/<feature>/` |
| Interface Control Documents | Contracts between components/subsystems/external systems | `system/interfaces/<feature>/` |
| Architecture Decision Records | Why a significant design choice was made | `system/decisions/` |

## Directory Structure

| Directory | Contains |
| --- | --- |
| `product/personas/`, `product/use-cases/<feature>/`, `product/requirements/<feature>/` | Core SA-owned product artifacts |
| `system/requirements/`, `system/architecture/`, `system/data/`, `system/deployment/`, `system/interfaces/`, `system/decisions/` | Core SA/SE-owned system artifacts, each grouped by feature bucket except `decisions/` (sequential ADRs) |
| `templates/` | Canonical blank starting point for each artifact type |
| `example/` | One fictional feature (`low-battery-return-to-dock`) worked end-to-end through every artifact type, for reference |
| `extensions/` | Stub folders for safety, coding, testing, QA/CM, change/risk, and metrics documentation — see `extensions/README.md` |
| `reference/` | `bkm-document-set.md` (what a mature SE doc set looks like), `standards-framework.md` (cross-industry standards, scored per applicability), `tooling-recommendations.md` (skills/plugins/connectors) |
| `traceability/` | `TRACEABILITY.md` (persona → architecture matrix) and `STANDARDS-MAPPING.md` (which standards apply, at what rigor) |
| `glossary/` | Shared terminology |
| `tools/`, `tests/` | `validate.py` (the artifact validator) and its test suite |

Feature buckets (the `<feature>` in the paths above) are kebab-case directories chosen by the author. Reuse an existing bucket when new content fits; create a new one only when no existing bucket is a good fit.

## Naming Conventions

| Artifact | Pattern | Example |
| --- | --- | --- |
| Persona | `<role-or-team>.md` | `remote-operator.md` |
| Use case | `uc-<description>.md` | `uc-geofence-breach-alert.md` |
| Product requirement | `req-<description>.md` | `req-geofence-alert-latency.md` |
| System requirement | `sysreq-<description>.md` | `sysreq-geofence-check-interval.md` |
| Architecture diagram | `arch-<description>.md` | `arch-geofence-alert-flow.md` |
| Data specification | `data-<description>.md` | `data-geofence-zone-schema.md` |
| Deployment architecture | `deploy-<description>.md` | `deploy-geofence-service-topology.md` |
| Interface control document | `icd-<description>.md` | `icd-geofence-alert-api.md` |
| Architecture decision record | `adr-NNNN-<description>.md` | `adr-0001-geofence-service-boundary.md` |

All names use kebab-case. Cross-references in frontmatter use the **filename only**, no directory prefix — `tools/validate.py` resolves them by matching filenames within the correct artifact-type glob, not by path.

## Table Format

All artifact tables use **plain Markdown table syntax** — not HTML `<table>` markup. Keep cells short; move long prose into paragraphs below the table rather than cramming it into a cell.

## Frontmatter Requirements

Every artifact file opens with YAML frontmatter (`---` delimited). Required fields per type, enforced by `tools/validate.py`:

| Artifact | Required fields |
| --- | --- |
| Persona | `id`, `title`, `class` (one of `developer-integrator` / `runtime-operator` / `external-system`) |
| Use case | `id`, `title`, `primary-actors`, `parent-personas` |
| Product requirement | `id`, `title`, `parent-use-cases`, `priority` |
| System requirement | `id`, `title`, `parent-product-requirement`, `allocation`, `priority` |
| Architecture diagram | `id`, `title`, `parent-product-requirement`, `diagram-type` |
| ICD | `id`, `title`, `parent-product-requirement`, `owning-component`, `consumers` |
| Data specification | `id`, `title`, `parent-product-requirement` |
| Deployment architecture | `id`, `title`, `scope` |
| ADR | `id`, `title`, `status` (one of `proposed` / `accepted` / `superseded` / `obsolete`), `date` |

`tools/validate.py` also checks: filename matches the kebab-case + prefix pattern for its type; every cross-reference field resolves to a file that actually exists at the correct layer; architecture files contain at least one fenced ` ```mermaid ` block.

## Diagram Format

Architecture diagrams use Mermaid inside a fenced ` ```mermaid ` block, accompanied by a short Markdown table (Purpose, Scope, Notes). One diagram per file, so each file maps to a single reviewable unit.

## Extension Folders

`extensions/` holds stub documents for the parts of the SE lifecycle not authored at kickoff: safety, coding, testing, QA/CM, change/risk, and metrics (see `reference/bkm-document-set.md` for the full rationale per category). When you author real content for a stub, keep the filename stable so existing links keep working. If a category is deliberately deferred rather than authored, say so explicitly in the stub — who decided, why, when it'll be revisited — rather than leaving it silently empty.

## Standards

`reference/standards-framework.md` lists cross-industry standards (IEC 60204-1, ISO 13849-1/IEC 62061, ISO 26262, ISO 12207, ASPICE PAM 4.0, ISO 9001 §8.3, MISRA C/C++, IEC 62443, ISO/IEC/IEEE 15288/29148/42010/24765, ISO 10218-1/-2, ANSI/A3 R15.06, ISO 3691-4, ISO 21448/SOTIF, ISO/SAE 21434, ISO 31000) with scoring rubrics where available. Not every standard applies to every project — `traceability/STANDARDS-MAPPING.md` is where a project records its actual applicability decisions. Default to "engineering reference" language; only call a standard a "compliance obligation" if that is genuinely the project's posture.

## Tooling and Skills

`reference/tooling-recommendations.md` covers recommended Claude Code skills (not yet built as of this writing — see `TODO.md`), MCP connectors worth connecting for a given project (Atlassian, Microsoft 365, Google Drive), and built-in document-export skills (docx/pptx/xlsx/pdf) for turning artifacts into stakeholder-facing deliverables. Check it before assuming a capability needs to be built from scratch.

## Traceability

`traceability/TRACEABILITY.md` — Markdown matrix linking each persona to its use cases, product requirements, system requirements, architecture diagrams, ICDs, and data specifications via relative links. Update it whenever you add or change an artifact; an empty cell means "not yet authored," not "not applicable" — use `n/a` with a note for deliberate exclusions.
