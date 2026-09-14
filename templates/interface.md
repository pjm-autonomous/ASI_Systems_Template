---
id: int-
title:
class:
status:
producer:
consumer:
---

<!-- An interface is owned by the nearest common ancestor of the two parties,
     and is stated in terms of THAT OWNER'S IMMEDIATE DESCENDANTS - never
     deeper. An L1 interface says "System A <-> System B" even when the exchange
     is between sub-systems inside them. Naming anything deeper publishes
     internals across a boundary this level cannot bind.

     class:  external-icd | internal | physical | build-time
     status: Draft | For Review | Baseline | Deprecated

     Ownership is arbitration authority and baseline control, not authorship -
     drafting is routinely delegated to the producing side. Record the drafter
     under Notes if it is not the owning level. -->

| Field | Value |
|---|---|
| Class | |
| Status | |
| Producer | |
| Consumer | |

## Purpose

<!-- Why does this interface exist? -->

## Contract

### Data Schema

### Protocol / Transport

### Behavioral Semantics

<!-- Request/response flows, streaming/eventing semantics, timing expectations, idempotency/retry rules -->

### Error Handling & Status Model

### Security Properties

<!-- authn/authz, encryption, key handling, where applicable -->

### Versioning & Compatibility Policy
