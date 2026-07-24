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
| IEC 60204-1 / ISO 13850 | Direct | stop-category vocabulary used in every ASI safety requirement |
| ISO 13849-1 / IEC 62061 | Direct | functional safety for machinery control systems (industrial deployments) |
| ISO 26262 | Guide for Risk Analyses | Road vehicle deployment safety lifecycle discipline and requirement patterns |
| ISO 29119, ISO 12100 | Direct | systems engineering |
| ISO 12207 | Direct | software development lifecycle processes |
| ISO 25010 | Direct | software quality/testing |
| IEC 61508 | Guide | functional safety |
| ASPICE PAM 4.0 | Referenced compliance obligation | process assessment maturity |
| IEC 60204 | Direct | electrical safety |
| ISO 9001:2015 §8.3 | Guide | design and development quality management |
| IEC 62443 | Direct | cybersecurity |
| MISRA C/C++ 2023 | Direct | coding guidelines for safety-critical C/C++ software |
| ISO/IEC/IEEE 15288:2023 | Direct | system life cycle processes — the foundational SE framework this template's artifact hierarchy (personas → use cases → requirements → architecture) is built on |
| ISO/IEC/IEEE 29148:2018 | Direct | requirements engineering — construct of a good requirement, requirements information items, guidance behind `product/requirements/` and `system/requirements/` |
| ISO/IEC/IEEE 42010:2022 | Direct | architecture description — viewpoints/framework guidance behind `system/architecture/`, ICDs, and ADRs |
| ISO 10218-1:2025 / ISO 10218-2:2025 | Direct | industrial robot safety — design (Part 1) and system integration/robot cells (Part 2); the 2025 revision consolidates collaborative-robot requirements formerly in ISO/TS 15066 |
| ANSI/A3 R15.06-2025 | Referenced compliance obligation | US national adoption of ISO 10218-1/-2:2025, relevant when a domestic (ANSI/A3) certification path is needed alongside or instead of ISO |
| ISO 3691-4:2023 | Direct | safety requirements for driverless industrial trucks and their systems (AGV/AMR) — Type-C machinery standard, directly applicable to ASI's autonomous ground vehicles |
| ISO 21448:2022 (SOTIF) | Direct | safety of the intended functionality — hazards from functional insufficiency or foreseeable misuse (e.g. perception/autonomy limitations), distinct from and complementary to ISO 26262's fault-based safety |
| ISO/SAE 21434:2021 | Guide | road vehicle cybersecurity engineering across the lifecycle — companion to ISO 26262 at the road-vehicle E/E integration boundary; use alongside, not instead of, IEC 62443 for the industrial/embedded side |
| ISO 31000:2018 | Guide | general risk management guidelines — informs `extensions/change-risk/risk-register.md` structure |
| ISO/IEC/IEEE 24765:2017 | Guide | systems and software engineering vocabulary (SEVOCAB) — informs `glossary/GLOSSARY.md` term definitions |

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

#### ISO 13849 Ranking Reference

| Performance Level | PFHd (per hour) | ISO 26262 Analogy |
| --- | --- | --- |
| PLa | 10⁻⁵–10⁻⁴ | — |
| PLb | 3×10⁻⁶–10⁻⁵ | ≈ ASIL A |
| PLc | 10⁻⁶–3×10⁻⁶ | ≈ ASIL B |
| PLd | 10⁻⁷–10⁻⁶ | ≈ ASIL C |
| PLe | 10⁻⁸–10⁻⁷ | ≈ ASIL D |

#### IEC 62061 Ranking Reference

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

---

### ISO/IEC/IEEE 15288:2023 — System Life Cycle Processes

**Foundational SE standard — this template's artifact hierarchy is one tailoring of it.** Second edition, published 2023. Defines process descriptions for the life cycle of human-made systems (conception through retirement) across hardware, software, data, humans, processes, services, and facilities. Shares its process model with ISO/IEC/IEEE 12207; use 12207 when software is the predominant element of interest, 15288 for the system as a whole.

| This Template's Artifact | 15288 Process Area |
| --- | --- |
| `product/personas/`, `product/use-cases/` | Stakeholder Needs and Requirements Definition |
| `product/requirements/`, `system/requirements/` | System/Software Requirements Definition |
| `system/architecture/`, `system/interfaces/`, `system/data/`, `system/deployment/` | Architecture Definition, Design Definition |
| `system/decisions/` (ADRs) | Decision Management |
| `traceability/` | Configuration Management, Verification (traceability aspects) |

#### Coverage Notes

Not scored 0–5 like the safety standards above — record instead whether the project's process explicitly maps to 15288 process areas (useful when a customer or auditor expects SE-process traceability) or is only informally followed.

---

### ISO/IEC/IEEE 29148:2018 — Requirements Engineering

**Direct — governs how requirements in `product/requirements/` and `system/requirements/` should be constructed.** Specifies the processes for engineering requirements, the required information items (requirements specifications), and the characteristics of a well-formed individual requirement (unambiguous, complete, singular, feasible, verifiable, traceable, etc.).

#### Coverage Notes

| Area | Coverage Level | Details |
| --- | --- | --- |
| Individual requirement quality (per 29148 characteristics) | None / Partial / Consistently applied | |
| Requirements specification structure | | |
| Traceability methodology defined | | Compare against `traceability/TRACEABILITY.md` |

EARS phrasing (used throughout this template's requirement templates) is a widely adopted way of satisfying 29148's "unambiguous and singular" characteristics, not a competing standard.

---

### ISO/IEC/IEEE 42010:2022 — Architecture Description

**Direct — governs the structure/viewpoint conventions behind `system/architecture/`, `system/interfaces/`, and `system/decisions/`.** Specifies requirements for an architecture description: viewpoints, model kinds, and the framework relating them to stakeholder concerns. Does not prescribe a specific notation (Mermaid, C4, UML, etc. all satisfy it if applied consistently) or process.

#### Coverage Notes

| Area | Coverage Level | Details |
| --- | --- | --- |
| Stakeholders and their architectural concerns identified | None / Partial / Defined | |
| Consistent viewpoints across `system/architecture/` diagrams | | |
| Architecture rationale traceable to decisions (ADRs) | | |

---

### ISO 10218-1:2025 / ISO 10218-2:2025 — Robots and Robotic Devices Safety

**Direct and safety-critical for any physical robot ASI designs, manufactures, or integrates.** Part 1 (design/manufacture/rebuild) and Part 2 (system integration, robot cells) — jointly revised in 2025, expanding significantly from the 2011 editions. The 2025 revision **consolidates collaborative-robot safety requirements formerly in the separate ISO/TS 15066** into Part 1 directly, adds two industrial-robot classes (Class 1 for low-hazard robots under reduced control requirements), and adds cybersecurity guidance as it pertains to robot safety.

#### Coverage Scoring

| Level | Criteria |
| --- | --- |
| 0 | Not referenced |
| 1 | Referenced by name only |
| 2 | Robot classification (Class 1/2 or equivalent) and applicable Part identified |
| 3 | Risk assessment performed per Part 2; safety functions and performance levels assigned |
| 4 | Above + collaborative-application requirements addressed where applicable + validation evidence |
| 5 | Above + full traceability from risk assessment to safety requirement to design to test |

---

### ANSI/A3 R15.06-2025 — US National Industrial Robot Safety Standard

**Referenced compliance obligation when a US/ANSI certification path is needed.** The US national adoption of ISO 10218-1:2025 / ISO 10218-2:2025 (published by A3, jointly with ISO in January 2025). Functionally aligned with the ISO standard; cite this instead of (or alongside) ISO 10218 when the target market or customer expects ANSI/A3 certification specifically.

---

### ISO 3691-4:2023 — Driverless Industrial Trucks (AGV/AMR) Safety

**Direct — the primary safety standard for ASI's autonomous ground vehicles as a vehicle class**, distinct from ISO 10218's robot-arm/manipulator focus. Covers powered trucks designed to operate automatically (AGVs, AMRs, automated guided carts) — the vehicle, its control system, guidance means, and system context. Excludes power-source requirements and vehicles guided solely by mechanical rail or pure remote control. A Type-C standard: applies to manufacturers, integrators, and operators alike.

#### Coverage Scoring

| Level | Criteria |
| --- | --- |
| 0 | Not referenced |
| 1 | Referenced by name only |
| 2 | Person-detection and mode-of-operation requirements identified |
| 3 | Safety functions and performance levels assigned per risk assessment |
| 4 | Above + validation of automated functions in the final installation environment |
| 5 | Above + full traceability from risk assessment to safety requirement to design to test |

---

### ISO 21448:2022 — Safety of the Intended Functionality (SOTIF)

**Direct and increasingly critical as autonomy/perception sophistication grows.** Addresses hazards that arise when a system behaves exactly as designed, but the design itself has functional insufficiencies (e.g., a perception model that misclassifies a novel obstacle) or is subject to reasonably foreseeable misuse — as opposed to ISO 26262, which addresses hazards from systematic or random *faults*. Originally published as ISO/PAS 21448:2019; the 2022 edition is a full International Standard (not a PAS) with reworked hazard-model clauses.

| Standard | Addresses |
| --- | --- |
| ISO 26262 | Hazards from system malfunction/failure |
| ISO 21448 (SOTIF) | Hazards from functional insufficiency or foreseeable misuse, even with no failure present |

#### Coverage Scoring

| Level | Criteria |
| --- | --- |
| 0 | Not referenced |
| 1 | Referenced by name only |
| 2 | Known perception/autonomy limitations documented informally |
| 3 | Functional insufficiencies identified via structured analysis; linked to requirements |
| 4 | Above + foreseeable-misuse scenarios analyzed + mitigations defined |
| 5 | Above + validation evidence (scenario/simulation testing) traced to SOTIF findings |

---

### ISO/SAE 21434:2021 — Road Vehicles Cybersecurity Engineering

**Guide — companion to ISO 26262 at the road-vehicle E/E integration boundary; use IEC 62443 for the industrial/embedded control side.** Specifies cybersecurity risk management requirements across concept, development, production, operation, maintenance, and decommissioning of road-vehicle E/E systems. Process-oriented (does not prescribe specific technology).

#### Coverage Notes

Applicable primarily when PRAK-class products integrate with or are deployed on production road vehicles. For purely industrial/off-road deployments, IEC 62443's checklist above is the more directly applicable cybersecurity reference.

---

### ISO 31000:2018 — Risk Management Guidelines

**Guide — general-purpose, not industry-specific.** Eleven principles for effective risk management: identifying, analyzing, evaluating, treating, monitoring, and communicating risk. Not a certifiable standard. Use as the structural reference for `extensions/change-risk/risk-register.md` regardless of which safety/security standards apply to a given project.

---

### ISO/IEC/IEEE 24765:2017 — Systems and Software Engineering Vocabulary (SEVOCAB)

**Guide — terminology reference, not a process or safety standard.** Published snapshot of the SEVOCAB database (also browsable live at [https://www.computer.org/sevocab](https://www.computer.org/sevocab)). Use when a term in `glossary/GLOSSARY.md` needs a citeable, industry-standard definition rather than a project-invented one.
