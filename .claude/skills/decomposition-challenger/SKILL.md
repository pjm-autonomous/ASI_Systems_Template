---
name: decomposition-challenger
description: Adversarially audit a requirement decomposition for architectural soundness — allocation substance, derived-requirement rationale, decomposition balance, tier discipline, and function coverage. Use when a chain looks complete on paper and you want to know whether it carries engineering substance. Reviews only; creates and edits nothing.
---

# Skill: decomposition-challenger

Adversarially review a decomposition and report findings.

Requirement hierarchies can be mathematically complete and architecturally
hollow — every row traced, and the allocation boundaries bearing no relation to
how the systems actually interact. This skill asks whether the decomposition
makes engineering sense, not administrative sense.

**Read-only.** It produces findings and changes nothing. Do not create, edit or
move artifacts, and do not write `traceability/TRACEABILITY.md` — it is generated
(D-46).

## Why this exists

A survey found **250 artifacts sitting at a level that does not own them**,
across two repos governed by this standard. Three shapes:

- A repo declaring one level holding **208** requirements of a tier a *lower*
  level owns, and **20** of a tier a *higher* level owns.
- The artifacts that repo does own, filed under a directory named for a different
  tier.
- A repo designated for one level holding **22** artifacts, **every one** of them
  content from a level two steps above it, with all three of its own tiers empty.

Every one passed validation, because a validator checks that a reference
**resolves** — not that the thing it resolves to **belongs where it is**. Check 4
exists for that gap.

## Levels and tiers are not the same thing

Read this before starting. Using level vocabulary where a tier is meant produces
wrong findings.

| | What it is | Declared in |
|---|---|---|
| **Level** | A property of a **repo**. One repo occupies exactly one level; a level may hold many repos (D-01). | `repo-standard.yaml` `level:`, and nowhere else |
| **Tier** | Internal structure — the directory an artifact type lives in. | `standard/artifact-schema.yaml` |

The decomposition chain is made of **tiers**:

```text
persona → use-case → product-requirement → capability-requirement
        → system-requirement → subsystem-requirement → component-requirement
```

Which level owns which tier is in `standard/tier-schema.md` §4. Two joins in that
chain **cross a repo boundary** — product→capability (L0→L1) and
capability→system (L1→L2). Those parents are external and are resolved by
`tools/broker.py` (D-53), not by reading a local file.

Never describe a finding in level vocabulary when you mean a tier, and never
suggest naming a directory after a level (D-14).

## Review flow

1. Read `repo-standard.yaml` for this repo's `level` and declared `tiers`.
2. Read `standard/tier-schema.md` §4 for which level owns which tier.
3. Read `standard/artifact-schema.yaml` for the `parent-*` chain. Do not work
   from a remembered chain — it is data, and it changes.
4. Run every check below unless the user scopes you to specific ones.
5. Emit the report in **Report format**.

## Findings

**Every table under a check below is output.** Each row is one finding you
report; the columns are the fields that finding must carry. Emit the table even
when it has no rows — an empty table states that the check ran and found
nothing, which a missing section does not.

Two columns are common to every check and are never omitted:

| Column | Rule |
|---|---|
| **File** | Repo-relative path of the artifact the finding is about. A finding with no file is an opinion, not a finding. |
| **Line** | Line number of the specific statement at fault. Use `—` **only** when the finding is genuinely about the artifact as a whole — a whole-file placement error has no line. Never guess a number. |

## Check 1 — Allocation substance

**Does the child add engineering substance, or restate the parent in new words?**

Look for:

- A child mirroring its parent's structure and language without adding
  specificity about the entity it is allocated to.
- Hollow qualifiers — "shall ensure", "shall maintain", "shall support" — that
  defer the actual constraint to a lower tier.
- "And-ing" decompositions: one parent split into several children with identical
  wording except for the `allocation` value.
- Missing rationale: why *this* parent to *this* child and not another.
- A child written at its parent's level of abstraction.

| File | Line | Child | Parent | What the child adds | Gap | Verdict |
|---|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `SOUND` | Adds constraints, behaviour or performance specific to what it is allocated to. |
| `THIN` | Adds some detail, but no testable criterion and no architectural rationale. |
| `RESTATED` | The parent with a name substituted. No new engineering substance. |
| `MISSING` | A child should exist for this parent and does not. |

## Check 2 — Derived-requirement audit

**Does every derived requirement have a defensible reason to exist?**

A derived requirement's content does not come from its parent — it comes from an
analysis, a standard, a supplier constraint, or an engineering judgement. Look
for:

- Derived requirements with no recorded basis. If the basis is a bound, it
  belongs in a `param-*` artifact (D-26), not in prose.
- Requirements asserting a value whose authority lives elsewhere — a governing
  safety document, a standard, an ICD.
- Requirements that are really design decisions. Those belong in an ADR.

| File | Line | Requirement | Origin | Basis | Verdict |
|---|---|---|---|---|---|

Origin is one of `analysis`, `standard`, `supplier`, `judgement`, `UNSTATED`.

| Verdict | Means |
|---|---|
| `JUSTIFIED` | Origin is stated and the basis is recorded where a reviewer can read it. |
| `UNSOURCED` | The requirement is plausible but nothing records where its content came from. |
| `MISPLACED` | The content is real but belongs in another artifact — a `param-*`, an ADR, or an ICD. Name which. |

## Check 3 — Decomposition balance

**Is the decomposition lopsided in a way that signals missing analysis?**

Look for:

- One parent with twenty children while its siblings have one each.
- A tier that is one-to-one throughout — a pass-through adding nothing.
- Entities named in the architecture with no requirements allocated to them.
- Whole feature buckets with no decomposition below one tier.

Report counts. A ratio is evidence; an impression is not.

| File | Line | Parent | Children | Peer median | Signal | Verdict |
|---|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `BALANCED` | Child count is in line with its peers. |
| `OVERLOADED` | Far more children than peers — usually one parent doing the work of several, or a decomposition that never split. |
| `PASS_THROUGH` | One-to-one with its parent and adding no constraint. The tier is being traversed, not used. |
| `STARVED` | Far fewer children than peers, or none where the architecture implies some. Suggests analysis not yet done. |

## Check 4 — Tier discipline

**Does each artifact live at the tier that owns it, and does the chain skip a tier?**

This is the check that earned the skill its place. Look for:

- An artifact in a repo whose declared `level` does not own that tier
  (`tier-schema.md` §4).
- An artifact under a directory that does not match its tier — capability
  requirements filed under `product/requirements/`, for instance.
- A requirement carrying detail belonging to a lower tier: a component's watchdog
  period stated in a system requirement.
- A requirement written so abstractly that no child could refine it.
- A **skipped tier** — a parent reference jumping from capability straight to
  sub-system. The `parent-*` chain makes this visible; the skipped tier is the
  one missing between them.
- A parent reference crossing a repo boundary at a join that should be local, or
  the reverse. The external joins are product→capability and capability→system,
  and only those.

| File | Line | Artifact | Sits in tier | Repo level | Level owns it | Written at | Correct tier | Verdict |
|---|---|---|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `CORRECT` | Tier matches the content's abstraction, and this repo's level owns that tier. |
| `WRONG_TIER` | Right repo, wrong directory. A move within the repo. |
| `WRONG_REPO` | The tier belongs to a different level. The artifact must move repos — a migration, not an edit. **Say so explicitly**; the cost is not comparable. |
| `SKIPPED` | The chain jumps a tier. Name the tier that is missing. |
| `UNDECOMPOSED` | No children at the next tier, and there should be. |

## Check 5 — Function coverage

**Is every behaviour the use cases describe required somewhere?**

Look for:

- Use-case steps describing system behaviour that trace to no requirement.
- Implicit functions nobody required: fallback to manual, graceful shutdown,
  comms watchdog, rate limiting, startup ordering.
- Cross-entity coordination that no requirement owns — if two entities must stay
  in sync and nothing says so, the agreement exists only in someone's head.
- Behaviour at a boundary with no interface artifact. A boundary is owned by the
  nearest common ancestor of the parties (D-04); if no interface exists, name the
  owner who should hold it.

| File | Line | Function | Source use case | Requirement trace | Covered by | Verdict |
|---|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `COVERED` | Explicit requirement exists and is allocated. |
| `IMPLICIT` | Addressed in design or code but never required. Upgrade to an explicit requirement. |
| `MISSING` | No requirement anywhere. Name the tier where one should be authored. |
| `RISKY_IMPLICIT` | Implicit **and** safety- or operation-critical. Reserved for that case — do not use it for convenience features, or it stops meaning anything. |

## Report format

```markdown
# Decomposition Challenge Report

| Field | Value |
|---|---|
| Scope | <what was examined> |
| Repo | <name> |
| Level | <from repo-standard.yaml> |
| Date | <YYYY-MM-DD> |

## Summary

<Three sentences. Most consequential finding first.>

| Check | Findings | Most severe |
|---|---:|---|
| 1 Allocation substance | n | <verdict> |
| 2 Derived requirements | n | <verdict> |
| 3 Balance | n | <verdict> |
| 4 Tier discipline | n | <verdict> |
| 5 Function coverage | n | <verdict> |

## Check 1 — Allocation substance

<the findings table, empty if nothing found>

... one section per check ...

## Recommended order

<What to fix first and why. Flag any WRONG_REPO finding here: it is a migration
that blocks work in two repos, not a file edit.>
```

## Rules

- **Cite the artifact.** File always; line wherever a specific statement is at fault.
- **Count.** "Several requirements are thin" is not a finding. "9 of 22 are `RESTATED`" is.
- **Do not propose wording.** This skill finds problems. `/requirement` and the authoring skills fix them.
- **A cross-repo parent is not a gap.** It is unverifiable from here, which is a different statement. Write "unverifiable locally" and leave it to `tools/broker.py`.
- **Separate a defect from a decision.** If the decomposition is sound but disagrees with `standard/decisions.md`, that is a decision to revisit, not a defect to fix. Name the decision.
- **Do not invent a tier or a verdict.** Tiers come from `standard/artifact-schema.yaml`; verdicts are the tables above.
