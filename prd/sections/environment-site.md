---
pdp-08-section: "Environmental / Site Requirements (ER / STR)"
pdp-08-ref: "§7.5"
status: stub
owner: Functional Safety   # clearly-owned domain — confirm per project
---

# Environmental / Site Requirements

<!-- STUB -->

Structure from PDP-08 rev A §7.5. These requirements establish the intended operating envelope
so requirements, KPIs, architecture, and validation planning are interpreted in the proper
context. Capture only conditions that materially affect product scope, safety, performance,
readiness, or customer expectation — not a full engineering decomposition, ODD taxonomy, or
verification plan. Make clear whether each condition is a required capability, an assumption
(provided by the site or another system), an exclusion, or a deferred future need.

## Environmental Requirements

Conditions the product must tolerate, interpret, or operate within:

| REQ ID | Req. Statement | Markets (§5.1) | Use Case (§5.2) | Release (§5.3) | Goal (§6) |
|---|---|---|---|---|---|
| ER-01 | [The product shall operate within the defined ambient temperature range for the intended market, use case, and release.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| ER-02 | [The product shall tolerate the expected dust, debris, visibility, and surface contamination conditions of the intended environment.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| ER-03 | [The product shall operate within the defined terrain, grade, and surface-condition limits for the intended market and release.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |

## Site Requirements

Site conditions, infrastructure assumptions, and operational-context expectations — state who
provides each (the site, another system, or the product itself):

| REQ ID | Req. Statement | Markets (§5.1) | Use Case (§5.2) | Release (§5.3) | Goal (§6) |
|---|---|---|---|---|---|
| STR-01 | [The product shall operate with the defined positioning, localization, or correction-service assumptions for the intended site context.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| STR-02 | [The product shall operate with the defined communications and connectivity conditions for the intended release.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |
| STR-03 | [The product shall support operation within the defined work-zone, geofence, or site-boundary structure for the intended use case.] | [Market(s)] | [Use case(s)] | [Release] | [Goal(s)] |

## Consideration Checklist

PDP-08 rev A Appendix A carries the full Environmental and Site Consideration Library with
classification scales (Beaufort wind, precipitation rates, illuminance, oktas, etc.); consult
the controlled template when authoring. Topic areas to screen — promote a condition into the
tables above only when it materially shapes the product boundary or release commitment:

- Weather and atmospheric conditions (temperature, wind, rain, snow, humidity, hail)
- Particulates and visibility (dust, sand, smoke, spray; perception impact)
- Illumination and sky conditions (day/night, artificial light, glare, sun angle)
- Connectivity and positioning (comms type/technology, throughput/latency, GNSS/RTK dependency)
- Traffic agents and special vehicles (people, equipment, animals; density and flow)
- Scenery and operating-zone context (geofences, zone types, structures, barriers)
- Junctions and road structures (intersections, crossings, bridges, gates)
- Drivable-area definition (surface types, geometry, lane structure, edges, markings)
- Temporary structures and off-nominal conditions (work zones, layout changes, degradation, weather transitions)
