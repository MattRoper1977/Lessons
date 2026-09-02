# Changes for planners

Things the timetable, the SoW or a curriculum lead needs to decide or know. Roles
only — no names. Each entry says what changed, who it is for, and what happens if
nobody acts.

---

## 1 · Capacity: three cells are excluded from lesson counting

Ruled 2026-09-02 (D-G). Three weekly-plan cells resolve to something that is not a
lesson in this estate:

- **Behaviour Intervention** — an intervention slot, not a taught lesson. It is
  staffed and timetabled, but no deck is owed for it.
- **DT (two cells)** — out of scope for this build; no subject tree exists here.

They are excluded from both readings of coverage, so the horizon count never shows
them as gaps. **For the curriculum lead:** if either is meant to carry a taught
lesson with its own deck, say so and it re-enters the count. If nobody acts, they
stay excluded and no deck is ever authored for them.

## 2 · The BUILD lane has no named ASDAN period

Ruled 2026-09-02 (D-I). BUILD ASDAN work is real and is being authored, but the
BUILD lane's timetable shows no slot explicitly labelled ASDAN — it is taught
inside the lane's existing periods (**timetabled by practice**).

**For the timetabler:** please name the slot the BUILD lane's ASDAN work occupies,
so the evidence a pupil produces can be pointed at a period on the timetable. If
nobody acts, authoring continues against the workbook rows and the slot stays
unnamed — which makes an external verifier's question ("when is this taught?")
harder to answer than it should be.


## 3 · LAUNCH Science weeks 9–15: labels back to their filename numbers

**Superseded 2026-09-02 by ORDER VB-RUN11F (SPINE).** The one-week offset that
run 8 applied was the old spine's error, not the lessons'. On the confirmed
2026–27 calendar (`_sownb/CALENDAR_2026_27.json`: Autumn 1 = 8 weeks, half term
26–30 Oct, Autumn 2 = 7 weeks) the deck called W9 teaches the week commencing
2 November, which is absolute week 9 and workbook cell C39. Every label and
config week in the W8–W13, W14 and Autumn 2 packs has been returned to its
filename number: W9 → week 9 … W13 → week 13, the W14 trio → week 14, the
Autumn 2 W7 trio → week 15 (C45). The cell citations were already right and
did not move. Nothing was renamed.

**For anyone reading a timetable or a folder:** the filename, the label and the
cited cell now agree. If a printed planner still shows the run-8 labels, the
lesson file is the authority.

## 4 · The enzyme and amylase trio is Week 8, enrichment

Updated 2026-09-02 (SPINE). Absolute week 8 (w/c 19 October, the last week of
Autumn 1) is an enrichment week with no workbook row. The three LAUNCH Science
enzyme and amylase lessons sit there: they are labelled **Week 8 Enrichment**,
carry `week: 8` with the placement "enrichment — week 8, no workbook row", and
stay live in their folder. They are still never counted as covering a workbook
cell.

**For the curriculum lead:** the trio now has a week. If a workbook row is
ever written for week 8, the lessons are already in place for it.

## 5 · Planner drift after the spine change (2026-09-02)

The 2026–27 calendar moved every absolute week number from Autumn 2 onward up
by one against the old spine: Autumn 2 week 1 is now absolute week 9 (not 8),
Spring 1 week 1 is week 16 (not 15), Spring 2 week 1 is week 22 (not 21), and
Spring 2 has five timetabled weeks, so its sixth column is not timetabled.
Autumn 1 is unchanged.

- **BUILD:** the SharePoint planners for weeks 1–8 and the science rows of the
  Autumn Year Plan were corrected by hand on 2026-09-02. Do not re-flag them.
- **GROW and LAUNCH:** the planners for those pathways have **not** been
  checked for the same drift in their support and evaluation columns. That is
  a Cowork job for the pathway leads, not something the lesson build can do.
- **Any week whose absolute number moved** (every week from Autumn 2 onward)
  should be read from the calendar file, not from a planner printed before
  2 September 2026.
