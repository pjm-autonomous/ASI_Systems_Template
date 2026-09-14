---
name: product-requirement
description: Create or update a product requirement in product/requirements/. Use when the user wants to state what the system shall do to satisfy a use case, including safety and performance obligations.
---

# Skill: product-requirement

Create or update a product requirement in `product/requirements/`.

**Check first:** this repo must declare the `product` tier in
`repo-standard.yaml`. If it does not, the artifact belongs at the level that
owns that tier — in another repo. Stop and say so rather than creating it here.

## What this type covers

Product performance **and** safety requirements both use this type. The
distinction is the `requirement-type` field, not a separate type and **not**
priority: priority says when you would build it, `requirement-type` says what
kind of obligation it is.

## Create flow

Ask the user for:

1. A short description → becomes the kebab-case filename after `prodreq-`
2. Parent use case(s) — one or more `uc-*.md` filenames from
   `stakeholder/use-cases/`. Both tiers are L0, so these resolve locally and
   must exist
3. Requirement type, priority, verification method — **read the legal values
   from `standard/artifact-schema.yaml`**; do not offer a list from memory
4. Feature bucket, if the project uses them
5. A plain-language description of the obligation

Then create `product/requirements/<bucket>/prodreq-<description>.md` from
`templates/product-requirement.md`:

- Populate frontmatter with exactly the fields the schema requires for
  `product-requirement`
- **Requirement Statement** — EARS form: *When `<trigger>`, the system shall
  `<response>`* (also While / If / Where)
- **Rationale** — trace the obligation to the stakeholder need behind it
- **Acceptance Criteria** — observable and testable

**If the requirement cites a bound** — a timeout, a rate, a distance, a
threshold — do not write the number into the prose. Ask whether a `param-*.md`
exists for it; if not, offer to create one with `/parameter` first. A cited bound
with no parameter makes the requirement unverifiable by construction.

**Do not hand-edit `traceability/TRACEABILITY.md`.** It is generated from
frontmatter (D-46). The parent reference you set is what puts this artifact in
the matrix. Run `build-traceability` to regenerate it; CI fails on a stale one.

Finish by running `validate-artifacts` and fixing anything it reports.

## Update flow

1. Read the file
2. Ask what needs to change
3. Apply only the requested changes — do not regenerate the file
4. If the statement changed, confirm it is still valid EARS
5. Re-run `validate-artifacts`

## Conventions

- Filename: `prodreq-<description>.md`, kebab-case
- Plain Markdown tables, never HTML
- Describes stakeholder-observable behaviour. If it names a component, a service
  or an algorithm, it has gone too far — allocation happens at L2, in another
  repo, and naming one here binds a design decision that is not this level's to
  make
