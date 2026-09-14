<!-- GENERATED FILE - DO NOT EDIT.
     Produced by tools/trace.py from artifact frontmatter (D-46).
     Regenerate with `build-traceability`; CI runs `--check`.
     Editing this file by hand is reverted by the next run. -->

# Traceability Matrix

8 artifact(s) across 7 traceable tier(s), 2 lineage path(s).

| Persona | Use Case | Product Requirement | Capability Requirement | System Requirement | Subsystem Requirement | Component Requirement |
|---|---|---|---|---|---|---|
| fleet-operator.md | uc-low-battery-return-to-dock.md | prodreq-return-before-depletion.md | capreq-autonomous-return-to-dock.md | sysreq-battery-threshold-monitor.md | subreq-battery-state-sampling.md | compreq-voltage-sampler-rate.md |
| fleet-operator.md | uc-low-battery-return-to-dock.md | prodreq-return-before-depletion.md | capreq-autonomous-return-to-dock.md | sysreq-dock-availability-check.md |  |  |

- `†` parent is in the upstream repo; its existence is checked by `tools/broker.py`, not here.
- `‡` named as a parent but not found in this repo and not declared external — `validate-artifacts` reports it.

## Artifacts with no declared lineage

These types declare no `parent-*` field in the artifact schema, so there is no edge to trace. They are listed rather than given a matrix column, because a column that can only be blank reads as a gap and a guessed link reads as a fact.

| Type | Artifact |
|---|---|
| ADR | adr-0001-centralize-dock-reservation-in-fleet-service.md |
| Architecture | arch-dock-return-flow.md |
| Data Specification | data-dock-reservation-schema.md |
| Deployment Architecture | deploy-fleet-coordination-topology.md |
| ICD | int-dock-reservation-api.md |
| Parameter | param-battery-reserve-threshold.md |
