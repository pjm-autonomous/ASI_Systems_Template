---
artifact-type: deployment-architecture
tier: system
---

# Deployment Architecture

- [What belongs here](#what-belongs-here)
- [One document per topology concern](#one-document-per-topology-concern)
- [Availability and safety-relevant topology](#availability-and-safety-relevant-topology)
- [Relationship to architecture diagrams](#relationship-to-architecture-diagrams)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `system/deployment/deploy-<description>.md`, optionally grouped
into a feature-bucket directory. Start from
`templates/deployment-architecture.md`.

## What belongs here

Where a system requirement's `allocation` says **which** part does something, a
deployment architecture says **where that part runs**: nodes and environments
(on-premises, cloud, edge; regions; dev, test, production), execution units
(services, containers, processes), networking and segmentation, and scaling and
availability characteristics.

`scope` is required. It is either a feature-bucket name or `whole-system` for
topology that is not specific to one feature.

A deployment architecture carries **no parent requirement**. Like architecture
and data specifications, it is context several requirements are written against
rather than a decomposition of any one of them.

## One document per topology concern

**Not one per service.** Create one per meaningfully distinct topology — often
one per feature, plus a `whole-system` document covering shared infrastructure
(network segmentation, shared data stores, deployment targets) that belongs to no
single feature.

The test is whether two topologies could change independently. If deploying
feature A never affects where feature B runs, they are two documents.

## Availability and safety-relevant topology

Where a component's availability characteristics are **safety-relevant** — a stop
authority path that must have no single point of failure, for instance — say so
explicitly in the Scaling and Availability section, and cross-reference the
system requirement that drives it.

Do not leave an availability obligation implicit in a diagram. A topology picture
showing two instances does not say whether two are *required*, and the difference
is the whole of the safety argument.

## Relationship to architecture diagrams

A `deployment` diagram in `architecture/` and a deployment architecture document
here are not duplicates. The diagram shows the shape; this document states the
obligations — environments, segmentation, scaling rules, availability targets.

Where both exist, the diagram should reference this document rather than
restating its numbers.

## Maturity

Deployment architecture starts at `M1`. A state at or above `M2` requires a dated
promotion record in `_registry/` — see
[`standard/decisions.md`](../../standard/decisions.md) D-40 … D-43.
