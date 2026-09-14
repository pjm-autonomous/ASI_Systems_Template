---
artifact-type: param
tier: system
---

# Program Parameters

- [What belongs here](#what-belongs-here)
- [Why this type exists](#why-this-type-exists)
- [Every cited bound needs one](#every-cited-bound-needs-one)
- [Value and basis](#value-and-basis)
- [Which tier a parameter belongs to](#which-tier-a-parameter-belongs-to)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `system/parameters/param-<description>.md`. Start from
`templates/parameter.md`.

## What belongs here

A parameter is **a value a robot program declares**, cited by name from
requirements rather than written into their prose.

One parameter per file: a value, a unit, who declares it, and what it applies to.

## Why this type exists

Requirements routinely defer to a bound they do not state — *"within the
configured interval"*, *"below the configured threshold"*. Without somewhere for
that value to live, the requirement is **unverifiable by construction**: no
verification test can state a pass criterion, because nothing says what passing
is.

The survey that produced this standard found **17 distinct configured bounds**
named across a requirement set with no value declared anywhere and no artifact
type to hold them. Every requirement citing one of them was unverifiable, and
every test that should have covered them could not be written.

## Every cited bound needs one

If a requirement cites a timeout, a rate, a distance, a tolerance or a threshold,
that bound needs a `param-*.md` holding a real value.

Cite it by name. Do not write the number into the requirement prose — a number in
two places is a number that will disagree with itself, and the requirement is the
copy people read while the parameter is the copy people change.

## Value and basis

**A value without a basis is a placeholder, and should say so.**

Record where the value came from: an analysis, a standard, a supplier datasheet,
a test result, or an engineering judgement recorded as such. The basis is what
lets a reviewer tell a measured value from a guess that has been sitting there
long enough to look settled.

Define the bound precisely enough that two engineers would measure it the same
way, and name the measurement point. "Latency under 100 ms" is not yet a
specification until it says latency between what and what.

## Which tier a parameter belongs to

Parameters are valid at `product`, `capability`, `system`, `subsystem` and
`component`.

**File a parameter at the tier of the requirement that cites it.** A budget the
platform commits to belongs at `capability/parameters/`; a component's internal
timeout belongs at `component/parameters/`.

Where several tiers cite the same bound, it belongs at the highest one that does
— the lower requirements are inheriting a constraint, not declaring their own,
and two files declaring the same bound is the disagreement this type exists to
prevent.

## Maturity

Parameters start at `M1`. A state at or above `M2` requires a dated promotion
record in `_registry/` — see
[`standard/decisions.md`](../../standard/decisions.md) D-40 … D-43.

A parameter should not lag the requirements that cite it. If a requirement is
being promoted while the bound it depends on is still `M1`, the requirement is
being reviewed against a value nobody has checked.
