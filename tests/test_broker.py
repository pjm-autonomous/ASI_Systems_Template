"""Tests for tools/broker.py — cross-repo upward enforcement.

The network is never touched: `_from_api` is monkeypatched wherever a fetch
would otherwise happen, so these tests are hermetic and fast.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from tools import broker as brk


def _decl(**over) -> dict:
    base = {
        "parents": [
            {"tier": "subsystem", "repo": "asirobots/prak-v-model",
             "ref": "main", "prefixes": ["sysreq-"]}
        ]
    }
    base.update(over)
    return base


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Fail loudly if a test reaches for the API without asking."""
    monkeypatch.setattr(brk, "_from_api", lambda *a, **k: None)


# --------------------------------------------------------------------------
# Declaration parsing
# --------------------------------------------------------------------------

def test_parses_a_parent():
    parents = brk.parse_parents(_decl())
    assert len(parents) == 1
    p = parents[0]
    assert p.tier == "subsystem"
    assert p.repo == "asirobots/prak-v-model"
    assert p.name == "prak-v-model"
    assert p.prefixes == ("sysreq-",)


def test_absent_parents_is_not_an_error():
    assert brk.parse_parents({}) == ()
    assert brk.parse_parents({"parents": None}) == ()


def test_empty_list_is_valid():
    assert brk.parse_parents({"parents": []}) == ()


def test_ref_defaults_to_main():
    parents = brk.parse_parents({"parents": [{"tier": "t", "repo": "o/r"}]})
    assert parents[0].ref == "main"


@pytest.mark.parametrize("bad", [
    {"parents": "nope"},
    {"parents": ["nope"]},
    {"parents": [{"tier": "subsystem"}]},
    {"parents": [{"repo": "o/r"}]},
    {"parents": [{"tier": "t", "repo": "no-slash"}]},
])
def test_malformed_declarations_raise(bad):
    with pytest.raises(brk.BrokerError):
        brk.parse_parents(bad)


# --------------------------------------------------------------------------
# Resolution
# --------------------------------------------------------------------------

def _make_sibling(tmp_path: Path, names: list[str], with_index: bool) -> Path:
    child = tmp_path / "embedded-core"
    child.mkdir()
    parent = tmp_path / "prak-v-model"
    (parent / "system" / "requirements").mkdir(parents=True)
    for name in names:
        (parent / "system" / "requirements" / name).write_text("x", encoding="utf-8")
    if with_index:
        (parent / brk.INDEX_FILENAME).write_text(
            json.dumps({"artifacts": {n: {} for n in names}}), encoding="utf-8"
        )
    return child


def test_resolves_from_sibling_index(tmp_path):
    child = _make_sibling(tmp_path, ["sysreq-a.md", "sysreq-b.md"], with_index=True)
    res = brk.resolve_parent(brk.parse_parents(_decl())[0], root=child)
    assert res.source == "sibling"
    assert res.available
    assert res.filenames == {"sysreq-a.md", "sysreq-b.md"}
    assert brk.INDEX_FILENAME in res.detail


def test_resolves_by_scanning_sibling_without_an_index(tmp_path):
    child = _make_sibling(tmp_path, ["sysreq-a.md"], with_index=False)
    res = brk.resolve_parent(brk.parse_parents(_decl())[0], root=child)
    assert res.source == "sibling"
    assert res.filenames == {"sysreq-a.md"}
    assert "scanned" in res.detail


def test_prefix_filter_excludes_other_artifacts(tmp_path):
    child = _make_sibling(tmp_path, ["sysreq-a.md", "capreq-b.md"], with_index=False)
    res = brk.resolve_parent(brk.parse_parents(_decl())[0], root=child)
    assert res.filenames == {"sysreq-a.md"}


def test_corrupt_sibling_index_falls_back_to_scanning(tmp_path):
    child = _make_sibling(tmp_path, ["sysreq-a.md"], with_index=False)
    (tmp_path / "prak-v-model" / brk.INDEX_FILENAME).write_text("{bad", encoding="utf-8")
    res = brk.resolve_parent(brk.parse_parents(_decl())[0], root=child)
    assert res.source == "sibling"
    assert res.filenames == {"sysreq-a.md"}


def test_unavailable_when_nothing_resolves(tmp_path, monkeypatch):
    monkeypatch.setattr(brk, "_from_cache", lambda *a, **k: None)
    child = tmp_path / "embedded-core"
    child.mkdir()
    res = brk.resolve_parent(brk.parse_parents(_decl())[0], root=child)
    assert not res.available
    assert res.source == "unavailable"


def test_fetch_is_skipped_when_disallowed(tmp_path, monkeypatch):
    monkeypatch.setattr(brk, "_from_cache", lambda *a, **k: None)
    called = []
    monkeypatch.setattr(brk, "_from_api", lambda *a, **k: called.append(1))
    child = tmp_path / "embedded-core"
    child.mkdir()
    brk.resolve_parent(brk.parse_parents(_decl())[0], allow_fetch=False, root=child)
    assert not called, "allow_fetch=False must not reach the network"


def test_stale_cache_is_ignored(tmp_path, monkeypatch):
    cache = tmp_path / "cache"
    cache.mkdir()
    parent = brk.parse_parents(_decl())[0]
    path = cache / f"{parent.repo.replace('/', '-')}.json"
    path.write_text(json.dumps({"artifacts": {"sysreq-a.md": {}}}), encoding="utf-8")
    old = time.time() - (brk.CACHE_TTL_S + 60)
    import os
    os.utime(path, (old, old))
    monkeypatch.setattr(brk, "CACHE_DIR", cache)
    monkeypatch.setattr(brk.ParentRepo, "cache_path", property(lambda self: path))
    assert brk._from_cache(parent) is None


def test_fresh_cache_is_used(tmp_path, monkeypatch):
    cache = tmp_path / "cache"
    cache.mkdir()
    parent = brk.parse_parents(_decl())[0]
    path = cache / "c.json"
    path.write_text(json.dumps({"artifacts": {"sysreq-a.md": {}}}), encoding="utf-8")
    monkeypatch.setattr(brk.ParentRepo, "cache_path", property(lambda self: path))
    res = brk._from_cache(parent)
    assert res is not None and res.source == "cache"


# --------------------------------------------------------------------------
# The check — upward enforcement
# --------------------------------------------------------------------------

def _refs(*names):
    return {"subsystem": [(Path("a.md"), "parent-system-requirements", n) for n in names]}


def test_valid_reference_passes(tmp_path):
    child = _make_sibling(tmp_path, ["sysreq-a.md"], with_index=True)
    errors, notes = brk.check_external_parents(
        _refs("sysreq-a.md"), brk.parse_parents(_decl()), root=child
    )
    assert errors == []
    assert any("resolved" in n for n in notes)


def test_broken_reference_is_caught(tmp_path):
    child = _make_sibling(tmp_path, ["sysreq-a.md"], with_index=True)
    errors, _ = brk.check_external_parents(
        _refs("sysreq-typo.md"), brk.parse_parents(_decl()), root=child
    )
    assert len(errors) == 1
    assert "no such artifact exists" in errors[0]


def test_multiple_parents_all_checked(tmp_path):
    child = _make_sibling(tmp_path, ["sysreq-a.md", "sysreq-b.md"], with_index=True)
    errors, _ = brk.check_external_parents(
        _refs("sysreq-a.md", "sysreq-b.md", "sysreq-missing.md"),
        brk.parse_parents(_decl()), root=child,
    )
    assert len(errors) == 1
    assert "sysreq-missing.md" in errors[0]


def test_undeclared_parent_tier_is_an_error(tmp_path):
    """A reference leaving the repo with no declared parent is unverifiable."""
    child = tmp_path / "embedded-core"
    child.mkdir()
    errors, _ = brk.check_external_parents(
        _refs("sysreq-a.md"), parents=(), root=child
    )
    assert len(errors) == 1
    assert "no parent is declared" in errors[0]


def test_unresolvable_parent_is_a_note_locally(tmp_path, monkeypatch):
    monkeypatch.setattr(brk, "_from_cache", lambda *a, **k: None)
    child = tmp_path / "embedded-core"
    child.mkdir()
    errors, notes = brk.check_external_parents(
        _refs("sysreq-a.md"), brk.parse_parents(_decl()),
        allow_fetch=False, require_resolution=False, root=child,
    )
    assert errors == []
    assert any("shape only" in n for n in notes)


def test_unresolvable_parent_is_an_error_in_ci(tmp_path, monkeypatch):
    monkeypatch.setattr(brk, "_from_cache", lambda *a, **k: None)
    child = tmp_path / "embedded-core"
    child.mkdir()
    errors, _ = brk.check_external_parents(
        _refs("sysreq-a.md"), brk.parse_parents(_decl()),
        allow_fetch=False, require_resolution=True, root=child,
    )
    assert len(errors) == 1
    assert "could not resolve parent" in errors[0]


def test_no_references_means_no_work(tmp_path):
    errors, notes = brk.check_external_parents({}, brk.parse_parents(_decl()))
    assert errors == [] and notes == []


def test_empty_reference_list_for_a_tier_is_skipped(tmp_path):
    errors, notes = brk.check_external_parents(
        {"subsystem": []}, brk.parse_parents(_decl())
    )
    assert errors == [] and notes == []


# --------------------------------------------------------------------------
# Index emission
# --------------------------------------------------------------------------

def test_index_records_tier_type_and_path(tmp_path):
    from tools.schema import build_bindings, load_schema
    bindings = [b for b in build_bindings(load_schema())
                if b.name == "system-requirement" and b.tier == "system"]
    f = tmp_path / "system" / "requirements" / "sysreq-a.md"
    f.parent.mkdir(parents=True)
    f.write_text("x", encoding="utf-8")

    index = brk.build_index(bindings, {bindings[0].label: [f]}, root=tmp_path)
    entry = index["artifacts"]["sysreq-a.md"]
    assert entry["tier"] == "system"
    assert entry["type"] == "system-requirement"
    assert entry["path"] == "system/requirements/sysreq-a.md"
    assert "generated" in index and "commit" in index


def test_emit_index_writes_at_repo_root(tmp_path):
    path = brk.emit_index({"artifacts": {}}, root=tmp_path)
    assert path == tmp_path / brk.INDEX_FILENAME
    assert json.loads(path.read_text(encoding="utf-8")) == {"artifacts": {}}


def test_index_paths_use_forward_slashes(tmp_path):
    """A child repo on Linux must resolve an index written on Windows."""
    from tools.schema import build_bindings, load_schema
    bindings = [b for b in build_bindings(load_schema())
                if b.name == "system-requirement" and b.tier == "system"]
    f = tmp_path / "system" / "requirements" / "geofencing" / "sysreq-a.md"
    f.parent.mkdir(parents=True)
    f.write_text("x", encoding="utf-8")
    index = brk.build_index(bindings, {bindings[0].label: [f]}, root=tmp_path)
    assert "\\" not in index["artifacts"]["sysreq-a.md"]["path"]
