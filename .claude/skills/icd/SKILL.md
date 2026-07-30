---
name: icd
description: Create or update an interface control document in system/interfaces/<feature>/. Use when the user wants to define a contract between components, subsystems, or external systems.
---

# Skill: icd

Create or update an interface control document (ICD) artifact in `system/interfaces/<feature>/`.

An ICD is the contract for one interface: who owns it, who consumes it, and the schema/protocol/semantics both sides can rely on.

## Create flow

Ask the user for:

- ICD title (short description for the filename, usually named after the interface, e.g. `dock-reservation-api`)
- Parent product requirement filename (e.g. `req-autonomous-return-to-dock.md`) — **required**; must exist under `product/requirements/` (if not, direct the user to `/product-requirement` first)
- Owning component — the component/subsystem that owns the interface contract
- Consumer(s) — one or more components, subsystems, or external systems that consume the interface
- A brief description of the interface's purpose and (if known) its transport/protocol

Locate the parent product requirement under `product/requirements/`. The feature bucket is the directory the parent lives in — reuse it for the new ICD. If the parent cannot be located, ask the user for the correct filename rather than guessing.

Then:

1. Create `system/interfaces/<feature>/icd-<short-description>.md` from `templates/icd.md`. Create the feature directory if it doesn't exist.
2. Populate YAML frontmatter:
   - `id`: filename without the `.md` extension
   - `title`: human-readable title
   - `parent-product-requirement`: parent filename including `.md`, no directory path
   - `owning-component`: as provided
   - `consumers`: YAML list (singleton list is fine)
3. Fill the plain Markdown table rows: **Owning Component**, **Consumers** (comma-separated), **Parent Product Requirement**
4. Fill the sections — `TBD` for anything unknown rather than deleting the heading:
   - **Purpose** — why this interface exists
   - **Contract → Data Schema** — message/payload definitions (plain Markdown tables or fenced code blocks)
   - **Contract → Protocol / Transport** — e.g. REST/HTTP, gRPC, MQTT, CAN, shared memory
   - **Contract → Behavioral Semantics** — request/response flows, streaming/eventing semantics, timing expectations, idempotency/retry rules
   - **Contract → Error Handling & Status Model** — error codes, degraded modes, timeouts
   - **Contract → Security Properties** — authn/authz, encryption, key handling, where applicable
   - **Contract → Versioning & Compatibility Policy** — how breaking vs. non-breaking changes are handled
5. Update `traceability/TRACEABILITY.md`: fill the ICD cell on the row containing the parent product requirement. Link relative to `traceability/`: `[icd-<name>.md](../system/interfaces/<feature>/icd-<name>.md)`. If the requirement has multiple ICDs, duplicate the row.

Finish by running `python tools/validate.py` from the repo root and fixing anything it reports.

## Update flow

If the ICD already exists:

1. Locate it under `system/interfaces/` and read it
2. Ask the user what needs to change
3. Apply only the requested changes — do not regenerate the whole file
4. Re-run `python tools/validate.py`

## Conventions

- Filename: `icd-<short-description>.md` in kebab-case
- Tables are plain Markdown, never HTML `<table>` markup
- Examples: `icd-geofence-alert-api.md`, `icd-dock-reservation-api.md`
