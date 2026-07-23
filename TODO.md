# Template Follow-Ups

Known open items on this template itself (not on any project built from it). Resolve or consciously re-defer each before treating the template as final.

- [ ] Review `CLAUDE.md`. Generalized from `prak-v-model` in a first pass; needs a dedicated review to confirm it's accurate and sufficient without the Claude Code skills/agents that `prak-v-model` relies on.
- [ ] Revisit Claude Code skills/agents. Explicitly out of scope for v1 of this template (2026-07-22 decision) to keep the initial build simple. Reconsider once the core structure has been used on a real project — `/persona`, `/use-case`, `/requirement`, etc. slash-command skills meaningfully reduced authoring friction in `prak-v-model`.
- [ ] Revisit a docs site. No mkdocs/GitHub Pages site in v1. Reconsider if projects built from this template want a browsable rendered view like `prak-v-model` has.
- [ ] Revisit Jama (or equivalent) paste format. v1 uses plain Markdown tables. If a project needs to paste artifacts into a requirements-management tool's rich text editor, HTML `<table>` markup may be needed again for that project — decide per-project rather than reintroducing it here by default.
- [ ] Populate `traceability/STANDARDS-MAPPING.md` per project. The template ships the standard list; each project should confirm which standards actually apply and at what rigor (see `reference/standards-framework.md`'s "ASI Compliance Posture" section).
- [x] Move `config/pre-commit-config.yaml` to the repo root as `.pre-commit-config.yaml`. The tooling that built this template can't write files named `.pre-commit-config.yaml` directly (protected-filename restriction), so the real content is parked at `config/pre-commit-config.yaml` — move and rename it by hand, then delete the `config/` folder.
-[ ] Add sub-directories in `product/` and `system/` as kebab-case. Create for use cases and requirements. See `example/` for what a fully worked feature bucket looks like end-to-end.
