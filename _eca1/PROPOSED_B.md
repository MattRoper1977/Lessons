# ECA-1 PROPOSED_B — visibility judgement calls for Matt (PART B)

The ruled default (§7 of the order) is applied everywhere; these are the calls made
inside it, plus alternatives Matt may prefer. Veto from the contact sheets in
`_eca1/visibility/<chassis>/` (3 slides × default/revealed × 390/1440 px each).

## 1. Per-role reveal split — PROPOSED, not built
One switch reveals staff + route + lundy together (kept simple per the order). If a
per-role split is wanted (e.g. reveal Lundy to the class without staff notes), the
tags already carry roles (`data-mbm-guide="staff|route|lundy"`), so it is a CSS +
three-button change — no re-tagging.

## 2. The dedicated Lundy Loop slide now opens empty-ish (v5 + hum chassis)
In ASDAN/D&T/Art/Humanities decks all four SPACE/VOICE/AUDIENCE/INFLUENCE boxes sit
on ONE dedicated slide, which now shows just its heading until G is pressed (see the
v5-asdan contact sheet). The ruled default hides Lundy everywhere except Exit/close,
and Matt's words name the Lundy loop as hideable — but if a whole quiet slide feels
odd in the room, the alternative is: keep the dedicated Lundy slide's boxes visible
and treat only the science-style per-slide strips as clutter. One-line patcher
change; say the word.

## 3. Science access lines KEPT (deviation-from-letter, recorded as ruled)
`retr-route` ("Non-reading route: point to it, say it… Next step up:") and the
access-reassurance notes ("You can change how you answer. The Science goal stays
the same." / "Access changes the response route, not the GCSE Biology entitlement."
/ GROW's "A pause or different route changes access, not the learning goal.") stay
visible: despite staff-ish phrasing they are the pupil's access offer, and hiding
them would cut against the accessibility invariants. The class NAME `retr-route` is
routing-of-response, not lesson-route commentary.

## 4. What was classified staff on science (hidden by default)
`teacher-say` ("Staff influence opener — SAY, don't record…"), `retr-declare`
("Weeks 1 and 2 were baseline…" — the order's own example, route role), the
voice-keyed `.note` blocks ("Arrival retrieves…", "Fade it:/Fade:"), the GROW
"TA fade route:" tail inside WORD HELP (wrapped, counter-safe). Pupil-voiced notes
were left alone. If any of these reads pupil-facing to Matt, it is one tag.

## 5. Unclassified organs left visible (v5-art)
"Watch for:" (7) and "Second model:" (7) li-boxes read as modelled pupil content and
stay visible; if Matt reads them as staff guidance, they are one label each in the
patcher's STAFF_LABELS list.

## 6. Science source-note provenance lines
Tagged `route` (they carry "TEST prototype · derived from … at main SHA … " text).
Note for a future pass: that sentence itself looks stale now that SCA-1 treats
v3_40min as the audited production suite — a wording refresh needs its own ruling.

## 7. Slideshows ART suite (24 decks) — not in PART B
`{Build,Grow,Launch}/Slideshows/*_ART_*` remain untagged (outside the ordered
universe, which names Art = Art_Teesside). If they are still teaching surfaces,
the v5 patcher covers them unchanged — one command in a follow-up.
