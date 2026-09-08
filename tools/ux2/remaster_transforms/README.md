# UX2 lane E — remaster transform patches

Provenance for the nine `Games/*.html` remasters landed on this branch.

## What was landed

Each game is **Lessons main's own `Games/<file>`** (education canonical host retained,
main's newer bytes retained) with the collection's transform applied to it:

    <engine> upgrades/<slug>/transform.{py,cjs} <main copy of Games/<file>> <output>

from the *Made by Matt Ten Remaster Collection* (`Made_by_Matt_Ten_Remaster_Collection/`,
"Afterlight III", 2026-09-08). The collection's own `source/<slug>/index.html` was **not**
shipped: it was cut from Play-served downloads (Play canonical host) rather than from this
repository. Its offline review builds (`games/*.html`), launcher and embedded three.js
copies were not shipped either.

| slug | chapter | landed file | transform | main sha256 | landed sha256 | Δ lines vs R/source |
|---|---|---|---|---|---|---|
| axiom-shift | The Broken Proof | `Games/Axiom_Shift.html` | transform.py | 2390d7dd6a4c… | 563c1df39eb3… | 6 |
| hold-the-mark | The Last Impression | `Games/Hold_the_Mark.html` | transform.cjs | d25e430a2ea3… | eaedd9a82de8… | 2 |
| globe-snake | The Last Constellation | `Games/Globe_Snake (1).html` | transform.py | f91419bee6db… | 80f14f7b73c6… | 2 |
| neon-snake | Blackout Circuit | `Games/Neon_Snake_Overdrive.html` | transform.py | a34bc5f6d277… | 9f2c83cc3548… | 2 |
| neon-siege | Blackout Protocol | `Games/Neon_Siege.html` | transform.cjs | 89cc313a110e… | fb23ab0492ca… | 2 |
| slipstream | Relay Run | `Games/Slipstream.html` | transform.py | 94265389e6d2… | 05fb65b6fcc9… | 2 |
| slipstream-gp | Heatline Protocol | `Games/Slipstream_GP.html` | transform.py | 204bd02d9b88… | e8051e0c4616… | 2 |
| one-guy | The Last Signal | `Games/OneGuy.html` | transform.py | 9d3a3164cb19… | c10d54075f6c… | 2 |
| trekkers | Coastguard Relay | `Games/Trekkers_Trail_Runner_Tees_Coast.html` | transform.py | 0f8e5a758b43… | 497a5dbcacd4… | 4 |

"Δ lines vs R/source" is the unified-diff line count between the landed file and the
collection's `source/<slug>/index.html`: the `<link rel="canonical">` host line (2 lines,
every game) plus the patched lines below. Nothing else differs.

## The three patches in this directory

Applied with `patch -p1` from the collection root before running the transform. They are
the whole of the session's edits to the collection.

* `neon-snake.patch` — `transform.py:10` asserted on the **Play** canonical line to fix a
  `">>"` typo, so the transform could not run on this repository's file at all
  (`AssertionError: (0, '<link rel="canonical" href="https://madebymatt-play.uk/…">>')`).
  Re-anchored on the education canonical; the typo is still fixed.
* `axiom-shift.patch` — the new `proofDown` pointer handler called `e.stopPropagation()`
  and dereferenced `e.currentTarget` unconditionally. The repository's PR gate
  `tools/verify_axiomshift.js` (line 71, `dispatch`) drives that handler with a stub event
  carrying only `preventDefault`, so the collection's build failed the gate with
  `TypeError: e.stopPropagation is not a function`. Both members are now guarded. The
  harness is unchanged; `tools/verify_axiomshift.sh` is ALL GREEN on the landed file.
* `trekkers.patch` — `transform.py:11` set `TREKKERS_URL` to an absolute Play URL under
  `/Lessons/Games/`, where the evidence page does not exist on either domain. The page lives
  only on the education host at `/Lessons/5_6 Local Choice/Trekkers_AQA_Evidence_L1.html`,
  so the constant is that absolute education URL. It is only ever assigned to an `<a href>`
  (`#trek-evidence-link`); nothing fetches it. Note for the Play publisher: its literal
  host rewrite (`domain-split/build_publications.py`, `source_origin → games_origin`) will
  turn this into a Play-host URL in the published copy, which 404s there exactly as the
  original relative link did.

## Reproducing

    cp -r <collection>/upgrades work/ && cd work
    patch -p1 < tools/ux2/remaster_transforms/neon-snake.patch     # and the other two
    python3 upgrades/neon-snake/transform.py Games/Neon_Snake_Overdrive.html out.html

`out.html` is byte-identical to the landed file at the "nine remasters rebuilt from main"
commit (before the separate GS1 `<h1>` demotion commit that follows it).
