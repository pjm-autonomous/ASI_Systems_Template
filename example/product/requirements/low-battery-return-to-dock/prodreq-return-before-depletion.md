---
id: prodreq-return-before-depletion
title: Return to Dock Before Battery Depletion
parent-use-cases:
  - uc-low-battery-return-to-dock.md
priority: Must Have
requirement-type: Functional
verification-method: Test
---

| Field | Value |
|---|---|
| ID | prodreq-return-before-depletion |
| Parent Use Cases | uc-low-battery-return-to-dock.md |
| Requirement Type | Functional |
| Priority | Must Have |
| Verification Method | Test |

## Requirement Statement

When a robot's remaining charge falls to the reserve threshold, the system shall
return the robot to a dock before the charge is exhausted.

## Rationale

A robot that depletes in an aisle blocks the aisle and needs manual recovery,
which is the outcome the fleet operator's use case exists to avoid. Stating the
obligation at the product tier keeps it stakeholder-facing: it says the robot
gets back, not how the platform works out that it needs to.

## Acceptance Criteria

1. A robot that reaches the reserve threshold arrives at a dock without operator
   intervention.
2. A robot that cannot reach a dock raises an alert before it is stranded rather
   than after.

The reserve threshold is not written here as a number. It is declared once in
`param-battery-reserve-threshold.md` and cited by name — see that artifact for
the value and its basis.
