# Contributing

This repository holds the SA/SE artifacts for [PROJECT NAME]. Artifacts are authored as plain Markdown files; validation tooling and CI are layered on top of that artifact tree.

## Before You Start

- Read [`CLAUDE.md`](CLAUDE.md) for the artifact hierarchy, naming conventions, frontmatter requirements, and table/diagram format rules. These are enforced by CI.
- Skim [`README.md`](README.md) for the directory layout and feature buckets.
- Skim [`traceability/TRACEABILITY.md`](traceability/TRACEABILITY.md) so you understand what your artifact must link to.
- Look at [`example/`](example/) if you want to see a fully worked feature end-to-end before authoring your own.

## How to Add an Artifact

1. Copy the relevant file from `templates/` into the correct feature bucket (create the bucket directory if it doesn't exist yet).
2. Rename it using the kebab-case + prefix rules from `CLAUDE.md` (`uc-*.md`, `req-*.md`, `sysreq-*.md`, `arch-*.md`, `icd-*.md`, `data-*.md`, `deploy-*.md`, `adr-NNNN-*.md`).
3. Fill in YAML frontmatter — cross-references use **filename only** (no directory prefix).
4. Use plain Markdown table syntax, not HTML `<table>` markup.
5. Update [`traceability/TRACEABILITY.md`](traceability/TRACEABILITY.md) so your artifact appears in the matrix.
6. If your change affects which standards apply or how well they're covered, update [`traceability/STANDARDS-MAPPING.md`](traceability/STANDARDS-MAPPING.md).

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
