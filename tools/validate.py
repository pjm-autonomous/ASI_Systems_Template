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

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

try:
    from tools import broker as brk
    from tools import maturity as mat
    from tools.schema import ArtifactType, SchemaError, build_bindings, load_schema
except ImportError:  # invoked as `python tools/validate.py`, not `-m tools.validate`
    import broker as brk
    import maturity as mat
    from schema import ArtifactType, SchemaError, build_bindings, load_schema

REPO_ROOT = Path(__file__).resolve().parent.parent

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MERMAID_FENCE = re.compile(r"^```mermaid\s*$", re.MULTILINE)

PERSONA_CLASSES = {"developer-integrator", "runtime-operator", "external-system"}


def _default_bindings() -> tuple[ArtifactType, ...]:
    """Every binding with all schema tiers active — the template's own view.

    Exposed as ARTIFACT_TYPES for callers that just want the model. `main()`
    resolves against the repo's declaration instead, which is narrower.
    """
    try:
        return build_bindings(load_schema())
    except SchemaError:
        return ()


ARTIFACT_TYPES: tuple[ArtifactType, ...] = _default_bindings()


# The artifact model is DATA, not code: see standard/artifact-schema.yaml.
# `ArtifactType` here is one resolved (type, tier) binding produced from it.
# Everything below this point checks bindings and does not know how they
# were declared.


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
        # Every parent field is many-to-many capable (harvest item H2: the
        # one-parent-only model was a Jira limitation, and both GitHub and Jama
        # allow m:m). A single parent may still be written as a plain scalar -
        # requiring list syntax for one item is friction with no benefit - so a
        # scalar is normalized to a one-element list here.
        if ref_field in atype.list_parent_fields:
            if raw_value is None:
                continue
            if isinstance(raw_value, str):
                raw_value = [raw_value] if raw_value.strip() else []
            elif not isinstance(raw_value, list):
                errors.append(
                    f"{rel}: '{ref_field}' must be a filename or a YAML list "
                    f"of filenames"
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

def _check_enum_fields(atype: ArtifactType, rel: Path, fm: dict) -> list[str]:
    """Check every field the schema constrains to a vocabulary.

    Replaces what used to be one hardcoded branch per enum. A new vocabulary is
    now added in the schema and needs no code change.
    """
    errors: list[str] = []
    for field_name, allowed in atype.enum_fields.items():
        if field_name not in fm:
            continue
        raw = fm[field_name]
        if raw is None:
            continue
        # A multi-select field may arrive as a YAML list or a comma-separated
        # string; check each member either way.
        if isinstance(raw, list):
            members = [str(v).strip() for v in raw if v is not None]
        elif isinstance(raw, str):
            members = (
                [part.strip() for part in raw.split(",")]
                if "," in raw else [raw.strip()]
            )
        else:
            members = [str(raw)]
        for member in members:
            if member and member not in allowed:
                errors.append(
                    f"{rel}: '{field_name}' must be one of "
                    f"{sorted(allowed)}, got '{member}'"
                )
    return errors


def collect_external_refs(
    atype: ArtifactType, rel: Path, fm: dict
) -> list[tuple[Path, str, str]]:
    """Gather (artifact, field, referenced filename) for cross-repo parents.

    Shape checking happens in `_check_external_refs`; this only harvests the
    values so the broker can verify they exist upstream.
    """
    out: list[tuple[Path, str, str]] = []
    for ref_field in atype.external_parent_fields:
        raw = fm.get(ref_field)
        if raw is None:
            continue
        values = raw if isinstance(raw, list) else [raw]
        for value in values:
            if value is None or not str(value).strip():
                continue
            out.append((rel, ref_field, str(value).strip()))
    return out


def _check_external_refs(atype: ArtifactType, rel: Path, fm: dict) -> list[str]:
    """Shape-check references whose target lives in another repo.

    A sub-system requirement's parent is a system requirement mastered in the
    product/system repo, so it cannot be resolved against local files. The
    reference is authoritative in the requirements-management tool; here we can
    only confirm it is well formed.
    """
    errors: list[str] = []
    for ref_field, prefix in atype.external_parent_fields.items():
        if ref_field not in fm:
            continue
        raw = fm[ref_field]
        values = raw if isinstance(raw, list) else [raw]
        for value in values:
            if value is None or not str(value).strip():
                continue
            value = str(value).strip()
            if not value.endswith(".md"):
                errors.append(
                    f"{rel}: '{ref_field}' value '{value}' must include the "
                    f"'.md' filename extension"
                )
                continue
            if not value.startswith(prefix):
                errors.append(
                    f"{rel}: '{ref_field}' value '{value}' must start with "
                    f"'{prefix}'"
                )
                continue
            slug = value[len(prefix):-len(".md")]
            if not slug or not KEBAB.match(slug):
                errors.append(
                    f"{rel}: '{ref_field}' value '{value}' is not a kebab-case "
                    f"'{prefix}<slug>.md' reference"
                )
    return errors


def validate_file(
    path: Path,
    atype: ArtifactType,
    files_by_filename: dict[str, set[str]],
    check_maturity: bool = False,
    maturity_out: dict[str, list] | None = None,
) -> list[str]:
    """Return all error messages for the given artifact file.

    When `check_maturity` is set, the artifact's maturity declaration is checked
    and recorded into `maturity_out` keyed by tier, so the caller can apply the
    cross-tier gating rule afterwards.
    """
    rel = _rel(path)
    errors = _check_filename(atype, path)

    text = path.read_text(encoding="utf-8")
    fm, fm_err = parse_frontmatter(text)
    if fm_err is not None:
        errors.append(f"{rel}: {fm_err}")
        return errors
    assert fm is not None

    errors.extend(_check_required_fields(atype, rel, fm))

    errors.extend(_check_enum_fields(atype, rel, fm))
    errors.extend(_check_external_refs(atype, rel, fm))

    errors.extend(_check_cross_refs(atype, rel, fm, files_by_filename))

    if atype.is_architecture and not MERMAID_FENCE.search(text):
        errors.append(
            f"{rel}: architecture file must contain a fenced mermaid code block"
        )

    if check_maturity:
        slug = path.stem
        errors.extend(
            mat.check_artifact(rel, slug, text, fm, root=REPO_ROOT)
        )
        if maturity_out is not None:
            maturity_out.setdefault(atype.tier, []).append(
                (rel, mat.read_maturity(text, fm))
            )

    return errors

# ---------------------------------------------------------------------------
# Conformance declaration
# ---------------------------------------------------------------------------
# `repo-standard.yaml` records which template version this repo was cut from and
# which parts of the standard it implements. Review item A7: consumption is a
# one-way "Use this template" copy with no version stamp, so a downstream repo
# drifts with no way to detect it. Reading the declaration here is what turns the
# standard from a convention into something enforced.

REPO_STANDARD_NAME = "repo-standard.yaml"
VERSION_NAME = "VERSION"

# Placeholder written by the template; /new-project replaces it at instantiation.
STAMP_PLACEHOLDER = "TEMPLATE"


def read_repo_standard(root: Path | None = None) -> tuple[dict, list[str]]:
    """Load repo-standard.yaml. Returns (declaration, errors).

    A missing file is not fatal - it yields one advisory error and an empty
    declaration, so a repo predating the standard still validates its artifacts.
    """
    root = root or REPO_ROOT
    path = root / REPO_STANDARD_NAME
    if not path.exists():
        return {}, [
            f"{REPO_STANDARD_NAME}: missing - this repo records no template "
            f"version, so drift from the standard cannot be detected (see "
            f"standard/ decision record A7)"
        ]
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return {}, [f"{REPO_STANDARD_NAME}: unreadable - {exc}"]
    if not isinstance(data, dict):
        return {}, [f"{REPO_STANDARD_NAME}: must be a YAML mapping"]
    return data, []


def _check_conformance(decl: dict, root: Path | None = None) -> list[str]:
    """Validate the declaration itself, and flag an un-stamped instantiation."""
    root = root or REPO_ROOT
    errors: list[str] = []
    if not decl:
        return errors

    standard = decl.get("standard") or {}
    if not isinstance(standard, dict):
        return [f"{REPO_STANDARD_NAME}: 'standard' must be a mapping"]

    declared = standard.get("version")
    if not declared:
        errors.append(f"{REPO_STANDARD_NAME}: 'standard.version' is not set")

    # In the template itself the stamp is the literal placeholder. Downstream that
    # means /new-project never ran, which is exactly the drift A7 describes.
    is_template = (root / VERSION_NAME).exists() and (root / "standard").is_dir()
    for key in ("commit", "instantiated"):
        if standard.get(key) == STAMP_PLACEHOLDER and not is_template:
            errors.append(
                f"{REPO_STANDARD_NAME}: 'standard.{key}' is still the "
                f"'{STAMP_PLACEHOLDER}' placeholder - run /new-project to stamp "
                f"this repo with the template version it was created from"
            )

    # A declared version that no longer matches the template's VERSION means the
    # repo is behind (or ahead of) the standard. Advisory in the template itself.
    version_file = root / VERSION_NAME
    if is_template and version_file.exists() and declared:
        actual = version_file.read_text(encoding="utf-8").strip()
        if actual and declared != actual:
            errors.append(
                f"{REPO_STANDARD_NAME}: declares standard.version "
                f"'{declared}' but {VERSION_NAME} says '{actual}'"
            )

    tiers = decl.get("tiers")
    if tiers is not None and not isinstance(tiers, list):
        errors.append(f"{REPO_STANDARD_NAME}: 'tiers' must be a list")

    packets = decl.get("packets")
    if packets is not None and not isinstance(packets, dict):
        errors.append(f"{REPO_STANDARD_NAME}: 'packets' must be a mapping")

    conventions = decl.get("conventions") or {}
    if isinstance(conventions, dict):
        fmt = conventions.get("table-format")
        if fmt is not None and fmt not in {"markdown", "html", "both"}:
            errors.append(
                f"{REPO_STANDARD_NAME}: 'conventions.table-format' must be "
                f"markdown, html or both - got '{fmt}'"
            )
        diagram = conventions.get("diagram-format")
        if diagram is not None and diagram not in {"mermaid", "puml"}:
            errors.append(
                f"{REPO_STANDARD_NAME}: 'conventions.diagram-format' must be "
                f"mermaid or puml - got '{diagram}'"
            )

    return errors


def _collect_files(
    bindings: tuple[ArtifactType, ...],
) -> dict[str, list[Path]]:
    """Map each binding's label to the files it governs.

    Globs are prefix-anchored and scoped to one subdirectory, so index files
    (README.md and friends) never match and `**` cannot wander into docs/,
    archive/ or example/.
    """
    out: dict[str, list[Path]] = {}
    for binding in bindings:
        found: set[Path] = set()
        for pattern in binding.glob:
            found.update(
                path for path in REPO_ROOT.glob(pattern)
                if path.is_file() and path.name.lower() != "readme.md"
            )
        out[binding.label] = sorted(found)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate-artifacts",
        description="Validate artifacts against the ASI systems engineering standard.",
    )
    parser.add_argument(
        "--require-parents", action="store_true",
        help="fail when a declared parent repo cannot be resolved (use in CI; "
             "locally an unreachable parent degrades to a shape-only check)",
    )
    parser.add_argument(
        "--no-fetch", action="store_true",
        help="never reach the network; use a sibling clone or cached index only",
    )
    args = parser.parse_args(argv)

    # CI and Windows consoles capture with the locale encoding, which mangles
    # the non-ASCII characters in these messages. Force UTF-8 where we can.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass   # already UTF-8, or a stream that cannot be reconfigured

    decl, decl_errors = read_repo_standard()
    all_unknown_tier_errors: list[str] = []

    # Resolve the schema against what this repo says it implements. Tiers and
    # packets it does not declare are simply not validated - omitting a tier is
    # a legitimate choice, not a gap.
    try:
        schema = load_schema()
    except SchemaError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    repo_tiers = decl.get("tiers") if isinstance(decl.get("tiers"), list) else None

    # A declared tier the schema does not know yields zero bindings, so the repo
    # validates nothing and CI passes green. Observed 2026-09-12 while re-tiering
    # this template: `tiers: [capability, interfaces, architecture]` against a
    # schema still declaring product/system/subsystem/component reported
    # "tiers: none" and exit 0. Silence must not look like success.
    if repo_tiers is not None:
        known = set(schema.get("tiers") or ())
        unknown = [t for t in repo_tiers if t not in known]
        if unknown:
            for tier in unknown:
                all_unknown_tier_errors.append(
                    f"{REPO_STANDARD_NAME}: declares tier '{tier}', which the "
                    f"artifact schema does not define (known tiers: "
                    f"{sorted(known)}) — nothing would be validated for it"
                )
        elif not [t for t in repo_tiers if t in known]:
            all_unknown_tier_errors.append(
                f"{REPO_STANDARD_NAME}: 'tiers' is empty after matching against "
                f"the schema, so no artifact would be validated at all"
            )
    packets = decl.get("packets") if isinstance(decl.get("packets"), dict) else None
    try:
        bindings = build_bindings(schema, repo_tiers=repo_tiers, packets=packets)
    except SchemaError as exc:
        print(f"ERROR: artifact-schema.yaml: {exc}", file=sys.stderr)
        return 1

    files_by_label = _collect_files(bindings)

    # Cross-references target a TYPE, not a tier: a parent field naming a system
    # requirement resolves whether that requirement sits at the system or the
    # sub-system tier. So the lookup index is keyed by type name, merging every
    # tier the type occupies.
    files_by_filename: dict[str, set[str]] = {}
    for binding in bindings:
        files_by_filename.setdefault(binding.name, set()).update(
            path.name for path in files_by_label[binding.label]
        )

    # Maturity gating is opt-in: a repo that does not run the AxS M1-M4 model
    # is never failed for lacking maturity declarations.
    gate_maturity = bool((decl.get("packets") or {}).get("maturity-gates", False))
    maturity_by_tier: dict[str, list] = {}

    all_errors: list[str] = list(decl_errors)
    all_errors.extend(all_unknown_tier_errors)
    all_errors.extend(_check_conformance(decl))
    external_refs: dict[str, list[tuple[Path, str, str]]] = {}
    for binding in bindings:
        for path in files_by_label[binding.label]:
            all_errors.extend(
                validate_file(
                    path,
                    binding,
                    files_by_filename,
                    check_maturity=gate_maturity,
                    maturity_out=maturity_by_tier,
                )
            )
            if binding.external_parent_fields:
                text = path.read_text(encoding="utf-8")
                fm, err = parse_frontmatter(text)
                if err is None and fm is not None:
                    refs = collect_external_refs(binding, _rel(path), fm)
                    if refs:
                        external_refs.setdefault(binding.tier, []).extend(refs)

    # M4 at one tier requires M4 at the tier above it - a rule that spans files
    # and so cannot be checked while validating any single one.
    if gate_maturity:
        all_errors.extend(
            mat.check_tier_gating(maturity_by_tier, list(schema["tiers"]))
        )

    # Upward enforcement: every parent reference leaving this repo must exist in
    # the declared parent repo. Locally this degrades when the parent is
    # unreachable; in CI (--require-parents) it does not.
    broker_notes: list[str] = []
    if external_refs:
        try:
            parents = brk.parse_parents(decl)
        except brk.BrokerError as exc:
            all_errors.append(f"{REPO_STANDARD_NAME}: {exc}")
            parents = ()
        errs, broker_notes = brk.check_external_parents(
            external_refs,
            parents,
            allow_fetch=not args.no_fetch,
            require_resolution=args.require_parents,
            root=REPO_ROOT,
        )
        all_errors.extend(errs)

    if all_errors:
        for err in all_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(
            f"\n{len(all_errors)} validation error(s) found.",
            file=sys.stderr,
        )
        return 1

    total = sum(len(paths) for paths in files_by_label.values())
    version = (decl.get("standard") or {}).get("version", "unknown")
    tiers = ", ".join(sorted({b.tier for b in bindings})) or "none"
    for note in broker_notes:
        print(f"  note: {note}")
    gates = "maturity-gated" if gate_maturity else "no maturity gate"
    print(
        f"Validated {total} artifact file(s) against standard v{version} "
        f"[schema v{schema.get('schema-version')}; tiers: {tiers}; {gates}] "
        f"- no issues found."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
