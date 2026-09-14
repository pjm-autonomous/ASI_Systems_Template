"""Generate `traceability/TRACEABILITY.md` from artifact frontmatter.

D-46 declared the matrix generated on 2026-09-10. Nothing generated it, so what
shipped was a hand-maintained file — which is the arrangement D-46 exists to end:
the repo this standard learned from carried **316 rows with 0 populated**.

**Two defects in the shipped matrix, both found on 2026-09-13 while building
this.** They are why the generator does not simply fill in the existing columns.

*It promised columns the model cannot link.* `Architecture`, `ICD` and
`Data Spec` were columns three, five and six. None of `architecture`, `interface`
or `data-specification` declares a `parent-*` field in
`standard/artifact-schema.yaml` — there is no edge to follow. The worked example
filled them by sharing a feature-bucket directory name, which is a convention,
not a link. Inferring lineage from a directory name is exactly the heuristic
`tools/params.py` refused to apply to requirement prose, and it is refused here
for the same reason: a traced link that was guessed is worse than a blank,
because a blank is honest.

*It omitted three tiers that do have edges.* `product-requirement`,
`subsystem-requirement` and `component-requirement` were absent, so the example's
own `prodreq-`, `subreq-` and `compreq-` artifacts appeared nowhere in the file
that calls itself "the single place to check does everything trace to something
real". The example row jumped use case straight to capability requirement —
the same skip `tests/test_example.py` was written to prevent in `example/`,
surviving in the matrix that describes it.

**So the columns are derived, not declared.** The chain is read out of the schema
by following `parent-*` fields, which means adding a tier or re-pointing a parent
changes this matrix with no edit here. Types with no parent edge are listed
separately as an inventory, under a heading that says plainly that the model
declares no lineage for them.

**`--check` answers a different question from generating.** Taken from
`axs/scripts/build_trace_matrix.py`, which learned it the hard way: whether the
tracked file still matches what the generator would emit is independent of
whether the generator runs. A matrix that was correct last month and has not been
regenerated since passes every other check and is still wrong.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

try:
    from tools.schema import ArtifactType, build_bindings, load_schema
    from tools.validate import parse_frontmatter, read_repo_standard
except ImportError:  # invoked as `python tools/trace.py`
    from schema import ArtifactType, build_bindings, load_schema
    from validate import parse_frontmatter, read_repo_standard

REPO_ROOT = Path(__file__).resolve().parent.parent

MATRIX_PATH = Path("traceability") / "TRACEABILITY.md"

# Marks a parent that lives in the upstream repo. The broker verifies it exists
# (D-53); this file only shows that the chain leaves the repo here.
# Both marks are deliberately inside cp1252: a Windows console encodes stdout
# with it by default, and a generator whose own output cannot be printed on the
# platform this repo is developed on is a generator nobody runs twice.
UPSTREAM_MARK = "†"   # dagger
MISSING_MARK = "‡"    # double dagger

GENERATED_BANNER = (
    "<!-- GENERATED FILE - DO NOT EDIT.\n"
    "     Produced by tools/trace.py from artifact frontmatter (D-46).\n"
    "     Regenerate with `build-traceability`; CI runs `--check`.\n"
    "     Editing this file by hand is reverted by the next run. -->"
)


@dataclass(frozen=True)
class Artifact:
    filename: str
    type_name: str
    rel: Path
    frontmatter: dict


# Type names that do not title-case into what engineers actually call them.
DISPLAY_NAMES: dict[str, str] = {
    "adr": "ADR",
    "param": "Parameter",
    "interface": "ICD",
}


def humanize(type_name: str) -> str:
    """`product-requirement` -> `Product Requirement`; `adr` -> `ADR`."""
    override = DISPLAY_NAMES.get(type_name)
    if override:
        return override
    return " ".join(word.capitalize() for word in type_name.split("-"))


def parent_edges(schema: dict) -> dict[str, list[tuple[str, str, bool]]]:
    """Type -> [(field, parent type, is_external)], lineage fields only.

    Only `parent-*` fields count as lineage. `use-case` also declares
    `primary-actors: persona`, which is a cast list rather than a parent — D-20
    names the `parent-*` prefix as the lineage convention, and treating an actor
    reference as ancestry would duplicate every use case per actor.
    """
    types = schema.get("types") or {}
    by_prefix = {
        decl["prefix"]: name
        for name, decl in types.items()
        if decl.get("prefix")
    }
    edges: dict[str, list[tuple[str, str, bool]]] = {}
    for name, decl in types.items():
        found: list[tuple[str, str, bool]] = []
        for field, parent_type in (decl.get("parents") or {}).items():
            if field.startswith("parent-"):
                found.append((field, parent_type, False))
        for field, prefix in (decl.get("external-parents") or {}).items():
            if not field.startswith("parent-"):
                continue
            parent_type = by_prefix.get(prefix)
            if parent_type:
                found.append((field, parent_type, True))
        edges[name] = found
    return edges


def chain_types(schema: dict) -> tuple[str, ...]:
    """The traceable chain, ordered ancestor-first, derived from the schema.

    A type participates when it declares a lineage parent or is named as one.
    Everything else is unlinked and reported separately rather than given a
    column that can only ever be blank.
    """
    edges = parent_edges(schema)
    participating: set[str] = set()
    parents_of: dict[str, set[str]] = defaultdict(set)
    for name, found in edges.items():
        for _, parent_type, _ in found:
            participating.add(name)
            participating.add(parent_type)
            parents_of[name].add(parent_type)

    # Depth from a root orders the chain without assuming it is linear.
    def depth(name: str, seen: frozenset[str] = frozenset()) -> int:
        if name in seen:
            return 0                      # defensive: a cycle stops here
        ancestors = parents_of.get(name) or set()
        if not ancestors:
            return 0
        return 1 + max(depth(a, seen | {name}) for a in ancestors)

    return tuple(sorted(participating, key=lambda n: (depth(n), n)))


def unlinked_types(schema: dict) -> tuple[str, ...]:
    """Types the model declares no lineage for, in schema order."""
    linked = set(chain_types(schema))
    return tuple(n for n in (schema.get("types") or {}) if n not in linked)


def _as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if v is not None and str(v).strip()]
    text = str(value).strip()
    return [text] if text else []


def collect_artifacts(
    bindings: tuple[ArtifactType, ...], root: Path
) -> dict[str, Artifact]:
    """Every artifact in the repo, keyed by filename.

    Filenames are unique repo-wide (D-22), which is what makes a filename-keyed
    index safe and is why cross-references carry no directory prefix.
    """
    found: dict[str, Artifact] = {}
    for binding in bindings:
        for pattern in binding.glob:
            for path in sorted(root.glob(pattern)):
                if not path.is_file() or path.name.lower() == "readme.md":
                    continue
                fm, err = parse_frontmatter(path.read_text(encoding="utf-8"))
                found[path.name] = Artifact(
                    filename=path.name,
                    type_name=binding.name,
                    rel=path.relative_to(root),
                    frontmatter=fm if err is None and fm else {},
                )
    return found


def _parent_refs(
    artifact: Artifact, edges: dict[str, list[tuple[str, str, bool]]]
) -> list[tuple[str, str, bool]]:
    """(filename, parent type, is_external) for each parent this artifact names."""
    refs: list[tuple[str, str, bool]] = []
    for field, parent_type, external in edges.get(artifact.type_name, []):
        for name in _as_list(artifact.frontmatter.get(field)):
            refs.append((name, parent_type, external))
    return refs


def build_rows(
    artifacts: dict[str, Artifact],
    chain: tuple[str, ...],
    edges: dict[str, list[tuple[str, str, bool]]],
) -> list[tuple[str, ...]]:
    """One row per root-to-leaf path through the lineage graph.

    An artifact with several parents yields several rows — parents are
    many-to-many (D-20), and collapsing them would hide one of the links.
    """
    index = {name: position for position, name in enumerate(chain)}
    in_chain = {
        name: art for name, art in artifacts.items() if art.type_name in index
    }

    has_child: set[str] = set()
    for artifact in in_chain.values():
        for parent_name, _, _ in _parent_refs(artifact, edges):
            has_child.add(parent_name)

    def paths_up(
        artifact: Artifact, seen: frozenset[str]
    ) -> list[list[tuple[str, str]]]:
        """Every upward path from this artifact, as (cell text, type) pairs."""
        here = (artifact.filename, artifact.type_name)
        refs = _parent_refs(artifact, edges)
        if not refs or artifact.filename in seen:
            return [[here]]
        out: list[list[tuple[str, str]]] = []
        for parent_name, parent_type, external in refs:
            parent = in_chain.get(parent_name)
            if parent is None:
                # The chain leaves the repo, or names something that is not
                # here. Either way it stops: this file cannot show ancestors it
                # cannot read. `tools/broker.py` is what says whether an
                # upstream parent exists.
                mark = UPSTREAM_MARK if external else MISSING_MARK
                out.append([(f"{parent_name} {mark}", parent_type), here])
                continue
            for prefix in paths_up(parent, seen | {artifact.filename}):
                out.append(prefix + [here])
        return out

    rows: set[tuple[str, ...]] = set()
    for artifact in in_chain.values():
        if artifact.filename in has_child:
            continue                      # appears in its descendants' rows
        for path in paths_up(artifact, frozenset()):
            cells = [""] * len(chain)
            for text, type_name in path:
                position = index.get(type_name)
                if position is not None:
                    cells[position] = text
            rows.add(tuple(cells))
    return sorted(rows)


def render(
    rows: list[tuple[str, ...]],
    chain: tuple[str, ...],
    artifacts: dict[str, Artifact],
    unlinked: tuple[str, ...],
) -> str:
    """Render the matrix. Deterministic: same inputs, byte-identical output."""
    lines: list[str] = [GENERATED_BANNER, "", "# Traceability Matrix", ""]

    counted = sum(1 for a in artifacts.values() if a.type_name in set(chain))
    lines += [
        f"{counted} artifact(s) across {len(chain)} traceable tier(s), "
        f"{len(rows)} lineage path(s).",
        "",
    ]

    lines.append("| " + " | ".join(humanize(t) for t in chain) + " |")
    lines.append("|" + "---|" * len(chain))
    if rows:
        for row in rows:
            lines.append("| " + " | ".join(cell or "" for cell in row) + " |")
    else:
        lines.append("|" + " |" * len(chain))
        lines += [
            "",
            "**No artifacts yet.** The row above is the empty shape, not a gap "
            "to fill in by hand — add artifacts and regenerate.",
        ]
    # A bullet list, not two-space line breaks: the `trailing-whitespace` hook
    # strips those, and the stripped file would then differ from what this
    # function emits - a `--check` that could never pass.
    lines += [
        "",
        f"- `{UPSTREAM_MARK}` parent is in the upstream repo; its existence is "
        f"checked by `tools/broker.py`, not here.",
        f"- `{MISSING_MARK}` named as a parent but not found in this repo and "
        f"not declared external — `validate-artifacts` reports it.",
        "",
    ]

    # --- Types the model declares no lineage for ---------------------------
    present = defaultdict(list)
    for artifact in sorted(artifacts.values(), key=lambda a: a.filename):
        if artifact.type_name in unlinked:
            present[artifact.type_name].append(artifact)

    lines += ["## Artifacts with no declared lineage", ""]
    if present:
        lines += [
            "These types declare no `parent-*` field in the artifact schema, so "
            "there is no edge to trace. They are listed rather than given a "
            "matrix column, because a column that can only be blank reads as a "
            "gap and a guessed link reads as a fact.",
            "",
            "| Type | Artifact |",
            "|---|---|",
        ]
        for type_name in sorted(present):
            for artifact in present[type_name]:
                lines.append(f"| {humanize(type_name)} | {artifact.filename} |")
    else:
        lines.append("None in this repo.")

    # Exactly one trailing newline, and no doubled blank lines.
    # `end-of-file-fixer` and markdownlint MD012 both rewrite a file that
    # breaks either rule, and a rewritten file can never again equal what this
    # function emits - the same --check-fails-forever trap as trailing
    # whitespace, arriving by a different hook.
    while lines and not lines[-1].strip():
        lines.pop()
    collapsed: list[str] = []
    for line in lines:
        if not line.strip() and collapsed and not collapsed[-1].strip():
            continue
        collapsed.append(line)
    return "\n".join(collapsed) + "\n"


def generate(root: Path | None = None) -> str:
    """Build the matrix text for a repo rooted at `root`."""
    root = root or REPO_ROOT
    schema = load_schema()
    decl, _ = read_repo_standard(root)
    repo_tiers = decl.get("tiers") if isinstance(decl.get("tiers"), list) else None
    packets = decl.get("packets") if isinstance(decl.get("packets"), dict) else None
    bindings = build_bindings(schema, repo_tiers=repo_tiers, packets=packets)

    artifacts = collect_artifacts(bindings, root)
    chain = chain_types(schema)
    rows = build_rows(artifacts, chain, parent_edges(schema))
    return render(rows, chain, artifacts, unlinked_types(schema))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate traceability/TRACEABILITY.md from frontmatter."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="write nothing; fail if the tracked file is not what would be "
             "emitted now (currency is a separate failure from correctness)",
    )
    parser.add_argument(
        "--root", type=Path, default=REPO_ROOT,
        help="repo root to generate for (default: this repo)",
    )
    args = parser.parse_args(argv)

    expected = generate(args.root)
    target = args.root / MATRIX_PATH

    if args.check:
        if not target.is_file():
            print(f"ERROR: {MATRIX_PATH} does not exist — run `build-traceability`",
                  file=sys.stderr)
            return 1
        if target.read_text(encoding="utf-8").replace("\r\n", "\n") != expected:
            print(
                f"ERROR: {MATRIX_PATH} is out of date — regenerate it with "
                f"`build-traceability`. A matrix that was right last month and "
                f"has not been regenerated since passes every other check and "
                f"is still wrong.",
                file=sys.stderr,
            )
            return 1
        print(f"{MATRIX_PATH} is current.")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(expected, encoding="utf-8")
    print(f"Wrote {MATRIX_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
