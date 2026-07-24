"""Validate SA/SE artifacts against repo conventions.

Checked per artifact:
- Filename pattern (kebab-case + correct prefix for the artifact type)
- YAML frontmatter is present, parseable, and contains all required fields
- Persona `class` value is one of the documented enum members
- Cross-reference fields point to filenames that actually exist at the
  correct layer
- Architecture files contain at least one fenced mermaid code block

Run via `validate-artifacts` after `pip install -e .` from the repo root.

Generalized from prak-v-model's validator: adds ICD, data-specification,
deployment-architecture, and ADR artifact types, and switches the
architecture/table convention from HTML tables to plain Markdown (which
doesn't change what this validator checks — it never parsed table markup).
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MERMAID_FENCE = re.compile(r"^```mermaid\s*$", re.MULTILINE)

PERSONA_CLASSES = {"developer-integrator", "runtime-operator", "external-system"}


@dataclass(frozen=True)
class ArtifactType:
    name: str
    glob: str
    prefix: str
    required_fields: tuple[str, ...]
    parent_fields: dict[str, str] = field(default_factory=dict)
    list_parent_fields: frozenset[str] = field(default_factory=frozenset)
    is_architecture: bool = False


ARTIFACT_TYPES: tuple[ArtifactType, ...] = (
    ArtifactType(
        name="persona",
        glob="product/personas/*.md",
        prefix="",
        required_fields=("id", "title", "class"),
    ),
    ArtifactType(
        name="use-case",
        glob="product/use-cases/*/*.md",
        prefix="uc-",
        required_fields=("id", "title", "primary-actors", "parent-personas"),
        parent_fields={"primary-actors": "persona", "parent-personas": "persona"},
        list_parent_fields={"primary-actors", "parent-personas"},
    ),
    ArtifactType(
        name="product-requirement",
        glob="product/requirements/*/*.md",
        prefix="req-",
        required_fields=("id", "title", "parent-use-cases", "priority"),
        parent_fields={"parent-use-cases": "use-case"},
        list_parent_fields={"parent-use-cases"},
    ),
    ArtifactType(
        name="system-requirement",
        glob="system/requirements/*/*.md",
        prefix="sysreq-",
        required_fields=(
            "id",
            "title",
            "parent-product-requirement",
            "allocation",
            "priority",
        ),
        parent_fields={
            "parent-product-requirement": "product-requirement",
            "parent-use-cases": "use-case",
        },
        list_parent_fields={"parent-use-cases"},
    ),
    ArtifactType(
        name="architecture",
        glob="system/architecture/*/*.md",
        prefix="arch-",
        required_fields=("id", "title", "parent-product-requirement", "diagram-type"),
        parent_fields={"parent-product-requirement": "product-requirement"},
        is_architecture=True,
    ),
    ArtifactType(
        name="icd",
        glob="system/interfaces/*/*.md",
        prefix="icd-",
        required_fields=(
            "id",
            "title",
            "parent-product-requirement",
            "owning-component",
            "consumers",
        ),
        parent_fields={"parent-product-requirement": "product-requirement"},
    ),
    ArtifactType(
        name="data-specification",
        glob="system/data/*/*.md",
        prefix="data-",
        required_fields=("id", "title", "parent-product-requirement"),
        parent_fields={"parent-product-requirement": "product-requirement"},
    ),
    ArtifactType(
        name="deployment-architecture",
        glob="system/deployment/*/*.md",
        prefix="deploy-",
        required_fields=("id", "title", "scope"),
    ),
    ArtifactType(
        name="adr",
        glob="system/decisions/*.md",
        prefix="adr-",
        required_fields=("id", "title", "status", "date"),
    ),
)

ADR_STATUSES = {"proposed", "accepted", "superseded", "obsolete"}


def _rel(path: Path) -> Path:
    """Path relative to REPO_ROOT for error messages, falling back to the
    path as given when it isn't under REPO_ROOT (e.g. a temp path in tests).
    """
    try:
        return path.relative_to(REPO_ROOT)
    except ValueError:
        return path


def parse_frontmatter(text: str) -> tuple[dict | None, str | None]:
    """Return (frontmatter dict, error message). Exactly one is None."""
    if not text.startswith("---\n"):
        return None, "missing YAML frontmatter (file must start with '---')"
    end_idx = text.find("\n---\n", 4)
    if end_idx == -1:
        return None, "unterminated YAML frontmatter (missing closing '---')"
    fm_text = text[4:end_idx]
    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        return None, f"invalid YAML in frontmatter: {exc}"
    if data is None:
        return {}, None
    if not isinstance(data, dict):
        return None, "frontmatter must be a YAML mapping"
    return data, None


def _check_filename(atype: ArtifactType, path: Path) -> list[str]:
    rel = _rel(path)
    errors: list[str] = []
    stem = path.stem
    if atype.prefix:
        if not stem.startswith(atype.prefix):
            errors.append(
                f"{rel}: filename must start with '{atype.prefix}' for {atype.name}"
            )
            return errors
        slug = stem[len(atype.prefix):]
        if not slug:
            errors.append(f"{rel}: filename has only the prefix; missing slug")
        elif not KEBAB.match(slug):
            errors.append(f"{rel}: '{slug}' after prefix is not kebab-case")
    else:
        if not KEBAB.match(stem):
            errors.append(f"{rel}: filename '{stem}' is not kebab-case")
    return errors


def _check_required_fields(
    atype: ArtifactType, rel: Path, fm: dict
) -> list[str]:
    errors: list[str] = []
    for field_name in atype.required_fields:
        if field_name not in fm:
            errors.append(f"{rel}: missing required frontmatter field '{field_name}'")
            continue
        value = fm[field_name]
        if value is None:
            errors.append(f"{rel}: frontmatter field '{field_name}' is empty")
        elif isinstance(value, list):
            if not [v for v in value if v is not None and str(v).strip()]:
                errors.append(f"{rel}: frontmatter field '{field_name}' is empty")
        elif isinstance(value, str) and not value.strip():
            errors.append(f"{rel}: frontmatter field '{field_name}' is empty")
    return errors


def _check_cross_refs(
    atype: ArtifactType,
    rel: Path,
    fm: dict,
    files_by_filename: dict[str, set[str]],
) -> list[str]:
    errors: list[str] = []
    for ref_field, target_type in atype.parent_fields.items():
        if ref_field not in fm:
            continue
        raw_value = fm[ref_field]
        # List-form parent fields hold multiple references; scalar form holds one.
        if ref_field in atype.list_parent_fields:
            if raw_value is None:
                continue
            if not isinstance(raw_value, list):
                errors.append(
                    f"{rel}: '{ref_field}' must be a YAML list of filenames"
                )
                continue
            ref_values = [v for v in raw_value if v is not None and str(v).strip()]
            if not ref_values:
                errors.append(
                    f"{rel}: '{ref_field}' list is empty; must contain at least one filename"
                )
                continue
        else:
            if not isinstance(raw_value, str) or not raw_value.strip():
                continue
            ref_values = [raw_value]
        for ref_value in ref_values:
            if not isinstance(ref_value, str) or not ref_value.endswith(".md"):
                errors.append(
                    f"{rel}: '{ref_field}' value '{ref_value}' must include the "
                    f"'.md' filename extension"
                )
                continue
            if ref_value not in files_by_filename.get(target_type, set()):
                errors.append(
                    f"{rel}: '{ref_field}' references '{ref_value}' but no "
                    f"{target_type} with that filename exists"
                )
    return errors


def validate_file(
    path: Path, atype: ArtifactType, files_by_filename: dict[str, set[str]]
) -> list[str]:
    """Return all error messages for the given artifact file."""
    rel = _rel(path)
    errors = _check_filename(atype, path)

    text = path.read_text(encoding="utf-8")
    fm, fm_err = parse_frontmatter(text)
    if fm_err is not None:
        errors.append(f"{rel}: {fm_err}")
        return errors
    assert fm is not None

    errors.extend(_check_required_fields(atype, rel, fm))

    if atype.name == "persona" and isinstance(fm.get("class"), str):
        cls = fm["class"]
        if cls not in PERSONA_CLASSES:
            errors.append(
                f"{rel}: 'class' must be one of "
                f"{sorted(PERSONA_CLASSES)}, got '{cls}'"
            )

    if atype.name == "adr" and isinstance(fm.get("status"), str):
        status = fm["status"]
        if status not in ADR_STATUSES:
            errors.append(
                f"{rel}: 'status' must be one of "
                f"{sorted(ADR_STATUSES)}, got '{status}'"
            )

    errors.extend(_check_cross_refs(atype, rel, fm, files_by_filename))

    if atype.is_architecture and not MERMAID_FENCE.search(text):
        errors.append(
            f"{rel}: architecture file must contain a fenced mermaid code block"
        )

    return errors


def _collect_files() -> dict[str, list[Path]]:
    # README.md files document their directory; they are not artifacts.
    return {
        atype.name: sorted(
            p for p in REPO_ROOT.glob(atype.glob) if p.name.lower() != "readme.md"
        )
        for atype in ARTIFACT_TYPES
    }


def main() -> int:
    files_by_type = _collect_files()
    files_by_filename: dict[str, set[str]] = {
        type_name: {p.name for p in paths}
        for type_name, paths in files_by_type.items()
    }
    type_lookup = {atype.name: atype for atype in ARTIFACT_TYPES}

    all_errors: list[str] = []
    for type_name, paths in files_by_type.items():
        atype = type_lookup[type_name]
        for path in paths:
            all_errors.extend(validate_file(path, atype, files_by_filename))

    if all_errors:
        for err in all_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(
            f"\n{len(all_errors)} validation error(s) found.", file=sys.stderr
        )
        return 1

    total = sum(len(paths) for paths in files_by_type.values())
    print(f"Validated {total} artifact file(s) — no issues found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
