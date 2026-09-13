# ASI Systems Standard — Work Plan

**Date:** 2026-09-10
**Source:** `PRAK-Architecture-Repo-Review/PRAKArchitectureRepoReviewOutcomes.md`, updated
after the 2026-09-10 session (rows dispositioned through **A4**)
**Owner:** Patrick McKee
**Companion:** `ASI-Systems-Standard-Decision-Record-v1.md`

The review confirmed the programme's direction and the template's central role
(`R3`, `R7`, `D3`: *"Prioritize completion of `ASI_Systems_Template` then pilot
with `prak-embedded-core`"*). It also invalidated three things already built.
Those come first, because everything downstream inherits them.

---

## 1. Contradicted by the 2026-09-10 decisions — fix before building further

### C-1 The level model is wrong · **blocking**

`R2` was restated and decision 1 was reversed:

| Was implemented (2026-09-10 am) | Decided (2026-09-10 pm) |
|---|---|
| AxS **removed** from the chain | **`axs` is L0**, owned by Compliance & Safety (`R2`, `A1`) |
| ASAM at **L0** | ASAM is **categorical, not architectural** — not a level at all (`R2`) |
| PRAK spans L1–L2 | **PRAK is L1** (decision 1, explicitly changed from L2) |
| sub-system at L3–L4 | **sub-system is L2** (`R2`) |

The corrected chain:

```text
L0   axs                 Compliance & Safety     controls the L1 interface (A1)
     ASAM                categorical classification, not an architecture level
L1   prak-v-model        Systems Architect
L2   sub-system repos    respective Systems Engineer
```

**The deeper correction: levels are repo-scoped, not tier-scoped.** The current
`repo-standard.yaml` maps each *tier* to a level one-for-one, which cannot express
"PRAK is L1 and holds both the product and system tiers." Replace it:

```yaml
# This repo's position in the architecture chain.
level: L1
# The artifact tiers this repo masters, internal to that level.
tiers: [product, system]
```

Levels then describe repos, tiers describe structure inside a repo, and the two
stop fighting. This also aligns the level model with the brokering model, where a
parent is already a *repo* rather than a tier.

Cost: the level map is one table by design, so this is a small edit plus the
`levels.map` → `level` change in the loader. **Nothing else moves** — no artifact
stores a level, which is exactly why it was built that way.

Still unresolved and **not** answered by this: `G7` (level-2 subfolders are team
groupings, not subsystems), `G10` (diagram implies two tiers below system, not
one), `I2` (`NO ANSWER` — the ID standard targets the tier that has no IDs).

### C-2 Two maturity decisions disagree on mechanism · **needs a ruling**

Both are recorded as decided, and they specify different things:

| | `A4` — harvest from AxS | `P1` (via `W4`, `S0`, `T2`) |
|---|---|---|
| States | `M1 M2 M2+ M3 M4` | `draft reviewed baselined` |
| Where it lives | a `**Status:**` field in the body header | **file location** — a move between directories |
| Anti-drift | evidence record required in `_registry/` | *"maturity is a function of location, not a self-declared field that drifts"* |
| Gating | M4 at a level requires M4 at the level above | threshold gates ID assignment, `TRACEABILITY.md` entry, V&V entry |

P1 explicitly rejects the field-based approach, citing `refinement-status` (49%
adoption, tracking a distinction that does not exist) as the precedent for why a
self-declared field fails.

**What is built today is the AxS scheme**, per the instruction to adopt it — with
an evidence requirement that answers P1's drift objection by a different route: a
state at or above M2 fails validation unless a dated promotion record exists. A
field that cannot be raised without evidence does not drift.

**Recommendation — take both, they are separable:**

1. Keep **AxS M1–M4 as the vocabulary** (`A4`, and it keeps PRAK and AxS speaking
   one language — `A1` makes that linkage a live programme).
2. Adopt **P1's gating consequences**, which are the valuable half and are
   currently unimplemented: maturity threshold gates short-ID assignment, entry
   into `TRACEABILITY.md`, and entry into the V&V plan.
3. Treat **location-based segregation as optional** — a `draft/` subtree a repo
   may declare. The evidence requirement already prevents drift; requiring a file
   move as well is defensible but is a second mechanism for one problem.

Map, if both vocabularies must coexist: `M1 → draft`, `M2/M2+ → reviewed`,
`M3/M4 → baselined`.

**Open question P1 raises and nobody has answered:** does ID assignment happen at
`reviewed` or at `baselined`? P1 recommends `reviewed`, because waiting for
`baselined` means no system requirement gets an ID until hazard analysis
completes — 26% of the set today.

### C-3 The Jama 169 structure spec may be obsolete · **paused**

`X1` (DEFERRED): *"the preference is for **all PRAK artifacts in one Jama
project**. Follow-up with Dallon Schofield for SE alignment."*

`polymorphous-v-model/jama/169-structure-spec-v1.md` is built entirely on a
156/169 split, with cross-project `Derive` relationships between them. If one
project wins, the folder tree survives but the cross-project relationship design
does not.

**Do not implement that spec until `X1` resolves.** The TIM capture
(`jama/tim-relationship-rules.md`) stays valid either way — it is tenant-wide
configuration.

---

## 2. New work the decisions created

Ranked by whether something else waits on it.

| # | Work | Source | Size | Waits on |
|---|------|--------|------|----------|
| **W1** | Correct the level model to repo-scoped (C-1) | `R2`, decision 1 | S | — |
| **W2** | Rule on the maturity conflict, then implement the gating half (C-2) | `A4` vs `P1` | M | a ruling |
| **W3** | **P2 — generate the body table from frontmatter** | decision 3, `S1`, `T1` | **L** | — |
| **W4** | **P3 — `param-*` artifact type** for program-declared values | decision 4, `V2` | M | — |
| **W5** | **T2 — generate `TRACEABILITY.md`** | `T2` | M | W2, W3 |
| **W6** | Harvest AxS **agents** (not just the maturity schema) | `A4` | **L** | — |
| **W7** | Structure the template for **compliance evidence** | `S5` | M | review with Erich + Ben |
| **W8** | **T3 — consolidate skills** into the template, repair, test, version them from `system-engineering-tools` | `T3` | L | — |
| **W9** | P4 — declare the tier boundary explicitly | `P4` | S | mostly done by `repo-standard.yaml` |
| **W10** | Plan the bulk **HTML → Markdown** conversion, executed in reviewable chunks | `D1` | M | PRAK-side |

### Notes on the larger ones

**W3 (P2) is the highest-value item on the list.** It fixes 104 of 207
non-compliant requirements *structurally* rather than by hand, and prevents the
105th: a generated table cannot disagree with frontmatter, cannot use an
unsanctioned row label, and cannot hold an out-of-enum value. The enabling work is
already done in PRAK — PR #41 taught the verifier to compare both table forms, and
PR #40 proved an HTML→Markdown conversion content-neutral. It also subsumes W10:
once the body table is generated, the HTML/Markdown question stops being a
migration and becomes a renderer setting.

**W4 (P3) is cheap now and was not before.** With the artifact model as data, a
`param-*` type is a schema entry plus a validator rule that every cited parameter
resolves. It unblocks `V2` (17 named bounds, zero values) and `E5`/`E6`, which the
proposal calls *"one blocker seen from two directions"* — every timed requirement
is unverifiable by construction until parameters have a home.

**W6 is larger than it sounds.** `A4` says harvest the schema, gates, process
**and agents**. AxS ships ~30 agents (C1–C19 constructive, A1–A13 adversarial)
including the maturity gate assessor that writes promotions back into files. Only
the state vocabulary and the evidence rule are built so far.

**W8 has a subtlety.** `T3` says to lock skills down as *versioned artifacts from
`system-engineering-tools`* — a repo no session has read yet. That is a
distribution question, and §7 of the decision record already answered the shape:
tooling travels as a pinned package, not as a copied directory.

---

## 3. Confirmed by the review — no change needed

Worth recording so they are not re-litigated:

| Item | Confirms |
|------|----------|
| `A1` *"Establish dynamic upward linkage between repos"* | The broker (`tools/broker.py`) is exactly this. Upward enforcement, built and tested. |
| `S3` *"Subsystem will move to separate repo. Create dynamic link back to `prak-v-model`"* | Same mechanism. |
| `S7` *"AxS will be the authoritative parent"* | The parent declaration in `repo-standard.yaml` — now pointing at `axs` for L1, not only PRAK for L2. |
| `T2` *"`TRACEABILITY.md` has no generator and nothing reads it"* | Confirms decision-record C9: generate it, retire the hand-maintained TM-ID ordering. |
| `M2` platform-team is **team-based** | The enum stays an enum; membership is by team. |
| `D3` *"Template should apply at all levels and draw from `axs`"* | Template scope confirmed; adds `axs` as a harvest source alongside PRAK. |
| decisions 0 and 2 | Jama remains source of truth **and** identity authority. Cross-repo identity is the Jama key, as recommended. |

Also corrected: the sub-system repo is **`prak-embedded-core`** (`R3`, `R7`), not
`embedded-core-v-model` as `HANDOFF.md` recorded.

---

## 4. Sequence

```text
NOW ──────────────────────────────────────────────────────────────
  W1  level model -> repo-scoped                      (small, unblocks nothing else but is wrong today)
  W4  param-* artifact type                           (cheap now the schema is data)
  W3  P2 generated body tables                        (highest value; large)

THEN ─────────────────────────────────────────────────────────────
  W2  maturity gating half            <- needs the C-2 ruling
  W5  TRACEABILITY generator          <- needs W2 + W3
  W6  AxS agent harvest
  W8  skills consolidation + versioning

REVIEW-GATED ─────────────────────────────────────────────────────
  W7  compliance evidence structure   <- review with Erich + Ben before implementing (S5)
  W10 HTML -> Markdown bulk plan      <- subsumed by W3 if W3 lands first

PAUSED ───────────────────────────────────────────────────────────
  Jama 169 structure spec             <- X1: one Jama project or two? (Dallon Schofield)
  Cross-repo Jama-key traces          <- External ID still null on every sampled requirement
```

---

## 5. Decisions needed from you

1. **C-2** — AxS M1–M4 field-based, P1 location-based, or the hybrid recommended above?
2. **P1's open question** — does short-ID assignment happen at `reviewed` or at `baselined`?
3. **W3 scope** — does the template grow its own table generator, or port PRAK's `tools/prd_build`? PRAK's is proven but carries PRD-specific baggage.
4. **W6 scope** — all ~30 AxS agents, or the maturity-gate assessor plus the terminology watchdog first?

---

## 6. Rows still blank in the outcomes record

The session stopped at `A4`. These remain undispositioned and several bear
directly on the template:

`S4` · `R4` · `R5` · `R6` · `M1` · `M3` · `M4` · `M5` · `M6` · `T5` · `T6` · `T7` ·
`D4` · `D5` · `D7` · `X4` · `A2` · `A3` · `A5` · `A6` · **`A7`** · `A8` · `A9` ·
`A10` · `A11` · `A12` · `A13` · `A14` · `G6` · `G7` · `G8` · `G9` · `G10`

**`A7` is the one to raise first.** It is the finding that the template cannot
serve as a governed standard without versioned distribution — and it is now
*implemented* (VERSION, CHANGELOG, `repo-standard.yaml` stamp, `/new-project`
stamping, drift detection). It should be dispositioned as closed rather than
carried forward as an open risk.

`G7` and `G10` block the level model from being fully settled even after W1.
