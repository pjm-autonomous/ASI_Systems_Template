---
artifact-type: product-requirement
tier: product
---

# Product Requirements

- [What belongs here](#what-belongs-here)
- [Performance and safety requirements share this type](#performance-and-safety-requirements-share-this-type)
- [What a product requirement traces to](#what-a-product-requirement-traces-to)
- [EARS format](#ears-format)
- [Cited bounds need a parameter](#cited-bounds-need-a-parameter)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `product/requirements/prodreq-<description>.md`, optionally grouped
into a feature-bucket directory. Start from `templates/product-requirement.md`.

## What belongs here

A product requirement is a **stakeholder-facing statement of what the system shall do to satisfy a use case** — EARS-formatted, prioritised, with acceptance
criteria.

It describes stakeholder-observable behaviour: *when X happens, the system shall Y*. It does not name a component, a service, or an algorithm. If it does, the
content belongs further down — allocation to a subsystem or component happens at
L2, in another repo, and naming one here binds a design decision that is not this
level's to make.

## Performance and safety requirements share this type

L0 owns **product performance requirements and safety requirements**, and both
use this one artifact type. The distinction is the `requirement-type` field, not
a separate type and **not** the priority field. 

Priority says *when you would build it*, `requirement-type` says
*what kind of obligation it is*. Conflating them means dropping a safety
requirement's priority quietly reclassifies it.

The schema's `requirement-type` enum carries four safety values — technical,
system, hardware and software safety — alongside functional, performance,
nonfunctional and environmental. The authoritative list is in
[`standard/artifact-schema.yaml`](../../standard/artifact-schema.yaml).

Cross-reference safety-bearing requirements from `extensions/safety/` once that
category is authored. `reference/standards-framework.md` lists the standards that
typically drive them on an autonomous-systems project.

## What a product requirement traces to

```text
use case                          stakeholder tier, SAME repo
   └─ product requirement         product tier      ← you are here
        └─ capability requirement L1, ANOTHER repo
```

- **Upstream:** `parent-use-cases`, resolved locally — both tiers are L0.
- **Downstream:** a capability requirement in the L1 repo names this one in its
  `parent-product-requirements`. That link is created by the child, not by you,
  and is verified upstream against this repo's published `artifact-index.json`.

Nothing at L2 names a product requirement directly. A system requirement's parent
is a capability requirement, one step further down.

## EARS format

- **When** `<trigger>`, the system shall `<response>`.
- **While** `<state>`, the system shall `<behavior>`.
- **If** `<condition>`, the system shall `<action>`.
- **Where** `<feature is included>`, the system shall `<capability>`.

`ISO/IEC/IEEE 29148` is the standard behind why this phrasing matters — EARS is
one way of satisfying its "unambiguous and singular" characteristics. See
`reference/standards-framework.md`.

## Cited bounds need a parameter

If a requirement cites a bound — a timeout, a rate, a distance, a tolerance —
that bound needs a `param-*.md` artifact holding a real value. A requirement that
defers to "the configured interval" with no parameter declaring it is
**unverifiable by construction**, and no test can state a pass criterion for it.

This is not hypothetical: the survey that produced this standard found 17 distinct
configured bounds named across a requirement set with no value declared anywhere
and no artifact type to hold them.

## Maturity

Product requirements start at `M1`. A state at or above `M2` requires a dated
promotion record in `_registry/` — see
[`standard/decisions.md`](../../standard/decisions.md) D-40 … D-43.

Short IDs are assigned at **M3**, and assignment triggers a review in which no
reply equals acceptance (D-43).
