# Traceability Matrix (Example)

Formatted exactly as it would appear in the real `traceability/TRACEABILITY.md` at the repo root, using this example feature's artifacts.

| Persona | Use Case | Product Requirement | System Requirement | Architecture | ICD | Data Spec |
|---|---|---|---|---|---|---|
| fleet-operator | uc-low-battery-return-to-dock | req-autonomous-return-to-dock | sysreq-battery-threshold-monitor | arch-dock-return-flow | icd-dock-reservation-api | data-dock-reservation-schema |
| fleet-operator | uc-low-battery-return-to-dock | req-autonomous-return-to-dock | sysreq-dock-availability-check | arch-dock-return-flow | icd-dock-reservation-api | data-dock-reservation-schema |

`adr-0001-centralize-dock-reservation-in-fleet-service` and `deploy-fleet-coordination-topology` are cross-cutting and referenced from the architecture/system-requirement content rather than given their own matrix column.
