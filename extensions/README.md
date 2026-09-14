# Extensions

- [What these are](#what-these-are)
- [Categories](#categories)
- [Rules for these folders](#rules-for-these-folders)
- [Relationship to the artifact tiers](#relationship-to-the-artifact-tiers)
- [Known gap: security](#known-gap-security)

## What these are

Stub folders for the parts of the systems engineering lifecycle **not authored at
project kickoff**. Each file is a placeholder, not content — replace it when the
project reaches that maturity point.

They ship as stubs rather than as empty directories so that missing lifecycle
documentation is **visible in every project baseline** instead of silently
absent. An empty directory looks like nothing is needed; a stub says something is
owed.

`extensions` is an opt-in packet. A project that will genuinely never need these
turns it off in `repo-standard.yaml` — but turning it off is a decision worth
recording, not a tidying-up.

## Categories

| Folder | Covers | BKM reference |
|---|---|---|
| `safety/` | Safety management, hazard analysis, functional safety concept, FMEA, safety case | `reference/bkm-document-set.md` §3 |
| `coding/` | Coding standard, static analysis, code review, build and integration | `reference/bkm-document-set.md` §5 |
| `testing/` | Test strategy, unit / integration / system testing, coverage analysis | `reference/bkm-document-set.md` §6 |
| `qa-cm/` | Quality assurance, configuration management, version control, dev environment | `reference/bkm-document-set.md` §7 |
| `change-risk/` | Change management, risk register | `reference/bkm-document-set.md` §9 |
| `metrics/` | Metrics program, lessons learned | `reference/bkm-document-set.md` §10 |

## Rules for these folders

- **Do not delete a stub because the category does not seem relevant yet.** Edit
  it to record the decision to defer: who decided, why, and when it is revisited.
  A deferral with an owner is a decision; a deleted file is an absence nobody can
  explain later.
- **When you author real content, keep the filename.** Remove the `STUB` marker
  and the pointer boilerplate, but leave the file where it is, so links from
  `traceability/STANDARDS-MAPPING.md` and elsewhere keep resolving.
- **These are not validated by `tools/validate.py`.** They are documentation, not
  traceability-chain artifacts — no frontmatter schema, no parent, no maturity
  gate. Completeness here is a review question, not a CI question.

## Relationship to the artifact tiers

Extensions are **lifecycle documentation, not tier artifacts**. They describe how
the project works rather than what the system does, so they sit outside the
tier model and carry no `parent-*` field.

They do reference tier artifacts — a safety case cites the requirements it
argues over, a test strategy cites what it verifies — and those references point
into whichever tiers this repo declares. Keep the reference one-way: an extension
document cites artifacts; artifacts do not cite extension documents as parents.

Which level authors which category is not settled and is deliberately not
asserted here. A safety case and a coding standard plainly do not belong to the
same owner, but the mapping is a project decision until recorded otherwise.

## Known gap: security

**There is no `security/` category**, and there should be. The lifecycle
categories above cover safety, coding, testing, QA/CM, change and risk, and
metrics — security engineering practice is absent entirely, from both this folder
and `reference/bkm-document-set.md`.

That matters on a project with IEC 62443 or ISO/SAE 21434 exposure, and
`reference/standards-framework.md` already lists both. Tracked in `TODO.md`;
the shape would be `security-risk-assessment.md` (threat model),
`security-plan.md`, and `vulnerability-management.md`, following the same
owner-frontmatter and `STUB`-marker pattern as the categories above.

Until it exists, a project with security obligations should say so explicitly in
`traceability/STANDARDS-MAPPING.md` rather than letting the absence read as
"not applicable".
