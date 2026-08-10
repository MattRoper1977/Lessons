# A7, second half — does each retrieval box answer its own Supported prompt?

> The retrieval box must answer that lesson's Supported arrival prompt by reading alone.
> Where a box falls short, **add the missing fact to the box** (retrieval content, not new
> teaching); never soften the prompt.

**32 lessons with a predecessor. 17 boxes correct as they stand, 15 extended.**
(The three W3 lessons are excluded: their box is the baseline statement and their prompts
are elicitation by design.)

## How this was judged, and why the first attempt was thrown away

A word-overlap heuristic flagged 27 of 32 as short. It is a bad instrument: it cannot tell
a recall question from a point-at-the-object task, and it cannot tell a missing *retrieval*
fact from one that would **pre-teach today's concept** — which arrival explicitly forbids.

So each lesson was judged by an agent that read the lesson AND its predecessor, then
adversarially verified by a second agent testing two failure modes: not-actually-taught-in-
the-predecessor, and would-pre-teach. **All fifteen additions were confirmed as genuine
retrieval; five were tightened by the verifier, and the tightened wording is what shipped.**

A first run of this audit was **discarded**: the prompts had been hand-transcribed into the
agents' brief and 25 of 32 were wrong (BUILD W3B is about a robin, not "fish or crab";
BUILD W4A was reversed). The re-run carries no lesson text at all — every agent extracts the
box and the prompt from the file itself.

## The fifteen extended

| lesson | Supported prompt | fact added to the box |
|---|---|---|
| BUILD W4B | Point to the band that contracts when the model bends. | When the arm bends, the biceps (the top band) contracts and the triceps relaxes. |
| BUILD W5A | From last lesson: point to the part of the model that pulled. | In the model the bands stood for the muscles: pulling a band bent or straightened the arm, and neither band ever pushed. |
| BUILD W6A | Point to one food card and the job it helped with last lesson. | The jobs were energy, growth and repair, and keeping the body working. |
| GROW W3B | Point to the example with more friction: trainer sole on dry floor OR sock on smooth floor. | Rough, grippy surfaces make more friction than smooth ones. |
| GROW W6B | Put Earth, Mars and Jupiter in order from the Sun. | Order from the Sun: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune. |
| GROW W7A | From last lesson: what does Earth orbit — the Sun or the Moon? | Earth and the other planets orbit the Sun. |
| LAUNCH W5L2 | State what moves in osmosis. | Water moves from a dilute to a more concentrated solution. |
| LAUNCH W5L3 | What does +% mass change mean? | A positive % change means mass was gained. |
| LAUNCH W6L1 | Which process moves water only? | Osmosis moves water only, through a partially permeable membrane. |
| LAUNCH W3L2 | Complete total magnification = eyepiece × ___. | Total magnification = eyepiece × objective. |
| LAUNCH W3L3 | Complete magnification = image ÷ ___. | Magnification = image size ÷ actual size. |
| LAUNCH W4L2 | Complete oxygen diffuses from higher to lower ___. | Diffusion is the net movement of particles from higher to lower concentration. |
| LAUNCH W5L1 | Complete diffusion is high to ___. | Diffusion is the net movement of particles from higher to lower concentration, down a gradient, with no cell energy. |
| LAUNCH W6L3 | Which moves water only? | Osmosis: net movement of water only, from a dilute to a more concentrated solution, through a partially permeable membrane. |
| LAUNCH W7L3 | Choose process: water across partially permeable membrane. | Osmosis: water moves through a partially permeable membrane. |

The five the verifier tightened: BUILD W5A, LAUNCH W5L1, W6L1, W6L3, W7L3.

## The seventeen left alone, and why

| lesson | Supported prompt | reason |
|---|---|---|
| BUILD W3B | Point to BACKBONE or NO BACKBONE for a robin. | **elicitation — the fact would pre-teach today's concept** |
| BUILD W4A | Point to the bone on the model that a muscle could pull. | the prompt points at something in the room today |
| BUILD W5B | Match one card to ENERGY or GROWTH/REPAIR. | the prompt points at something in the room today |
| BUILD W6B | Place one example card into its group. | the prompt points at something in the room today |
| BUILD W7A | Point to an animal and a food source it could eat. | **elicitation — the fact would pre-teach today's concept** |
| BUILD W7B | Match rabbit → grass. | the box already carries the answer |
| GROW W4A | ◆ SupportedFrom last lesson, point to the force that opposed the trolley/block moving across a surface. | the box already carries the answer |
| GROW W4B | ◆ SupportedPoint to the pivot on the lever diagram. | the prompt points at something in the room today |
| GROW W5A | ◆ SupportedFrom the lever lesson, point or say: what did we deliberately change? | the box already carries the answer |
| GROW W7B | Point to where the Moon’s visible light comes from: Sun / Earth / Moon itself. | the box already carries the answer |
| GROW W5B | Point to the box that tells you what you will CHANGE in today’s plan. | the prompt points at something in the room today |
| GROW W6A | From last lesson, point or say one thing that made the force test fair. | the box already carries the answer |
| LAUNCH W6L2 | Complete active transport needs ___. | the box already carries the answer |
| LAUNCH W4L1 | Point to the side with higher concentration. | **elicitation — the fact would pre-teach today's concept** |
| LAUNCH W4L3 | Write high → low beside diffusion. | the box already carries the answer |
| LAUNCH W7L1 | Write magnification equation from reference. | the prompt points at something in the room today |
| LAUNCH W7L2 | Match DESCRIBE to what/why. | **elicitation — the fact would pre-teach today's concept** |

**Three would have been actively wrong to "fix"** — BUILD W3B, BUILD W7A and LAUNCH W4L1
are elicitations into the lesson's own new concept. Putting the answer in the retrieval box
would pre-teach, which every one of these lessons forbids on the same slide.

## Where the fact landed

Appended to the arrival retrieval box **and** to the retrieval line at the head of print
page 1 — a mid-year arrival is usually handed paper first, and the rule is "by reading
alone" either way. The original box text survives byte-for-byte as a prefix in all fifteen;
the gate asserts that, and that the only addition is one of the fifteen verified facts.
