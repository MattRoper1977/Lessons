# ECA-1 — Decisions record

Pass: `eca-1-2026-08-19` · written at the time, per `_bsg1`/`_gsafix1` convention.

## Base and branch

- **BASE / ROLLBACK SHA**: `72778591e8c1fe1d9c5b979c90ccbbd868de4b3a` (`origin/main`
  at pass start, 2026-08-19). Local HEAD verified equal before any edit.
- **Branch ruling (PART A):** the master prompt names `claude/eca-1-correctness`; the
  session's designated branch is `claude/new-session-jbjr5k`. Per the convention
  recorded in `_gsafix1/DECISIONS.md` ("system instruction outranks the prompt's
  spelling"), PART A runs on the **designated branch**. PART B (a second PR by design)
  has no second designated branch, so it takes the prompt's name
  `claude/eca-1-visibility`, cut from main after A merges.
- Merges are **conditional** on the §9 gates, authorised by the master prompt itself
  ("merge --no-ff only if all green").

## Identity gate — 6/6 PASS (measured)

remote = MattRoper1977/Lessons · ASDAN lessons 31/18/30 (START_HERE excluded) ·
Art_Teesside with House_Standard + Partnership_Log · humanities 24 at
{Build,Grow,Launch}/Slideshows + SoW/Tracker in Humanities_Teesside (folder trap
confirmed: no lessons there) · resources.json present · sentinels derived
**50 loop-mark / 123 written-closure** over git-tracked *.html at origin/main
(patterns: `ll-g:loop-mark`; `What I said, and what it changed`).

## Inherited state (verified, not assumed)

- **PR #133 MERGED** (2026-08-18, merge b0379c7). Toggle present on exactly 85 decks
  (31+18+30 ASDAN + 6 D&T) — extend in PART B, do not duplicate. **C7 LANDED**
  (GROW Scheme_and_Resources now reads "a registration decision, not a re-teach…
  at most 3 adjacent-level credits count toward an L1 qualification"). **Workbook
  LANDED** (all 7 remaining "10-hour" strings in LAUNCH_Autumn_Year_Plan_ASDAN.xlsx
  negate the rule on ComSk1; A14 carries the dated correction note).
- **SCA-1 absent from main** (no branch/PR/record; science passes on main are
  GSA-1/BSA-1/GSA-FIX-1) → PART B **DEFERS the 35 science v3_40min decks**, listed.
- Humanities year-tag AMBER from the prompt: **already resolved** — all 59 Humanities
  resources.json entries read 2026-27. No metadata edit needed.
- No `_asdan_private/` in this checkout → ASDAN facts mode from `_passpq/SPEC_FACTS.md`.

## Closure-marker vs sentinel ruling

BUILD HUM decks close orally by design ("out loud, as a class, is enough here" +
scribe offer) — no ring+R strip; GROW/LAUNCH HUM W7 lack the written line. Adding
either would move the sentinels (50→58, 123→125), which **hold set-identical at every
commit** by order. Both therefore go to `PROPOSED_A.md`, not to a fix. LL-INST-09 is
the render gate for decks that carry the strip, not a mandate to add one.

## SCA-1 landed mid-pass (2026-08-19)

SCA-1 (science v3_40min) merged to main (e907653, record a810d44) while ECA-1's
audits ran — after this pass's baseline was pinned. Zero file overlap with PART A's
diff; merged into the PART A branch before the conditional merge; sentinels held
50/123 set-identical and the PROTECTED manifest was byte-identical across the
merge. **PART B's conditional therefore resolves to INCLUDE the 35 science
v3_40min decks** (CHASSIS.md's "deferred" note is superseded by this entry).

## Slideshows/*_ART_* (24 decks) — OWNER RULING, 2026-08-19 (SCA-1 CLOSE v2, 3e)

`{Build,Grow,Launch}/Slideshows/*_ART_*` is the **superseded 2025-26 legacy art set**:
Art_Teesside replaced it and it is excluded from every staff pack. **Do not patch it** —
not for visibility tagging, not for correctness. ECA-1 left it untouched (recorded then
as "outside the ordered universe"); this ruling closes the question permanently, and any
PROPOSED item raised against those 24 decks is withdrawn rather than held.
