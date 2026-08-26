# Live-Teach Projector Kit

A projector view for the class, an optional teacher window for you, and one set
of keys that drives both. Nothing installs, nothing signs in, and no pupil data
ever leaves the machine.

**Open it at** `/Lessons/liveteach/` — that page launches both views and
explains which setup you are in.

---

## The one constraint that decides everything

The two windows talk over `BroadcastChannel`, which is **same browser, same
device, only**. Two windows on the classroom PC, or two tabs — fine. The
teacher HUD on your phone and the projector on the PC — **not** fine; they
cannot see each other, and the HUD will honestly say "no projector heard yet"
rather than pretending.

That is why the projector view is complete on its own. Every teaching action
is on it. The HUD is an extra pair of hands, never the only pair.

### One screen (or you are not sure)

Open the **projector view**. Move the mouse to wake the control strip at the
bottom; the keys below all work. A USB clicker plugged into the PC works too.

### Two screens (extended desktop)

1. Press **Windows key + P** on the classroom PC and choose **Extend**.
2. Open the projector view and drag it onto the projector screen.
3. Open the teacher HUD and keep it on your screen.
4. Click each window once so it has focus at least once.

Both windows must be in the **same browser on the same PC**.

---

## Keys

The same keys work in both windows, so the clicker keeps working whichever one
has focus.

| Key | What it does |
|---|---|
| **Space** | Pause / resume the simulation |
| **1 / 2 / 3** | Timer: 1, 3 or 5 minutes |
| **0** | Clear every overlay — hint, poll, timer, the cold-call name, the tally and the bell (the tally's **counts** survive; Reset tally is what throws those away) |
| **H** | Hint on / off |
| **P** | Show-of-hands poll |
| **PageUp / PageDown** | Previous / next lesson stage — this is what a USB clicker sends |
| **← / →** | Previous / next lesson stage |
| **B** or **.** | Blackout the projector (and back) |
| **D** | Draw on the screen &nbsp;·&nbsp; **C** clears the ink |
| **N** | Cold call: pick the next pupil &nbsp;·&nbsp; **M** passes the question on |
| **7 / 8 / 9** | Class-check tally: stuck / nearly / got it |
| **Q** | Share / QR — an address that reopens this lesson state |
| **Esc** | Close whatever is on top; blackout comes down first |

Two deliberate absences. **F5** does not reload a live lesson: it explains how
to go fullscreen instead. And the **silent bell has no key** — it is a button
only, so a held or fumbled key cannot flash the room.

---

## Pupil names: what the kit does and does not do

This is the part worth reading twice.

- **The class list lives in one browser tab's memory and nowhere else.** You
  paste it at the start of the lesson. It is never saved to the computer,
  never put in the web address or the QR code, never written to a file, and
  never logged. Closing the tab deletes it. You paste it again next lesson, on
  purpose.
- **The list never travels between the two windows.** The only thing that can
  reach the projector is a *single picked name*, and only when you press
  **Show on projector**. Draw again and that name is taken back down, so the
  class is never looking at a name you have moved on from.
- **On a one-screen setup the projector is the screen the class can see.** A
  name you pick there is shown to the room as you pick it — usually the point,
  but worth knowing before you open the panel in front of everyone. The panel
  says so itself.
- **The class-check tally counts responses and nothing else.** There is no
  record of who said what, so there is nothing to keep private.
- **The worksheet leaves a ruled space for a name rather than printing one**,
  and a name showing on the wall is not carried onto the page or into a PDF.
- The only thing this kit saves to the computer is **two display settings**
  (high-lumen and Calm), under one registered key.

### Cold call, and why it cannot ask twice

The pupil who has just been asked **cannot** come up on the very next pick.
Not rarely — the guarantee is built into how the weighting works, not bolted
on as a low probability. The only exception is a room with nobody else
available to ask, and when that happens the kit says so on screen instead of
quietly repeating. Everyone's odds are shown, so you can see the room is being
shared out; **Pass** bounces a question on without letting anyone escape the
queue.

---

## What each part is for

- **Stages** — a lesson is a small file under `liveteach/manifests/`. Each
  stage sets the simulation, a banner, labels and an optional spotlight. Open
  `?lesson=waves_v1` to pick one; a name the loader cannot use gets a visible
  error rather than a silent fallback.
- **Draw (telestrator)** — annotate anything on the screen. Ink is stored as
  vectors, so it survives a resize; the mini-pad on the HUD draws onto the
  projector at the same place.
- **Share / QR** — builds an address carrying the lesson, stage, speed,
  display and an optional tag. Five things, and nothing else: scan it with a
  phone or copy it. **Bookmark state** is the one action that adds a history
  entry, so the back button really does return there.
- **Class check** — 7/8/9 tallies how the room is doing, with a graph you can
  copy or download for a report.
- **Silent bell** — draws eyes with a slow amber glow instead of a noise, and
  becomes a still banner if reduced motion or Calm is on.
- **Sound** — off every time the kit opens, on purpose, and turning it on
  lasts for that session only.
- **Worksheet** — on a wave stage, prints the figure the class was looking at
  with its grid and scale bar intact, so pupils can measure straight off the
  page. The worked answer stays on your HUD, not on their sheet.

---

## Accessibility, briefly

Calm Mode and the operating system's reduced-motion setting are the authority:
they stop the distortion and the movement while keeping every label and every
cue. Colour is never the only signal — the tally rows carry a word, a shape and
a number; the exported graph uses dashes as well as hues. High-lumen swaps the
whole page to a light palette for a washed-out projector. Every control is at
least 44 px, keyboard-reachable, and keeps its focus ring.

---

## If something is wrong

- **"No projector heard yet"** — the two windows are not in the same browser
  on the same PC, or the projector window is closed. That message is honest;
  it does not mean the kit is broken.
- **Fullscreen refused** — a managed school Chrome can forbid it. Press **F11**.
- **Copying blocked** — school machines often block clipboard writes. The kit
  downloads the file instead and tells you that is what happened.
- **A lesson will not load** — the address bar's `?lesson=` name is wrong. The
  error on screen names the value it rejected. Timers, hint and poll keep
  working; only the stages are off.

---

## For whoever maintains this

Everything is in two self-contained files (`projector.html`, `teacher.html`)
plus a launcher — no build step, no CDN, openable from `file://`. Shared code
(the bus and keyboard core, the Made by Matt splash, the QR encoder, the picker
engine) is authored once under `tools/liveteach/` and **stamped byte-identically**
into the views; edit the source and run its stamper, never a stamped copy. The
drift gates go red otherwise.

```sh
tools/liveteach/run.sh        # 26 steps: stampers, static gates, units,
                              # the QR decode gate, the 10k picker simulation,
                              # and seven headless-browser suites
```

Every gate has a **negative control** — a proof it can fail. That is the
house rule that matters most here: several checks in this kit passed for the
wrong reason until their red control was written, and each one is documented in
`LIVETEACH_LEDGER.md` alongside the phase that found it.
