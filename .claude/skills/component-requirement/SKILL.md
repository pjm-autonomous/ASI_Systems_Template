---
name: component-requirement
description: Create or update a component requirement in component/requirements/. Use when decomposing a sub-system requirement onto one component — the lowest tier in the model.
---

# Skill: component-requirement

Create or update a component requirement in `component/requirements/`.

**Check first:** this repo must declare the `component` tier in
`repo-standard.yaml`.

## Create flow

Ask the user for:

1. A short description → becomes the kebab-case filename after `compreq-`
2. Parent sub-system requirement(s) — `subreq-*.md` filenames. These are in
   **this repo** and must exist
3. Allocation — the component that carries the obligation
4. Component type, requirement type, priority, verification method — **read the
   legal values from `standard/artifact-schema.yaml`**
5. A plain-language description

Then create `component/requirements/<bucket>/compreq-<description>.md` from
`templates/component-requirement.md`:

- Populate frontmatter with exactly the fields the schema requires
- **Requirement Statement** — EARS form with the **component** as the subject
- **Rationale** — say what budget this takes from the tier above, and what it
  leaves for everything else sharing that budget
- **Acceptance Criteria** — must be assertable by a test, directly

## This is the lowest tier

There is nothing below this. If a component requirement still feels too coarse
to implement, **do not reach for another tier** — the answer is usually one of:

- the component is really two components, and the sub-system decomposition above
  needs revisiting;
- the detail belongs in a design artifact rather than a requirement; or
- the requirement describes *how* rather than *what*, and the implementation
  choice belongs in code or an ADR.

Say which of these applies rather than writing a vaguer requirement.

## Verification is required for coverage

Every component requirement needs a **verification test case**. The requirements
tool marks that relationship as required for coverage, so one without it leaves
the project reporting partial coverage however complete the requirement reads.

Ask what test would assert the acceptance criterion. If the criterion cannot be
asserted, the requirement is not finished — most often because it cites a bound
no `param-*.md` gives a value to. Note the intended test case in Requirement
Context when it does not exist yet.

**Do not touch `traceability/TRACEABILITY.md`** — generated (D-46).

Finish by running `validate-artifacts`.

## Update flow

1. Read the file
2. Ask what needs to change
3. Apply only the requested changes
4. If the statement changed, confirm it is still valid EARS
5. Re-run `validate-artifacts`

## Conventions

- Filename: `compreq-<description>.md`, kebab-case
- Plain Markdown tables, never HTML
