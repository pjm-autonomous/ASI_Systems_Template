# Traceability

| File | Purpose | Maintained |
| --- | --- | --- |
| `TRACEABILITY.md` | Matrix linking each persona down the requirement chain to component requirements. The single place to check "does everything trace to something real" for this project. | **Generated** (D-46) |
| `STANDARDS-MAPPING.md` | Which cross-industry standards (from `reference/standards-framework.md`) actually apply to this project, at what posture (engineering reference vs. compliance obligation), and current coverage level. | By hand |

## `TRACEABILITY.md` is generated — do not edit it

Run `build-traceability` after adding or re-pointing an artifact. `tools/trace.py` reads the `parent-*` fields in frontmatter and writes the whole file; a hand edit is reverted by the next run.

`build-traceability --check` writes nothing and asks a different question: is the tracked file still what the generator would emit? It runs in CI and as a pre-commit hook, because **currency is a separate failure from correctness** — a matrix that was right last month and has not been regenerated since passes every other check in this repo and is still wrong.

### The columns are derived, not chosen

They come from following `parent-*` fields through `standard/artifact-schema.yaml`. Adding a tier, or re-pointing a parent, changes the matrix with no edit to the generator.

That is also why **architecture, ICDs, data specifications, ADRs, deployment architecture and parameters have no column.** None of them declares a `parent-*` field, so there is no edge to trace. They are listed under *Artifacts with no declared lineage* instead.

This is deliberate. An earlier hand-maintained version of this matrix carried `Architecture`, `ICD` and `Data Spec` columns and filled them from artifacts that merely shared a feature-bucket directory name. A link inferred from a directory name is a guess presented as a fact, which is worse than a blank — a blank is honest about what is not known.

If those types should trace to a requirement, the fix is to give them a `parent-*` field in the artifact schema. That is a change to the model, made in `standard/`, and this matrix picks it up automatically.

### An empty cell

An empty cell means the chain stops there — either the artifact has not been decomposed yet, or its parent is upstream. The two are distinguished by the marks in the legend: `†` is an upstream parent, checked by `tools/broker.py`; `‡` is a parent named but not found, which `validate-artifacts` reports as an error.

There is no `n/a` convention any more. Nothing hand-writes a cell, so nothing can annotate one — record a deliberate exclusion in the artifact's own body, where a reviewer reads it.

## `STANDARDS-MAPPING.md`

Hand-maintained, and it should change in the **same PR** as the work that changes which standards apply.

An unmarked standard reads as "not applicable", which is indistinguishable from "nobody looked" — see item F5 of `standard/checklists/new-repo.md`.
