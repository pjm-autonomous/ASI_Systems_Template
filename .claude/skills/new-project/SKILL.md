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

4. Walk the user through the remaining first-run decisions (offer, don't force):
   - Keep or delete `example/` (the worked `low-battery-return-to-dock` feature) — keeping it is harmless; it's clearly marked as fictional
   - Record standards applicability in `traceability/STANDARDS-MAPPING.md` (which standards from `reference/standards-framework.md` apply, at what rigor) — can be deferred, but note the deferral in that file
   - Install `pre-commit` locally so validation runs before every commit (see `CONTRIBUTING.md`)

5. Verify: re-grep for the placeholders (same exclusions) to confirm none remain, and run `python tools/validate.py` to confirm the repo still validates.

6. Point the user at the authoring entry point: author the first persona with `/persona`, then work down the hierarchy (`/use-case` → `/product-requirement` → `/system-requirement`, `/architecture`, `/icd`, `/data-spec` as needed), and run the `derive` agent later to find traceability gaps.

## Do not

- Touch `example/` content, `templates/`, or `tools/` — they are project-independent
- Rewrite README/CLAUDE.md sections beyond the placeholder replacements — structure and conventions stay as the template defined them
