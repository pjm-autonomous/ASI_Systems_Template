# Templates

Canonical blank starting point for each artifact type. Copy the relevant
file into the tier it belongs to and rename it per the convention below —
do not edit these files in place when authoring a real artifact.

**A tier directory only exists if `repo-standard.yaml` declares that tier.**
If the destination below is not a tier this repo masters, the artifact
belongs in a different repo — see `standard/tier-schema.md`.

| Template | Valid tiers | Copy into | Filename pattern |
| --- | --- | --- | --- |
| `adr.md` | `stakeholder`, `product`, `capability`, `system`, `subsystem`, `component` | `<tier>/decisions/` | `adr-<description>.md` |
| `architecture-diagram.md` | `architecture` | `<tier>/` | `arch-<description>.md` |
| `capability-requirement.md` | `capability` | `<tier>/requirements/` | `capreq-<description>.md` |
| `component-requirement.md` | `component` | `<tier>/requirements/` | `compreq-<description>.md` |
| `data-specification.md` | `system`, `subsystem` | `<tier>/data/` | `data-<description>.md` |
| `deployment-architecture.md` | `system` | `<tier>/deployment/` | `deploy-<description>.md` |
| `interface.md` | `interfaces` | `<tier>/` | `int-<description>.md` |
| `parameter.md` | `product`, `capability`, `system`, `subsystem`, `component` | `<tier>/parameters/` | `param-<description>.md` |
| `persona.md` | `stakeholder` | `<tier>/personas/` | `<name>.md` |
| `product-requirement.md` | `product` | `<tier>/requirements/` | `prodreq-<description>.md` |
| `subsystem-requirement.md` | `subsystem` | `<tier>/requirements/` | `subreq-<description>.md` |
| `system-requirement.md` | `system` | `<tier>/requirements/` | `sysreq-<description>.md` |
| `use-case.md` | `stakeholder` | `<tier>/use-cases/` | `uc-<description>.md` |

A feature-bucket directory may sit between the destination and the file
(`system/requirements/geofencing/sysreq-foo.md`). Buckets are optional and
kebab-case.

## Required fields

**Not listed here.** They are defined in `standard/artifact-schema.yaml`,
and each template's frontmatter is checked against it by
`tests/test_templates.py`. A prose copy of a field list is a second source
of truth that drifts — an audit on 2026-09-13 found five templates teaching
fields the schema had already stopped accepting.

## If you are not sure what a filled-in version looks like

Look at the matching file under `example/` before starting from a blank
template. A worked artifact's frontmatter and section content is a closer
reference than placeholder comments alone.

## Editing these templates

If a template is missing a field every real instance needs, fix the
template — but as a deliberate change with a note in the PR, not as a side
effect of authoring one artifact.

Add or remove a **required** field in `standard/artifact-schema.yaml`, never
in a template alone. The schema is the model; templates follow it, and the
test suite fails if they disagree in either direction.
