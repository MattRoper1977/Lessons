# `quality/toolkits/` — the trust layer for the support estate

**STATUS: draft · OWNER: Matt · Pass TK-1, 2026-08-04 · base `74e6fee`**

Source: the read-only *SEMH Resource Toolkits* audit of 2026-08-04, taken at `6aaffb7`. That audit covers the
**support/toolkit layer** — hubs, Lundy Loop staff/QA/SEND tools, schemes of work, planners, evidence packs,
safety cards, knowledge organisers, primary hubs, Tutor Time/RSHE — and is a **separate audit** from the SEMH-1
lesson audit whose output is the nine files in `quality/`.

## What this directory is for, and what it deliberately is not

The audit's central judgement, adopted here verbatim:

> The pedagogy is often stronger than the governance around it. Preserve the practical, visual, relational and
> authentic design; **standardise the trust layer** — status, evidence, accessibility, safety, data and current
> awarding-body mapping.

So this directory standardises **only** the trust layer. It does not standardise how a toolkit looks, teaches or
is sequenced, and nothing here is a licence to make two toolkits resemble each other.

## Relationship to `quality/` — extension, not duplication

`quality/` already carries nine files from Pass SEMH-1 (merged at `73d6330`). This directory **extends** them.
Where a question is already answered upstairs, these files cross-reference rather than restate — a second copy
of a rule is the R-G01 cached-claim shape, and it goes stale silently.

| upstream file | what it owns | what `toolkits/` adds |
|---|---|---|
| `DELIVERY_READINESS_CHECKLIST.md` | the **seven readiness states** of a *resource* (drafted → print-offline-verified) | nothing — reused as-is. `CLAIMS_REGISTER.md` adds an orthogonal axis about a *pupil's evidence*; see the warning there |
| `QUALIFICATION_CLAIMS_REGISTRY.json` | per-claim provenance rows `Q-001…Q-010` | `QUALIFICATION_CLAIM_REGISTER.md` adds a **per-product** view and cites Q-IDs; it introduces no new claim rows |
| `SAFEGUARDING_CONTENT_GATE.md` | **safeguarding** content — disclosure routes, help lines, legal claims to pupils | `SAFETY_CONTENT_GATE.md` covers **physical safety** — burns, tools, dust, benches. Adjacent, not overlapping |
| `SEMH_PEDAGOGY_STANDARD.md` | SEMH pedagogy non-negotiables | `TOOLKIT_HOUSE_STANDARD.md` §C defers to it entirely |
| `INDEPENDENT_WORK_RUBRIC.md`, `PATHWAY_CHALLENGE_MAP.md` | independence and demand | referenced; not restated |
| `DESIGN_prompt_record.md` | the accepted prompt-fading design (SEMH-1 §8) | **nothing.** TK-1 authored no rival scheme — see `CLAIMS_REGISTER.md` §Deferred |
| `CONTENT_INTEGRITY_RULES.json`, `LESSON_AUDIT_SCHEMA.json` | machine-readable lesson checks | out of scope here |

## The files

| file | what it settles |
|---|---|
| `TOOLKIT_HOUSE_STANDARD.md` | the A–H standard every support toolkit is held to |
| `CLAIMS_REGISTER.md` | the controlled evidence-status vocabulary + the Phase-0 claims census |
| `QUALIFICATION_CLAIM_REGISTER.md` | one row per product actually delivered: what may and may not be claimed |
| `DATA_GOVERNANCE.md` | purpose, minimum fields, retention, export and deletion for local-only tools |
| `SAFETY_CONTENT_GATE.md` | safety/medical wording needs a source, a checked date, a review date, local approval |
| `ACCESSIBILITY_CONTRACT.md` | the WCAG 2.2 AA interactive baseline and the print baseline |
| `METADATA_SCHEMA.md` | the per-toolkit metadata strip, as a schema plus a bounded pilot |
| `PROPOSED_lundy_definition_reconciliation.md` | **PROPOSED ONLY** — queued into LL-I/B2, applied nowhere |

## Standing constraints these files inherit and must not break

Every one of these is a repository ruling that outranks the audit and outranks the TK-1 brief (**R-SEMH01**).

1. **ASDAN and Trinity centre registration are DONE.** No file here frames either as outstanding. The genuinely
   open QA items are the first-year EQA sampling booking, the IQA-before-EQA rhythm, and names to ASDAN roughly
   four weeks before sampling — all already logged at `_close/OPEN_ITEMS.md` #11.
2. **No hours threshold at any level, for any award.** TQT is guidance. Three fabricated hours-gates have been
   killed in this estate already, and the most recent — the LAUNCH ComSk1 "ten-hour window" — was a false
   accreditation claim on a public site (**R-K04**).
3. **Arts Award: the adviser is trained at Explore, Bronze and Silver — not Gold.** No Gold-facing progression
   claim may be made. A public showing is a **Gold Unit 2** requirement and is never asserted below Gold.
4. **"Portfolio of record" is not marketing.** It is Matt's deliberate declaration resolving which of two
   competing print routes is authoritative. It may gain status metadata; it is not softened or stripped.
5. **Lundy closure is settled.** BUILD closes on an adult receiving it; GROW/LAUNCH closure is **pupil-owned** —
   the written line closes it. An adult may be audience or next-step-giver, **never a signatory, verifier or
   receipt-mark**. Reading is not recording. No daily collection register. **R-A09**: if a second copy of the
   Loop Mark exists anywhere — a list, a sheet, a column, a total — the thing has changed species.
6. **No storage-schema change.** `ps_coldcall_roster` name persistence on school-owned machines is accepted
   (**R-B01**); `coldCall_y10` holds graded objects and must never be naively migrated (**R-B02**). No key
   renames anywhere.
7. **UAS-as-qualification is RETIRED as FALSE** (**R-SEMH06**) and is not re-raised here. TK-1 re-measured at
   `74e6fee` and confirms it.
8. **Sentinel populations are derived, never quoted.** Run `python3 LundyLoop/tools/bundle_facts.py` and read
   *Sentinel · loop-mark (BUILD)* and *Sentinel · written line (GROW/LAUNCH)*. They read 50 and 98 at both
   `6aaffb7` and `74e6fee`; that is an observation, not a constant.

   *This file deliberately does not quote either marker string verbatim.* A document that names a sentinel
   **joins the population that counts it** (**R-G06**, **R-E10**) — the `*.html` derivation of record is
   unaffected because it drops `.md` files, but the whole-repo count moves, and a describer inflating the thing
   it describes is the cached-claim shape one turn out. The command above emits both figures with their
   universe stated, which is the form that cannot go stale.

## Two honesty rules that govern every file here

**No verification was performed against any awarding body's website.** This container has no useful egress to
`nhs.uk`, `asdan.org.uk`, `jcq.org.uk` or `trinitycollege.com`. Anything not confirmed by a document actually in
this repository is labelled **SUPPLIED-BY-AUDIT** with a review-by date of **1 September 2026**, and needs the
named coordinator's confirmation before it is relied on.

**No visual or print claim was rendered.** There is no browser here. Every print or layout statement is tagged
**PRINT-UNVERIFIED** and carries the physical check Matt has to run. A skipped gate is unverified, never passed.
