# Decision Register

Every ratified decision governing this standard, one row each. **This is the only
place a decision is recorded.** Other files apply decisions; they do not restate
them. If a file asserts something not in this register, either the decision is
missing here or the assertion is wrong.

Superseded rows are kept with a strikethrough and a pointer, never deleted — a
decision that was reversed is more useful than one that vanished.

## Architecture and levels

| Key | Decision | Date | Source |
|-----|----------|------|--------|
| **D-01** | **A repo occupies exactly one level; a level may hold many repos.** L0 `axs` · L1 `prak-v-model` · L2 `prak-embedded-core` and siblings (SMU, Driver, …). The level is a property of the repo, declared once, stored nowhere else. | 2026-09-11 | Tier schema agreement |
| **D-02** | **ASAM is a categorical classification, not an architecture level.** | 2026-09-10 | Review `R2` |
| **D-03** | **L0 owns** stakeholder/market needs → use cases, product performance requirements, safety requirements. **L1 owns** capability requirements. **L2 owns** system, sub-system and component requirements plus architecture. | 2026-09-11 | Tier schema agreement |
| **D-04** | **An interface is owned by the nearest common ancestor of the parties it connects, and is expressed in terms of that owner's immediate descendants.** A sub-system in System A talking to a sub-system in System B is owned by L1 and stated as *System A ↔ System B* — never naming L3 internals. Ownership is arbitration authority and baseline control, not authorship. | 2026-09-13 | Tier schema agreement; granularity half added by SE |
| **D-05** | ~~System requirements exist at both L1 and L2 as a "hinge" artifact~~ — **superseded by D-03.** The L1→L2 join is capability requirement → system requirement and crosses a repo boundary. | 2026-09-11 | superseded |
| **D-06** | ~~AxS removed from the architecture chain; ASAM at L0~~ — **superseded by D-01, D-02.** | 2026-09-10 | superseded |
| **D-07** | Level numbering is **not ratified org-wide.** Three schemes exist (`G3`); `G7` and `G10` are unanswered. This standard states its own numbering. | 2026-09-10 | Review `G3` |
| **D-08** | **An L2 repo decomposes into sub-systems internally by default.** One or more L3 sub-systems may be split into their own repos where complexity warrants it — **conditional on clear traceability being preserved across the split.** A split that cannot demonstrate an unbroken parent chain is not permitted. | 2026-09-13 | SE, resolving the D-01/D-03 ambiguity |
| **D-09** | **Every level carries architecture, including L0.** A level that owns boundaries must own the architecture those boundaries are drawn on; an interface defined without one is ungrounded. Architecture and interfaces are one responsibility seen from two sides. | 2026-09-13 | SE |

| **D-61** | **The tier schema is Systems-Architect-confirmed.** D-01–D-04 are ratified, not provisional. The template states the levels and tiers as the standard's own, no longer as "ours pending a reply". | 2026-09-14 | X-03 closed; SA confirmation |

## Terminology and naming

| Key | Decision | Date | Source |
|-----|----------|------|--------|
| **D-10** | Artifact prefixes follow `prak-v-model`, which follows Jama: `capreq-` `sysreq-` `compreq-` `int-` `arch-` `adr-` `uc-`. | 2026-09-10 | Conflict C1, C3 |
| **D-11** | **"Capability requirement"** replaces "product requirement" throughout. Matches Jama terminology. | 2026-09-10 | Conflict C3 |
| **D-12** | Interface artifacts use **`int-`**, not `icd-`. The catalog entry and the document it may refine to are different things. | 2026-09-10 | Conflict C1 |
| **D-13** | `platform-team` is **team-based**, not project-based. | 2026-09-10 | Review `M2` |
| **D-14** | Directories are named after **tiers, never levels**. A directory named for a level makes renumbering a migration. | 2026-09-11 | Tier schema |
| **D-15** | **Relationship direction uses Jama's vocabulary: upstream and downstream.** Upstream is toward the parent and the source need; downstream is toward derived artifacts. Note `maturity.py` retains "from M2 upward", which is magnitude (M2-and-above), not a relationship — a blind rename would have corrupted it. | 2026-09-13 | SE |

## Artifact model

| Key | Decision | Date | Source |
|-----|----------|------|--------|
| **D-20** | **Every `parent-*` field is many-to-many.** The one-parent-only model was a Jira limitation; both GitHub and Jama allow m:m. A single parent may still be written as a scalar. | 2026-09-10 | Harvest H2 |
| **D-21** | **Everything traces upstream** to a customer-defined need, safety included. A parent is required; it need not be in the same repo or level. | 2026-09-10 | Conflict C4 |
| **D-22** | Filenames, `id` and `title` are **unique**, enforced. | 2026-09-10 | Harvest H3 |
| **D-23** | Verification methods are **Test · Analysis · Inspection · Demonstration** — deliberately tighter than Jama's picklist. | 2026-09-10 | Conflict C6 |
| **D-24** | Enum vocabularies are enumerated and enforced. Enumeration is a control: the `platform-team` enum is why a rename could not land silently across 178 artifacts. | 2026-09-10 | Harvest H8 |
| **D-25** | Requirements-tool picklists (Jama) constrain the fields that map onto them. A value the tool rejects is not valid here. | 2026-09-10 | Harvest H17 |
| **D-26** | A **`param-*` artifact type** holds program-declared values, with every cited parameter required to resolve. | 2026-09-09 | Review decision 4 |
| **D-27** | The artifact model is **data** (`standard/artifact-schema.yaml`), not code. Types declare tiers; locations are derived. | 2026-09-10 | Harvest H1, option D+E |
| **D-28** | Agile planning artifacts are **not specified in the repo.** The only requirement is that work items trace back to the requirement they support, via the Jama↔Jira story-level join. | 2026-09-10 | Harvest H10 |
| **D-29** | **Links are established by the child, looking up.** The lower artifact names its parent; the parent level observes coverage rather than creating links. This is why enforcement is upstream (D-53) and coverage is a separate, later problem. | 2026-09-13 | SE |
| **D-58** | **A parameter's `Cited By` list is hand-maintained and checked, not generated.** D-46 made `TRACEABILITY.md` generated because nothing read the hand-maintained version, so nothing caught it drifting. That reasoning does not transfer once a checker reads the list: `tools/params.py` fails the build on drift in **either** direction, so hand-maintenance is honest rather than decorative. | 2026-09-13 | Phase 3 item 1.1; first defect found in `example/` |
| **D-59** | **The generated matrix is written to `traceability/TRACEABILITY.md`, not the repo root.** `axs` writes its matrix into `_registry/`; this standard keeps `traceability/` as the one place a reader looks for coverage, alongside `STANDARDS-MAPPING.md`. | 2026-09-14 | H-3, SE |
| **D-60** | **The matrix's columns are derived from `parent-*` fields, not declared.** A type with no `parent-*` field gets no column and is inventoried instead. Lineage is never inferred from a shared feature-bucket directory name: a guessed link presented as a fact is worse than a blank. | 2026-09-14 | Phase 3 item 1.2 |
| **D-62** | **A PRD is authored at both L0 and L1.** The `prd` packet is valid at either level; it is not an L0-only deliverable. The earlier observation — that every generated section draws on `stakeholder`/`product` artifacts — was true and did **not** settle the question, because L1 has a product-facing deliverable of its own. | 2026-09-14 | X-06 closed; SA |

## Format and content

| Key | Decision | Date | Source |
|-----|----------|------|--------|
| **D-30** | **Markdown is the standard table format.** HTML is legacy, accepted during transition. | 2026-09-10 | Conflict C5 |
| **D-31** | Artifact body tables are **generated from frontmatter**, not hand-authored. `prak-v-model/tools/prd_build` is a reference only; the template grows its own generator. | 2026-09-11 | Review decision 3 |
| **D-32** | Bulk HTML→Markdown conversion is executed **in reviewable chunks**, not one pass. | 2026-09-10 | Review `D1` |
| **D-33** | Diagram source format is declared per repo. `.puml` is preferred for expressiveness; Mermaid renders natively in GitHub. | 2026-09-10 | Harvest H5 |

## Maturity and identity

| Key | Decision | Date | Source |
|-----|----------|------|--------|
| **D-40** | **Maturity matches the AxS schema as baseline** — `M1 M2 M2+ M3 M4`, recorded in a `**Status:**` body header. Automation may be added **provided it does not change or conflict with that core schema.** | 2026-09-11 | Review `A4` |
| **D-41** | A maturity state **at or above M2 requires a dated promotion record** in `_registry/`. A state that cannot be raised without evidence does not drift. | 2026-09-10 | Applies D-40 |
| **D-42** | **M4 at one level requires M4 at the level above.** | 2026-09-10 | AxS gate rule |
| **D-43** | **Jama-matched short IDs are assigned at M3.** Assignment triggers a review in which **no reply equals acceptance.** | 2026-09-11 | Review decision 2 |
| **D-44** | **Jama is the source of truth and the identity authority.** Changes only on documented evidentiary justification with approval. Cross-repo identity is the Jama key, never a filename. | 2026-09-09 | Review decisions 0, 2 |
| **D-45** | Repo-local IDs stay **contiguous and unique within the repo**, with no cross-repo meaning. | 2026-09-10 | Review `C9`, `I3` |
| **D-46** | `TRACEABILITY.md` is **generated**, not hand-maintained. Nothing reads the hand-maintained matrix and no generator exists for it. | 2026-09-10 | Review `T2` |

## Governance and distribution

| Key | Decision | Date | Source |
|-----|----------|------|--------|
| **D-50** | **Convention + checklist + human review. A tool is added only where a named, counted failure demands one**, and ships with that failure recorded beside it. | 2026-09-11 | Governing principle |
| **D-51** | The template is a **versioned standard**, not a one-way copy. Every downstream repo records the version and commit it was cut from. | 2026-09-10 | Review `A7` |
| **D-52** | A repo declares which parts of the standard it implements (`repo-standard.yaml`). Omitting a tier or packet is a legitimate choice, not a gap. **Packets are only for genuinely optional content** — the level's requirement type, `interfaces` and `architecture` are core and carry no flag, because a flag that cannot be set to false is not a packet. **`maturity-gates` is required**, since maturity gates review itself. | 2026-09-13 | Conflict C10; refined by SE 2026-09-13 |
| **D-53** | **Cross-repo enforcement is upstream.** A repo declares its parent and every outbound parent reference is verified to exist upstream. Coverage (downstream) is deliberately out of scope. | 2026-09-10 | Review `A1`, `S3` |
| **D-54** | The template **applies at all levels** and draws from `axs` as well as from `prak-v-model` evolution. | 2026-09-10 | Review `D3` |
| **D-55** | **Jama TIM / relationship rules are org-admin configuration and are not mirrored in any GitHub repo.** Not viewable at SE permission level. Confirm rules with the Jama Org admin. | 2026-09-11 | SE decision |
| **D-56** | The L2 pilot repo is **`prak-embedded-core`** (formerly `polymorphous-v-model`). Template completion comes first, then the pilot. | 2026-09-10 | Review `R3`, `R7` |
| **D-57** | `prak-v-model` holds **no component tier.** | 2026-09-10 | Review `R1`, conflict C8 |

## Deferred — decided not to decide yet

| Key | Item | Owner | Unblocks when |
|-----|------|-------|---------------|
| **X-01** | One Jama project for all PRAK artifacts, or several | Erich Felger → Dallon Schofield | SE alignment reached |
| **X-02** | Jira integration standard | Erich Felger, Patrick McKee | gated by X-01 |
| ~~**X-03**~~ | ~~Systems Architect confirmation of the tier schema~~ — **resolved 2026-09-14: confirmed.** See D-61. | Erich Felger | closed |
| **X-04** | ADR, data-spec, deployment, extensions, PRD, glossary scope | Systems Architect | his discretion |
| **X-05** | Jama External ID backfill | 156 owner | blocks mechanical cross-repo traces |
| ~~**X-06**~~ | ~~Which level authors a PRD~~ — **resolved 2026-09-14: L0 and L1 both.** See D-62. | Systems Architect, Patrick McKee | closed |
