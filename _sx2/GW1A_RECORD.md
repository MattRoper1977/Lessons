# GW1-A — the record that survives the session

Order GW1-A, 2026-09-10. §L two stale lines, §M the merge gate, §N the tenth
promotion. Everything below is measured today unless it says otherwise.

---

## §L1 — builder_ref stays where it is

The pin is `2e49afdd`. It is a **child** of `ee56d2c7`, carrying GC1's rows on
top. It does not move.

## §L2 — the stored trigger, amended at the trigger

Two lines in the SX2R §5 trigger were true when written at 00:55 and false by
the time it was due to fire at 15:31.

| stale line | what it said | what was true |
|---|---|---|
| builder_ref | *"advance `2a154e33` → `ee56d2c7`"* | the pin was already `2e49afdd`, a child of `ee56d2c7`; obeying the line moves it **backwards** and drops 163 admitted rows |
| GC1 P2–P6 | *"BLOCKED, the order text is not recorded in any repo, ask Matt to re-post it"* | recorded at `docs/orders/AMEND-3R-GC1.md`, merged in #490 |

**Both lines are now gone from the stored prompt itself**, not merely flagged in
a readback. The trigger `trig_01WsXeYVWaiHhsNYD3nq9T9b` was updated at 15:19 BST,
twelve minutes before its fire time. The builder_ref instruction now reads:

> builder_ref is re-derived at fire time from the current pin; never advanced
> from a stored value.

The GC1 line is deleted outright. The trigger also now opens with a note saying
it carries instructions and not measurements, so the next thing that reads it
knows which of its contents to trust.

The earlier trigger that carried the original text, `trig_01GJy58uhn2YbDm3HGHxakid`,
was a one-shot; it fired at 14:00 UTC and disabled itself, so it cannot fire the
stale text again.

**Why this is filed as a rule and not an incident** — see `REGISTER.md`,
*GW1-A N1*. I found the first stale line and flagged it. I found the second and
flagged that too. An unattended trigger cannot read a flag.

> A stale line in a stored trigger is corrected in the same turn it is found, or
> the trigger is disarmed until it is.

## §L3 — GC1 P2–P6 is not blocked

Verified against `origin/main` today, not remembered:

```
docs/orders/AMEND-3R-GC1.md   12,860 bytes
added in 83be7307  "B0: AMEND-3R-GC1, SECOND ISSUE, as a file instead of a chat message"  (#490)
```

P2–P6 have their order text and can proceed whenever they are scheduled. Nothing
needs re-posting. **Matt: this is the correction to what an earlier readback told
you.**

---

## §M — the merge gate

> **Neither BUILD nor GROW merges while any marking card's provenance line reads
> "asserted".**

The gate is live and currently **CLOSED**. Both cards carry:

> *"…so its stated hash `aa41d679…` is asserted, not verified."*

It opens when the Feedback & Marking Policy 2025/2026 (Issue 1, May 2026, Earwig
version) reaches the session and its sha256 is checked against
`aa41d67963846cf35e9bb6e53e708c7b46725c2d5cef432c2e1994a78e434e53`. Not before.

### §M3 — which text on each card is transcription-derived

Three provenances, and they are not the same strength:

| what | source | strength |
|---|---|---|
| the **eight codes and their expansions** — `VF`, `WS`, `I`, `NS + …`, `E`, `R`, `//`, `?` | ORDER GW1 §A3: Matt's own transcription of the policy's two columns | **transcription-derived.** RW1-B §J1 rules Matt's own written expansions a valid C2 source. The document itself was never in the session. |
| the **margin-edit line** — *"in the same colour, on the same page"* | same GW1 §A3 transcription | **transcription-derived**, same standing |
| the **R gate** — Voice (*point, sign, verbal response, demonstration, re-attempt, edit or authorised short clip*) and Audience (*an adult genuinely receives the response*) | `_sciv3/build/POLICY_ALIGNMENT.md`, hash-pinned at sha256 `9d16fb2c…` | **repository-verified.** Read from a file in the tree, hash checked. |
| the **five cause reads** | the removed "Lundy alongside learning" desk card's own three-column table | **authored pack content**, compressed one line each, not invented |
| the **policy hash** `aa41d679…` | GW1 §A1, given in the order | **asserted, not verified** — and the card says so |

Struck under GW1 §A2 as contaminated and now absent from both cards and the
generator: *"Yellow Box"*, *"green pen"*, *"pupil responds in their own colour"*,
*"EFL"*. Those were a reconstruction of mine that entered the record and was then
quoted back at me as the source. See `REGISTER.md` A6.

### §M4 — what §4.5's compression removed, measured

Measured today with `tools/rw1/a4_fit.cjs` under print emulation at A4 portrait,
794 × 1123 px at 96 CSS px/inch, `#print-area` vertical padding read from the
element (it is 0, so this is a zero-margin A4 — the honest worst case).

| print card | uncompressed | compressed (shipped) | change |
|---|---|---|---|
| W8A `print-marking` | **1185px — overflows by 62px** | **976px — fits by 147px** | −209px |
| W8B `print-marking` | **1163px — overflows by 40px** | **955px — fits by 168px** | −208px |

Both shipped cards clear a zero-margin A4 by more than a printer's own
unprintable margin (~10 mm top and bottom, ~76px together), so they fit on real
paper too.

**What came out, exactly.** Diffing the two card bodies shows one contiguous
differing span and nothing else — identical for 1457 leading and 1172 trailing
characters on W8A, 1396 and 1052 on W8B. The span is the *"Read the cause, not
the child"* block:

- **removed from print:** the five-row, three-column table — columns *Cause* /
  *What you see* / *Next teaching move*
- **put in its place:** one line naming the five causes — Secure · Mixed ·
  Misconception · Access barrier · Method or data

So the **cause labels survive**; the *"what you see"* and *"next teaching move"*
cells are the only content that leaves, and they leave **the print variant only**.
The on-page card keeps the full table: one A4 side is a print constraint, and
nothing is lost on screen.

**No policy content was touched.** Counted in both variants and equal in every
one: Codes 2/2, Margin edits 1/1, The R gate 1/1, Voice 3/3, Audience 3/3,
NS + … 2/2, Involvement moment 1/1. That is §4.5's sanctioned order of sacrifice
observed — the codes and the R gate are why the sheet exists, so they are the
last things that could go, and they did not go.

---

## §N — the tenth promotion

Filed in `REGISTER.md` as **GW1-A N1 — A stored trigger carries instructions,
not measurements**, alongside RW1-C's N1–N3, RW1-D's T1 and GW1's A6.

What makes it different in kind from the other nine: those were caught by a
person or an instrument reading the output. **This class executes with no
reader.**

---

# GW1-B addenda

## §Q1 — 165 and 163, reconciled

**Both figures are right, and they count different things.** Measured today by
diffing the two registry blobs directly:

| | at `ee56d2c7` | at `2e49afdd` |
|---|---|---|
| `education-site` | 191 | 191 |
| `education-lessons` | 3,575 | **3,738** |
| `education-apps` | 106 | 106 |
| **total rows** | **3,872** | **4,035** |

- **163 = rows ADDED.** New paths admitted at `2e49afdd` that did not exist at
  `ee56d2c7`. All 163 are under `ICT/Teaching_Packs/GROW_Computing/`:
  pdf 62 · docx 54 · sb3 23 · html 11 · pptx 8 · zip 4 · txt 1 = 163. It is also
  exactly the unit's source-file count on `claude/fin5-gc1-place` — 163 source
  files, 163 admitted rows, one to one.
- **165 = rows TOUCHED.** 163 added **+ 0 removed + 2 changed in place**. The two
  changed are `education-lessons | ICT/Teaching_Packs/index.html` and
  `education-site | data/usage-registry.json` — the unit's index entry and the
  usage registry, both of which had to move because the unit arrived.

So: **163 is the admitted-rows figure and 165 is the rows-touched figure.** Both
were measured, at different moments, against different denominators — which is
the same lesson as 38 → 35 and is exactly what R1 now requires be stated.

**The pin decision is unaffected, and the consequence is slightly worse than
either number alone.** Re-pinning backwards regresses all 165: the 163 vanish
entirely, and the 2 changed rows revert to their pre-GC1 digests.

## §S2 — the A4 figures re-measured through the fixed tool

| card | in the GW1-A record | re-measured after the printer fix | match |
|---|---|---|---|
| W8A `print-marking` | 976px, fits by 147px | **976px, fits by 147px** | **yes** |
| W8B `print-marking` | 955px, fits by 168px | **955px, fits by 168px** | **yes** |

They match, and the reason is worth stating rather than treated as luck. The
broken line was

```
console.log('%s %s height %dpx / printable %4dpx (A4 %d less %dpx padding)  %s', …)
```

The corruption began **at** `%4d`. Everything before it — `%s`, `%s`, `%d` ← the
card height — bound correctly. So the heights were never wrong; `printable`,
`A4`, `padding` and the verdict were the four that shifted. That is why the
verdict still read FITS: it was computed, not formatted, and then printed in the
wrong slot as a trailing extra argument.

**The figures stand.** They are no longer standing on an unverified printer.

## §S3 — denominators for the four instruments already banked

| instrument | what it examined | what it found |
|---|---|---|
| `parity.py` | **22 markers** against 1,563 elements (440 with a class), 94 ids, 4 scripts (A); 1,668 / 398 / 108 / 4 (B) | 22 rows, substring and DOM side by side; 1 declared equivalence, checked and holding |
| `render_check.cjs` | 1,573 elements, **94 ids**, **0 console messages**, **1 request** (A); 1,678 / 108 / 0 / 1 (B) | 0 duplicate ids, 0 console errors, 0 non-file requests |
| `print_identity.apply` | **16 print sections**, of which 5 staff and **11 pupil** | 4 added + 3 dates removed + 4 normalised + 0 already correct = **11 of 11**, asserted |
| `w5_screen_delta.cjs` | **16 print sections**, **15 science-meta**, 1,573 elements | 0 of 16 visible on screen, 0 of 15 meta on screen |

Three things this surfaced that a bare count had hidden:

1. **`render_check`'s request denominator is 1.** These are single self-contained
   files, so the only request is the file itself. "0 non-file requests" is true
   and it is as strong as a population of one allows — which is worth saying out
   loud rather than implying a sweep.
2. **16 sections but 15 identity lines**, and the gap reconciles: `#print-marking`
   (class `print-section mk-print`) is a staff sheet, and print identity leaves
   staff sheets alone by design (§W3). The sixteenth is the marking card.
3. **`parity.py` was exiting non-zero on every run** over `[data-ta1] → 0`. Live
   names the TA prompt hosts `data-ta1`; the pack names them `data-prompt`;
   nothing was renamed by this build. That is now a declared equivalence, checked
   (live 9 hosts, now 9, HOLDS) rather than assumed, and reported separately from
   an unexplained drop. A gate that cries wolf stops being read.

And one row was wrong in kind: `button.n6m-guide-btn` asked a static parse for a
tag that a script builds at runtime with `createElement`. The parse returned 0
forever against a substring count of 6. The file's own docstring already required
that a non-element marker be declared and given the nearest real DOM question;
this row had not been. It is now `SCRIPT-CREATED`, the static question is "does a
script still construct it" (1 of 4 scripts), and the rendered proof stays with
`render_check.cjs`, which finds it present, visible, labelled "ⓘ Guidance".
