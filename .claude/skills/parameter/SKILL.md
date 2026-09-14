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

## Keep `Cited By` accurate — it is checked

The `## Cited By` section lists the artifacts that cite this parameter.
`tools/params.py` checks it against the citations it finds in the repo and fails
on drift in **either** direction: a requirement that cites the parameter but is
absent from the list, and a list entry that cites nothing.

Unlike `TRACEABILITY.md`, this list is **hand-maintained on purpose** (D-58) —
once something reads it, drift is caught on the next run.

So when adding a citation, do both halves:

1. Cite the parameter **by filename** in the requirement body —
   `` `param-<name>.md` ``, in a backtick, a link or plain prose; the check
   accepts any form.
2. Add that requirement's filename under this parameter's `## Cited By`.

**Never write the value into the requirement's prose.** A number copied into a
requirement is the duplicate this artifact type exists to remove: when the value
is re-derived for a site, the copy is what gets missed.

**A placeholder value fails once anything cites it.** `TBD`, `TBR`, `?` and `n/a`
are rejected for a cited parameter — a citation that resolves to a placeholder is
no better than one that dangles. Declaring a placeholder *before* any requirement
cites it is fine and reported only as a note; that is the right order to work in.

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
