"""Load the artifact schema and resolve it against a repo's declaration.

The schema (`standard/artifact-schema.yaml`) is the normative statement of the
artifact model; this module turns it into the bindings `validate.py` checks.

Two ideas do the work:

**Tier-derived paths.** An artifact type declares which *tiers* it may occupy,
never a directory path. The tier name is the directory name, so a location is
computed:

    <tier>/<subdir>/**/<prefix>*.md

Architecture level numbers appear nowhere in the schema — a repo declares one
`level:` in `repo-standard.yaml` and which `tiers:` it masters. Renumbering the
architecture is therefore a one-line change rather than a repo-wide migration.
This matters because PRAK stores the level on every artifact *and* validates it
against the directory, whose own comment concedes the two are "the same
statement made twice."

**One binding per (type, tier).** A type occupying several tiers may need
different fields at each — `param` and `adr` appear at most tiers, and an ADR at
the capability tier answers to a different parent than one at the component
tier. A flat list of globs cannot express that; a binding per tier can. Bindings
keep the shared type *name*, so a cross-reference resolves to "an ADR" whatever
tier it sits at.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

SCHEMA_PATH = REPO_ROOT / "standard" / "artifact-schema.yaml"
# A downstream repo has no standard/ directory; it carries the resolved schema
# at the repo root instead. Checked in this order.
FALLBACK_SCHEMA_PATH = REPO_ROOT / "artifact-schema.yaml"

# Packets that are always enforced, whatever the repo declares.
CORE_PACKET = "core"


class SchemaError(Exception):
    """The schema itself is malformed — distinct from an artifact being wrong."""


@dataclass(frozen=True)
class ArtifactType:
    """One (type, tier) binding, resolved and ready to validate against.

    Field names match the shape `validate.py`'s checks already expect, so the
    move from hardcoded declarations to schema-driven ones changed how these are
    built and nothing about how they are used.
    """

    name: str
    tier: str
    glob: tuple[str, ...]
    prefix: str
    required_fields: tuple[str, ...]
    parent_fields: dict[str, str] = field(default_factory=dict)
    list_parent_fields: frozenset[str] = field(default_factory=frozenset)
    external_parent_fields: dict[str, str] = field(default_factory=dict)
    enum_fields: dict[str, frozenset[str]] = field(default_factory=dict)
    is_architecture: bool = False
    packet: str = CORE_PACKET

    @property
    def label(self) -> str:
        """`name` for a single-tier type, `name@tier` when it spans tiers."""
        return f"{self.name}@{self.tier}"


def load_schema(path: Path | None = None) -> dict[str, Any]:
    """Read and sanity-check the schema file."""
    if path is None:
        path = SCHEMA_PATH if SCHEMA_PATH.exists() else FALLBACK_SCHEMA_PATH
    if not path.exists():
        raise SchemaError(
            f"artifact schema not found (looked for {SCHEMA_PATH} and "
            f"{FALLBACK_SCHEMA_PATH}) — without it there is no artifact model "
            f"to validate against"
        )
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise SchemaError(f"{path.name}: unreadable — {exc}") from exc
    if not isinstance(data, dict):
        raise SchemaError(f"{path.name}: must be a YAML mapping")
    for key in ("schema-version", "tiers", "types"):
        if key not in data:
            raise SchemaError(f"{path.name}: missing required key '{key}'")
    if not isinstance(data["types"], dict):
        raise SchemaError(f"{path.name}: 'types' must be a mapping")
    if not isinstance(data["tiers"], list):
        raise SchemaError(f"{path.name}: 'tiers' must be a list")
    return data


def _resolve_enums(
    spec_enums: dict[str, str], vocab: dict[str, list], type_name: str
) -> dict[str, frozenset[str]]:
    """Turn `field -> enum name` into `field -> allowed values`."""
    out: dict[str, frozenset[str]] = {}
    for field_name, enum_name in spec_enums.items():
        values = vocab.get(enum_name)
        if values is None:
            raise SchemaError(
                f"type '{type_name}' references unknown enum '{enum_name}'"
            )
        out[field_name] = frozenset(str(v) for v in values)
    return out


def _merge_per_tier(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """Merge a per-tier block over the base type spec.

    `required`, `list-parents` are additive — a tier adds fields, never removes
    the type's shared ones. Mappings are merged key-wise.
    """
    merged = dict(base)
    for key, value in overlay.items():
        if key in ("required", "list-parents"):
            merged[key] = list(base.get(key) or []) + list(value or [])
        elif key in ("parents", "external-parents", "enums"):
            combined = dict(base.get(key) or {})
            combined.update(value or {})
            merged[key] = combined
        else:
            merged[key] = value
    return merged


def build_bindings(
    schema: dict[str, Any],
    repo_tiers: list[str] | None = None,
    packets: dict[str, bool] | None = None,
) -> tuple[ArtifactType, ...]:
    """Resolve the schema into one binding per (type, tier) this repo validates.

    `repo_tiers` None means "every tier in the schema" — the template itself, and
    the safe default for a repo that declares nothing. `packets` gates optional
    types; the core packet is always on.
    """
    vocab: dict[str, list] = schema.get("enums") or {}
    schema_tiers: list[str] = list(schema["tiers"])
    active_tiers = schema_tiers if repo_tiers is None else [
        t for t in schema_tiers if t in repo_tiers
    ]
    packets = packets or {}

    bindings: list[ArtifactType] = []
    for type_name, raw in sorted(schema["types"].items()):
        if not isinstance(raw, dict):
            raise SchemaError(f"type '{type_name}': declaration must be a mapping")

        packet = raw.get("packet", CORE_PACKET)
        if packet != CORE_PACKET and not packets.get(packet, True):
            continue   # repo opted out of this packet

        declared_tiers = raw.get("tiers")
        if not declared_tiers:
            raise SchemaError(f"type '{type_name}': 'tiers' must be non-empty")
        for tier in declared_tiers:
            if tier not in schema_tiers:
                raise SchemaError(
                    f"type '{type_name}': unknown tier '{tier}' "
                    f"(schema tiers: {schema_tiers})"
                )

        subdir = raw.get("subdir")
        if not subdir:
            raise SchemaError(f"type '{type_name}': 'subdir' is required")
        prefix = raw.get("prefix", "")

        per_tier: dict[str, Any] = raw.get("per-tier") or {}
        for tier in declared_tiers:
            if tier not in active_tiers:
                continue   # tier not mastered by this repo
            spec = _merge_per_tier(raw, per_tier.get(tier) or {})

            # Prefix-anchored so README.md and other index files never match.
            # `**` is scoped to one known subdirectory, which is what makes it
            # safe here: it covers both flat catalogs and feature-bucketed
            # trees without needing a per-type layout flag.
            #
            # subdir "." means the tier directory IS the home - used where the
            # tier and the artifact type are the same thing (interfaces,
            # architecture), so the path stays `interfaces/**` not
            # `interfaces/./**`.
            base = tier if subdir == "." else f"{tier}/{subdir}"
            pattern = f"{base}/**/{prefix}*.md"

            bindings.append(
                ArtifactType(
                    name=type_name,
                    tier=tier,
                    glob=(pattern,),
                    prefix=prefix,
                    required_fields=tuple(dict.fromkeys(spec.get("required") or ())),
                    parent_fields=dict(spec.get("parents") or {}),
                    list_parent_fields=frozenset(spec.get("list-parents") or ()),
                    external_parent_fields=dict(spec.get("external-parents") or {}),
                    enum_fields=_resolve_enums(
                        spec.get("enums") or {}, vocab, type_name
                    ),
                    is_architecture=bool(spec.get("architecture", False)),
                    packet=packet,
                )
            )
    return tuple(bindings)
