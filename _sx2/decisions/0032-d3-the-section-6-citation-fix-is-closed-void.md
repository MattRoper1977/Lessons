## D3 — the §6 citation fix is CLOSED-VOID

**Status: CLOSED-VOID. There was never anything to ship.** Recorded here so nobody
rebuilds it off the ticket title.

FIN3 §6 carried forward two "unshipped citation fixes". They are the two
`youtube.com` occurrences in `V08_Belonging_Without_Assumptions` — one in the
`DATA` payload, one in the rendered staff aside.

Measured by rendering, with both controls in one invocation:

| | pupil-visible | in the staff aside |
|---|---|---|
| V08 as shipped | **`[]`** | all four third-party URLs |
| V08 with the same URL planted into pupil prose | **fires, exit 1** | — |

So the detector is correct, and the file is clean. The premise rested on **D24**,
which was withdrawn once the measurement was taken by rendering instead of by a
source regex: byte 24,225 is inside the staff aside and byte 35,793 is inside the
`DATA` payload, neither of which a pupil reads.

**No branch was ever opened**, because the work was never begun — the premise
failed the first time it was checked. There is nothing to delete. A search of the
remotes for a citation branch returns only `claude/hc3-s6-glitch-receiver`, which
is HC3's §6 and unrelated; it is named here so it is not mistaken for this one and
deleted by someone tidying up.

The lesson worth keeping is not about V08. It is that a source scan and a render
disagreed, the source scan was believed, and a ruling was issued on it. Every
pupil-visible text claim is a rendered census now.
