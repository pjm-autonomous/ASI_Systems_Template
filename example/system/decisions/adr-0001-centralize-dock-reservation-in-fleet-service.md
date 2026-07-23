---
id: adr-0001
title: Centralize Dock Reservation in Fleet Coordination Service
status: accepted
date: 2026-07-22
---

## Context

Multiple robots may cross the low-battery threshold near the same time and could race for the same dock if reservation logic lived on each robot independently.

## Options Considered

| Option | Tradeoffs |
|---|---|
| Per-robot local reservation with peer negotiation | No single point of failure, but complex distributed-consensus logic for a low-frequency event |
| Centralized reservation in fleet-coordination-service | Simple, consistent; introduces a service dependency for this flow |

## Decision

Centralize dock reservation in fleet-coordination-service (`sysreq-dock-availability-check`).

## Rationale

Dock-return events are infrequent enough that a centralized service is not a throughput bottleneck, and it eliminates an entire class of race-condition bugs that per-robot negotiation would require careful distributed-systems work to avoid.

## Implications / Follow-ups

fleet-coordination-service becomes a dependency for this flow — its availability requirements are captured in `deploy-fleet-coordination-topology.md` (active/standby). If it becomes a bottleneck at larger fleet sizes, revisit.
