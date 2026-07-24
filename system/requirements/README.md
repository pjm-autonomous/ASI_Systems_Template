# System Requirements

Grouped by feature bucket: `system/requirements/<feature>/sysreq-<description>.md`. Start from `templates/system-requirement.md`. See `example/system/requirements/low-battery-return-to-dock/` for two worked samples.

## What Belongs Here

A system requirement is the engineering decomposition of a product requirement, allocated to a specific component or subsystem (the `allocation` frontmatter field — e.g. `power-management-service`, `fleet-coordination-service`). It traces up to exactly one `parent-product-requirement` and, optionally, directly to `parent-use-cases` when it's useful to show that trace without going through the product requirement.

Where a product requirement says *what* the system does for a stakeholder, a system requirement says *which component* does it and under *what measurable condition* — timing budgets, thresholds, allocation. Multiple system requirements commonly decompose a single product requirement (see the example: `sysreq-battery-threshold-monitor` and `sysreq-dock-availability-check` both decompose `req-autonomous-return-to-dock`).

## Allocation

The `allocation` field should name a real component or subsystem in the project's actual architecture (matching the `owning-component` used in `system/interfaces/` ICDs and the execution units named in `system/deployment/`). Keep allocation names consistent across all three — `tools/validate.py` doesn't currently cross-check this, so consistency is a discipline, not an enforced rule.

## Cross-Industry Process Standards

This layer is where ASPICE PAM 4.0 (SWE.1–SWE.6, SYS.2–SYS.3) and ISO/IEC/IEEE 15288's requirements/design process areas map most directly — see `reference/standards-framework.md` if a project needs to show that mapping explicitly for a customer or audit.
