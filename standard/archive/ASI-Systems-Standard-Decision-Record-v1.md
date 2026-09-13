# ASI Systems Standard — Decision Record

**Revision:** v1 (v0 archived at `archive/ASI-Systems-Standard-Decision-Record-v0.md`)
**Status:** Conflicts ruled; three items still open
**Date:** 2026-09-10
**Owner:** Patrick McKee (Systems Engineer)
**Approach:** harvest `prak-v-model` into this template, reconcile conflicts, freeze
the template as normative, conform all repos to it.

**v1 changes:** records Patrick's rulings on C1–C10 and H1–H17; folds in the
2026-09-09 PRAK Architecture / Repo Review outcomes; adds §7 (distribution gap),
§8 (maturity tagging), §9 (level-scheme contradiction), and the H1 worked example.

---

## 1. Rulings on conflicts

| # | Conflict | **Ruling** |
|---|----------|-----------|
| **C1** | Interface prefix `icd-` vs `int-` | **Template adopts `int-`** to match `prak-v-model`. |
| **C2** | Interface location | **Open pending §9.** PRAK encodes boundary level as directory — see §3. Yesterday's architecture decisions may move it. |
| **C3** | `product` vs `capability` requirement | **Template adopts `capability requirement`**, matching both `prak-v-model` and Jama terminology. Retire "product requirement". |
| **C4** | Is a parent required? | **Yes — everything flows upward** to a customer-defined need, safety included. The parent need not live in the same repo or architecture level (a use case may define safe deployment, connect to AxS, and become ancestral). So: parent **required**, resolution **may be cross-repo**. This makes C7 mandatory, not optional. |
| **C5** | Markdown vs HTML tables | **Markdown is the standard** (`prak-v-model/ai-context/03-conventions.md`). HTML is legacy; PRAK converts files as they are touched. Validator accepts both during transition. |
| **C6** | Verification methods | **Keep the restricted set** — Test, Analysis, Inspection, Demonstration. Deliberately tighter than Jama. My v0 recommendation to adopt Jama's superset is **withdrawn**. |
| **C7** | Cross-repo parent resolution | **Open — recommendation in §5.** Direction: use cases and capability requirements exclusive to L1/L2; system requirements the lowest level in L1/L2 **and** the highest in L3 and below. |
| **C8** | What `component/` means | **No component level in `prak-v-model`.** Verified below: Jama *does* permit it, so the boundary is a convention Jama will not enforce. |
| **C9** | ID scheme | **Contiguous and unique IDs within a repo, enforced by workflow — port to the template.** Cross-repo ID rigor undefined; recommendation in §6. |
| **C10** | Mandatory vs optional | **Packets to choose from**, if achievable with native GitHub functionality. See §7 — this is harder than it looks. |

### C8 verification — does Jama allow component requirements?

**Yes.** Item type **201 `CMPRQ` "Component Requirement"** is in the allowed-item-type
list for **both** project 156 (`PLAT3`) and project 169 (`POLY`), and TIM rule 593
permits System Requirement → Component Requirement via Derive. Read 2026-09-09;
full evidence in `polymorphous-v-model/jama/tim-relationship-rules.md`.

**Implication:** Jama will not stop anyone authoring a component requirement in 156.
If the L1/L2 boundary is to be structural rather than advisory, ask the Jama admin to
**remove `CMPRQ` from project 156's allowed item types**. Otherwise the boundary
depends entirely on discipline.

---

## 2. Harvest dispositions

| # | Item | **Disposition** |
|---|------|----------------|
| H1 | Multi-glob / multi-prefix types | Explained in §4; awaiting go |
| H2 | List-valued parents | **Adopt.** One-parent-only was a Jira limitation; the plan to track architecture in Jira is abandoned. Both GitHub and Jama support m:m. Drop the single-parent model. |
| H3 | Unique filename / id / title | **Adopt and enforce** |
| H4 | Interface catalog | **Adopt** |
| H5 | Diagram interface annotations | **Adopt**, but prefer `.puml` or another format more flexible than Mermaid |
| H6 | BOM tolerance | **Adopt**; prefers tagging/metadata over frontmatter — see §8 |
| H7 | Parse-once structure | **Adopt**; same preference — see §8 |
| H8 | Enum vocabularies | **Adopt** |
| H9 | Traceability order check | Folded into C9 |
| H10 | Agile planning types | **Do not specify in the repo.** Only requirement: a traceability expectation from work-tracking tools back to the requirements they support. See §2.1. |
| H11–H14 | ADR, data spec, deployment, extensions, PRD, glossary | **Refer to the System Architect** — his discretion |
| H15 | Sub-system / component tiers | **Adopt** |
| H16 | Cross-repo reference resolution | **No good solution yet** — same open problem as C7 |
| H17 | Requirements-tool picklist enums | **Adopt** |

### 2.1 Work-tracking traceability — the abandoned duplication

The original scheme duplicated GitHub → Jama → hand-authored Jira: a Use Case became
a Jira Objective, a Capability a Jira Initiative, a System Requirement a Jira Epic.
**That became a maintenance nightmare and was abandoned.**

Current mechanism:

```text
GitHub artifact  --(jama-mcp, semi-automated)-->  Jama item
                                                     |
                                          Jama↔Jira sync at STORY level
                                                     |
                                            Jira story ← linked to Jama sysreq
```

So the standard should require exactly one thing: **every work item traces back to
the requirement it supports**, via the Jama sysreq join. It must *not* specify
initiative/epic/story artifacts in the repo. Note the review flagged `X5` — *"the
Jira layer the tooling targets is being deleted"* — so any tooling assumption about
Jira levels above story is already stale.

---

## 3. C2 — what `prak-v-model` encodes as its boundary, and where

Boundary level is encoded as **directory position**, declared in `tools/validate.py`:

```python
INTERFACE_LEVEL_DIRS = {
    "L0": "product/interfaces",
    "L1": "system/interfaces",
    "L2": "component/interfaces",
}
```

Enforced three ways: a `refinement-level` frontmatter field constrained to
`{L0, L1, L2}`; a validator check that the declared level matches the directory the
file sits in; and `INTERFACE_CLASSES = {external-icd, internal, physical, build-time}`
classifying the boundary kind. Governing prose is `ai-context/03-conventions.md`
("Interface catalog") and `02-strategy.md`.

Reality check: `component/interfaces/` holds **one** artifact
(`int-mobius-objective-manager-icd.md`). The model is well-specified and barely
populated — consistent with review item `R5`, *"no `int-*` entries for several real
boundaries."*

**This is the only place in any of the three repos where architecture level is
machine-checked.** It is the pattern to generalize — but see §9 first, because it
hardcodes an L0/L1/L2 scheme that yesterday's decisions may have invalidated.

---

## 4. H1 explained — multi-glob / multi-prefix artifact types

**The problem.** The template binds each artifact type to exactly one directory
pattern and one filename prefix:

```python
ArtifactType(
    name="icd",
    glob="system/interfaces/*/*.md",   # ONE pattern
    prefix="icd-",                     # ONE prefix
    ...
)
```

An interface artifact can therefore only ever live at one tier. To validate
interfaces at product, system *and* component level you must declare three separate
artifact types — three names, three duplicated field lists, three sets of rules that
drift apart.

**PRAK's fix.** Widen the two fields to accept a tuple:

```python
@dataclass(frozen=True)
class ArtifactType:
    glob: str | tuple[str, ...]      # one pattern, or several
    prefix: str | tuple[str, ...]
```

One type, three locations, one rule set:

```python
ArtifactType(
    name="interface",
    glob=(
        "product/interfaces/int-*.md",     # L0
        "system/interfaces/int-*.md",      # L1
        "component/interfaces/int-*.md",   # L2
    ),
    prefix="int-",
    required_fields=("id", "title", "class", "status", "refinement-level", ...),
)
```

**Why it is the keystone.** Every tier-crossing artifact type needs it:

| Type | Lives at |
|------|----------|
| interface | product · system · component (3 locations) |
| architecture | system · product (PRAK already globs both) |
| system requirement | **lowest in L1/L2 and highest in L3** (per C7) — inherently two locations |

Without H1, the C7 model — a system requirement being the hinge artifact shared
between the L1/L2 repo and the L3/L4 repo — **cannot be expressed at all**. That is
why it is ranked first and why everything else waits on it.

Cost: two type-annotation changes plus normalizing to a tuple at the glob site.
Roughly 15 lines. Nothing else in the validator changes.

---

## 5. C7 recommendation — requirement levels and cross-repo resolution

### The constraint

Jama offers a limited set of requirement types. Confirmed available in 156 and 169:
Market Requirement (194), Product Requirement (193), System Requirement (141),
Component Requirement (201), Safety Requirement (140). That is the whole ladder —
there is no fifth or sixth tier to spend.

### Recommendation: the system requirement is the hinge, not a duplicated tier

Patrick's direction — sysreq lowest in L1/L2 and highest in L3+ — works, and it is
better than it first appears, **provided the sysreq is one artifact seen from two
sides rather than two artifacts kept in sync**.

| Level | Repo | Artifact types | Jama |
|-------|------|---------------|------|
| L0 | `axs` | Losses, hazards, safety goals | — |
| L1 | `prak-v-model` | Use case, **capability requirement** | 156 `PLAT3` |
| L1/L2 | `prak-v-model` | **System requirement** ← the hinge | 156 `PLAT3` |
| L3 | sub-system repo | **System requirement** (highest here) → sub-system requirement | 169 + siblings |
| L4 | sub-system repo | Component requirement | 169 + siblings |

**The join is Jama, and that is now settled rather than a preference.** The
2026-09-09 review answered decisions 0 and 2 identically: *"For now both source of
truth and Identity authority will continue to be Jama"* — favoured by ASI executive
and division-chief teams, changeable only on documented evidentiary justification.

So the cross-repo parent reference resolves as:

```text
compreq (L4, sub-system repo)
  → parent: subsystem requirement (L4/L3, same repo)      resolved LOCALLY
      → parent: system requirement (L3 top = L2 bottom)   resolved via JAMA
          → capability requirement (L1)                   in prak-v-model / 156
```

Only **one** link in the chain crosses a repo boundary, and Jama already owns the
identity on both sides of it.

### How to implement the cross-repo link

Recommended, in order:

1. **Reference Jama identity, not filenames.** A `compreq-` frontmatter field
   `parent-jama-key: PLAT3-SYSRQ-1195` (or the Global ID `GID-…`) is resolvable by
   *anything* — validator, Jama, a human. A filename is resolvable only by whoever
   has that repo cloned. Since Jama is the ratified identity authority, use it.
2. **Keep the slug too, as a human-readable alias** —
   `parent-system-requirement: sysreq-geofence-map-validation.md`. Shape-checked
   locally, authoritative only in Jama.
3. **Publish an index for offline validation.** Each repo emits
   `artifact-index.json` (slug → Jama key → title → status) on release. A sibling
   repo validates against the published index; CI fetches it. Avoids requiring
   sibling clones and works identically for four platform-team repos.

**Blocking prerequisite, unchanged:** Jama **External ID is null on every requirement
sampled in both 156 and 169**. It is the field that makes slug↔Jama-key resolution
mechanical, and until it is backfilled none of the above works. This is the single
highest-value unblocking action in the whole programme.

---

## 6. C9 recommendation — ID rigor across repos

Within a repo, PRAK's rule stands and ports cleanly: **contiguous, unique, enforced
by workflow.** Adopt it.

Across repos it should **not** be extended, for a reason the review itself documents:

| Review item | Finding |
|---|---|
| `I1` | requirement identity lives in **three authorities** |
| `I3` | **duplicate Trace IDs live on `main`** |
| `I5` | Trace ID zero-padding inconsistent |
| `T2` | `TRACEABILITY.md` has **no generator and nothing reads it** |

A globally contiguous ID space across four repos requires a central allocator. Jama
already is one, and it issues `PLAT3-SYSRQ-1195` / `GID-3353672` — unique across the
tenant, by construction.

**Recommendation:**

- **Repo-local IDs stay repo-local** — contiguous and unique within the repo, no cross-repo meaning.
- **Cross-repo identity is the Jama key.** Never mint a second global scheme.
- **Generate `TRACEABILITY.md` from frontmatter.** Per `T2` nothing reads it and no generator exists, so hand-maintaining row order (which PRAK's TM-`<n>` allocation depends on) is pure cost for no consumer. This retires H9 and closes `I3`/`I5` structurally rather than by cleanup.

---

## 7. C10 — the distribution gap, and why it outranks the content work

Review item **A7** is the most important finding for this template, and it changes
the priority order:

> Consumption is GitHub **"Use this template"** — a one-way copy at kickoff. There is
> **no CHANGELOG, no git tags, no version field, no submodule guidance, and no
> procedure for pulling template updates** into an existing repo. Once copied, a
> sub-system repo drifts with no way to detect it — there is not even a stamp
> recording which template version it was cut from.

Restated: **however good the standard's content becomes, it degrades to a convention
on day one of every downstream repo.** `D3` makes the same point — *"every sub-system
repo forks `templates/` on day one."*

### What GitHub actually offers

| Mechanism | Fit for "packets to choose from" |
|-----------|----------------------------------|
| **Template repository** ("Use this template") | One-way copy. No update path. What A7 indicts. |
| **Git tags / Releases** | Versions the template. **Does not** propagate to copies. Prerequisite for everything else. |
| **Submodule** | Real update path (`git submodule update`), pinned by commit. Shares one subtree — good for `templates/`, `tools/`, `extensions/`; awkward for content directories. Widely disliked by contributors. |
| **Subtree** | Copies with merge-back capability. Update is a real merge. No extra clone step. |
| **Composite Actions / reusable workflows** | Genuinely centralized — a downstream repo references `asirobots/ASI_Systems_Template/.github/workflows/validate.yml@v1`. **Updates propagate automatically on tag.** The strongest native option for the *validator*. |
| **Published Python package** | `pip install asi-se-tools==1.2` pins the validator. Standard, versioned, no git plumbing. |
| **GitHub Packages / Releases as artifact host** | Ship packets as versioned release assets a repo pulls at instantiation. |

### Recommendation

Split the standard by how each part wants to travel:

| Part | Distribution | Update |
|------|-------------|--------|
| **Validator + tooling** | Python package, pinned version | `pip install -U` |
| **CI enforcement** | Reusable workflow referenced `@v1` | Automatic on tag |
| **Templates, extensions, reference docs** | Template repo copy, **stamped** | Explicit, via a `standard-sync` skill |
| **Content (`product/`, `system/`, …)** | Copied once, owned locally | Never |

Plus the two cheap asks A7 names, which should land **first**:

1. **`repo-standard.yaml` in every downstream repo**, written at instantiation —
   template version, git SHA, date, tiers in use, table format, RM tool. This is the
   drift stamp *and* the C10 packet declaration in one file.
2. **Tag template releases.** `v0.1` today. Without a version there is nothing for a
   stamp to record.

"Packets" then become the `tiers`/`profiles` list in `repo-standard.yaml`, with the
validator enforcing declared packets only — achievable natively, no GitHub feature
required that does not exist.

---

## 8. Maturity tagging — what GitHub can and cannot do

**GitHub has no per-file tagging or metadata facility.** No mechanism attaches a
maturity value to a file and makes it queryable. Specifically:

| Considered | Why it fails |
|-----------|--------------|
| Labels | Attach to issues and PRs, never to files |
| Git tags | Repo-wide snapshots, not per-file |
| Git notes | Per-object metadata, but not fetched by default, invisible in the UI, and routinely lost |
| GitHub Projects | Tracks items, not files |
| Custom properties | Repo-level, not file-level |
| CODEOWNERS-style path file | Path→value mapping is possible, but it is a sidecar you maintain by hand |

So the realistic options are **in-file** (frontmatter or a body header block) or a
**sidecar registry**. Since the preference is to avoid frontmatter, that points
directly at the AxS approach.

### What AxS actually does — and it is a working precedent

Review item `A4`: *"AxS already runs the maturity model being proposed."*

1. **A bold key-value header block in the document body**, immediately after the H1 —
   not frontmatter:

   ```markdown
   # Agent: Decomposition Challenger
   **Agent ID:** AxS-AGENT A11
   **Version:** 1.0
   **Status:** M2+
   **Tier:** Adversarial
   **Classification:** PLd Autonomous System (AxS) Documentation Suite
   ```

2. **States M1 → M2 → M2+ → M3 → M4**, with defined gate criteria per transition.
3. **A registry directory** (`AxS/_registry/`) holding `m2_records/`, `m3_reviews/`
   and agent reports — the evidence behind each promotion.
4. **An assessor that writes the promotion back into the file**: agent C10 aggregates
   quality-gate results and, on PASS, *"updates the artifact's `**Status:**` header
   line in the source file."*
5. **Level gating**: M4 on level N requires M4 on level N−1.

**Recommendation: adopt the AxS scheme.** Reasons, in order of weight:

- It is **already running** in a sibling repo, on the same programme, reviewed by the same people — not a proposal.
- It satisfies the stated preference: metadata in a body header block, not frontmatter.
- The registry gives promotions **evidence and a date**, which a tag never would.
- It closes review item `W4` — *"no maturity gate on review."*
- AxS↔PRAK linkage is already a live programme (`A1`), and 14 Functional Safety gaps are registered against PRAK (`A2`). Sharing the maturity vocabulary removes a translation layer rather than adding one.

**Caveat to settle:** a body header block is harder to parse reliably than
frontmatter (no schema, order-dependent, easy to reformat by accident). If maturity
is to gate CI, the parser must be strict and the format specified precisely — a
regex over `**Key:** value` lines between the H1 and the first `---`. Worth doing,
but the validator has to own the format rather than infer it.

---

## 9. The level-scheme contradiction — blocking

The template is meant to serve **every level in every project**, so it must encode
levels. It cannot yet, because the schemes disagree.

| Source | Statement |
|--------|-----------|
| Patrick, 2026-09-10 | PRAK bounded at **L1 & L2**; a separate related repo covers **L3 & L4** |
| Review `R2` (DECIDED) | `axs` **L0** → ASAM **L1** → PRAK **L1** → sub-system **L2** |
| Review decision 1 (DECIDED) | *"Component tier — PRAK, or sub-system repos at L2? → **PRAK at L2**"* |
| PRAK `validate.py` | Interfaces are **L0 / L1 / L2**, L2 = `component/interfaces` |
| Review `G3` (DECIDED) | **Three** level schemes exist — SA, AxS, PRAK |
| Review `G10` (open) | *"Diagram implies **two tiers below system**, not one"* |
| Review `G7` (unanswered) | *"Level-2 subfolders are **team groupings, not subsystems**"* |

Two concrete collisions:

1. **Is a sub-system L2 or L3?** `R2` says L2, owned by the respective Systems
   Engineer. Patrick says the sub-system repo is L3/L4. Both cannot hold with one
   numbering.
2. **PRAK's validator already means something specific by L2** — component
   interfaces. If sub-systems become L3, `INTERFACE_LEVEL_DIRS` is wrong and every
   `refinement-level: L2` value shifts meaning.

**Recommendation:** before any level-aware code lands, publish a **single level
register** — one table mapping level number → owner → repo → artifact types → Jama
project, with the SA/AxS/PRAK schemes as crosswalk columns (`G3` already
acknowledges the need). Put it in the template as normative, since the template is
the thing claiming to span all levels.

Until then, hold C2 and defer H4's `INTERFACE_LEVEL_DIRS` port. Everything else in
the harvest is level-agnostic and can proceed.

---

## 10. Revised sequence

| Step | Work | Blocked by |
|------|------|-----------|
| 1 | **Tag template `v0.1`; add `repo-standard.yaml` + instantiation stamp** (§7) | nothing — do first |
| 2 | Harvest H1, H2, H6, H7 — the foundation (§4) | nothing |
| 3 | Publish the **level register** (§9) | SA + AxS + PRAK reconciliation |
| 4 | Harvest H3, H8, H17; adopt AxS maturity headers + registry (§8) | step 2 |
| 5 | Harvest H4, H5 (interface catalog, `.puml`) | step 3 |
| 6 | Add sub-system / component tiers (H15) | step 3 |
| 7 | Implement cross-repo resolution (§5) | **Jama External ID backfill** |
| 8 | Move validator to a package + reusable workflow (§7) | step 2 |
| 9 | Freeze template v1.0 | SA review |
| 10 | Conform sub-system repo, then `prak-v-model` | step 9; Erich ratifies |

Steps 1, 2 and 8 are template-internal, unblocked, and worth the most. Steps 3 and 7
are the two real dependencies and neither is mine to close alone.

---

## 11. Still open

1. **The level scheme (§9).** Blocks all level-aware work.
2. **Jama External ID backfill.** Blocks every mechanical cross-repo link.
3. **H11–H14** — ADR, data spec, deployment, extensions, PRD, glossary: referred to the System Architect.
4. **Who ratifies this standard?** PRAK's rule is *AI Architect proposes, Human Architect ratifies*. No equivalent is stated for the template, which now governs repos Patrick does not own. `A7` and `D3` both turn on this.
5. **`.puml` vs Mermaid (H5).** PRAK's `%% @interface` annotation is Mermaid-comment syntax; switching diagram format means redesigning that hook. Also note this repo renders Mermaid natively in GitHub and PlantUML does not.
