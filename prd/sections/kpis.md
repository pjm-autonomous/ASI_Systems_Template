---
pdp-08-section: "KPIs + Goal-to-KPI Alignment"
pdp-08-ref: "§6.3–6.4"
status: stub
owner: Product Manager   # default per PDP-08 §3 RACI — confirm per project
---

# KPIs

<!-- STUB -->

Structure from PDP-08 rev A §6.3. KPIs translate goals into measurable indicators that guide
product decisions, engineering tradeoffs, and release readiness. Focus on the indicators most
important for decisions — not every possible measure, and not a verification plan.

**Scope cautions (PRAK precedent, 2026-07-27):** if the goals section is discarded, keep only
goal-independent, top-level guardrail metrics here. Any metric that is subsystem- or
component-specific (e.g. a timing spec allocated to one component) moves with its system
requirement to the SRS — it does not belong in a product-level PRD.

| KPI ID | KPI | Supports Goal(s) | Target | Release |
|---|---|---|---|---|
| KPI-01 | [Primary workflow completion rate] | [SG-01, PG-01] | [Achieve X%] | [R1.0] |
| KPI-02 | [Intervention rate per operating hour / cycle] | [SG-01] | [Decrease] | [R1.0 → R2.0] |
| KPI-03 | [Availability / uptime] | [SG-03, PG-03] | [Achieve X%] | [R1.0] |
| KPI-04 | [Safety-critical event rate] | [SG-02, PG-01] | [Minimize / zero tolerance as defined] | [All releases] |

## Goal-to-KPI Alignment Summary

Lightweight readability aid (PDP-08 §6.4), not a second traceability system — include only the
most important relationships. Auto-derive from goal references where tooling exists.

| Goal ID | Goal Summary | Primary KPI Coverage |
|---|---|---|
| [PG-01] | [Safe and predictable execution of the primary workflow.] | [KPI-01, KPI-04] |
