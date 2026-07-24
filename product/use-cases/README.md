# Use Cases

Grouped by feature bucket: `product/use-cases/<feature>/uc-<description>.md`. Start from `templates/use-case.md`. See `example/product/use-cases/low-battery-return-to-dock/` for a worked sample.

## What Belongs Here

A use case is a specific need a persona has of the system — one coherent interaction with a main flow, preconditions, postconditions, and the exception paths worth calling out. It traces up to `parent-personas` and down to one or more product requirements (`product/requirements/<feature>/req-*.md`, via that requirement's `parent-use-cases`).

Write use cases from the persona's point of view ("As a fleet operator, I need...") rather than as a system-behavior statement — that phrasing belongs one layer down, in the product requirement's EARS statement.

## Creating a Feature Bucket

No feature buckets exist until the first use case is authored against a real persona need. Name the bucket for the capability, not the persona or a specific implementation detail (`low-battery-return-to-dock`, not `fleet-operator-stuff` or `power-management-service`). Reuse an existing bucket if a new use case is a natural extension of it; create a new bucket only when the use case doesn't fit any existing one.

## Sizing a Use Case

If a use case's main flow is growing past 6-8 steps, or it's accumulating many unrelated exception flows, it's probably two use cases. Split along "what triggers this" rather than trying to keep one file that covers every trigger for a capability.
