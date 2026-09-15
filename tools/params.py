"""Parameter citation and resolution — does every cited bound have a value?

**The failure this exists to prevent.** A requirement that names a bound but
does not resolve it to a value is unverifiable by construction: no test can
state a pass criterion for "the configured threshold". The count, taken from
`prak-v-model` on 2026-09-13: **223** requirement files, **136** `TBD`/`TBR`
occurrences across **37** files, and **0** `param-*` artifacts — every named
bound in that repo has nowhere to hold a value. Nine requirement files cite one
directly.

The `param` artifact type (D-26) gave those bounds a home. It did not make
anything check that a citation reaches one, which is what this module does.

**What is deliberately NOT checked.** A bare number in a requirement statement
is not flagged. Detecting "this digit should have been a parameter" needs a
heuristic, and a heuristic on requirement prose produces false positives at a
rate that gets the whole check ignored — which is the failure mode the
governing principle exists to avoid. A tool that cries wolf is worse than no
tool, because it also teaches people to skip the ones that do not.

So this checks only what is unambiguous: a citation that does not resolve, a
resolved parameter with no usable value, and a back-reference list that
disagrees with reality.

**Why `Cited By` is checked rather than generated.** D-46 made
`TRACEABILITY.md` generated because nothing read the hand-maintained version,
so nothing caught it drifting. That reasoning does not transfer here: once this
module reads `Cited By`, drift is caught on the next run. A checked
hand-maintained list is honest; an unchecked one is decoration.

The check found its first defect in this template's own `example/`:
`param-battery-reserve-threshold.md` listed `sysreq-battery-threshold-monitor.md`
under `Cited By`, and that requirement — which says "the configured low-battery
threshold" — cited no parameter at all. The link existed in one direction only,
in the worked example every instantiated repo copies.
"""
from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

# A citation is the parameter's filename, wherever it appears in the body:
# backticked, in a Markdown link, or in prose. Matching the filename rather
# than a link form keeps the check indifferent to how an author writes it.
CITATION = re.compile(r"\bparam-[a-z0-9]+(?:-[a-z0-9]+)*\.md\b")

# Any artifact filename, for reading a `## Cited By` list.
ARTIFACT_REF = re.compile(r"\b[a-z0-9]+(?:-[a-z0-9]+)*\.md\b")

# The `## Cited By` section, ending at the next heading of any level or EOF.
CITED_BY_SECTION = re.compile(
    r"^#{1,6}\s+Cited\s+By\s*$(?P<body>.*?)(?=^#{1,6}\s|\Z)",
    re.MULTILINE | re.DOTALL | re.IGNORECASE,
)

# Values that satisfy the required-fields check but state nothing. `value: ""`
# and a missing key are already caught by the validator's required-field pass,
# so what is left is a placeholder someone typed to make the field non-empty.
PLACEHOLDER_VALUES = frozenset(
    {"tbd", "tbr", "tba", "todo", "?", "??", "???", "n/a", "na",
     "xxx", "none", "unknown", "pending", "placeholder"}
)


@dataclass(frozen=True)
class ParamDecl:
    """One declared parameter, as much of it as this check needs."""

    rel: Path                    # repo-relative path, for messages
    filename: str                # `param-foo.md`
    value: object                # frontmatter `value`, any YAML scalar
    cited_by: frozenset[str]     # filenames listed under `## Cited By`


def is_placeholder(value: object) -> bool:
    """True when a value is present but states nothing.

    `0` and `False` are real values. Treating a falsy number as missing is the
    obvious bug here, and a reserve threshold of 0 is a legitimate — if
    alarming — engineering statement that this module has no business
    second-guessing.
    """
    if value is None:
        return True
    if isinstance(value, bool) or isinstance(value, (int, float)):
        return False
    text = str(value).strip()
    if not text:
        return True
    return text.casefold() in PLACEHOLDER_VALUES


def parse_cited_by(text: str) -> frozenset[str]:
    """Read the filenames listed under a parameter's `## Cited By` heading.

    Returns an empty set when the section is absent or empty — indistinguishable
    on purpose, because both mean "this parameter claims no citations" and the
    citation scan is what decides whether that is true.
    """
    match = CITED_BY_SECTION.search(text)
    if not match:
        return frozenset()
    return frozenset(ARTIFACT_REF.findall(match.group("body")))


def collect_citations(
    documents: Iterable[tuple[str, str]],
) -> dict[str, frozenset[str]]:
    """Map each cited `param-*.md` to the filenames of the artifacts citing it.

    `documents` is (filename, text) pairs over every artifact in the repo. A
    parameter file naming itself does not count as a citation of itself — its
    own frontmatter and body table repeat its id — so self-references are
    dropped rather than producing a parameter that appears to cite itself.
    """
    found: dict[str, set[str]] = {}
    for filename, text in documents:
        for target in set(CITATION.findall(text)):
            if target == filename:
                continue
            found.setdefault(target, set()).add(filename)
    return {target: frozenset(names) for target, names in found.items()}


def check_parameters(
    declared: Sequence[ParamDecl],
    citations: Mapping[str, frozenset[str]],
) -> tuple[list[str], list[str]]:
    """Check citation resolution, parameter values and back-references.

    Returns `(errors, notes)`. Errors fail the validator. Notes are reported
    but do not fail: an uncited parameter is untidy, not wrong, and failing a
    build over one would punish declaring a value before writing the
    requirement that needs it — which is the order this standard wants.
    """
    errors: list[str] = []
    notes: list[str] = []

    by_filename = {decl.filename: decl for decl in declared}

    # --- Citations that do not resolve -------------------------------------
    for target in sorted(citations):
        if target in by_filename:
            continue
        for citer in sorted(citations[target]):
            errors.append(
                f"{citer}: cites '{target}', which is not a declared parameter "
                f"— the bound has no value anywhere, so nothing verifies this"
            )

    for decl in sorted(declared, key=lambda d: d.filename):
        actual = citations.get(decl.filename, frozenset())

        # --- A cited parameter that states nothing -------------------------
        if is_placeholder(decl.value):
            if actual:
                errors.append(
                    f"{decl.rel}: 'value' is a placeholder "
                    f"({decl.value!r}) and {len(actual)} artifact(s) cite it "
                    f"({', '.join(sorted(actual))}) — a citation that resolves "
                    f"to a placeholder is no better than one that dangles"
                )
            else:
                notes.append(
                    f"{decl.rel}: 'value' is a placeholder ({decl.value!r}); "
                    f"nothing cites it yet, so this is not failing the build"
                )

        # --- Back-reference drift, both directions -------------------------
        missing = sorted(actual - decl.cited_by)
        stale = sorted(decl.cited_by - actual)
        if missing:
            errors.append(
                f"{decl.rel}: cited by {missing} but its 'Cited By' section "
                f"does not list them"
            )
        if stale:
            errors.append(
                f"{decl.rel}: 'Cited By' lists {stale}, which do not cite this "
                f"parameter — the link exists in one direction only"
            )

        # --- Declared and unused -------------------------------------------
        if not actual and not decl.cited_by:
            notes.append(
                f"{decl.rel}: no artifact cites this parameter"
            )

    return errors, notes
