# `prd/` — PRD (PDP-08) section stubs

Source folder for the **Product Requirements Document** deliverable (ASI template **PDP-08**).
The requirement-bearing PRD sections are generated from this repo's artifacts; the
governance/overview sections have no artifact home, so they are authored here — one file per
section, shipped as stubs so the gap is visible in every project baseline instead of silently
absent.

Each stub carries the official PDP-08 rev A section structure (tables, guidance) with
`[bracketed placeholders]`, plus frontmatter (`pdp-08-section`, `pdp-08-ref`, `status`,
`owner`) and a `<!-- STUB -->` marker. Author sections one at a time; when a section is real,
delete the marker and set `status: authored`.

`owner` is seeded with a role/group default so no section ships unowned — confirm each when
instantiating a project. The rule: a section with a clearly responsible party lists that group
(Functional Safety owns the safety and environmental/site domains); product-intent and
document-governance sections default to Product Manager per the PDP-08 §3 RACI; anything with
mixed or unclear ownership defaults to Systems Architect. Role titles and group names only —
never a person; names live in `meta.yaml`.

Completeness is computed, not tracked by hand:

```text
grep -r "<!-- STUB -->" prd/
```

## Section map

| PDP-08 § | Section | Source |
|---|---|---|
| §1 | Purpose / Document Purpose | Near-boilerplate — carried by the document template, not a stub |
| §2 | Scope (In / Out) + Boundary Notes | `sections/scope.md` |
| — | Reference Standards | `sections/standards.md` — **not in PDP-08 rev A**; recommended governance addition (PRAK precedent, 2026-07-27) |
| §3 | RACI Matrix for Deliverable | `sections/raci.md` |
| §4.1 | Product Summary | `sections/overview.md` |
| §4.2 | Customer / User Personas | Generated from `product/personas/` |
| §4.3 + §5.1 | Target Markets & Site Archetypes | `sections/markets.md` |
| §5.2 | Use Case Overview | Generated from `product/use-cases/` |
| §5.3 | Release Plan & Phasing | `sections/release-plan.md` |
| §6.1–6.2 | Product Goals / System Goals | `sections/goals.md` — read its lineage caution before authoring |
| §6.3–6.4 | KPIs + Goal-to-KPI Alignment | `sections/kpis.md` |
| §7.1–7.2 | Product / Functional Requirements | Generated from `product/requirements/` |
| §7.3 | Safety Requirements | `sections/safety.md` |
| §7.4 | Security / Cybersecurity Requirements | `sections/security.md` |
| §7.5 | Environmental / Site Requirements | `sections/environment-site.md` |
| §7.6 | Performance Requirements | `sections/performance.md` |
| §8 | Use Case Mapping Summary | Derived from `traceability/TRACEABILITY.md` |
| §9 | Appendix A — Environmental & Site Consideration Library | Authoring aid in the controlled PDP-08 template; condensed checklist in `sections/environment-site.md` |

Engineering decomposition (`system/requirements/`, `system/architecture/`) is deliberately
**not** a PRD section — it is a sibling deliverable (System Requirements Specification /
Architecture Description). The PRD references the product/functional requirements it supports.

## Document control

`meta.yaml` fills the PDP-08 cover and control tables (template ID/revision, document
owner/prepared-by/approver/contributors). Rendered prose should use **role titles**; names
live only in `meta.yaml` so personnel changes are a one-line edit rather than a drift source
in committed sections. `change-log.md` records one row per PRD revision.

## Generating the document

This template ships no generator. The reference implementation is `prak-v-model`
`tools/prd_build/` (see its `docs/DesignPlans/prd-prak-doc-generation.md`): assemble artifacts
plus these sections into committed Markdown, render `.docx` via pandoc against the controlled
template, and verify the output matches the committed source. Port or adapt it when a project
needs the controlled deliverable; until then this folder is still useful as the authored home
for the governance content.
