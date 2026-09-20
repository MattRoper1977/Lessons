# RENDERED ACCEPTANCE — 390x844, Chromium
ORDER HUM-T · stage B · STOP-T2

Every figure below was produced by `tools/hum/render_proof.cjs` driving the decks' 
own controls. Chassis contract standing rule 5: a static parse cannot emit PASS for
a behavioural row, and a rendered count is not enough either — the control is driven.

| row | what it proves | result |
|---|---|---|
| 38 | audience is refused before voice | **519 / 519 panels** |
| 39 | influence is refused before audience | **519 / 519 panels** |
| 40 | driven in order, the panel reaches INFLUENCE | **519 / 519 panels** |
| 41 | every panel is reachable by the deck's own navigation | **519 / 519**, 73 / 73 decks |
| 42 | no panel control is double-driven by the deck's own handler | **0 double-driven** |
| — | page errors while driving every panel | **0** |

## Row 43 red-proof — the guard removed on one deck

The order requires the refusal behaviour to be proved by breaking it. The two order
guards were removed from the injected script on one deck and nothing else changed
(61,999 -> 61,817 bytes). The same harness was run on both.

| deck | rows 38 / 39 / 40 |
|---|---|
| GROW W4 RE, shipped bytes | **7 / 7 / 7** |
| GROW W4 RE, guards removed | **0 / 0 / 0** |

The battery detects the guard's absence on every panel, so a green row 43 means the
sequence is enforced and not merely present.

## Accessibility, measured like for like

The first comparison I ran was invalid twice over: it compared violation *rules* with
violation *nodes*, and it sampled the baseline at page load against the transplant at
the last stage. These decks also carry entrance animations, so repeat runs disagreed.
The figures below disable animation, use a fixed settle and compare the same state,
node by node. **Instrument correction #15.**

| measure | before | after |
|---|---|---|
| serious + critical nodes, 73 decks | 191 | 148 |
| violations **introduced** by the transplant | — | **0** |
| violations removed by the transplant | — | **43** (scrollable-region-focusable 43) |

The transplant introduces nothing and removes 43. The 148 that remain are the decks' 
own palette and were there before this order; the acceptance line "axe 0 serious" is
not reachable from a baseline of 191 without a separate colour decision, so it is
reported rather than claimed.

## What a pupil can do that they could not before

On 607 stages the pupil surface carried a four-word banner and no way to act on it.
It now carries, on every stage that invites a response, a response point naming that
stage's own task, an adult-receives control, and an influence branch — and the panel
refuses to record Audience before Voice, or Influence before Audience.