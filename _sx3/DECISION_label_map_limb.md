# Decision — the label-map limb

## Signature

> Ruling thread, 2026‑11‑04: a recorded title‑slide quote still proves a page's timing when the
> quote, after the one committed word map, is present verbatim in the page's current visible text
> and (for a Science row) every term·week token is still present. The map is applied to the quote
> only, never to the page. No existing limb is changed. Rationale as recorded here.

## What the limb is

`tools/catalogue/build_lesson_order.py` proves a page's timing when its bytes no longer match the
`sha256` recorded in `tools/catalogue/TERM_AND_STYLE_EVIDENCE.json`. The existing limbs — the
Science term·week token limb (`_sx3/DECISION_quote_limb.md`), explicit cell, preserved outcome,
the Humanities strand row, the Science row and label limbs — each prove the page through its
calendar binding. A page none of them proves lands in `unresolvedTiming`, and for a `recommended`
page that is an `AssertionError`.

The **label-map limb** (`label_map_proof`) is one more arm, tried **last**, only where a string
`own title slide declaration` quote is recorded and no other limb holds. It proves the page when:

1. every recorded title‑slide quote, after the word map, is present verbatim
   (whitespace‑normalised) in the page's current **visible** text — every text node outside
   `<script>`, `<style>` and `<template>`;
2. each quote still carries the same half‑terms and term·week keys it was recorded with, after
   the map as before it;
3. for a page with a `SCIENCE_WEEK_BINDINGS` row, every term·week token of that row is still in
   the visible text;
4. the quote names a half‑term at all — a quote with no calendar binding proves nothing.

The Science title‑stage claim check (ruled on W16B) still outranks it: a stray week claim refuses
the page whichever limb proved it.

## The word map

One committed file, `tools/catalogue/LABEL_MAP.json`, `{"map": [{"from": ..., "to": ...}]}`.
It carries the three public pathway entries now: `BUILD→BASE`, `GROW→TRACK`, `LAUNCH→SUMMIT`.

<!-- A second entry, mapping the former ownership label in the `.sow-strip` quotes to "Made by Matt",
     is owner-supplied: the owner adds it to LABEL_MAP.json. The word is written nowhere in this repository. -->

The loader (`load_label_map`) refuses, before any quote is read, an entry that is not letters
only (spaces, hyphens, apostrophes and ampersands allowed inside), an entry that names a season or
week word (`Aut`, `Autumn`, `Spr`, `Sum`, `W`, `Week`), `from == to`, and a word mapped twice.
The map is applied in **one pass**, whole words only, to the quote and never to the page, so no
entry's output is read by another and a word the map does not name is never touched.

## Why it is narrow enough

The map cannot write a digit, so it cannot write a week or a half‑term; and the judge compares
the quote's half‑terms and term·week keys before and after the map and refuses any difference.
What remains is a verbatim quote — the original, pre‑narrowing quote limb, with a fixed set of
label words allowed to differ. A page whose half‑term or week moved no longer carries the recorded
quote in any mapped form, so the limb refuses it by name
(`the mapped quote is not in the current visible text`).

An **empty map** is exactly the verbatim quote limb: a relabelled page is refused.

It is the **mapped** quote that must be present, not the recorded one. While the map carries
`BUILD→BASE`, a page that still says `BUILD` is not proved by this limb — its recorded digest is
what proves it — so the limb reaches only pages that were relabelled exactly as the map says.

## Red proofs

`tools/catalogue/restamp_evidence_sha256.py --self-test` (pure judge, loader, and the wiring
through `derive()` on a real page's bytes moved in memory) and `tools/ux2/unit_tags.py --self-test`
(the re‑proof branch of `verify_classes`):

| case | outcome |
|---|---|
| quote mapped `BUILD→BASE`, verbatim in the visible text | **proved**, listed in `labelMapProofs` |
| the page's half‑term moved (`Aut 1` → `Aut 2`) | **refused** |
| the page's week token moved (`Aut1·W3` → `Aut1·W4`) | **refused** |
| a Science row token absent from the text | **refused** |
| empty map, page relabelled | **refused** (the verbatim limb, unchanged) |
| empty map, quote verbatim | proved (today's quote limb) |
| a word the map does not name this way (`BUILD→SUMMIT`), or an entry absent from the map | **refused** |
| a map entry that would move a half‑term (`Aut→Spr`) | refused by the loader and by the judge |
| a quote naming no half‑term | **refused** |

Measured 2026‑11‑04 on `Build/Slideshows/BUILD_HUM_W1_Human_Timeline.html` (digest‑bound, no
strand row, no Science row — no other limb reaches it): relabelled `<title>`/`.sow-strip`
`BUILD→BASE` → `labelMapProofs == [page]`, `restamp_plan` re‑stamps it; `Aut 1→Aut 2` in the
`.sow-strip` → `unresolvedTiming`, `restamp_plan` refuses with the limb's reason.

## What is unchanged

Every existing limb, every assertion, and every field of the evidence file other than the
`sha256` a reviewed `--write` re‑stamps. On the current tree the limb proves nothing
(`labelMapProofs` is absent from `lesson-order.json`), so the projection's bytes are those
`derive()` produced before this limb existed.

## Pins

`build_lesson_order.py`, `restamp_evidence_sha256.py` and `check_catalogue_static.py` are
reviewed, digest‑pinned tools, so the cross‑estate gate reads their new bytes as
`reviewed catalogue bytes differ` until the next re‑pin; that re‑pin is the ruling side's, not
this branch's. `LABEL_MAP.json` is a reviewed record of the same standing as the strand and
Science binding records and should join `CATALOGUE_PINS` at that re‑pin.

## Where it is wired

- `build_lesson_order.derive()` — one more `proved` arm; `labelMapProofs` and `labelMapRefusals`
  in the projection, named only while a moved page awaits its re‑stamp.
- `restamp_evidence_sha256.py` — `--write` re‑stamps a page the limb proves; a refusal names
  `labelmap` with its reason.
- `unit_tags.verify_classes` — the re‑proof branch counts a moved digest the limb re‑proves, the
  quote naming the same half‑term.
- `check_catalogue_static.py` — re‑judges every listed label‑map proof on the tree.
