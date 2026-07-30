---
name: deployment-arch
description: Create or update a deployment architecture document in system/deployment/<feature>/. Use when the user wants to document nodes, environments, networking, or scaling topology.
---

# Skill: deployment-arch

Create or update a deployment architecture artifact in `system/deployment/<feature>/`.

Deployment architecture is cross-cutting — it documents where the system runs (nodes, environments, networking, scaling) and can span multiple features. It is not a child of any single requirement, so it does not appear in the traceability matrix.

## Create flow

Ask the user for:

- Document title (short description for the filename, e.g. `fleet-coordination-topology`)
- Scope — `whole-system`, or a specific feature bucket name if the document covers one feature's topology
- A brief description of the deployment: nodes/environments, execution units, and anything known about networking or scaling

Choose the directory from the scope:

- Feature-scoped → `system/deployment/<feature>/` (reuse the feature's existing bucket name)
- Whole-system → `system/deployment/whole-system/` (the validator requires every deployment doc to live in a subdirectory bucket)

Then:

1. Create `system/deployment/<bucket>/deploy-<short-description>.md` from `templates/deployment-architecture.md`. Create the bucket directory if it doesn't exist.
2. Populate YAML frontmatter:
   - `id`: filename without the `.md` extension
   - `title`: human-readable title
   - `scope`: `whole-system` or the feature bucket name
3. Fill the sections — `TBD` for anything unknown rather than deleting the heading:
   - **Nodes / Environments** — on-prem vs cloud vs edge; regions/availability zones; dev/test/prod environments
   - **Execution Units** — services, containers, processes, functions
   - **Networking & Connectivity** — segmentation model, routing/load balancing, ingress/egress model
   - **Scaling & Availability** — replication, failover, capacity assumptions
4. Optionally include a Mermaid deployment diagram (`flowchart` with subgraphs for nodes) — follow the **Mermaid conventions** in `.claude/skills/architecture/SKILL.md`. Note: a formal `arch-*.md` diagram with `diagram-type: deployment` belongs in `system/architecture/` instead when it needs to trace to a product requirement.

Finish by running `python tools/validate.py` from the repo root and fixing anything it reports.

## Update flow

If the deployment doc already exists:

1. Locate it under `system/deployment/` and read it
2. Ask the user what needs to change
3. Apply only the requested changes — do not regenerate the whole file
4. Re-run `python tools/validate.py`

## Conventions

- Filename: `deploy-<short-description>.md` in kebab-case
- Tables are plain Markdown, never HTML `<table>` markup
- Examples: `deploy-geofence-service-topology.md`, `deploy-fleet-coordination-topology.md`
