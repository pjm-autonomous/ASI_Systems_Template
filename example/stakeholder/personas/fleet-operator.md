---
id: fleet-operator
title: Fleet Operator
class: runtime-operator
---

## Summary

A human who monitors and manages a fleet of warehouse robots from a fleet-management console during a shift. Responds to exceptions the fleet can't resolve on its own.

## Class

runtime-operator

## Responsibilities / Goals

- Keep the fleet productive with minimal manual intervention
- Notice and respond to robots that need help (stuck, faulted, low battery with no path to a dock)
- Approve manual overrides when the automated system can't resolve a situation

## Boundaries

Does not manually route individual robots to docks under normal operation — that's the system's job (see `uc-low-battery-return-to-dock.md`). Only intervenes on exception.
