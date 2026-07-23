# Best-Known-Method: Complete SE Documentation Set

Condensed from ASI's SE-documentation best-known-method reference (`analyze-se-docs` skill, `bkm-complete.md`). This is the target document inventory for a **mature** SE package — not a day-one requirement. Use it to know what a stub in `extensions/` should grow into, and to decide, project by project, which categories actually apply.

A complete SE documentation package contains or references these documents, grouped by category. Numbers are illustrative ordering, not IDs to enforce.

## 1. Project Governance & Strategy

- **Vision and Strategy** — business case, market drivers, success metrics
- **Project Charter** — scope, constraints, stakeholder register, approval authority

## 2. Requirements Management (ISO 12207: Requirements Phase)

- **Requirements Management Standard** — process for capturing, tracing, and managing requirements; must mandate a configuration/change-management tool, define traceability methodology, establish review/approval workflow, and address requirements across lifecycle phases
- **System Requirements Specification** — functional and non-functional requirements, uniquely identified with traceability IDs, cross-referenced to hazard analysis where applicable

*In this template, requirements management is the core `product/` + `system/requirements/` tree plus `traceability/TRACEABILITY.md` — not a separate extension.*

## 3. Safety & Compliance (`extensions/safety/`)

- **Safety Management Plan** — safety strategy, integrity-level assignment methodology, safety lifecycle roles, resourcing
- **Hazard Analysis and Risk Assessment (HARA)** — identified hazards with severity/probability, integrity-level assignments, mitigation strategies, links to safety requirements
- **Functional Safety Concept** — how hazards are mitigated: safety functions and allocations, safe states, error detection, diagnostic coverage targets
- **Failure Modes and Effects Analysis (FMEA/FMECA)** — component failure modes, detection/mitigation mechanisms, traceability to safety requirements
- **Safety Case** — integrated safety evidence argument (claim → evidence) across design, code, test, analysis

## 4. Architectural & Design (ISO 12207: Design Phase)

*Core in this template:* `system/architecture/`, `system/data/`, `system/deployment/`, `system/interfaces/` (ICDs), `system/decisions/` (ADRs).

- **System Architecture Specification** — overall decomposition, context diagram, system boundaries and external interfaces, safety-critical vs. non-critical separation
- **Detailed Design Standard** — module interface specs, algorithm descriptions, data structures, resource allocation
- **Design Verification Plan** — review cadence, analysis techniques, verification artifact collection, approval cycle

## 5. Code & Implementation (`extensions/coding/`)

- **Coding Standard** — cites applicable language standard(s) (e.g., MISRA C/C++), naming conventions, code organization, complexity limits, memory-safety rules, formatting configuration
- **Static Analysis Standard** — tool(s), rule configuration, CI integration, deviation procedure, traceability from findings to review
- **Code Review Procedure** — checklist, approval authority, PR procedure, traceability from review findings to issues
- **Build and Integration Procedure** — build reproducibility, compiler flags, dependency/versioning, artifact management, baseline definitions

## 6. Testing & Verification (`extensions/testing/`)

- **Test Strategy** — test levels, coverage targets, tools/frameworks, environment setup, traceability to requirements
- **Unit Testing Standard** — pass/fail case expectations, file naming/location, mocking conventions, coverage measurement and thresholds
- **Integration Testing Procedure** — component-interaction test cases, interface verification, failure injection/recovery testing
- **System Testing Plan** — requirement-to-test traceability, performance/stress testing, safety scenario testing, environmental testing
- **Test Coverage Analysis** — statement/branch/MC-DC coverage measurement, gaps and re-test procedures

## 7. Quality Assurance & Configuration Management (`extensions/qa-cm/`)

- **Quality Assurance Plan** — process/product audits, metrics collection, corrective action procedures
- **Configuration Management Plan** — configuration items, baseline definitions, change control process, branching strategy, tag/release procedures
- **Version Control Standard** — repository structure, branch naming/lifecycle, commit format, PR/merge rules, release tagging
- **Development Environment Standard** — required tools/versions, setup automation, container/VM specs, onboarding, license management

## 8. Safety Case & Compliance Documentation

- **Compliance Matrix** — standards/regulations coverage, gap-closure procedures. *In this template, tracked as `traceability/STANDARDS-MAPPING.md`, not a separate extension.*

## 9. Change & Risk Management (`extensions/change-risk/`)

- **Change Management Procedure** — change request process, impact analysis, approval authority by risk, traceability update procedure
- **Risk Register** — technical/safety/process risks, mitigation actions and owners, review and closure criteria

## 10. Process Metrics & Continuous Improvement (`extensions/metrics/`)

- **Metrics Program** — defect metrics, code metrics, process metrics, safety metrics, trends and improvement targets
- **Lessons Learned** — retrospective findings, process changes implemented, training needs identified

---

## Using This List

For each category above that applies to your project:

1. Open the matching `extensions/<category>/` folder.
2. Replace the stub file(s) with real content, following the bullet points here as a checklist of what the document should cover.
3. Update `traceability/STANDARDS-MAPPING.md` if the category ties to a specific standard (most do — see `reference/standards-framework.md`).
4. If a category is deliberately deferred rather than authored, say so explicitly in the stub (who decided, why, and when it'll be revisited) rather than leaving it silently empty.
