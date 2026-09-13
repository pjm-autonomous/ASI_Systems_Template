---
name: new-project
description: Set up a freshly instantiated copy of this template — replace the template-repo / [PROJECT NAME] placeholders with the real project name and walk through first-run decisions. Run once, right after "Use this template".
---

# Skill: new-project

One-time setup for a repository just created from this template. Run it right after clicking **Use this template** on GitHub. Safe to re-run: if no placeholders remain, report that setup already happened and stop.

## Instructions

1. Ask the user for:
   - The project name (as it should appear in prose and as the repo tree root label)
   - A one-paragraph description of the product/system this repo will cover

2. Find every remaining placeholder before editing anything:
   - Grep the repo for `[PROJECT NAME]` and `template-repo` (excluding `.claude/skills/`, `reference/tooling-recommendations.md`, and `example/`, which legitimately mention the template)
   - Expected hits in a fresh copy: `CLAUDE.md` (intro line), `CONTRIBUTING.md` (intro line), `README.md` (title/tree/getting-started), `repo_structure.md` (tree roots)

3. Apply the replacements:
   - `CLAUDE.md` — replace the entire first paragraph under the title with the one-paragraph description (dropping the "replace this line…" instruction and the "If you're reading this in `template-repo`…" sentence)
   - `CONTRIBUTING.md` — replace `[PROJECT NAME]` with the project name
   - `README.md` — replace `template-repo` tree-root labels and prose references with the project name; delete or check off the "Rename references…" step under **Getting Started With a New Project** so it doesn't read as still pending
   - `repo_structure.md` — replace `template-repo` tree roots with the project name

4. **Stamp the template version into `repo-standard.yaml`.** This is the step that
   makes the standard a standard rather than a convention — without it the repo has
   no record of what it was cut from and drift is undetectable (review item A7).

   Replace the three `TEMPLATE` placeholders under `standard:`:
   - `version` — read from the template's `VERSION` file (do not invent it)
   - `commit` — the template's git SHA at instantiation. If the repo was created via
     GitHub "Use this template", the template SHA is not in local history; get it with
     `gh api repos/asirobots/ASI_Systems_Template/commits/main --jq .sha`, or record
     the tag name (e.g. `v0.1.0`) if the SHA is unavailable.
   - `instantiated` — today's date, ISO format

   Then walk the user through the rest of the declaration, because the validator
   enforces exactly what it says:
   - `levels.map` — confirm the tier→level numbering, or record that it is provisional
   - `tiers` — which tiers this repo masters (`product`/`system` for a system-tier
     repo; `system`/`subsystem`/`component` for a sub-system repo)
   - `packets` — turn off anything this project will not use; omitting a packet is a
     legitimate choice, not a gap
   - `conventions.table-format` and `conventions.diagram-format`
   - `requirements-tool` — Jama project key and ID, if known

   Delete the two `VERSION` and `standard/` items from the new repo: they belong to
   the template, not to a project built from it. Their absence is how the validator
   tells a downstream repo from the template.

5. Walk the user through the remaining first-run decisions (offer, don't force):
   - Keep or delete `example/` (the worked `low-battery-return-to-dock` feature) — keeping it is harmless; it's clearly marked as fictional
   - Record standards applicability in `traceability/STANDARDS-MAPPING.md` (which standards from `reference/standards-framework.md` apply, at what rigor) — can be deferred, but note the deferral in that file
   - Install `pre-commit` locally so validation runs before every commit (see `CONTRIBUTING.md`)

6. Verify: re-grep for the placeholders (same exclusions) to confirm none remain, and run `python tools/validate.py` — it now reports the standard version it validated against, and fails if any `TEMPLATE` placeholder survives in `repo-standard.yaml`.

7. Point the user at the authoring entry point: author the first persona with `/persona`, then work down the hierarchy (`/use-case` → `/capability-requirement` → `/system-requirement`, `/architecture`, `/interface`, `/data-spec` as needed), and run the `derive` agent later to find traceability gaps.

## Do not

- Touch `example/` content, `templates/`, or `tools/` — they are project-independent
- Invent a `standard.version` or `commit` value — read them, or record the tag name and say so
- Rewrite README/CLAUDE.md sections beyond the placeholder replacements — structure and conventions stay as the template defined them
