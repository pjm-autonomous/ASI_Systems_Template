"""Artifact maturity states — the AxS M1..M4 scheme.

Adopted from `asirobots/axs`, which already runs this model on the same
programme and with the same reviewers (PRAK Architecture Review item A4). Using
the same vocabulary removes a translation layer between the two repo sets rather
than adding one, and it closes review item W4 ("no maturity gate on review").

**Where the state lives.** AxS records it as a bold key-value block in the
document body, immediately after the H1 heading — not in YAML frontmatter:

    # Geofence Map Validation
    **Status:** M2+
    **Version:** 1.0
    **Date:** 2026-09-10

This module parses that block strictly. A body header is easier to read and
edit than frontmatter but far easier to break, so the format is specified rather
than inferred: contiguous `**Key:** value` lines, starting on the first
non-blank line after the H1, ending at the first line that is not one.

Frontmatter is accepted as a fallback so a repo can migrate gradually, but the
header block is canonical — a cross-repo tool should only ever need to read one
format.

**What the states mean.** Gate criteria are owned by the governing engineering
lifecycle document, not by this module. What is enforced here:

- the value is a legal state
- from M2 upward, a promotion record exists in `_registry/`, so a state claim is
  backed by dated evidence rather than by someone editing a line
- M4 at one tier requires M4 at the tier above it, mirroring AxS's rule that
  M4 on level N requires M4 on level N-1
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REGISTRY_DIRNAME = "_registry"

# Ordered weakest to strongest. M2+ is M2 plus adversarial-tier review; it is a
# distinct state in AxS, not a decoration.
MATURITY_ORDER: tuple[str, ...] = ("M1", "M2", "M2+", "M3", "M4")
MATURITY_STATES = frozenset(MATURITY_ORDER)

# States that must be backed by a promotion record in _registry/.
EVIDENCE_REQUIRED_FROM = "M2"

# Which registry subdirectory holds the evidence for each state.
EVIDENCE_DIRS: dict[str, str] = {
    "M2": "m2_records",
    "M2+": "m2_records",
    "M3": "m3_reviews",
    "M4": "m3_reviews",
}

# An H1 heading: `# Some Title`.
H1 = re.compile(r"^#\s+\S")
# One line of the AxS header block: `**Key:** value`. Key is captured without
# the asterisks; the value runs to end of line.
HEADER_LINE = re.compile(r"^\*\*(?P<key>[^*:]+?):\*\*\s*(?P<value>.*?)\s*$")


class MaturityError(Exception):
    """The maturity declaration is malformed."""


@dataclass(frozen=True)
class MaturityState:
    """A parsed maturity declaration."""

    state: str | None          # None when the artifact declares none
    source: str                # "header" | "frontmatter" | "absent"
    header: dict[str, str]     # the whole parsed header block

    @property
    def rank(self) -> int:
        """Position in MATURITY_ORDER, or -1 when no state is declared."""
        if self.state is None:
            return -1
        return MATURITY_ORDER.index(self.state)

    def at_least(self, other: str) -> bool:
        """True when this state is `other` or stronger."""
        if self.state is None:
            return False
        return self.rank >= MATURITY_ORDER.index(other)


def parse_header_block(text: str) -> dict[str, str]:
    """Extract the AxS `**Key:** value` block that follows the H1.

    Returns an empty dict when there is no H1 or no block. Frontmatter, if
    present, is skipped first so the H1 is found in the body.
    """
    lines = text.splitlines()
    idx = 0

    # Skip YAML frontmatter if the file opens with it.
    if lines and lines[0].strip().lstrip("﻿") == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                idx = i + 1
                break

    # Find the H1.
    while idx < len(lines) and not H1.match(lines[idx]):
        # Only blank lines may precede the H1; anything else means no header
        # block is being declared and we should not go hunting for one.
        if lines[idx].strip():
            return {}
        idx += 1
    if idx >= len(lines):
        return {}
    idx += 1

    # Skip blank lines between the H1 and the block.
    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    # Consume contiguous header lines.
    header: dict[str, str] = {}
    while idx < len(lines):
        match = HEADER_LINE.match(lines[idx])
        if not match:
            break
        header[match.group("key").strip()] = match.group("value").strip()
        idx += 1
    return header


def read_maturity(text: str, frontmatter: dict | None = None) -> MaturityState:
    """Resolve an artifact's maturity state.

    The body header block is canonical; a `maturity` or `status` frontmatter key
    is accepted as a migration fallback. Note `status` is also used by ADRs and
    interfaces for their own lifecycles, so it is only read as maturity when the
    value is actually a maturity state.
    """
    header = parse_header_block(text)

    raw = header.get("Status") or header.get("Maturity")
    if raw:
        return MaturityState(state=raw.strip(), source="header", header=header)

    if frontmatter:
        for key in ("maturity", "status"):
            value = frontmatter.get(key)
            if isinstance(value, str) and value.strip() in MATURITY_STATES:
                return MaturityState(
                    state=value.strip(), source="frontmatter", header=header
                )

    return MaturityState(state=None, source="absent", header=header)


def registry_root(root: Path | None = None) -> Path:
    return (root or REPO_ROOT) / REGISTRY_DIRNAME


def find_evidence(slug: str, state: str, root: Path | None = None) -> Path | None:
    """Locate the promotion record backing a maturity claim.

    Matched on the artifact slug appearing in the record's filename, which is
    how AxS names them (`{Level}-{Artifact}_M2_Record.md`).
    """
    subdir = EVIDENCE_DIRS.get(state)
    if subdir is None:
        return None
    directory = registry_root(root) / subdir
    if not directory.is_dir():
        return None
    for candidate in sorted(directory.rglob("*.md")):
        if slug.lower() in candidate.stem.lower():
            return candidate
    return None


def check_artifact(
    rel: Path,
    slug: str,
    text: str,
    frontmatter: dict | None = None,
    root: Path | None = None,
    require_declaration: bool = True,
) -> list[str]:
    """Validate one artifact's maturity declaration.

    Only called when the `maturity-gates` packet is enabled, so a repo not
    running maturity gates is never failed for lacking them.
    """
    errors: list[str] = []
    maturity = read_maturity(text, frontmatter)

    if maturity.state is None:
        if require_declaration:
            errors.append(
                f"{rel}: no maturity state declared — add a '**Status:** M1' line "
                f"directly after the H1 heading (see tools/maturity.py)"
            )
        return errors

    if maturity.state not in MATURITY_STATES:
        errors.append(
            f"{rel}: maturity '{maturity.state}' is not a legal state; "
            f"must be one of {list(MATURITY_ORDER)}"
        )
        return errors

    # A claim of M2 or better needs dated evidence behind it, or the state is
    # just a line somebody edited.
    if maturity.at_least(EVIDENCE_REQUIRED_FROM):
        if find_evidence(slug, maturity.state, root) is None:
            subdir = EVIDENCE_DIRS.get(maturity.state, "m2_records")
            errors.append(
                f"{rel}: claims maturity {maturity.state} but no promotion "
                f"record naming '{slug}' exists in {REGISTRY_DIRNAME}/{subdir}/ "
                f"— a state at or above {EVIDENCE_REQUIRED_FROM} requires "
                f"recorded evidence"
            )

    return errors


def check_tier_gating(
    states_by_tier: dict[str, list[tuple[Path, MaturityState]]],
    tier_order: list[str],
) -> list[str]:
    """M4 at a tier requires M4 at the tier above it.

    Mirrors AxS's rule that M4 on level N requires M4 on level N-1: a component
    cannot be more mature than the system requiring it. `tier_order` is
    outermost-inward, so the tier above is the preceding entry.
    """
    errors: list[str] = []
    for position, tier in enumerate(tier_order):
        if position == 0:
            continue   # outermost tier has nothing above it
        parent_tier = tier_order[position - 1]
        parent_entries = states_by_tier.get(parent_tier) or []
        if not parent_entries:
            continue   # tier not present in this repo; nothing to gate against
        parent_all_m4 = all(
            state.state == "M4" for _, state in parent_entries
        )
        if parent_all_m4:
            continue
        for rel, state in states_by_tier.get(tier) or []:
            if state.state == "M4":
                laggards = sum(
                    1 for _, s in parent_entries if s.state != "M4"
                )
                errors.append(
                    f"{rel}: claims M4 but the {parent_tier} tier above it is "
                    f"not fully M4 ({laggards} artifact(s) below M4) — M4 at "
                    f"one tier requires M4 at the tier above"
                )
    return errors
