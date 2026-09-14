"""Tier README frontmatter must agree with where the README actually is.

Each tier directory's README opens with orientation frontmatter:

    ---
    artifact-type: persona
    tier: stakeholder
    ---

**Only two fields, deliberately.** `declared-by` and `owner` are real
orientation a reader wants, and both are excluded because they are maintained
elsewhere: `declared-by` in `tier-schema.md` §4, `owner` in §1. Copied into nine
READMEs they would mean a level renumbering edits nine files — undoing the
property the derived-level design exists to provide, where a renumbering is a
one-line change. The READMEs point at the tier schema instead.

The two that remain cost nothing to maintain, because neither is checked against
another document:

- `tier` is checked against the directory the README sits in. Moving the
  directory already means editing the file.
- `artifact-type` is checked against the artifact schema, and changes only if a
  type is renamed.

Note what is deliberately NOT done: none of these fields appear on an *artifact*.
An artifact's tier is its location, and storing it would repeat the mistake PRAK
made with `refinement-level` — whose own validator comment concedes the level and
the folder are "the same statement made twice," and which review item M1 records
at 49% adoption "tracking a distinction that does not exist."
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from tools.schema import load_schema

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_KEYS = {"artifact-type", "tier"}

# Maintained in standard/tier-schema.md, and only there. A README naming one of
# these has reintroduced the duplication they were removed to avoid.
FORBIDDEN_KEYS = {"declared-by", "owner", "level"}


def _tier_readmes() -> list[Path]:
    """Every README inside a declared tier directory."""
    found: list[Path] = []
    for tier in load_schema()["tiers"]:
        tier_dir = REPO_ROOT / tier
        if tier_dir.is_dir():
            found.extend(sorted(tier_dir.rglob("README.md")))
    return found


def _frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        return None
    return yaml.safe_load(match.group(1)) or {}


def _ids(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def test_at_least_one_tier_readme_exists():
    assert _tier_readmes(), "no tier READMEs found — has the tree moved?"


@pytest.mark.parametrize("path", _tier_readmes(), ids=_ids)
def test_tier_readme_has_orientation_frontmatter(path):
    fm = _frontmatter(path)
    assert fm is not None, (
        f"{_ids(path)}: no frontmatter. Every tier README opens with "
        f"artifact-type and tier."
    )
    missing = sorted(REQUIRED_KEYS - set(fm))
    assert not missing, f"{_ids(path)}: missing {missing}"


@pytest.mark.parametrize("path", _tier_readmes(), ids=_ids)
def test_tier_readme_tier_matches_its_location(path):
    """`tier:` must name the directory the README actually sits in."""
    fm = _frontmatter(path) or {}
    actual = path.relative_to(REPO_ROOT).parts[0]
    assert fm.get("tier") == actual, (
        f"{_ids(path)}: declares tier '{fm.get('tier')}' but sits in '{actual}/'"
    )


@pytest.mark.parametrize("path", _tier_readmes(), ids=_ids)
def test_tier_readme_artifact_type_is_real(path):
    """`artifact-type:` must name a type the schema actually declares."""
    fm = _frontmatter(path) or {}
    declared = fm.get("artifact-type")
    known = set(load_schema()["types"])
    assert declared in known, (
        f"{_ids(path)}: artifact-type '{declared}' is not a type in "
        f"standard/artifact-schema.yaml"
    )


@pytest.mark.parametrize("path", _tier_readmes(), ids=_ids)
def test_tier_readme_artifact_type_belongs_to_this_tier(path):
    """The type named must be one the schema allows at this tier."""
    fm = _frontmatter(path) or {}
    schema = load_schema()
    declared_type, tier = fm.get("artifact-type"), fm.get("tier")
    spec = schema["types"].get(declared_type)
    if spec is None:
        pytest.skip("artifact-type is invalid; covered by its own test")
    assert tier in spec["tiers"], (
        f"{_ids(path)}: type '{declared_type}' is not valid at tier '{tier}' "
        f"(schema allows: {spec['tiers']})"
    )


@pytest.mark.parametrize("path", _tier_readmes(), ids=_ids)
def test_tier_readme_does_not_duplicate_the_tier_schema(path):
    """Level and owner are maintained in tier-schema.md, and only there.

    Copying them here is convenient, and is exactly how a one-line renumbering
    becomes a nine-file migration.
    """
    fm = _frontmatter(path) or {}
    duplicated = sorted(FORBIDDEN_KEYS & set(fm))
    assert not duplicated, (
        f"{_ids(path)}: frontmatter carries {duplicated}, which is maintained "
        f"in standard/tier-schema.md. Point at it instead of copying it."
    )


@pytest.mark.parametrize("path", _tier_readmes(), ids=_ids)
def test_tier_readme_frontmatter_does_not_collide_with_artifact_fields(path):
    """`class` is a persona's own field; a README must not reuse the key.

    The orientation key is `artifact-type` precisely so that grepping `class:`
    finds persona artifacts and not the README describing them.
    """
    fm = _frontmatter(path) or {}
    assert "class" not in fm, (
        f"{_ids(path)}: uses 'class', which is a persona artifact field — "
        f"use 'artifact-type'"
    )


@pytest.mark.parametrize("path", _tier_readmes(), ids=_ids)
def test_tier_readme_points_at_the_tier_schema(path):
    """Having removed level and owner, a README must say where they live."""
    text = path.read_text(encoding="utf-8")
    assert "tier-schema.md" in text, (
        f"{_ids(path)}: does not reference standard/tier-schema.md, so a reader "
        f"has nowhere to find which level declares this tier or who owns it"
    )
