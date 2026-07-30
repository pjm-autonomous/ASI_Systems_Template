---
pdp-08-section: "Scope (In / Out) + Boundary Notes"
pdp-08-ref: "§2"
status: stub
owner: Product Manager   # default per PDP-08 §3 RACI — confirm per project
---

# Scope

<!-- STUB -->

Structure from PDP-08 rev A §2. The PRD is written at the single-product level: it refines the
Product Concept Document into structured use cases and high-level requirements that guide
development across planned releases. Requirements define outcomes, expected behaviors,
constraints, and operating boundaries — the *what* — not detailed implementation methods — the
*how*. The PRD should be detailed enough to drive engineering direction without becoming a
substitute for system architecture, subsystem specifications, software design, or verification
planning. Add enough detail here to prevent scope creep; name where excluded content lives.

## In Scope

The PRD includes the following:

| In-Scope | Description |
|---|---|
| [Single-product definition] | [Definition of the product and the use cases it is intended to support.] |
| [Target markets, users, and site context] | [High-level context for where the product operates and why the requirements matter.] |
| [Customer and user personas] | [The stakeholders that interact with the product across its lifecycle — generated from `product/personas/`.] |
| [Use case overview] | [The specific needs personas have of the product — generated from `product/use-cases/`.] |
| [High-level requirement categories] | [Product, functional, safety, security, environmental/site, and performance requirements.] |
| [Operating expectations and constraints] | [Intended operating envelope, key site assumptions, and major boundaries that shape design and validation.] |
| [Use case mapping] | [Tracing of use cases to the product and functional requirements that satisfy them.] |

## Out of Scope

The PRD does not define the following except where needed to clarify product boundaries. Name
where each exclusion lives:

| Out-of-Scope | Where It Lives |
|---|---|
| [Fleet-level or cross-product behaviors] | [The applicable Market Solution Requirements Document(s).] |
| [Detailed technical design or architecture] | [`system/architecture/` — future Architecture Description / SAD.] |
| [Engineering decomposition (system requirements)] | [`system/requirements/` — sibling deliverable (System Requirements Specification); or the requirements-management tool of record.] |
| [Code-level, algorithm-level, or component-level specifications] | [Engineering-owned specifications.] |
| [Detailed verification methods and test procedures] | [`extensions/testing/` — test strategy and plans.] |
| [Program execution detail] | [Program/product management plans — schedules, staffing, milestones.] |
| [Commercial business case development] | [Other PDP artifacts — e.g. PDP-03 Market Analysis, PDP-11 Product Opportunity Evaluation, PDP-14 Commercialization Plan.] |

## Document Boundary Notes

[Clarify important product-boundary decisions for this specific product — e.g. whether support
equipment, an operator console, an autonomy kit, inherited platform software, or site
infrastructure assumptions are treated as part of the product definition for this PRD.]
