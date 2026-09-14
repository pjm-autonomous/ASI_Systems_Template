"""Every artifact type has an authoring skill, and no skill teaches a dead rule.

Justified by a counted failure: an audit on 2026-09-13 found that 8 of 11 skills
described the pre-re-tier model, 4 artifact types had no skill at all, and every
one of the 8 instructed the author to write a row into
`traceability/TRACEABILITY.md`.

That last one is the reason this file exists rather than a review note. A skill
is executable. A stale README misleads a reader who can push back; a stale skill
produces a broken artifact and hand-edits a generated file, without anyone
reading the instruction that caused it.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from tools.schema import load_schema

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = REPO_ROOT / ".claude" / "skills"
AGENTS = REPO_ROOT / ".claude" / "agents"

# Artifact type -> skill directory. A type absent from this map fails
# `test_every_type_has_a_skill`, so adding a type forces adding a skill.
SKILL_FOR: dict[str, str] = {
    "persona": "persona",
    "use-case": "use-case",
    "product-requirement": "product-requirement",
    "capability-requirement": "capability-requirement",
    "system-requirement": "system-requirement",
    "subsystem-requirement": "subsystem-requirement",
    "component-requirement": "component-requirement",
    "architecture": "architecture",
    "interface": "interface",
    "data-specification": "data-spec",
    "deployment-architecture": "deployment-arch",
    "param": "parameter",
    "adr": "adr",
}

# Directories that were moved by the re-tier. A skill naming one sends an author
# to a path that does not exist.
DEAD_PATHS = (
    "product/personas/",
    "product/use-cases/",
    "system/architecture/",
    "system/interfaces/",
)

# Fields the re-tier removed from the types that used to carry them.
DEAD_FIELDS = ("owning-component", "consumers:")


def _authoring_docs() -> list[Path]:
    return sorted(SKILLS.glob("*/SKILL.md")) + sorted(AGENTS.glob("*.md"))


def _ids(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def test_every_type_has_a_skill():
    missing = sorted(set(load_schema()["types"]) - set(SKILL_FOR))
    assert not missing, (
        f"artifact types with no authoring skill: {missing} — add one under "
        f".claude/skills/ and register it in SKILL_FOR"
    )


@pytest.mark.parametrize("type_name,skill", sorted(SKILL_FOR.items()))
def test_mapped_skill_exists(type_name, skill):
    assert (SKILLS / skill / "SKILL.md").is_file(), (
        f"skill '{skill}' is mapped to type '{type_name}' but does not exist"
    )


@pytest.mark.parametrize("path", _authoring_docs(), ids=_ids)
def test_skill_does_not_write_the_generated_matrix(path):
    """TRACEABILITY.md is generated (D-46). A skill must not write to it."""
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if "TRACEABILITY.md" not in line:
            continue
        lowered = line.lower()
        instructs = any(
            verb in lowered
            for verb in ("update ", "add a new row", "fill the", "append", "write")
        )
        forbids = any(
            word in lowered for word in ("do not", "never", "generated")
        )
        assert not (instructs and not forbids), (
            f"{_ids(path)}: instructs an author to write the generated matrix:\n"
            f"  {line.strip()}"
        )


@pytest.mark.parametrize("path", _authoring_docs(), ids=_ids)
def test_skill_names_no_dead_path(path):
    text = path.read_text(encoding="utf-8")
    found = [p for p in DEAD_PATHS if p in text]
    assert not found, (
        f"{_ids(path)}: names {found}, which the re-tier moved — an author "
        f"following this writes to a directory that does not exist"
    )


@pytest.mark.parametrize("path", _authoring_docs(), ids=_ids)
def test_skill_names_no_removed_field(path):
    text = path.read_text(encoding="utf-8")
    found = [f for f in DEAD_FIELDS if f in text]
    assert not found, (
        f"{_ids(path)}: names {found}, which no type carries any more"
    )


@pytest.mark.parametrize("path", _authoring_docs(), ids=_ids)
def test_skill_does_not_restate_a_priority_scheme(path):
    """Enum values live in the schema; a skill offering its own list drifts."""
    text = path.read_text(encoding="utf-8")
    assert not re.search(r"`Critical`.*`High`.*`Medium`", text), (
        f"{_ids(path)}: restates a priority scheme the schema does not use — "
        f"read the enum from standard/artifact-schema.yaml instead"
    )
