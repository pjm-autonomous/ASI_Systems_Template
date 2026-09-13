"""Cross-repo parent brokering — upward enforcement across architecture tiers.

The problem: a sub-system requirement's parent is a system requirement mastered
in another repo. Nothing local can confirm it exists, so the reference has been
shape-checked only — `sysreq-<kebab>.md` and nothing more. A typo, a rename, or
a deleted parent all pass.

The solution, and it is simpler than it looked: **enforce upward, not downward.**

A child repo always knows who its parent is, so it can always check that its
parent references resolve. The reverse — does every parent have children, i.e.
coverage — needs the parent to know about every child, which needs a registry
and is a much bigger problem. Upward enforcement is the piece that prevents
broken traces from being committed, and it needs nothing but a parent repo name
in a config file.

    repo-standard.yaml
      parents:
        - tier: system
          repo: asirobots/prak-v-model
          ref: main

Resolution order, first hit wins:

1. **Sibling clone** — `../prak-v-model`. Zero network, and the common case on a
   developer machine where both repos are checked out side by side.
2. **Cached index** — `.cache/parent-index/<owner>-<repo>.json`, written by a
   previous fetch. Keeps pre-commit fast and lets it work offline.
3. **GitHub API** — the Git Trees API returns the parent's whole file list in one
   request, with no clone. This is the authoritative path, used in CI.

If none is available the check degrades to shape-only and says so. A missing
network must not block a commit; a *wrong* reference should.

Enforcement points differ deliberately:

| Where | Mode | Why |
|-------|------|-----|
| pre-commit | sibling clone or cache, else skip | fast, offline-tolerant |
| CI | fetch required, no skipping | authoritative gate before merge |
"""
from __future__ import annotations

import json
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CACHE_DIR = REPO_ROOT / ".cache" / "parent-index"
CACHE_TTL_S = 24 * 60 * 60          # a day; parents do not move often

# Emitted by `emit-artifact-index` in the parent repo, committed at its root.
INDEX_FILENAME = "artifact-index.json"

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class BrokerError(Exception):
    """The parent declaration is malformed."""


@dataclass(frozen=True)
class ParentRepo:
    """One declared parent, from repo-standard.yaml `parents:`."""

    tier: str
    repo: str                       # "owner/name"
    ref: str = "main"
    prefixes: tuple[str, ...] = ()  # artifact prefixes to index; empty = all

    @property
    def name(self) -> str:
        return self.repo.split("/")[-1]

    @property
    def cache_path(self) -> Path:
        return CACHE_DIR / f"{self.repo.replace('/', '-')}.json"


@dataclass(frozen=True)
class Resolution:
    """What a lookup attempt produced."""

    parent: ParentRepo
    filenames: frozenset[str]
    source: str                     # sibling | cache | api | unavailable
    detail: str = ""

    @property
    def available(self) -> bool:
        return self.source != "unavailable"


def parse_parents(decl: dict) -> tuple[ParentRepo, ...]:
    """Read the `parents:` block from a repo-standard declaration."""
    raw = decl.get("parents")
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise BrokerError("'parents' must be a list")
    out: list[ParentRepo] = []
    for entry in raw:
        if not isinstance(entry, dict):
            raise BrokerError("each 'parents' entry must be a mapping")
        for key in ("tier", "repo"):
            if not entry.get(key):
                raise BrokerError(f"'parents' entry missing '{key}'")
        repo = str(entry["repo"])
        if "/" not in repo:
            raise BrokerError(
                f"'parents.repo' must be 'owner/name', got '{repo}'"
            )
        out.append(
            ParentRepo(
                tier=str(entry["tier"]),
                repo=repo,
                ref=str(entry.get("ref", "main")),
                prefixes=tuple(entry.get("prefixes") or ()),
            )
        )
    return tuple(out)


# ---------------------------------------------------------------------------
# Resolution strategies
# ---------------------------------------------------------------------------

def _from_sibling(parent: ParentRepo, root: Path | None = None) -> Resolution | None:
    """Look for the parent checked out beside this repo."""
    sibling = (root or REPO_ROOT).parent / parent.name
    if not sibling.is_dir():
        return None

    # Prefer the parent's published index when it has one: it is what the parent
    # asserts about itself, rather than what its working tree happens to hold.
    index = sibling / INDEX_FILENAME
    if index.is_file():
        try:
            data = json.loads(index.read_text(encoding="utf-8"))
            names = frozenset(data.get("artifacts", {}))
            if names:
                return Resolution(parent, names, "sibling",
                                  f"{sibling.name}/{INDEX_FILENAME}")
        except (OSError, json.JSONDecodeError):
            pass   # fall through to scanning the tree

    names = frozenset(
        p.name for p in sibling.rglob("*.md")
        if ".git" not in p.parts and _wanted(p.name, parent.prefixes)
    )
    if not names:
        return None
    return Resolution(parent, names, "sibling", f"scanned {sibling}")


def _from_cache(parent: ParentRepo, max_age_s: int = CACHE_TTL_S) -> Resolution | None:
    path = parent.cache_path
    if not path.is_file():
        return None
    age = time.time() - path.stat().st_mtime
    if age > max_age_s:
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    names = frozenset(data.get("artifacts", {}))
    if not names:
        return None
    return Resolution(parent, names, "cache", f"{age / 3600:.1f}h old")


def _from_api(parent: ParentRepo, timeout_s: int = 30) -> Resolution | None:
    """Fetch the parent's file list via the GitHub Git Trees API.

    One request returns the entire tree, so this needs no clone and no
    per-directory walk. Requires `gh` to be authenticated; returns None rather
    than raising when it is not, so an offline or unauthenticated run degrades
    instead of failing.
    """
    cmd = [
        "gh", "api",
        f"repos/{parent.repo}/git/trees/{parent.ref}?recursive=1",
        "--jq", ".tree[] | select(.type==\"blob\") | .path",
    ]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout_s
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0 or not proc.stdout.strip():
        return None

    names = frozenset(
        Path(line).name for line in proc.stdout.splitlines()
        if line.endswith(".md") and _wanted(Path(line).name, parent.prefixes)
    )
    if not names:
        return None

    # Cache it so pre-commit and subsequent runs stay fast and work offline.
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        parent.cache_path.write_text(
            json.dumps(
                {
                    "repo": parent.repo,
                    "ref": parent.ref,
                    "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "artifacts": {name: {} for name in sorted(names)},
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    except OSError:
        pass   # caching is an optimization, never a requirement

    return Resolution(parent, names, "api", f"{parent.repo}@{parent.ref}")


def _wanted(filename: str, prefixes: tuple[str, ...]) -> bool:
    if not filename.endswith(".md"):
        return False
    if not prefixes:
        return True
    return any(filename.startswith(prefix) for prefix in prefixes)


def resolve_parent(
    parent: ParentRepo,
    allow_fetch: bool = True,
    root: Path | None = None,
) -> Resolution:
    """Resolve one parent by sibling clone, then cache, then API."""
    for strategy in (
        lambda: _from_sibling(parent, root),
        lambda: _from_cache(parent),
        (lambda: _from_api(parent)) if allow_fetch else (lambda: None),
    ):
        result = strategy()
        if result is not None:
            return result
    return Resolution(
        parent, frozenset(), "unavailable",
        "no sibling clone, no fresh cache, and no successful fetch",
    )


# ---------------------------------------------------------------------------
# The check
# ---------------------------------------------------------------------------

def check_external_parents(
    references: dict[str, list[tuple[Path, str, str]]],
    parents: tuple[ParentRepo, ...],
    allow_fetch: bool = True,
    require_resolution: bool = False,
    root: Path | None = None,
) -> tuple[list[str], list[str]]:
    """Verify that every cross-repo parent reference resolves upward.

    `references` maps a tier to (artifact path, field name, referenced filename)
    triples. Returns (errors, notes) — notes carry resolution provenance so a
    green run says *how* it was verified rather than leaving it ambiguous.

    With `require_resolution` set (CI), an unresolvable parent is an error. Left
    unset (pre-commit), it is a note: a developer offline on a train must still
    be able to commit.
    """
    errors: list[str] = []
    notes: list[str] = []

    by_tier = {p.tier: p for p in parents}

    for tier, refs in sorted(references.items()):
        if not refs:
            continue
        parent = by_tier.get(tier)
        if parent is None:
            # No declared parent for this tier. Upward enforcement is impossible
            # and the trace is unverifiable, which is worth saying out loud.
            sample = refs[0]
            errors.append(
                f"{sample[0]}: '{sample[1]}' points outside this repo but no "
                f"parent is declared for tier '{tier}' — add one to "
                f"repo-standard.yaml 'parents:' so the reference can be checked"
            )
            continue

        resolution = resolve_parent(parent, allow_fetch=allow_fetch, root=root)
        if not resolution.available:
            message = (
                f"tier '{tier}': could not resolve parent {parent.repo} "
                f"({resolution.detail}) — {len(refs)} reference(s) checked for "
                f"shape only"
            )
            (errors if require_resolution else notes).append(message)
            continue

        notes.append(
            f"tier '{tier}': resolved {parent.repo} via {resolution.source} "
            f"({resolution.detail}); {len(resolution.filenames)} artifact(s)"
        )
        for artifact_path, field, referenced in refs:
            if referenced not in resolution.filenames:
                errors.append(
                    f"{artifact_path}: '{field}' references '{referenced}' but "
                    f"no such artifact exists in {parent.repo}@{parent.ref}"
                )

    return errors, notes


# ---------------------------------------------------------------------------
# Index emission — what makes this repo brokerable by its children
# ---------------------------------------------------------------------------

def build_index(
    bindings, files_by_label: dict[str, list[Path]], root: Path | None = None
) -> dict:
    """Build the artifact index a child repo resolves against.

    Filename plus tier, type and the requirements-tool key when present. The
    tool key is what makes the trace authoritative rather than advisory: Jama is
    the ratified identity authority, so a reference that carries a Jama key can
    be verified by anything, while a filename can only be verified by whoever
    has the repo.
    """
    root = root or REPO_ROOT
    artifacts: dict[str, dict] = {}
    for binding in bindings:
        for path in files_by_label.get(binding.label, []):
            entry = {"tier": binding.tier, "type": binding.name}
            try:
                entry["path"] = str(path.relative_to(root)).replace("\\", "/")
            except ValueError:
                entry["path"] = path.name
            artifacts[path.name] = entry
    return {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "commit": _git_sha(root),
        "artifacts": dict(sorted(artifacts.items())),
    }


def _git_sha(root: Path) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10,
        )
        return proc.stdout.strip() if proc.returncode == 0 else "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def emit_index(index: dict, root: Path | None = None) -> Path:
    path = (root or REPO_ROOT) / INDEX_FILENAME
    path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    """`emit-artifact-index` — write artifact-index.json for child repos."""
    import sys

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    try:
        from tools.schema import build_bindings, load_schema
        from tools.validate import _collect_files, read_repo_standard
    except ImportError:
        from schema import build_bindings, load_schema
        from validate import _collect_files, read_repo_standard

    decl, _ = read_repo_standard()
    schema = load_schema()
    repo_tiers = decl.get("tiers") if isinstance(decl.get("tiers"), list) else None
    packets = decl.get("packets") if isinstance(decl.get("packets"), dict) else None
    bindings = build_bindings(schema, repo_tiers=repo_tiers, packets=packets)
    files = _collect_files(bindings)

    index = build_index(bindings, files)
    path = emit_index(index)
    print(
        f"Wrote {path.name} — {len(index['artifacts'])} artifact(s) "
        f"at commit {index['commit'][:8]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
