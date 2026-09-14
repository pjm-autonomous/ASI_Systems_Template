# Checklist — Standing Up a New Systems Engineering Repo

**No tooling required.** This checklist is the standard; `tools/` only automates
parts of it. A repo built by working through this by hand is conformant. If a step
here can only be done with a tool, that is a defect in the checklist — raise it.

Print it, work down it, tick as you go. Anything you cannot answer is a gap to
record, not a step to skip.

---

## A. Before creating anything

- [ ] **A1.** Read `standard/tier-schema.md`. You cannot place a single artifact
      correctly without it.
- [ ] **A2.** Identify **this repo's level** — L0, L1, or L2. One repo is one
      level. If you cannot say which, stop: the answer decides everything below.
- [ ] **A3.** Identify the **owner role** for that level (Compliance & Safety at
      L0, Systems Architect at L1, Systems Engineer / owning team at L2).
- [ ] **A4.** Identify the **parent repo** — the level above. An L2 repo's parent
      is the L1 repo; an L1 repo's parent is L0. L0 has no parent.
- [ ] **A5.** Confirm the parent repo actually exists and you can read it. If it
      does not, record that as a gap now — every parent reference you author will
      be unverifiable until it does.

## B. Provenance and conformance

- [ ] **B1.** Copy the template (GitHub **Use this template**).
- [ ] **B2.** Delete `VERSION` and `standard/` from the new repo — they belong to
      the template, not to a project built from it.
- [ ] **B3.** Fill in `repo-standard.yaml` `standard:` — `version` from the
      template's `VERSION`, `commit` from the template's git SHA (or the release
      tag), `instantiated` as today's date. **Do not invent these.** Without them
      nobody can tell what this repo was cut from or whether it has drifted.
- [ ] **B4.** Set `level:` to the answer from A2.
- [ ] **B5.** Set `tiers:` to the tiers that level declares — `tier-schema.md` §4
      lists which tiers belong to which level. Declaring a tier the schema does
      not define means nothing gets validated, so check the spelling.
- [ ] **B6.** Set `parents:` to the repo from A4, with the tier whose parents live
      upstream. An L0 repo leaves this empty.
- [ ] **B7.** Set `conventions.table-format` and `conventions.diagram-format`.
- [ ] **B8.** Set `requirements-tool` — project key and ID, if known. Leave the
      placeholders only if genuinely undecided, and record that as a gap.
- [ ] **B9.** Decide `packets:` — turn off what this project will not use.
      Omitting a packet is a legitimate choice, not a gap. Note that the level's
      requirement type, `interfaces` and `architecture` carry **no flag**: every
      level owns boundaries and the architecture they stand on, so they are core.
      `maturity-gates` is required — maturity gates review itself.

## C. Naming and placement

- [ ] **C1.** Confirm every directory is named after a **tier**, never a level.
      A directory called `L2/` makes renumbering a migration.
- [ ] **C2.** Confirm artifact filename prefixes match the standard:
      `uc-` `prodreq-` `capreq-` `sysreq-` `subreq-` `compreq-` `int-` `arch-`
      `data-` `deploy-` `param-` `adr-NNNN-`. Personas carry no prefix. These
      align with `prak-v-model` and with Jama terminology; do not invent local
      variants.
- [ ] **C3.** Confirm feature-bucket directory names match the parent repo's
      buckets where the same feature appears in both. The mapping between a repo
      path and its requirements-tool location is string equality — a renamed
      bucket on one side silently stops matching.

## D. Interfaces

- [ ] **D1.** List the boundaries **this level owns** — the interfaces between the
      entities of the level below (`tier-schema.md` §3).
- [ ] **D2.** For each, confirm it is owned by the **nearest common ancestor** of
      the two parties. A boundary between entities in different branches rises
      above the immediate parent.
- [ ] **D2a.** Confirm each interface is **stated in terms of the owning level's
      immediate descendants**, not the deeper entities that actually carry the
      traffic. An L1 interface says *System A ↔ System B* even when the exchange
      is between sub-systems inside them. Naming anything deeper publishes
      internals across a boundary that level cannot bind, and couples the two
      systems' internals to each other. This is what keeps an interface a
      contract rather than a description of today's implementation.
- [ ] **D3.** Classify each as `external-icd`, `internal`, `physical`, or
      `build-time`.
- [ ] **D4.** Confirm no interface artifact lives in the repo of the thing it
      describes. If one does, it is filed one level too low.
- [ ] **D5.** Record who **drafts** each interface if it is not the owning level —
      ownership is arbitration authority, not authorship.

## E. Traceability

- [ ] **E1.** Confirm every artifact has a parent, and that the parent is at the
      level above or at the same level one tier up. Everything traces upstream to a
      customer-defined need; safety is not an exception.
- [ ] **E2.** For parents in another repo, confirm the reference resolves against
      the parent repo as it actually stands — not as you remember it.
- [ ] **E3.** Confirm the requirements-tool identity (Jama key) is recorded for
      any artifact that has one. Jama is the ratified source of truth and identity
      authority; a filename is only resolvable by whoever has the repo.

## F. Before the first review

- [ ] **F1.** Every artifact carries a maturity state, if this repo runs maturity
      gates. Default is `M1`.
- [ ] **F2.** Nothing claims a state above `M1` without a promotion record.
- [ ] **F3.** Run `validate-artifacts`. Zero errors.
- [ ] **F3a.** Run `validate-artifacts --require-parents` — the CI gate. It
      resolves every outbound parent reference against the parent repo. Passing
      locally without this flag only means the references are *well formed*.
- [ ] **F3b.** Run `emit-artifact-index` and commit `artifact-index.json`, so
      child repos can resolve their parents against this one.
- [ ] **F4.** Confirm the validator reported a **non-zero artifact count and the
      tiers you expected.** "Validated 0 artifact file(s)" with a green exit means
      nothing was checked — usually a tier name that does not match the schema.
- [ ] **F5.** Record every gap found while working this list, with a date and an
      owner, in `GAPS.md`.

## G. The question to ask at every file

> **Does this file assert a decision that is not recorded in `standard/`?**

If yes: either record the decision, or delete the assertion. Do not leave it
asserted and unrecorded — that is how a default becomes policy without anyone
choosing it.

---

## Recording a gap

Date, what is missing, who owns it, and what unblocks it. A gap with no owner is a
gap that will be rediscovered rather than closed.
