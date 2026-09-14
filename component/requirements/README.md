---
artifact-type: component-requirement
tier: component
---

# Component Requirements

- [What belongs here](#what-belongs-here)
- [What a component requirement traces to](#what-a-component-requirement-traces-to)
- [This is where decomposition stops](#this-is-where-decomposition-stops)
- [Verification](#verification)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `component/requirements/compreq-<description>.md`, optionally
grouped into a feature-bucket directory. Start from
`templates/component-requirement.md`.

## What belongs here

A component requirement is **the decomposition of a sub-system requirement onto one component** — the smallest unit the engineering model names.

It is specific enough to implement against and to verify directly: a named
component, a measurable condition, and an acceptance criterion a test can assert.

## What a component requirement traces to

```text
system requirement            system tier, SAME repo
   └─ sub-system requirement  subsystem tier, SAME repo
        └─ component requirement   component tier   ← you are here
```

- **Upstream:** `parent-subsystem-requirements`, resolved **locally**. Several
  parents are allowed (D-20).
- **Downstream:** nothing in the requirement model. The next thing that refers to
  a component requirement is a verification test case.

## This is where decomposition stops

The model has no tier below this one. If a component requirement still feels too
coarse to implement, the answer is **not** another requirement tier — it is
usually one of:

- the component is actually two components, and the sub-system decomposition
  above needs revisiting;
- the detail belongs in a design artifact rather than a requirement; or
- the requirement is describing *how* rather than *what*, and the implementation
  choice should sit in code or in an ADR.

Adding depth to escape a decomposition problem moves the problem rather than
solving it, and every added tier multiplies the traceability that must be
maintained.

## Verification

**Every component requirement needs a verification test case.** The requirements
tool marks that relationship as required for coverage, so a component requirement
without one leaves the project reporting partial traceability coverage regardless
of how complete the requirement itself looks.

Plan the test case alongside the requirement, not after. If the acceptance
criterion cannot be stated as something a test asserts, the requirement is not
finished — most often because it cites a bound that no `param-*.md` gives a
value to, which makes it **unverifiable by construction**.

## Maturity

Component requirements start at `M1`. A state at or above `M2` requires a dated
promotion record in `_registry/` — see
[`standard/decisions.md`](../../standard/decisions.md) D-40 … D-43.

**M4 requires the tier above to be at M4** (D-42), and that chain runs the full
height of the model: component → sub-system → system in this repo, then
capability requirement in the L1 repo, then product requirement and use case in
the L0 repo. A component requirement is the last artifact to reach M4, never the
first.
