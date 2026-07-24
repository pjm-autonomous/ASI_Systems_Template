# Interface Control Documents (ICDs)

Grouped by feature bucket: `system/interfaces/<feature>/icd-<description>.md`. Start from `templates/icd.md`. See `example/system/interfaces/low-battery-return-to-dock/icd-dock-reservation-api.md` for a worked sample.

## What Belongs Here

An ICD is a contract between an `owning-component` and one or more `consumers` — internal service-to-service, or the boundary to an external system. It covers data schema, protocol/transport, behavioral semantics (request/response flows, timing, idempotency/retry rules), error handling, security properties, and a versioning/compatibility policy. It traces up to a `parent-product-requirement`.

Write the contract from the consumer's point of view — what must a caller be able to rely on — not as an implementation description of the owning component's internals.

## One ICD Per Interface, Not Per Message Type

If a component exposes several related operations to the same consumer(s) as part of one coherent contract, that's one ICD file with multiple entries in its Data Schema section, not one file per operation. Split into multiple ICD files when the operations serve genuinely different consumers or have independent versioning needs.

## Security Properties

Every ICD's "Security Properties" section should state authentication/authorization model, encryption expectations, and key-handling approach, even for purely internal service-to-service calls — "internal network boundary, standard service auth applies" is a valid answer, but it should be stated, not silently omitted. See the IEC 62443 cybersecurity-requirements checklist in `reference/standards-framework.md` for the property categories to check against (authentication, integrity, authorization, secure boot, non-repudiation).

## Versioning

State the compatibility policy explicitly (additive-only within a major version, deprecation window for breaking changes, etc.) — this is the field most often left as a placeholder and then never revisited once a second consumer shows up.
