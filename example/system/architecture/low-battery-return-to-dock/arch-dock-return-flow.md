---
id: arch-dock-return-flow
title: Dock Return Flow
parent-product-requirement: req-autonomous-return-to-dock.md
diagram-type: sequence
---

| Field | Value |
|---|---|
| Purpose | Show the sequence of calls from battery-threshold detection through dock reservation to navigation start |
| Scope | low-battery-return-to-dock feature |
| Notes | Dock reservation is centralized in fleet-coordination-service per `adr-0001-centralize-dock-reservation-in-fleet-service.md` |

```mermaid
sequenceDiagram
    participant PM as power-management-service
    participant FC as fleet-coordination-service
    participant NAV as navigation-service

    PM->>FC: dock-return request (robot_id, position)
    FC->>FC: find nearest available dock
    alt dock available
        FC-->>PM: dock reserved (dock_id, pose)
        PM->>NAV: navigate-to(dock_id, pose)
        NAV-->>PM: arrived + charging started
    else no dock available
        FC-->>PM: unavailable
        PM->>PM: raise exception to fleet console
    end
```
