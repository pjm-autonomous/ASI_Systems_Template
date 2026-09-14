# Template Follow-Ups

**Open items on this template itself** — not on any project built from it, and
not on any other repo.

Anything scoped to a specific project belongs in that project's own tracking. An
item that names `prak-v-model`, `axs`, or a particular Jama project is in the
wrong file here: move it rather than carrying it.

Reviewed and triaged 2026-09-13. Nine PRAK-scoped items were moved to
`prak-v-model/TODO.md`; five were resolved by Phases 0–2; one moved into
`standard/checklists/new-repo.md` where it is actually actionable.

---

## Open — template scope

- [ ] **Ship `extensions/security/` stubs.** The lifecycle categories omit
  security engineering practice entirely, in both `extensions/` and
  `reference/bkm-document-set.md`. Shape: `security-risk-assessment.md` (threat
  model), `security-plan.md`, `vulnerability-management.md`, IEC 62443-shaped,
  following the owner-frontmatter and `STUB`-marker pattern. Update
  `extensions/README.md` and `reference/bkm-document-set.md` in the same pass.
  The gap is already surfaced in `extensions/README.md` so it is visible while
  it remains open.

- [ ] **Ship safety-analysis artifact stubs** — HARA, FMEA, safety case — with
  `owner:` frontmatter and a `STUB` marker, so missing safety-analysis evidence
  is visible in every project baseline rather than silently absent. The lesson
  behind it: a repo whose own governing safety document required an FMEA and a
  safety case to substantiate its PL claims had no artifact, no stub and no owner
  for either, anywhere.

- [ ] **Decide whether the template carries a safety-integrity field at all, and
  if so, forbid a hardcoded default.** There is currently no
  `safety-classification` or PL field in `standard/artifact-schema.yaml`, while
  `prak-v-model` has one. Two questions: does the standard need it, and where is
  its authority.

  The rule to encode either way: **never hardcode a PL/SIL default** in a
  template, a skill or a validator. The governing safety-integrity document is
  the single source, and everything else points at it. The failure this prevents
  is documented: a governing document mandated PLe/SIL 3 while a template, a
  locked decision, a validator and 36 populated fields all carried PLd — two
  authoritative sources disagreeing on the target a requirements tool would
  baseline.

- [ ] **Wire `prd/` into project startup.** Have `/new-project` walk
  `prd/meta.yaml` and section-owner assignment. Gated by **X-06** — which level
  authors a PRD is undecided, so what `/new-project` should do at L1 and L2 is
  undecided with it.

- [ ] **Revisit a docs site.** No mkdocs or GitHub Pages site ships today.
  Reconsider if projects want a browsable rendered view. Note the constraint
  recorded in the standard: a Pages site does **not** follow a repo rename, so
  any site needs an explicit `site_url` from the start.

---

## Tooling gaps

**Superseded by `standard/phase-3-harvest.md`.** That register inventories all
103 candidate tools, skills and agents across `axs` and `prak-v-model`, carries
the count behind each one, and records a disposition for every item — including
the six gaps that were listed here.

Kept as a pointer rather than a copy: the counts move as the source repos move,
and two lists of the same six items drift. The register is the single source.

**Ask before starting any of them.** Current recommendation, from the register:
the `param-*` resolution checker first.

## Repo-wide sweeps

Both run against the whole repo rather than a phase. Listed once here so they
cannot be half-done in several places.

- [ ] **Reference and path verification sweep.** Walk every cross-reference and
  path and confirm it resolves:
  - **Paths** — every directory and filename named in prose exists. The re-tier
    moved four directories and created four more. Stale paths were fixed wherever
    noticed, which is not the same as having checked.
  - **Pointers** — every "see X" resolves to a real file *and* to the section it
    claims. Several files cite `standard/tier-schema.md` §1 and §4 **by number**;
    a section renumber breaks all of them silently.
  - **Anchors** — the section list at the top of each tier README matches the
    headings below it.
  - **Deliberate exclusions** — `standard/archive/` records superseded content and
    must not be repointed; `CHANGELOG.md` describes past state.

  Worth a link checker if the manual sweep returns a meaningful count. Run the
  sweep first, so the tool is justified by a number rather than a worry.

- [ ] **Portability audit of harvested tools.** Run **after** skills and agents
  are harvested from `axs` and `prak-v-model`, not before.

  A tool that works in its home repo is not necessarily ready to deploy from a
  template. Audit each harvested skill, agent and script for:
  - **Hardcoded repo identity** — paths, repo names, Jama project IDs, team
    names, branch names, or a level baked into logic that should read
    `repo-standard.yaml`.
  - **Assumed tiers** — a tool assuming `system/requirements/` exists breaks in an
    L0 or L1 repo that declares neither. It must read the declared tiers.
  - **Assumed packets** — a tool touching an artifact type the repo opted out of.
  - **Assumed upstream** — anything assuming a parent repo exists, is readable, or
    is named a particular thing.
  - **Assumed field lists** — a tool holding its own copy of required fields
    rather than reading `standard/artifact-schema.yaml`.
  - **Environment assumptions** — an interpreter, an installed CLI, network
    access, or an authenticated connector, none of which a fresh repo has.

  The bar: an instantiated repo gets tools that **run as delivered**, at whatever
  level it declares, without editing. Anything that cannot meet that bar is fixed
  or shipped clearly marked as needing configuration — never shipped silently
  broken.

---

## Resolved

Kept with what resolved them, so a reader can tell a closed item from one that
was quietly dropped.

- [x] **Review `CLAUDE.md`** — rewritten in Phase 2 onto the re-tiered model. Its
  prose copy of every type's required fields was removed; the schema is the
  single source and the file explains how to read it.
- [x] **Build the authoring skills** — 15 skills and the `derive` agent.
  `tests/test_skills.py` fails if an artifact type is added without one.
- [x] **Jama paste format** — decided (D-30): Markdown is the standard, HTML is
  legacy, and `conventions.table-format` in `repo-standard.yaml` records what a
  given repo uses.
- [x] **Move `config/pre-commit-config.yaml` to the repo root** — done; the
  `config/` folder no longer exists.
- [x] **Feature-bucket sub-directories** — resolved as convention rather than as
  a task. Buckets are optional, created on demand, and documented in each tier
  README; `example/` shows a worked one.

## Moved

- **Nine PRAK-scoped items** → `prak-v-model/TODO.md`, 2026-09-13. PL default
  repointing, the system-requirement actions repo, PDP-08 stub content, PRD
  content-scope build changes, the Arena PLM placeholder, ISO/SAE 21434
  applicability, cybersecurity requirement modelling, the release procedure, and
  the completed AxS rating-scheme assessment.
- **"Populate `STANDARDS-MAPPING.md` per project"** → `standard/checklists/new-repo.md`.
  It was never a template task: the template ships the standards list, and
  confirming which apply is something an instantiated repo does once, which is
  what the checklist is for.
