# Maturity Registry

Evidence behind every maturity claim in this repo. A `**Status:** M2` line on an
artifact is a claim; the record in here is what makes it true.

Adopted from `asirobots/axs`, which runs the same M1–M4 model (PRAK Architecture
Review item A4). Enabled per repo via `packets.maturity-gates` in
`repo-standard.yaml`; when that flag is off, nothing here is required.

## Layout

| Directory | Holds |
|-----------|-------|
| `m2_records/` | M1→M2 and M2→M2+ readiness records — quality-gate scorecards, findings, verdicts |
| `m3_reviews/` | M3 named-review records and M4 closure evidence |

## Naming

`{Tier}-{ArtifactSlug}_{State}_Record.md`, e.g.
`system-sysreq-geofence-map-validation_M2_Record.md`.

`tools/validate.py` locates a record by matching the **artifact slug** inside the
filename, so the slug must appear verbatim. Everything else in the name is for
humans.

## States

| State | Means | Evidence required |
|-------|-------|-------------------|
| **M1** | Authored. Structurally valid, content not yet assessed. | None |
| **M2** | All quality gates pass, zero critical findings. | `m2_records/` |
| **M2+** | M2 plus adversarial review. | `m2_records/` |
| **M3** | Named reviewer assigned, review completed. | `m3_reviews/` |
| **M4** | M3 action items closed or accepted; tier above is M4. | `m3_reviews/` |

Two rules the validator enforces:

1. **Anything at or above M2 needs a record.** Without this the state is a line
   somebody edited.
2. **M4 at one tier requires M4 at the tier above.** A component cannot be more
   mature than the system that requires it — AxS's "M4 on level N requires M4 on
   level N−1", expressed over tiers.

Gate criteria themselves belong to the governing engineering lifecycle document,
not to the validator. This directory holds evidence; it does not define the bar.
