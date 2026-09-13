"""Every artifact type has a template, and every template matches its type.

Justified by a counted failure: an audit on 2026-09-13 found nine defects in
`templates/`. Five templates carried frontmatter the schema no longer accepted —
`interface.md` still asked for `owning-component` and `consumers`,
`capability-requirement.md` still named use cases as its parent, and
`architecture-diagram.md` and `data-specification.md` still carried a
capability-requirement parent that had been removed. Four types added when the
model was re-tiered had no template at all.

A template that disagrees with the schema is worse than a missing one: it teaches
the wrong shape and every artifact copied from it fails validation afterwards.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from tools.schema import build_bindings, load_schema

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

# Artifact type -> template filename. A type missing from this map fails
# `test_every_type_has_a_template`, so adding a type forces adding a template.
TEMPLATE_FOR: dict[str, str] = {
    "persona": "persona.md",
    "use-case": "use-case.md",
    "product-requirement": "product-requirement.md",
    "capability-requirement": "capability-requirement.md",
    "system-requirement": "system-requirement.md",
    "subsystem-requirement": "subsystem-requirement.md",
    "component-requirement": "component-requirement.md",
    "architecture": "architecture-diagram.md",
    "interface": "interface.md",
    "data-specification": "data-specification.md",
    "deployment-architecture": "deployment-architecture.md",
    "param": "parameter.md",
    "adr": "adr.md",
}


def _bindings() -> dict:
    """One binding per type name, all tiers active."""
    return {b.name: b for b in build_bindings(load_schema())}


def _frontmatter(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        return set()
    data = yaml.safe_load(match.group(1))
    return set(data or {})


def test_every_type_has_a_template():
    """A type without a template cannot be authored from the standard."""
    missing = sorted(set(_bindings()) - set(TEMPLATE_FOR))
    assert not missing, (
        f"artifact types with no template: {missing} — add one to templates/ "
        f"and register it in TEMPLATE_FOR"
    )


def test_every_mapped_template_exists():
    missing = [fn for fn in TEMPLATE_FOR.values()
               if not (TEMPLATES_DIR / fn).is_file()]
    assert not missing, f"templates referenced but absent: {missing}"


@pytest.mark.parametrize("type_name,filename", sorted(TEMPLATE_FOR.items()))
def test_template_carries_every_required_field(type_name, filename):
    """A template must not omit a field the validator will demand."""
    binding = _bindings()[type_name]
    present = _frontmatter(TEMPLATES_DIR / filename)
    missing = sorted(set(binding.required_fields) - present)
    assert not missing, (
        f"{filename}: missing required frontmatter {missing} — an artifact "
        f"copied from this template would fail validation"
    )


@pytest.mark.parametrize("type_name,filename", sorted(TEMPLATE_FOR.items()))
def test_template_carries_no_unknown_field(type_name, filename):
    """A template must not teach a field the schema does not know.

    This is the half that actually bit: the fields were not merely unused, they
    described a contract that had been replaced.
    """
    binding = _bindings()[type_name]
    known = (
        set(binding.required_fields)
        | set(binding.parent_fields)
        | set(binding.external_parent_fields)
        | set(binding.enum_fields)
    )
    extra = sorted(_frontmatter(TEMPLATES_DIR / filename) - known)
    assert not extra, (
        f"{filename}: frontmatter {extra} is not in the schema for "
        f"'{type_name}' — either the schema or the template is wrong"
    )


def test_templates_do_not_restate_enum_values():
    """Enum values live in the schema; a prose copy drifts.

    `capability-requirement.md` carried `priority: Critical | High | Medium |
    Low` while the schema enforced MoSCoW. Any artifact authored from it would
    have been rejected on a value the template itself suggested.
    """
    offenders = []
    for filename in TEMPLATE_FOR.values():
        text = (TEMPLATES_DIR / filename).read_text(encoding="utf-8")
        if re.search(r"Critical\s*[|/,]\s*High", text):
            offenders.append(filename)
    assert not offenders, (
        f"{offenders}: restate a priority scheme the schema does not use"
    )
