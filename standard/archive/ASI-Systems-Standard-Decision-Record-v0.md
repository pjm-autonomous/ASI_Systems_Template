# ASI Systems Standard — Decision Record

**Status:** Proposed — nothing implemented, nothing ratified
**Date:** 2026-09-09
**Owner:** Patrick McKee (Systems Engineer)
**Approach ratified 2026-09-09:** harvest `prak-v-model` into this template, reconcile
conflicts, freeze the template as normative, then conform all repos to it.

## Scope

This record covers the standard repo structure for ASI systems engineering, to be
used by every SE repo: `prak-v-model` (system tier), the four platform-team repos
(Embedded-Core, GNC, ODOA, Electronics), and anything built from this template
hereafter.

Sources compared, 2026-09-09:

| Repo | Role today | Validator |
|------|-----------|-----------|
| `ASI_Systems_Template` | Intended standard; derived from PRAK lessons | 325 lines |
| `prak-v-model` | Most mature working repo, 530 files | **750 lines** |
| `polymorphous-v-model` | Becoming the Embedded-Core component-tier repo | 397 lines |

**Central finding: the template and PRAK have diverged in both directions.**
Neither is a superset. The template added artifact types PRAK never adopted
(data specs, ADRs, deployment, extensions, worked example); PRAK added machinery
the template lacks (multi-glob types, list-valued parents, the interface catalog,
uniqueness and ordering checks, agile planning). A harvest must run both ways.

---

## 1. Harvest inventory — `prak-v-model` → template

Ranked by value. "Effort" is implementation only, excluding review.

| # | Capability | Why it belongs in the standard | Effort |
|---|-----------|-------------------------------|--------|
| H1 | **Multi-glob / multi-prefix artifact types** (`glob: str \| tuple`, `prefix: str \| tuple`) | Without it one artifact type cannot live at two tiers. This is the single blocker for the interface catalog and the component tier. Everything else depends on it. | S |
| H2 | **`list_parent_fields`** — list-valued cross-references | A system requirement legitimately serves several use cases. The template's one-parent-only model forces a false choice. | S |
| H3 | **Identity uniqueness checks** (`_check_identity_uniqueness`) | Filenames unique repo-wide; `id` and `title` unique per type. Catches copy-paste drift that silently breaks Jama's External ID match key. | M |
| H4 | **Interface catalog** (`_check_interface_fields`) — class/status/refinement enums, L0/L1/L2 → directory mapping, conditional required fields, mandatory link-loss row | The most developed idea in PRAK and absent here. Conditional requirements (`baseline-date` only at Baseline, `icd-ref` only at L2) are the pattern worth generalizing. | L |
| H5 | **Interface annotations in diagrams** (`%% @interface <A> <B> <int-*.md>`) | Makes architecture diagram edges resolve to real interface artifacts. Cheap, high leverage, nothing equivalent exists. | S |
| H6 | **BOM tolerance** | PowerShell 5.1 `Set-Content` writes a UTF-8 BOM by default. Without this, files authored on Windows fail frontmatter parsing over an invisible character. Non-negotiable for a Windows-first org. | XS |
| H7 | **`split_frontmatter` / `ParsedArtifact` / `read_artifact`** | Read-once, parse-once structure. The template re-reads files per check. Needed before H3/H4 make sense. | S |
| H8 | **Enum vocabularies** — MoSCoW priority, safety classification, verification methods, platform teams | The `platform-team` enum is why the Polymorphous→Embedded-Core rename could not land silently on 178 artifacts. Enumerating names is a control, not bureaucracy. | S |
| H9 | **`_check_traceability_order`** — TM-`<n>` IDs never decrease | Only useful if trace IDs are allocated by reading the matrix. Adopt **only** if the standard keeps that allocation scheme (see C9). | S |
| H10 | **Agile planning types** (initiative / epic / story) | Real and working in PRAK, but it is delivery management, not systems engineering. Recommend specified-but-optional (C10). | M |

### Harvest the other way — template capabilities PRAK lacks

| # | Capability | Note |
|---|-----------|------|
| H11 | **ADR type** + status enum (`system/decisions/adr-NNNN-*.md`) | PRAK records architecture decisions in `ai-context/02-architecture-decisions.md` as a numbered locked-decision list — a parallel mechanism with no validation. Reconcile. |
| H12 | **Data specification** (`system/data/`) and **deployment architecture** (`system/deployment/`) | Genuine gaps in PRAK. |
| H13 | **`extensions/`** — safety, coding, testing, qa-cm, change-risk, metrics | The BKM document set. PRAK has `safety/` only. |
| H14 | **`prd/`**, **`glossary/`**, **`reference/`**, **worked `example/`** | Template is ahead. Keep. |

### From `polymorphous-v-model`

| # | Capability | Note |
|---|-----------|------|
| H15 | **Sub-system and component requirement tiers** | `subsystem/` + `component/` requirements and architecture. The tier every platform-team repo needs and no repo has. See C8. |
| H16 | **Cross-repo reference shape-checking** (`EXTERNAL_REF_FIELDS`) | A component requirement's parent lives in another repo and cannot be resolved locally. Currently shape-checked only. Needs a real answer (C7). |
| H17 | **Requirements-tool picklist enums** | Component type, requirement type, verification method validated against the target tool's picklists so a typo fails CI, not the import. |

---

## 2. Conflicts requiring a ruling

Each needs a winner before code moves. **Recommendation** is mine; the call is yours.

| # | Conflict | Template | prak-v-model | Recommendation |
|---|----------|----------|--------------|----------------|
| **C1** | Interface artifact prefix | `icd-` | `int-` | **`int-`**. PRAK's catalog distinguishes the *entry* (`int-`) from the *document* it may refine to (`icd-ref`). `icd-` conflates them, and only PRAK has real content. Cost: rename template stubs + skill. |
| **C2** | Interface location | `system/interfaces/<feature>/` | `{product,system,component}/interfaces/` by L0/L1/L2 | **PRAK's.** Boundary level is a real property and the directory encodes it. Requires H1. |
| **C3** | Product-tier requirement name | `parent-product-requirement` | `parent-capability-requirement` | **Decide deliberately — this is a vocabulary change, not a rename.** PRAK's "capability requirement" is ratified across 15 `capreq-*` artifacts and its glossary. Template says "product requirement". Recommend adopting **capability** and retiring "product requirement", but it touches every repo. |
| **C4** | Is a sysreq's parent required? | Yes | No | **No, but warn.** PRAK has legitimate orphan sysreqs (safety-derived, standards-derived). Hard-failing forces fake parents. Recommend a non-fatal warning channel — which the validator does not currently have. |
| **C5** | Table markup | Markdown | HTML `<table>` | **Per-repo, declared once.** Already flagged in `TODO.md`. HTML is required for Jama rich-text paste; Markdown is better for diffing and the docs site. Recommend a repo-level `table-format:` setting the validator enforces for consistency, rather than one global answer. |
| **C6** | Verification method vocabulary | — | Test, Analysis, Inspection, Demonstration | **Jama's superset**: adds `Unassigned` and `Special qualification methods`. If the tool is the system of record, its picklist wins; a value the tool rejects is not valid regardless of what we prefer. |
| **C7** | Cross-repo parent resolution | n/a | n/a | **Unsolved and blocking.** A `compreq-` names a `sysreq-` in another repo. Options: sibling clone, published index (e.g. each repo emits `artifact-index.json` on release), or the RM tool as broker. Must work identically for four platform-team repos. **Expensive to retrofit — decide before the first component requirement is authored.** |
| **C8** | What `component/` means | n/a | component **interfaces** (L2) | **Both.** `component/interfaces/` (PRAK, exists) + `component/requirements/` and `component/architecture/` (new). Consistent: `component/` is the tier, subdirectories are the artifact types — same shape as `product/` and `system/`. |
| **C9** | Trace ID allocation | none | TM-`<n>`, allocated by reading the matrix, order load-bearing | **Drop it.** A hand-maintained matrix whose *row order* is load-bearing does not survive four repos and concurrent PRs. Recommend generating traceability from frontmatter instead, making H9 unnecessary. Biggest simplification available. |
| **C10** | Mandatory vs optional content | — | — | **Specified-but-optional.** The standard specifies every artifact type; a repo may omit types it does not use, but anything present must conform. Avoids forcing agile-planning on every repo or stripping it from PRAK. |

---

## 3. Proposed target structure

```text
<repo>/
├─ product/          personas · use-cases · requirements · interfaces (L0) · architecture
├─ system/           requirements · architecture · interfaces (L1) · data · deployment · decisions
├─ subsystem/        requirements · architecture                          [platform-team repos]
├─ component/        requirements · architecture · interfaces (L2)        [platform-team repos]
├─ prd/              PDP-08 section sources
├─ extensions/       safety · security · coding · testing · qa-cm · change-risk · metrics
├─ traceability/     TRACEABILITY.md · STANDARDS-MAPPING.md
├─ glossary/ reference/ templates/ tools/ tests/ example/
└─ repo-standard.yaml    declares: standard version · tiers used · table-format · RM tool
```

`repo-standard.yaml` is the conformance declaration C10 and C5 need — one file
saying which parts of the standard this repo implements, which the validator
reads instead of assuming.

Tier ownership, for the platform-team split:

```text
product → system          mastered in prak-v-model      (Jama 156 PLAT3)
subsystem → component     mastered in platform repos    (Jama 169 + siblings)
```

---

## 4. Sequence

| Step | Work | Gate |
|------|------|------|
| 1 | Ratify §2 conflicts | **This document** |
| 2 | Harvest validator: H1, H2, H6, H7 (the foundation) | Tests green on all three repos' fixtures |
| 3 | Harvest H3, H4, H5, H8; add H11–H13 stubs | — |
| 4 | Add the component tier (H15) + `repo-standard.yaml` | — |
| 5 | Answer C7 and implement it | **Before any `compreq-` is authored** |
| 6 | Freeze template v1.0; tag it | System Architect review |
| 7 | Conform `polymorphous-v-model` → `embedded-core-v-model` | — |
| 8 | Conform `prak-v-model` | Erich Felger ratifies |

Steps 2–4 are template-internal and safe. Step 8 touches a repo owned by the
System Architect and is the only one with an external dependency.

---

## 5. Defects found in the template while surveying

| Item | Detail |
|------|--------|
| `repo_structure.md` contains the **same tree twice** | Second copy differs only by including `repo_structure.md` itself. Looks like a bad paste, in the file that is supposed to define the standard. |
| `repo_structure.md` is **stale** | It still lists `config/pre-commit-config.yaml`, which no longer exists — the file was moved to `.pre-commit-config.yaml` at the root. It also omits `.github/`, `.gitignore`, `.pre-commit-config.yaml`, `.claude/`, `example/traceability/` and `standard/`. The document defining the standard does not match the repo it describes. |
| No `LICENSE` | `polymorphous-v-model` and `prak-v-model` both have one. |
| `extensions/` has no `security/` | Already tracked in `TODO.md`; C-level gap given IEC 62443 / ISO 21434 exposure. |

---

## 6. Open questions

1. **C7 — cross-repo trace resolution.** The one genuine blocker. Everything else
   is reversible; this is not, once artifacts exist.
2. **Do GNC, ODOA and Electronics definitely get repos?** The standard is shaped
   very differently for one platform-team repo versus four.
3. **Does the Embedded Software framework have a code repo?** If so, component
   requirements should allocate to modules in it, and it becomes the verification
   target — which changes what `allocation` means at the component tier.
4. **Who ratifies the standard itself?** PRAK's rule is *the AI Architect proposes;
   the Human Architect ratifies*. No equivalent is stated for the template, and the
   standard now governs a repo Patrick does not own.
