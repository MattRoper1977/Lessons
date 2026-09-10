## D21 — 75 of the 205 refusals are a numbered question, not a week

Found while proving the three `Spr2·W6` pages under F6, because all three refuse
on `W1.`, not on anything calendrical.

Classifying every one of the 205 refusals by the token that actually blocked the
file — normalised so `W3` and `Week 3` count the same — leaves no residue:

| the blocking token is | files | |
|---|---:|---:|
| a real week reference | 130 | 63.4% |
| **a numbered question** (`W1.` `W2:` `W3)`) | **75** | **36.6%** |

| code | total | numbered question | week reference |
|---|---:|---:|---:|
| **F1** | 68 | **59** | 9 |
| F2 | 109 | 13 | 96 |
| F3 | 10 | 0 | 10 |
| F5 | 15 | 0 | 15 |
| F6 | 3 | 3 | 0 |

**87% of F1 is question numbering.** F1 is the code R-CAL-1 calls "the majority
case, correct behaviour, not a backlog", and it is even more correct than that
description: most of it is not a cross-unit reference at all. It is
`W1. Sort A, B and C. Give one evidence clue.` — the first question on a
worksheet — being read as week 1 and, quite rightly, refused rather than rewritten
into `Lesson 1. Sort A, B and C.`

Two consequences worth carrying into SX3.

**The scope finding is softer than it reads.** "Seven in eight Science pages carry
an un-re-tokenisable calendar token" is true of the gate's output, but over a
third of those pages carry **no calendar token in the blocking position**. They
carry a question number. The genuine cross-unit-reference population is smaller
than the refusal count suggests.

**The gate counts question numbers as pupil-facing calendar tokens.** `FORBID`'s
`\bW(?:eek)?\s?\d+\b` cannot tell `W1.` on a worksheet from `W1` meaning week 1,
so every hit count the gate has ever produced includes them. **Not changed here** —
narrowing `FORBID` changes what the gate blocks on, and that wants a ruling, not
a commit. Filed beside the UNSEEN asymmetry in D20, which is the same shape of
problem in the opposite direction: one pattern sees what it should not, the other
does not see what it should.
