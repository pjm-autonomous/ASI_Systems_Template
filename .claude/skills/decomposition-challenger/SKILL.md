---
name: decomposition-challenger
description: Adversarially audit a requirement decomposition for architectural soundness — allocation substance, derived-requirement rationale, decomposition balance, tier discipline, and function coverage. Use when a chain looks complete on paper and you want to know whether it carries engineering substance. Reviews only; creates and edits nothing.
---

# Skill: decomposition-challenger

Adversarial review of a decomposition. You are a systems architect who has seen
hierarchies that were mathematically complete and architecturally hollow — every
row traced, and the allocation boundaries had nothing to do with how the systems
actually interacted. Your job is to ask whether the decomposition makes
engineering sense, not administrative sense.

**Read-only.** Produce findings. Do not create, edit or move artifacts, and do
not write `traceability/TRACEABILITY.md` — it is generated (D-46).

## Why this skill exists

A survey on 2026-09-14 found **250 artifacts sitting at a level that does not
own them**, across two repos governed by this standard. The three shapes it took:

- A repo declaring one level, holding **208** requirements of a tier a *lower*
  level owns — and **20** of a tier a *higher* level owns.
- The artifacts that repo does own, filed under a directory named for the wrong
  tier.
- A repo designated for one level holding **22** artifacts, **every one** of them
  content from a level two steps above it, with all three of its own tiers empty.

Every one of those artifacts passed validation, because a validator checks that a
reference **resolves** — not that the thing it resolves to **belongs where it
is**. That gap is what Challenge 4 exists for, and it is why this was the first
adversarial skill harvested.

The instances are recorded in `standard/phase-3-harvest.md`; they are not
restated here, so this skill stays usable in a repo that has never heard of
them.

## Levels and tiers are not the same thing — read this before starting

This skill was ported from a repo that used `L0 → L1 → L2` to mean *abstraction
levels of requirements*. **That is not this standard's model**, and using that
vocabulary here produces wrong findings.

| | What it is | Where it is declared |
|---|---|---|
| **Level** | A property of a **repo**. One repo occupies exactly one level; a level may hold many repos (D-01). | `repo-standard.yaml` `level:`, and nowhere else |
| **Tier** | Internal structure — the directory a type lives in. | `standard/artifact-schema.yaml` |

The decomposition chain is made of **tiers**:

```text
persona → use-case → product-requirement → capability-requirement
        → system-requirement → subsystem-requirement → component-requirement
```

Which level owns which tier is in `standard/tier-schema.md` §4. Two joins in that
chain **cross a repo boundary** — product→capability (L0→L1) and
capability→system (L1→L2) — and those parents are external, resolved by
`tools/broker.py` (D-53).

**Never describe a finding in level vocabulary when you mean a tier**, and never
suggest naming a directory after a level (D-14).

## The five challenges

Run all five unless the user scopes you to specific ones. Each produces
structured findings; the report format is at the end.

### Challenge 1 — Allocation substance

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

```text
ALLOCATION: <parent id and statement> → <child id and statement>
SUBSTANCE:  what the child adds, or that it adds nothing
GAP:        the constraints or rationale missing
VERDICT:    SOUND | THIN | RESTATED | MISSING
```

- **SOUND** — adds constraints, behaviour or performance specific to what it is allocated to.
- **THIN** — adds some detail, but no testable criterion or architectural rationale.
- **RESTATED** — the parent with a name substituted.
- **MISSING** — a child should exist and does not.

### Challenge 2 — Derived-requirement audit

**Does every derived requirement have a defensible reason to exist?**

A derived requirement is one whose content does not come from its parent — it
comes from an analysis, a standard, a supplier constraint or an engineering
judgement. Look for:

- Derived requirements with no recorded basis. If the basis is a bound, it
  belongs in a `param-*` artifact (D-26), not in prose.
- Requirements asserting a value whose authority lives elsewhere — a governing
  safety document, a standard, an ICD.
- Requirements that are really design decisions. Those belong in an ADR.

```text
REQUIREMENT: <id and statement>
ORIGIN:      derived-from-analysis | standard | supplier | judgement | UNSTATED
BASIS:       the evidence, or that none is recorded
VERDICT:     JUSTIFIED | UNSOURCED | MISPLACED
```

### Challenge 3 — Decomposition balance

**Is the decomposition lopsided in a way that signals missing analysis?**

Look for:

- One parent with twenty children while its siblings have one each.
- A tier that is one-to-one throughout — a pass-through tier adding nothing.
- Entities in the architecture with no requirements allocated to them.
- Whole feature buckets with no decomposition below one tier.

Report counts. A ratio is evidence; an impression is not.

```text
PARENT:   <id>   CHILDREN: <n>
PEERS:    <median children across siblings>
SIGNAL:   what the imbalance suggests
VERDICT:  BALANCED | OVERLOADED | PASS_THROUGH | STARVED
```

### Challenge 4 — Tier discipline

**Does each artifact live at the tier that owns it, and does the chain skip a tier?**

This is the challenge that earned the skill its place. Check:

- An artifact in a repo whose declared `level:` does not own that tier
  (`tier-schema.md` §4). This is the 250-artifact failure above.
- An artifact under a directory that does not match its tier — 15 capability
  requirements under `product/requirements/` is the live example.
- A requirement carrying detail belonging to a lower tier: a component's watchdog
  period stated in a system requirement.
- A requirement written so abstractly that no child could refine it.
- A **skipped tier** — a parent reference jumping from capability straight to
  sub-system. The schema's `parent-*` chain makes this visible; the skipped tier
  is the one missing between them.
- A parent reference crossing a repo boundary at a join that should be local, or
  vice versa. The external joins are product→capability and capability→system,
  and only those.

```text
ARTIFACT:      <id>
DECLARED_TIER: <tier it sits in>
REPO_LEVEL:    <level from repo-standard.yaml>
OWNS_IT:       yes | no  (tier-schema.md §4)
ABSTRACTION:   what the content is actually written at
CORRECT_TIER:  <tier>
VERDICT:       CORRECT | WRONG_TIER | WRONG_REPO | SKIPPED | UNDECOMPOSED
```

- **WRONG_TIER** — right repo, wrong directory.
- **WRONG_REPO** — the tier belongs to a different level; the artifact must move
  repos, which makes it a migration, not an edit. Say so.
- **SKIPPED** — the chain jumps a tier; name the tier that is missing.
- **UNDECOMPOSED** — no children at the next tier, and there should be.

### Challenge 5 — Function coverage

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

```text
FUNCTION:   <name, and the use case it comes from>
SOURCE:     <use case id>
TRACE:      <requirement id, or NONE>
COVERAGE:   which requirements implement it
VERDICT:    COVERED | IMPLICIT | MISSING | RISKY_IMPLICIT
```

**RISKY_IMPLICIT** is reserved for behaviour that is safety- or
operation-critical and required nowhere. Do not use it for convenience features.

## Output format

```markdown
# Decomposition Challenge Report

**Scope:** <what was examined>
**Repo / level:** <name> / <level from repo-standard.yaml>
**Date:** <YYYY-MM-DD>

## Summary

<Three sentences. The single most consequential finding first.>

| Challenge | Findings | Most severe |
|---|---:|---|
| 1 Allocation substance | n | verdict |
| 2 Derived requirements | n | verdict |
| 3 Balance | n | verdict |
| 4 Tier discipline | n | verdict |
| 5 Function coverage | n | verdict |

## Challenge 1 — Allocation substance
<findings, in the block format above>

... one section per challenge ...

## Recommended order

<What to fix first, and why that order. A migration between repos is expensive
and blocks work in both; say when a finding is one.>
```

## Rules

- **Cite the artifact.** A finding without an id is an opinion.
- **Count.** "Several requirements are thin" is not a finding; "9 of 22 are
  RESTATED" is.
- **Do not propose wording.** This skill finds problems. `/requirement` and the
  authoring skills fix them.
- **A cross-repo parent is not a gap.** It is unverifiable from here, which is a
  different statement. `tools/broker.py` resolves it; say "unverifiable locally".
- **Separate a defect from a decision.** If the decomposition is sound but
  disagrees with a decision in `standard/decisions.md`, that is a decision to
  revisit, not a defect to fix. Name the decision.
- **Do not invent a tier.** The tiers are in `standard/artifact-schema.yaml`.
