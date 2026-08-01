# Instrument index — named future passes

Work this session identified but did not open. Each entry names the class, the
search pattern that would find it, and what a pass would have to prove. **Nothing
here has been audited.** An entry is a scope, not a finding.

Companion: `LundyLoop/tools/INSTRUMENTS.md` is the instrument register proper
(LL-INST-NN entries, with derivation and quarantine status). This file is the
*backlog* — classes of defect worth a pass, not instruments that exist.

---

## IDX-1 · Early returns that skip trailing work

**Filed 2026-08-01. Not audited.**

`if (!x) return;` at the top of a function whose *tail* does something unrelated to
`x` is a silent-skip generator: the guard is written for the head, and every later
addition to the function silently inherits it.

**This estate has been bitten by it once, measurably.** `grow-anim.js`'s `paint()`
opened with

```js
function paint(stage) {
  var st = stage._g, bar = $('.g-bar', stage); if (!st || !bar) return;
```

and a later pass appended `fit(stage);` to its tail. The guard exists because the
*bar-painting* code needs a bar; the *fitting* code does not. Result: every stage
carrying `data-grow-nobar` was never fitted — five stages across the five BUILD
decks, each left depending on an async `ResizeObserver` as its only backstop. That
is a visible reflow in the classroom and invisible to any synchronous check. It was
found only because two probes disagreed by 37px.

**Search pattern.** Functions whose first statement is a guard-return and whose body
is longer than the guard's concern:

```bash
# candidate sites: a guard-return in the first two lines of a function
rg -n --multiline --multiline-dotall \
  'function [a-zA-Z]+\([^)]*\) \{\n\s*(var [^\n]*)?\n?\s*if \([^)]*\) return;' \
  --glob '*.js' --glob '!node_modules'
```

Each hit needs reading, not counting: the question is whether anything after the
guard is independent of what the guard tests. A pass would have to (a) enumerate
every guard-return site in `grow-anim/`, `build-anim/` and `LundyLoop/tools/`,
(b) for each, state what the guard protects and what the tail does, and (c) prove
by a failing-then-passing test that no tail is unreachable for a live input class.

**Why it is worth a pass rather than a lint.** A lint would flag every guard-return
in the estate, which is most of them and nearly all correct. The defect is semantic
— *unrelated* tail work — and only reading separates the two.

---

## IDX-2 · Instruments not yet entered in the register

**Carried from the session brief. Not verified in this session.**

The brief names "27 instruments by register" as an outstanding backlog. That count
and its scope were **not re-derived here** — `LundyLoop/tools/INSTRUMENTS.md` holds
LL-INST-NN entries but was not enumerated against the tree in this pass. Recorded so
the item is not lost, explicitly marked unverified so the number is not inherited as
fact. See rule 3 in `reports/SESSION_CLOSE.md`.

---

## IDX-3 · Fill-mode enumeration, known incomplete

**Carried from the session brief. Not verified in this session.**

The brief names a fill-mode enumeration known to be incomplete. Neither the
enumeration nor the sense in which it is incomplete was checked here, and no file in
this repository matched a search for `fill-mode` outside CSS animation shorthand.
Recorded as a backlog with its provenance, not as a finding.
