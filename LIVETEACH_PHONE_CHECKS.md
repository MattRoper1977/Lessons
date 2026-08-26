# Live-Teach — phone checks

Physical checks only a real device can settle. **Nothing here is ticked by the
session — the checkbox is the only ground truth.** Everything below was proven
in a headless browser; what a headless browser cannot tell you is whether it
reads well in a lit classroom, on a real projector, under your thumb.

Live at `https://madebymatt.uk/Lessons/liveteach/` once the Pages build for
`main` has finished. (I could not fetch the served bytes from this container —
its proxy refuses that host — so **the first check is that the page is there at
all**.)

---

## 1 · It is live (do this first)

- [ ] `https://madebymatt.uk/Lessons/liveteach/` opens on the phone.
- [ ] The **Made by Matt** splash appears and clears.
- [ ] Both launch buttons open something: **📽 Projector view**, **🧑‍🏫 Teacher HUD**.
- [ ] `← Lessons` at the top goes back to the catalogue.

## 2 · The HUD on your phone — the one you said you would check

Open **teacher.html** on the phone, portrait.

- [ ] Nothing overflows sideways. No horizontal scrolling, anywhere.
- [ ] Every button is comfortably thumb-sized.
- [ ] It says **"no projector heard yet"** — correct and honest, because the
      projector is not in this browser on this device.
- [ ] Paste a class list of ~10 names into **Cold call** and press **Load class
      list**. The rows are readable: name, "here"/"away", a percentage.
- [ ] **The name column is not squeezed to two characters.** This was a real
      defect found in review; it is the thing most worth your eyes.
- [ ] Press 🎲 **Pick** a dozen times. No name comes up twice in a row.
- [ ] Mark someone **away**: the row says "away", shows 0%, and stops coming up.
- [ ] Press **Load** again after typing nothing — it should tell you to type a
      name, not do something odd.
- [ ] Close the tab, reopen it. **The class list is gone.** (This is the whole
      safeguarding promise — please check it yourself.)

## 3 · The projector view on the classroom PC

Open **projector.html** on the PC driving the projector, fullscreen (⛶ or F11).

- [ ] From the back of the room, the stage banner is readable.
- [ ] **☀ High lumen** — the whole page goes light. On your actual projector,
      is this the more readable of the two? (It exists for washed-out lamps.)
- [ ] **✖ Blackout** blacks the screen; **B**, **.** or **Esc** brings it back,
      and the way back is visible from the back of the room.
- [ ] **🖊 Draw**, scribble with the mouse or the board pen, **C** clears it.
- [ ] **🔔 Bell** — a slow amber glow, not a strobe. Watch it with a pupil in
      mind: is it calm enough for your room?
- [ ] **🎲 Cold call** on this window shows the whole list on the class screen
      while the panel is open. Decide whether that is acceptable in your room,
      or whether you will only ever use the picker from the HUD.

## 4 · The clicker

Plug the USB clicker into the classroom PC.

- [ ] Forward / back move the lesson stages.
- [ ] They keep working after you click on the *other* window.
- [ ] Whatever the clicker's third button sends, it does not do anything
      alarming. (If it reloads the page, tell me what it sends.)

## 5 · The worksheet — the one to check on paper

On a **wave** stage, press **🖨 Worksheet** and save as PDF, then print one.

- [ ] The wave figure has a **grid** and a bar marked **1 metre**.
- [ ] Measure one wavelength off the printed grid. **Do you get 2 m on stage 2?**
- [ ] Measure the height from the middle line to a crest on the "Bigger wave"
      stage. **Do you get 1 m?** (A clipped trough here was a real defect; the
      fix is proven in a headless render, but paper is the real test.)
- [ ] The answer lines are actually there, and wide enough to write on.
- [ ] There is a **blank space** for a name — not a printed one.
- [ ] No `$` signs, no backslashes, no `\times`.
- [ ] Nothing else from the screen bleeds onto the page.

## 6 · The QR code

- [ ] Press **Q** on the projector, scan the code with the phone camera.
- [ ] It opens the lesson **at the same stage and speed**.
- [ ] Type a tag like `period 3` and scan again — the tag chip appears on the
      projector.
- [ ] The address under the code is selectable, and **contains no pupil name**.

## 7 · Sound and Calm

- [ ] Open the kit fresh. **Sound is off.** Turn it on, close the tab, reopen:
      **it is off again.** (Deliberate — an SEMH room should never be surprised
      by noise.)
- [ ] With sound on, press 7/8/9 — short, quiet ticks. Nothing repeats or rings.
- [ ] Turn on **🌙 Calm**. The bell becomes a still banner instead of a glow,
      and the simulation stops moving while everything stays readable.

## 8 · Anything that made you hesitate

- [ ] Write it here. Wording that reads oddly to a pupil, a control you went
      looking for and could not find, anything that felt slow.

---

**If a check fails**, the fastest useful report is: which page, which step,
what you expected, what happened, and the phone or PC you were on.
