---
name: interface-integrity-auditor
description: Adversarially audit interfaces as a set rather than one at a time — timing budgets, signal completeness, failure propagation, assumption mismatches, integration sequencing, and ownership. Use before integration, or when individually correct ICDs still do not add up. Reviews only; creates and edits nothing.
---

# Skill: interface-integrity-auditor

Adversarially review the repo's interfaces **as a system** and report findings.

Individually correct ICDs routinely fail to integrate. One side sends at 50 Hz
and the other expects 100 Hz, and both teams are right according to their own
document. A safety-critical path's latencies sum past the response time the
function allows, and nobody added them up, because no single ICD owns the sum.

This skill does not check whether one interface is internally correct — the
validator and `/icd` do that. It asks whether the interfaces, taken together,
describe something that can actually integrate.

**Read-only.** It produces findings and changes nothing. Do not create, edit or
move artifacts, and do not write `traceability/TRACEABILITY.md` — it is generated
(D-46).

## Why this exists

A survey of one repo's interfaces found **228 unresolved fields across 10
interface artifacts**. Every one of the ten carried at least three; one carried
124. Not a single interface in the repo was fully specified.

Unresolved fields are invisible to a validator, which checks that required
frontmatter is present — not that the contract underneath it says anything. An
interface whose transport, encoding and failure semantics all read `TBD` passes
every check in this repo and binds nobody to anything.

## Interface ownership — read this before starting

An interface is owned by the **nearest common ancestor** of the parties it
connects, and is expressed in terms of **that owner's immediate descendants**
(D-04). Two peers cannot arbitrate a boundary they both sit on.

Consequences you are auditing against:

- `producer` and `consumer` name the owner's immediate descendants — never the
  components inside them. An L1 interface says *System A* and *System B*, not the
  sub-systems within either.
- A repo has **one** `interfaces/` directory, describing the boundaries between
  the entities one level below it. Interfaces scattered across several tiers mean
  the ownership rule is not being applied.
- Ownership is arbitration authority and baseline control — not authorship.
  Whoever writes it, the owner arbitrates it.

## Review flow

1. Read `repo-standard.yaml` for this repo's `level`.
2. Read every `int-*.md` under `interfaces/`.
3. Read the requirements that describe behaviour at those boundaries — the
   timing, rate and failure-handling claims live there, not only in the ICD.
4. Run every check below unless scoped to specific ones.
5. Emit the report in **Report format**.

## Findings

**Every table under a check below is output.** Each row is one finding; the
columns are the fields it must carry. Emit the table even when empty — that
states the check ran and found nothing, which a missing section does not.

| Column | Rule |
|---|---|
| **File** | Repo-relative path. A finding with no file is an opinion. |
| **Line** | Line of the statement at fault. `—` only when the finding is about the artifact as a whole, or spans several files (an end-to-end path has no single line). Never guess. |

## Check 1 — Timing budget

**Do the latencies along a path sum to less than the time the function allows?**

For each time-bounded function, trace the end-to-end path: input event →
transmission across each interface → processing at each entity → output action.
Sum the contributions and compare against the requirement's bound.

Look for:

- A path whose sum exceeds its bound, or has no bound to compare against.
- Interfaces on a timed path that state no latency at all. Unstated is not zero.
- A bound stated as a number in prose instead of citing a `param-*` (D-26).
- Jitter ignored — a 50 ms mean with ±40 ms jitter is not a 50 ms path.
- Retries or buffering that silently add a transmission time.

| File | Line | Function | Path | Budget | Sum of stated | Unstated hops | Verdict |
|---|---|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `WITHIN` | Stated contributions sum below the bound, with every hop stated. |
| `EXCEEDS` | The sum is over the bound. A defect now, not at integration. |
| `UNBOUNDED` | The path has no stated bound to check against. |
| `INCOMPLETE` | One or more hops state no latency, so no sum is possible. Name the hops. |

## Check 2 — Signal completeness

**Does every signal have both a producer and a consumer?**

Build a signal map across all interfaces. For each signal, confirm one interface
defines it as an output and one defines it as an input.

Look for:

- **Dead ends** — produced, consumed by nothing.
- **Phantoms** — a requirement expects a signal no interface produces.
- **Orphans** — a safety- or operation-critical signal consumed only by something
  outside the baseline.
- Signals crossing a boundary with no interface artifact at all.

| File | Line | Signal | Produced by | Consumed by | Verdict |
|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `COMPLETE` | Producer and consumer both defined, in interfaces owned by the right level. |
| `DEAD_END` | Produced, consumed nowhere. Either remove it or name the consumer. |
| `PHANTOM` | Expected by a requirement, produced nowhere. |
| `ORPHANED` | Critical, and its only consumer is outside the baseline architecture. |

## Check 3 — Failure propagation

**When one side fails, does the other side's stated behaviour match?**

Look for:

- An interface with no link-loss or staleness semantics. Every interface has a
  failure mode; an interface that does not state one has an undocumented one.
- Producer and consumer disagreeing on what a timeout means — hold last value,
  reject, or fall back.
- A failure that is detected but not propagated: something notices and nothing
  downstream is told.
- Fallback behaviour that is unsafe in the state the system will actually be in.
- Malformed, out-of-range or late data with no stated handling.

| File | Line | Interface | Failure mode | Producer behaviour | Consumer behaviour | Verdict |
|---|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `CONSISTENT` | Both sides state the same behaviour for this failure. |
| `MISMATCHED` | Both state behaviour and the two disagree. The most dangerous result here — both sides believe they are handling it. |
| `UNDEFINED` | One or both sides state nothing. The behaviour exists and is undocumented. |
| `UNSAFE` | Stated behaviour is defined and wrong for the state it applies in. |

## Check 4 — Assumption mismatch

**Do the two sides of a boundary assume the same values?**

Cross-reference both sides — the ICD and the requirements allocated either side
of it — for:

- **Rate / update frequency** — one says 50 Hz, the other 100 Hz.
- **Format, encoding, payload size.**
- **Timing tolerance and jitter.**
- **Valid range** — and what happens in the gap between two ranges.
- **Units and resolution** — radians against degrees; 0.01 m against 0.1 m.
- **Fault-handling semantics** — ignore against report.
- **State assumptions** — accepting a command in a state the sender may not be in.
- **Buffering** — one side buffers, the other assumes synchronous handling.

| File | Line | Boundary | Attribute | Producer states | Consumer states | Verdict |
|---|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `ALIGNED` | Both sides state the same value. |
| `MISMATCH` | Both state a value and they differ. Quote both. |
| `ASSUMPTION_GAP` | One side states a value, the other assumes silently. |
| `UNSTATED` | Neither side states it, and the attribute matters for this interface. |

## Check 5 — Integration sequence

**Is there a defined order, and is every function covered during the transients?**

Review startup, shutdown and mode transitions.

Look for:

- No defined order for bringing entities online.
- A transient state where a protective function is not yet covered — one entity
  running before the thing it depends on is ready.
- Readiness assumed with no handshake or health signal to confirm it.
- No timeout or fallback when an entity fails to reach its expected state.
- Shutdown that does not address operations in flight.
- A dependency on something no interface documents — time sync is the usual one.

| File | Line | Sequence | Transient state | What is uncovered | Verdict |
|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `DEFINED` | Order, handshakes, timeouts and fallbacks are all stated. |
| `GAP` | A transient state exists in which a function is not covered. |
| `ASSUMED` | The sequence depends on readiness that nothing confirms. |
| `UNDOCUMENTED` | No sequence is stated at all. |

## Check 6 — Ownership and expression

**Is each interface owned by the right level, and expressed at the right depth?**

Look for:

- An interface naming entities **deeper** than the owner's immediate descendants
  — publishing internals across a boundary the owner cannot bind (D-04).
- An interface between two entities whose nearest common ancestor is a different
  level from the repo holding it.
- Interfaces spread across several tier directories rather than one
  `interfaces/`.
- Two peers arbitrating a boundary they both sit on, with no owner named.

| File | Line | Interface | Producer | Consumer | Nearest common ancestor | Verdict |
|---|---|---|---|---|---|---|

| Verdict | Means |
|---|---|
| `CORRECT` | Owned by the nearest common ancestor and expressed in its immediate descendants. |
| `TOO_DEEP` | Names entities below the owner's immediate descendants. |
| `WRONG_OWNER` | The nearest common ancestor is a different level. Moving it is a migration, not an edit — say so. |
| `UNOWNED` | No level arbitrates it; the two parties are settling it between themselves. |

## Report format

```markdown
# Interface Integrity Audit

| Field | Value |
|---|---|
| Scope | <interfaces examined> |
| Repo | <name> |
| Level | <from repo-standard.yaml> |
| Date | <YYYY-MM-DD> |

## Summary

<Three sentences. Most consequential finding first.>

| Check | Findings | Most severe |
|---|---:|---|
| 1 Timing budget | n | <verdict> |
| 2 Signal completeness | n | <verdict> |
| 3 Failure propagation | n | <verdict> |
| 4 Assumption mismatch | n | <verdict> |
| 5 Integration sequence | n | <verdict> |
| 6 Ownership | n | <verdict> |

## Check 1 — Timing budget

<findings table, empty if nothing found>

... one section per check ...

## Recommended order

<What to fix first. Flag any WRONG_OWNER finding here — it is a migration that
blocks work in two repos.>
```

## Rules

- **Cite the artifact.** File always; line wherever a specific statement is at fault.
- **Count.** "Several interfaces are underspecified" is not a finding. "228 unresolved fields across 10 interfaces, all 10 affected" is.
- **Unstated is not zero.** An interface that states no latency, no failure mode or no rate has an undocumented one, not an absent one. Report it as unstated rather than assuming a default.
- **A `MISMATCH` beats an `UNSTATED`.** Two sides that disagree while both believing they are right is more dangerous than a gap nobody has filled, because nobody is looking for it.
- **Do not write the contract.** This skill finds problems; `/icd` fixes them.
- **A bound with no value belongs in a `param-*`** (D-26). Report the citation as missing rather than inventing a number.
- **Separate a defect from a decision.** If an interface is coherent but disagrees with `standard/decisions.md`, name the decision.
