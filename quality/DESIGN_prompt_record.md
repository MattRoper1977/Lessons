# DESIGN — the prompt record

**STATUS: PROPOSED — approved in principle by Matt 2026-08-04, build gated on the
triggers below. Derive the sentinel populations at build time; the 50/98 in this
document were true at `6aaffb7` only.**

*Pass SEMH-1 §8. Accepted as written (Matt, 2026-08-04). Two sentences survive every
future edit verbatim: the `SC`-is-not-on-the-ladder briefing point, and the withdrawal
clause — if a spreadsheet appears with these codes as columns, the design has failed and
should be withdrawn.*

**Build triggers, all three required:** (a) the LL-I specimen judged; (b) the TA card
briefing having actually happened — not merely landed at `9af1e63`; (c) one specimen per
pathway, chosen to break the design, before any batch.

**Pre-authorised fallback, no fresh ruling needed:** if the specimen shows *Most help*
filled and *Try without next time* blank, cut to the two fields — *Try without next time*
and *Keep (access)*.

Queue position: **after entry 12.** It waits on LL-I, not beside it.

---

## 0. What already exists, measured — not remembered

The audit proposed a "least-prompt-first evidence strip" and an independence scale. Both
overlap an architecture that already shipped. **Derived at `6aaffb7`, not quoted:**

| sentinel | derivation | recorded | **derived at HEAD** |
|---|---|---|---|
| LL-G modality strip `ll-g:loop-mark v1` | `git grep -l "ll-g:loop-mark v1" -- '*.html'` | 45 | **50** — all BUILD, 0 elsewhere |
| written closure line *"What I said, and what it changed"* | `git grep -l` on the phrase | 48 | **98** — all GROW/LAUNCH, 0 elsewhere |

**Both recorded counts are stale.** The architecture is intact and correctly distributed
— every loop-mark file is BUILD, every closure-line file is GROW/LAUNCH — but the numbers
describing it have not been re-derived since their populations grew. This is the estate's
own registered defect class ("a number in prose can be stale; a number a script prints
cannot"), and this is its fifth sighting. **Anything built from this design must derive
these counts at build time, not copy them from here.**

## 1. What binds this design

- **Paper is primary**, not a fallback. **No pupil words persist on the device.**
- **The ring/mark is never counted or aggregated.** "Watch for the first spreadsheet" is
  a named register check. This design must not become the spreadsheet.
- **The adult is a witness and a next-step-giver — never a signatory, never a receipt-mark.**
- **A wrong prediction is never coded as failure.**
- **R-A09: no second copy, ever.**
- The strip must remain **byte-identical in print-feedback**.
- The day-close design is in flight under **LL-I/B2–B3** with a **September real-room
  observation gate**. This design must not pre-empt it.

## 2. The gap worth closing

The existing strip and closure line capture **what the pupil did and what changed**. The
audit is right that one thing is missing, and it is the thing that makes support fade:

> Nothing records **how much help it took**, or **what should be removed next time**.

A TA who supported heavily and a TA who waited both leave the same mark. The next adult
cannot tell, so the same scaffold is offered again by default. That is the actual
mechanism by which "Supported" becomes permanent — not attitude, not expectation, just
missing information at handover.

## 3. The design — one line, adult-side, on the paper that already exists

**Add nothing to the pupil's surface.** The strip and the closure line are the pupil's.
This design adds a **single adult-side line** to the TA brief / print-feedback margin
that already accompanies them.

### 3a. BUILD — extends the LL-G strip (50 files)

Printed **beside**, never inside, *"Pupil response — my next step"*:

```
Adult note (not the pupil's):   Most help I gave: WT · SP · VC · GV · SV · MO · SC · DS
                                They decided: ______________________________
                                I did not decide: __________________________
                                Try without next time: _____________________
                                Keep (access): _____________________________
```

Five fields, all adult-written, all optional, no box for a mark or a score.

### 3b. GROW / LAUNCH — companion to the written closure line (98 files)

The pupil writes *"What I said, and what it changed"*. The adult writes one sentence
underneath:

```
Adult note:  Most help: ____   ·   Try without next time: ____   ·   Keep (access): ____
```

Shorter deliberately. At GROW/LAUNCH the pupil's own line already carries the decision;
duplicating "they decided" here would be the second copy R-A09 forbids.

### 3c. Why "I did not decide" is on the BUILD form only

It is the field that does the real work, and it is the one an adult finds hardest. At
BUILD the risk of adult authorship is highest and the pupil's own written account is
thinnest, so the adult states the boundary explicitly. At GROW/LAUNCH the pupil's line
supplies it.

## 4. The prompt ladder, as the adult meets it

`WT` wait time · `SP` self-prompt/reference · `VC` visual cue · `GV` general verbal ·
`SV` specific verbal · `MO` model revisited · `SC` scribe/access only · `DS` direct
solution.

**`SC` is not on the ladder in the same sense as the others.** Scribing is an access
arrangement, not help with the thinking. It is ringed in the *"Keep (access)"* field, not
the *"Most help"* field. Conflating them is how a reasonable adjustment gets withdrawn in
the name of independence. **This is the single most important thing to brief.**

`DS` is not a failure state either. Sometimes the right call is to supply the step and
move on. It is recorded so the *next* adult knows where to start, not to grade the last one.

## 5. What this must NOT become

- **Not a register.** No name column. No class list. No per-pupil row that outlives the sheet.
- **Not a score.** The codes have no order-as-value. `DS` today and `WT` tomorrow is not
  "improvement of 7"; it may be a harder task.
- **Not aggregated.** No totals, no percentages, no "% of pupils at SV or below". If a
  spreadsheet appears with these codes as columns, this design has failed and should be
  withdrawn.
- **Not a second copy of the loop.** It records the *support*, never the learning. The
  loop-mark and the closure line remain the only record of what the pupil did.
- **Not a signature.** No initials box, no date-and-sign line. The adult is a witness.
- **Not on the device.** Paper only. Nothing typed, nothing saved, nothing synced.

## 6. Interaction with the LL-I day-close design

They operate at different grain and must not merge:

| | LL-I day-close (B2/B3) | this prompt record |
|---|---|---|
| grain | the day | the single lesson |
| author | the pupil (re-read) | the adult |
| subject | what the pupil said and what changed | how much help it took |
| status | ratified, awaiting a September real-room observation | proposed, unbuilt |

**The dependency runs one way: this waits on that.** The day-close is the pupil-facing
mechanism and must be observed working in a real room first. Adding an adult-side field
before the pupil-side close is proven would repeat the failure LL-G named — a TA who
meets the record before they meet the behaviour fills it in on the pupil's behalf.

**Concretely: do not build this until the LL-I specimen has been judged.** It is queue
position *after* entry 12.

## 7. What would have to be true to build it

1. Matt reads and approves the five fields and the two variants.
2. The **TA card lands first** (queue entry 10 — landed at `9af1e63`, but the briefing
   itself has not happened). The card is the behaviour; the line is only the trace.
3. The LL-I specimen is judged (queue entry 12).
4. One specimen file per pathway, chosen to **break** the design, gated before any batch.
5. Sentinel counts **re-derived at build time** — not the 50/98 in this document.

## 8. The honest risk

The most likely failure is not that adults refuse it. It is that they fill in **"Most
help"** and leave **"Try without next time"** blank — recording the past and skipping the
future, which is the only field that fades anything.

If the specimen shows that pattern, **cut the form to two fields**: *"Try without next
time"* and *"Keep (access)"*. Those two alone would close the audit's gap. The other
three are useful, not essential, and a form that is 60% blank teaches staff the whole
thing is optional.

**A blank field is not a failure to record. It is a record that nothing needed removing.**
That must be said in the briefing, or blanks will be read as non-compliance and the
spreadsheet will follow.
