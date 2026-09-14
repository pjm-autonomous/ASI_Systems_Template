---
artifact-type: subsystem-requirement
tier: subsystem
---

# Sub-system Requirements

- [What belongs here](#what-belongs-here)
- [What a sub-system requirement traces to](#what-a-sub-system-requirement-traces-to)
- [When to split a sub-system into its own repo](#when-to-split-a-sub-system-into-its-own-repo)
- [Allocation and component type](#allocation-and-component-type)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `subsystem/requirements/subreq-<description>.md`, optionally grouped
into a feature-bucket directory. Start from `templates/subsystem-requirement.md`.

## What belongs here

A sub-system requirement is **the decomposition of a system requirement onto one sub-system**. It narrows a system-level obligation to a part of the design that
one team or one build unit is responsible for.

Both this tier and the system tier above it live in the **same repo and the same level**. That is the point: L2 owns the whole engineering decomposition, and only
the link up to the capability requirement leaves the repo.

## What a sub-system requirement traces to

```text
capability requirement            L1, ANOTHER repo
   └─ system requirement          system tier, SAME repo
        └─ sub-system requirement subsystem tier   ← you are here
             └─ component requirement   component tier, SAME repo
```

- **Upstream:** `parent-system-requirements`, resolved **locally** — the parent is
  in this repo and must exist. Several parents are allowed (D-20).
- **Downstream:** component requirements in this repo name this one.

Unlike the system tier above, neither link here crosses a repository boundary.
A broken reference is caught immediately rather than at the next index publish.

## When to split a sub-system into its own repo

The default is to decompose **inside this repo**. A sub-system may be split into
its own repo where complexity genuinely warrants it — **conditional on traceability surviving the split** (D-08).

That condition is not a formality. A split repo must be able to show an unbroken
parent chain from its artifacts back to this one, which means it declares this
repo as its parent and this repo publishes an `artifact-index.json` for it to
resolve against. A split that cannot demonstrate that chain is not permitted.

Split when a sub-system has its own team, its own release cadence, or its own
compliance obligations. Do not split to make directories smaller.

## Allocation and component type

- `allocation` names the specific unit within the sub-system that carries the
  obligation.
- `component-type` declares whether that unit is `Software`, `Hardware` or
  `Electrical`. The authoritative values are in
  [`standard/artifact-schema.yaml`](../../standard/artifact-schema.yaml); they
  match the requirements tool's own picklist, so a value rejected there is
  rejected here.

Keep `allocation` consistent with the entities named in `architecture/` and with
the `producer` and `consumer` of interfaces in `interfaces/`.

## Maturity

Sub-system requirements start at `M1`. A state at or above `M2` requires a dated
promotion record in `_registry/` — see
[`standard/decisions.md`](../../standard/decisions.md) D-40 … D-43.

**M4 requires the tier above to be at M4** (D-42). A sub-system requirement
cannot be more mature than the system requirement it decomposes, and that chain
runs all the way up through the capability requirement in the L1 repo.
