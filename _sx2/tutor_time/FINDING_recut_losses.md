# FINDING — the re-cut losses are three assignment statements, not editorial judgement

ORDER LF1-M §4. Measured on the uploaded batches 01–07, the four originals packs
and the master collection. **Nothing has been edited. No deck has been touched.**

---

## 1. The cause

`source/build/adapt_batch_content.py`, which builds a weekly re-cut from an
original session's content JSON, lines 12–13:

```python
a.update(status='Linked week edition', delivery_day=day, week_theme=cfg['theme'],
         batch=cfg['batch'], hook=cfg['hooks'][k])
a['staff']['delivery'] = cfg['bridges'][k] + ' ' + day + ' morning, 20 minutes. ' \
                         'Arrival/welcome 1; fictional decision 3; ... ' + cfg['strategies'][k]
```

Both **assign**. Neither appends. The original `hook` and the original
`staff.delivery` are overwritten wholesale by generated weekly framing.

`staff.delivery` is where the safeguarding routing lives. It is where *"arrange
immediate appropriate adult support rather than investigating in the hall"* lived,
and *"safeguarding action begins now; it never waits for an exit ticket or tutor
follow-up"*, and the SEMH access floor — *"pass, point, think silently"*.

**Twelve of the thirteen lines §4 named by hand are in `staff.delivery`.** The
thirteenth is in `model.steps`. This is not scattered prose loss and it was never
an editorial decision. It is `=` where `+=` was meant, in one build script, applied
to seventeen sessions.

| where the loss is | lines | |
|---|---:|---:|
| `staff.delivery` — **overwritten**, line 13 | 38 | 36.9% |
| `hook` — **overwritten**, line 12 | 35 | 34.0% |
| `status` — `Revised`/`New` → `Linked week edition` | 16 | 15.5% |
| `followup.action` | 4 | 3.9% |
| `model.steps` | 3 | 2.9% |
| `practice.support` · `followup.response_by` · `model.caption` | 6 | 5.8% |
| `model.type` | 1 | 1.0% |
| **total** | **103** | |

**89 of 103 — 86% — come from the three overwrites.**

`status` and `model.type` are **not** content loss: `'Revised'` → `'Linked week
edition'` is a deliberate change of state. Excluding those 17 leaves **86 lines to
restore**, listed per id and per JSON path in `RESTORE_LIST.md`.

---

## 2. Why this makes §4c safer, not harder

§4c asks for every dropped line back "in the equivalent structural position". Because
the diff was taken on the **content JSON** rather than on rendered text, every one of
the 86 already carries its position as a JSON path — `staff.delivery`,
`model.steps[3].text`, `followup.action`. There is nothing to guess.

And for the two overwritten fields the target state is not a judgement either. §4e
says the target is *original ∪ re-cut*; for `hook` and `staff.delivery` that is
exactly **original text plus the generated framing**, which is what line 12 and
line 13 would have produced had they appended.

---

## 3. One count I could not reproduce, stated plainly

§4 reports 183 dropped sentences across the 17. **I measure 103, of which 86 are
content.** I could not reach 183 with any instrument:

| instrument | total |
|---|---:|
| visible-text sentences, exact set difference | 106 |
| visible text, substring absence (§4's own probe method) | 109 |
| visible text, multiset difference | 116 |
| content JSON, whole-field difference | 61 |
| **content JSON, sentence within field** (used here) | **103** |

Adding the 18 sentences that are present but **reworded** gives 121, still short.
The per-id gaps are not a constant factor either — mine is lower than §4's on
sixteen ids and *higher* on V04 (10 against 7 before metadata exclusion, 9 after),
so the two instruments differ in kind, not in calibration.

**What makes me confident the list is nonetheless complete where it matters: all
thirteen lines §4 named by hand appear in it**, each with the JSON path it restores
to. Whatever the 80-line difference is, it does not contain any line §4 identified.

If the 183 came from a specific script, point me at it and I will re-run against it
before restoring. Restoring on a list that is 40% short is exactly the failure this
document exists to prevent.

---

## 4. Two things §4 did not name, both worth a look

- **`followup.action`, B05:** *"Collect no incident details in a class form."*
  Dropped. That is the same C01 worry-box guard as the S09 line §4 flagged, in a
  different field, and it was not on the list.
- **`model.caption`, V04:** *"Liberty includes a voice and personal choices; it does
  not entitle someone to control another person."* Dropped — the definitional line
  of the session.

---

## 5. What is confirmed, independently

- **§3's map closes exactly.** The content JSONs give 21 originals and 21 batch
  sessions, overlapping on 17. Originals with no re-cut: **S01, S05, S08, V01** —
  §3's four. New in the batches: **B06, B07, S10, V08** — §3's four. 25 unique.
- **§6b holds, 21 of 21.** Every master-collection payload equals its per-deck file
  minus the pack-link, **71 bytes every time**, no exceptions.
- **§9's premise is out of date.** `Safeguarding_Assemblies_Part_2.zip` **is** in the
  upload set, carrying per-deck packs for S06, S07, S08 and S09. The
  master-collection fallback was not needed; all 21 originals are available per-deck,
  and they agree with the payloads.
- **All duplicate uploads are md5-identical** (§6e), including the four zips that
  arrived twice and the collection that arrived five times.
