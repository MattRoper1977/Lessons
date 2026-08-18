# PHONE SWEEP — four routes, tap by tap

Three of the four are live now. **Town Life is not deployed** — Part B stopped at a keyboard
trap, so `/townlife/` will 404. Its row is kept below so the sweep is complete once B lands,
but do not tap it yet.

---

## 1. `madebymatt.uk/townlife/` — NOT LIVE YET ⛔

Skip. Part B is unmerged pending a Town Life build whose welcome dialog releases keyboard
focus to the exit control. When it lands, the checks are:

- boots to the welcome screen, then **Enter Town**;
- the district panel names **Northstar Exchange** (the Washworks rename from Part A);
- claim a plot or change one thing, reload the page — the change is still there;
- a **Back: Arcade** control sits bottom-left, at least 44 px, and returns you to `/games/`;
- **the one that stopped B**: from the welcome screen, press Tab repeatedly — you must be
  able to reach that Back control. Today focus cycles between the name field, Enter Town and
  Controls forever.

## 2. `madebymatt.uk/Games/afterdark/` — LIVE (unlisted; type the URL) ✅

- Made by Matt splash, then the START card. **No "launch through the included local server"
  message may appear at any point** — that was the CDN dependency, now vendored.
- Tap once anywhere → audio unlocks. On a phone expect a "best played with keyboard + mouse"
  notice and LITE quality defaults.
- **Settings → Touch controls → On**, then start a match: left thumb is a move stick, right
  side is look-drag; FIRE / JUMP / SLIDE / USE / RELOAD / BUILD and the weapon slots are
  visible; COMBAT and BUILD swap the HUD.
- **Report the fps chip after about 60 seconds of play.** That number decides whether touch
  comes out from behind the Settings override — the software-render harness measured 6.3 fps
  against a 30 fps floor, which is an honest red from a machine with no GPU, not a verdict on
  a real phone.
- Background the tab and return, and rotate the phone: no stuck movement, and the match
  pauses and resumes rather than dying.

## 3. LundyLoop — `madebymatt.uk/Matt-s-Apps-/LundyLoop_Professional_OS.html` — LIVE ✅

- Open **Settings → Replace with demonstration data** so nothing real is involved.
- Tap the 🧒 **Pupil mode** button, confirm **Turn pupil mode on**.
- Expect: only **Pupil Capture** reachable — dashboard, triage, decision, return, audit and
  settings all gone; the Shield stays; a "Pupil mode · this device shows Pupil Capture only"
  bar with **Hold to return to staff view**.
- **Press and hold that button for about 1.5 seconds** — it should take you back to staff
  view, and a quick tap should not.
- Finish with **Settings → Delete all local cases and audio** to clear the demo data.

## 4. Maker Lab — `madebymatt.uk/Matt-s-Apps-/Teesside_Maker_Lab_PRO/STUDIO_SHELL.html?app=1` — LIVE ✅

- The Shadow Rig studio loads inside the shell. Type anything into a field.
- **The autosave chip must read "saved HH:MM"** — never "browser storage unavailable". That
  one string is the reason v2.1 exists.
- Then open
  `madebymatt.uk/Matt-s-Apps-/Teesside_Maker_Lab_PRO/01_Anamorphic_Shadow_Rig_Studio_PRO_v2.html`
  directly, on the same phone: what you typed should still be there.
- Both of these already pass on the live origin from a runner (8/8), so this is confirmation
  on a real device rather than discovery.

---

## Chromebook — still owed, before first pupil use in September

Deferred by ruling, **not performed, and claimed nowhere**. Repeat routes 1 and 2 on a school
Chromebook before any class uses them: Town Life because the pupil homepage is pupil use, and
Afterdark because its fps on school hardware is the open question. Throttled proxies measured
5.17–7.11 fps at 6x on Town Life-class devices, which is why a real reading matters.
