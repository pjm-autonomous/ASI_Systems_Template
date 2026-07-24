# Deployment Architecture

Grouped by feature bucket, or `whole-system` for a project-wide topology doc: `system/deployment/<feature>/deploy-<description>.md`. Start from `templates/deployment-architecture.md`. See `example/system/deployment/low-battery-return-to-dock/deploy-fleet-coordination-topology.md` for a worked sample.

## What Belongs Here

Where a system requirement's `allocation` says *which component* does something, a deployment architecture doc says *where that component runs*: nodes/environments (on-prem/cloud/edge, regions, dev/test/prod), execution units (services, containers, processes), networking/segmentation, and scaling/availability characteristics. `scope` in the frontmatter is either a feature-bucket name or `whole-system` for topology that isn't specific to one feature.

## One Doc Per Topology Concern, Not Per Component

Don't create a deployment doc per microservice. Create one per meaningfully distinct deployment topology — often that's one per feature bucket (as in the example) plus one `whole-system` doc covering shared infrastructure (network segmentation, shared databases, CI/CD deployment targets) that doesn't belong to any single feature.

## Availability and Safety-Relevant Topology

If a component's availability characteristics are safety-relevant (e.g., a stop-authority path that must not have a single point of failure), say so explicitly in the "Scaling & Availability" section and cross-reference the driving system requirement — don't leave availability requirements implicit in an architecture diagram alone.
