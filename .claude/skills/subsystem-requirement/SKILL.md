---
name: subsystem-requirement
description: Create or update a sub-system requirement in subsystem/requirements/. Use when decomposing a system requirement onto one sub-system.
---

# Skill: subsystem-requirement

Create or update a sub-system requirement in `subsystem/requirements/`.

**Check first:** this repo must declare the `subsystem` tier in
`repo-standard.yaml`.

## Create flow

Ask the user for:

1. A short description → becomes the kebab-case filename after `subreq-`
2. Parent system requirement(s) — `sysreq-*.md` filenames. These are in **this
   repo** and must exist; the validator resolves them locally
3. Allocation — the unit within the sub-system that carries the obligation
4. Component type, requirement type, priority, verification method — **read the
   legal values from `standard/artifact-schema.yaml`**
5. A plain-language description

Then create `subsystem/requirements/<bucket>/subreq-<description>.md` from
`templates/subsystem-requirement.md`:

- Populate frontmatter with exactly the fields the schema requires
- **Requirement Statement** — EARS form with the **sub-system** as the subject
- **Rationale** — say what the parent obligation is and why this decomposition
  satisfies it. A budget that narrows should say what it narrows from
- **Acceptance Criteria** — observable and testable

If the requirement cites a bound, confirm a `param-*.md` declares it; offer
`/parameter` if not.

**Do not hand-edit `traceability/TRACEABILITY.md`** — it is generated (D-46). The parent reference you set is what puts this artifact in the matrix. Run `build-traceability` to regenerate it; CI fails on a stale matrix.

Finish by running `validate-artifacts`.

## Update flow

1. Read the file
2. Ask what needs to change
3. Apply only the requested changes
4. If the statement changed, confirm it is still valid EARS
5. Re-run `validate-artifacts`

## Conventions

- Filename: `subreq-<description>.md`, kebab-case
- Plain Markdown tables, never HTML
- Keep `allocation` consistent with the entities named in `architecture/` and
  with the `producer` and `consumer` of interfaces in `interfaces/`
