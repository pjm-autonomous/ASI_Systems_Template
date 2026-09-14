# Project Context for AI Assistants

Artifact repository for **[PROJECT NAME]** — replace this line with a one-paragraph description of the product/system this repo covers. If you're reading this in `template-repo` itself rather than an instantiated project, see `README.md` first — this file assumes the template has already been used to create a real project.

This file is written for Claude (or another AI assistant) working in this repo. A human contributor should read `README.md` and `CONTRIBUTING.md` first; this file adds machine-actionable detail on top of those.

## What This Repo Is

A traceability chain of SA/SE artifacts — personas, use cases, requirements, architecture, interfaces, data, deployment, and decisions — plus extension points for the rest of the SE lifecycle (safety, coding, testing, QA/CM, change/risk, metrics) that get filled in as the project matures. See `README.md` for the full directory tree and `reference/bkm-document-set.md` for what a mature version of each extension category looks like.

## Governing Principle

**Convention + checklist + human review. A tool is added only where a named,
counted failure demands one** (agreed 2026-09-11). Every tool ships with the
failure it prevents recorded beside it. Before proposing tooling, name the failure
and count it; if you cannot count it, write a convention and a checklist instead.
See `CONTRIBUTING.md` for the record of what this rule is reacting to.

## Artifact Hierarchy

> **`standard/tier-schema.md` is normative** for levels, tiers, ownership and
> interface authority, and carries the architecture diagram. This section
> summarises it; where they disagree, the tier schema wins.

**One repo is one level** (D-01). Which level *this* repo occupies, and which
tiers it masters, are declared in `repo-standard.yaml` — not inferred from the
directory tree, and never encoded in a directory name (D-14).

```text
L0   stakeholder   personas · use cases
     product       product performance + safety requirements
       │                                    owns interfaces BETWEEN L1 systems
       ▼  crosses a repo boundary
L1   capability    capability requirements
       │                                    owns interfaces BETWEEN L2 systems
       ▼  crosses a repo boundary
L2   system        system requirements
       └─ subsystem   sub-system requirements
            └─ component   component requirements
                                            owns interfaces BETWEEN L3..n
```

Three things follow, and each contradicts a model this template used to carry:

- **A system requirement is an L2 artifact and only an L2 artifact** (D-03).
  It is not a child of a product requirement in the same repo.
- **Every level-to-level link crosses a repository boundary.** Those parents
  cannot be resolved locally; they are brokered upstream against the parent repo's
  published index (D-53).
- **Links are established by the child, looking up** (D-29). The lower artifact
  names its parent; the parent level observes coverage rather than creating links.

**Interfaces and architecture exist at every level** (D-09), including L0, and are
core rather than optional — a flag you cannot set to false is not a packet (D-52).
An interface is owned by the nearest common ancestor of the parties it connects
and is stated in terms of that owner's **immediate descendants** (D-04): an L1
interface says *System A ↔ System B* even when the traffic is between sub-systems
inside them.

## Directory Structure

Paths are `<tier>/<subdir>/`, computed from the schema — a tier directory only
exists if `repo-standard.yaml` declares that tier.

| Directory | Contains |
| --- | --- |
| `stakeholder/personas/`, `stakeholder/use-cases/` | L0 — who the system serves and what they need |
| `product/requirements/` | L0 — product performance and safety requirements |
| `capability/requirements/` | L1 — capability requirements |
| `system/`, `subsystem/`, `component/` `requirements/` | L2 — the engineering decomposition |
| `interfaces/` | the boundaries **this** level owns |
| `architecture/` | what those boundaries are drawn on |
| `<tier>/decisions/`, `<tier>/parameters/`, `<tier>/data/`, `<tier>/deployment/` | ADRs, program-declared values, data specs, deployment topology |
| `standard/` | **the standard itself** — decisions, tier schema, artifact schema, plan, checklists |
| `_registry/` | maturity promotion evidence (D-41) |
| `repo-standard.yaml` | this repo's level, tiers, packets, parents and provenance |
| `prd/` | PDP-08 PRD section stubs — see `prd/README.md` |
| `templates/` | canonical blank starting point for each artifact type |
| `example/` | one fictional feature worked end-to-end, for reference |
| `extensions/` | safety, coding, testing, QA/CM, change/risk, metrics — see `extensions/README.md` |
| `reference/` | BKM document set, standards framework, tooling recommendations |
| `traceability/` | `TRACEABILITY.md` (**generated**, D-46) and `STANDARDS-MAPPING.md` |
| `glossary/` | shared terminology |
| `tools/`, `tests/` | validator, schema loader, maturity, broker, parameter resolution, traceability generator, and their tests |
| `.claude/` | authoring skills and the `derive` gap-analysis agent |

Feature buckets (an optional directory level inside a tier's subdir) are
kebab-case and chosen by the author. Reuse an existing bucket when content fits.

## Naming Conventions

| Artifact | Pattern | Example |
| --- | --- | --- |
| Persona | `<role-or-team>.md` | `remote-operator.md` |
| Use case | `uc-<description>.md` | `uc-geofence-breach-alert.md` |
| Product requirement | `prodreq-<description>.md` | `prodreq-geofence-alert-latency.md` |
| Capability requirement | `capreq-<description>.md` | `capreq-geofence-enforcement.md` |
| System requirement | `sysreq-<description>.md` | `sysreq-geofence-check-interval.md` |
| Sub-system requirement | `subreq-<description>.md` | `subreq-geofence-map-load.md` |
| Component requirement | `compreq-<description>.md` | `compreq-map-validator-checksum.md` |
| Architecture diagram | `arch-<description>.md` | `arch-geofence-alert-flow.md` |
| Data specification | `data-<description>.md` | `data-geofence-zone-schema.md` |
| Deployment architecture | `deploy-<description>.md` | `deploy-geofence-service-topology.md` |
| Interface catalog entry | `int-<description>.md` | `int-geofence-alert-api.md` |
| Program parameter | `param-<description>.md` | `param-geofence-eval-interval.md` |
| Architecture decision record | `adr-NNNN-<description>.md` | `adr-0001-geofence-service-boundary.md` |

All names use kebab-case. Cross-references in frontmatter use the **filename only**, no directory prefix — `tools/validate.py` resolves them by matching filenames within the correct artifact-type glob, not by path.

## Table Format

All artifact tables use **plain Markdown table syntax** — not HTML `<table>` markup. Keep cells short; move long prose into paragraphs below the table rather than cramming it into a cell.

## Frontmatter Requirements

Every artifact opens with YAML frontmatter (`---` delimited). **The required
fields are defined in `standard/artifact-schema.yaml`, not here.** That file is
the artifact model; this one summarises how to read it.

Do not restate a type's field list in prose anywhere in this repo. A prose copy
is a second source of truth that drifts silently — this very section previously
described an interface as requiring `parent-capability-requirements`,
`owning-component` and `consumers`, none of which had been true since the model
was re-tiered.

To see what a type requires:

```bash
python -c "import sys; sys.path.insert(0,'.'); from tools.schema import *;   print([ (b.label, b.required_fields) for b in build_bindings(load_schema()) ])"
```

Field families, so the schema reads clearly:

| Family | Meaning |
| --- | --- |
| `parent-*` | the artifact this one derives from. Always many-to-many capable (D-20); a single parent may be written as a plain scalar. |
| `parent-*` resolved **locally** | the target is in this repo and must exist |
| `parent-*` resolved **externally** | the target is in the parent repo — shape-checked here, verified upstream against the parent's published index (D-53) |
| enum fields | constrained to a vocabulary declared once in the schema and enforced (D-24) |
| `producer` / `consumer` | an interface's two parties, named at the owning level's **immediate descendants** (D-04) |

`tools/validate.py` additionally checks filename pattern, cross-reference
resolution, uniqueness of filename/`id`/`title` (D-22), and that architecture
files contain a diagram block.

**Parameter resolution** (`tools/params.py`, gated on the `params` packet):
every `param-*.md` cited from any artifact body must exist and must carry a real
value — a placeholder such as `TBD` fails exactly as a dangling citation does,
because a citation resolving to a placeholder is no better than one resolving to
nothing. A parameter's `Cited By` list is checked against the actual citations in
both directions (D-58). A bare number in a requirement statement is deliberately
**not** flagged: detecting "this digit should have been a parameter" needs a
heuristic, and a heuristic on requirement prose produces false positives at a
rate that gets the whole check ignored.

## Diagram Format

Architecture diagrams use Mermaid inside a fenced ` ```mermaid ` block, accompanied by a short Markdown table (Purpose, Scope, Notes). One diagram per file, so each file maps to a single reviewable unit.

## Extension Folders

`extensions/` holds stub documents for the parts of the SE lifecycle not authored at kickoff: safety, coding, testing, QA/CM, change/risk, and metrics (see `reference/bkm-document-set.md` for the full rationale per category). When you author real content for a stub, keep the filename stable so existing links keep working. If a category is deliberately deferred rather than authored, say so explicitly in the stub — who decided, why, when it'll be revisited — rather than leaving it silently empty.

## Standards

`reference/standards-framework.md` lists cross-industry standards (IEC 60204-1, ISO 13849-1/IEC 62061, ISO 26262, ISO 12207, ASPICE PAM 4.0, ISO 9001 §8.3, MISRA C/C++, IEC 62443, ISO/IEC/IEEE 15288/29148/42010/24765, ISO 10218-1/-2, ANSI/A3 R15.06, ISO 3691-4, ISO 21448/SOTIF, ISO/SAE 21434, ISO 31000) with scoring rubrics where available. Not every standard applies to every project — `traceability/STANDARDS-MAPPING.md` is where a project records its actual applicability decisions. Default to "engineering reference" language; only call a standard a "compliance obligation" if that is genuinely the project's posture.

## Tooling and Skills

Artifact authoring goes through the skills in `.claude/skills/` — one per artifact type (`/persona`, `/use-case`, `/capability-requirement`, `/system-requirement`, `/architecture`, `/interface`, `/data-spec`, `/deployment-arch`, `/adr`), plus `/requirement` (EARS formatter, no file output) and `/new-project` (one-time template setup). Skills exist for every artifact type; `tests/test_skills.py` fails if a type is added without one. Prefer invoking the matching skill over authoring an artifact by hand: each one enforces the conventions in this file and runs `tools/validate.py`. The `derive` agent (`.claude/agents/derive.md`) finds traceability gaps and proposes new artifacts without creating files. `.claude/skills/architecture/SKILL.md` is the single source for Mermaid conventions (theme directive, node color classes, shapes, gotchas).

`reference/tooling-recommendations.md` additionally covers MCP connectors worth connecting for a given project (Atlassian, Microsoft 365, Google Drive) and built-in document-export skills (docx/pptx/xlsx/pdf) for turning artifacts into stakeholder-facing deliverables. Check it before assuming a capability needs to be built from scratch.

## Traceability

`traceability/TRACEABILITY.md` is **generated from frontmatter, not
hand-maintained** (D-46). Do not edit it by hand and do not ask an author to
update it when adding an artifact — a hand-maintained matrix is what produced 316
rows, 316 placeholders and 0 populated entries in the repo this standard learned
from.

Coverage is observed downstream; links are established upstream (D-29). An artifact
declares its parent, and the matrix is derived from those declarations.

`build-traceability` regenerates it; `build-traceability --check` writes nothing
and asks whether the tracked file is still what the generator would emit. Both CI
and a pre-commit hook run the check, because **currency is a separate failure from
correctness** — a matrix that was right last month and has not been regenerated
passes every other check in this repo.

**Columns are derived, not chosen** (D-60): they follow `parent-*` fields through
the schema. Architecture, ICDs, data specifications, ADRs, deployment architecture
and parameters declare no `parent-*` field, so they get no column and are
inventoried under *Artifacts with no declared lineage* instead. Lineage is never
inferred from a shared feature-bucket directory name — a guessed link presented as
a fact is worse than a blank.

Cross-repo links are verified against the parent repo's published
`artifact-index.json` — run `emit-artifact-index` in a repo to make it resolvable
by its children.

## Maturity

Artifacts carry a maturity state in a `**Status:**` body header, matching the AxS
scheme as baseline (D-40): `M1 M2 M2+ M3 M4`. Automation may be added around it
but must not change or conflict with that core schema.

- A state **at or above M2 requires a dated promotion record** in `_registry/`
  (D-41). A state that cannot be raised without evidence does not drift.
- **M4 at one level requires M4 at the level above** (D-42).
- **Jama-matched short IDs are assigned at M3** (D-43), and assignment triggers a
  review in which no reply equals acceptance.

Maturity gating is enabled per repo via `packets.maturity-gates`.
