---
id: param-
title:
value:
unit:
---

<!-- A program-declared value, cited by name from requirements rather than
     written into their prose.

     This type exists because 17 distinct configured bounds were found named in
     requirements with no value declared anywhere and no artifact type to hold
     them. Until a bound has a home and a value, every requirement that cites it
     is unverifiable by construction, and no test can state a pass criterion. -->

| Field | Value |
|---|---|
| ID | |
| Value | |
| Unit | |
| Declared by | |
| Applies to | |

## Definition

<!-- What this parameter bounds, precisely enough that two engineers would
     measure it the same way. Name the measurement point. -->

## Basis

<!-- Where the value comes from: an analysis, a standard, a supplier datasheet,
     a test result, or an engineering judgement recorded as such. A value with
     no basis is a placeholder - say so explicitly rather than letting it read
     as settled. -->

## Cited By

<!-- Requirements that reference this parameter by name, one filename per line.

     Checked, not decorative: tools/params.py compares this list against the
     citations it finds across the repo and fails on drift in either direction
     (D-58). A requirement citing this parameter but missing here is an error,
     and so is an entry here that cites nothing. -->
