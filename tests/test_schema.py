"""Tests for tools/schema.py — the schema loader and tier-binding resolver.

These pin the two properties the design exists for:
  1. Levels are derived, so renumbering the architecture touches one table.
  2. A type spanning tiers resolves different parents per tier, which a flat
     list of globs cannot express.
"""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

import pytest
import yaml

from tools import schema as sch

MINIMAL = {
    "schema-version": 1,
    "tiers": ["product", "system", "subsystem"],
    "enums": {"priority": ["Must Have", "Could Have"]},
    "types": {
        "widget": {
            "packet": "core",
            "tiers": ["product"],
            "subdir": "widgets",
            "prefix": "wid-",
            "required": ["id", "title"],
            "enums": {"priority": "priority"},
        }
    },
}


def _write(tmp_path: Path, data: dict) -> Path:
    p = tmp_path / "artifact-schema.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    return p


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def test_loads_minimal_schema(tmp_path):
    data = sch.load_schema(_write(tmp_path, MINIMAL))
    assert data["schema-version"] == 1


def test_missing_file_raises_schema_error(tmp_path):
    with pytest.raises(sch.SchemaError, match="not found"):
        sch.load_schema(tmp_path / "nope.yaml")


@pytest.mark.parametrize("missing", ["schema-version", "tiers", "types"])
def test_missing_required_key_raises(tmp_path, missing):
    data = {k: v for k, v in MINIMAL.items() if k != missing}
    with pytest.raises(sch.SchemaError, match=missing):
        sch.load_schema(_write(tmp_path, data))


def test_malformed_yaml_raises(tmp_path):
    p = tmp_path / "artifact-schema.yaml"
    p.write_text("types: [unclosed\n", encoding="utf-8")
    with pytest.raises(sch.SchemaError):
        sch.load_schema(p)


# --------------------------------------------------------------------------
# Tier-derived paths
# --------------------------------------------------------------------------

def test_glob_is_derived_from_tier_and_subdir():
    """No path is ever written in the schema; it is computed."""
    b = sch.build_bindings(MINIMAL)[0]
    assert b.glob == ("product/widgets/**/wid-*.md",)


def test_no_level_numbers_anywhere_in_the_schema():
    """Levels live only in repo-standard.yaml, so a renumber is one edit.

    If a level token ever appears in the shipped schema, the derived-level
    property is broken and a renumbering becomes a migration again.
    """
    text = sch.SCHEMA_PATH.read_text(encoding="utf-8")
    # Strip whole-line AND trailing comments. A comment may name a level for the
    # reader's benefit; the guard is that no level appears in the data itself,
    # because data is what would make a renumbering a migration.
    body = "\n".join(
        re.sub(r"#.*$", "", line)
        for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )
    for token in ("L0", "L1", "L2", "L3", "L4"):
        assert token not in body, f"level token {token} leaked into the schema"


def test_undeclared_tiers_are_not_validated():
    assert sch.build_bindings(MINIMAL, repo_tiers=["system"]) == ()
    assert len(sch.build_bindings(MINIMAL, repo_tiers=["product"])) == 1


def test_none_tiers_means_all_tiers():
    assert len(sch.build_bindings(MINIMAL, repo_tiers=None)) == 1


# --------------------------------------------------------------------------
# One binding per (type, tier) — the reason for the design
# --------------------------------------------------------------------------

def test_multi_tier_type_yields_one_binding_per_tier():
    data = dict(MINIMAL)
    data["types"] = {
        "thing": {
            "tiers": ["product", "system", "subsystem"],
            "subdir": "things",
            "prefix": "th-",
            "required": ["id"],
        }
    }
    bindings = sch.build_bindings(data)
    assert {b.tier for b in bindings} == {"product", "system", "subsystem"}
    assert {b.name for b in bindings} == {"thing"}          # shared type name
    assert len({b.label for b in bindings}) == 3            # distinct labels


def test_per_tier_overrides_change_parents_not_the_type_name():
    """The hinge case: same type, locally-resolved parent at one tier and a
    cross-repo parent at another."""
    data = dict(MINIMAL)
    data["types"] = {
        "req": {
            "tiers": ["system", "subsystem"],
            "subdir": "requirements",
            "prefix": "sysreq-",
            "required": ["id"],
            "per-tier": {
                "system": {"parents": {"parent-cap": "capability-requirement"}},
                "subsystem": {"external-parents": {"parent-sys": "sysreq-"}},
            },
        }
    }
    by_tier = {b.tier: b for b in sch.build_bindings(data)}
    assert by_tier["system"].parent_fields == {"parent-cap": "capability-requirement"}
    assert by_tier["system"].external_parent_fields == {}
    assert by_tier["subsystem"].parent_fields == {}
    assert by_tier["subsystem"].external_parent_fields == {"parent-sys": "sysreq-"}


def test_per_tier_required_fields_are_additive():
    data = dict(MINIMAL)
    data["types"] = {
        "req": {
            "tiers": ["system"],
            "subdir": "requirements",
            "prefix": "sysreq-",
            "required": ["id", "title"],
            "per-tier": {"system": {"required": ["parent-cap"]}},
        }
    }
    b = sch.build_bindings(data)[0]
    assert set(b.required_fields) == {"id", "title", "parent-cap"}


def test_required_fields_are_deduplicated():
    data = dict(MINIMAL)
    data["types"] = {
        "req": {
            "tiers": ["system"], "subdir": "r", "prefix": "x-",
            "required": ["id", "title"],
            "per-tier": {"system": {"required": ["id"]}},
        }
    }
    assert sch.build_bindings(data)[0].required_fields.count("id") == 1


# --------------------------------------------------------------------------
# Packets
# --------------------------------------------------------------------------

def test_packet_opt_out_removes_the_type():
    data = dict(MINIMAL)
    data["types"] = {
        "extra": {"packet": "fancy", "tiers": ["product"], "subdir": "x", "prefix": "e-"}
    }
    assert sch.build_bindings(data, packets={"fancy": False}) == ()
    assert len(sch.build_bindings(data, packets={"fancy": True})) == 1


def test_undeclared_packet_defaults_to_enabled():
    data = dict(MINIMAL)
    data["types"] = {
        "extra": {"packet": "fancy", "tiers": ["product"], "subdir": "x", "prefix": "e-"}
    }
    assert len(sch.build_bindings(data, packets={})) == 1


def test_core_packet_cannot_be_switched_off():
    assert len(sch.build_bindings(MINIMAL, packets={"core": False})) == 1


# --------------------------------------------------------------------------
# Schema errors
# --------------------------------------------------------------------------

def test_unknown_enum_reference_raises():
    data = dict(MINIMAL)
    data["types"] = {
        "w": {"tiers": ["product"], "subdir": "w", "prefix": "w-",
               "enums": {"priority": "does-not-exist"}}
    }
    with pytest.raises(sch.SchemaError, match="unknown enum"):
        sch.build_bindings(data)


def test_unknown_tier_reference_raises():
    data = dict(MINIMAL)
    data["types"] = {"w": {"tiers": ["nowhere"], "subdir": "w", "prefix": "w-"}}
    with pytest.raises(sch.SchemaError, match="unknown tier"):
        sch.build_bindings(data)


def test_missing_subdir_raises():
    data = dict(MINIMAL)
    data["types"] = {"w": {"tiers": ["product"], "prefix": "w-"}}
    with pytest.raises(sch.SchemaError, match="subdir"):
        sch.build_bindings(data)


def test_empty_tiers_raises():
    data = dict(MINIMAL)
    data["types"] = {"w": {"tiers": [], "subdir": "w", "prefix": "w-"}}
    with pytest.raises(sch.SchemaError, match="non-empty"):
        sch.build_bindings(data)


# --------------------------------------------------------------------------
# The shipped schema must itself be valid
# --------------------------------------------------------------------------

def test_shipped_schema_builds():
    bindings = sch.build_bindings(sch.load_schema())
    assert bindings, "the shipped schema produced no bindings"
    names = {b.name for b in bindings}
    for expected in (
        "persona", "use-case", "product-requirement", "capability-requirement",
        "system-requirement", "subsystem-requirement", "component-requirement",
        "interface", "architecture",
    ):
        assert expected in names


def test_system_requirement_is_l2_only():
    """The hinge is gone (D-05). A system requirement is an L2 artifact only.

    It previously spanned system+subsystem so one type could serve as the
    cross-repo join. The join is now capability requirement -> system
    requirement, which crosses a repo boundary and is brokered.
    """
    tiers = {
        b.tier for b in sch.build_bindings(sch.load_schema())
        if b.name == "system-requirement"
    }
    assert tiers == {"system"}


def test_each_tier_has_exactly_one_requirement_type():
    """Every requirement tier owns one requirement type - no overlaps."""
    bindings = sch.build_bindings(sch.load_schema())
    expected = {
        "product": "product-requirement",
        "capability": "capability-requirement",
        "system": "system-requirement",
        "subsystem": "subsystem-requirement",
        "component": "component-requirement",
    }
    for tier, type_name in expected.items():
        names = {b.name for b in bindings
                 if b.tier == tier and b.name.endswith("-requirement")}
        assert names == {type_name}, f"{tier}: expected {type_name}, got {names}"


def test_requirement_chain_parents_are_correct():
    """Each requirement type names the tier above it as parent (D-03)."""
    by = {b.name: b for b in sch.build_bindings(sch.load_schema())}
    # Within-repo parents resolve locally.
    assert "parent-system-requirements" in by["subsystem-requirement"].parent_fields
    assert "parent-subsystem-requirements" in by["component-requirement"].parent_fields
    # Cross-repo parents are external and brokered upstream.
    assert "parent-product-requirements" in by["capability-requirement"].external_parent_fields
    assert "parent-capability-requirements" in by["system-requirement"].external_parent_fields


def test_interfaces_and_architecture_are_core_not_packets():
    """A flag you cannot set to false is not a packet (D-52)."""
    names = {b.name for b in sch.build_bindings(
        sch.load_schema(), packets={"interfaces": False, "architecture": False})}
    assert "interface" in names
    assert "architecture" in names


def test_shipped_prefixes_match_prak():
    """Prefixes align with prak-v-model, which aligns with Jama."""
    by_name = {b.name: b.prefix for b in sch.build_bindings(sch.load_schema())}
    assert by_name["capability-requirement"] == "capreq-"
    assert by_name["system-requirement"] == "sysreq-"
    assert by_name["interface"] == "int-"
    assert by_name["architecture"] == "arch-"


def test_tier_list_agrees_with_tier_schema_prose():
    """standard/tier-schema.md §4 and artifact-schema.yaml must list the same tiers.

    They hold different information about the same key: the schema says which
    types live at a tier, the tier schema says which LEVEL declares it. Levels
    are deliberately absent from the schema, so neither file can be derived from
    the other and the overlap has to be checked.

    Justified by a counted pattern rather than a hypothetical: two prose copies
    of structure in this repo drifted within one week — CLAUDE.md's per-type
    field table (described an interface as requiring parent-capability-
    requirements long after that stopped being true) and README's hand-kept
    directory tree (still listed a deleted config/ directory). This is the third
    such copy.
    """
    import re as _re

    schema_tiers = set(sch.load_schema()["tiers"])

    prose = (sch.SCHEMA_PATH.parent / "tier-schema.md").read_text(encoding="utf-8")
    header = "| Tier | Level that declares it | Holds |"
    assert header in prose, "tier table not found in tier-schema.md section 4"
    table = prose[prose.index(header) + len(header):]
    table = table[: table.index("\n\n")]
    prose_tiers = set(_re.findall(r"^\| `([a-z-]+)` \|", table, _re.M))

    assert prose_tiers == schema_tiers, (
        f"tier-schema.md §4 and artifact-schema.yaml disagree — "
        f"only in prose: {sorted(prose_tiers - schema_tiers)}; "
        f"only in schema: {sorted(schema_tiers - prose_tiers)}"
    )
