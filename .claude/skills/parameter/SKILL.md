---
name: parameter
description: Create or update a program parameter in <tier>/parameters/. Use when a requirement cites a bound — a timeout, rate, distance, tolerance or threshold — that needs a declared value.
---

# Skill: parameter

Create or update a `param-*.md` artifact — a value a robot program declares,
cited by name from requirements rather than written into their prose.

## Why this exists

A requirement that defers to "the configured interval" with no parameter
declaring it is **unverifiable by construction**: no test can state a pass
criterion, because nothing says what passing is.

The survey behind this standard found **17 distinct configured bounds** named
across a requirement set with no value declared anywhere and no artifact type to
hold them. Every requirement citing one was unverifiable, and every test that
should have covered them could not be written.

## Which tier

Parameters are valid at `product`, `capability`, `system`, `subsystem` and
`component`.

**File it at the tier of the requirement that cites it.** Where several tiers
cite the same bound, file it at the **highest** one that does — the lower
requirements are inheriting a constraint, not declaring their own, and two files
declaring the same bound is the disagreement this type exists to prevent.

## Create flow

Ask the user for:

1. A short description → becomes the kebab-case filename after `param-`
2. The **value** and its **unit**
3. Who declares it, and what it applies to
4. Which requirement(s) cite it
5. The **basis** — where the value came from

Then create `<tier>/parameters/param-<description>.md` from
`templates/parameter.md`.

Two sections carry the weight:

- **Definition** — precise enough that two engineers would measure it the same
  way. **Name the measurement point.** "Latency under 100 ms" is not a
  specification until it says latency between what and what; a threshold measured
  at a different point can trigger at a different time under load.
- **Basis** — an analysis, a standard, a supplier datasheet, a test result, or an
  engineering judgement recorded as such. **A value with no basis is a
  placeholder and must say so.** This is what lets a reviewer tell a measured
  value from a guess that has sat there long enough to look settled.

If the value is site-specific or deployment-specific, say so explicitly and say
it must be re-derived rather than inherited.

**Do not touch `traceability/TRACEABILITY.md`** — generated (D-46).

Finish by running `validate-artifacts`.

## Update flow

Changing a parameter's value changes every requirement that cites it.

1. Read the file
2. **List the requirements that cite it** before changing anything, and tell the
   user which ones are affected
3. Apply the change, and update the Basis to say why the value moved
4. Re-run `validate-artifacts`

## Conventions

- Filename: `param-<description>.md`, kebab-case
- Plain Markdown tables, never HTML
- Requirements cite the parameter **by name**. A number written into a
  requirement body as well as here is a number that will disagree with itself
