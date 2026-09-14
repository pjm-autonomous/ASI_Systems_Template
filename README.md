# SA/SE Project Template

A GitHub template repository for starting a new ASI systems architecture (SA) / systems engineering (SE) project.

Fork this repository (GitHub "Use this template" button) at project kickoff so every project shares the same artifact structure, naming conventions, and validation tooling.

## Sources

This template was

1. Derived from lessons learned building [`prak-v-model`](https://github.com/asirobots/prak-v-model)
2. Generalized for reuse
3. Rescoped against ASI's standards framework (see `reference/standards-framework.md`)

## What This Template Is

This template provides repeatable, architecture-driven traceability. SA-owned artifacts (personas, use cases, requirements, architecture, interfaces, data, deployment, decisions) that every system requires should be clearly labeled. They are foundational for the entire SE lifecycle (safety, coding, testing, QA/CM, change/risk, metrics).

It is a framework to outline systems-related requirements to be populated upon project initiation.

Validation tooling is included to avoid scope-creep and maintain integrity as systems mature.

## Core Artifacts

**One repo is one level.** Which level this repo occupies, and which tiers it
masters, are declared in `repo-standard.yaml`. `standard/tier-schema.md` is
normative and carries the architecture diagram.

```text
L0   stakeholder   personas · use cases
     product       product performance + safety requirements
       │                                    owns interfaces BETWEEN L1 systems
       ▼  crosses a repo boundary
L1   capability    capability requirements
       │                                    owns interfaces BETWEEN L2 systems
       ▼  crosses a repo boundary
L2   system        system requirements
       └─ subsystem   sub-system requirements
            └─ component   component requirements
                                            owns interfaces BETWEEN L3..n
```

| Tier | Level | Description | Directory |
| --- | --- | --- | --- |
| Personas | L0 | Stakeholders who interact with the system across its lifecycle | `stakeholder/personas/` |
| Use Cases | L0 | A specific need a persona has of the system | `stakeholder/use-cases/` |
| Product Requirements | L0 | Product performance and safety requirements satisfying a use case | `product/requirements/` |
| Capability Requirements | L1 | What the platform must be able to do, derived by the Systems Architect | `capability/requirements/` |
| System Requirements | L2 | Engineering decomposition of a capability requirement | `system/requirements/` |
| Sub-system Requirements | L2 | Decomposition of a system requirement | `subsystem/requirements/` |
| Component Requirements | L2 | Decomposition of a sub-system requirement | `component/requirements/` |
| Interfaces | every | The boundaries **this** level owns | `interfaces/` |
| Architecture | every | What those boundaries are drawn on | `architecture/` |
| Data Specifications | L2 | Entity/schema definitions, ownership, retention | `<tier>/data/` |
| Deployment Architecture | L2 | Nodes, environments, networking | `system/deployment/` |
| Program Parameters | most | Values a robot program declares, cited by requirements | `<tier>/parameters/` |
| Architecture Decision Records | every | Why a significant design choice was made | `<tier>/decisions/` |

Two rules do most of the work:

- **An interface is owned by the nearest common ancestor of the parties it
  connects**, and is stated in terms of that owner's *immediate descendants*. Two
  peers cannot arbitrate a boundary they both sit on. An L1 interface says
  *System A ↔ System B* even when the traffic is between sub-systems inside them.
- **Links are established by the child, looking up.** An artifact names its
  parent; the parent level observes coverage. Parents at the level above live in
  another repo and are verified upstream against that repo's published index.

## Full Template Repository Structure

**See [`repo_structure.md`](repo_structure.md)** — it is generated from the repo,
so it cannot drift. This section previously carried a hand-maintained copy of the
same tree; it had already gone stale, still listing a `config/` directory that no
longer exists and omitting `standard/`, `_registry/`, `VERSION` and `CHANGELOG.md`.

The top level, annotated:

| Path | What it is |
| --- | --- |
| `standard/` | **The standard itself.** `decisions.md` (every ratified decision), `tier-schema.md` (normative architecture), `artifact-schema.yaml` (the artifact model as data), `plan.md`, `checklists/` |
| `repo-standard.yaml` | This repo's conformance declaration — level, tiers, packets, parent repos, and the template version it was cut from |
| `VERSION`, `CHANGELOG.md` | The standard is versioned; downstream repos record which version they carry |
| `tools/`, `tests/` | `validate.py` (artifact validator), `schema.py` (model loader), `maturity.py` (M1–M4 gates), `broker.py` (cross-repo upstream enforcement) |
| `templates/` | Blank starting point per artifact type |
| `_registry/` | Maturity promotion evidence — `m2_records/`, `m3_reviews/` |
| `stakeholder/`, `product/`, `capability/`, `system/`, `subsystem/`, `component/` | Artifact tiers. A tier directory exists only if `repo-standard.yaml` declares it |
| `interfaces/`, `architecture/` | The boundaries this level owns, and what they are drawn on |
| `prd/` | PDP-08 PRD section sources |
| `extensions/` | Safety, coding, testing, QA/CM, change/risk, metrics |
| `reference/`, `glossary/`, `traceability/` | BKM set and standards framework, terminology, the generated matrix and standards mapping |
| `example/` | One fictional feature worked end-to-end |
| `.claude/` | Authoring skills and the `derive` gap-analysis agent |

## Naming Conventions

| Artifact | Pattern | Example |
| --- | --- | --- |
| Persona | `<role-or-team>.md` | `remote-operator.md` |
| Use case | `uc-<description>.md` | `uc-geofence-breach-alert.md` |
| Product requirement | `prodreq-<description>.md` | `prodreq-geofence-alert-latency.md` |
| Capability requirement | `capreq-<description>.md` | `capreq-geofence-enforcement.md` |
| System requirement | `sysreq-<description>.md` | `sysreq-geofence-check-interval.md` |
| Sub-system requirement | `subreq-<description>.md` | `subreq-geofence-map-load.md` |
| Component requirement | `compreq-<description>.md` | `compreq-map-validator-checksum.md` |
| Program parameter | `param-<description>.md` | `param-geofence-eval-interval.md` |
| Architecture diagram | `arch-<description>.md` | `arch-geofence-alert-flow.md` |
| Data specification | `data-<description>.md` | `data-geofence-zone-schema.md` |
| Deployment architecture | `deploy-<description>.md` | `deploy-geofence-service-topology.md` |
| Interface control document | `int-<description>.md` | `int-geofence-alert-api.md` |
| Architecture decision record | `adr-NNNN-<description>.md` | `adr-0001-geofence-service-boundary.md` |

All names use kebab-case. Frontmatter cross-references use the filename only (no directory prefix).

## Getting Started With a New Project

1. Click **Use this template** on GitHub to create a new repository from this one.
2. Rename references to "template-repo" in this README and `CLAUDE.md` to your project name — or run the `/new-project` skill in Claude Code, which does this and walks the remaining first-run decisions.
3. Read `CONTRIBUTING.md` and `CLAUDE.md` before authoring your first artifact.
4. **Fill in `repo-standard.yaml`** — the level this repo occupies, the tiers it masters, its parent repo, and the template version it was cut from. `standard/checklists/new-repo.md` walks every step by hand, no tooling required.
5. Author artifacts for the tiers your level owns. An L1 repo authors capability requirements; an L2 repo authors system → sub-system → component requirements. Every repo authors the interfaces and architecture it owns.
6. `traceability/TRACEABILITY.md` is **generated** — do not hand-maintain it. Record standards applicability in `traceability/STANDARDS-MAPPING.md` as you go.
7. When a stakeholder-facing PRD (PDP-08) is needed, author the governance sections in `prd/sections/` — each ships as a stub carrying the official template's structure, tables, and owner defaults; `prd/README.md` maps every PDP-08 section to its stub or its generating artifact set.
8. When a project matures into needing safety, coding, testing, QA/CM, change/risk, or metrics documentation, open the matching folder under `extensions/` — each has a stub explaining what a complete document looks like per `reference/bkm-document-set.md`.
9. Install `pre-commit` locally (see `CONTRIBUTING.md`) so validation runs before every commit; the same checks run in CI.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the authoring workflow, branching model, and validation instructions.
