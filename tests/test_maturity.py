"""Tests for tools/maturity.py — the AxS M1..M4 maturity scheme.

The header-block parser gets the most attention on purpose. A bold key-value
block in the document body is easier for a human to read than frontmatter and
much easier to break by accident, so the format has to be pinned by tests rather
than left to whatever the regex happens to tolerate.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tools import maturity as mat

AXS_STYLE = """\
# Geofence Map Validation
**Artifact ID:** sysreq-geofence-map-validation
**Version:** 1.0
**Status:** M2+
**Tier:** System

---

## Requirement
"""

WITH_FRONTMATTER = """\
---
id: sysreq-thing
title: Thing
---

# Thing
**Status:** M3

Body text.
"""


# --------------------------------------------------------------------------
# Header block parsing
# --------------------------------------------------------------------------

def test_parses_axs_header_block():
    header = mat.parse_header_block(AXS_STYLE)
    assert header["Status"] == "M2+"
    assert header["Version"] == "1.0"
    assert header["Artifact ID"] == "sysreq-geofence-map-validation"


def test_parses_block_after_frontmatter():
    assert mat.parse_header_block(WITH_FRONTMATTER)["Status"] == "M3"


def test_block_ends_at_first_non_header_line():
    text = "# T\n**Status:** M1\nprose here\n**Version:** 9\n"
    header = mat.parse_header_block(text)
    assert header == {"Status": "M1"}, "must not resume after prose"


def test_blank_lines_between_h1_and_block_are_allowed():
    assert mat.parse_header_block("# T\n\n\n**Status:** M2\n")["Status"] == "M2"


def test_no_h1_means_no_block():
    assert mat.parse_header_block("**Status:** M4\n") == {}


def test_prose_before_h1_means_no_block():
    """Refuse to go hunting for a header in an arbitrary document."""
    assert mat.parse_header_block("Some intro.\n\n# T\n**Status:** M4\n") == {}


def test_empty_value_is_captured_not_skipped():
    assert mat.parse_header_block("# T\n**Status:**\n") == {"Status": ""}


def test_bold_text_that_is_not_a_header_line_is_ignored():
    assert mat.parse_header_block("# T\n**Note** this is prose\n") == {}


def test_handles_bom():
    assert mat.parse_header_block("﻿---\nid: x\n---\n\n# T\n**Status:** M1\n") \
        ["Status"] == "M1"


# --------------------------------------------------------------------------
# Resolving a state
# --------------------------------------------------------------------------

def test_header_is_canonical_source():
    state = mat.read_maturity(AXS_STYLE)
    assert state.state == "M2+"
    assert state.source == "header"


def test_frontmatter_is_a_fallback():
    state = mat.read_maturity("# T\n\nbody\n", {"maturity": "M2"})
    assert state.state == "M2"
    assert state.source == "frontmatter"


def test_header_wins_over_frontmatter():
    assert mat.read_maturity("# T\n**Status:** M4\n", {"maturity": "M1"}).state == "M4"


def test_non_maturity_status_frontmatter_is_not_read_as_maturity():
    """ADRs and interfaces use `status` for their own lifecycles."""
    assert mat.read_maturity("# T\n\nbody\n", {"status": "accepted"}).state is None
    assert mat.read_maturity("# T\n\nbody\n", {"status": "Baseline"}).state is None


def test_absent_state():
    state = mat.read_maturity("# T\n\nbody\n")
    assert state.state is None
    assert state.source == "absent"
    assert state.rank == -1
    assert not state.at_least("M1")


# --------------------------------------------------------------------------
# Ordering
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "state,threshold,expected",
    [
        ("M1", "M1", True), ("M1", "M2", False),
        ("M2", "M2", True), ("M2+", "M2", True),
        ("M2", "M2+", False), ("M3", "M2+", True),
        ("M4", "M4", True), ("M3", "M4", False),
    ],
)
def test_at_least_ordering(state, threshold, expected):
    assert mat.read_maturity(f"# T\n**Status:** {state}\n").at_least(threshold) is expected


def test_m2_plus_ranks_above_m2():
    order = mat.MATURITY_ORDER
    assert order.index("M2+") > order.index("M2")
    assert order.index("M3") > order.index("M2+")


# --------------------------------------------------------------------------
# Evidence requirement
# --------------------------------------------------------------------------

def _artifact(state: str) -> str:
    return f"# Thing\n**Status:** {state}\n\nbody\n"


def test_m1_needs_no_evidence(tmp_path):
    errors = mat.check_artifact(
        Path("a.md"), "sysreq-thing", _artifact("M1"), root=tmp_path
    )
    assert errors == []


@pytest.mark.parametrize("state", ["M2", "M2+", "M3", "M4"])
def test_states_above_m1_require_a_record(tmp_path, state):
    errors = mat.check_artifact(
        Path("a.md"), "sysreq-thing", _artifact(state), root=tmp_path
    )
    assert len(errors) == 1
    assert "no promotion record" in errors[0]


def test_matching_record_satisfies_the_requirement(tmp_path):
    d = tmp_path / "_registry" / "m2_records"
    d.mkdir(parents=True)
    (d / "system-sysreq-thing_M2_Record.md").write_text("evidence", encoding="utf-8")
    errors = mat.check_artifact(
        Path("a.md"), "sysreq-thing", _artifact("M2"), root=tmp_path
    )
    assert errors == []


def test_record_for_a_different_artifact_does_not_count(tmp_path):
    d = tmp_path / "_registry" / "m2_records"
    d.mkdir(parents=True)
    (d / "system-sysreq-other_M2_Record.md").write_text("evidence", encoding="utf-8")
    errors = mat.check_artifact(
        Path("a.md"), "sysreq-thing", _artifact("M2"), root=tmp_path
    )
    assert len(errors) == 1


def test_m3_looks_in_m3_reviews_not_m2_records(tmp_path):
    d = tmp_path / "_registry" / "m2_records"
    d.mkdir(parents=True)
    (d / "sysreq-thing_M2_Record.md").write_text("evidence", encoding="utf-8")
    errors = mat.check_artifact(
        Path("a.md"), "sysreq-thing", _artifact("M3"), root=tmp_path
    )
    assert len(errors) == 1
    assert "m3_reviews" in errors[0]


def test_illegal_state_is_rejected(tmp_path):
    errors = mat.check_artifact(
        Path("a.md"), "sysreq-thing", _artifact("M9"), root=tmp_path
    )
    assert len(errors) == 1
    assert "not a legal state" in errors[0]


def test_missing_declaration_is_reported_when_required(tmp_path):
    errors = mat.check_artifact(
        Path("a.md"), "sysreq-thing", "# T\n\nbody\n", root=tmp_path
    )
    assert len(errors) == 1
    assert "no maturity state declared" in errors[0]


def test_missing_declaration_tolerated_when_not_required(tmp_path):
    errors = mat.check_artifact(
        Path("a.md"), "sysreq-thing", "# T\n\nbody\n",
        root=tmp_path, require_declaration=False,
    )
    assert errors == []


# --------------------------------------------------------------------------
# Cross-tier gating
# --------------------------------------------------------------------------

TIERS = ["product", "system", "subsystem", "component"]


def _state(value: str) -> mat.MaturityState:
    return mat.read_maturity(f"# T\n**Status:** {value}\n")


def test_m4_blocked_when_tier_above_is_not_m4():
    errors = mat.check_tier_gating(
        {
            "system": [(Path("sys.md"), _state("M2"))],
            "subsystem": [(Path("sub.md"), _state("M4"))],
        },
        TIERS,
    )
    assert len(errors) == 1
    assert "not fully M4" in errors[0]


def test_m4_allowed_when_tier_above_is_fully_m4():
    errors = mat.check_tier_gating(
        {
            "system": [(Path("sys.md"), _state("M4"))],
            "subsystem": [(Path("sub.md"), _state("M4"))],
        },
        TIERS,
    )
    assert errors == []


def test_one_laggard_above_blocks_m4_below():
    errors = mat.check_tier_gating(
        {
            "system": [
                (Path("a.md"), _state("M4")),
                (Path("b.md"), _state("M3")),
            ],
            "subsystem": [(Path("sub.md"), _state("M4"))],
        },
        TIERS,
    )
    assert len(errors) == 1
    assert "1 artifact(s) below M4" in errors[0]


def test_below_m4_is_never_gated():
    errors = mat.check_tier_gating(
        {
            "system": [(Path("sys.md"), _state("M1"))],
            "subsystem": [(Path("sub.md"), _state("M3"))],
        },
        TIERS,
    )
    assert errors == []


def test_absent_tier_above_does_not_gate():
    """A sub-system repo has no product tier; it must not be blocked by one."""
    errors = mat.check_tier_gating(
        {
            "subsystem": [(Path("sub.md"), _state("M4"))],
            "component": [(Path("cmp.md"), _state("M4"))],
        },
        TIERS,
    )
    assert errors == []


def test_outermost_tier_is_never_gated():
    errors = mat.check_tier_gating(
        {"product": [(Path("p.md"), _state("M4"))]}, TIERS
    )
    assert errors == []


# --------------------------------------------------------------------------
# Shipped registry
# --------------------------------------------------------------------------

def test_registry_directories_exist():
    root = mat.registry_root()
    assert (root / "m2_records").is_dir()
    assert (root / "m3_reviews").is_dir()
    assert (root / "README.md").is_file()


def test_every_state_maps_to_an_evidence_dir_except_m1():
    for state in mat.MATURITY_ORDER:
        if state == "M1":
            assert state not in mat.EVIDENCE_DIRS
        else:
            assert mat.EVIDENCE_DIRS[state] in {"m2_records", "m3_reviews"}
