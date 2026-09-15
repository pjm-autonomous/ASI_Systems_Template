---
id: sysreq-battery-threshold-monitor
title: Battery Threshold Monitor
parent-capability-requirements:
  - capreq-autonomous-return-to-dock.md
allocation: power-management-service
priority: Must Have
---

| Field | Value |
|---|---|
| ID | sysreq-battery-threshold-monitor |
| Parent Capability Requirement | capreq-autonomous-return-to-dock.md |
| Allocation | power-management-service |
| Priority | Must Have |

## Requirement Statement

When the reported state of charge drops below the configured low-battery threshold, the power-management-service shall emit a dock-return request within 500 ms.

## Rationale

Detection latency directly bounds how much runway the robot has to safely reach a dock before a harder power fault.

## Acceptance Criteria

- Dock-return request observed on the internal event bus within 500 ms of the state-of-charge reading crossing the threshold, measured across 100 simulated discharge trials.

The threshold crossed is the one declared in `param-battery-reserve-threshold.md`.
Stating it by name rather than as a number is what makes this criterion testable
against a site that re-derives the value: the trial reads the parameter, not a
figure copied into prose here that would then have to be found and changed.
