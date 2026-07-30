---
pdp-08-section: "Reference Standards"
pdp-08-ref: "not in PDP-08 rev A — recommended governance addition"
status: stub
owner: Systems Architect   # mixed/unclear ownership defaults to Systems Architect — confirm per project
---

# Reference Standards

<!-- STUB -->

Not a section of PDP-08 rev A; recommended as a governance addition (PRAK precedent,
content-scope decision 2026-07-27) so every standard the requirements invoke is cited with a
specific revision and date of citation. Reconcile against the controlled PDP-08 template when
it changes.

**Posture.** Default to engineering-reference language: alignment with a standard's safety
principles, requirement patterns, and process discipline — not certification. Only call a
standard a compliance obligation if that is genuinely the project's posture. Applicability
decisions and coverage live in `traceability/STANDARDS-MAPPING.md` (candidates and scoring
rubrics in `reference/standards-framework.md`); do not restate them here.

## Directly Invoked

Standards that requirements or their governing documents cite as the basis for an obligation:

| Standard | Cited | Role for This Product |
|---|---|---|
| [e.g. ISO 13849-1:2023] | [YYYY-MM-DD] | [Governing performance-level (PLr) basis — point to the project's governing safety-integrity document as the single authoritative source.] |
| [e.g. IEC 60204-1:2016] | [YYYY-MM-DD] | [Stop-category vocabulary used in safety requirements.] |

## Engineering Guides

Standards used as discipline and pattern references, without a direct obligation:

| Standard | Cited | Role for This Product |
|---|---|---|
| [e.g. ISO/IEC/IEEE 29148:2018] | [YYYY-MM-DD] | [Requirements engineering — EARS-pattern requirement construction.] |

[Software process, testing, and coding standards are typically cited by their owning
engineering documents (`extensions/testing/`, `extensions/coding/`) rather than restated in
the PRD.]
