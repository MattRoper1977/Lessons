## D24 — WITHDRAWN (Matt, 2026-09-09). §8a's amended wording survives it.

**Withdrawn, not superseded: the ruling was correct on the evidence and the
evidence was wrong.** D24 ordered V08's YouTube URL relocated into the staff
aside. It is already there — byte **24,225** in the aside's `Video status:`
paragraph, byte **35,793** in the `DATA` payload that aside renders from.
**V08 needs no relocation and no hold**; it lands with B06, S10 and B07 on the §5
clearance as written.

Three things survive D24 permanently:

1. **The amended §8a wording**, below — a better gate than "0 YouTube", now with
   measured numbers behind it: **0/42 and 0/8 on both limbs**.
2. **`tools/lf1/gate_thirdparty.cjs` as the sole authority** for that gate, with
   its `<details>` scoping intact. A collapsed disclosure is pupil-visible; a
   staff aside is not. That distinction is not to be "simplified".
3. **Its application to GC1 G4**: the Scratch editor and AQA unit links stay,
   because their visible text is a label, not a URL.

The original ruling and the measurement that withdrew it follow.

Ruled by Matt, 2026-09-09. This wording replaces the "0 YouTube" line:

> Zero third-party **LOADS** on any pupil route (no iframe, script src, font,
> image or fetch), and zero third-party **URLs in pupil-visible text**. Cited
> third-party URLs are permitted inside staff asides.

Two properties, and the old wording only measured the first. A count of embeds
says nothing about a URL printed as prose, and a count of `https?://` in the
source says nothing about where it renders.

### The correction I owe on V08

I reported that `V08_Belonging_Without_Assumptions` renders a youtube.com URL on
a pupil-facing surface. **That was wrong.** Both occurrences are in the permitted
place:

| occurrence | where | |
|---|---|---|
| byte 24,225 | **inside** `<aside class="staff" hidden>`, in the `Video status:` paragraph | permitted |
| byte 35,793 | inside `<script>`, the `DATA` payload `note` field the aside renders from | not rendered as itself |

**V08 needs no relocation and no hold.** The error was measuring source with a
regex instead of rendering: the citations live in a `DATA` payload and the page
renders them into the staff aside, which a source scan cannot see.

### The gate, and what it took to make it honest

`tools/lf1/gate_thirdparty.cjs` walks all 8 stages and all 3 task routes with the
staff aside in its default state and reads **text nodes only** — never an `href`,
because a link whose visible text is "Open Scratch" shows no URL while a paragraph
that prints one does.

It got the wrong answer first, and the reason is worth keeping. A **detached**
clone has no layout, so `innerText` degrades to `textContent` and swallows every
`<script>` body — the `DATA` payload included. That reported **25 of 42 decks**
as failing, and the tell was that the pupil-visible count equalled the
staff-aside count on almost every deck: the same citations counted twice. With
`script`, `style`, `template` and `aside.staff` stripped explicitly, it reads
`textContent`, so text inside a **collapsed `<details>`** still counts — a pupil
can open a disclosure, and that is not what "inside a staff aside" means.

### The result, with a two-sided control

| | decks | collections |
|---|---:|---:|
| third-party **loads** | **0** of 42 | **0** of 8 |
| third-party **URLs in pupil-visible text** | **0** of 42 | **0** of 8 |
| console/page errors while walking 8 stages × 3 routes | **0** of 42 | — |

The control proves the gate both fires and stays silent correctly. The same
sentence was planted twice in a copy of V08:

- in footer prose, outside the aside → **caught**, gate red;
- inside `<aside class="staff">` → **not caught**, correctly permitted.

A gate that only ever passes has proved nothing; this one is shown to fail on the
forbidden case and to allow the permitted one.

Collections are measured on their shell, because their `ITEMS` payloads **are** the
deck files — byte-equal minus the pack-link, 42 of 42 — so measuring them again
would be measuring the same bytes twice.

**This gate also governs GROW Computing** (GC1 G4): the Scratch editor and AQA unit
links stay as links with `rel="noopener"`, because their visible text is a label,
not a URL.
