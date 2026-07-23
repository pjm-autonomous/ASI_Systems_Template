---
id: data-dock-reservation-schema
title: Dock Reservation Schema
parent-product-requirement: req-autonomous-return-to-dock.md
---

| Field | Value |
|---|---|
| Owner (source of truth) | fleet-coordination-service |
| Parent Product Requirement | req-autonomous-return-to-dock.md |

## Entity Definition

A `DockReservation` represents one robot's claim on one dock for the duration of a charging cycle.

## Schema

| Field | Type | Constraints | Description |
|---|---|---|---|
| reservation_id | string (UUID) | required, unique | Reservation identifier |
| robot_id | string | required | Robot holding the reservation |
| dock_id | string | required | Reserved dock |
| created_at | timestamp | required | When the reservation was made |
| released_at | timestamp | nullable | When the reservation ended, if it has |

## Relationships

One `DockReservation` references exactly one robot and one dock. A dock has at most one active (unreleased) reservation at a time.

## Lifecycle

Created when `sysreq-dock-availability-check` succeeds. Released when the robot begins charging confirmation, or on timeout if the robot never arrives.

## Storage & Retention

Stored in fleet-coordination-service's operational database. Active reservations only; released reservations move to a rolling 30-day history table for diagnostics.

## Validation Rules

`dock_id` must reference a dock that exists and is not already actively reserved at creation time.
