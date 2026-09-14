---
id: param-battery-reserve-threshold
title: Battery Reserve Threshold
value: 20
unit: percent state-of-charge
---

| Field | Value |
|---|---|
| ID | param-battery-reserve-threshold |
| Value | 20 |
| Unit | percent state-of-charge |
| Declared by | Fleet operations, per site |
| Applies to | All robots in the fleet |

## Definition

The state of charge, as reported by the battery management system at the pack
terminals, at or below which a robot must begin returning to a dock.

Measured at the pack, not at the motor controller — the two differ under load,
and a threshold measured downstream would trigger late during a heavy-lift task,
which is exactly when the margin matters.

## Basis

Site survey: the longest return path in the reference warehouse is 180 m, and a
loaded robot consumes 11–14% state-of-charge over that distance at the slowest
permitted speed. 20% leaves margin for one re-route around a blocked aisle.

**Site-specific.** A site with longer aisles must re-derive this value rather
than inherit it. A deployment that has not run the survey should treat this as a
placeholder and say so, not carry it as settled.

## Cited By

- `prodreq-return-before-depletion.md`
- `sysreq-battery-threshold-monitor.md`
