# ECA-1 PROPOSED_B — visibility judgement calls for Matt (PART B)

The ruled default (§7 of the order) is applied everywhere; these are the calls made
inside it, plus alternatives Matt may prefer. Veto from the contact sheets in
`_eca1/visibility/<chassis>/` (3 slides × default/revealed × 390/1440 px each).

## 1. Per-role reveal split — PROPOSED, not built
One switch reveals staff + route + lundy together (kept simple per the order). If a
per-role split is wanted (e.g. reveal Lundy to the class without staff notes), the
lundy/staff/route tags carry roles (`data-mbm-guide="staff|route|lundy"`) on only 90
of the 175 decks. The other 85 carry PH-3's roleless `data-mbm-guide="1"`, so a
per-role split is a CSS + three-button change **plus a re-tagging pass over those 85**
— not the no-re-tagging change this section originally claimed. (Measured 2026-08-20:
85 roleless + 90 role-valued = 175.)

## 2. The dedicated Lundy Loop slide now opens empty-ish (v5 + hum chassis)
In ASDAN/D&T/Art/Humanities decks all four SPACE/VOICE/AUDIENCE/INFLUENCE boxes sit
on ONE dedicated slide, which now shows just its heading until G is pressed (see the
v5-asdan contact sheet). The ruled default hides Lundy everywhere except Exit/close,
and Matt's words name the Lundy loop as hideable — but if a whole quiet slide feels
odd in the room, the alternative is: keep the dedicated Lundy slide's boxes visible
and treat only the science-style per-slide strips as clutter. One-line patcher
change; say the word.

## 3. Science access lines KEPT (deviation-from-letter, recorded as ruled) — RATIFIED
`retr-route` ("Non-reading route: point to it, say it… Next step up:") and the
access-reassurance notes ("You can change how you answer. The Science goal stays
the same." / "Access changes the response route, not the GCSE Biology entitlement."
/ GROW's "A pause or different route changes access, not the learning goal.") stay
visible: despite staff-ish phrasing they are the pupil's access offer, and hiding
them would cut against the accessibility invariants. The class NAME `retr-route` is
routing-of-response, not lesson-route commentary.

**Ratified under PROP-1 (2026-08-20), and this section understated its own evidence.**
It reads as three strings; there are **four**, and they are not occasional. Measured at
`e63f047`: `Non-reading route` **300** occurrences across 25 decks · `You can change how
you answer` **60** across 10 · `Access changes the response route` **90** across 15 ·
`A pause or different route changes access` **60** across 10 — **510 occurrences, and
every one of the 35 v3_40min lesson decks carries at least one.** Hiding them by default
would have removed the pupil's access offer from the entire science suite, not from a
handful of slides. The ruling to keep them visible stands, on stronger evidence than the
section claimed.

## 4. What was classified staff on science (hidden by default)
`teacher-say` ("Staff influence opener — SAY, don't record…"), `retr-declare`
("Weeks 1 and 2 were baseline…" — the order's own example, route role), the
voice-keyed `.note` blocks ("Arrival retrieves…", "Fade it:/Fade:"), the
"TA fade route:" tail inside WORD HELP on 25 decks (GROW 10 + LAUNCH 15;
wrapped, counter-safe). Pupil-voiced notes
were left alone. If any of these reads pupil-facing to Matt, it is one tag.

## 5. Unclassified organs left visible (v5-art)
"Watch for:" (7) and "Second model:" (7) li-boxes read as modelled pupil content and
stay visible; if Matt reads them as staff guidance, they are one label each in the
patcher's STAFF_LABELS list.

## 6. Science source-note provenance lines
Tagged `route` (they carry "v3 40-minute route · derived from current GROW lesson …"
text). The "future pass" this section asked for has already happened: SCA-1 CLOSE v2
landed the wording refresh (the suite no longer describes itself as a TEST prototype —
measured 2026-08-20: 0 occurrences estate-wide), so that half of this item is closed.
The residual is only that the provenance line still points at the pre-v3 source lesson.

## 7. Slideshows ART suite (24 decks) — not in PART B
`Slideshows/*_ART_*` (24 decks) — CLOSED by owner ruling 2026-08-19 (SCA-1 CLOSE v2, 3e; recorded in `_eca1/DECISIONS.md`): the superseded 2025-26 legacy art set is not to be patched, and no follow-up is offered.
