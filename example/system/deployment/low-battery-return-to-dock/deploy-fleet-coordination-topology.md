---
id: deploy-fleet-coordination-topology
title: Fleet Coordination Service Deployment Topology
scope: low-battery-return-to-dock
---

## Nodes / Environments

fleet-coordination-service runs on-site (on-prem edge server) per warehouse deployment — not cloud-hosted, to keep dock-reservation latency low and functioning during connectivity loss to any central system.

## Execution Units

Single containerized service per site, active/standby pair for availability.

## Networking & Connectivity

Communicates with per-robot power-management-service and navigation-service over the site's local fleet network. No direct external/internet exposure.

## Scaling & Availability

Active/standby failover within a site; no cross-site sharing of dock reservations (each site's docks are independent).
