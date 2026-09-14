# Glossary

Shared terminology. Add a term the first time it is used in an artifact with any
risk of ambiguity, rather than letting each author define it slightly
differently.

**This is an index, not a second source of truth.** Definitions here are one line
and point at where the term is actually specified. A full definition in two
places is a definition that will disagree with itself.

## Structure

The two most confusable terms in this standard, so they lead:

| Term | One line | Defined in |
|---|---|---|
| **Level** | A position in the architecture chain. **One repo is one level**; a level may hold many repos. | `standard/tier-schema.md` §1 |
| **Tier** | Structure *inside* a repo — `stakeholder`, `system`, `interfaces`, … A repo declares which tiers it masters. | `standard/tier-schema.md` §4 |
| Upstream | Toward the parent and, ultimately, the stakeholder need. | `standard/decisions.md` D-15 |
| Downstream | Toward derived artifacts. | `standard/decisions.md` D-15 |
| Packet | An optional part of the standard a repo opts into. Something that cannot be switched off is core, not a packet. | `standard/decisions.md` D-52 |
| Feature bucket | An optional kebab-case directory inside a tier, grouping artifacts by capability. | tier READMEs |

A directory is never named after a level. Levels change; tier names do not.

## Artifacts

| Term | One line | Defined in |
|---|---|---|
| Persona | A stakeholder who interacts with the system across its lifecycle. | `stakeholder/personas/README.md` |
| Use case | A specific need a persona has of the system. | `stakeholder/use-cases/README.md` |
| Product requirement | A stakeholder-facing statement of what the system shall do to satisfy a use case. Covers performance **and** safety; the distinction is `requirement-type`. | `product/requirements/README.md` |
| Capability requirement | What the platform must be able to do, derived from a product requirement. | `capability/requirements/README.md` |
| System requirement | Engineering decomposition of a capability requirement, allocated to a subsystem or component. | `system/requirements/README.md` |
| Sub-system requirement | Decomposition of a system requirement onto one sub-system. | `subsystem/requirements/README.md` |
| Component requirement | Decomposition of a sub-system requirement onto one component. The lowest tier. | `component/requirements/README.md` |
| Interface | A contract between a `producer` and a `consumer`, owned by the nearest common ancestor of the two. | `interfaces/README.md` |
| ICD | The document an interface entry may refine to. **Not** a synonym for the catalog entry — the entry is `int-*.md`. | `interfaces/README.md` |
| Architecture | The entities one level down and how they relate — the context an interface is defined against. | `architecture/README.md` |
| Data specification | The definition of one entity: schema, lifecycle, ownership, retention. | `system/data/README.md` |
| Deployment architecture | Where the parts run, and the obligations that come with it. | `system/deployment/README.md` |
| Parameter | A value a robot program declares, cited by name from requirements. | `system/parameters/README.md` |
| ADR | Architecture Decision Record — why a significant design choice was made. | `system/decisions/README.md` |

## Maturity

| Term | One line | Defined in |
|---|---|---|
| M1 | Authored. Structurally valid, content not yet assessed. | `_registry/README.md` |
| M2 | Quality gates pass, zero critical findings. Requires a dated promotion record. | `_registry/README.md` |
| M2+ | M2 plus adversarial review. | `_registry/README.md` |
| M3 | Named reviewer assigned, review completed. **Short IDs are assigned here.** | `_registry/README.md` |
| M4 | M3 actions closed; requires the level above to be at M4. | `_registry/README.md` |

`status` on an interface or an ADR is **not** maturity. `status` says where the
thing stands; maturity says how well the record of it has been reviewed.

## Requirement phrasing

| Term | One line | Defined in |
|---|---|---|
| EARS | Easy Approach to Requirements Syntax — the When / While / If / Where forms. | requirement tier READMEs |
| MoSCoW | The priority scheme: Must Have, Should Have, Could Have, Will Not Have. | `standard/artifact-schema.yaml` |

## Project-specific terms

Add terms genuinely specific to this project below — a custom stop-mode name, an
internal service name — and say so when you do.

Prefer citing an established definition (`ISO/IEC/IEEE 24765`, the systems and
software engineering vocabulary, is the usual source — see
`reference/standards-framework.md`) over inventing phrasing for a concept that
already has an industry-standard term.

| Term | Definition |
|---|---|
| Cat 0 / Cat 1 / Cat 2 | IEC 60204-1 stop categories — see `reference/standards-framework.md` |
