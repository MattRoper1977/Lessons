# Phone checklist — game estate sitting, 6 August 2026

Physical checks only a real phone can settle. Everything below changed this
sitting (Lessons PRs #74–#77) or was measured and left for your eyes. Nothing
here is marked done by the session — **the checkbox is the only ground truth.**
(The audit pack's own template was not available; this is the equivalent,
written from what actually changed.)

## 1 · Slipstream — the big one (two fixes in one game)

Open `/Lessons/Games/Slipstream.html` on the phone.

- [ ] **Portrait**: drive around the arch lobby for ~20 seconds. The page must
      never scroll sideways or jiggle horizontally, however the camera swings.
- [ ] **Landscape**: same drive, same check.
- [ ] The floating arch labels (`▶ START RACE`, `MODE`, `SEED`…) still sit on
      their arches and follow them as you drive.
- [ ] **Interrupted-touch fix**: steer hard left with a finger held down, then
      swipe up to the home screen (or take a call) mid-steer, come back. The
      car must NOT still be steering left on its own.

## 2 · The seven offline games — aeroplane mode

Put the phone in **aeroplane mode with Wi-Fi off**, then open each and confirm
it reaches actual play (not just its menu):

- [ ] Trail Runner — START THE TREK runs
- [ ] Trekkers Trail Runner (Tees Coast) — START THE TREK runs
- [ ] Wrecking Crew — a shift starts, physics moves
- [ ] Slipstream GP — lobby renders in 3D, a race starts
      *(also check the BRAKE button and touch steering still feel exactly as
      they did — this file's patch set is protected and the edit was two lines)*
- [ ] Neon Snake Overdrive — the snake runs
- [ ] VoxelCraft — TAP TO PLAY loads a world (first build takes a few seconds)
- [ ] Voxel Frontier `/voxel/` and the games hub still behave (nothing changed
      there — control check)

## 3 · Fonts — fifteen games, thirty seconds

The decorative web fonts are gone; system fonts took over. Flick through any
three of: Globe Snake, Grid Chase, Marble, Neon Garden, Neon Siege, Orbital,
Prism, Slipstream, Static, Vortex, Trail Runner, Trekkers, Wrecking Crew.

- [ ] Titles and HUDs still look intentional (bold, spaced, readable) — not
      broken or overlapping. If one looks wrong on the phone, name it; the fix
      is per-file CSS, not a font restore.

## 4 · The three 2px overflows

- [ ] Trail Runner, Trekkers, Wrecking Crew, portrait: no sideways scroll on
      the start screens; Wrecking Crew's title entrance animation still looks
      right (it is now clipped to its container during the zoom).

## 5 · Named inputs (screen-reader spot check, optional but valuable)

With TalkBack/VoiceOver on, focus the seed box in any of Globe Snake / Orbital
/ Prism / Vortex:

- [ ] It announces a real description ("Seed number — enter a seed…"), not
      just "edit text".

## 6 · Nothing else moved — two spot controls

- [ ] Off-Brand and Charcoal open and play exactly as before (their dedicated
      gates ran green; your eyes are the second factor).
- [ ] The Games shelf at `/games/` still shows 41 cards with Echo Vault as the
      only NEW· holder (unchanged this sitting; control check).

## Known-open, not yours to check yet

Splash coverage patches and the three expansions (Glitch Clash league, Axiom
Shift Proofline, Lumins workshop) were parked with their census and constraints
recorded — they arrive as their own sittings with their own checklists.

---

## 7 · The ten new splashes (added 6 August, second sitting)

Each of these games now opens with the canonical Made by Matt splash. Open any
of them and check the splash itself, then **tap the "Skip intro" button**:

- [ ] Globe Snake — skip by touch, game underneath does nothing on that tap
- [ ] Neon Snake Overdrive — same
- [ ] Neon Siege — same
- [ ] Neon Garden — same
- [ ] Orbital — same
- [ ] Grid Chase — same
- [ ] Prism — same
- [ ] Slipstream — same
- [ ] Kids vs Staff: Showdown — same
- [ ] Trekkers Trail Runner (Tees Coast) — same

**The thing to watch for:** after the splash disappears you should land on the
game's normal start screen — one start screen, not two, and nothing should
already be moving. If a tap on "Skip intro" also does something in the game
(fires a shot, starts a run), that is the leak the gate is meant to prevent —
tell Claude which game.

- [ ] With **reduced motion on** in your phone's accessibility settings, open
      any two of them: the splash should appear fully-formed and hold still,
      then go. No fade-in, no drawing animation.

Unchanged and deliberately left alone: Trail Runner, Marble and Apex Golf keep
their own bespoke Made by Matt intros.

---

## Relicforge: Fracture Engine — madebymatt.uk/fracture/

New game, launched 6 August 2026. Everything below is a physical check no gate
in a container can do. **Nothing here is ticked for you.**

- [ ] **The splash, by touch.** Open `/fracture/` and **tap the screen while the
      MadeByMatt loading screen is still up.** It should go immediately, and
      you should land on the main menu — not in the game, and nothing should
      have been fired, started or selected by that tap. (The gate proves this
      with synthetic events; your thumb is the real test.)

- [ ] **Frame rate — the one number no gate here could measure.** The build
      container renders this game through software at about 3 fps, which says
      nothing about your phone. So: does it actually feel smooth in Ironwood
      Verge, and does it hold up in the Glitchworks with several enemies
      active? If it stutters, say which realm and which phone.

- [ ] **Touch controls under the thumb.** Joystick, attack, heavy, dodge, jump,
      interact and potion. Every one measures over 44px rendered — but are
      they where your thumb actually is, and can you dodge and attack at the
      same time without stretching?

- [ ] **The forge under the thumb.** Open the forge panel mid-run and temper
      something. Are the controls reachable one-handed?

- [ ] **Reduced motion, on the device.** Turn reduced motion on in your phone's
      accessibility settings, then open the game. Hit-stop should be gone
      entirely, the camera should not shake, and the splash should not fade.
      Then check the Settings panel: the reduced-motion switch should show as
      **disabled with a reason**, because your OS is holding the floor and the
      switch is not allowed to override it.

- [ ] **Both orientations.** Portrait and landscape, no horizontal scroll, no
      control pushed off-screen or under the notch.

- [ ] **Save and come back.** Play a few minutes, switch apps (the game should
      pause itself), come back, then close the tab entirely and reopen
      `/fracture/`. Continue Adventure should put you back in the same realm
      with the same level and the same relics.

- [ ] **The Chronicle on a phone.** Press Export Chronicle and open the file it
      downloads. It should be a readable standalone page on a phone screen —
      no blank fields, no "undefined", no "NaN".

- [ ] **Card art and the shelf.** On the arcade, does the Fracture Engine card
      read clearly at phone size, and is the new **Action RPG rail** (two
      cards: Fracture Engine and Strip the Machine) obviously a pair rather
      than one game listed twice?

- [ ] **The homepage box.** Fracture Engine now sits at the top of New
      Releases, above Neon Sync and Neon Breach. Neither of those was
      displaced — check all three are still there and the poster image loads.

- [ ] **The question no gate answers: is it fun?** Three realms, three classes.
      Does the hit-stop make combat feel weightier, or just sticky? Is the
      end-of-realm report a satisfying beat or an interruption?
