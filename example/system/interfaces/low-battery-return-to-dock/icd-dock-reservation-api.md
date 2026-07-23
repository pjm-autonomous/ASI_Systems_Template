---
id: icd-dock-reservation-api
title: Dock Reservation API
parent-product-requirement: req-autonomous-return-to-dock.md
owning-component: fleet-coordination-service
consumers:
  - power-management-service
---

| Field | Value |
|---|---|
| Owning Component | fleet-coordination-service |
| Consumers | power-management-service |
| Parent Product Requirement | req-autonomous-return-to-dock.md |

## Purpose

Lets a robot's power-management-service request and receive a dock reservation without needing to know about other robots' reservations.

## Contract

### Data Schema

`ReserveDockRequest { robot_id: string, position: {x, y, zone_id} }`
`ReserveDockResponse { status: "reserved" | "unavailable", dock_id?: string, dock_pose?: {x, y, heading} }`

### Protocol / Transport

Internal RPC over the fleet message bus, request/response pattern.

### Behavioral Semantics

Single request per dock-return event; the service does not retry automatically. Caller (power-management-service) decides retry policy on `unavailable`.

### Error Handling & Status Model

`unavailable` is a normal response, not an error. Transport-level failures (timeout, disconnect) are the caller's responsibility to detect and retry.

### Security Properties

Internal service-to-service call within the fleet network boundary; not exposed externally. Standard internal service authentication applies (see project-level security architecture once authored).

### Versioning & Compatibility Policy

Additive fields only within a major version; breaking changes require a new endpoint version and a deprecation window for the old one.
