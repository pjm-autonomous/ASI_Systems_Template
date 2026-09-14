---
artifact-type: interface
tier: interfaces
---

# Interfaces

- [What belongs here](#what-belongs-here)
- [Who owns an interface](#who-owns-an-interface)
- [State it at your own descendants, never deeper](#state-it-at-your-own-descendants-never-deeper)
- [Class and status](#class-and-status)
- [One interface per contract, not per message](#one-interface-per-contract-not-per-message)
- [Security properties](#security-properties)
- [Versioning](#versioning)
- [Maturity](#maturity)

> **Which level declares this tier, and who owns it:**
> [`standard/tier-schema.md`](../standard/tier-schema.md) §1 and §4.
> Deliberately not repeated here — a renumbering must stay a one-line change.

Files live at `interfaces/int-<description>.md`, optionally grouped into a
feature-bucket directory. Start from `templates/interface.md`.

## What belongs here

An interface is a **contract between two parties**: `producer` and `consumer`.

It covers data schema, protocol and transport, behavioural semantics
(request/response flows, timing, idempotency and retry rules), error handling,
security properties, and a versioning and compatibility policy.

Write it from the **consumer's** point of view — what must a caller be able to
rely on — not as a description of the producer's internals. An interface that
reads like a design document has already leaked what it exists to hide.

## Who owns an interface

> **An interface is owned by the nearest common ancestor of the parties it
> connects** (D-04).

Where the two parties are siblings — the ordinary case — that is their immediate
parent. Where they sit in different branches, ownership rises to whichever level
contains both.

The reason is that **two peers cannot arbitrate a boundary they both sit on**.
Neither has standing to bind the other, so a disagreement has no venue. The
integrating level has both the system view and the authority.

The stronger reason is schedule: the interface must be fixed **before** either
side can be built or verified independently. An undefined boundary serialises
work that ought to run in parallel.

Two consequences:

- **An interface never lives in the repo of the thing it describes.** It lives
  with whoever arbitrates the boundary — one level up.
- **Ownership is arbitration authority and baseline control, not authorship.**
  Drafting is routinely delegated, usually to the producing side. Record the
  drafter in Notes when it is not the owning level. Both parties owe conformance
  evidence; only one owns the contract.

## State it at your own descendants, never deeper

`producer` and `consumer` name **this level's immediate descendants**.

An L1 interface says *System A ↔ System B* even when the actual exchange is
between sub-systems inside them. Naming anything deeper publishes internals
across a boundary this level has no authority to bind, and couples the two
systems' internals to each other.

This is what keeps an interface a **contract** rather than a description of
today's implementation: either side may restructure internally without
renegotiating, so long as the statement at this granularity still holds.

## Class and status

Both are required. The authoritative value lists are the `interface-class` and
`interface-status` enums in
[`standard/artifact-schema.yaml`](../standard/artifact-schema.yaml).

| `class` | Means |
| --- | --- |
| `external-icd` | crosses this system's boundary to a party outside the tree |
| `internal` | between two entities inside the tree |
| `physical` | a mechanical or electrical boundary |
| `build-time` | consumed at build or integration time, not at runtime |

`status` runs `Draft` → `For Review` → `Baseline` → `Deprecated`. Baseline is the
point at which both sides may build against it without asking.

## One interface per contract, not per message

Several related operations serving the same consumer as one coherent contract are
**one** file with multiple entries in its Data Schema section.

Split into separate files when the operations serve genuinely different consumers
or have independent versioning needs — that is, when one could go to `Baseline`
while the other is still `Draft`.

## Security properties

State the authentication and authorisation model, encryption expectations, and
key handling — **even for purely internal calls**. *"Internal network boundary,
standard service auth applies"* is a valid answer; silence is not, because a
reader cannot tell it apart from an oversight.

See the IEC 62443 checklist in `reference/standards-framework.md` for the
categories to check against: authentication, integrity, authorisation, secure
boot, non-repudiation.

## Versioning

State the compatibility policy explicitly — additive-only within a major version,
deprecation window for breaking changes, and so on.

This is the field most often left as a placeholder and never revisited, and the
cost lands the day a second consumer appears and nobody can say whether a change
is permitted.

## Maturity

Interfaces start at `M1`. A state at or above `M2` requires a dated promotion
record in `_registry/` — see [`standard/decisions.md`](../standard/decisions.md)
D-40 … D-43.

Interface maturity and `status` are different things and both matter: `status`
says how settled the contract is for the parties, maturity says how reviewed the
artifact is. An interface at `Baseline` with maturity `M1` is a contract two
teams are building against that nobody has formally reviewed.
