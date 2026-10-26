# Accessibility contract — support toolkits

**STATUS: draft · OWNER: Matt · Pass TK-1, 2026-08-04 · measured at `74e6fee`**

Scope: the support/toolkit layer. Lesson slideshows are out of scope here.

---

## Interactive baseline — WCAG 2.2 AA

- **Programmatic labels.** Every control has an accessible name: `<label for>` bound to an `id`, or
  `aria-label`/`aria-labelledby`. A visually adjacent caption is not a label.
- **Grouping.** Related controls in `<fieldset>` with a `<legend>`.
- **State.** `aria-pressed` on toggles, `aria-expanded` + `aria-controls` on disclosures.
- **Feedback.** Save, error and validation messages announced via `aria-live="polite"`.
  **Never put `aria-live` on anything that updates per second** — a live-region timer makes a screen reader
  unusable, and that is an accessibility regression wearing an accessibility badge.
- **Keyboard.** Everything operable without a mouse; visible focus; no traps; sensible order.
- **Targets.** 24px minimum; **44px preferred** for anything used repeatedly.
- **Motion.** `prefers-reduced-motion` honoured. **[estate]** Detection must recognise **both** estate
  implementations — the CSS `@media` query **and** the JS `matchMedia` + class-toggle pattern (`body.reduce …`).
  A CSS-only classifier once called ASDAN a defect when its implementation is in fact better, because it also
  gates audio.
- **Meaning never carried by colour or symbol alone.** A red border, a green tick or an emoji needs a text
  equivalent.
- **Visibility gating.** **[estate] R-E22** — hide with `visibility`, never `opacity` alone. An animation with
  `fill-mode: both`/`forwards` applies its final keyframe in the CSS animation origin, which outranks every
  normal author declaration regardless of specificity, so `opacity: 0` can be defeated. Pair the two.

### Measured at HEAD — `LundyLoop/2_leadership/Loop_Walk_Logger.html`

| check | value |
|---|---|
| form controls | **9** |
| `label for=` | **0** |
| `<fieldset>` / `<legend>` | **0** / **0** |
| `aria-live` | **0** |
| `aria-pressed` / `aria-expanded` | **0** / **0** |
| network egress constructs | **0** — see `DATA_GOVERNANCE.md` |

The gap is real and is TK-1 Phase 5's target. The zero-egress property is a **constraint on the fix**: no
remediation may introduce a font link, an icon CDN or a `<form action>`.

### Emoji-only meaning — measured, and largely a non-finding here

The audit flagged emoji-only cues. On the sampled support surfaces —
`BUILD_ASDAN/Resources_and_Tools.html`, `BUILD_ASDAN/BUILD_ASDAN_Hub.html`, `Loop_Walk_Logger.html`,
`Loop_Passports.html` — the count is **0 emoji each**. Emoji-carried meaning lives in **lesson slideshows**
(`👀 Look:`, `🏅📸✍️`), which are out of scope. The rule below stands for new work; there was almost nothing to
fix on the support layer, and that is recorded rather than quietly padded.

**Rule for new work:** every symbol pairs with a written label, and meaning survives monochrome, a screen
reader, and an environment with no emoji font.

---

## Print baseline

**Body text is normally 11.5–12pt or larger.**

### Measured at HEAD — the eleven `WEEKS[]` evidence-pack generators

Eight `Art_Teesside` packs carry an identical size ladder — they are clones of one generator:

```
6.6 · 6.8 · 7 · 7.2 · 7.4 · 7.6 · 7.8 · 8 · 8.2 · 8.4 · 8.6 · 9.4 · 9.6 · 12.5 pt
```

**The floor is 6.6pt, not the audit's 7pt.** Three `Humanities_Teesside` packs express sizes in non-`pt` units
and are a separate model, unmeasured here.

### The honest remedy, and why the base size is not simply raised

These packs are **one page per week by design**. Raising a 6.6pt body to 11.5pt inside a fixed A4 page does not
produce a readable pack; it produces a pack with content missing, and the loss would be silent.

So the contract is:

1. **Raise measured-small body text toward ≥11.5pt wherever the layout survives it** — verified by eye on paper,
   not asserted.
2. **Add a "Large print" render option to every `WEEKS[]` generator.** It scales type and spacing and **may
   paginate**. Pagination is the honest cost of legibility; one-page-per-week is a design choice, not a
   requirement, and it is not worth a pupil not being able to read the sheet.
3. **Content is preserved in meaning across both renders.** Part badges, recovery tiles, locator forms,
   authorship rows and *"the adviser audits Parts, not attendance"* all survive intact.

**PRINT-UNVERIFIED.** This container has no browser; print geometry cannot be measured here, and a skipped gate
is unverified, never passed (`quality/DELIVERY_READINESS_CHECKLIST.md` state 7). Matt's physical check is named
in the readback.

### Alternative evidence — no criterion may be handwriting-dependent

Every Evidence Locator Form carries locator lines for **audio · video · artefact · observation · digital
record**, alongside the written route. A pupil who cannot write fluently is not thereby unable to evidence a
criterion, and a one-page pack must never become the only permitted container.

---

## Offline

Core content and navigation work with the network disabled. **No external font, script, style or image host.**

**Measured at HEAD:** `primary/index.html:8–10` imports Google Fonts (`preconnect` ×2 plus a `css2?family=`
stylesheet) despite the primary estate's offline-first positioning. Confirmed; fixed on Phase 5 for the hub
**only**. Primary **lesson** files and unit `index.html` files carry the same import and are **template-locked**
(§3) — recorded as debt, untouched. Two `Tutor_Time/` decks also carry it; same disposition.

---

## What this contract does not ask for

- Not a redesign. The audit judged the pedagogy and visual identity strong; this contract is a floor under them.
- Not uniformity between toolkits.
- Not the removal of handwriting as a route — only the removal of handwriting as the **only** route.
- Not an `aria-live` region on a ticking timer. Named explicitly because it is the obvious wrong fix.
