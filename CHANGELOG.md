# Changelog

All notable changes to the ASI Systems Engineering repo standard.

This template is a **versioned standard**, not a one-way copy. Every repo
instantiated from it records the version it was cut from in `repo-standard.yaml`,
so drift is detectable and updates can be pulled deliberately. See
`standard/ASI-Systems-Standard-Decision-Record-v1.md` §7 for why.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning is [Semantic Versioning](https://semver.org/spec/v2.0.0.html), applied
to the *standard*:

| Bump | Means |
|------|-------|
| **MAJOR** | A downstream repo must change files to stay conformant — a renamed prefix, a removed artifact type, a newly required field. |
| **MINOR** | New optional capability. A conformant repo stays conformant without editing anything. |
| **PATCH** | Documentation, wording, or tooling fixes with no conformance effect. |

## [Unreleased]

### Added

- `VERSION`, this changelog, and `repo-standard.yaml` — the template-version stamp
  and conformance declaration that review item **A7** identified as missing. Without
  them a downstream repo drifts with no way to detect it, and the standard degrades
  to a convention on day one.
- `standard/` — the decision record governing this standard.

- `standard/artifact-schema.yaml` — the artifact model as **versioned data**
  rather than hardcoded Python. `tools/schema.py` interprets it. Types declare
  the *tiers* they may occupy and locations are derived
  (`<tier>/<subdir>/**/<prefix>*.md`), so one type can span tiers with different
  parent resolution at each — which a flat glob list cannot express.
- Architecture level numbering, in `repo-standard.yaml` `levels.map` **only**.
  Levels are derived from the tier and stored nowhere else, so renumbering is a
  one-line change. AxS is a reference outside the chain; ASAM is L0; product L1,
  system L2, subsystem L3, component L4.
- `component-requirement` (`compreq-`) and the `subsystem`/`component` tiers.
- Cross-repo parent shape-checking for references whose target is mastered in
  another repo.
- **Maturity states — the AxS M1..M4 scheme** (`tools/maturity.py`, `_registry/`).
  Adopted from `asirobots/axs`, which already runs this model on the same
  programme with the same reviewers. The state lives in a bold `**Status:**`
  header block in the document body, as AxS records it, not in frontmatter;
  frontmatter is accepted as a migration fallback. Two rules are enforced:
  anything at or above M2 needs a dated promotion record in `_registry/`, and
  M4 at one tier requires M4 at the tier above. Opt-in via the
  `maturity-gates` packet — a repo not running gates is never failed for
  lacking them.
- **Cross-repo parent brokering** (`tools/broker.py`, `emit-artifact-index`).
  Upward enforcement: a repo declares its parent in `repo-standard.yaml`
  `parents:`, and every parent reference leaving the repo is verified to exist
  upstream. Resolution is sibling clone -> cached index -> GitHub Trees API, so
  no clone or network is required when a sibling checkout is present. Locally an
  unreachable parent degrades to a shape-only check; CI uses
  `validate-artifacts --require-parents` and does not degrade.
  A parent repo makes itself resolvable by running `emit-artifact-index`.
  Downward enforcement (coverage) is deliberately out of scope — it needs a
  registry, whereas upward needs one config value.
- `tests/test_schema.py`, `tests/test_maturity.py`, `tests/test_broker.py` —
  94 new tests, including a guard that no level token ever leaks into the schema.

### Changed

- Artifact prefixes aligned to `prak-v-model`, which aligns to Jama terminology:
  - product requirement `req-` → capability requirement **`capreq-`** (conflict C3)
  - interface `icd-` → **`int-`** (conflict C1)
- **BREAKING** `parent-capability-requirement` → `parent-capability-requirements`
  and `parent-system-requirement` → `parent-system-requirements`. Plural, to
  match `parent-use-cases` / `parent-personas` now that every parent field
  accepts multiple values. Free to do today because no repo has yet been
  instantiated from this template.
- `tools/validate.py` is now an interpreter of the schema. Enum checks are
  schema-driven; adding a vocabulary no longer needs a code change.
- `repo_structure.md` is generated. It previously held the same tree twice and
  listed a `config/` directory that no longer existed.

- Every `parent-*` field is now many-to-many capable (harvest item **H2**): the
  one-parent-only model was a Jira limitation, and both GitHub and Jama allow
  m:m. A single parent may still be written as a plain scalar — requiring list
  syntax for one item is friction with no benefit.

### Removed

- `refinement-level` as a stored field. The boundary level is the tier, derived.
  PRAK's validator concedes the point in its own comment: the level and the
  folder are "the same statement made twice."

## [0.1.0] — 2026-09-10

First versioned baseline. Content as it stood when the standard programme began:
product/system artifact trees, PRD section sources, `extensions/` BKM document set,
worked `example/`, glossary, reference framework, and a 325-line validator.

Known gaps at this baseline are tracked in `TODO.md` and
`standard/ASI-Systems-Standard-Decision-Record-v1.md` §11.
