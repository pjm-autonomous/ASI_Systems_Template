# Architecture Decision Records (ADRs)

Not feature-bucketed — sequential across the whole project: `system/decisions/adr-NNNN-<description>.md`, zero-padded, incrementing. Start from `templates/adr.md`. See `example/system/decisions/adr-0001-centralize-dock-reservation-in-fleet-service.md` for a worked sample.

## What Belongs Here

An ADR captures a significant, hard-to-reverse design decision: the context/problem, the options considered with their tradeoffs, the decision, the rationale, and follow-up implications. "Significant" is a judgment call — a good test is whether a new team member would ask "wait, why did we do it this way?" without it. Naming conventions, formatting choices, and easily-reversible implementation details don't need an ADR.

## Numbering

Numbers increment sequentially and are never reused, even if a decision is later superseded or made obsolete — update the `status` field instead of renumbering. Check the highest existing `adr-NNNN` before creating a new one; don't leave gaps.

## Status Field

`status` is one of `proposed`, `accepted`, `superseded`, or `obsolete`. When a new ADR supersedes an old one, set the old one's status to `superseded` and reference the new ADR's ID in its "Implications / Follow-ups" section — don't delete superseded ADRs; they're part of the project's decision history.

## Referencing ADRs From Elsewhere

Architecture diagrams, system requirements, and data specifications frequently reference the ADR that explains *why* they're shaped the way they are (see how `arch-dock-return-flow.md` and `sysreq-dock-availability-check.md` both reference `adr-0001` in the example). Prefer that pattern over re-explaining the same rationale in multiple places.
