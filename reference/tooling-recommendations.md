`./reference/tooling-recommendations.md`
Author: Patrick McKee
Company: Autonomous Solutions, Inc.
Creation Date: 2026-07-24
Modification Date: --

# Recommended Skills, Plugins, and Connectors

Recommendations for Claude Code / Cowork tooling to use alongside this template.

## Scope

The spectrum of recommendations is deliberately broad. Each should be useful in any project instantiated from this template.

<u>Do not</u> add *project-specific* tools or configurations (e.g., Jira project keys, SharePoint URLs, Slack channels) to this repository. Those should only be added after creating a new repository based on this template. A new project's `CLAUDE.md` or `README.md` file is an appropriate place to reference those, if needed.

## Sources

Recommended tools were researched by checking actual MCP connector registry and plugin marketplace on 2026-07-23. This provided a broad selection that should encompass any project needs without limiting usefulness of this template repository.
Refer to "Tool Search Parameters" below for a list of strings used to identify useful tools.

## 1. Claude Code Skills (Built — `.claude/skills/`)

No marketplace plugin was discovered  for authoring Systems Architecture artifacts. A hierarchy of persona >> use-case >> capability requirement >> system requirement is not unique, so an ASI specific plugin may be built. The `prak-v-model` repository, used as a general reference for this template, contained `.claude/skills/` slash commands. Those were incorporated into this template on its creation date, generalized (no PRAK-specific language, plain Markdown tables, this template's priority and diagram-type enums). One skill per core artifact type, shipped in `.claude/skills/` so every project instantiated from the template inherits them:

| Skill | Purpose |
| --- | --- |
| `/persona` | Create or update a persona in `stakeholder/personas/` |
| `/use-case` | Create or update a use case; require parent persona(s) |
| `/capability-requirement` | Create or update a capability requirement; enforce EARS; require parent **product** requirement, which lives in the L0 repo |
| `/system-requirement` | Create or update a system requirement; enforce EARS; require parent capability requirement, which lives in the L1 repo |
| `/architecture` | Create or update an architecture diagram |
| `/interface` | Create or update an interface catalog entry; require `producer` and `consumer` at this level's immediate descendants |
| `/data-spec` | Create or update a data specification |
| `/deployment-arch` | Create or update a deployment architecture doc |
| `/adr` | Create or update an architecture decision record, allocating the next repo-wide `adr-NNNN` |
| `/requirement` | EARS formatter — converts plain language into an EARS statement without creating a file (utility, not an artifact skill) |

| `/product-requirement` | Create or update a product requirement; performance and safety share this type, distinguished by `requirement-type` |
| `/subsystem-requirement` | Create or update a sub-system requirement; parent resolves locally |
| `/component-requirement` | Create or update a component requirement; the lowest tier, and the one that owes a verification test case |
| `/parameter` | Create or update a `param-*.md` — the type that makes a cited bound verifiable |

Plus two more:

- **`/new-project` setup skill** — walks through renaming "template-repo" / `[PROJECT NAME]` placeholders in `README.md` and `CLAUDE.md` to the real project name right after "Use this template" is clicked, then the remaining first-run decisions (keep/delete `example/`, `STANDARDS-MAPPING.md`, pre-commit install). Nothing in `prak-v-model` covered this; it's new.
- **`derive` agent** (`.claude/agents/derive.md`) — reads all artifacts, finds personas without use cases, use cases without requirements, requirements without decomposition, and proposes new artifacts for approval before any files are created. Ported from `prak-v-model`'s `.claude/agents/derive.md`, generalized and extended down the hierarchy.

Each skill enforces: naming convention and prefix, the required frontmatter
fields **as declared in `standard/artifact-schema.yaml`** rather than from a list
held in the skill, plain Markdown tables, and a `tools/validate.py` run at the
end of every authoring flow — so authoring and validation cannot drift apart.

A skill does **not** update `traceability/TRACEABILITY.md`. The matrix is
generated from frontmatter (D-46); a skill writing rows into it would reintroduce
the hand-maintenance that produced a 316-row, 0-populated matrix in the repo this
standard learned from. `.claude/skills/architecture/SKILL.md` is additionally the single source for the repo's Mermaid conventions (pinned light theme, node color classes, shape conventions, syntax gotchas).

## 2. MCP Connectors Worth Connecting

Checked against this environment's connector registry directly (not assumed):

| Connector | Status Here | When It's Worth Connecting |
| --- | --- | --- |
| **Atlassian Rovo** (Jira + Confluence) | Already connected | If a project mirrors `traceability/` items into Jira issues/epics, or publishes `reference/` material to a Confluence space for non-technical stakeholders |
| **Microsoft 365** (SharePoint / OneDrive / Teams) | Available, not connected | Directly relevant here — `reference/standards-framework.md` cites ASI's SharePoint-hosted Standards Hub as the source of full standard texts. Connecting lets Claude actually open and quote the current text instead of relying on the condensed summaries in this repo |
| **Google Drive** | Available, not connected | Alternative to Microsoft 365 if a project's supporting docs live in Drive instead |
| **Figma** | Available, not connected | Only relevant if a project has UI or hardware/CAD design context that architecture diagrams need to cross-reference; skip for pure back-end/embedded projects |
| GitHub (issues/PRs) | **No dedicated connector found** in this environment's registry | For GitHub interaction, use `git`/`gh` CLI directly (as we did to push this repo) rather than expecting an MCP connector — none is currently available here |

## 3. Built-In Skills (Already Available, No Install Needed)

These ship with Claude/Cowork generally and need no connector setup:

- **`docx` / `pptx` / `xlsx` / `pdf`** — use when an artifact needs to leave this repo as a stakeholder-facing deliverable: a capability requirement set exported to Word for an external partner, `traceability/TRACEABILITY.md` exported to Excel for a compliance audit, an architecture diagram set exported to a PDF or slide deck for a design review. Keep the Markdown in this repo as the source of truth; treat exports as generated, disposable artifacts, not something to maintain in parallel.
- **`doc-coauthoring`** — useful for iteratively drafting the heavier documents once an `extensions/` category is no longer a stub (a Safety Management Plan or Safety Case benefits from the structured co-authoring workflow more than a single-shot generation does).

## 4. Checked, Not Recommended

- **`engineering` plugin** (marketplace: `knowledge-work-plugins`) — offers `architecture`, `system-design`, and `documentation` skills, but scoped to general software-team workflows (standups, incident response, deploy checklists) rather than SA/SE artifact authoring or traceability. Skip unless a project specifically wants those adjacent workflows alongside this template's own structure.
- No plugin found purpose-built for systems-engineering documentation, requirements traceability, or safety-case authoring — confirms the gap that this template's `extensions/` stubs and the recommended custom skills above are meant to fill.

## Tool Search Parameters

MCP registry searches: `github`/`git`/`pull request`, `jira`/`confluence`/`atlassian`, `sharepoint`/`onedrive`/`google drive`, `slack`/`teams`. Plugin marketplace searches against `knowledge-work-plugins` for systems-engineering, requirements, architecture, diagramming, documentation, compliance, safety, and traceability keywords. Re-run these searches periodically — connector and plugin availability changes over time and isn't tied to this template's version.
