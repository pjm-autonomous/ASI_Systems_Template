---
pdp-08-section: "Safety Requirements"
pdp-08-ref: "§7.3"
status: stub
owner: Functional Safety   # clearly-owned domain — confirm per project
---

# Safety Requirements

<!-- STUB -->

Structure from PDP-08 rev A §7.3. Safety is a first-class product requirement here, not only
an engineering or compliance activity: define the safety outcomes and constraints required for
the product to operate in its intended environments — interaction with people, equipment, site
conditions, and degraded states. Write outcome statements using "shall"; keep each requirement
singular and testable in intent.

**Safety-integrity single source:** do not state a default performance level (PLr/SIL) in this
section, in requirement templates, or in validators. The project's governing safety-integrity
document (e.g. `extensions/safety/functional-safety-concept.md` or a dedicated governing
document) is the one authoritative source for default integrity targets; requirements
reference it. Ground integrity claims in established standards — ISO 13849-1 (PL) / IEC 62061
(SIL), with IEC 60204-1 stop-category vocabulary; record any organization-specific rating
scheme's mapping to those standards in the governing document before adopting it.

| REQ ID | Req. Statement | Markets (§5.1) | Use Case (§5.2) | Release (§5.3) | Goal (§6) |
|---|---|---|---|---|---|
| SR-01 | [The product shall operate within defined safety boundaries for intended human, equipment, and site interactions.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| SR-02 | [The product shall support clear and appropriate transitions to a safe state when required conditions for operation are not met.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| SR-03 | [The product shall provide the safety-related behaviors, indications, and controls needed for intended users to supervise and interact with it appropriately.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |

[Drop the Release and Goal columns if the project excludes release tracking or discards the
goals section (PRAK precedent, 2026-07-27). Safety-analysis evidence — HARA, FMEA, safety
case — lives in `extensions/safety/`; safety-flagged requirements trace there.]
