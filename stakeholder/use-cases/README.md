---
artifact-type: use-case
tier: stakeholder
---

# Use Cases

- [What belongs here](#what-belongs-here)
- [What a use case traces to](#what-a-use-case-traces-to)
- [Creating a feature bucket](#creating-a-feature-bucket)
- [Sizing a use case](#sizing-a-use-case)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `stakeholder/use-cases/uc-<description>.md`, optionally grouped into
a feature-bucket directory. Start from `templates/use-case.md`, and read the
worked use case under `example/` before authoring your first.

## What belongs here

A use case is **a specific need a persona has of the system** — one coherent
interaction, with a main flow, preconditions, postconditions, and the exception
paths worth calling out.

Write it from the persona's point of view — *"As a fleet operator, I need…"* —
not as a statement of system behaviour. That phrasing belongs one tier down, in a
product requirement's EARS statement. A use case that reads like a requirement
has usually skipped the step of saying who wants it and why.

## What a use case traces to

```text
persona                         stakeholder tier
   └─ use case                  stakeholder tier   ← you are here
        └─ product requirement  product tier, SAME repo
             └─ capability requirement   L1, ANOTHER repo
```

Two things about this chain are easy to get wrong:

- **A use case's child is a product requirement, not a capability requirement.**
  A `prodreq-*.md` names this use case in its `parent-use-cases`. Both live at
  L0, so that link resolves locally.
- **The capability requirement is one step further down, and in another repo.**
  It derives from a *product requirement*, not from a use case. Nothing at L1
  names a use case directly.

Upstream, a use case names `parent-personas`, and everything below it reaches a
stakeholder need through that link.

## Creating a feature bucket

Feature buckets are optional directories inside the tier, and none exist until
the first use case is authored against a real persona need.

Name the bucket for the **capability**, not for the persona and not for an
implementation — `low-battery-return-to-dock`, not `fleet-operator-stuff` or
`power-management-service`. Reuse an existing bucket when a new use case extends
it; create one only when the use case fits nowhere.

Bucket names are matched by string against the requirements tool, and against the
parent repo's buckets where the same feature appears in both. A renamed bucket on
one side silently stops matching.

## Sizing a use case

If the main flow grows past six to eight steps, or it accumulates unrelated
exception flows, it is probably two use cases. **Split on what triggers it**
rather than keeping one file that covers every trigger for a capability.

## Maturity

Use cases start at `M1`. A state at or above `M2` requires a dated promotion
record in `_registry/` — see [`standard/decisions.md`](../../standard/decisions.md)
D-40 … D-43.

Like personas, use cases are worth stabilising early: every requirement in every
repo below reaches a stakeholder need through one, so a use case that changes
shape invalidates work at levels its author cannot see.
