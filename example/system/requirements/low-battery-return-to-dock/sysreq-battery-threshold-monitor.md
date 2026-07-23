---
id: sysreq-battery-threshold-monitor
title: Battery Threshold Monitor
parent-product-requirement: req-autonomous-return-to-dock.md
parent-use-cases:
  - uc-low-battery-return-to-dock.md
allocation: power-management-service
priority: High
---

| Field | Value |
|---|---|
| ID | sysreq-battery-threshold-monitor |
| Parent Product Requirement | req-autonomous-return-to-dock.md |
| Parent Use Cases | uc-low-battery-return-to-dock.md |
| Allocation | power-management-service |
| Priority | High |

## Requirement Statement

When the reported state of charge drops below the configured low-battery threshold, the power-management-service shall emit a dock-return request within 500 ms.

## Rationale

Detection latency directly bounds how much runway the robot has to safely reach a dock before a harder power fault.

## Acceptance Criteria

- Dock-return request observed on the internal event bus within 500 ms of the state-of-charge reading crossing the threshold, measured across 100 simulated discharge trials.
