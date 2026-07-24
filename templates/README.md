# Templates

Canonical blank starting point for each core artifact type. Copy the relevant file into the correct feature bucket under `product/` or `system/` and rename it per the convention in `CLAUDE.md` — don't edit these files in place when authoring a real artifact.

| Template | Copy Into | Filename Pattern |
| --- | --- | --- |
| `persona.md` | `product/personas/` | `<role-or-team>.md` |
| `use-case.md` | `product/use-cases/<feature>/` | `uc-<description>.md` |
| `product-requirement.md` | `product/requirements/<feature>/` | `req-<description>.md` |
| `system-requirement.md` | `system/requirements/<feature>/` | `sysreq-<description>.md` |
| `architecture-diagram.md` | `system/architecture/<feature>/` | `arch-<description>.md` |
| `icd.md` | `system/interfaces/<feature>/` | `icd-<description>.md` |
| `data-specification.md` | `system/data/<feature>/` | `data-<description>.md` |
| `deployment-architecture.md` | `system/deployment/<feature>/` | `deploy-<description>.md` |
| `adr.md` | `system/decisions/` | `adr-NNNN-<description>.md` |

Each template's HTML-comment placeholders (`<!-- ... -->`) explain what goes in that section or field — delete the comment once you've filled the section in, don't leave both the comment and the real content.

If you're not sure what a filled-in version should look like, look at the matching file under `example/` before starting from a blank template — the example thread's frontmatter and section content is a closer reference than the template's placeholder comments alone.

## Editing These Templates Themselves

If you find a template is missing a field every real instance of that artifact ends up needing, that's worth fixing in the template — but do it as a deliberate change (with a note in the PR description), not as a side effect of authoring one specific artifact. Keep `tools/validate.py`'s required-fields list and each template's frontmatter in sync if you add or remove a required field.
