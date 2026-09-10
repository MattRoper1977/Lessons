## D19 — A manifest entry with no week is a data defect, not a labelling decision

Granted by Matt, 2026-09-09, on the amendment argued in
`_sx2/FINDING_relabeller_scope.md` §4b.

The rule Matt started from refuses any reference to a week outside the folder's
own sequence. It was silent on a third case: a file the folder's manifest *does*
list, whose entry carries no `week`. `Grow/v3_40min/manifest-v3.json` is the only
one in the estate — its Build and Launch siblings carry `week`, it does not.

Those are not out-of-folder references. They are in-folder references the
manifest cannot currently answer. **Adding the missing `week` fields would move
them from refuse to resolve without any judgement about what a pupil reads** —
which is the whole test. So it is referred for data repair, and the tool refuses
it under its own reason code (**F3**) rather than lumping it in with F2.

The repair itself is not a licence to derive. §2 of LF1-I applies: a week is
recovered from an authority or it goes on a list for Matt. The same rule that
governed the 121.

### D19 as amended — Ruling 2, LF1-M, 2026-09-09: missing is not inapplicable

> - **ABSENT** week field, where a week exists and should be recorded → manifest
>   defect → **F3** → repair.
> - **INAPPLICABLE** week, where no week will ever be correct (the three
>   `Spr2·W6`) → not a defect; repairing it would mean inventing a week.

A manifest entry may therefore carry an **explicit no-week marker with a stated
reason**, and the tool refuses it under a new code:

> **F6.** Entry carries an explicit no-week marker. The literal label stands. Not
> a defect, not a backlog, no repair.

The reason is the whole marker. `noWeek: true`, `noWeek: ""` and a blank string
are **not** markers and fall back to F3 — "this has no week" without "because …"
is indistinguishable from having forgotten, and the point of the amendment is to
separate exactly those two. Accepted forms: `noWeek` or `weekNotApplicable`,
either a non-empty string or an object carrying `reason`.

The three markers written under this ruling all quote the same authority:
`_sownb/TERM_DATES.md` — *"Spring 2 has five timetabled weeks, so its sixth
column is NOT-TIMETABLED"* — plus the collision the mapping makes explicit
(`Spr2 Wn → 21+n` puts a sixth at 27; `Sum1 Wn → 26+n` already holds it).

**What a pupil reads on those three pages, measured rather than assumed.** All
three already render `BUILD/GROW/LAUNCH · SCIENCE · Lesson 10 of 10` (11 of 11
for GROW). `Spr2·W6` survives only inside `data-mbm-cal`, the reversibility
store, which is never rendered. Browser census over all three, every route:
**`Spr2·W6` renders 0 times** on deck, print, guide and accessible names, against
a positive control ("Lesson 1") rendering 14/15/15 on the deck. So there is no
literal calendar label there to be wrong on its face, and F6 defers nothing.
