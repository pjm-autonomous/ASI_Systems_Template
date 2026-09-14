---
id: sysreq-dock-availability-check
title: Dock Availability Check and Reservation
parent-capability-requirements:
  - capreq-autonomous-return-to-dock.md
allocation: fleet-coordination-service
priority: Must Have
---

| Field | Value |
|---|---|
| ID | sysreq-dock-availability-check |
| Parent Capability Requirement | capreq-autonomous-return-to-dock.md |
| Allocation | fleet-coordination-service |
| Priority | Must Have |

## Requirement Statement

When a dock-return request is received, the fleet-coordination-service shall reserve the nearest available dock for the requesting robot, or return an unavailability response if none exists.

## Rationale

Centralizing reservation avoids two robots racing for the same dock; see `adr-0001-centralize-dock-reservation-in-fleet-service.md`.

## Acceptance Criteria

- No two robots are ever assigned the same dock reservation concurrently.
- Unavailability response returned within 1 second when no dock is free.
