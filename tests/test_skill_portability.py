"""A harvested skill must not carry its source repo's identity.

The template's promise is that an instantiated repo gets tooling that **runs as
delivered**. A skill ported from another programme breaks that promise quietly:
it still runs, and it teaches that programme's vocabulary as if it were the
standard.

The count that justifies a test rather than a review note, taken 2026-09-14 from
the 19 skills in the harvest pool:

    AxS                131        Safety Controller   93
    MR-SC               43        PLd                 40
    STPA                33        MR-L0               26
    ASAM                26        _sanctuary          12
    IEC 61508            1
    ------------------------------------------------ 405

405 tokens to remove by hand across 19 files. Missing one is not a question of
diligence, it is a question of arithmetic — and a missed token is invisible,
because the skill still works.

Scoped to `.claude/`, which is what ships and executes. `tools/` docstrings cite
their provenance deliberately (`maturity.py` explains that the M1..M4 scheme came
from AxS, which a reader needs); `standard/` records the harvest itself. Neither
is shipped as an instruction to an author.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_DIR = REPO_ROOT / ".claude"

# Identity from the repos this template harvests from. Case-sensitive where the
# token is a proper noun, so "a safety controller" in prose is not a hit while
# "the Safety Controller" — a named subsystem of another programme — is.
FORBIDDEN = {
    r"\bAxS\b": "the source repo's programme name",
    r"\bMR-SC-": "an AxS requirement ID prefix",
    r"\bMR-L0-": "an AxS requirement ID prefix",
    r"\b_sanctuary\b": "an AxS-only process directory",
    r"\bSafety Controller\b": "a named subsystem of another programme",
    r"\bASAM\b": "a programme-specific entity",
    r"\bAgent [AC]\d+\b": "the AxS agent numbering",
    r"\bprak-v-model\b": "a specific repo, not the template",
    r"\bpolymorphous-v-model\b": "a specific repo, not the template",
    r"\bprak-embedded-core\b": "a specific repo, not the template",
}

# Safety-integrity values. The template declares no safety-integrity field at
# all (an open TODO item), so a skill naming a level is asserting one the
# standard does not have - the PLd-vs-PLe failure that motivated the
# never-hardcode-a-default rule.
FORBIDDEN_INTEGRITY = r"\bPL[a-e]\b|\bSIL ?[1-4]\b"


def _shipped_docs() -> list[Path]:
    if not CLAUDE_DIR.is_dir():
        return []
    return sorted(CLAUDE_DIR.rglob("*.md"))


def _ids(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


@pytest.mark.parametrize("path", _shipped_docs(), ids=_ids)
def test_no_source_repo_identity(path: Path):
    text = path.read_text(encoding="utf-8")
    hits: list[str] = []
    for pattern, why in FORBIDDEN.items():
        found = re.findall(pattern, text)
        if found:
            hits.append(f"{sorted(set(found))} ({why})")
    assert not hits, (
        f"{_ids(path)}: carries source-repo identity: {'; '.join(hits)}. "
        f"A harvested skill must run as delivered in a repo that has never "
        f"heard of the programme it came from."
    )


@pytest.mark.parametrize("path", _shipped_docs(), ids=_ids)
def test_no_safety_integrity_level(path: Path):
    """No skill may assert a PL or SIL the standard does not declare."""
    found = sorted(set(re.findall(FORBIDDEN_INTEGRITY, path.read_text(encoding="utf-8"))))
    assert not found, (
        f"{_ids(path)}: names safety-integrity level(s) {found}. This template "
        f"declares no safety-integrity field, so a skill naming one asserts a "
        f"target no governing document here sets — the failure that produced "
        f"the never-hardcode-a-PL-default rule."
    )


def test_the_guard_covers_the_harvest_target():
    """A guard that scans nothing passes forever."""
    assert _shipped_docs(), ".claude/ has no Markdown - the guard scans nothing"
