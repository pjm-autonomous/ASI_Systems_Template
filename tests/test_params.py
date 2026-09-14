"""Tests for tools/params.py — does every cited bound resolve to a value?

The counted failure behind the module: `prak-v-model` carries 223 requirement
files and 136 `TBD`/`TBR` occurrences across 37 files against 0 `param-*`
artifacts. This module is what makes an unresolved bound fail rather than pass.

Two areas get disproportionate attention on purpose.

**Falsy values.** `value: 0` is the obvious bug waiting in any "is this
missing?" check, and a threshold of 0 is a legitimate engineering statement.

**Back-reference drift.** The check earned its place by finding a real defect in
this repo's own `example/` — a parameter listing a requirement under `Cited By`
that cited no parameter at all. Both directions are therefore pinned: a citation
absent from the list, and a list entry absent from the citations.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tools import params as prm


def _decl(
    filename: str = "param-thing.md",
    value: object = 20,
    cited_by: tuple[str, ...] = (),
) -> prm.ParamDecl:
    return prm.ParamDecl(
        rel=Path("system/parameters") / filename,
        filename=filename,
        value=value,
        cited_by=frozenset(cited_by),
    )


# --------------------------------------------------------------------------
# Placeholder detection
# --------------------------------------------------------------------------

@pytest.mark.parametrize("value", ["TBD", "tbd", " TBR ", "?", "N/A", "todo",
                                   "pending", "placeholder", "", "   ", None])
def test_placeholder_values_are_rejected(value):
    assert prm.is_placeholder(value) is True


@pytest.mark.parametrize("value", [0, 0.0, False, 20, -5, "20", "0", "off",
                                   "20 percent", 1e-9])
def test_real_values_are_accepted(value):
    """`0` and `False` are values. Treating falsy as missing is the bug here."""
    assert prm.is_placeholder(value) is False


def test_zero_is_not_a_placeholder_even_as_a_string():
    assert not prm.is_placeholder("0")


# --------------------------------------------------------------------------
# Citation scanning
# --------------------------------------------------------------------------

def test_citation_found_in_backticks():
    cites = prm.collect_citations(
        [("sysreq-a.md", "see `param-battery-reserve.md` for the bound")]
    )
    assert cites == {"param-battery-reserve.md": frozenset({"sysreq-a.md"})}


def test_citation_found_in_a_markdown_link():
    cites = prm.collect_citations(
        [("sysreq-a.md", "[the threshold](../parameters/param-x.md)")]
    )
    assert cites["param-x.md"] == frozenset({"sysreq-a.md"})


def test_citation_found_in_bare_prose():
    """Authors write it plainly; the check must not require a link form."""
    cites = prm.collect_citations([("sysreq-a.md", "declared in param-x.md.")])
    assert cites["param-x.md"] == frozenset({"sysreq-a.md"})


def test_self_reference_is_not_a_citation():
    """A parameter repeats its own id in frontmatter and its body table."""
    text = "---\nid: param-x\n---\n| ID | param-x.md |\n"
    assert prm.collect_citations([("param-x.md", text)]) == {}


def test_multiple_citers_are_all_recorded():
    cites = prm.collect_citations(
        [("a.md", "`param-x.md`"), ("b.md", "`param-x.md`"), ("c.md", "nope")]
    )
    assert cites["param-x.md"] == frozenset({"a.md", "b.md"})


def test_repeated_citation_in_one_file_counts_once():
    cites = prm.collect_citations([("a.md", "param-x.md and param-x.md again")])
    assert cites["param-x.md"] == frozenset({"a.md"})


def test_id_without_extension_is_not_a_citation():
    """`param-x` is an id; `param-x.md` is a reference to the artifact."""
    assert prm.collect_citations([("a.md", "the param-x bound")]) == {}


# --------------------------------------------------------------------------
# Cited By parsing
# --------------------------------------------------------------------------

CITED_BY = """\
# Thing

## Basis

Some prose mentioning other-file.md which must not be read as a citation.

## Cited By

- `sysreq-a.md`
- `prodreq-b.md`
"""


def test_parses_cited_by_list():
    assert prm.parse_cited_by(CITED_BY) == frozenset({"sysreq-a.md", "prodreq-b.md"})


def test_cited_by_does_not_absorb_the_preceding_section():
    """`other-file.md` sits under Basis and must not be counted."""
    assert "other-file.md" not in prm.parse_cited_by(CITED_BY)


def test_cited_by_section_ends_at_the_next_heading():
    text = "## Cited By\n\n- a.md\n\n## Notes\n\n- b.md\n"
    assert prm.parse_cited_by(text) == frozenset({"a.md"})


def test_absent_cited_by_section_is_empty():
    assert prm.parse_cited_by("# T\n\nno such section\n") == frozenset()


def test_cited_by_heading_is_case_insensitive():
    assert prm.parse_cited_by("## cited by\n\n- a.md\n") == frozenset({"a.md"})


# --------------------------------------------------------------------------
# The checks
# --------------------------------------------------------------------------

def test_clean_parameter_passes():
    errors, notes = prm.check_parameters(
        [_decl(cited_by=("sysreq-a.md",))],
        {"param-thing.md": frozenset({"sysreq-a.md"})},
    )
    assert errors == []
    assert notes == []


def test_dangling_citation_is_an_error():
    errors, _ = prm.check_parameters(
        [], {"param-missing.md": frozenset({"sysreq-a.md"})}
    )
    assert len(errors) == 1
    assert "not a declared parameter" in errors[0]
    assert "sysreq-a.md" in errors[0]


def test_every_citer_of_a_missing_parameter_is_named():
    """Naming one of three leaves two authors unaware they must act."""
    errors, _ = prm.check_parameters(
        [], {"param-missing.md": frozenset({"a.md", "b.md", "c.md"})}
    )
    assert len(errors) == 3


def test_cited_placeholder_is_an_error():
    errors, _ = prm.check_parameters(
        [_decl(value="TBD", cited_by=("sysreq-a.md",))],
        {"param-thing.md": frozenset({"sysreq-a.md"})},
    )
    assert any("placeholder" in e for e in errors)


def test_uncited_placeholder_is_only_a_note():
    """Declaring the parameter before writing the requirement is the right order."""
    errors, notes = prm.check_parameters([_decl(value="TBD")], {})
    assert errors == []
    assert any("placeholder" in n for n in notes)


def test_citation_missing_from_cited_by_is_an_error():
    errors, _ = prm.check_parameters(
        [_decl(cited_by=())], {"param-thing.md": frozenset({"sysreq-a.md"})}
    )
    assert any("does not list them" in e for e in errors)


def test_stale_cited_by_entry_is_an_error():
    """The defect found in this repo's own example/ on 2026-09-13."""
    errors, _ = prm.check_parameters([_decl(cited_by=("sysreq-ghost.md",))], {})
    assert any("one direction only" in e for e in errors)
    assert any("sysreq-ghost.md" in e for e in errors)


def test_orphan_parameter_is_a_note_not_an_error():
    errors, notes = prm.check_parameters([_decl()], {})
    assert errors == []
    assert any("no artifact cites" in n for n in notes)


def test_zero_valued_parameter_with_a_citation_is_clean():
    """The falsy-value bug, end to end rather than only in is_placeholder."""
    errors, notes = prm.check_parameters(
        [_decl(value=0, cited_by=("sysreq-a.md",))],
        {"param-thing.md": frozenset({"sysreq-a.md"})},
    )
    assert errors == []
    assert notes == []


# --------------------------------------------------------------------------
# The shipped example
# --------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = REPO_ROOT / "example"


def _example_docs() -> list[tuple[str, str]]:
    return [
        (p.name, p.read_text(encoding="utf-8"))
        for p in sorted(EXAMPLE.rglob("*.md"))
        if p.name.lower() != "readme.md"
    ]


def test_example_parameter_is_cited_by_the_requirement_that_names_the_bound():
    """`sysreq-battery-threshold-monitor.md` says "the configured low-battery
    threshold" — the exact case the param type exists for. It listed itself
    under the parameter's `Cited By` while citing nothing.
    """
    cites = prm.collect_citations(_example_docs())
    citers = cites.get("param-battery-reserve-threshold.md", frozenset())
    assert "sysreq-battery-threshold-monitor.md" in citers, (
        "the system requirement naming the threshold does not cite the "
        "parameter that holds its value"
    )


def test_example_parameters_resolve_cleanly():
    """The worked example must pass the check it demonstrates."""
    import re

    import yaml

    docs = _example_docs()
    decls = []
    for path in sorted(EXAMPLE.rglob("param-*.md")):
        text = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---", text, re.S)
        fm = yaml.safe_load(match.group(1)) if match else {}
        decls.append(
            prm.ParamDecl(
                rel=path.relative_to(EXAMPLE),
                filename=path.name,
                value=(fm or {}).get("value"),
                cited_by=prm.parse_cited_by(text),
            )
        )
    errors, _ = prm.check_parameters(decls, prm.collect_citations(docs))
    assert errors == [], errors


def test_validator_actually_runs_the_param_gate(capsys):
    """The unit tests above would all pass with the module wired to nothing.

    This asserts the gate is live in `validate.main`: the summary line names
    every gate that ran, so a repo with `params: false` cannot read identically
    to one where every citation resolved.
    """
    from tools import validate

    assert validate.main([]) == 0
    assert "params resolved" in capsys.readouterr().out
