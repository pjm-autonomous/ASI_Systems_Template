"""No Jira identifier may enter this repo.

Decided at the PRAK architecture review as item **X3** — "`jira-key` frontmatter
not yet landed: remove from `ASI_Systems_Template`" — and recorded here as D-63.

The field was proposed and never landed, which is exactly the state a guard is
for. There is nothing to remove; there is something to keep out. Traceability
between a requirement and the work that implements it runs **Jama-side**: a Jama
User Story is created from a Jama requirement, the sync creates it in Jira, and
the Jira story carries a `Jama URL` field pointing back. The repo is not part of
that chain and must not pretend to be.

Why a test rather than a note. A `jira-key` field is the obvious thing to reach
for the first time someone wants to see a requirement's sprint status, and it
would look helpful. Every artifact carrying one becomes a copy of a link that
Jama already owns and Jira already renders, drifting the moment an issue is moved
or a project re-keyed — and D-64 removes the Jira layer above the story, so some
of those keys would point at work items that no longer exist.

`Jama URL` is deliberately not forbidden: it is a **Jira-side** field. This guard
covers what lives in the repo.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Frontmatter keys that would carry a Jira identifier into an artifact.
FORBIDDEN_KEYS = ("jira-key", "jira_key", "jira-id", "jira_id", "jira-issue")

# A bare Jira issue key: PROJ-123. Matched only in frontmatter, where it would be
# a machine-read identifier; prose may legitimately discuss one.
JIRA_KEY_VALUE = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")

SKIP_DIRS = {".git", "node_modules", ".venv", "site", "__pycache__", "standard"}


def _markdown_files() -> list[Path]:
    """Every tracked Markdown file except the decision register.

    `standard/` is excluded because `decisions.md` must be able to name the field
    it forbids — a register that cannot state a decision is useless.
    """
    found: list[Path] = []
    for path in REPO_ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        found.append(path)
    return sorted(found)


def _ids(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def _frontmatter_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    return match.group(1).splitlines() if match else []


@pytest.mark.parametrize("path", _markdown_files(), ids=_ids)
def test_no_jira_key_field(path: Path):
    lines = _frontmatter_lines(path)
    for line in lines:
        key = line.split(":", 1)[0].strip().lstrip("- ").casefold()
        assert key not in FORBIDDEN_KEYS, (
            f"{_ids(path)}: frontmatter carries '{key}'. No Jira identifier "
            f"belongs in this repo (D-63) — traceability is story-to-requirement "
            f"in Jama, and the Jira story links back via its `Jama URL` field."
        )


@pytest.mark.parametrize("path", _markdown_files(), ids=_ids)
def test_no_bare_jira_issue_key_in_frontmatter(path: Path):
    """Catches the same thing smuggled in under a differently-named key."""
    for line in _frontmatter_lines(path):
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip().strip("\"'")
        if not value or "url" in key.casefold():
            continue
        assert not JIRA_KEY_VALUE.match(value), (
            f"{_ids(path)}: frontmatter '{key.strip()}' holds '{value}', which "
            f"is shaped like a Jira issue key (D-63)."
        )


def test_the_schema_declares_no_jira_field():
    """The artifact model itself must not offer one."""
    text = (REPO_ROOT / "standard" / "artifact-schema.yaml").read_text(
        encoding="utf-8"
    )
    lowered = text.casefold()
    for key in FORBIDDEN_KEYS:
        assert key not in lowered, (
            f"standard/artifact-schema.yaml declares '{key}' — removed by "
            f"review item X3 and forbidden by D-63"
        )
