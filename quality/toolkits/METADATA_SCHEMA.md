# Toolkit metadata schema — and a bounded pilot

**STATUS: draft · OWNER: Matt · Pass TK-1, 2026-08-04**

---

## The strip

One block per support toolkit, rendered visibly and expressed once in the markup.

| field | required | value |
|---|---|---|
| `title` | yes | the toolkit's own name |
| `purpose` | yes | one plain sentence |
| `audience` | yes | `staff` · `pupil` · `both` — and if `both`, which parts are which |
| `owner` | yes | a person |
| `version` | yes | `MAJOR.MINOR` |
| `reviewed` | yes | ISO date last actually read |
| `next_review` | yes | ISO date |
| `readiness` | yes | one of the **seven** states in `quality/DELIVERY_READINESS_CHECKLIST.md` |
| `evidence_status` | where evidence is captured | one of the **six** states in `CLAIMS_REGISTER.md` |
| `awarding_source` | where a qualification claim appears | body + document + version, e.g. `ASDAN PEQ spec v1.2 (Oct 2025)` |
| `supersedes` / `superseded_by` | where either applies | relative path |
| `data` | where anything is stored | `none`, or a pointer to `DATA_GOVERNANCE.md` |
| `local_approval` | where a control is implied | `[local ref]` + date, or `PENDING-LOCAL-APPROVAL (owner)` |

### Suggested markup

```html
<!-- toolkit-meta v1 -->
<div class="toolkit-meta" role="note" aria-label="Toolkit status">
  <p><b>Owner</b> Matt · <b>Version</b> 1.0 · <b>Readiness</b> delivery-ready
     · <b>Reviewed</b> 2026-08-04 · <b>Next review</b> 2026-09-01</p>
</div>
```

`role="note"` and the `aria-label` are load-bearing: the strip must announce itself as status rather than
merge into the body text of the page. **[estate] R-F05** — much of this estate's text lives in `aria-label` and
`alt` and never renders. A metadata rollout checked by eye would miss most of it. **Grep, don't glance.**

---

## The pilot — bounded at ten files, and deliberately not more

**Estate-wide rollout is a recorded debt, not this pass.** Applying a status strip to ~500 files from a session
that has read a handful would produce 500 assertions nobody verified — the exact cached-claim shape the estate
keeps catching (**R-G01**, **R-G03**). A strip whose `reviewed` date is false is worse than no strip, because
something now depends on it.

The pilot is the ten hub and support pages TK-1 actually measured and edited in Phases 2–5. Each gets a strip
whose values are **true of that file on the day it was touched**, and no others do.

### Rules the rollout must inherit

1. **A `reviewed` date means a person read the file.** Never stamped in bulk.
2. **`readiness` is asserted by the role entitled to assert it**, per the seven-state table. States 5 and 6 are
   centre actions and no commit sets them.
3. **Never invent `local_approval`.** `PENDING-LOCAL-APPROVAL (H&S)` is a true value; a fabricated reference is
   not, and it is the more dangerous of the two because it looks finished.
4. **The strip carries no pupil data**, ever.
5. **Historical stamps name a commit; currency stamps name a pass** (**R-G04**). A file cannot truthfully state
   its own currency as the commit that is about to contain the sentence — the stamp is false the instant it
   lands. `reviewed` is a date, which is safe; do not "improve" it into a SHA.
6. **The strip must not become a second copy of anything derivable.** It does not restate a sentinel count, a
   file total or a population — those are derived at run time or not stated (**R-G06**).

### Recorded debt

| debt | scope | why deferred |
|---|---|---|
| metadata rollout beyond the pilot | the rest of the support layer | each strip asserts facts about a file, and the facts have to be true of that file. Needs a pass that reads them. |
| `Humanities_Teesside` pack print units | 3 `WEEKS[]` generators | non-`pt` units; a separate measurement model from the eight Art packs |
| primary lesson + unit-index Google Fonts | ~40 files | template-locked (§3); hub only was in scope |
| `Tutor_Time` Google Fonts | 2 decks | outside §9's stated scope |
| Progress-branded staff-pack zips | `build_staff_pack.py` scope | go stale after any merge; **`MARK_SVG`/`gen_entry` reconciliation is a hard precondition** of the next full rebuild (R-J01, R-K01, R-K02) |
