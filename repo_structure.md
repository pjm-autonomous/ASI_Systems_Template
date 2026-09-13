# Repository Structure

The canonical directory layout of the ASI systems engineering standard.

**Generated** — regenerate rather than hand-editing, or it drifts from the
repo it describes (it previously contained the same tree twice and still
listed a `config/` directory that no longer exists).

Directories are named **semantically**, never after a level number. The
tier-to-level mapping lives in `repo-standard.yaml` alone, so a renumbering
is a one-line change rather than a repo-wide migration.

```text
├─ .claude/
│  ├─ agents/
│  │  └─ derive.md
│  └─ skills/
│     ├─ adr/
│     │  └─ SKILL.md
│     ├─ architecture/
│     │  └─ SKILL.md
│     ├─ capability-requirement/
│     │  └─ SKILL.md
│     ├─ data-spec/
│     │  └─ SKILL.md
│     ├─ deployment-arch/
│     │  └─ SKILL.md
│     ├─ interface/
│     │  └─ SKILL.md
│     ├─ new-project/
│     │  └─ SKILL.md
│     ├─ persona/
│     │  └─ SKILL.md
│     ├─ requirement/
│     │  └─ SKILL.md
│     ├─ system-requirement/
│     │  └─ SKILL.md
│     └─ use-case/
│        └─ SKILL.md
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  │  ├─ config.yml
│  │  ├─ documentation-issue.yml
│  │  ├─ propose-new-artifact.yml
│  │  ├─ report-artifact-issue.yml
│  │  └─ tooling-ci-bug.yml
│  ├─ workflows/
│  │  └─ ci.yml
│  └─ PULL_REQUEST_TEMPLATE.md
├─ example/
│  ├─ product/
│  │  ├─ personas/
│  │  │  └─ fleet-operator.md
│  │  ├─ requirements/
│  │  │  └─ low-battery-return-to-dock/
│  │  └─ use-cases/
│  │     └─ low-battery-return-to-dock/
│  ├─ system/
│  │  ├─ architecture/
│  │  │  └─ low-battery-return-to-dock/
│  │  ├─ data/
│  │  │  └─ low-battery-return-to-dock/
│  │  ├─ decisions/
│  │  │  └─ adr-0001-centralize-dock-reservation-in-fleet-service.md
│  │  ├─ deployment/
│  │  │  └─ low-battery-return-to-dock/
│  │  ├─ interfaces/
│  │  │  └─ low-battery-return-to-dock/
│  │  └─ requirements/
│  │     └─ low-battery-return-to-dock/
│  ├─ traceability/
│  │  └─ TRACEABILITY.md
│  └─ README.md
├─ extensions/
│  ├─ change-risk/
│  │  ├─ change-management-procedure.md
│  │  └─ risk-register.md
│  ├─ coding/
│  │  ├─ build-and-integration-procedure.md
│  │  ├─ code-review-procedure.md
│  │  ├─ coding-standard.md
│  │  └─ static-analysis-standard.md
│  ├─ metrics/
│  │  ├─ lessons-learned.md
│  │  └─ metrics-program.md
│  ├─ qa-cm/
│  │  ├─ configuration-management-plan.md
│  │  ├─ development-environment-standard.md
│  │  ├─ quality-assurance-plan.md
│  │  └─ version-control-standard.md
│  ├─ safety/
│  │  ├─ fmea.md
│  │  ├─ functional-safety-concept.md
│  │  ├─ hazard-analysis-and-risk-assessment.md
│  │  ├─ safety-case.md
│  │  └─ safety-management-plan.md
│  ├─ testing/
│  │  ├─ integration-testing-procedure.md
│  │  ├─ system-testing-plan.md
│  │  ├─ test-coverage-analysis.md
│  │  ├─ test-strategy.md
│  │  └─ unit-testing-standard.md
│  └─ README.md
├─ glossary/
│  ├─ GLOSSARY.md
│  └─ README.md
├─ prd/
│  ├─ sections/
│  │  ├─ environment-site.md
│  │  ├─ goals.md
│  │  ├─ kpis.md
│  │  ├─ markets.md
│  │  ├─ overview.md
│  │  ├─ performance.md
│  │  ├─ raci.md
│  │  ├─ release-plan.md
│  │  ├─ safety.md
│  │  ├─ scope.md
│  │  ├─ security.md
│  │  └─ standards.md
│  ├─ change-log.md
│  ├─ meta.yaml
│  └─ README.md
├─ product/
│  ├─ personas/
│  │  └─ README.md
│  ├─ requirements/
│  │  └─ README.md
│  └─ use-cases/
│     └─ README.md
├─ reference/
│  ├─ bkm-document-set.md
│  ├─ README.md
│  ├─ standards-framework.md
│  └─ tooling-recommendations.md
├─ standard/
│  ├─ archive/
│  │  └─ ASI-Systems-Standard-Decision-Record-v0.md
│  └─ ASI-Systems-Standard-Decision-Record-v1.md
├─ system/
│  ├─ architecture/
│  │  └─ README.md
│  ├─ data/
│  │  └─ README.md
│  ├─ decisions/
│  │  └─ README.md
│  ├─ deployment/
│  │  └─ README.md
│  ├─ interfaces/
│  │  └─ README.md
│  └─ requirements/
│     └─ README.md
├─ templates/
│  ├─ adr.md
│  ├─ architecture-diagram.md
│  ├─ capability-requirement.md
│  ├─ data-specification.md
│  ├─ deployment-architecture.md
│  ├─ interface.md
│  ├─ persona.md
│  ├─ README.md
│  ├─ system-requirement.md
│  └─ use-case.md
├─ tests/
│  ├─ __init__.py
│  └─ test_validate.py
├─ tools/
│  ├─ __init__.py
│  └─ validate.py
├─ traceability/
│  ├─ README.md
│  ├─ STANDARDS-MAPPING.md
│  └─ TRACEABILITY.md
├─ .editorconfig
├─ .gitignore
├─ .markdownlint.yaml
├─ .markdownlintignore
├─ .pre-commit-config.yaml
├─ CHANGELOG.md
├─ CLAUDE.md
├─ CONTRIBUTING.md
├─ NOTICE.md
├─ pyproject.toml
├─ README.md
├─ repo-standard.yaml
├─ repo_structure.md
├─ SECURITY.md
├─ TODO.md
└─ VERSION
```
