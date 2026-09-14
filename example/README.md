# Example: Low-Battery Return-to-Dock

- [The chain](#the-chain)
- [Where the repo boundaries fall](#where-the-repo-boundaries-fall)
- [What this example is built to show](#what-this-example-is-built-to-show)
- [Using it](#using-it)

A single fictional feature worked end to end through every artifact type, so the
pieces can be seen connected before authoring your own.

Illustrative only — not a real ASI product feature, and deliberately generic
(warehouse fleet robotics) so it does not read as authoritative guidance for any
specific product.

## The chain

```text
L0  stakeholder/personas/fleet-operator.md
      └─ stakeholder/use-cases/uc-low-battery-return-to-dock.md
L0         └─ product/requirements/prodreq-return-before-depletion.md
═══════════════════ repo boundary ═══════════════════
L1              └─ capability/requirements/capreq-autonomous-return-to-dock.md
═══════════════════ repo boundary ═══════════════════
L2                   ├─ system/requirements/sysreq-battery-threshold-monitor.md
L2                   │    └─ subsystem/requirements/subreq-battery-state-sampling.md
L2                   │         └─ component/requirements/compreq-voltage-sampler-rate.md
L2                   └─ system/requirements/sysreq-dock-availability-check.md

  cross-cutting, no parent:
    architecture/arch-dock-return-flow.md          sequence diagram
    interfaces/int-dock-reservation-api.md         fleet-coordination ↔ power-management
    system/data/data-dock-reservation-schema.md    the entity that interface carries
    system/deployment/deploy-fleet-coordination-topology.md
    system/decisions/adr-0001-centralize-dock-reservation-in-fleet-service.md
    system/parameters/param-battery-reserve-threshold.md    cited by two requirements
```

## Where the repo boundaries fall

**This example carries all three levels in one tree. A real deployment does
not.** L0, L1 and L2 are three separate repositories, and the two links marked
above cross between them.

That changes how to read it:

- The two crossing links are **shape-checked locally and verified upstream**
  against the parent repo's published `artifact-index.json`. Here both ends
  happen to sit in the same tree, which is a property of the example, not of the
  model.
- **Nobody sees this whole chain at once in practice.** The Systems Architect
  authoring the capability requirement cannot see the component requirement; the
  Systems Engineer authoring the component requirement cannot see the use case.
  That is why parent references matter — they are the only thing carrying intent
  across a boundary a person cannot see over.
- Everything below the second boundary — system, sub-system, component — is one
  repo and resolves locally.

## What this example is built to show

Four things that are easy to get wrong, demonstrated rather than described:

1. **The product tier is not optional.** A use case's child is a *product*
   requirement, and the capability requirement derives from **that**, not from
   the use case. Collapsing the two is the most common misreading of the model.
2. **Decomposition runs to the component tier.**
   `sysreq-battery-threshold-monitor` → `subreq-battery-state-sampling` →
   `compreq-voltage-sampler-rate` shows the budget narrowing at each step: detect
   the threshold, sample once a second, convert within 100 ms.
3. **A cited bound has a parameter.** The product requirement says "the reserve
   threshold" and writes no number. `param-battery-reserve-threshold.md` holds
   the value, the measurement point, and the basis — including that it is
   site-specific and must be re-derived rather than inherited. Without it the
   requirement would be unverifiable by construction.
4. **An interface names its two parties, not its internals.**
   `int-dock-reservation-api.md` is `fleet-coordination-service` ↔
   `power-management-service` — services, not the components inside them.

## Using it

Copy the **pattern**, not the content. Swap in your own persona, feature name and
allocations.

Two things not to copy:

- **The single-tree layout.** A real repo declares one level and holds only the
  tiers that level owns.
- **`traceability/TRACEABILITY.md`.** It is shown filled in so the shape is
  visible, but in a real repo the matrix is **generated from frontmatter**, never
  hand-written.

`tests/test_example.py` holds every artifact here to the same schema your
artifacts are held to — so if the example ever disagrees with the standard, the
build says so rather than an author discovering it.
