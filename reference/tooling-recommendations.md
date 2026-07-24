# Recommended Skills, Plugins, and Connectors

Recommendations for Claude Code / Cowork tooling to use alongside this template. Scoped deliberately broad — everything here should be useful on **any** project instantiated from this template, not just ASI/PRAK-style robotics work. Do not add project-specific tool configuration (specific Jira project keys, SharePoint URLs, Slack channels) here — that belongs in the instantiated project's own `CLAUDE.md` once it exists.

Researched by checking this environment's actual MCP connector registry and plugin marketplace (2026-07-23), not just reasoning from first principles — see "What Was Checked" at the bottom.

## 1. Claude Code Skills to Build (Recommended — Not Yet Built)

No marketplace plugin does artifact-authoring for a personas → use-cases → requirements → architecture chain like this template's. `prak-v-model` (the repo this template was generalized from) solved this with bespoke `.claude/skills/` slash commands, and deferred bringing them into this template for the v1 build (see `TODO.md`). Recommendation: build them now, generalized (no PRAK-specific language), one skill per core artifact type:

| Skill | Purpose |
| --- | --- |
| `/persona` | Create or update a persona in `product/personas/` |
| `/use-case` | Create or update a use case, prompting for feature bucket |
| `/product-requirement` | Create or update a product requirement; enforce EARS format; require parent use case |
| `/system-requirement` | Create or update a system requirement; enforce EARS format; require parent product requirement |
| `/architecture` | Create or update an architecture diagram (Mermaid) |
| `/icd` | Create or update an interface control document |
| `/data-spec` | Create or update a data specification |
| `/deployment-arch` | Create or update a deployment architecture doc |
| `/adr` | Create or update an architecture decision record, auto-incrementing the `adr-NNNN` number |
| `/requirement` | EARS-format formatter/checker — converts plain language into an EARS statement without creating a file (utility, not an artifact skill) |

Plus two agents:

- **`/new-project` setup skill** — walks through renaming "template-repo" / `[PROJECT NAME]` placeholders in `README.md` and `CLAUDE.md` to the real project name right after "Use this template" is clicked. Nothing in `prak-v-model` covers this; it's new.
- **`derive` agent** — reads all artifacts plus `traceability/TRACEABILITY.md`, finds personas without use cases / use cases without requirements / requirements without decomposition, and proposes new artifacts for approval before creating files. Directly portable from `prak-v-model`'s `.claude/agents/derive.md`, generalized.

Each skill should enforce: naming convention + prefix (`CLAUDE.md`), required frontmatter fields, plain Markdown tables (not HTML), and an automatic `traceability/TRACEABILITY.md` update — mirroring what `tools/validate.py` checks, so authoring and validation never drift apart.

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

- **`docx` / `pptx` / `xlsx` / `pdf`** — use when an artifact needs to leave this repo as a stakeholder-facing deliverable: a product requirement set exported to Word for an external partner, `traceability/TRACEABILITY.md` exported to Excel for a compliance audit, an architecture diagram set exported to a PDF or slide deck for a design review. Keep the Markdown in this repo as the source of truth; treat exports as generated, disposable artifacts, not something to maintain in parallel.
- **`doc-coauthoring`** — useful for iteratively drafting the heavier documents once an `extensions/` category is no longer a stub (a Safety Management Plan or Safety Case benefits from the structured co-authoring workflow more than a single-shot generation does).

## 4. Checked, Not Recommended

- **`engineering` plugin** (marketplace: `knowledge-work-plugins`) — offers `architecture`, `system-design`, and `documentation` skills, but scoped to general software-team workflows (standups, incident response, deploy checklists) rather than SA/SE artifact authoring or traceability. Skip unless a project specifically wants those adjacent workflows alongside this template's own structure.
- No plugin found purpose-built for systems-engineering documentation, requirements traceability, or safety-case authoring — confirms the gap that this template's `extensions/` stubs and the recommended custom skills above are meant to fill.

## What Was Checked

MCP registry searches: `github`/`git`/`pull request`, `jira`/`confluence`/`atlassian`, `sharepoint`/`onedrive`/`google drive`, `slack`/`teams`. Plugin marketplace searches against `knowledge-work-plugins` for systems-engineering, requirements, architecture, diagramming, documentation, compliance, safety, and traceability keywords. Re-run these searches periodically — connector and plugin availability changes over time and isn't tied to this template's version.
