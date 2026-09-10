## D32 — G5 revised: rewrite becomes add

All eight lessons carry base64 `data:` URIs only, so **there is no href to
repoint**. The reason is unchanged and stronger for it: a managed school browser
that blocks `data:` downloads removes **every** Scratch file from **every** lesson
at once, with no error a teacher would see.

- **(a)** On the **served copies only**, P3 *adds* a relative href
  (`../Scratch_Projects/<file>.sb3`, plus `download`) as the primary route, by a
  canonical writer with a red proof. Never a hand edit, never per-file.
- **(b)** The base64 payload is **retained in place, untouched.** Stripping is a
  content edit, and the offline zips are byte-identical to the served source today.
- **(c)** The offline zips are unchanged and keep `data:` primary. No server behind
  them.
- **(d)** Gate: every added href resolves 200 on the served origin with bytes equal
  to the tree; the count equals the supplied projects for that lesson; and the page
  still offers a working download with JavaScript disabled.
- **(e)** Two-sided control per D28: a planted missing sibling reds the gate, a
  planted correct one passes.

**The retained-bytes finding (b), measured, for a later ruling — no action here:**

| | lesson bytes | base64 bytes | share | projects |
|---|---:|---:|---:|---:|
| W01 | 33,712 | 2,284 | 6.8% | 1 |
| W02 | 38,445 | 6,780 | 17.6% | 3 |
| W03 | 26,427 | 932 | 3.5% | 1 |
| W04 | 30,609 | 5,032 | 16.4% | 2 |
| W05 | 31,304 | 5,592 | 17.9% | 2 |
| W06 | 31,838 | 6,068 | 19.1% | 2 |
| W07 | 35,092 | 6,968 | 19.9% | 2 |
| W08 | 35,421 | 7,628 | 21.5% | 2 |
| **total** | **262,848** | **41,284** | **15.7%** | **15** |

The base64 measurement needed correcting once: the data URI is **built at runtime**
from a `FILES[].data` field, so a regex for `data:application/x.scratch.sb3;base64,`
returns **0 payloads on all eight lessons** — a clean, confident zero from an
instrument looking for a string the file never contains. D28 again.

**The G5(d) baseline**: 23 `.sb3` = **15 pupil projects in `Scratch_Projects/`**,
every one embedded in its own lesson with names matching exactly, plus **8 teacher
models in `Teacher_Only/`**, one per week, **none embedded in a pupil lesson** — G3
already holds. So the added-href count per lesson is 1,3,1,2,2,2,2,2.
