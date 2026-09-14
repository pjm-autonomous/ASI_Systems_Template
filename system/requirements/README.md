---
artifact-type: system-requirement
tier: system
---

# System Requirements

- [What belongs here](#what-belongs-here)
- [What a system requirement traces to](#what-a-system-requirement-traces-to)
- [Allocation](#allocation)
- [Cited bounds need a parameter](#cited-bounds-need-a-parameter)
- [Cross-industry process standards](#cross-industry-process-standards)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `system/requirements/sysreq-<description>.md`, optionally grouped
into a feature-bucket directory. Start from `templates/system-requirement.md`.

## What belongs here

A system requirement is **the engineering decomposition of a capability
requirement**, allocated to a specific subsystem or component.

Where a capability requirement says *what* the system does for a stakeholder, a
system requirement says *which part* does it and under *what measurable condition* — timing budgets, thresholds, allocation. Several system requirements
commonly decompose one capability requirement.

This is the **highest** tier in an L2 repo. Everything above it is authored
elsewhere, by someone else.

## What a system requirement traces to

```text
capability requirement            L1, ANOTHER repo
   └─ system requirement          system tier      ← you are here
        └─ sub-system requirement subsystem tier, SAME repo
             └─ component requirement   component tier, SAME repo
```

- **Upstream:** `parent-capability-requirements` names one or more capability
  requirements in the L1 repo. **More than one is allowed** — every `parent-*`
  field is many-to-many (D-20); the one-parent-only model was a Jira limitation
  and neither GitHub nor Jama imposes it. A single parent may still be written as
  a plain scalar.
- **Downstream:** sub-system requirements in *this* repo name this one. That link
  resolves locally.

The upstream link cannot be resolved from here. It is shape-checked locally and
verified upstream against the L1 repo's published `artifact-index.json`.

> A system requirement does **not** name a use case. Use cases are L0, two
> levels up, and the trace reaches them through the capability requirement.

## Allocation

The `allocation` field names a real subsystem or component in this project's
architecture. Keep it consistent with:

- the entities named in `architecture/` diagrams, and
- the `producer` and `consumer` of any interface in `interfaces/`.

`tools/validate.py` does not cross-check allocation against those, so consistency
here is a discipline rather than an enforced rule. If that proves to be a
recurring failure rather than a worry, it earns a check — see the governing
principle in `CONTRIBUTING.md`.

> An interface names its two parties as `producer` and `consumer`, at the
> granularity of the owning level's *immediate descendants* (D-04) — so an
> allocation naming a deep component will not appear verbatim in an interface
> one level up, and should not.

## Cited bounds need a parameter

If a requirement cites a bound — a timing budget, a threshold, a rate — that
bound needs a `param-*.md` artifact holding a real value. A requirement deferring
to "the configured interval" with no parameter declaring it is **unverifiable by construction**, and no verification test can state a pass criterion for it.

This tier is where it bites hardest: system requirements are where timing budgets
and thresholds are normally written down.

## Cross-industry process standards

This tier is where ASPICE PAM 4.0 (SWE.1–SWE.6, SYS.2–SYS.3) and
ISO/IEC/IEEE 15288's requirements and design process areas map most directly. See
`reference/standards-framework.md` if a project needs to show that mapping for a
customer or an audit.

## Maturity

System requirements start at `M1`. A state at or above `M2` requires a dated
promotion record in `_registry/` — see
[`standard/decisions.md`](../../standard/decisions.md) D-40 … D-43.

Short IDs are assigned at **M3**, and assignment triggers a review in which no
reply equals acceptance (D-43). **M4 additionally requires the level above to be
at M4** (D-42) — a system requirement cannot be more mature than the capability
requirement it decomposes.
