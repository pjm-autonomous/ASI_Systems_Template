"""The worked example must satisfy the schema it demonstrates.

`example/` is deliberately outside the validator's globs — its artifacts are
illustrative, not part of this repo's traceability chain, and validating them as
if they were would report a fictional feature as real content.

The cost of that exclusion is that the example drifted silently. It was still on
the pre-re-tier model: `priority: High` where the schema requires MoSCoW,
`parent-use-cases` on artifacts that no longer accept it, a capability
requirement parented to a use case rather than a product requirement, and a
parent reference missing its `.md`. Every one of those would have failed
validation in a real repo, and the example is what an author copies from.

So these tests run the same checks against `example/`, rooted there instead of at
the repo root. The example is held to the standard it teaches.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from tools import validate
from tools.schema import build_bindings, load_schema

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = REPO_ROOT / "example"


def _bindings():
    """All tiers active: the example demonstrates the whole model."""
    return build_bindings(load_schema())


def _example_artifacts() -> list[tuple[Path, object]]:
    """Every example artifact, paired with the binding that governs it."""
    found: list[tuple[Path, object]] = []
    for binding in _bindings():
        for pattern in binding.glob:
            for path in EXAMPLE.glob(pattern):
                if path.is_file() and path.name.lower() != "readme.md":
                    found.append((path, binding))
    return sorted(found, key=lambda pair: str(pair[0]))


def _ids(pair) -> str:
    return str(pair[0].relative_to(EXAMPLE)).replace("\\", "/")


def _frontmatter(path: Path) -> dict:
    match = re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    return yaml.safe_load(match.group(1)) if match else {}


def test_example_has_artifacts():
    """A worked example with nothing in it teaches nothing."""
    found = _example_artifacts()
    assert found, (
        "no example artifacts matched any schema binding — either example/ has "
        "moved or its directories no longer match the tier names"
    )


def test_example_demonstrates_the_whole_requirement_chain():
    """Every requirement tier appears, so the chain can be followed end to end.

    The example previously jumped from use case straight to capability
    requirement, skipping the product tier, and stopped at system requirement —
    so the two links most likely to be got wrong were the two it did not show.
    """
    names = {binding.name for _, binding in _example_artifacts()}
    for required in (
        "persona", "use-case", "product-requirement", "capability-requirement",
        "system-requirement", "subsystem-requirement", "component-requirement",
    ):
        assert required in names, f"example does not demonstrate '{required}'"


@pytest.mark.parametrize("pair", _example_artifacts(), ids=_ids)
def test_example_artifact_filename(pair):
    path, binding = pair
    errors = validate._check_filename(binding, path)
    assert not errors, errors


@pytest.mark.parametrize("pair", _example_artifacts(), ids=_ids)
def test_example_artifact_required_fields(pair):
    path, binding = pair
    errors = validate._check_required_fields(
        binding, path.relative_to(EXAMPLE), _frontmatter(path)
    )
    assert not errors, errors


@pytest.mark.parametrize("pair", _example_artifacts(), ids=_ids)
def test_example_artifact_enum_values(pair):
    """Catches the class of drift that hit hardest: `priority: High`."""
    path, binding = pair
    errors = validate._check_enum_fields(
        binding, path.relative_to(EXAMPLE), _frontmatter(path)
    )
    assert not errors, errors


@pytest.mark.parametrize("pair", _example_artifacts(), ids=_ids)
def test_example_artifact_external_refs_are_well_formed(pair):
    path, binding = pair
    errors = validate._check_external_refs(
        binding, path.relative_to(EXAMPLE), _frontmatter(path)
    )
    assert not errors, errors


def test_example_local_cross_references_resolve():
    """A parent named inside example/ must exist inside example/.

    Cross-repo parents are the exception: in a real deployment they live in
    another repo, so the example carries both ends and the reference resolves
    here. That is a property of the example, not of the model.
    """
    artifacts = _example_artifacts()
    by_type: dict[str, set[str]] = {}
    for path, binding in artifacts:
        by_type.setdefault(binding.name, set()).add(path.name)

    errors: list[str] = []
    for path, binding in artifacts:
        fm = _frontmatter(path)
        errors.extend(
            validate._check_cross_refs(
                binding, path.relative_to(EXAMPLE), fm, by_type
            )
        )
        # External parents resolve within the example too, since it carries
        # every level in one tree.
        for field, prefix in binding.external_parent_fields.items():
            raw = fm.get(field)
            for value in (raw if isinstance(raw, list) else [raw]):
                if not value:
                    continue
                known = {p.name for p, _ in artifacts}
                if str(value) not in known:
                    errors.append(
                        f"{path.relative_to(EXAMPLE)}: '{field}' names "
                        f"'{value}', which is not present in example/"
                    )
    assert not errors, errors


def test_example_cited_parameter_exists():
    """A requirement citing a bound by name needs the parameter to be there.

    This is the point the `param` type exists to make, so the example has to
    make it rather than describe it.
    """
    params = {
        path.stem for path, binding in _example_artifacts()
        if binding.name == "param"
    }
    assert params, "example demonstrates no parameter"

    citing = [
        path for path, _ in _example_artifacts()
        if any(p in path.read_text(encoding="utf-8") for p in params)
    ]
    assert len(citing) >= 2, (
        "the example parameter is not cited by any requirement, so it does not "
        "demonstrate why the type exists"
    )
