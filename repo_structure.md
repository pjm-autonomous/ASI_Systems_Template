
```text
template-repo
├─ README.md
├─ CLAUDE.md
├─ NOTICE.md
├─ SECURITY.md
├─ TODO.md
├─ .editorconfig
├─ .markdownlint.yaml
├─ .markdownlintignore
├─ pyproject.toml
├─ config
│  └─ pre-commit-config.yaml
├─ CONTRIBUTING.md
├─ templates
│  ├─ persona.md
│  ├─ use-case.md
│  ├─ product-requirement.md
│  ├─ system-requirement.md
│  ├─ architecture-diagram.md
│  ├─ icd.md
│  ├─ data-specification.md
│  ├─ deployment-architecture.md
│  └─ adr.md
├─ reference
│  ├─ bkm-document-set.md
│  └─ standards-framework.md
├─ traceability
│  ├─ TRACEABILITY.md
│  └─ STANDARDS-MAPPING.md
├─ glossary
│  └─ GLOSSARY.md
├─ product
│  ├─ personas
│  │  └─ README.md
│  ├─ use-cases
│  │  └─ README.md
│  └─ requirements
│     └─ README.md
├─ system
│  ├─ requirements
│  │  └─ README.md
│  ├─ architecture
│  │  └─ README.md
│  ├─ data
│  │  └─ README.md
│  ├─ deployment
│  │  └─ README.md
│  ├─ interfaces
│  │  └─ README.md
│  └─ decisions
│     └─ README.md
├─ prd
│  ├─ README.md
│  ├─ meta.yaml
│  ├─ change-log.md
│  └─ sections
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
├─ extensions
│  ├─ README.md
│  ├─ safety
│  │  ├─ safety-management-plan.md
│  │  ├─ hazard-analysis-and-risk-assessment.md
│  │  ├─ functional-safety-concept.md
│  │  ├─ fmea.md
│  │  └─ safety-case.md
│  ├─ coding
│  │  ├─ coding-standard.md
│  │  ├─ static-analysis-standard.md
│  │  ├─ code-review-procedure.md
│  │  └─ build-and-integration-procedure.md
│  ├─ testing
│  │  ├─ test-strategy.md
│  │  ├─ unit-testing-standard.md
│  │  ├─ integration-testing-procedure.md
│  │  ├─ system-testing-plan.md
│  │  └─ test-coverage-analysis.md
│  ├─ qa-cm
│  │  ├─ quality-assurance-plan.md
│  │  ├─ configuration-management-plan.md
│  │  ├─ version-control-standard.md
│  │  └─ development-environment-standard.md
│  ├─ change-risk
│  │  ├─ change-management-procedure.md
│  │  └─ risk-register.md
│  └─ metrics
│     ├─ metrics-program.md
│     └─ lessons-learned.md
├─ example
│  ├─ README.md
│  ├─ product
│  │  ├─ personas
│  │  │  └─ fleet-operator.md
│  │  ├─ use-cases
│  │  │  └─ low-battery-return-to-dock
│  │  │     └─ uc-low-battery-return-to-dock.md
│  │  └─ requirements
│  │     └─ low-battery-return-to-dock
│  │        └─ req-autonomous-return-to-dock.md
│  ├─ system
│  │  ├─ requirements
│  │  │  └─ low-battery-return-to-dock
│  │  │     ├─ sysreq-battery-threshold-monitor.md
│  │  │     └─ sysreq-dock-availability-check.md
│  │  ├─ architecture
│  │  │  └─ low-battery-return-to-dock
│  │  │     └─ arch-dock-return-flow.md
│  │  ├─ interfaces
│  │  │  └─ low-battery-return-to-dock
│  │  │     └─ icd-dock-reservation-api.md
│  │  ├─ data
│  │  │  └─ low-battery-return-to-dock
│  │  │     └─ data-dock-reservation-schema.md
│  │  ├─ deployment
│  │  │  └─ low-battery-return-to-dock
│  │  │     └─ deploy-fleet-coordination-topology.md
│  │  └─ decisions
│  │     └─ adr-0001-centralize-dock-reservation-in-fleet-service.md
│  └─ traceability
│     └─ TRACEABILITY.md
├─ tools
│  ├─ __init__.py
│  └─ validate.py
└─ tests
   ├─ __init__.py
   └─ test_validate.py

```

```text
template-repo
├─ README.md
├─ CLAUDE.md
├─ NOTICE.md
├─ SECURITY.md
├─ TODO.md
├─ .editorconfig
├─ .markdownlint.yaml
├─ .markdownlintignore
├─ pyproject.toml
├─ config
│  └─ pre-commit-config.yaml
├─ CONTRIBUTING.md
├─ templates
│  ├─ persona.md
│  ├─ use-case.md
│  ├─ product-requirement.md
│  ├─ system-requirement.md
│  ├─ architecture-diagram.md
│  ├─ icd.md
│  ├─ data-specification.md
│  ├─ deployment-architecture.md
│  └─ adr.md
├─ reference
│  ├─ bkm-document-set.md
│  └─ standards-framework.md
├─ traceability
│  ├─ TRACEABILITY.md
│  └─ STANDARDS-MAPPING.md
├─ glossary
│  └─ GLOSSARY.md
├─ product
│  ├─ personas
│  │  └─ README.md
│  ├─ use-cases
│  │  └─ README.md
│  └─ requirements
│     └─ README.md
├─ system
│  ├─ requirements
│  │  └─ README.md
│  ├─ architecture
│  │  └─ README.md
│  ├─ data
│  │  └─ README.md
│  ├─ deployment
│  │  └─ README.md
│  ├─ interfaces
│  │  └─ README.md
│  └─ decisions
│     └─ README.md
├─ prd
│  ├─ README.md
│  ├─ meta.yaml
│  ├─ change-log.md
│  └─ sections
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
├─ extensions
│  ├─ README.md
│  ├─ safety
│  │  ├─ safety-management-plan.md
│  │  ├─ hazard-analysis-and-risk-assessment.md
│  │  ├─ functional-safety-concept.md
│  │  ├─ fmea.md
│  │  └─ safety-case.md
│  ├─ coding
│  │  ├─ coding-standard.md
│  │  ├─ static-analysis-standard.md
│  │  ├─ code-review-procedure.md
│  │  └─ build-and-integration-procedure.md
│  ├─ testing
│  │  ├─ test-strategy.md
│  │  ├─ unit-testing-standard.md
│  │  ├─ integration-testing-procedure.md
│  │  ├─ system-testing-plan.md
│  │  └─ test-coverage-analysis.md
│  ├─ qa-cm
│  │  ├─ quality-assurance-plan.md
│  │  ├─ configuration-management-plan.md
│  │  ├─ version-control-standard.md
│  │  └─ development-environment-standard.md
│  ├─ change-risk
│  │  ├─ change-management-procedure.md
│  │  └─ risk-register.md
│  └─ metrics
│     ├─ metrics-program.md
│     └─ lessons-learned.md
├─ example
│  ├─ README.md
│  ├─ product
│  │  ├─ personas
│  │  │  └─ fleet-operator.md
│  │  ├─ use-cases
│  │  │  └─ low-battery-return-to-dock
│  │  │     └─ uc-low-battery-return-to-dock.md
│  │  └─ requirements
│  │     └─ low-battery-return-to-dock
│  │        └─ req-autonomous-return-to-dock.md
│  ├─ system
│  │  ├─ requirements
│  │  │  └─ low-battery-return-to-dock
│  │  │     ├─ sysreq-battery-threshold-monitor.md
│  │  │     └─ sysreq-dock-availability-check.md
│  │  ├─ architecture
│  │  │  └─ low-battery-return-to-dock
│  │  │     └─ arch-dock-return-flow.md
│  │  ├─ interfaces
│  │  │  └─ low-battery-return-to-dock
│  │  │     └─ icd-dock-reservation-api.md
│  │  ├─ data
│  │  │  └─ low-battery-return-to-dock
│  │  │     └─ data-dock-reservation-schema.md
│  │  ├─ deployment
│  │  │  └─ low-battery-return-to-dock
│  │  │     └─ deploy-fleet-coordination-topology.md
│  │  └─ decisions
│  │     └─ adr-0001-centralize-dock-reservation-in-fleet-service.md
│  └─ traceability
│     └─ TRACEABILITY.md
├─ tools
│  ├─ __init__.py
│  └─ validate.py
├─ tests
│  ├─ __init__.py
│  └─ test_validate.py
└─ repo_structure.md

```
