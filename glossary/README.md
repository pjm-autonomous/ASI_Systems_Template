# Glossary

`GLOSSARY.md` holds shared terminology. Add a term the first time it is used in
an artifact with any risk of ambiguity, rather than letting each author define it
slightly differently across files.

## It is an index, not a definition

Each entry is **one line plus a pointer** to where the term is actually
specified — a tier README, `standard/tier-schema.md`, or
`standard/artifact-schema.yaml`.

Writing the full definition here as well would make the glossary a second source
of truth, and the copy that drifts is always the one nobody is looking at when
they change the model. If a one-line summary is not enough, the fix is to improve
the definition where it lives and leave the pointer alone.

## Prefer an established definition

Cite an existing standard rather than inventing phrasing for a concept that
already has an industry-standard term. `ISO/IEC/IEEE 24765` — the systems and
software engineering vocabulary — is the usual source; see
`reference/standards-framework.md`.

Reserve project-invented definitions for concepts genuinely specific to this
project: a custom stop-mode name, an internal service name. Say so when you add
one, so a reader can tell a local coinage from a standard term.

## Terms that earn an entry

- Anything two people on the project have used differently.
- Anything that looks like a synonym and is not. `ICD` and `interface` are the
  live example: an interface catalog entry is `int-*.md`; an ICD is the document
  it may refine to.
- Anything whose meaning depends on where you are standing — `level` and `tier`
  most of all.
