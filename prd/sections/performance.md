---
pdp-08-section: "Performance Requirements (PER)"
pdp-08-ref: "§7.6"
status: stub
owner: Systems Architect   # mixed/unclear ownership defaults to Systems Architect — confirm per project
---

# Performance Requirements

<!-- STUB -->

Structure from PDP-08 rev A §7.6. Define the level of operational performance the product must
achieve to deliver its intended value: throughput, cycle time, quality, availability,
accuracy, recovery, and operational consistency. The distinction from KPIs (§6.3): this
section defines the **required level** of performance; KPIs define how success is measured and
tracked. Do not restate the KPI table or write verification methods here.

| REQ ID | Req. Statement | Markets (§5.1) | Use Case (§5.2) | Release (§5.3) | Goal (§6) |
|---|---|---|---|---|---|
| PER-01 | [The product shall achieve the minimum required throughput, cycle rate, or task completion rate for the intended use case and release.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| PER-02 | [The product shall achieve the required task-quality or output-conformance level for the intended market, use case, and release.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| PER-03 | [The product shall meet the defined availability and uptime expectations for intended field operation.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| PER-04 | [The product shall maintain acceptable operational performance within the environmental and site envelopes defined in §7.5.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| PER-05 | [The product shall recover from defined faults, pauses, or common off-nominal conditions within the required time or operational-impact threshold.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |

[Drop the Release and Goal columns if the project excludes release tracking or discards the
goals section. Subsystem-specific performance targets move with their system requirements to
the SRS — they do not belong in a product-level PRD.]
