# Reference

Background material this template's conventions are built on. Read these before assuming a convention is arbitrary — most of them exist because they satisfy a specific standard's requirements.

| File | Covers |
| --- | --- |
| `bkm-document-set.md` | The full ~31-document inventory a *mature* SE documentation package contains, grouped by category. Use it to know what an `extensions/` stub should grow into, and to decide, project by project, which categories actually apply. |
| `standards-framework.md` | Cross-industry standards (systems engineering, functional safety, cybersecurity, coding, robot/vehicle safety) relevant to autonomous-systems work, with scoring rubrics where the standard provides one. Seeds `traceability/STANDARDS-MAPPING.md`. |
| `tooling-recommendations.md` | Claude Code skills, MCP connectors, and built-in document-export skills worth using alongside this template — and what was checked but not recommended. |

## How These Three Relate

`standards-framework.md` tells you *which external standards* might apply and how mature your coverage of each one is. `bkm-document-set.md` tells you *which internal documents* to write as a result. `tooling-recommendations.md` tells you *what tools* help you write and maintain both. Read them in that order when planning what an `extensions/` category should contain for your specific project — don't treat any of the three as exhaustive on its own.

## Keeping This Current

Standards get revised (see the 2025 ISO 10218 revision noted in `standards-framework.md` as an example of exactly this happening). Re-verify a standard's current edition before citing a specific year/version in a real requirement — don't assume the version recorded here is still current by the time you're reading it.
