# Live-Teach — what was deferred, and why

The handover note. Everything the build did **not** do, with enough context to
decide each one without re-reading the whole ledger. Nothing here blocks using
the kit; several items are decisions that are yours rather than mine.

---

## 1 · Safeguarding items still open (from LT1)

These came out of the pupil-name sweep and were deliberately left.

**C1 — CLOSED 2026-08-26 (sitting SAT-F §6).** `biology/Structure_of_the_Thorax.html:1372`
carried a nine-name `Y10_FALLBACK` list. On Matt's recorded word the freeze was
lifted for that one file and it took the same one-line neutralisation the other
twenty-three files got — nine names to `Pupil A`–`Pupil I`, array length and
quote style preserved. `eviRoster()` at :1379 only reads the list when the
pasted roster is empty, so behaviour is unchanged. The legacy-science freeze
otherwise stands; no other file under a frozen path was touched.

**C4 — NEW, found by the same census, NOT fixed.** Closing C1 meant re-running
the nine-name sweep estate-wide, and it surfaced a line LT1 never read:
`ASDAN/Consent_Aimee_La.html` and `ASDAN/Consent_Aimee_P2.html` each carry a
teacher-facing TA deployment note naming **three real pupils** by first name
(one of them the distinctive hyphenated entry), plus a named adult. LT1
classified this whole `Consent_*` family under contact-sheet **B1** — the
filename character is adjudicated fictional, which is correct — and so never
looked past the filename at the body text. The other eight `Consent_*` files
are clean; the pattern appears nowhere else in the estate. It is one line,
duplicated across the two files.

Left unfixed deliberately: this is a safeguarding change, and your rule is that
safeguarding changes are not self-merged — the same rule that held C1 for a
year. It needs the same one word. The fix is the neutralisation LT1 already
uses. **These two files are live on Pages**, which is why this is the first
item in the readback rather than a footnote.

**C2 — two strings in the site repo.**
`mattroper1977.github.io`: `uas/app.html:449` (a placeholder caption) and
`asdan/moderation-lab/index.html:597` (a demo forename). Both read as demo data
— surname "Demo", an "e.g." caption — but each first name coincides with a real
class member. Outside this order's scope; worth a site-repo pass.

**C3 — git history.**
The names removed in LT1 remain in this public repo's history. Clearing them
needs a history rewrite and a force-push across a repo with live Pages
deployments. Disruptive, and your call — not attempted.

## 2 · Things I could not verify from here

**The served bytes.** This container's proxy refuses `madebymatt.uk`, so I
could never fetch the live page. Everything is verified against the files in
the repo and in a headless browser; **that the deployed page matches** is the
first item on `LIVETEACH_PHONE_CHECKS.md` for exactly this reason.

**Real hardware.** A USB clicker's third button, how the amber bell reads on
your actual projector lamp, whether high-lumen is the better mode in your room,
and whether a printed worksheet measures true on paper. All in the phone-check
list.

**Screen-reader behaviour.** Live regions, labels, focus order and announcement
text are checked structurally and by computed style. They have not been heard
through NVDA or VoiceOver. If a pupil or colleague uses one, that pass is worth
booking.

## 3 · Decisions taken under the order that you may want to revisit

Each was made under a delegated decision in ORDER LT-GO. Quote the override
line and it changes.

**The roster is session-only (D2).** You paste the class list each lesson and
it dies with the tab. The alternative — remembering it on the device — would be
more convenient and is what the original spec's P1 assumed. It was ruled out
because the safeguarding promise gets much harder to keep once a class list is
written to a disk in a classroom. *Override: "let the picker remember the
roster in localStorage."*

**The picker exists on the projector too (D1).** In a one-screen room the
projector *is* the class screen, so the panel shows the list to everyone while
it is open. The alternative is HUD-only, which would leave single-screen
teaching with no picker at all. The panel says plainly what it is doing.
*Override: "make the picker HUD-only."*

**Sound never persists.** Turning it on lasts for that session. This is
stricter than the spec's "off by default" and was chosen because a toggle that
remembers "on" from last lesson is precisely the sensory surprise the rule
exists to prevent. *Override: "let the sound toggle persist."*

**The worksheet does not print the answer.** It moved to the HUD. In a
one-screen room that means you work `v = f × λ` yourself, which is a second's
arithmetic, rather than the pupils reading it off their own sheet.
*Override: "print an answer box on the worksheet."*

**Version 6 QR cap.** Share addresses over 106 bytes cannot be encoded; the
modal says so and keeps the address selectable. In practice only a long tag
gets you there. Lifting it means versions 7+ and a fresh round of decode
proofs. *Override: "extend the QR encoder past version 6."*

## 4 · Known limits, stated rather than fixed

- **Same browser, same device.** `BroadcastChannel` cannot cross machines. A
  phone HUD driving a classroom PC is not possible, and the kit says so instead
  of pretending. Making it work needs a server, which this estate does not have
  and probably should not acquire for this.
- **A bus message is not a user gesture**, so the HUD cannot put the projector
  into fullscreen. It explains F11 rather than failing silently.
- **Forty names, thirty-two characters each.** A larger paste is capped and the
  kit says how many it dropped.
- **The lesson library is one manifest** (`waves_v1`). The stage engine, the
  units checker and the worksheet are all general; the content is not. Adding
  a lesson is a small data file under `liveteach/manifests/` — and
  `tools/liveteach/units_check.mjs` will refuse it if a claim does not
  recompute.
- **Reduced motion is honoured; reduced *sound* has no OS signal.** Audio is
  off by default instead.

## 5 · If you want more

Obvious next things, in the order I would do them:

1. **A second lesson manifest** — the machinery is built and gated; this is now
   authoring, not engineering.
2. **The screen-reader pass** above.
3. **Worksheet variants** — the print layer is a general builder; a "describe
   what you see" sheet or a graph-axes sheet would be small additions.
4. **A tally history across a lesson** — the sparkline records it already; a
   "compare to last lesson" view would need storage, and that decision is the
   same one as the roster's.

---

**Where the detail lives.** `LIVETEACH_LEDGER.md` has a block per phase: what
shipped, which gates ran, which negative controls were named, and what each
adversarial review round found. `LIVETEACH_RECON.md` has the original estate
survey. `LIVETEACH_LT1_CONTACT_SHEET.md` has the redacted before/after for the
name sweep.
