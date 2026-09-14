---
id: compreq-voltage-sampler-rate
title: Voltage Sampler Conversion Rate
parent-subsystem-requirements:
  - subreq-battery-state-sampling.md
allocation: voltage-sampler
priority: Must Have
component-type: Software
requirement-type: Functional
verification-method: Test
---

| Field | Value |
|---|---|
| ID | compreq-voltage-sampler-rate |
| Parent Sub-system Requirements | subreq-battery-state-sampling.md |
| Allocation | voltage-sampler |
| Component Type | Software |
| Requirement Type | Functional |
| Priority | Must Have |
| Verification Method | Test |

## Requirement Statement

The voltage sampler shall complete a pack-voltage conversion within 100 ms of
being triggered.

## Rationale

The sub-system above owes a sample every second. A conversion budget of 100 ms
leaves the remaining 900 ms for cell balancing reads, filtering, and the
state-of-charge estimate, which share the same ADC.

This is the lowest tier in the model: it names a component, a measurable
condition, and a budget a test can assert directly.

## Acceptance Criteria

1. Conversion completes within 100 ms at the maximum rated pack voltage.
2. A conversion exceeding the budget sets a fault flag rather than returning a
   stale value.
