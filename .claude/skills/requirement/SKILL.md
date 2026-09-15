---
name: requirement
description: EARS requirement formatter and quality auditor — converts plain-language descriptions into EARS statements, and reviews existing requirements for atomicity, testability, ambiguity and substance. Utility only; creates no files.
---

# Skill: requirement

Two modes over one set of rules:

| Mode | Use when | Produces |
|---|---|---|
| **Format** | Turning a plain-language description into a requirement statement | One EARS statement per behaviour |
| **Audit** | Reviewing requirements that already exist | A findings table, one row per requirement |

They share the quality criteria below deliberately. A rule used to write a
requirement and a rule used to reject one must be the same rule, or authors and
reviewers work to different standards.

**Creates no files.** To author a requirement artifact use
`/product-requirement`, `/capability-requirement`, `/system-requirement`,
`/subsystem-requirement` or `/component-requirement` — each applies these rules.

## Format mode

1. Ask for a plain-language description of what the system must do, or use the
   one already given.
2. Pick the EARS keyword from the reference table below.
3. Output the formatted statement.
4. If the trigger type is ambiguous, ask which keyword fits before formatting.
5. If the description bundles several behaviours, propose one statement per
   behaviour — see **Atomicity**.
6. Iterate until the user is satisfied.

Present the statement as a plain quoted block. No file is created.

## Audit mode

Apply all five criteria to every requirement. A requirement passes only if it
passes all five.

### 1. EARS syntax

Every requirement follows one of the five patterns in the reference table.
Natural-language requirements are ambiguous; the patterns force structure.

### 2. Grooming — apply in order

The order matters: delete before optimising.

| # | Rule | What to check |
|---|---|---|
| 1 | **Make it less dumb** | Every requirement has a named owner — a person, not a department. If you cannot say in one sentence why it exists, flag it. "Because the standard says so" is a citation, not a purpose; the purpose is the harm it prevents. |
| 2 | **Delete it** | Would the system still be safe and correct without this requirement — because another covers the ground, or because the condition cannot arise? Recommend deletion. This is the hardest rule to apply honestly, and the one most often skipped. |
| 3 | **Simplify** | After pruning, remove jargon, passive voice, compound clauses. One sentence, one requirement. If it needs a paragraph of rationale to be understood, it is too complex. |
| 4 | **Consolidate** | Two requirements saying the same thing in different words become one. Question a constraint tighter than it needs to be — "within 10 ms" where 100 ms is safe is a cost with no buyer. |
| 5 | **Automate last** | A requirement describing a manual step — "the operator shall verify" — may exist only because that is how it has always been done. Flag it; do not assume it is wrong. |

### 3. Atomicity

One requirement expresses exactly one verifiable condition. Split on:

- **"and"** — "shall detect obstacles **and** stop" is two requirements.
- **"and/or"** — always split; it is ambiguous by definition.
- **Compound subjects** — one requirement per responsible entity.
- **Multiple conditions** — "when speed exceeds X **or** range is under Y" is two
  event-driven requirements.

*Exception:* a compound predicate may stay whole when both halves are
inseparable aspects of one atomic function and splitting would invent a
dependency. **Record why you did not split**, or the exception becomes the rule.

### 4. Testability

Every requirement is verifiable by test, analysis, inspection or demonstration —
the four methods this standard allows (D-23). Flag:

- **Unmeasurable terms** — adequate, sufficient, appropriate, reasonable,
  robust, reliable, user-friendly.
- **Missing tolerance** — a limit with no tolerance and no stated conditions.
- **Missing time bound** — "shall respond quickly".
- **Undefined scope** — "shall handle all failure modes"; which ones.
- **Unverifiable negatives** — "shall not cause harm" cannot be tested;
  decompose into specific outcomes that can be shown absent.

Provide a testable rewrite for each, and name the measurement point where it is
not obvious. A bound that needs a value belongs in a `param-*` artifact cited by
name (D-26) — never a number copied into prose.

### 5. Ambiguity

Flag:

- **Vague quantifiers** — several, many, few, some, most.
- **Undefined acronyms** on first use.
- **Numbers without units or bounds.**
- **Undefined time references** — immediately, promptly, in a timely manner.
- **Implicit assumptions** — "the operator shall be notified" says nothing about
  how, or from how far away.
- **Pronouns with no clear antecedent** — "it shall…".

## Audit output

**The table below is output.** One row per requirement reviewed:

| File | Line | Requirement | EARS | Atomic | Testable | Unambiguous | Verdict | Rewrite |
|---|---|---|---|---|---|---|---|---|

**File** is always present. **Line** is the line of the statement at fault, or
`—` when the finding is about the artifact as a whole. Never guess a number.

| Verdict | Means |
|---|---|
| `APPROVED` | Passes all five criteria as written. |
| `REWRITE` | Fixable in place; the rewrite column carries the replacement. |
| `SPLIT` | Not atomic; give one statement per behaviour. |
| `DELETE` | Rule 2 applies — say what already covers it, or why the condition cannot arise. |
| `ESCALATE` | Cannot be judged here: the content is a design decision (ADR), a bound with no parameter (`param-*`), or a value whose authority is a governing document. Name which. |

Close with counts per verdict and the single most consequential finding.

### When reviewing generated requirements

If the set shows signs of being machine-written, add a short assessment:

- **Template uniformity** — every requirement sharing one sentence shape. Real
  sets vary, because different functions have different characteristics.
- **Standard parroting** — restating a clause without adding system-specific
  detail. Naming a target is a citation; a requirement says *how* this system
  meets it.
- **Missing domain specifics** — generic enough to apply to any system at all.
  Generic is suspicious.
- **No deletions** — reviewing 30 or more requirements and recommending no
  deletion usually means Rule 2 was not applied honestly.

## EARS reference

| Keyword | Pattern | Use when |
|---|---|---|
| When | `When <trigger>, the system shall <response>.` | A discrete event occurs |
| While | `While <state>, the system shall <behavior>.` | A continuous state holds |
| If | `If <condition>, the system shall <action>.` | A condition may or may not be true |
| Where | `Where <feature is included>, the system shall <capability>.` | A feature is optionally present |
| (none) | `The system shall <capability>.` | The behavior is unconditional |

Replace "the system" with the entity actually responsible. Passive voice that
hides which part of the system acts is a defect, not a style choice.
