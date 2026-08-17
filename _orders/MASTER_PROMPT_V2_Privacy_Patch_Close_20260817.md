# MASTER PROMPT — Apply the V2 privacy patch and close it
**Date:** 2026-08-17 · **Subject:** `Virtual_Science_Laboratory_PRO_v0_4.html` (287,161 B · 1,978 lines · sha256 `137bbfac…` · 13 benches)
**Verdict on the method: GO. Apply exactly what was proposed, plus the two additions in §0.2.**

**The finding as it now stands, and it is worse than the one we started with:** `syncHash()` has 119 call sites and both fields update state on every keystroke, so the moment a pupil types a name the next bench interaction rewrites `location.hash` with it. It then sits in the address bar for the whole session — browser history, bookmarks, screen shares, **a projector in a room with other pupils**, and any copied URL. **Share is the loudest exit, not the only one.**

---

## §0 RULINGS

### §0.1 Accepted as proposed
- **`serialisableState()` stays untouched, and that is a correction to my own P2 wording.** `exportEvidence()` calls it at line 1805 and the evidence JSON legitimately carries the name — it is a local download named after the pupil. Mine would have stripped it from the export too. The split is right: **private in the URL, present in the local download.**
- **The caption is not reworded.** *"Name for print/export only"* becomes **true** with this patch. That was always the requirement — a caption that lies must not survive — and it is satisfied by making the code honest rather than the words weaker.
- Change 2 (`delete incoming.pupil; delete incoming.notes;` in `loadHash()`) and change 3 (the toast naming the guarantee) as written.

### §0.2 THE TWO ADDITIONS
- **A — a gate that never touches Share.** Every proposed gate goes through the Share path; the finding is that the hash is rewritten without it. Add: type both canaries, trigger **any ordinary bench interaction**, read `location.hash` — neither canary present. Red-on-revert applies. Reading from the hash rather than the clipboard was the right call and this extends the same logic.
- **B — push the patched file to a branch before the session ends.** A patched HTML handed back and living nowhere is the tag's failure exactly: **a file in a disposable container is a countdown, not preservation.** Branch it; that is preservation, and it is not placement.

### §0.3 SCOPE — name and notes only
`phaseAnswers` and drawing strokes are the **same principle at lower severity** and are their own change: they are not identifying, and stripping strokes makes the reload cost far worse — a lost drawing is lost work, a lost name is one retype. **Do not widen this patch.** Record explicitly that **P2 is half-implemented**, so nobody later reads this as having closed the URL principle.

### §0.4 THE RELOAD COST — accepted, and no storage
The file has **zero storage APIs**; the URL is the only persistence, so after this fix a reload loses the typed name and notes. **Do not add storage to compensate.** On a shared classroom machine `localStorage` would leave a pupil's name for whoever sits down next — arguably worse than the address bar — and it breaks a declared property of the file that other checks rely on. The answer to a lost note is **Print or Export before reloading**; both still carry the fields. Refusing to add storage was the right instinct.

### §0.5 VERSION — and this one matters more than it looks
**Do not call the output v0.4.1.** In every order and ledger entry in this estate, *v0.4.1* means **the patch order ran** — P1 through P9, all six V-findings and three N-findings. Only P2 has run. Labelling this v0.4.1 guarantees that a future reader concludes V1, V3, V4, V5, V6 and N1–N3 are fixed when they are not.
- **File version label: `v0.4-privacy1`** (or an equivalent that cannot be mistaken for the patch order's output). State the reason in the file's own header comment.
- **Bump the hash state-version tag** (currently "0.2"/"0.3"): the URL payload shape has changed, and the bump is what lets a future reader tell a pre-fix link from a post-fix one. The bump is for the record — change 2 is the mechanism.

### §0.6 STILL NOT SHIPPABLE, AND PLACEMENT STILL WAITS
This makes the file **safer, not deployable.** V1 still rewards the procedure it teaches against. V5 still marks *"the glowing splint does not relight"* as correct. N1 still deletes a pupil's oldest drawing stroke without a word. **No placement, no route, no hub, no `resources.json`** — §0.2's branch is the whole of the landing. The unlinked-until-paper-read ruling stands for whenever placement does happen.

---

## §1 PRECONDITIONS — DERIVED (R0.18, R0.30)
1. State **where the artefact is** and print it.
2. Verify the input **before** patching: 287,161 B · 1,978 lines · sha256 `137bbfac3ea98255fad55b44c3073810d2a0876cc833e555b61f6989114daf7f` · 13 benches. **A delta is a stop** — a different file is a different subject.
3. Confirm 13/13 benches boot: 0 page errors, 0 console errors, 0 console warnings. This is the baseline §3's page-error gate is measured against.
4. Re-confirm the 119 `syncHash()` call sites and the two keystroke handlers from the file, not from this document (R0.12).

---

## §2 APPLY — three changes, nothing else
`shareableState()` used only by `syncHash()` · the two deletes in `loadHash()` · the toast. Plus §0.5's version label and hash-version bump. **Every other line of the file is untouched**, and the diff is emitted in full so that claim is checkable rather than asserted.

---

## §3 GATES — every one both directions, each named

| gate | green | red |
|---|---|---|
| canary absent via Share | type both, Share, decode hash → neither present | revert the patch → both present |
| **A: canary absent WITHOUT Share** | type both, any ordinary bench interaction, read hash → neither present | revert → both present |
| evidence export | exported JSON still contains name + notes | strip from `serialisableState()` instead → export loses them |
| print pack | print HTML still contains the notes | as above |
| state round-trip | photosynthesis at 65 cm shares and restores in a fresh page | corrupt the token → restore refuses |
| legacy link | a pre-fix URL carrying the canary opens with the field empty | without change 2 → it repopulates |
| page errors | 0 across 13 benches | — |

Read from `location.hash`, **never the clipboard** — a headless clipboard permission must not be able to fake a pass. **Output shows both directions on every run**: *n* reds fired, *n* greens returned (R0.24). If any control fails to fire, report and land nothing.

---

## §4 BRANCH IT (§0.2 B)
Push to a working branch. **Ref table before/after (R0.19)** with a one-line loss statement. No PR is required, but say which you did and why. Nothing is placed, linked, catalogued or merged.

---

## §5 RECORD — by dated supersession, never rewrite
1. **The widened severity**, in its own words: 119 call sites, every keystroke, the address bar for the whole session, a projector at an SEMH provision. This is why the finding outranked everything else on the board.
2. **The new measurements** — bytes, lines, sha256 — as a dated set beside the pinned intake set, not replacing it.
3. **P2 is half-implemented**: name and notes out, `phaseAnswers` and strokes still in the URL, with the reason.
4. **The reload cost**, accepted, with the print-or-export guidance and the reason storage was refused.
5. **Residue that cannot be fixed, named not tidied: links already minted, bookmarks already saved and screenshots already taken are unrecoverable.** The patch stops new ones; it does not reach the old ones.
6. **The version reasoning** from §0.5, so the name cannot later be read as the patch order's output.
7. **Still not deployable**, with V1, V5 and N1 named as the reasons.

---

## §6 READBACK — six items
1. Preconditions as derived, including the re-confirmed call-site count.
2. The full diff, and the assertion that nothing else moved.
3. The gate table with **both directions fired**, gate A included, and the reds named individually.
4. The branch, with its ref table.
5. The record entries from §5, each as landed.
6. What remains open by name — the eight unpatched findings, placement, the paper read, and everything on the wider board.

---

## §7 STOP CONDITIONS
- Any input measurement differs → stop.
- Any gate cannot be shown red on revert, or green on a known-good input → it is not a gate; land nothing.
- The diff touches anything beyond the three changes plus the version strings → stop and show it.
- Adding storage is proposed → stop; that is a design change and it is refused.
- A record edit would rewrite rather than supersede → stop.

---

## §8 OUT OF SCOPE
Placement, routes, hubs, `resources.json` · `phaseAnswers` and drawing strokes · V1, V3, V4, V5, V6, N1, N2, N3 · storage of any kind · `#116` · the wider close order's §3–§8 · anything on Matt's own list.

---

*The patch is six lines and it removes a pupil's name from the address bar of a machine that gets projected at the front of an SEMH classroom. Everything else in this file — the chemistry that is right, the biology maths that is exact, the seventeen checksums that verify — was always true and never made it safe to use. This does, for one thing, and names the eight that are still waiting.*
