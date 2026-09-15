"""A skill declares `name` and `description`. Nothing else.

**Only these two are read.** The invocation gate requires a `name` matching the
directory and a non-empty `description` under 1024 characters, and it reads
nothing else. Every other frontmatter key is inert.

That is what makes extra keys worse than useless. `trigger_words`, `keywords` and
`tags` *look* like they control when a skill fires. They do not. Someone adds a
keyword, expects the skill to trigger on it, and nothing changes — a silent
failure with no error to notice. The trigger vocabulary belongs in the
`description`, which is the text actually consulted.

The counted inconsistency, from the 19 skills in the harvest pool: 16 declare
`name` + `description`; three declare more, and **no two of the three agree** —

    name description tags keywords author version created
    name title version tier trigger_words description
    name alias version author tier scope trigger_words description

Three schemes, three skills, zero overlap. Nothing can consume a convention that
inconsistent, which is the other half of the argument: even a reader cannot rely
on them.

Version and authorship are excluded for a separate reason (D-69): git history
and `CHANGELOG.md` already carry them, and a hand-maintained `version:` that
nobody bumps on edit is worse than no version at all — it asserts something false.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = REPO_ROOT / ".claude" / "skills"

ALLOWED_KEYS = {"name", "description"}

# The invocation gate's limits.
NAME_LIMIT = 64
DESCRIPTION_LIMIT = 1024


def _skills() -> list[Path]:
    return sorted(SKILLS.glob("*/SKILL.md"))


def _ids(path: Path) -> str:
    return path.parent.name


def _frontmatter(path: Path) -> dict:
    match = re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    assert match, f"{_ids(path)}: SKILL.md does not open with YAML frontmatter"
    return yaml.safe_load(match.group(1)) or {}


@pytest.mark.parametrize("path", _skills(), ids=_ids)
def test_only_name_and_description(path: Path):
    extra = sorted(set(_frontmatter(path)) - ALLOWED_KEYS)
    assert not extra, (
        f"{_ids(path)}: frontmatter declares {extra}. Only 'name' and "
        f"'description' are read (D-68); anything else is inert metadata that "
        f"looks functional. Put trigger vocabulary in the description."
    )


@pytest.mark.parametrize("path", _skills(), ids=_ids)
def test_name_matches_directory(path: Path):
    name = _frontmatter(path).get("name")
    assert isinstance(name, str) and name.strip(), f"{_ids(path)}: 'name' is empty"
    assert len(name) <= NAME_LIMIT, f"{_ids(path)}: 'name' exceeds {NAME_LIMIT} chars"
    assert name == path.parent.name, (
        f"{_ids(path)}: frontmatter 'name' is '{name}' but the directory is "
        f"'{path.parent.name}'. The upload gate matches the two, so a skill "
        f"known by one name in its directory, another in its frontmatter and a "
        f"third in the documentation is a skill nobody can reliably invoke."
    )


@pytest.mark.parametrize("path", _skills(), ids=_ids)
def test_description_is_present_and_within_budget(path: Path):
    desc = _frontmatter(path).get("description")
    assert isinstance(desc, str) and desc.strip(), (
        f"{_ids(path)}: 'description' is empty — it is the only text consulted "
        f"when deciding whether to invoke this skill"
    )
    assert len(desc) <= DESCRIPTION_LIMIT, (
        f"{_ids(path)}: 'description' is {len(desc)} characters, over the "
        f"{DESCRIPTION_LIMIT} limit"
    )


def test_the_guard_covers_every_skill():
    assert _skills(), ".claude/skills/ has no SKILL.md - the guard scans nothing"
