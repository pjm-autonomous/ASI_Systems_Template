# Phase 3 — Harvest Register

**Date:** 2026-09-13
**Owner:** Patrick McKee
**Governs:** which tools, skills and agents the template takes from `axs` and
`prak-v-model`, and which it declines.

Applies the principle from `plan.md` without softening it:

> A tool is added **only where a named, counted failure demands one.** Every
> tool ships with the failure it prevents recorded beside it.

An item on this page is **not** approved by appearing here. Approval is the
`Build` or `Harvest` disposition plus a counted failure in the same row. An item
with no count is `Defer`, and the reason it has no count is stated.

---

## 1. What was inventoried

Walked 2026-09-13 across both source repos. Counts are of files and directories
as they exist today, not carried over from a prior audit.

| Source | What | Count |
|--------|------|------:|
| `axs` | `AxS/skills/` — real skills | 19 |
| `axs` | `AxS/skills/` — `*-workspace/` directories | 12 |
| `axs` | `AxS/agents/` — agents | 27 |
| `axs` | `AxS/agents/` — templates and master index | 3 |
| `axs` | `scripts/` — top level | 7 |
| `axs` | `scripts/jama/` | 16 |
| `prak-v-model` | `.claude/skills/` | 12 |
| `prak-v-model` | `.claude/agents/` | 1 |
| `prak-v-model` | `tools/` | 6 |
| | **Total inventoried** | **103** |

The template today holds 15 skills, 1 agent and 4 modules under `tools/`. Phase 3
is not an exercise in making those numbers converge.

---

## 2. Three findings that shape the harvest

Recorded before any disposition, because each one removes candidates that a
straight port would have carried in.

### F-1 — 12 of 31 entries under `axs/AxS/skills/` are not skills

Every `*-workspace/` directory holds eval iteration output — the working data a
skill produced, not the skill. None carries a `SKILL.md`. They are also where the
repo-specific vocabulary is concentrated: the **nine densest directories in the
entire skills tree are all workspaces**, led by `standards-auditor-workspace/` at
**1,226** occurrences of `AxS`, `MR-SC`, `PLd`, `SOTIF`, `STPA`, `61508` or
`_registry`, against **28** in the skill it belongs to.

Rejected as a class. A template that shipped them would distribute one
programme's review transcripts as if they were tooling.

### F-2 — 12 of 27 `axs` agents duplicate a same-named skill

All eight A-series adversarial agents have a skill of the same name, as do C1,
C17, C18 and C19. Harvesting both ships one behaviour twice, under two invocation
paths that will drift apart.

The template must pick **one** carrier per behaviour before harvesting any of
this set. Recorded as open question H-1 in §6 rather than settled here: the
choice is about how this template expects tools to be invoked, not about these
particular twelve.

### F-3 — the template's own traceability matrix contradicts D-46

`traceability/TRACEABILITY.md` is declared **generated** by D-46. It ships a
section headed `## How to Update This Table` carrying hand-edit instructions —
"Add a new row whenever…", "Link using relative Markdown links…".

Phase 2 stopped all eight authoring skills writing to that file. It did not reach
the file itself, which still instructs a human to do exactly what the skills were
stopped from doing. This is the same defect Phase 2 kept finding — a prose copy
of something the standard owns, drifting from it — surviving in the one file that
most advertises the rule.

Fixed in this phase alongside the generator, not before it: an empty generated
file with no generator is not an improvement on a hand-maintained one.

### F-4 — the matrix promised three columns the model cannot link

`Architecture`, `ICD` and `Data Spec` were columns in the shipped matrix. None of
`architecture`, `interface` or `data-specification` declares a `parent-*` field in
`standard/artifact-schema.yaml` — there is no edge to follow. The worked example
filled those cells from artifacts that merely shared a feature-bucket directory
name.

Inferring lineage from a directory name is the same heuristic `tools/params.py`
refused to apply to requirement prose, refused here for the same reason: a
guessed link presented as a fact is worse than a blank, because a blank is honest
about what is not known. Recorded as **D-60**; those types are inventoried
instead of given a column.

### F-5 — and omitted three tiers that do have edges

`product-requirement`, `subsystem-requirement` and `component-requirement` had no
column, so the example's own `prodreq-`, `subreq-` and `compreq-` artifacts
appeared nowhere in the file that calls itself "the single place to check does
everything trace to something real". Its rows jumped use case straight to
capability requirement — the same skip `tests/test_example.py` exists to prevent
in `example/`, surviving in the matrix that describes it.

Both are fixed by deriving the columns from the schema rather than declaring them,
which also means adding a tier changes the matrix with no edit to the generator.

---

## 3. Wave 1 — build, one counted failure each

Builds rather than ports. Where a source implementation exists it is named as a
precedent, with the reason it cannot be taken as-is.

| # | Item | Counted failure | Precedent, and why not a port |
|---|------|-----------------|-------------------------------|
| **1.1** ✅ | `param-*` resolution check — **shipped** as `tools/params.py` | `prak-v-model` carries **223** requirement files and **136** `TBD`/`TBR` occurrences across **37** files, against **0** `param-*` artifacts. **9** requirement files cite a bound with nowhere to hold its value. | None. `axs` has no equivalent type. Pure build. |
| **1.2** ✅ | `TRACEABILITY.md` generator — **shipped** as `tools/trace.py` | D-46 declares the matrix generated; nothing generates it. The shipped matrix is **one empty row** plus hand-edit instructions (F-3). | `axs/scripts/build_trace_matrix.py` (467 lines) maps **test → requirement** from pytest markers. The template's matrix is **persona → architecture**. Different axis; the traversal is not reusable. |
| **1.3** | Body-table generator from frontmatter | **104 of 207** requirements had a body table disagreeing with frontmatter, or using unsanctioned row labels (`S1`/`E3`). | `prak-v-model/tools/prd_build` is reference only per D-31 — it renders a PRD document, not artifact body tables. |
| **1.4** | Maturity-gated ID minting at M3 | Duplicate Trace IDs reached `main` (`I3`); padding drift (`I5`). Both caused by reading the file to find the next free id. | `prak-v-model/tools/next_id.py` (199 lines) allocates and preflights correctly and **is harvestable**. Missing: the M3 gate, the notification, the timer, the acceptance record (D-43). Port the allocator, build the gate. |

**Recommended order: 1.1, then 1.2.** 1.1 is the cheapest and closes the gap that
makes a requirement unverifiable by construction. 1.2 unblocks 1.5 and removes F-3.

### 1.1 — done 2026-09-13

`tools/params.py`, wired into `tools/validate.py` behind the `params` packet and
covered by 46 tests. Checks: a citation that does not resolve; a cited parameter
whose value is a placeholder; `Cited By` drift in both directions; and, as notes
rather than errors, an uncited placeholder and an orphan parameter.

**It found a defect in this template's own `example/` on its first run.**
`param-battery-reserve-threshold.md` listed `sysreq-battery-threshold-monitor.md`
under `Cited By`; that requirement — whose statement says "the configured
low-battery threshold" — cited no parameter at all. The link existed in one
direction only, in the worked example every instantiated repo copies. Fixed by
making the requirement cite the parameter, which is what it should have done.

Deliberately not built: bare-number detection in requirement prose. It needs a
heuristic, and a heuristic there produces false positives at a rate that gets the
whole check ignored — which also teaches people to skip the checks that are right.
`Cited By` is checked rather than generated, recorded as **D-58**.

### 1.2 — done 2026-09-14

`tools/trace.py`, the `build-traceability` command, a `--check` mode run by CI
and a pre-commit hook, and 27 tests. Writes to `traceability/TRACEABILITY.md`
(**D-59**, answering H-3 — `axs` writes into `_registry/`; this standard keeps
`traceability/` as the one place a reader looks for coverage).

**Building it found two more defects in the shipped matrix**, neither of which
was F-3. They are recorded as F-4 and F-5 below because they change what the
generator emits, not merely how it is maintained.

The `--check` idea is the one thing taken from `axs/scripts/build_trace_matrix.py`:
currency is a failure independent of correctness. A matrix that was right last
month and has not been regenerated passes every other check in the repo.

One interaction worth recording, because it will recur with every generator that
names artifacts: the generated matrix lists parameter filenames, which made a
`tools/params.py` test read the matrix as a citer of every parameter. Production
was never affected — `validate.py` collects only schema-matched artifacts, and
the matrix is not one — but a test helper using `rglob("*.md")` was. Any future
check that scans "all Markdown" will hit this; scan the artifact globs instead.

### Deferred out of Wave 1

| Item | Why it waits |
|------|--------------|
| **1.5** Conformance report / coverage dashboard | Counted at **316 rows, 316 placeholders, 0 populated** (`E5`) — but it reports *on* the matrix. Building it before 1.2 means building a reader for a file with no writer. `axs/scripts/check_trace_coverage.py` is the precedent. |
| **1.6** Tool packet composer | No count. Nothing has yet been deployed to a repo at a declared level, so no packaging failure has occurred. Revisit in Phase 4. `prak-v-model/tools/package_skills.py` packages skills but is not level-aware. |

---

## 4. Wave 2 — the adversarial set

`axs` holds 19 skills and 27 agents, most of them adversarial review. The template
has **none** — the `adversarial` stage of the agreed five-stage taxonomy is empty.

That is a gap. It is not yet a counted failure, and the distinction is the whole
point of the governing principle. No review conducted against this template has
yet missed something an adversarial skill would have caught, because no review has
yet been conducted against this template.

**Wave 2 opened 2026-09-14** by D-65, before the gate below was met. The gate stands as the bar for each individual skill: a skill is harvested only when a counted failure is named beside it in this register. `decomposition-challenger` was first because its Challenge 4 addresses a **250-artifact** misplacement counted the same day (§4a). A skill that cannot earn a count is left in the pool.

The original gate, kept because it is still the right test: harvest an adversarial skill when a
review of a template-governed artifact misses a defect that skill would have
caught, and record the miss. Phase 4's pilot in `prak-embedded-core` is the first
opportunity to generate that evidence.

The eight most portable of the 18 candidates, ranked by repo-specific term density
in the skill body, lowest first:

| Skill | Density | Serves |
|-------|--------:|--------|
| `requirements-quality` | 7 | EARS enforcement; overlaps the template's own `requirement` skill |
| `odd-reality-checker` | 8 | operating-domain bounds |
| `decomposition-challenger` | 16 | tier decomposition — the template's own model |
| `architecture-decision-challenger` | 17 | ADRs |
| `interface-integrity-auditor` | 22 | **D-04 interface authority** — closest fit to a decision this standard already carries |
| `standards-auditor` | 28 | `traceability/STANDARDS-MAPPING.md` |
| `cybersecurity-red-team` | 32 | the open `extensions/security/` gap |
| `m3-review-assist` | 61 | the M1–M4 scheme in `tools/maturity.py`, already adopted |

Density estimates portability, not value. `m3-review-assist` is the densest of
these and also the most directly applicable, because the template already runs the
scheme it assists.

**Not candidates:** `sanctuary` (an AxS process with no template equivalent), and
the three functional-safety C-series agents — `C14` SISTEMA PL, `C16` SOTIF, `C2`
HARA/STPA. Those belong to a safety extension if the template ever grows one, not
to the core standard.

---

## 4a. Wave 2 progress — harvested skills

Each row is a skill in `.claude/skills/`, with the counted failure that earned it.
A skill with no count is not here and is not harvested.

| Skill | Counted failure | Landed |
|-------|-----------------|--------|
| `decomposition-challenger` | **250 artifacts at a level that does not own them**, across two repos, counted 2026-09-14. A repo declaring L1 holds **208** system requirements (L2) and **20** use cases (L0); its own 15 capability requirements sit under `product/requirements/`. The designated L2 pilot holds **22** artifacts, all L0, with its three owned tiers empty. Every one passed validation — a validator checks that a reference *resolves*, not that the thing it resolves to *belongs where it is*. | 2026-09-14 |
| `interface-integrity-auditor` | **228 unresolved fields across 10 interface artifacts**, counted 2026-09-14 — every one of the ten carried at least three, one carried 124. Not a single interface in that repo was fully specified. A validator checks that required frontmatter is *present*, not that the contract underneath it *says anything*: an interface whose transport, encoding and failure semantics all read `TBD` passes every check here and binds nobody. | 2026-09-14 |
| `requirement` (audit mode) | Merged, not added: `requirements-quality` overlapped the existing `/requirement` skill. Shipping both would have put the writing rule and the rejecting rule in two files (D-67). | 2026-09-14 |

### Porting rules, set by the first port

1. **Translate levels to tiers.** The source repo uses `L0 → L1 → L2` for
   requirement abstraction. Here a level is a property of a **repo** (D-01) and
   the chain is made of **tiers**. Copying the source vocabulary produces wrong
   findings and invites naming a directory after a level (D-14).
2. **Strip source-repo identity.** Enforced by `tests/test_skill_portability.py`
   — 405 such tokens sit across the 19 skills in the pool, so a missed one is
   arithmetic rather than diligence.
3. **Name no safety-integrity level.** This template declares no such field; a
   skill asserting `PLd` states a target no governing document here sets.
4. **Keep the counted failure, drop the instance.** State the shape and the
   number in the skill; record which repos in this register. A skill naming
   another programme's repos is not portable.
5. **Do not duplicate an existing skill.** Merge what is missing into the skill
   that already exists (D-67). Shipping a second one is F-2 in a new form.
6. **Record no provenance** (D-66). Where the skill came from is unnecessary
   context in a stand-alone template. What the port *taught* is kept; where it
   came from is not.
7. **Every findings table is declared as output**, carries **File** always and
   **Line** where a specific statement is at fault, and defines **every** verdict
   it uses — not just the ones the source repo happened to define.
8. **Use this repo's formatting.** Markdown tables, not fenced ALLCAPS field
   blocks. Match the existing skills in `.claude/skills/`.

### On hold, by decision

`sanctuary` and the functional-safety agents (SISTEMA PL, SOTIF, HARA/STPA) are
**held** rather than rejected, until the clearly applicable tools have landed
(SE, 2026-09-14). Revisit after the skills PR.

---

## 5. `prak-v-model` — item by item

| Item | Disposition | Reason |
|------|-------------|--------|
| `tools/next_id.py` | **Harvest** (1.4) | Allocator is sound and repo-agnostic; the M3 gate is what must be built around it. |
| `tools/validate_skills.py` | **Harvest, deferred** | Its dead-path-reference checker is the tool the TODO's *reference and path verification sweep* would justify. TODO says run the sweep by hand first so the tool is justified by a number. Correct order — harvest **after** the sweep returns a count. |
| `tools/package_skills.py` | **Defer** | See 1.6. No counted packaging failure yet. |
| `tools/prd_build/` | **Reference only** | D-31. PRD-document-specific. |
| `tools/validate.py` | **Superseded** | The template's `tools/validate.py` is the schema-driven successor. |
| `tools/mkdocs_hooks.py` | **Reject** | 25 lines, and the template ships no docs site. Revisit only if the docs-site item in `TODO.md` is taken. |
| skills `architecture`, `capability-requirement`, `persona`, `requirement`, `system-requirement`, `use-case` | **Superseded** | Phase 2 wrote the template's own against the re-tiered schema. Porting these would reintroduce the pre-re-tier model. |
| skills `jama-import-workbooks`, `jira-import` | **Defer** | Both depend on an authenticated connector a fresh repo does not have — the exact "environment assumption" the portability audit in `TODO.md` exists to catch. Revisit with that audit. |
| skill `crossover-adjudication` | **Candidate** (Wave 2) | Adjudicating a boundary between two parties is D-04's subject. Read against D-04 before porting: if it lets two peers settle their own interface, it contradicts the standard. |
| skill `propose-requirement` | **Candidate** (Wave 2) | Overlaps the template's `requirement` skill; needs a diff before either changes. |
| skill `ai-architect-review` | **Defer** | No count. |
| skill `prak-team-board` | **Reject** | Names a specific team and board. Project-scoped by construction. |
| agent `derive.md` | **Superseded** | The template ships its own. |

## 5a. `axs/scripts/` — item by item

| Item | Disposition | Reason |
|------|-------------|--------|
| `build_trace_matrix.py` | **Reference** (1.2) | Wrong axis. Its `--check` idea is worth taking: *is the tracked file still what the generator would emit?* Tagging and currency are independent failures — a fully tagged matrix describing last month's collection passes the tagging gate and is still wrong. |
| `check_trace_coverage.py` | **Reference** (1.5) | The inverse check — a requirement with no verifying test. Reusable idea, AxS-shaped implementation. |
| `check_conformance_currency.py` | **Reference** (1.5) | Catches an audit that under-reports the system. Depends on `CONFORMANCE_*.md`, which the template has no equivalent of. |
| `check_normative_diff.py` | **Strong candidate, pending a count** | Enforces that a file whose normative fingerprint changed must move its `**Status:**` line in the same commit. The template **already runs that status scheme** (`tools/maturity.py`). Without it, `_registry/` evidence attaches to content no reviewer saw. See H-2. |
| `extract_standard.py`, `repair_clause_headings.py` | **Reject** | PDF ingestion for the `Standards/` library. `traceability/STANDARDS-MAPPING.md` names standards; it does not host their text. |
| `record_test_run.sh` | **Reject** | AxS SIL test harness. |
| `scripts/jama/` (16 scripts) | **Reject as a set** | Built to load one Jama project from one document structure, and blocked upstream regardless by X-01 and the External ID backfill (X-05). Revisit only if X-01 resolves. |
| `AGENT_TEMPLATE.md`, `REPORT_TEMPLATE.md`, `agent_00_master_index.md` | **Reference** | Structural precedent for how an agent set is documented, should H-1 settle on agents. |

---

## 6. Open questions this phase must answer

| # | Question | Blocks |
|---|----------|--------|
| ~~**H-1**~~ | ~~Skill or agent?~~ — **answered 2026-09-14 (D-65): skills first, in their own PR; agents after, grouped by type or function.** One part remains open: for the **12 duplicated pairs**, does the behaviour ship once as the skill, or twice? Harvesting proceeds on *once, as the skill* — shipping both is the F-2 defect in a new form. Say otherwise and it changes. | — |
| **H-2** | Does `check_normative_diff.py` have a count here? It needs a case where a template-governed artifact changed normatively while keeping its `**Status:**`. The template has no such history yet; `prak-v-model` and `axs` may. Count before building. | `check_normative_diff` port |
| **H-3** | Does the generated matrix live at `traceability/TRACEABILITY.md` or the repo root? `axs` writes to `_registry/`; this template holds `traceability/`. Settle before 1.2 writes anything. | Wave 1.2 |

---

## 7. Disposition of all 103 inventoried items

| Disposition | Count | Meaning |
|-------------|------:|---------|
| **Harvest** | 2 | `next_id.py` now; `validate_skills.py` once the sweep returns a count. |
| **Candidate, gated** | 20 | 18 `axs` skills + `crossover-adjudication` + `propose-requirement`. Gate is a recorded review miss, not a schedule. |
| **Held by H-1** | 12 | The agent/skill duplicate pairs. Undecided carrier, so undecided item. |
| **Superseded** | 8 | Phase 2 wrote the template's own. |
| **Defer** | 16 | Named reason, no count: 12 C-series agents, `package_skills`, 2 connector-dependent skills, `ai-architect-review`. |
| **Pending a count** | 1 | `check_normative_diff.py` (H-2). |
| **Reference only** | 7 | Read for the idea; not ported. |
| **Reject** | 37 | 12 workspace directories, 16 Jama loaders, 2 PDF tools, 3 functional-safety agents, `sanctuary`, `record_test_run.sh`, `mkdocs_hooks.py`, `prak-team-board`. |
| | **103** | |

103 items inventoried. **Two approved to harvest, four approved to build** — six
pieces of work, each carrying a count. Everything else is named, dispositioned,
and waiting on evidence rather than on enthusiasm.
