---
pdp-08-section: "Product Goals (PG) / System Goals (SG)"
pdp-08-ref: "§6.1–6.2"
status: stub
owner: Product Manager   # default per PDP-08 §3 RACI — confirm per project
---

# Goals

<!-- STUB -->

Structure from PDP-08 rev A §6.1 (Product Goals) and §6.2 (system-level goals — PDP-08 calls
these Vehicle-System Goals; rename per product). Goals are stable, directional,
outcome-focused statements of why the product exists and what the system must do well enough
for the product goals to be achieved. Not solution-prescriptive.

**Lineage caution (PRAK precedent, 2026-07-27):** goal IDs referenced from requirement
coverage fields are free text — unenforceable without a cross-referenced artifact or
frontmatter link. Either give goals real lineage (a goals artifact that requirements
reference, validated like other cross-references) or record a disposition here explicitly
discarding this section, and drop goal references from requirement coverage rows with it.
Do not ship a goals section that nothing traces to.

## Product Goals

| Goal ID | Product Goal | Why It Matters |
|---|---|---|
| PG-01 | [Enable safe and predictable execution of the primary workflow in target operating conditions.] | [The core customer-facing value of the product.] |
| PG-02 | [Reduce dependency on scarce or variable manual labor in the target workflow.] | [Customer productivity and labor-efficiency outcomes.] |
| PG-03 | [Improve operational consistency and repeatability versus incumbent approaches.] | [Schedule reliability, output confidence, commercial value.] |

## System Goals

| Goal ID | System Goal | Supported Goal(s) |
|---|---|---|
| SG-01 | [Perform the primary operational workflow within the defined operating envelope.] | [PG-01, PG-03] |
| SG-02 | [Operate with acceptable safety behavior around people, equipment, and site constraints.] | [PG-01] |
| SG-03 | [Maintain acceptable availability and recoverability in the field.] | [PG-03] |
