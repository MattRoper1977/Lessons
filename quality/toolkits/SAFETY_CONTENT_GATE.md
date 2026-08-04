# Safety content gate — physical safety, first aid, and workshop wording

**STATUS: draft · OWNER: Matt · Pass TK-1, 2026-08-04**

Companion to `quality/SAFEGUARDING_CONTENT_GATE.md`, which covers **safeguarding** — disclosure routes, help
lines, legal claims made to pupils. This file covers **physical safety**: burns, blades, dust, tools, benches.
Adjacent domains, no overlap.

---

## The gate

No safety, medical or first-aid wording ships without all five:

1. **A named source.** "NHS burns first aid", "HSE wood dust guidance" — not "best practice".
2. **A checked date.** When someone actually read the source.
3. **A review date.** When it must be read again.
4. **A named owner.** The person who owns the wording, not the file.
5. **Local approval**, where the wording implies a control the centre must actually operate.

## The status line — every bench and safety card carries it

> **Prompt card — not a risk assessment.** Approved risk assessment: `[local ref]`. Review: `[date]`.

**Why this is the whole point.** A laminated card at a bench is the thing a busy adult reads. If it is complete
enough to feel sufficient, it will be treated as sufficient — and it cannot be, because it does not know the
room, the cohort, the equipment or the day. The card names its own limits, or it quietly replaces the
assessment.

## Verified content — the two facts TK-1 corrected

### Burns

**Cool the burn under COOL running water for at least 20 minutes, as soon as possible.**

Two things were wrong in the estate, not one. The duration read **ten minutes**; the audit caught that. The
water read **cold**; the audit did not. Both are corrected. **Cold water and ice are not the instruction** —
they can deepen the injury and cause harm to a child who is already shocked. The word is *cool*.

Any "10 minutes" cooling instruction is wrong wherever it appears. Corrected at
`Art_Teesside/House_Standard_and_Safety.html` and `Art_Teesside/Launch/Printable_LAUNCH_Evidence_and_Lundy_Pack.html`.

Source: NHS burns and scalds first aid, via brief §2. **Checked 2026-08-04. Review 1 Sep 2026. Owner: first-aid
lead.** **PENDING-LOCAL-APPROVAL** — the escalation route is the centre's, not this file's.

### Wood dust

Wood dust is a **hazardous substance requiring risk-assessed control**: prevention first, then
extraction/LEV where required, then suitable RPE properly selected. **"Open a window" is not a control, and a
generic dust mask is not RPE selection.** Young people require particular risk assessment, instruction and
supervision.

Source: HSE wood dust guidance, via brief §2 — **directionally verified only**. The exact local controls are the
centre's. **PENDING-LOCAL-APPROVAL (H&S / COSHH / technician).** Review 1 Sep 2026.

## Wording standards for the recurring cases

### Missing tool

**Never:** "nobody leaves until it is found."

Collective detention is not a safety control. It escalates, it is disproportionate, it can put an SEMH pupil
into exactly the state that makes a room less safe, and it cuts across safeguarding — a pupil prevented from
leaving is a separate problem from a missing blade.

**Instead:** stop work · account for tools by count · tell a staff member immediately · **staff manage
movement and exits under the centre's missing-sharp procedure**. Pupils are never collectively detained.
**PENDING-LOCAL-APPROVAL (H&S and safeguarding).**

### Wire offcuts

**Never:** cutting into a cupped hand. It puts a bare palm at the cut line to catch something specifically
described as flying, and it is offered as the safe option.

**Instead:** contain the offcut — cut over a tray, into a bin, or against a magnetic collector, with the cut end
pointing down and away. Goggles throughout. Every cut end folded, taped or capped before the work goes down.

### Reclaimed timber acceptance

**An HT stamp is one check of several, never sufficient on its own.** It tells you the pallet was heat treated
rather than fumigated. It tells you nothing about what the pallet then carried.

Accept only if **all** hold: HT stamp present (never MB) · provenance known · no chemical/oil/food staining or
odour · no paint or varnish · no rot, splitting or delamination · nails and shanks swept with a magnet.
**Reject on any one failure, even when HT-stamped.** **PENDING-LOCAL-APPROVAL (H&S/technician).**

### Dust-generating tasks

Named control per task, not a blanket rule: **prevent** (choose the method that makes less dust) → **extract**
(on-tool extraction or LEV where required) → **RPE** (selected for the task, fitted, and only after the first
two). Plus a **named stop condition** — the point at which work halts and an adult is told.

---

## Where a P0 string sits inside a protected file

Several genuine safety strings live inside **lesson slideshows**, which TK-1 may not edit, and some are held by
in-flight branches. Those are delivered as **proposed diffs in the readback and applied nowhere**:

| file | string | why not applied |
|---|---|---|
| `Build/Slideshows/BUILD_DT_W5_Finish.html` | *"Dust masks for sanding, outdoors where possible"*; *"the door stays open"* as the stated ventilation control | protected lesson slideshow (§3); also held by in-flight `semh1-dt-semantic` (#34) |
| `Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html` | HT/MB framing as the wood decision | as above |
| `Build/Slideshows/BUILD_DT_W2,W3_*` | *"HT pallet wood only (never painted or MB)"* pre-tool line | as above |

**Recorded, not silently dropped.** A P0 string that cannot be fixed in this pass is still a P0 string, and the
readback carries it to Matt with the wording ready.
