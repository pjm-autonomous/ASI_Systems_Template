---
artifact-type: adr
tier: system
---

# Architecture Decision Records

- [What belongs here](#what-belongs-here)
- [ADRs exist at every tier](#adrs-exist-at-every-tier)
- [Numbering](#numbering)
- [Status](#status)
- [Referencing an ADR from elsewhere](#referencing-an-adr-from-elsewhere)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `system/decisions/adr-NNNN-<description>.md` — zero-padded,
incrementing, **not** feature-bucketed. Start from `templates/adr.md`.

## What belongs here

An ADR captures a **significant, hard-to-reverse design decision**: the context
and problem, the options considered with their trade-offs, the decision, the
rationale, and the follow-up implications.

"Significant" is a judgement call. A workable test: would a new team member ask
*"wait, why did we do it this way?"* without it. Naming conventions, formatting
choices and easily-reversible implementation details do not need one.

An ADR carries **no parent requirement**. It explains why something is shaped the
way it is; the artifacts it explains reference it, not the other way round.

## ADRs exist at every tier

ADRs are valid at every requirement-bearing tier — `stakeholder`, `product`,
`capability`, `system`, `subsystem`, `component`.

**File the ADR at the tier whose artifacts it constrains.** A decision about how
two sub-systems divide responsibility belongs at `subsystem/decisions/`; a
decision about what the platform commits to belongs at `capability/decisions/`.
Filing it too high makes it look binding on levels that never agreed to it;
filing it too low hides it from the people it binds.

## Numbering

Numbers are **sequential and unique across the whole repo**, not per tier. An ADR
at `subsystem/decisions/` and one at `system/decisions/` draw from the same
sequence.

Two reasons: filenames must be unique repo-wide (D-22), and repo-local IDs stay
contiguous and unique (D-45). Per-tier sequences would collide on `adr-0001-*.md`
the moment two tiers each had one.

Never reuse a number, even when a decision is superseded or made obsolete —
update `status` instead of renumbering. Check the highest existing `adr-NNNN`
across **all** tiers before allocating, and do not leave gaps.

## Status

`status` is one of `proposed`, `accepted`, `superseded`, `obsolete` — the
authoritative list is the `adr-status` enum in
[`standard/artifact-schema.yaml`](../../standard/artifact-schema.yaml).

When a new ADR supersedes an old one, set the old one's status to `superseded`
and reference the new ADR from its Implications section. **Do not delete a
superseded ADR.** A reversed decision is more useful than a vanished one: it
records that the question was asked, what was tried, and why it changed — which
is what stops the same wrong turn being taken twice.

## Referencing an ADR from elsewhere

Architecture diagrams, requirements and data specifications frequently reference
the ADR explaining *why* they are shaped as they are.

Prefer that over re-explaining the rationale in several places. The rationale
then has one home, and changing the decision does not mean finding every document
that paraphrased it.

## Maturity

ADRs start at `M1`. A state at or above `M2` requires a dated promotion record in
`_registry/` — see [`standard/decisions.md`](../../standard/decisions.md)
D-40 … D-43.

Note the distinction between `status` and maturity: `status` says where the
decision stands, maturity says how well the record of it has been reviewed. An
`accepted` ADR at `M1` is a decision people are acting on whose reasoning nobody
has checked.
