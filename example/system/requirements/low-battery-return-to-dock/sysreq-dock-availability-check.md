---
id: sysreq-dock-availability-check
title: Dock Availability Check and Reservation
parent-product-requirement: req-autonomous-return-to-dock.md
parent-use-cases:
  - uc-low-battery-return-to-dock.md
allocation: fleet-coordination-service
priority: High
---

| Field | Value |
|---|---|
| ID | sysreq-dock-availability-check |
| Parent Product Requirement | req-autonomous-return-to-dock.md |
| Parent Use Cases | uc-low-battery-return-to-dock.md |
| Allocation | fleet-coordination-service |
| Priority | High |

## Requirement Statement

When a dock-return request is received, the fleet-coordination-service shall reserve the nearest available dock for the requesting robot, or return an unavailability response if none exists.

## Rationale

Centralizing reservation avoids two robots racing for the same dock; see `adr-0001-centralize-dock-reservation-in-fleet-service.md`.

## Acceptance Criteria

- No two robots are ever assigned the same dock reservation concurrently.
- Unavailability response returned within 1 second when no dock is free.
