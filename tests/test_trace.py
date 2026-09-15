"""Tests for tools/trace.py — the generated traceability matrix.

D-46 declared the matrix generated in September 2026 and nothing generated it,
so the file that shipped was hand-maintained with hand-edit instructions in it.
These tests pin the two things that made the hand-maintained version wrong, and
which a generator can silently reintroduce:

**The columns must be derived, not declared.** The shipped matrix had columns for
`Architecture`, `ICD` and `Data Spec`, none of which declares a `parent-*` field
— there was no edge to follow, so those cells were populated by sharing a
feature-bucket directory name. It also omitted `product-requirement`,
`subsystem-requirement` and `component-requirement`, which do have edges. Three
columns that could not be traced, three tiers that could and were missing.

**Currency is a separate failure from correctness.** A matrix that was right last
month and has not been regenerated passes every other check in the repo.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from tools import trace
from tools.schema import load_schema

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = REPO_ROOT / "example"


@pytest.fixture(scope="module")
def schema() -> dict:
    return load_schema()


# --------------------------------------------------------------------------
# The chain is derived from the schema
# --------------------------------------------------------------------------

def test_chain_is_the_full_requirement_lineage(schema):
    assert trace.chain_types(schema) == (
        "persona",
        "use-case",
        "product-requirement",
        "capability-requirement",
        "system-requirement",
        "subsystem-requirement",
        "component-requirement",
    )


def test_chain_includes_the_three_tiers_the_old_matrix_omitted(schema):
    """`prodreq-`, `subreq-` and `compreq-` artifacts appeared in no column."""
    chain = trace.chain_types(schema)
    for missing in ("product-requirement", "subsystem-requirement",
                    "component-requirement"):
        assert missing in chain


def test_unlinked_types_get_no_column(schema):
    """The three columns the model cannot populate.

    A column that can only ever be blank reads as a gap; a cell filled by
    guessing from a directory name reads as a fact. Neither is acceptable, so
    these are inventoried instead.
    """
    chain = trace.chain_types(schema)
    for unlinked in ("architecture", "interface", "data-specification"):
        assert unlinked not in chain
        assert unlinked in trace.unlinked_types(schema)


def test_every_type_is_either_chained_or_unlinked(schema):
    """No type may fall through both, or an artifact would be invisible."""
    both = set(trace.chain_types(schema)) | set(trace.unlinked_types(schema))
    assert both == set(schema["types"])


def test_primary_actors_is_not_treated_as_lineage(schema):
    """`use-case` declares `primary-actors: persona`; it is a cast, not ancestry.

    Counting it would duplicate every use case once per actor and imply a
    persona is a use case's parent twice over.
    """
    fields = {field for field, _, _ in trace.parent_edges(schema)["use-case"]}
    assert fields == {"parent-personas"}


def test_external_parents_are_resolved_to_their_type(schema):
    """`capability-requirement` names a prefix, not a type name."""
    edges = trace.parent_edges(schema)["capability-requirement"]
    assert edges == [("parent-product-requirements", "product-requirement", True)]


# --------------------------------------------------------------------------
# Row building
# --------------------------------------------------------------------------

def _artifact(filename: str, type_name: str, **fm) -> trace.Artifact:
    return trace.Artifact(filename, type_name, Path(filename), dict(fm))


CHAIN = ("persona", "use-case", "product-requirement")
EDGES = {
    "persona": [],
    "use-case": [("parent-personas", "persona", False)],
    "product-requirement": [("parent-use-cases", "use-case", False)],
}


def test_single_lineage_makes_one_row():
    artifacts = {
        "p.md": _artifact("p.md", "persona"),
        "uc-a.md": _artifact("uc-a.md", "use-case", **{"parent-personas": "p.md"}),
    }
    assert trace.build_rows(artifacts, CHAIN, EDGES) == [("p.md", "uc-a.md", "")]


def test_a_parent_with_children_does_not_get_its_own_row():
    """It already appears in its descendants' rows; a second row is noise."""
    artifacts = {
        "p.md": _artifact("p.md", "persona"),
        "uc-a.md": _artifact("uc-a.md", "use-case", **{"parent-personas": "p.md"}),
    }
    rows = trace.build_rows(artifacts, CHAIN, EDGES)
    assert len(rows) == 1


def test_multiple_parents_make_multiple_rows():
    """Parents are many-to-many (D-20); collapsing would hide a link."""
    artifacts = {
        "p1.md": _artifact("p1.md", "persona"),
        "p2.md": _artifact("p2.md", "persona"),
        "uc-a.md": _artifact(
            "uc-a.md", "use-case", **{"parent-personas": ["p1.md", "p2.md"]}
        ),
    }
    rows = trace.build_rows(artifacts, CHAIN, EDGES)
    assert rows == [("p1.md", "uc-a.md", ""), ("p2.md", "uc-a.md", "")]


def test_orphan_artifact_still_gets_a_row():
    """An artifact with no parent and no child must not vanish."""
    artifacts = {"p.md": _artifact("p.md", "persona")}
    assert trace.build_rows(artifacts, CHAIN, EDGES) == [("p.md", "", "")]


def test_external_parent_is_marked_and_stops_the_walk():
    edges = {
        "use-case": [],
        "product-requirement": [("parent-use-cases", "use-case", True)],
        "persona": [],
    }
    artifacts = {
        "prodreq-a.md": _artifact(
            "prodreq-a.md", "product-requirement",
            **{"parent-use-cases": "uc-elsewhere.md"},
        )
    }
    rows = trace.build_rows(artifacts, CHAIN, edges)
    assert rows == [("", f"uc-elsewhere.md {trace.UPSTREAM_MARK}", "prodreq-a.md")]


def test_missing_local_parent_is_marked_differently_from_external():
    """A dangling reference is a defect; an upstream one is the design."""
    artifacts = {
        "uc-a.md": _artifact("uc-a.md", "use-case", **{"parent-personas": "gone.md"})
    }
    rows = trace.build_rows(artifacts, CHAIN, EDGES)
    assert rows == [(f"gone.md {trace.MISSING_MARK}", "uc-a.md", "")]


def test_rows_are_sorted_and_deduplicated():
    """Byte-identical output for identical input, or --check thrashes."""
    artifacts = {
        "p2.md": _artifact("p2.md", "persona"),
        "p1.md": _artifact("p1.md", "persona"),
    }
    rows = trace.build_rows(artifacts, CHAIN, EDGES)
    assert rows == sorted(rows)
    assert len(rows) == len(set(rows))


def test_a_parent_cycle_terminates():
    """Defensive: a cycle is a data defect, not a reason to hang the build."""
    artifacts = {
        "a.md": _artifact("a.md", "use-case", **{"parent-personas": "b.md"}),
        "b.md": _artifact("b.md", "persona"),
    }
    edges = {
        "persona": [("parent-personas", "use-case", False)],
        "use-case": [("parent-personas", "persona", False)],
        "product-requirement": [],
    }
    trace.build_rows(artifacts, CHAIN, edges)   # must return, not recurse forever


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def test_render_marks_the_file_generated():
    out = trace.render([], ("persona",), {}, ())
    assert "GENERATED FILE - DO NOT EDIT" in out
    assert "build-traceability" in out


def test_render_carries_no_hand_edit_instructions():
    """The defect this generator replaced: a generated file telling you to edit it.

    The shipped matrix had a `## How to Update This Table` section reading "Add a
    new row whenever...", in the file D-46 declared generated.
    """
    out = trace.render([], ("persona",), {}, ())
    assert "How to Update" not in out
    assert "Add a new row" not in out


def test_render_has_no_trailing_whitespace():
    """The `trailing-whitespace` pre-commit hook rewrites the file otherwise.

    A two-space Markdown line break is stripped on commit, after which the
    tracked file can never again equal what the generator emits — a `--check`
    that fails forever and teaches everyone to skip the hook.
    """
    out = trace.render(
        [("a.md", "b.md")], ("persona", "use-case"), {}, ()
    )
    offenders = [ln for ln in out.split("\n") if ln != ln.rstrip()]
    assert not offenders, f"lines with trailing whitespace: {offenders}"


def test_render_survives_the_formatting_hooks():
    """No trailing whitespace, no doubled blanks, exactly one trailing newline.

    This bit twice, via two different hooks. `trailing-whitespace` strips a
    two-space Markdown line break; `end-of-file-fixer` and markdownlint MD012
    strip a doubled blank. Either rewrite makes the tracked file permanently
    unequal to what this function emits, so `--check` fails forever and everyone
    learns to skip the hook. The generator must emit what the hooks would leave.
    """
    for rows, chain in (
        ([], ("persona",)),
        ([("a.md", "b.md")], ("persona", "use-case")),
    ):
        out = trace.render(rows, chain, {}, ())
        ragged = [ln for ln in out.split("\n") if ln != ln.rstrip()]
        assert not ragged, f"trailing whitespace: {ragged}"
        assert "\n\n\n" not in out, "doubled blank line"
        assert out.endswith("\n"), "must end with a newline"
        assert not out.endswith("\n\n"), "must end with exactly one newline"


def test_render_is_deterministic():
    args = ([("a.md", "b.md")], ("persona", "use-case"), {}, ())
    assert trace.render(*args) == trace.render(*args)


def test_acronyms_are_not_title_cased():
    assert trace.humanize("adr") == "ADR"
    assert trace.humanize("interface") == "ICD"
    assert trace.humanize("product-requirement") == "Product Requirement"


# --------------------------------------------------------------------------
# The shipped files
# --------------------------------------------------------------------------

def test_repo_matrix_is_current():
    """`build-traceability --check`, as a test rather than only a hook."""
    target = REPO_ROOT / trace.MATRIX_PATH
    assert target.is_file()
    actual = target.read_text(encoding="utf-8").replace("\r\n", "\n")
    assert actual == trace.generate(REPO_ROOT), (
        "traceability/TRACEABILITY.md is stale — run `build-traceability`"
    )


def test_example_matrix_is_current():
    target = EXAMPLE / trace.MATRIX_PATH
    assert target.is_file()
    actual = target.read_text(encoding="utf-8").replace("\r\n", "\n")
    assert actual == trace.generate(EXAMPLE), (
        "example/traceability/TRACEABILITY.md is stale — regenerate it"
    )


def test_example_matrix_shows_the_whole_chain():
    """The example's own prodreq/subreq/compreq were invisible before.

    `tests/test_example.py` already required the example to demonstrate every
    requirement tier. The matrix describing it showed four of seven.
    """
    text = (EXAMPLE / trace.MATRIX_PATH).read_text(encoding="utf-8")
    for filename in (
        "fleet-operator.md",
        "uc-low-battery-return-to-dock.md",
        "prodreq-return-before-depletion.md",
        "capreq-autonomous-return-to-dock.md",
        "sysreq-battery-threshold-monitor.md",
        "subreq-battery-state-sampling.md",
        "compreq-voltage-sampler-rate.md",
    ):
        assert filename in text, f"{filename} does not appear in the matrix"


def test_example_matrix_lists_unlinked_artifacts_rather_than_tracing_them():
    """Architecture, ICD and data spec are present but not given a column."""
    text = (EXAMPLE / trace.MATRIX_PATH).read_text(encoding="utf-8")
    header = text.split("\n")[text.split("\n").index("# Traceability Matrix") + 4]
    for absent in ("Architecture", "ICD", "Data Spec"):
        assert absent not in header, f"'{absent}' is a column it cannot populate"
    assert "arch-dock-return-flow.md" in text
    assert "int-dock-reservation-api.md" in text


def test_check_mode_fails_on_a_stale_file(tmp_path):
    matrix = tmp_path / trace.MATRIX_PATH
    matrix.parent.mkdir(parents=True)
    matrix.write_text("# Stale\n", encoding="utf-8")
    assert trace.main(["--check", "--root", str(tmp_path)]) == 1


def test_check_mode_fails_when_the_file_is_absent(tmp_path):
    assert trace.main(["--check", "--root", str(tmp_path)]) == 1


def test_generate_then_check_passes(tmp_path):
    assert trace.main(["--root", str(tmp_path)]) == 0
    assert trace.main(["--check", "--root", str(tmp_path)]) == 0


def test_generated_matrix_is_valid_markdown_table():
    """Every row has the same cell count as the header, or renderers mangle it."""
    text = (EXAMPLE / trace.MATRIX_PATH).read_text(encoding="utf-8")
    rows = [ln for ln in text.split("\n") if ln.startswith("|")]
    widths = {len(re.findall(r"(?<!\\)\|", ln)) for ln in rows[:4]}
    assert len(widths) == 1, f"ragged table: {widths}"
