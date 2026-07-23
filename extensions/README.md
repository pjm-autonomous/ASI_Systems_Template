# Extensions

Stub folders for the parts of the SE lifecycle that aren't authored at project kickoff. Each file here is a placeholder, not real content — replace it when the project reaches that maturity point.

| Folder | Covers | BKM Reference |
|---|---|---|
| `safety/` | Safety management, hazard analysis, functional safety concept, FMEA, safety case | `reference/bkm-document-set.md` §3 |
| `coding/` | Coding standard, static analysis, code review, build/integration | `reference/bkm-document-set.md` §5 |
| `testing/` | Test strategy, unit/integration/system testing, coverage analysis | `reference/bkm-document-set.md` §6 |
| `qa-cm/` | Quality assurance, configuration management, version control, dev environment | `reference/bkm-document-set.md` §7 |
| `change-risk/` | Change management, risk register | `reference/bkm-document-set.md` §9 |
| `metrics/` | Metrics program, lessons learned | `reference/bkm-document-set.md` §10 |

## Rules for These Folders

- Do not delete a stub file just because the category doesn't seem relevant yet. Instead, edit it to record the decision to defer: who decided, why, and when it should be revisited.
- When you do author real content, remove the "STUB" marker and the pointer boilerplate, but keep the file in place (same filename) so links from `traceability/STANDARDS-MAPPING.md` and elsewhere keep working.
- These are not validated by `tools/validate.py` — they're plain documentation, not traceability-chain artifacts.
