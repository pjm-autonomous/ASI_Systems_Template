# Systems Engineering Standards Framework

## Scope

Standards contained in this repository are used as examples only. None are bundled with this template. Refer to ASI Standards library for current and complete standards' texts.

Don't cite a standard as a "compliance obligation" unless that's actually the project's posture. Default to "engineering reference" language.

## Using This Reference

For each standard likely to apply, add a row (or section) to `traceability/STANDARDS-MAPPING.md`.
Record:
- applicability decision
- current coverage based on scoring tables where provided
- open gaps

NOTE, not all standards apply to every project. Defaulting to full standards list will impose unattainable compliance requirements. Confirm applicability of each standard cited.

As of 2026-07-21 current and complete standards' texts live [ASI Standards Hub](`https://autonomoussolutions.sharepoint.com/SitePages/resources/standards.aspx`). Confirm access separately before relying on a citation.

## ASI Compliance Posture

These are engineering guides and references. Where a standard is listed as a "compliance obligation" in an ASI product document, the intent is alignment, not compliance  with the standard safety, requirement patterns, and process discipline. 

No third-party certification is implied unless explicitly stated.

Confirm the actual posture per project before assuming "guided alignment" applies.

HARA and FMEA are conducted as engineering discipline. For example, ASIL/PLr determination is not a default ASI compliance obligation. 

## ASI Standards

Ordered by General Applicability to ASI's Industrial Autonomous Robot Context

| Citation | Applicability | Description |
| --- | --- | --- |
| IEC 60204-1 / ISO 13850| Direct | stop-category vocabulary used in every ASI safety requirement |
| ISO 13849-1 / IEC 62061| Direct | functional safety for machinery control systems (industrial deployments) |
| ISO 26262 | Guide for Risk Analyses | Road vehicle deployment safety lifecycle discipline and requirement patterns |
| ISO 29119, ISO 12100| Direct | systems engineering |
| ISO 12207| Direct | software development lifecycle processes |
| ISO 25010| Direct | software quality/testing |
| IEC 61508 | Guide | functional safety |
| ASPICE PAM 4.0 — referenced compliance obligation: process assessment maturity |
| IEC 60204| Direct | electrical safety |
| ISO 9001:2015 §8.3 | Guide | design and development quality management |
| IEC 62443| Direct | cybersecurity |
| MISRA C/C++ 2023| Direct | coding guidelines for safety-critical C/C++ software |

---

## Scoring Tables

### IEC 60204-1 — Safety of Machinery: Electrical Equipment of Machines

**This is a primary and safety critical standard.** Stop-category vocabulary is included in all ASI safety requirements.

#### Stop Categories (§9.2.2)

"All Stop" / "Remote Stop" describe the *source* of a stop command, not the category. 

Stop actions are always effected by the vehicle per the categories above.

| Category | Definition | Power at Rest | Typical Use |
| --- | --- | --- | --- |
| Cat 0 | Uncontrolled stop — immediate power removal | Removed | Emergency stop; hardwired fail-safe; most severe |
| Cat 1 | Controlled stop with power applied to achieve stop, then removed | Removed | Fault-triggered controlled stop, position hold not required |
| Cat 2 | Controlled stop with power maintained | Maintained | Normal operational stop; allows controlled resumption |

Escalation rule: a Cat 1 or Cat 2 stop escalates to Cat 0 when the controller estimates the controlled stop cannot complete within the available time or distance.

#### Coverage Scoring

| Level | Criteria |
| --- | --- |
| 0 | No stop categories referenced |
| 1 | Stop categories named but not defined |
| 2 | Stop categories defined; applied inconsistently |
| 3 | Stop categories defined, correctly assigned per hazard, escalation rule stated |
| 4 | Above + hardware independence requirement + mode interlocks documented |
| 5 | Above + IEC 60204-1 clause citations per requirement + validation evidence |

---

### ISO 13849-1 & IEC 62061 - Functional Safety of Control Systems

**These are primary and safety critical standards.**
Safety integrity rankings are included in all ASI industrial robot deployments.

ISO 26262 is an analogous standard for road vehicles, thus inherently less applicable.

| Standard | Best For | Integrity Metric |
| --- | --- | --- |
| ISO 13849-1 | Hardware-dominant or mixed systems; simpler architectures | Performance Level (PLa–PLe) |
| IEC 62061 | Complex programmable safety control systems | Safety Integrity Level (SIL 1–3) |

NOTE, both standards may apply simultaneously.

**ISO 13849 Ranking Reference**

| Performance Level | PFHd (per hour) | ISO 26262 Analogy |
| --- | --- | --- |
| PLa | 10⁻⁵–10⁻⁴ | — |
| PLb | 3×10⁻⁶–10⁻⁵ | ≈ ASIL A |
| PLc | 10⁻⁶–3×10⁻⁶ | ≈ ASIL B |
| PLd | 10⁻⁷–10⁻⁶ | ≈ ASIL C |
| PLe | 10⁻⁸–10⁻⁷ | ≈ ASIL D |

**IEC 62061 Ranking Reference**

| SIL | PFHd (per hour) | ISO 13849 Analogy |
| --- | --- | --- |
| SIL 1 | 10⁻⁶–10⁻⁵ | PLc |
| SIL 2 | 10⁻⁷–10⁻⁶ | PLd |
| SIL 3 | 10⁻⁸–10⁻⁷ | PLe |

### Applicability Decision

| Scenario | Applicable Standard |
| --- | --- |
| Integrated into on-road OEM vehicles | ISO 26262 applies at the vehicle-integration layer |
| Deployed as industrial machinery (off-road, industrial sites) | ISO 13849 / IEC 62061 governs the safety control system |
| Both | Both may apply at different system boundaries |

---

### ISO 26262 — Road Vehicles: Functional Safety

**This is a supplementary standard.**
 Autonomous *road-vehicle* safety lifecycle discipline and requirement patterns.

| Mode | Description | Language to Use |
| --- | --- | --- |
| Certification compliance | Full safety lifecycle with evidence for third-party audit | "Compliant with ISO 26262" |
| Guided alignment (default ASI mode) | Standard used as engineering reference; HARA/FMEA conducted as discipline; no ASIL assignment; no third-party audit | "Informed by ISO 26262" / "aligned with ISO 26262 safety requirement patterns" |

**Implication:** ASIL determination is only a gap is when ISO 26262 is explicitly cited with compliance language.
Use it as a guide for HARA/FMEA activities only.

### Lifecycle Phases and SE Documentation Relevance

| Phase | ISO 26262 Part | Key Outputs |
| --- | --- | --- |
| Concept | Part 3 | Item definition, HARA, Functional Safety Concept |
| System | Part 4 | Technical safety requirements, system design, FMEA |
| Hardware | Part 5 | HW design, safety analysis |
| Software | Part 6 | SW safety requirements, architecture, coding, unit test |
| Supporting | Part 8 | Configuration management, change management |

### Coverage Scoring (Guided Alignment)

| Level | Criteria |
| --- | --- |
| 0 | Standard not referenced |
| 1 | Vague "functional safety standards where applicable" citation |
| 2 | ISO 26262 explicitly cited with guided-alignment language; HARA planned |
| 3 | Requirements note clause alignment; safe states defined; HARA referenced |
| 4 | HARA complete; requirements cite hazard IDs; FMEA complete |
| 5 | Full traceability hazard → requirement → design → test; FMEA traces to requirements |

---

### ISO 12207 — Software Development Lifecycle Processes

**This standard governs software development process structure.**

Eleven primary processes between conception and retirement.


#### Key Phases Applicable to Systems Engineering

| Phase | Objectives | Documentation |
| --- | --- | --- |
| Conception | Business case, feasibility, high-level requirements, stakeholders | Charter/vision, feasibility study, stakeholder register |
| Requirements | Capture and trace system/software requirements | Requirements spec, RTM, change control |
| Design | Translate requirements into architecture | Architecture doc, SDS, ICDs, DVP, C4-style diagrams |
| Implementation | Enforce coding standards, maintain quality | Coding standard, formatting rules, build procedures, review checklist |
| Testing | Verify implementation, establish coverage | Test plans, TTM, coverage metrics, defect reports |
| QA & Metrics | Monitor quality, catch defects early | Static analysis procedures, process metrics, quality gates |
| Config Management | Manage baselines and changes | CM plan, version control procedures, branch/tag strategy |

---

### ASPICE PAM 4.0 — Automotive SPICE Process Assessment Model

**Primary ASI compliance obligation.**

#### Capability Levels

| Level | Name | Criteria |
| --- | --- | --- |
| 0 | Incomplete | Process not performed or fails to produce outputs |
| 1 | Performed | Process achieves its purpose; outputs exist |
| 2 | Managed | Process is planned, monitored, adjusted; outputs controlled |
| 3 | Established | Process uses a defined process tailored from org standards |
| 4 | Predictable | Process operates within defined limits; quantitative management |
| 5 | Optimizing | Process continuously improved to meet business goals |

#### Key Processes Applicable to Systems Engineering

| Process ID | Name | SE Package Relevance |
| --- | --- | --- |
| SWE.1 | Software Requirements Analysis | Requirements completeness, traceability, testability |
| SWE.2 | Software Architectural Design | Architecture documentation, design rationale |
| SWE.3 | Detailed Design and Unit Construction | Coding standards, unit test coverage |
| SWE.4 | Software Unit Verification | Unit test procedures, static analysis |
| SWE.5 | Software Integration and Integration Test | Integration test procedures, ICD verification |
| SWE.6 | Software Qualification Test | System-level test against requirements |
| SYS.2 | System Requirements Analysis | System-level requirements, stakeholder needs |
| SYS.3 | System Architectural Design | System architecture, safety allocation |
| SUP.1 | Quality Assurance | QA plan, process/product audits |
| SUP.8 | Configuration Management | Baselines, change control, version control |
| SUP.9 | Problem Resolution Management | Defect tracking, root cause analysis |
| SUP.10 | Change Request Management | Change impact, approval, traceability |
| MAN.3 | Project Management | Planning, risk, schedule |

---

### ISO 9001:2015 §8.3 — Design and Development of Products and Services

**Primary ASI compliance obligation.**

| Sub-clause | Topic | SE Documentation Requirement |
| --- | --- | --- |
| 8.3.2 | D&D Planning | Plan with stages, reviews, responsibilities, interfaces |
| 8.3.3 | D&D Inputs | Documented requirements — functional, regulatory, prior designs |
| 8.3.4 | D&D Controls | Reviews, verification, and validation at defined stages |
| 8.3.5 | D&D Outputs | Meet inputs; include acceptance criteria; approved before release |
| 8.3.6 | D&D Changes | Identified, reviewed, authorized, controlled; re-verification as required |

#### Coverage Scoring

| Level | Criteria |
| --- | --- |
| 0 | No D&D process documented |
| 1 | D&D referenced but process not described |
| 2 | Requirements doc exists as D&D input baseline; review stages mentioned |
| 3 | Formal review stages with documented sign-off; outputs with acceptance criteria |
| 4 | Above + controlled change process + re-verification on change |
| 5 | Above + metrics on D&D process effectiveness and trends |

---

### MISRA C/C++ 2023

**Primary ASI coding guidelines for safety-critical C/C++ software.**

- **Required** rule:  mandatory compliance
- **Advisory** rule:  should comply
- **Informational**:  guideline only

Enforcement typically through CppCheck Premium (MISRA plugin), clang-static-analyzer, or SonarQube with a MISRA profile.
- Should be integrated into CI/CD
- Code reviews must check MISRA compliance
    - static analysis failure blocks merge
    - deviations documented and approved

---

### IEC 62443 — Security for Industrial Automation and Control Systems

**Primary ASI standard.**

NOTE, if a regulatory or customer requirement demands a formal cybersecurity standard reference, IEC 62443-4-2 (component security requirements) is appropriate to industrial standard for ASI's deployment context.

#### Cybersecurity Requirements Checklist

| Requirement Pattern | Security Property | Adequate Without Formal Standard Citation? |
| --- | --- | --- |
| Authentication of command sources | Authentication | Yes — requirement is clear and testable |
| Message integrity/authenticity on ICDs | Integrity | Yes — crypto mechanism should be specified at design phase |
| Access control on configuration surfaces | Authorization | Yes — requirement is clear and testable |
| Secure boot / firmware integrity at startup | Integrity at boot | Yes — requirement is clear |
| Auditable safety event log | Non-repudiation | Yes — requirement is clear and testable |
