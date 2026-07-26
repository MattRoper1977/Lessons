# Instrument Register — LundyLoop

**What this is.** One line per instrument, written when the instrument is written,
committed with the pass it served. Not assembled at the end of a session.

**Why it exists.** The previous register, and every script it described, lived in a
session working directory and did not survive it. The document and its subject were
lost together. A thing that is safe only because of what someone currently has open
is not safe.

**What this register structurally cannot detect.** Everything here agreeing, and
everything here being wrong, are indistinguishable from inside this file. This is a
record of what was intended and what was built. It is not evidence that either was
correct. The only external check is re-deriving a finding by a method that shares no
premise with the instrument that produced it — and where that has been done, the
entry says so.

**Loading order.** Any pass that measures the estate loads this file before it runs.
An instrument marked QUARANTINED must not be used, and must not be used to validate
its own replacement (standing rule 6).

---

## Fields

| Field | Meaning |
|---|---|
| ID | Stable. Never reused, even after retirement. |
| Derives | What it outputs. |
| Method | **Literal** (presence only) or **Interpretive** (requires reading meaning). Standing rule 4. |
| Independent of | Which other instruments it does *not* share a premise with. |
| Consumed by | What downstream work depends on its numbers. |
| Status | current / superseded / QUARANTINED |

---

## LL-INST-01 — `hash_sweep.py`

- **Derives:** identical and near-identical file sets across the tracked estate, each member's catalogue status in `resources.json`, catalogue entries pointing at absent paths, and tracked HTML absent from the catalogue.
- **Method:** Literal for exact and normalised hashing and for catalogue membership (path match, percent-decoded). **Approximate** for near-identity (MinHash over 8-word shingles, 128 permutations, seed 20260726).
- **Independent of:** filename-based reasoning entirely — it never consults a name to decide identity. Cross-checked *against* stem similarity, which is the independent method.
- **Known sensitivity limit — declared, not hidden:** the near-identical list is a **floor, not a complete set**. At the 0.60 shingle-Jaccard threshold it did **not** surface `biology/L4_Aerobic.html` ↔ `biology/L4_Aerobic_Respiration.html`, which word-set Jaccard scores 0.763 and sequence ratio 0.914. Shingle Jaccard is far harsher than word-set Jaccard on files that share vocabulary but differ in ordering. Do not quote "N near-identical pairs" as a total.
- **Consumed by:** queue item 6 (hash sweep), item 7 (Respiration twin).
- **Status:** current.

## LL-INST-02 — `link_graph.py`

- **Derives:** resolved inbound-link graph — for any target, which files reference it, at which line, with what visible anchor text; plus in-repo broken links and zero-inbound orphans.
- **Method:** Literal. Resolves every link relative to the *containing file's directory*.
- **Independent of:** LL-INST-01. Content hashing and link topology share no premise; a file can be a byte-identical twin and still be the only one linked, or vice versa.
- **Built to avoid a specific bug:** a bare-basename grep counted `LundyLoop/3_subject_guides/science.html` as an inbound reference to root `science.html`. It reported 1–3 inbound links for files that in fact have zero. That grep is **not** an instrument and must not be reintroduced.
- **Known limit — must be quoted with the number:** "zero inbound" means **zero in-repo**. It cannot see printed QR codes, staff-pack PDFs, bookmarks, or emailed links. Zero inbound is *not* a deletion warrant.
- **Consumed by:** queue item 6, item 7 (Respiration twin delete-or-stub decision).
- **Status:** current.

## LL-INST-03 — `print_pack_audit.py`

- **Derives:** per file, the print slots the JavaScript requests vs the slots the markup provides, in both directions.
- **Method:** Literal on both sides, parsed from two independently-located regions of the file (script body vs markup attributes). Unenumerable variables are reported as UNRESOLVED, never silently counted as satisfied.
- **Independent of:** LL-INST-01 and -02.
- **Externally corroborated:** its count of 5 unsatisfiable slots in `6 Art/Lesson10_SurrealistCollage_HANDSON_v5 (1).html` matches, exactly and independently, the "five print references it can't satisfy" recorded before this instrument existed.
- **Status:** current (v2).

## LL-INST-03-v1 — `print_pack_audit.py`, first derivation — **QUARANTINED**

- **Defect:** hardcoded the tier level names as `('foundation','middle','higher')`. The Art_Teesside suite uses `('supported','standard','stretch')`. Every file using the second vocabulary was reported as missing six slots that in fact exist.
- **Numbers it produced, now retired and unquotable (standing rule 7):** *123 files with at least one absent slot; 691 absent slot-instances.* Both are false. The true figures from v2 are 13 files and 22 slot-instances.
- **Why it was caught:** standing rule 5. 691 was too large and too dramatic to be true of an estate this size, and that implausibility was treated as evidence about the instrument before it was treated as evidence about the estate.
- **Remedy, and why it is not the broken instrument (standing rule 6):** the level names are no longer a premise at all. v2 derives them literally, per file, from that file's own `printPack('...')` call sites. The failure set of v1 was "files whose vocabulary I assumed wrongly"; v2 has no vocabulary assumption to fail on.
- **Status:** QUARANTINED. Do not reuse. Retained here as the record.

---

## Seed conventions carried forward

These are decisions, not scan results, and belong in the exception register proper
(queue item 1). Listed here so they are not lost twice.

- The two assessed files' declared absences.
- The 56 BUILD files deliberately lacking the writing line.
- The **I Do** convention: no print counterpart, deliberately, because it is modelled live.
- The **Arrival** convention: settling routine the adult runs.
- The deliberately identical Standard/Stretch rows.
- `coldCall_y10` → `ps_coldcall_roster` migration state, and the deliberately estate-wide shared keys.
- The superseded Surrealist Collage file.
