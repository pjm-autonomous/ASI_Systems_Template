# ASI Systems Standard — Phased Plan for the Template Repo

**Date:** 2026-09-11
**Owner:** Patrick McKee
**Governing principle, agreed 2026-09-11:**

> Convention + checklist + human review. A tool is added **only where a named,
> counted failure demands one.** Every tool ships with the failure it prevents
> recorded beside it.

Foundational first, then content, **file by file**, refining one step at a time.
Risks and gaps are recorded as we pass them, not deferred to a separate exercise.

---

## 1. Foundations this plan rests on

Stated once, elsewhere. This plan does not restate them:

| Document | Holds |
|----------|-------|
| **`decisions.md`** | every ratified decision, one row each |
| **`tier-schema.md`** | levels, tiers, ownership, interface authority — **and the architecture diagram** |
| **`artifact-schema.yaml`** | the artifact model, as data |
| **`checklists/`** | how to do the work by hand, no tooling |

Phase 0 is complete: those four exist. What follows corrects the code to match
them.

## 2. Phases

Each phase ends in a state the repo can be reviewed in. No phase depends on a
decision that has not been made.

### Phase 0 — Lock the foundation *(no new tools)* ✅ COMPLETE 2026-09-12

Convention work only. Nothing is automated here.

| # | Step | File(s) | Done when |
|---|------|---------|-----------|
| 0.1 ✅ | Tier schema recorded as normative, with architecture diagram | `standard/tier-schema.md` | done |
| 0.2 ✅ | Governing principle recorded | `CLAUDE.md`, `CONTRIBUTING.md` | done, with the four failures it reacts to |
| 0.3 ✅ | Levels restated as repo-scoped | `repo-standard.yaml` | `levels.map` replaced by `level: L1` |
| 0.4 ✅ | New-repo checklist | `standard/checklists/new-repo.md` | 30 items, zero tooling required |

**Risk recorded:** the level numbering still has no org-wide ratification
(`G3` three schemes; `G7`, `G10` open). Phase 0.1 states *our* schema and marks it
as the standard's, not as agreed org-wide.

### Phase 1 — Correct the model *(schema edit)* ✅ COMPLETE 2026-09-13

| # | Step | File(s) | Done when |
|---|------|---------|-----------|
| 1.1 | Re-tier the artifact model | `standard/artifact-schema.yaml` | Tiers reflect §1: use-case and safety/performance requirements at L0; capability requirement at L1; system / sub-system / component at L2 |
| 1.2 | Remove the hinge | same | `system-requirement` occupies one tier; the L1→L2 join becomes a cross-repo parent |
| 1.3 | Collapse interface tiers to the recursive rule | same | One `interfaces/` per repo, describing the level below |
| 1.4 | Level becomes repo-scoped | `tools/schema.py`, `tools/validate.py` | `build_bindings` takes a level, not a tier→level map |
| 1.5 | Re-point the broker | `repo-standard.yaml` | An L2 repo declares `axs`-then-`prak` chain correctly; parent is a **capability requirement**, not a system requirement |
| 1.6 | Update tests | `tests/` | Existing 112 pass against the new shape; hinge tests replaced |

**No new tools.** This is correcting what exists.

### Phase 2 — Template content, file by file *(the bulk of the work)* ✅ COMPLETE 2026-09-13

Walk the repo in dependency order. For each file: read it, correct it against
Phases 0–1, record any gap found, move on. **This is review work, not tooling
work** — it is where the agreed principle is actually exercised.

Suggested order, foundational outward:

1. ✅ `CLAUDE.md`, `README.md`, `CONTRIBUTING.md` — the entry points *(b5bb759)*
2. ✅ `standard/` — decisions, tier schema, artifact schema, plan, checklists
3. ✅ `templates/` — every type, schema-checked
4. ✅ tier directories re-tiered; 13 tier READMEs
5. ✅ `glossary/` — rewritten as an index
6. ✅ `reference/`
7. ✅ `prd/`
8. ✅ `extensions/` — `security/` gap surfaced in the README
9. ✅ `example/` — rebuilt and validated by `tests/test_example.py`
10. ✅ `.claude/` — 9 corrected, 4 written, `tests/test_skills.py` added

**Gate at each file:** does anything here assert a decision that is not recorded
in `standard/`? If yes, either record the decision or delete the assertion. That
single question is what caught the PLd default and `refinement-status`.

### Phase 3 — Tools, only where Phase 2 named a failure (in progress)

Not a fixed list. Phase 2 produces the candidates, each with a counted failure.

**The candidates, their counts and their dispositions live in
`standard/phase-3-harvest.md`** — 103 items inventoried across `axs` and
`prak-v-model`, every one dispositioned. That register is the single source for
what this phase builds, harvests, defers and rejects; this plan does not restate
it.

Already built, failures named retrospectively: template drift (`A7`), broken
cross-repo parent references (`A1`/`S3`), level renumbering cost (26 files).

**Everything else waits for Phase 2 to name its failure.**

### Phase 4 — Pilot in `prak-embedded-core`

Per `R3`/`R7`: complete the template, then pilot. Not before.

---

## 3. Sequencing note — why content before more tooling

The five-stage tool taxonomy (define → populate → assess → report → gate →
adversarial → integrate) remains the right *classification*. It is deliberately
**not** the build order here.

Reason: four of the six failures above were caused by tools built ahead of the
decision they encoded. Phase 2 is what produces ratified decisions; tools built
after it encode something real. Building stage-by-stage instead would repeat the
pattern that produced `refinement-status`, the dormant `validate-skills`, and the
unpopulated matrix.

---

## 4. Open, tracked, not blocking Phase 0–2

| Item | Status |
|------|--------|
| Erich's reply on the tier schema | **Closed 2026-09-14 — confirmed** (D-61). The schema is ratified; Phase 0.1's provisional framing no longer applies. |
| Jama single-project decision (`X1`) | Erich → Dallon Schofield. Jama work paused; the 169 structure spec stays a design for review. |
| Jama External ID backfill | Still null on every sampled requirement. Blocks mechanical cross-repo traces, not the template. |
| `G7`, `G10` | Level-2 subfolders as team groupings; two tiers below system vs one. Both unanswered. |
| TIM rules | **Closed for repo purposes.** Org-admin configuration, not viewable at SE permission, and deliberately not mirrored in any repo (2026-09-11). The capture file has been deleted and all citations repointed. |

---

## 5. First step

**Phase 0.1** — write `standard/tier-schema.md` from §1 above, as the single
normative statement every other file references. It is a convention file, needs no
tooling, and every later phase depends on it being settled.
