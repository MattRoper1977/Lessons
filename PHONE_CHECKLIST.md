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
