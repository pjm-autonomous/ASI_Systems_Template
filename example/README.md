# Example: Low-Battery Return-to-Dock

A single fictional feature, worked end-to-end through every core artifact type, so you can see how the pieces connect before authoring your own. It is illustrative only — not a real ASI product feature, and deliberately generic (warehouse fleet robotics) so it doesn't read as authoritative guidance for any specific ASI product.

## The Chain

```text
fleet-operator.md (persona)
  └─ uc-low-battery-return-to-dock.md (use case)
       └─ req-autonomous-return-to-dock.md (product requirement)
            ├─ sysreq-battery-threshold-monitor.md (system requirement, allocation: power-management-service)
            ├─ sysreq-dock-availability-check.md (system requirement, allocation: fleet-coordination-service)
            ├─ arch-dock-return-flow.md (architecture, sequence diagram)
            ├─ icd-dock-reservation-api.md (ICD, fleet-coordination-service → robot navigation client)
            └─ data-dock-reservation-schema.md (data specification)
adr-0001-centralize-dock-reservation-in-fleet-service.md (ADR — cross-cutting, referenced from the architecture diagram)
deploy-fleet-coordination-topology.md (deployment architecture — cross-cutting)
```

See `traceability/TRACEABILITY.md` in this folder for the filled-in matrix row, formatted exactly as it would appear in the real `traceability/TRACEABILITY.md` at the repo root.

Copy the pattern, not the content — swap in your own persona, feature name, and allocations.
