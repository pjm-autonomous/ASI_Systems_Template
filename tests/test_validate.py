from __future__ import annotations

from pathlib import Path

import pytest

from tools import validate


PERSONA = next(a for a in validate.ARTIFACT_TYPES if a.name == "persona")
USE_CASE = next(a for a in validate.ARTIFACT_TYPES if a.name == "use-case")
PRODUCT_REQ = next(a for a in validate.ARTIFACT_TYPES if a.name == "product-requirement")
SYSTEM_REQ = next(a for a in validate.ARTIFACT_TYPES if a.name == "system-requirement")
ARCHITECTURE = next(a for a in validate.ARTIFACT_TYPES if a.name == "architecture")
ICD = next(a for a in validate.ARTIFACT_TYPES if a.name == "icd")
DATA_SPEC = next(a for a in validate.ARTIFACT_TYPES if a.name == "data-specification")
DEPLOYMENT = next(a for a in validate.ARTIFACT_TYPES if a.name == "deployment-architecture")
ADR = next(a for a in validate.ARTIFACT_TYPES if a.name == "adr")


def test_parse_frontmatter_missing():
    fm, err = validate.parse_frontmatter("no frontmatter here")
    assert fm is None
    assert "missing YAML frontmatter" in err


def test_parse_frontmatter_unterminated():
    fm, err = validate.parse_frontmatter("---\nid: x\n")
    assert fm is None
    assert "unterminated" in err


def test_parse_frontmatter_valid():
    fm, err = validate.parse_frontmatter("---\nid: x\ntitle: Y\n---\nbody")
    assert err is None
    assert fm == {"id": "x", "title": "Y"}


def test_check_filename_persona_kebab(tmp_path: Path):
    good = tmp_path / "fleet-operator.md"
    bad = tmp_path / "FleetOperator.md"
    assert validate._check_filename(PERSONA, good) == []
    assert validate._check_filename(PERSONA, bad) != []


def test_check_filename_prefix_enforced(tmp_path: Path):
    good = tmp_path / "uc-example.md"
    bad = tmp_path / "example.md"
    assert validate._check_filename(USE_CASE, good) == []
    errors = validate._check_filename(USE_CASE, bad)
    assert any("must start with 'uc-'" in e for e in errors)


def test_adr_allows_numeric_slug(tmp_path: Path):
    path = tmp_path / "adr-0001-example-decision.md"
    assert validate._check_filename(ADR, path) == []


def test_required_fields_missing():
    errors = validate._check_required_fields(
        PRODUCT_REQ, Path("req-example.md"), {"id": "req-example"}
    )
    assert any("title" in e for e in errors)
    assert any("parent-use-cases" in e for e in errors)
    assert any("priority" in e for e in errors)


def test_required_fields_empty_list_rejected():
    errors = validate._check_required_fields(
        USE_CASE,
        Path("uc-example.md"),
        {
            "id": "uc-example",
            "title": "Example",
            "primary-actors": [],
            "parent-personas": ["fleet-operator.md"],
        },
    )
    assert any("primary-actors" in e for e in errors)


def test_cross_refs_missing_target():
    files_by_filename = {"product-requirement": set()}
    errors = validate._check_cross_refs(
        SYSTEM_REQ,
        Path("sysreq-example.md"),
        {"parent-product-requirement": "req-does-not-exist.md"},
        files_by_filename,
    )
    assert any("no product-requirement" in e for e in errors)


def test_cross_refs_resolves_when_present():
    files_by_filename = {"product-requirement": {"req-example.md"}}
    errors = validate._check_cross_refs(
        SYSTEM_REQ,
        Path("sysreq-example.md"),
        {"parent-product-requirement": "req-example.md"},
        files_by_filename,
    )
    assert errors == []


def test_cross_refs_requires_md_extension():
    files_by_filename = {"product-requirement": {"req-example.md"}}
    errors = validate._check_cross_refs(
        SYSTEM_REQ,
        Path("sysreq-example.md"),
        {"parent-product-requirement": "req-example"},
        files_by_filename,
    )
    assert any("must include the '.md'" in e for e in errors)


def test_architecture_requires_mermaid_block(tmp_path: Path):
    path = tmp_path / "arch-example.md"
    path.write_text(
        "---\nid: arch-example\ntitle: Example\n"
        "parent-product-requirement: req-example.md\ndiagram-type: sequence\n---\nno diagram here\n"
    )
    errors = validate.validate_file(
        path, ARCHITECTURE, {"product-requirement": {"req-example.md"}}
    )
    assert any("mermaid" in e for e in errors)


def test_architecture_passes_with_mermaid_block(tmp_path: Path):
    path = tmp_path / "arch-example.md"
    path.write_text(
        "---\nid: arch-example\ntitle: Example\n"
        "parent-product-requirement: req-example.md\ndiagram-type: sequence\n---\n"
        "```mermaid\nflowchart TD\nA --> B\n```\n"
    )
    errors = validate.validate_file(
        path, ARCHITECTURE, {"product-requirement": {"req-example.md"}}
    )
    assert errors == []


def test_icd_required_fields():
    errors = validate._check_required_fields(
        ICD,
        Path("icd-example.md"),
        {"id": "icd-example", "title": "Example", "owning-component": "svc"},
    )
    assert any("parent-product-requirement" in e for e in errors)
    assert any("consumers" in e for e in errors)


def test_data_specification_required_fields():
    errors = validate._check_required_fields(
        DATA_SPEC,
        Path("data-example.md"),
        {"id": "data-example", "title": "Example"},
    )
    assert any("parent-product-requirement" in e for e in errors)


def test_deployment_required_fields():
    errors = validate._check_required_fields(
        DEPLOYMENT,
        Path("deploy-example.md"),
        {"id": "deploy-example", "title": "Example"},
    )
    assert any("scope" in e for e in errors)


def test_adr_status_enum(tmp_path: Path):
    path = tmp_path / "adr-0001-example.md"
    path.write_text(
        "---\nid: adr-0001\ntitle: Example\nstatus: made-up\ndate: 2026-07-22\n---\nbody\n"
    )
    errors = validate.validate_file(path, ADR, {})
    assert any("'status' must be one of" in e for e in errors)


def test_persona_class_enum(tmp_path: Path):
    path = tmp_path / "example-persona.md"
    path.write_text(
        "---\nid: example-persona\ntitle: Example\nclass: made-up\n---\nbody\n"
    )
    errors = validate.validate_file(path, PERSONA, {})
    assert any("'class' must be one of" in e for e in errors)
