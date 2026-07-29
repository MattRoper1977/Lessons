# Pass SCI — Clip register

**Purpose.** One row per lesson: whether it wants a clip, what the clip must show, what it must
**not** stray into, a candidate where one exists, and an honest verification status. Prepared so
wiring is a one-line change — the renderer supports a per-lesson `clip=dict(source,label,url,note)`
field; adding it to a lesson spec renders the labelled link in the I Do slide.

**Verification reality (SCI-2 §4).** The session fetch tool gets **HTTP 403** from every ad-free
source — Oak (`thenational.academy`), NASA (`spaceplace.nasa.gov`), and BBC is blocked outright.
So candidate URLs below come from the public **search index**, not a confirmed fetch: the lesson
exists, but the video player, its **captions**, **duration** and **embeddability** are **unverified**.
Per §4 nothing is wired that could not be verified. Matt clears the register in one sitting with his
30-second check (paste URL → loads? → scrub to 0:20 → demo started? → protected vocabulary? → then
ads/captions/embed). **Every lesson teaches fully without a clip; an empty slot is honest.**

**Standing constraints for any clip (§5):** beside the teaching in I Do, never replacing it; ad-free
first (Oak, BBC Teach/Bitesize, RSC, ESA/NASA/JPL); YouTube labelled as YouTube; iframe on the site
**and** a plain labelled link offline; never on a print surface; no autoplay; captions on; no
jump-scares or audio spikes.

Status key: **WIRED** (verified by Matt, live) · **CANDIDATE** (URL found, unverified — needs Matt's
check) · **SEARCH** (source named, no confirmed URL yet) · **EMPTY BY DESIGN** (no clip — reason given).

---

## LAUNCH (GCSE Biology 1BI0 Foundation)

| Lesson | Slot | Must SHOW | Must NOT stray into | Candidate | Status |
|---|---|---|---|---|---|
| W3·L1 Microscopy | I Do 1 | Setting up a light microscope; eyepiece×objective; focusing a real specimen | "bigger is always better" (ignoring resolution); no cell-biology beyond Topic 1 | Oak KS3 Science — *Observing cells with a light microscope* (`/teachers/programmes/science-secondary-ks3/units/cells/lessons/observing-cells-with-a-light-microscope`) | CANDIDATE |
| W3·L2 Magnification | I Do 1 | A worked magnification calculation, units matched | — | — | EMPTY BY DESIGN — a calc walkthrough is better modelled live; illuminator already carries the method |
| W3·L3 Exam skills | — | — | — | — | EMPTY BY DESIGN — exam technique, no demo |
| W4·L1 Diffusion | I Do 1 | Particles diffusing high→low; net movement; rate factors | active transport (kept for W6); no "energy needed" for diffusion | Oak KS4 Biology — *diffusion* (search: Oak "diffusion" KS4 Foundation) | SEARCH |
| W4·L2 Gas exchange | I Do 1 | Alveolus adaptations (surface area, thin wall, blood supply); gas exchange by diffusion | breathing ≠ respiration confusion; nothing on fitness/weight | Oak KS3 Science — *Adaptations of the human lungs for gas exchange* (`/pupils/lessons/adaptations-of-the-human-lungs-for-gas-exchange/video?share=true`) | CANDIDATE |
| W4·L3 Exam skills | — | — | — | — | EMPTY BY DESIGN — exam technique |
| W5·L1 Osmosis | I Do 1 | Water crossing a partially permeable membrane; dilute→concentrated | "sugar is bad" / any diet framing — sugar is only the solute | Oak KS4 Biology — *osmosis* intro (search: Oak "osmosis" KS4 Foundation) | SEARCH |
| **W5·L2 Osmosis core practical** | **I Do 1** | The potato-cylinders-in-sugar-solution practical set-up | calorie/weight/restriction language; unsafe glassware without narration | **Oak Foundation Edexcel — osmosis & sugar concentration on plant tissue: practical** | **WIRED** (Matt verified) |
| W5·L3 Analyse/evaluate | — | — | — | — | EMPTY BY DESIGN — data-analysis skills, no demo |
| W6·L1 Active transport | I Do 1 | Movement against the gradient; carrier proteins; mitochondria/energy | "just fast diffusion"; energy = "hard work" not "against the gradient" | Oak KS4 Biology — *active transport* (search: Oak "active transport" KS4 Foundation) | SEARCH |
| W6·L2 Root & gut | I Do 1 | Root hair cell; mineral/glucose uptake against the gradient | roots "sucking like a straw" | Oak — *Observing root hair cells using a light microscope: practical* (`/pupils/lessons/observing-root-hair-cells-using-a-light-microscope-practical/video`) | CANDIDATE |
| W6·L3 Compare | — | — | — | — | EMPTY BY DESIGN — exam technique |
| W7·L1 Round-up | — | — | — | — | EMPTY BY DESIGN — retrieval/consolidation |
| W7·L2 Command words | — | — | — | — | EMPTY BY DESIGN — exam technique |
| W7·L3 Exam practice | — | — | — | — | EMPTY BY DESIGN — independent exam practice |

## GROW (White Rose Y5/6 · ELC 8939)

| Lesson | Slot | Must SHOW | Must NOT stray into | Candidate | Status |
|---|---|---|---|---|---|
| W3 Friction | I Do 1 | Friction between surfaces; helpful vs unhelpful; a fair-ish surface comparison | "friction is bad"; no formulae/coefficients (beyond tier) | Oak/BBC Teach — *friction* KS3 (SEARCH) | SEARCH |
| W4 Levers/pulleys/gears | I Do 1 | A lever/pulley/gear trading force for distance | "free force" / perpetual motion | Oak/BBC Teach — *simple machines / levers* (SEARCH) | SEARCH |
| W5 Fair test | — | — | — | — | EMPTY BY DESIGN — working-scientifically skills; modelled live |
| W6 Earth & planets | I Do 1 | The 8 planets orbiting the Sun; rocky vs giant; gravity holding orbits | astrology; scale exaggeration; no "space has no gravity" | NASA/ESA — solar system order (`science.nasa.gov` / `esa.int`) | CANDIDATE (NASA, 403 — needs check) |
| W7 The Moon | I Do 1 | Half the Moon always lit; phases from viewing angle as it orbits | phases ≠ Earth's shadow (that's an eclipse); Moon making its own light | NASA — *Our World: Moon Phases* (`science.nasa.gov/eclips/videos/moon-phases/`) / STEMonstrations | CANDIDATE (NASA, 403 — needs check) |

## BUILD (White Rose Y3 · ELC 8939)

| Lesson | Slot | Must SHOW | Must NOT stray into | Candidate | Status |
|---|---|---|---|---|---|
| W3 Backbones | I Do 1 | Vertebrates vs invertebrates; the line of backbone; hard case outside | "big = backbone"; nothing gory/dissection | BBC Bitesize / Oak KS3 — *classification / vertebrates* (SEARCH) | SEARCH |
| W4 Muscle pairs | I Do 1 | Antagonistic muscle pair; biceps contracts / triceps relaxes | muscles "pushing"; nothing on the pupils' own bodies | BBC Bitesize — *antagonistic muscles* (SEARCH) | SEARCH |
| W5 What a body needs | — | — | — | — | **EMPTY BY DESIGN — food/nutrition. High caution: most clips carry "healthy/unhealthy" or restriction framing (§5 forbids calorie/weight/restriction language at any tier). Only an Eatwell "everyday/sometimes" clip with zero restriction language would qualify; none confirmed. Teach on the job-cards.** |
| W6 Balanced plate | — | — | — | — | **EMPTY BY DESIGN — same food-caution as W5. The Eatwell plate is taught on the model, not a clip, to avoid diet framing.** |
| W7 Food chain | I Do 1 | Producer→consumer; the arrow = "is eaten by" | predator gore/photographs (drawings only); no scary audio | BBC Bitesize — *food chains* KS2/3 (SEARCH) | SEARCH |

---

## Summary
- **WIRED: 1** (osmosis core practical — Matt-verified, live).
- **CANDIDATE (URL found, unverified — session fetch 403): 4** (microscopy, gas exchange, root-hair,
  and the two NASA space lessons).
- **SEARCH (source named, no confirmed URL): 6** (diffusion, osmosis intro, active transport,
  friction, mechanisms, backbones, muscles, food chain).
- **EMPTY BY DESIGN: the rest** — exam-technique/skills/retrieval lessons (no demo to show), plus
  BUILD W5 & W6 held empty on the food-safety rule.

Nothing here is wired that could not be verified. Slots are prepared; Matt's check turns a CANDIDATE
into a one-line `clip=` addition.
