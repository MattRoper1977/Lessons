# Orders — the documents that governed each pass

**Point a session here.** These are the master prompts that governed work on this
estate, committed so that a session can be handed the order rather than needing
to already hold it.

## Why this directory

`_orders/` follows the estate's existing convention, it does not invent one:
**an underscore prefix marks a directory of records rather than served routes.**
There are twenty-four of them (`_close/`, `_glv3/`, `_passq/`, `_sixclose/`, …),
none carries an `index.html`, and none is a route. Orders are records, and they
span passes rather than belonging to one — so they get one durable directory
under the same convention.

## The rule these exist to satisfy

R0.30 applied to the orders themselves: **an order that names where its subject
lives, but lives nowhere itself, is unrunnable by any session that does not
already hold it.** That is not hypothetical — it is exactly why the VSL patch
order could not run on 2026-08-17. The session held the artefact, verified all
seventeen checksums and all four measurements, and then stopped, because the
document saying what to do with it existed only as a chat output.

**Committed as written (§2.3).** A document committed later is still the document
that was written then. Nothing here is edited to match what happened. Where an
order was superseded or partly refused, that is recorded **beside** it — in
`RELEASE_LEDGER_2026-08-16.md` — never inside it.

## Index

| order | date | what it governed | outcome |
|---|---|---|---|
| `MASTER_PROMPT_Three_Tidy_Jobs_20260817.md` | 2026-08-17 | the site tag · the zero-check PRs · the path-filter matcher | tag proved gone rather than pushed; nine PR causes derived; matcher landed report-only (PR #132) |
| `MASTER_PROMPT_Close_Everything_20260817.md` | 2026-08-17 | VSL v0.4.1 · the matcher PR · record corrections · five routes · B2 | **§2 stopped** — the two VSL orders it told the session to execute were absent. Everything else completed |
| `MASTER_PROMPT_V2_Privacy_Patch_Close_20260817.md` | 2026-08-17 | apply the V2 privacy patch and close it | applied, gated 6 red / 7 green, branched `claude/vsl-v0.4-privacy1` |
| `MASTER_PROMPT_Board_Close_20260817.md` | 2026-08-17 | land these orders · the census gate · the five routes · retire B2 | this pass |

## Absent, and named individually (R0.8 — the enumeration is the measurement)

The estate references exactly **two** order documents by name that **no
repository contains and no session has held**:

| document | referenced by | status |
|---|---|---|
| `MASTER_PROMPT_VSL_Intake_and_Ledger_2026-08-17.md` | `RELEASE_LEDGER_2026-08-16.md`, `MASTER_PROMPT_Close_Everything_20260817.md` §2.1 | **ABSENT** |
| `MASTER_PROMPT_VSL_v0.4.1_RUN_2026-08-17.md` | `RELEASE_LEDGER_2026-08-16.md`, `MASTER_PROMPT_Close_Everything_20260817.md` §2.2 | **ABSENT** |

**These two could not be landed by this pass, and the reason is not the one the
ruling assumed.** The ruling reads *"they exist only as chat outputs"* and
directs that they be committed. The session that was directed to commit them
**does not hold them either** — they were never uploaded to it. A document cannot
be committed by a session that does not possess it, and writing a replacement
from the fragments quoted in other orders would be a reconstruction wearing a
dated filename, which is worse than an absence (R0.28).

**They remain the blocker to the next VSL order.** Whoever holds them should drop
them in this directory; nothing else is needed to make that order runnable.

One further order is referenced without a filename: **"the close order"**, whose
§5 required the B2 conformance matrix and three per-app verdicts. It is not on
disk, its filename is not recorded anywhere, and nothing names the three apps it
scoped — which is the substance of B2's retirement.
