---
id: subreq-battery-state-sampling
title: Battery State Sampling Interval
parent-system-requirements:
  - sysreq-battery-threshold-monitor.md
allocation: battery-management-subsystem
priority: Must Have
component-type: Software
requirement-type: Functional
verification-method: Test
---

| Field | Value |
|---|---|
| ID | subreq-battery-state-sampling |
| Parent System Requirements | sysreq-battery-threshold-monitor.md |
| Allocation | battery-management-subsystem |
| Component Type | Software |
| Requirement Type | Functional |
| Priority | Must Have |
| Verification Method | Test |

## Requirement Statement

While a robot is under power, the battery management subsystem shall sample pack
state of charge at least once per second.

## Rationale

The system requirement above must detect the reserve threshold without
overshooting it. At the fleet's maximum speed a robot covers roughly 1.5 m per
second, so a sampling interval longer than one second lets a robot travel further
past the threshold than the return-path margin allows.

## Acceptance Criteria

1. Sample interval does not exceed 1 s under maximum compute load.
2. A missed sample is logged, and two consecutive misses raise a fault.
