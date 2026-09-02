# Term dates 2026-27

Written once, under ORDER VB-RUN14 section C, so that "Spring 2 dates not in
the repository" is retired for good. Every count in the order is bound to these
dates, and CALENDAR_SPINE.json (its `termDates` block) points here.

Source line, verbatim from the order:
  School year 2026-27, Redcar & Cleveland published dates, 40 teaching weeks,
  shape 8·7·6·5·7·7.

  Autumn 1   absolute weeks 1-8     w/c Tue 1 Sep to w/c 19 Oct 2026
                                    half term 26-30 Oct
  Autumn 2   absolute weeks 9-15    w/c 2 Nov to w/c 14 Dec
                                    term ends Fri 18 Dec
  Spring 1   absolute weeks 16-21   w/c 4 Jan to w/c 8 Feb 2027
                                    half term 15-19 Feb, the end of week 21
  Spring 2   absolute weeks 22-26   w/c 22 Feb to w/c 22 Mar
                                    term ends Thu 25 Mar, Easter, the end of week 26
  Summer 1   absolute weeks 27-33   OUT OF SCOPE for this order
  Summer 2   absolute weeks 34-40   OUT OF SCOPE for this order

BOUNDARY = 26. The horizon is "lessons required through absolute week 26" and
nothing further. Any target whose ruled week is greater than 26 is excluded from
every count and every wave.

The mapping from a term-relative label to an absolute week, which is the only
way a week is ever derived in this estate (a week is a property of a workbook
cell; no tool reads one from a filename or a folder, and g27 enforces that):
  Aut1 Wn -> n          Aut2 Wn -> 8 + n
  Spr1 Wn -> 15 + n     Spr2 Wn -> 21 + n
  Sum1 Wn -> 26 + n     Sum2 Wn -> 33 + n
  Absolute week 8 is the enrichment week and has no workbook row.
  Spring 2 has five timetabled weeks, so its sixth column is NOT-TIMETABLED.

On the workbooks. They count 7/7/6/6/6/7 = 39 weeks. That is a labelling
dialect, not a disagreement about dates: the workbooks are never edited, and the
spine re-keyed in run 11 (VB-RUN11F SPINE) is the authority for converting a
workbook cell's term-relative position into an absolute week. CALENDAR_SPINE's
own `calendar.termBlocks` block still carries the older 7/7/6/6/6/7 shape and is
retained as history; it is not read for any week.

This file carries no bulleted list, on purpose. Register files in this estate are
tokenised bullet by bullet by the g10 name gate, and this is a record, not a
register.
