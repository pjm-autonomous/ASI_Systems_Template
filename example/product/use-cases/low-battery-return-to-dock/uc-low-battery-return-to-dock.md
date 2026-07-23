---
id: uc-low-battery-return-to-dock
title: Low-Battery Return to Dock
primary-actors:
  - fleet-operator
parent-personas:
  - fleet-operator
---

| Field | Value |
|---|---|
| ID | uc-low-battery-return-to-dock |
| Primary Actors | fleet-operator |
| Parent Personas | fleet-operator |

## Description

As a fleet operator, I need robots to autonomously return to a charging dock when their battery runs low, without me having to notice and manually route them, so the fleet stays productive without constant supervision.

## Preconditions

- Robot is in autonomous operating mode
- At least one dock exists in the robot's operating zone

## Main Flow

1. Robot's battery state of charge drops below the low-battery threshold.
2. System reserves the nearest available dock.
3. Robot navigates to the reserved dock and begins charging.
4. Fleet operator sees the transition reflected on the fleet console; no action required.

## Alternate / Exception Flows

- No dock is available within range → robot reports the exception; fleet operator is notified and may intervene manually.

## Postconditions

- Robot is docked and charging, or the fleet operator has been notified of an exception.

## Notes

Illustrative example — see `example/README.md`.
