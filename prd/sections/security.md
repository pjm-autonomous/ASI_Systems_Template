---
pdp-08-section: "Security / Cybersecurity Requirements"
pdp-08-ref: "§7.4"
status: stub
owner: Systems Architect   # mixed/unclear ownership defaults to Systems Architect — confirm per project
---

# Security / Cybersecurity Requirements

<!-- STUB -->

Structure from PDP-08 rev A §7.4. Define the minimum expectations for how the product protects
control, connectivity, and operational data **within its product boundary**: authentication,
authorization, secure access posture, logging, integrity, and safe behavior under loss or
degradation of connectivity. Broader fleet-management, cloud, or enterprise security
requirements belong in the solution-level document — do not duplicate them unless the product
itself must explicitly support them. IEC 62443 is the usual industrial basis; record the
applicability decision in `traceability/STANDARDS-MAPPING.md`.

| REQ ID | Req. Statement | Markets (§5.1) | Use Case (§5.2) | Release (§5.3) | Goal (§6) |
|---|---|---|---|---|---|
| CR-01 | [The product shall support authenticated access to its relevant control and configuration interfaces.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| CR-02 | [The product shall protect the integrity of critical control, status, and operational data within its intended connected operating context.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| CR-03 | [The product shall transition or behave safely under defined connectivity loss, degradation, or unauthorized access conditions.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |

[Drop the Release and Goal columns if the project excludes release tracking or discards the
goals section. Promote these to `product/requirements/` artifacts when per-requirement
traceability is needed.]
