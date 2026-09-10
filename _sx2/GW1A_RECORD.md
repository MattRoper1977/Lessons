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
