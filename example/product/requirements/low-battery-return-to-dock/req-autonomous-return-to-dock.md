---
id: req-autonomous-return-to-dock
title: Autonomous Return to Dock on Low Battery
parent-use-cases:
  - uc-low-battery-return-to-dock
priority: High
---

| Field | Value |
|---|---|
| ID | req-autonomous-return-to-dock |
| Parent Use Cases | uc-low-battery-return-to-dock |
| Priority | High |

## Requirement Statement

When a robot's battery state of charge drops below the configured low-battery threshold, the system shall autonomously route the robot to an available charging dock without requiring operator action.

## Rationale

Manual dock routing does not scale with fleet size and introduces avoidable downtime while waiting for operator attention.

## Acceptance Criteria

- Robot reaches a dock and begins charging without any operator input, for the common case where a dock is available.
- If no dock is available, the system raises an exception visible on the fleet console within 5 seconds of the threshold being crossed.
