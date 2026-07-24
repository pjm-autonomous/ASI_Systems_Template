# Traceability

| File | Purpose |
| --- | --- |
| `TRACEABILITY.md` | Matrix linking each persona down to use cases, product requirements, system requirements, architecture, ICDs, and data specifications. The single place to check "does everything trace to something real" for this project. |
| `STANDARDS-MAPPING.md` | Which cross-industry standards (from `reference/standards-framework.md`) actually apply to this project, at what posture (engineering reference vs. compliance obligation), and current coverage level. |

## Update Discipline

Both files should change in the **same PR** as the artifact change that motivates the update — not as a separate cleanup pass. A PR that adds a system requirement without touching `TRACEABILITY.md` is incomplete, even if `tools/validate.py` doesn't currently enforce that (it checks that cross-references resolve, not that the matrix is complete — see `system/requirements/README.md` and friends for artifact-level conventions, and `CONTRIBUTING.md`'s PR checklist for the process expectation).

## When a Cell Is Empty vs. `n/a`

An empty cell in `TRACEABILITY.md` means "not yet authored" — a real gap to close. `n/a` means "deliberately out of scope," and should always come with a short note explaining the decision (either inline or in a "Known Gaps" note at the bottom of the file) — a bare `n/a` with no reasoning is indistinguishable from someone forgetting to fill it in later.
