# GSA-FIX-1 — Decisions record

Pass: `gsa-fix-1-2026-08-18` · Branch: `claude/gsa-fix-1-drv4of`
Applies the findings of read-only passes GSA-1 (GROW) and BSA-1 (BUILD).
Written at the time, per the convention set by `_bsg1/DECISIONS.md`.

## Base and rollback

- **Base / rollback SHA**: `cc560092a618ec6ab63e89e2039746104c760317`
  (`origin/main` at pass start, 2026-08-18).
- **Landed**: `0e280783243fb9b4448ceeeffb082fcaab20038b`, fast-forward, no merge
  commit. Merge authorised explicitly by the owner in-session, overriding the
  session's branch-only rule for that one action.
- The local `main` ref arrived stale at `b7f3118`; `origin/main` was used
  throughout. A stale local `main` is another way a base check can lie.
- Branch note: the master prompt names `claude/gsa-fix-1`; the session's
  designated branch is `claude/gsa-fix-1-drv4of`. The designated branch is used
  (system instruction outranks the prompt's spelling).

## The two accepted exceptions

Both are deliberate departures from a standing rule, both owner-ruled, both
recorded here so they read as consistent rather than as drift.

### G2 — protected-string exception (owner ruling, 2026-08-18)

`SCI_G_W5B_Fair_Test_Do.html`, 2 occurrences (screen `wh-bridge` + print pack).

    - mean — the middle value of your repeats
    + mean — the total of the repeats divided by the number of repeats

The word bank defined the **mean** as the **median**. The lesson's own result
logic is `reduce((a,b)=>a+b,0)/3` — an arithmetic mean — so the protected string
contradicted the page it was protecting.

**Ruling**: word banks are protected against *drift*, not to preserve a wrong
definition. This is the only protected string this pass touched.

### G5 — reading-band exception (owner ruling, 2026-08-18)

`SCI_G_W7B_The_Moon_Do.html`, 4 occurrences (Supported "Next step up", Standard
`retr-ask`, the Standard panel's `data-speak-text`, and the print pack).

    - Week 6: what keeps the Moon travelling around Earth?
    + Week 6: what keeps the planets travelling around the Sun?

R2 was badged "Week 6" but asked a Moon question — *applying* W6's idea rather
than retrieving it. W6 taught planets orbiting the Sun and gravity's role.

The item carried a condition: keep Flesch-Kincaid at or below the surrounding
retrieval text. **The applied fix does not meet it** — FK rises 3.76 → 4.96 at
sentence level and 3.05 → 3.28 at panel level, against surrounding asks at
3.07 / 3.65 / 2.31. The condition is unsatisfiable for a correct fix: any true
W6 retrieval must contain the word "planets".

**Ruling**: a W6 retrieval that does not say "planets" is not a W6 retrieval.
Correctness wins over the FK condition. The GROW reading band remains
owner-held; when it is supplied, this line is the first thing to re-measure.

Retained deliberately: the Supported ask ("Point to the Sun in the model"), the
Stretch ask ("explain why an orbit needs motion and gravity acting together"),
and the lead-in paragraph on the Moon travelling around Earth — that one is the
bridge into today.

## Why some items changed more occurrences than the brief named

The brief anchored semantic sites. These lessons mirror the same sentence into
up to three places, and a half-applied fix is worse than none:

- **Screen → print pack.** Print parity is a gate; both copies always change.
- **Screen → `data-speak-text`.** The read-aloud text is a separate copy. A
  stale one makes the audio contradict the screen — an accessibility
  regression, not a cosmetic one. This is what took G5 from 2 to 4.
- **B1** = 6 question edits + 1 print-summary mirror + 1 slide note (below) = 8.

Anyone re-auditing these files should count occurrences, not sites.

## B1 — the note that had to move with the questions

`SCI_B_W3B_Backbone_Detectives_Do.html` carried

    Questions 2 and 3 draw on what you already know — weeks 1 and 2 were baseline.

That is true of **W3A** — where teaching starts and there is no previous lesson
to recall — and it was the stated justification for W3B's `What you know`
labelling. Once Q2/Q3 became W3A retrievals the note was false, so it became
`Questions 2 and 3 retrieve last lesson (W3A).`

The "W3 pair excepted" rule covers W3A only. W3A's own `What you know` framing
is correct and was left alone.

Q3 in Supported and Standard already retrieved W3A (the fish-picture backbone
from the W3A I Do); only their labels were wrong, so **only the labels changed**.
Rewriting sound text would have been churn against the print mirror.

Reading band, each rewritten question against its own panel's Q1:
Supported 1.87 vs 3.65 · Standard 6.01 vs 7.59 · Stretch 6.28 and 3.72 vs 15.56.

## `/hud.js` is not a gap — do not vendor it

Every lesson references `<script defer src="/hud.js">`, and `hud.js` is not in
this repo. Under `file://` — and in an isolated environment — that 404s, and it
will 404 in any local boot harness.

**It is not missing.** `hud.js` is served from the site repo at the origin root
(`madebymatt.uk/hud.js`); Lessons is a separate repo mounted under that origin,
so `/hud.js` resolves live. Owner ruling, 2026-08-18: **do not add, stub or
vendor it.** A boot harness should treat that 404 as expected, not as a red.

This is why the Chromium gate below is stated as *no new* errors rather than
zero errors: literal zero is unreachable locally, on this commit or its base.

## Gates

Measured against base `cc56009`; full method in the pass report.

| gate | result |
|---|---|
| anchors changed exactly N times, nowhere else | green — word-level diff shows only the listed strings |
| old strings gone repo-wide | green — 0 survivors |
| print parity (G2, G3, B2, and G5, B1) | green |
| `node --check` on inline JS | green — 22 blocks / 30 files, 0 failures |
| Chromium boot, 10 GROW + 10 BUILD + 2 matrices | green — 0 pages with new errors, 0 structural drift vs base |
| diff confined to listed strings | green — 8 files, +14 / −14 |
| no `hud.js` / back-link / splash / storage / network / `<form>` / branding change | green |
| structural markers (tiers, panels, speak hosts, print boxes, Lundy, witness, objectives) | green — 0 drift |
| food census, BUILD W5–W7 | green — identical |
| manifest parity (GROW, BUILD, **and LAUNCH**) | green — all three byte-identical, before and after landing |
| protected word-help parity | green — one drift, the named G2 exception |
| live raw-pin on the origin | **not run — network blocked** (`mattroper1977.github.io` 403 at the proxy). Owner pins the changed lines. |

Pre-existing red, not from this pass: the `FieldOps P2` workflow was already
failing on base `cc56009`.

## Still owner-held after this pass

- SoW W1–W2 planner tidy — `_passsg/inputs/` and the SoW workbooks untouched,
  as instructed.
- GROW reading band — not supplied; G5 is the open exception against it.
- LSA-1 fixes when its findings arrive. LAUNCH is untouched this pass.
