# MASTER PROMPT — Close what's left, and fix the thing that keeps blocking the rest
**Date:** 2026-08-17 · **After:** `claude/vsl-v0.4-privacy1` @ `ed6dfca` · Lessons main `c630fa8`
**The patch landed. This order clears the board around it and removes one recurring blocker.**

---

## §0 RULINGS

### §0.1 Two corrections to my orders, both accepted, and they form a pattern
- **The URL-only version bump** — `shareableState()` sets `0.4p1` while the export keeps `"0.4"` — is right, and better than my §0.5, which said "bump the hash state-version tag" without noticing `serialisableState()` shares it. Bumping there would have moved the evidence JSON, which §0.1 forbade.
- **The M2 print mutant.** My §3 gave *"strip from `serialisableState()`"* as the red for **both** the export and print gates. It does not reach print — `preparePrint()` reads `state.notes` directly. **A shared mutant must be proven to reach every gate that cites it**; one mutation is not N assertions, and this is that rule recurring on my own control table. Ratified, not a new id (R0.17 — the ledger allocates).
- **The pattern worth naming: three separate rulings of mine have now reached the export path by accident.** `serialisableState()`, the version tag, the print mutant. The export is the thing my rulings keep touching without meaning to. Record it, and treat any future VSL ruling that names a serialiser as touching the export until proven otherwise.

### §0.2 RULING — the order documents live in the repo, and this is the blocker to remove
Two VSL order documents are missing, and that is why the full patch could not run. They exist only as chat outputs. **This is R0.30 applied to the orders themselves: an order that names where its subject lives, but lives nowhere itself, is unrunnable by any session that does not already hold it.**
**Ruled: commit the order documents to the repo** under a single named directory, so any session can be pointed at them. They contain no pupil data — they are methodology, hashes and findings. §2 does it.

### §0.3 RULING — B2 is retired
It has been "recorded as a gap" through four readbacks, has never produced a surviving result, and **nobody can state its scope from the record.** An item nobody can scope is not a task. **Retire it**, with a retirement entry that says what is being given up and what would justify raising it again — so a future reader retires it knowingly rather than finding it quietly gone. If a specific need appears later it re-enters as a fresh, scoped order, not as a resurrected line.

### §0.4 RULING — a gate that cannot produce a verdict is fixed or disabled, never left running
The census gate has **exited 2 twice and cannot currently produce a verdict.** Exiting 2 rather than passing falsely is correct behaviour (R0.9, R0.28) — but a gate that is permanently inconclusive occupies the slot of a working check while asserting nothing. It is the mirror of *"a gate that is always red is deleted within the week."* **Diagnose, then fix it or disable it with a stated reason and a named condition for re-enabling.** Both outcomes are acceptable; leaving it is not.

---

## §1 DERIVE (R0.18, R0.30)
Heads for all three repos · open PRs with check counts · the branch `claude/vsl-v0.4-privacy1` intact at `ed6dfca` · the matcher's soak count as printed by the tool, never copied (R0.29) · which order documents are present in the repo and which are absent, **named individually**.

---

## §2 LAND THE ORDER DOCUMENTS

2.1 Create one directory for them and say why it is that one (derive from the estate's existing conventions — do not invent a new pattern).
2.2 Commit the VSL orders that are missing, plus any other order document the estate references but does not contain. **Enumerate what you found absent** — a list of two is a claim; the enumeration is the measurement (R0.8).
2.3 **Do not edit their content.** They are dated records; a document committed later is still the document that was written then. If one is superseded, that is recorded beside it, never inside it.
2.4 Add a one-line index so the next session can find them without knowing their filenames.

---

## §3 THE CENSUS GATE

3.1 Diagnose the exit 2 from the artefact — the two runs, the exact failure, the mechanism (R0.12: read the runs, not the summary line).
3.2 Then one of:
- **Fix it** — and prove it both ways: a real red on a real defect, and a green on a known-good input (R0.24). A fix that only restores the ability to exit 0 is not a fix.
- **Disable it** — with the reason, the condition for re-enabling, and an unfiltered census (R0.16) of anything that reads its output. A disabled gate that something still consumes is worse than a broken one.
3.3 Whichever, the workflow's `paths:` filter and matched path are printed (R0.1 limb 3).

---

## §4 THE FIVE ROUTES — implement the verdicts already made

Four **EXTEND**, one **EXEMPT**, disposed but not implemented.
4.1 Extend the deriver to cover the four, and prove each is now derived — count with its predicate before and after.
4.2 The exempt one carries its written reason in-repo, not in a chat transcript.
4.3 **The two JSON files are data, not pages** — if either is among the four, state which assertion it gets, because byte-identity of a served *page* is the wrong test for a data file. If that cannot be settled cleanly, EXEMPT it with the reason rather than assert the wrong thing.
4.4 Controls both directions: remove a route from the source → the deriver's count drops and names it; a known-good set returns green.

---

## §5 B2's RETIREMENT ENTRY
Per §0.3. One dated ledger entry: retired, what it was intended to cover as far as the record shows, **what is being given up**, and what would justify raising it again. Nothing is deleted from the record; the gap becomes a decision.

---

## §6 REPORT ONLY — no action

- **The matcher / PR #132** — soak as printed, no wiring, no PyYAML. `unenforced` is an honest state.
- **The five held PRs** — exempt-while-held; confirm each body carries its disposition, and touch nothing else.
- **`claude/vsl-v0.4-privacy1`** — stays a branch. No PR, no merge, no placement. A PR is a request to merge and nothing here asks to merge; that judgement was right.

---

## §7 THE LEDGER ENTRY
Dated supersession only. Contents: §0.1's three-strikes pattern on the export path · the order-document fix and what was found absent · the census gate's disposition · the four routes now derived and the one exempt · B2 retired with what was given up · **what remains open by name**, split into estate items and Matt's.

---

## §8 MATT'S LIST — attempt none of it
**Revoke the GitHub token** — security, and the oldest item on the board · auto-delete head branches · the Actions notification setting · PLANS-3 close-out · the 29 August reconvergence · **the VSL paper read**, which is what unlinks placement.

---

## §9 READBACK — six items
1. State as derived, with the order documents found present and absent, named.
2. §2 as landed, and the directory choice with its reason.
3. §3's diagnosis and disposition, with both-direction proof if fixed or the census if disabled.
4. §4's before/after counts with predicates, and each control fired both ways.
5. B2's retirement entry as written.
6. What remains open by name — estate and Matt's, apart.

---

## §10 STOP CONDITIONS
- An order document's content would need editing to commit it → stop; commit it as written or report why it cannot be.
- The census gate's cause cannot be established from the artefact → **disable it** rather than guess at a fix.
- Any control fires in only one direction → not a control.
- A ledger edit would rewrite rather than supersede → stop.
- Anything proposes merging, placing or linking the VSL branch → stop; that is not this order.

---

## §11 OUT OF SCOPE
The eight remaining VSL findings and P2's remainder — **that is the next order, and §2 is what makes it runnable** · placement, routes, hubs, `resources.json` for VSL · storage of any kind · `#116` · rebasing or merging any held PR · anything in §8.

---

*The patch that landed removes a pupil's name from a projected address bar, and the readback's last line is the one to keep: it stops new links and cannot reach the ones already pasted, bookmarked or screenshotted. Those are gone. Everything in this order is smaller than that — but §2 is the one that stops the next order failing for the same reason the last one did.*
