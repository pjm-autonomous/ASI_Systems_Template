---
name: architecture-decision-challenger
description: Adversarially audit architectural decisions — whether they are recorded at all, whether their context still holds, and whether the structure they produced carries hidden coupling, single points of failure or scaling limits. Use when the architecture exists but the reasoning behind it does not. Reviews only; creates and edits nothing.
---

# Skill: architecture-decision-challenger

Adversarially review the decisions behind an architecture and report findings.

A diagram records **what** was decided. It rarely records **why**, what else was
considered, or what was true at the time that may not be true now. Those are the
things that make a decision revisable — and without them a structure gets
inherited rather than chosen, until nobody left can say why it is that shape.

**Read-only.** It produces findings and changes nothing. Do not create, edit or
move artifacts, and do not write `traceability/TRACEABILITY.md` — it is generated
(D-46).

## Why this exists

A survey found **30 architecture diagrams and 0 ADRs**, with no `decisions/`
directory anywhere in either repo examined, alongside 208 system requirements.

Thirty diagrams are thirty sets of structural choices — what is one entity and
what is two, which side of a boundary a responsibility sits on, what talks to
what. Every one of those was decided. Not one was recorded with its alternatives
and its reasoning, so not one can be revisited by anybody who was not in the
room.

Check 1 is the instrument for that: it finds decisions that are **drawn** and
never **written**.

## Where decisions live

| | Location | Notes |
|---|---|---|
| ADR | `<tier>/decisions/adr-*.md` | Required: `id`, `title`, `status`, `date`. `status` is `proposed`, `accepted`, `superseded` or `obsolete`. |
| Architecture | `architecture/arch-*.md` | Mermaid diagram plus purpose and scope |
| Interfaces | `interfaces/int-*.md` | The boundaries the architecture draws |

An ADR is filed at the tier whose structure it decides. A decision that shapes
two tiers belongs at the higher one — the same nearest-common-ancestor logic that
governs interfaces (D-04).

A decision recorded in `standard/decisions.md` is a **standard** decision,
governing this repo's conventions. It is not an ADR and is not in scope here,
except to check that an ADR does not contradict one.

## Review flow

1. Read `repo-standard.yaml` for this repo's `level` and declared tiers.
2. Read every `arch-*.md` and every `int-*.md`.
3. Read every `adr-*.md` — often none exist, which is itself the finding.
4. Read the requirements that constrain the structure.
5. Run every check below unless scoped to specific ones.
6. Emit the report in **Report format**.

## Findings

**Every table under a check below is output.** Each row is one finding; the
columns are the fields it must carry. Emit the table even when empty — that
states the check ran and found nothing, which a missing section does not.

| Column | Rule |
|---|---|
| **File** | Repo-relative path. A finding with no file is an opinion. For an undocumented decision, cite the artifact where the decision is *visible* — usually the diagram. |
| **Line** | Line of the statement at fault. `—` only when the finding is about the artifact as a whole, or spans several. Never guess. |

## Check 1 — Decision inventory

**Is every architectural decision recorded, with its alternatives and its reason?**

Work from the structure outward. For each diagram, ask what had to be decided to
draw it that way, then look for where that decision is written.

Look for:

- A block on a diagram that is one entity and could have been several, or the
  reverse, with no prose saying why.
- A responsibility placed on one side of a boundary with no stated reason.
- A protocol, transport or pattern chosen with no alternatives recorded.
- A decision stated in a requirement's rationale rather than an ADR — the content
  exists but is filed where nobody looking for decisions will find it.
- A decision recorded with its outcome but no rejected alternative. "We chose X"
  with no "instead of Y, because Z" is a record of an action, not a decision.

| File | Line | Decision | Recorded in | Alternatives | Rationale | Verdict |
|---|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `RECORDED` | Decision, alternatives and rationale all written where a reader would look. |
| `PARTIAL` | The decision is written; alternatives or rationale are not. Revisable only by guesswork. |
| `MISFILED` | Fully reasoned, but recorded somewhere nobody searching for decisions will find — a requirement rationale, an ICD note, a commit message. |
| `UNDOCUMENTED` | Visible in the structure, written nowhere. |

## Check 2 — Decision staleness

**Does the context each decision was made in still hold?**

A decision is only as good as what was true when it was made. Look for:

- An ADR whose stated context names a constraint that has since changed — a
  supplier, a platform, a performance target, a team boundary.
- An `accepted` ADR contradicted by a later requirement or interface, with no
  `superseded` marker.
- A decision made for a scope smaller or larger than the current one.
- A decision depending on another that has since been superseded, with no
  reconsideration.
- An ADR with no `date`, which makes staleness unassessable rather than absent.

| File | Line | Decision | Context stated | What changed | Verdict |
|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `CURRENT` | The stated context still holds. |
| `STALE` | A named element of the context has changed; the decision may still be right but has not been rechecked. |
| `CONTRADICTED` | A later artifact assumes the opposite and the ADR is still `accepted`. One of the two is wrong. |
| `UNASSESSABLE` | No context or no date recorded, so staleness cannot be judged either way. |

## Check 3 — Coupling

**What depends on what, and is any of it accidental?**

Look for:

- Two entities that must change together but whose dependency no interface
  records — coupling that exists only in practice.
- A shared data structure, parameter or state owned by neither party.
- A dependency cycle between entities.
- An entity reaching past its immediate neighbour to something deeper, which
  breaks the boundary the owner is supposed to arbitrate (D-04).
- Temporal coupling: one entity relying on another's ordering or timing with no
  stated contract.

| File | Line | Entities | Dependency | Recorded in | Verdict |
|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `DECLARED` | The dependency exists and an interface records it. |
| `IMPLICIT` | Real and recorded nowhere. Nothing prevents either side breaking it. |
| `CYCLIC` | Mutual dependency. Name both directions and what breaks first. |
| `BOUNDARY_BREAK` | Reaches past an immediate neighbour into something deeper. |

## Check 4 — Single points of failure

**What fails alone and takes the rest with it?**

Look for:

- An entity every path passes through, with no stated redundancy or degraded mode.
- A single source for a value many consumers depend on.
- A shared resource — bus, clock, power domain, store — whose loss is not
  addressed by any requirement.
- A fallback that depends on the thing it is a fallback for.
- An entity whose failure mode is stated nowhere, which is different from an
  entity that cannot fail.

| File | Line | Entity | What depends on it | Redundancy or degraded mode | Verdict |
|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `MITIGATED` | Redundancy or a degraded mode is specified and required somewhere. |
| `ACCEPTED` | Single point, acknowledged in an ADR with reasoning. A decision, not a defect. |
| `UNMITIGATED` | Single point, not acknowledged anywhere. |
| `CIRCULAR_FALLBACK` | The mitigation depends on the thing it mitigates. |

## Check 5 — Scaling and change stress

**What does this structure cost when the obvious changes arrive?**

Pick changes the roadmap or the use cases make likely — another vehicle type,
another site, another consumer of an interface, ten times the message rate — and
trace what each would touch.

Look for:

- A change that touches every entity. That is a structure organised around
  something other than what varies.
- A limit designed to one value with no stated headroom.
- An enumeration or fixed set that a new variant would force open.
- A boundary that would have to move for a plausible change — the expensive kind.

| File | Line | Change | Entities touched | Cost signal | Verdict |
|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `ABSORBS` | The change is local to one entity or one interface. |
| `SPREADS` | Touches several entities that have no reason to be coupled to it. |
| `BLOCKED` | Cannot be made without moving a boundary or reopening a fixed set. |
| `UNTESTED` | The change is plausible and nothing in the architecture shows it was considered. |

## Coherence probes

Run these across everything read, not per artifact. They produce findings in the
same shape as the checks above; report them under **Probes**.

| Probe | Question |
|---|---|
| **Contradiction** | Do two artifacts assert incompatible things about the same structure? Quote both. |
| **Engineering judgement** | Where does a document assert a value or a choice with no source? Distinguish a judgement recorded as such — legitimate — from one presented as fact. |
| **Context assumption** | What is assumed true and stated nowhere? Environment, load, ordering, who operates it. |

## Report format

```markdown
# Architecture Decision Challenge Report

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
| 1 Decision inventory | n | <verdict> |
| 2 Staleness | n | <verdict> |
| 3 Coupling | n | <verdict> |
| 4 Single points of failure | n | <verdict> |
| 5 Scaling and change | n | <verdict> |
| Probes | n | — |

## Check 1 — Decision inventory

<findings table, empty if nothing found>

... one section per check, then Probes ...

## Rework priority

<Ordered. An UNDOCUMENTED decision on a structure still being built is more
urgent than one on a structure that is finished, because the cost of discovering
it was wrong is still falling.>
```

## Quick mode

When asked for a fast pass, run Check 1 only, over the diagrams alone, and report
the count of `UNDOCUMENTED` against the total number of decisions identified. That
single ratio is usually enough to decide whether a full pass is worth booking.

## Rules

- **Cite the artifact.** For an undocumented decision, cite where the decision is
  *visible* — the diagram — and say so, rather than leaving File blank because no
  ADR exists.
- **Count.** "Many decisions are undocumented" is not a finding. "26 of 31
  identified decisions are `UNDOCUMENTED`" is.
- **An absent ADR is not automatically a defect.** Not every choice needs one.
  Reserve `UNDOCUMENTED` for decisions that would be expensive to reverse, or
  that a newcomer would otherwise have to reverse-engineer.
- **Do not write the ADR.** This skill finds the gap; `/adr` fills it.
- **A standard decision is not an ADR.** `standard/decisions.md` governs
  conventions. Check only that an ADR does not contradict one; if it does, name
  the decision.
- **Distinguish a decision from a defect.** A single point of failure that an ADR
  acknowledges with reasoning is `ACCEPTED`, not `UNMITIGATED`. Say which.
