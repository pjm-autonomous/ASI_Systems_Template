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

```text
Personas
  └─ Use Cases
       └─ Product Requirements
            ├─ System Requirements
            ├─ Architecture Diagrams
            ├─ Interface Control Documents (ICDs)
            └─ Data Specifications
```

Architecture decisions (ADRs) and deployment architecture cover multiple levels in the hierarchy of artifacts. They are not children of any one artifact, but the system as a whole.

| Layer | Description | Directory |
| --- | --- | --- |
| Personas | Stakeholders who interact with the system across its lifecycle | `product/personas/` |
| Use Cases | A specific need a persona has of the system | `product/use-cases/<feature>/` |
| Product Requirements | Stakeholder-facing obligations that satisfy a use case | `product/requirements/<feature>/` |
| System Requirements | Engineering decomposition of a product requirement, allocated to a component/subsystem | `system/requirements/<feature>/` |
| Architecture Diagrams | Mermaid diagrams (structure, behavior, deployment) tracing to a product requirement | `system/architecture/<feature>/` |
| Data Specifications | Entity/schema definitions, ownership, retention | `system/data/<feature>/` |
| Deployment Architecture | Nodes, environments, networking | `system/deployment/<feature>/` |
| Interface Control Documents | Contracts between components/subsystems/external systems | `system/interfaces/<feature>/` |
| Architecture Decision Records | Why a significant design choice was made | `system/decisions/` |

## Full Template Repository Structure

```text
template-repo/
├─ README.md
├─ CLAUDE.md
├─ NOTICE.md
├─ SECURITY.md
├─ TODO.md
├─ .editorconfig
├─ .markdownlint.yaml
├─ .markdownlintignore
├─ pyproject.toml
├─ .pre-commit-config.yaml
├─ CONTRIBUTING.md
├─ .claude/
│  ├─ agents/
│  │  └─ derive.md
│  └─ skills/            (one SKILL.md per directory)
│     ├─ persona/
│     ├─ use-case/
│     ├─ product-requirement/
│     ├─ system-requirement/
│     ├─ architecture/
│     ├─ icd/
│     ├─ data-spec/
│     ├─ deployment-arch/
│     ├─ adr/
│     ├─ requirement/
│     └─ new-project/
├─ templates/
│  ├─ README.md
│  ├─ persona.md
│  ├─ use-case.md
│  ├─ product-requirement.md
│  ├─ system-requirement.md
│  ├─ architecture-diagram.md
│  ├─ icd.md
│  ├─ data-specification.md
│  ├─ deployment-architecture.md
│  └─ adr.md
├─ reference/
│  ├─ README.md
│  ├─ bkm-document-set.md
│  ├─ standards-framework.md
│  └─ tooling-recommendations.md
├─ traceability/
│  ├─ README.md
│  ├─ TRACEABILITY.md
│  └─ STANDARDS-MAPPING.md
├─ glossary/
│  ├─ README.md
│  └─ GLOSSARY.md
├─ product/
│  ├─ personas/
│  │  └─ README.md
│  ├─ use-cases/
│  │  └─ README.md
│  └─ requirements/
│     └─ README.md
├─ system/
│  ├─ requirements/
│  │  └─ README.md
│  ├─ architecture/
│  │  └─ README.md
│  ├─ data/
│  │  └─ README.md
│  ├─ deployment/
│  │  └─ README.md
│  ├─ interfaces/
│  │  └─ README.md
│  └─ decisions/
│     └─ README.md
├─ prd/
│  ├─ README.md
│  ├─ meta.yaml
│  ├─ change-log.md
│  └─ sections/
│     ├─ scope.md
│     ├─ standards.md
│     ├─ raci.md
│     ├─ overview.md
│     ├─ markets.md
│     ├─ release-plan.md
│     ├─ goals.md
│     ├─ kpis.md
│     ├─ safety.md
│     ├─ security.md
│     ├─ environment-site.md
│     └─ performance.md
├─ extensions/
│  ├─ README.md
│  ├─ safety/
│  │  ├─ safety-management-plan.md
│  │  ├─ hazard-analysis-and-risk-assessment.md
│  │  ├─ functional-safety-concept.md
│  │  ├─ fmea.md
│  │  └─ safety-case.md
│  ├─ coding/
│  │  ├─ coding-standard.md
│  │  ├─ static-analysis-standard.md
│  │  ├─ code-review-procedure.md
│  │  └─ build-and-integration-procedure.md
│  ├─ testing/
│  │  ├─ test-strategy.md
│  │  ├─ unit-testing-standard.md
│  │  ├─ integration-testing-procedure.md
│  │  ├─ system-testing-plan.md
│  │  └─ test-coverage-analysis.md
│  ├─ qa-cm/
│  │  ├─ quality-assurance-plan.md
│  │  ├─ configuration-management-plan.md
│  │  ├─ version-control-standard.md
│  │  └─ development-environment-standard.md
│  ├─ change-risk/
│  │  ├─ change-management-procedure.md
│  │  └─ risk-register.md
│  └─ metrics/
│     ├─ metrics-program.md
│     └─ lessons-learned.md
├─ example/
│  ├─ README.md
│  ├─ product/
│  │  ├─ personas/
│  │  │  └─ fleet-operator.md
│  │  ├─ use-cases/
│  │  │  └─ low-battery-return-to-dock/
│  │  │     └─ uc-low-battery-return-to-dock.md
│  │  └─ requirements/
│  │     └─ low-battery-return-to-dock/
│  │        └─ req-autonomous-return-to-dock.md
│  ├─ system/
│  │  ├─ requirements/
│  │  │  └─ low-battery-return-to-dock/
│  │  │     ├─ sysreq-battery-threshold-monitor.md
│  │  │     └─ sysreq-dock-availability-check.md
│  │  ├─ architecture/
│  │  │  └─ low-battery-return-to-dock/
│  │  │     └─ arch-dock-return-flow.md
│  │  ├─ interfaces/
│  │  │  └─ low-battery-return-to-dock/
│  │  │     └─ icd-dock-reservation-api.md
│  │  ├─ data/
│  │  │  └─ low-battery-return-to-dock/
│  │  │     └─ data-dock-reservation-schema.md
│  │  ├─ deployment/
│  │  │  └─ low-battery-return-to-dock/
│  │  │     └─ deploy-fleet-coordination-topology.md
│  │  └─ decisions/
│  │     └─ adr-0001-centralize-dock-reservation-in-fleet-service.md
│  └─ traceability/
│     └─ TRACEABILITY.md
├─ tools/
│  ├─ __init__.py
│  └─ validate.py
└─ tests/
   ├─ __init__.py
   └─ test_validate.py

```

## Naming Conventions

| Artifact | Pattern | Example |
| --- | --- | --- |
| Persona | `<role-or-team>.md` | `remote-operator.md` |
| Use case | `uc-<description>.md` | `uc-geofence-breach-alert.md` |
| Product requirement | `req-<description>.md` | `req-geofence-alert-latency.md` |
| System requirement | `sysreq-<description>.md` | `sysreq-geofence-check-interval.md` |
| Architecture diagram | `arch-<description>.md` | `arch-geofence-alert-flow.md` |
| Data specification | `data-<description>.md` | `data-geofence-zone-schema.md` |
| Deployment architecture | `deploy-<description>.md` | `deploy-geofence-service-topology.md` |
| Interface control document | `icd-<description>.md` | `icd-geofence-alert-api.md` |
| Architecture decision record | `adr-NNNN-<description>.md` | `adr-0001-geofence-service-boundary.md` |

All names use kebab-case. Frontmatter cross-references use the filename only (no directory prefix).

## Getting Started With a New Project

1. Click **Use this template** on GitHub to create a new repository from this one.
2. Rename references to "template-repo" in this README and `CLAUDE.md` to your project name — or run the `/new-project` skill in Claude Code, which does this and walks the remaining first-run decisions.
3. Read `CONTRIBUTING.md` and `CLAUDE.md` before authoring your first artifact.
4. Author your first persona, then work down the hierarchy: use case → product requirement → system requirement / architecture / ICD / data spec as needed.
5. Update `traceability/TRACEABILITY.md` and `traceability/STANDARDS-MAPPING.md` as you go.
6. When a stakeholder-facing PRD (PDP-08) is needed, author the governance sections in `prd/sections/` — each ships as a stub carrying the official template's structure, tables, and owner defaults; `prd/README.md` maps every PDP-08 section to its stub or its generating artifact set.
7. When a project matures into needing safety, coding, testing, QA/CM, change/risk, or metrics documentation, open the matching folder under `extensions/` — each has a stub explaining what a complete document looks like per `reference/bkm-document-set.md`.
8. Install `pre-commit` locally (see `CONTRIBUTING.md`) so validation runs before every commit; the same checks run in CI.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the authoring workflow, branching model, and validation instructions.
