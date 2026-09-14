---
artifact-type: capability-requirement
tier: capability
---

# Capability Requirements

- [What belongs here](#what-belongs-here)
- [This is the only requirement tier at this level](#this-is-the-only-requirement-tier-at-this-level)
- [What a capability requirement traces to](#what-a-capability-requirement-traces-to)
- [EARS format](#ears-format)
- [What this level also owns](#what-this-level-also-owns)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `capability/requirements/capreq-<description>.md`, optionally
grouped into a feature-bucket directory. Start from
`templates/capability-requirement.md`.

## What belongs here

A capability requirement states **what the platform must be able to do**, derived
by the Systems Architect from the product requirements one level upstream.

It is the bridge between a stakeholder-facing obligation and an engineering
decomposition: specific enough that a Systems Engineer can decompose it, general
enough that it does not pre-empt their design. If it names a component, it has
gone too far — allocation happens downstream, in a repo this level does not own.

## This is the only requirement tier at this level

**There are no system requirements here.** A system requirement is an L2 artifact
and only an L2 artifact — see [`standard/decisions.md`](../../standard/decisions.md)
D-03 and D-05.

If you are reaching for `sysreq-` in this repo, the artifact belongs in a
sub-system repo.

## What a capability requirement traces to

```text
product requirement           L0, ANOTHER repo
   └─ capability requirement  capability tier   ← you are here
        └─ system requirement L2, ANOTHER repo
```

Both links cross a repository boundary, and **both are created by the child**
(D-29):

- **Upstream:** this artifact names `parent-product-requirements`. It cannot be
  resolved locally; it is shape-checked here and verified upstream against the L0
  repo's published `artifact-index.json`.
- **Downstream:** a system requirement in an L2 repo names this one in its
  `parent-capability-requirements`. You do not author that link and will not see
  it in this repo. Coverage — which capability requirements have been decomposed —
  is observed, not declared.

For a child repo to resolve its parents against this one, run
`emit-artifact-index` here and commit the result.

## EARS format

- **When** `<trigger>`, the system shall `<response>`.
- **While** `<state>`, the system shall `<behavior>`.
- **If** `<condition>`, the system shall `<action>`.
- **Where** `<feature is included>`, the system shall `<capability>`.

## What this level also owns

Capability requirements are not the whole of this level's responsibility. **This
level also owns the interfaces between the systems one level down**, and the
architecture those boundaries are drawn on — see `interfaces/` and
`architecture/`.

That pairing is not incidental: a boundary between two L2 systems cannot be
defined without an architecture saying those systems exist and how they relate,
and neither of those two systems can arbitrate a boundary it sits on.

## Maturity

Capability requirements start at `M1`. A state at or above `M2` requires a dated
promotion record in `_registry/` — see
[`standard/decisions.md`](../../standard/decisions.md) D-40 … D-43.

Short IDs are assigned at **M3**, and assignment triggers a review in which no
reply equals acceptance (D-43). Because every L2 repo decomposes from these, an
unstable capability requirement invalidates work in repos this level cannot see —
stabilise before the sub-system teams build on it.
