# Traceability Matrix (Example)

> **Shown filled in so the shape is visible.** In a real repo this matrix is
> **generated from frontmatter** (D-46) and never hand-written — a
> hand-maintained matrix is what produced 316 rows with 0 populated in the
> repo this standard learned from.

Formatted exactly as it would appear in the real `traceability/TRACEABILITY.md` at the repo root, using this example feature's artifacts.

| Persona | Use Case | Capability Requirement | System Requirement | Architecture | ICD | Data Spec |
|---|---|---|---|---|---|---|
| fleet-operator | uc-low-battery-return-to-dock | capreq-autonomous-return-to-dock | sysreq-battery-threshold-monitor | arch-dock-return-flow | int-dock-reservation-api | data-dock-reservation-schema |
| fleet-operator | uc-low-battery-return-to-dock | capreq-autonomous-return-to-dock | sysreq-dock-availability-check | arch-dock-return-flow | int-dock-reservation-api | data-dock-reservation-schema |

`adr-0001-centralize-dock-reservation-in-fleet-service` and `deploy-fleet-coordination-topology` are cross-cutting and referenced from the architecture/system-requirement content rather than given their own matrix column.
