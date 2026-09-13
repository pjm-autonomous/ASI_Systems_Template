# Contributing

This repository holds the SA/SE artifacts for [PROJECT NAME]. Artifacts are authored as plain Markdown files; validation tooling and CI are layered on top of that artifact tree.

## Governing Principle

**Convention + checklist + human review. A tool is added only where a named,
counted failure demands one.**

Agreed 2026-09-11. Every tool in this repo ships with the failure it prevents
recorded beside it. A tool encodes a decision, so a tool built before its decision
is ratified either gets rewritten or *silently becomes* the decision. Both have
happened:

| What was built | What it cost |
|---|---|
| `refinement-status` | 49% adoption, tracking a distinction that does not exist |
| `TRACEABILITY.md` | 316 rows, 316 placeholders, 0 populated, no generator, nothing reads it |
| `validate-skills` | merged and dormant |
| a `PLd` default in an export script | became the de-facto safety target, contradicting the governing document |

Against that, tools that earned their place did so by preventing a counted
failure: the `platform-team` enum exists because a rename nearly landed silently
across 178 artifacts.

**Before adding a tool, name the failure and count it.** If you cannot count it,
write a convention and a checklist instead.

## Before You Start

- Read [`CLAUDE.md`](CLAUDE.md) for the artifact hierarchy, naming conventions, frontmatter requirements, and table/diagram format rules. These are enforced by CI.
- Skim [`README.md`](README.md) for the directory layout and feature buckets.
- Read [`standard/tier-schema.md`](standard/tier-schema.md) — it is normative, and you cannot place an artifact correctly without knowing which level this repo occupies and which tiers it owns.
- Check [`repo-standard.yaml`](repo-standard.yaml) for this repo's declared level, tiers and parent repo.
- Look at [`example/`](example/) if you want to see a fully worked feature end-to-end before authoring your own.

## How to Add an Artifact

1. Confirm the tier you are authoring into is one this repo declares in `repo-standard.yaml`. If it is not, the artifact belongs in a different repo — check `standard/tier-schema.md`.
2. Copy the relevant file from `templates/` into `<tier>/<subdir>/`, creating the feature-bucket directory if you use one.
3. Rename it using the kebab-case + prefix rules from `CLAUDE.md` (`uc-*`, `prodreq-*`, `capreq-*`, `sysreq-*`, `subreq-*`, `compreq-*`, `arch-*`, `int-*`, `data-*`, `deploy-*`, `param-*`, `adr-NNNN-*`).
4. Fill in YAML frontmatter. Required fields come from `standard/artifact-schema.yaml` — not from a prose list, which drifts.
5. **Name your parent.** Everything flows upward to a customer-defined need, safety included. A parent at the level above lives in another repo; reference it by filename and the validator verifies it upward against that repo's published index.
6. Use plain Markdown table syntax, not HTML `<table>` markup.
7. **Do not edit `traceability/TRACEABILITY.md`** — it is generated from frontmatter. Hand-maintaining it is what produced the 316-row, 0-populated matrix in the row above.
8. If your change affects which standards apply or how well they're covered, update [`traceability/STANDARDS-MAPPING.md`](traceability/STANDARDS-MAPPING.md).

## A Note on Conduct

Be direct, be kind, and assume good faith in reviews — disagree with the artifact, not the author. If a review thread gets stuck, escalate to the domain reviewer or project lead rather than letting it stall in comments.

## Branching and Commits

- Branch off `main`. Use kebab-case prefixes: `feat/<topic>` for additions, `chore/<topic>` for tooling/docs, `fix/<topic>` for corrections.
- Each branch should be one focused change — prefer several small PRs over one large one.
- Commit messages: imperative mood, short subject line, body explaining **why** if the change is non-obvious.
- Do not commit secrets, generated build output, or local environment files.

## Pull Requests

- Open the PR against `main`.
- The PR template will pre-populate a checklist — fill it out honestly.
- Request review from the appropriate domain reviewer.
- CI must be green before merge — markdown lint, frontmatter validation, cross-reference resolution, and mermaid block presence on architecture files.
- Squash-and-merge is the default merge strategy; keep the final commit message clean.

## Validating Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
validate-artifacts
pytest
```

`validate-artifacts` walks the artifact tree and reports filename, frontmatter, cross-reference, and mermaid-block violations. `pytest` runs the validator's own test suite.

To lint markdown locally (requires Node):

```bash
npx markdownlint-cli2 "**/*.md"
```

### Pre-commit Hooks

The repo ships pre-commit hook configuration (see `config/pre-commit-config.yaml` — move it to the repo root as `.pre-commit-config.yaml` per `TODO.md` if that hasn't been done yet) that runs the validator, markdown lint, and basic file hygiene checks automatically before each commit.

Install once after cloning:

```bash
pip install pre-commit
pre-commit install
```

After that, the hooks run on every `git commit`. To run them across the whole repo on demand:

```bash
pre-commit run --all-files
```

## Extending Beyond the Core

When this project matures into needing safety, coding, testing, QA/CM, change/risk, or metrics documentation, open the matching folder under `extensions/`. Each stub explains what a complete document looks like per `reference/bkm-document-set.md`. Replace the stub with real content; don't delete the folder even if you decide to defer that category — leave a note explaining the deferral instead.

## Reporting Issues

Use the issue templates under "New issue":

- **Propose new artifact** — flag a gap and propose what should fill it, before authoring
- **Report artifact issue** — broken reference, wrong content, unclear wording in an existing artifact
- **Documentation issue** — README / CLAUDE / CONTRIBUTING / reference docs
- **Tooling / CI bug** — validator, CI workflow, pre-commit, mkdocs-equivalent build (n/a in v1)

For security concerns, follow [`SECURITY.md`](SECURITY.md) — do not open a public issue.
