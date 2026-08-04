# Data governance — local-only tools

**STATUS: draft · OWNER: Matt · Pass TK-1, 2026-08-04**

Scope: every support tool that stores anything on a device — the Loop Walk Logger, QA and coaching sheets,
Loop Passports, evidence trackers. **Local-only storage is not governance by itself.** That is the whole point
of this file: `localStorage` answers *where*, not *why*, *for how long*, or *who may see it*.

---

## The standard — six questions every storing tool answers on its own face

1. **Purpose.** What is captured, and why. One sentence, visible before use — not in a footer.
2. **Minimum fields.** The least that serves the purpose. Initials over names. No field exists "in case".
3. **Location and device.** Which machines are approved. Data stays in that browser profile on that device.
4. **Retention and expiry.** How long a record stays useful, and the date it stops being so.
5. **Export.** What leaving the tool means, and who is then responsible for the file.
6. **Deletion.** A route the user can actually operate, described where they will find it.

## Settled positions this file records rather than reopens

- **Class lists on school-owned machines are accepted.** `ps_coldcall_roster` holds a plain array of pupil
  first names across 65 files, deliberately shared, labelled *"saved for all lessons"* — and the label is true
  (**R-B01**). Matt's accepted position. **No forced deletion. No schema migration. No key renames anywhere.**
- **`coldCall_y10` is a separate, richer system** holding `{name, grade}` objects that drive tier-matched
  questioning (**R-B02**). Writing objects to the shared key breaks 14 string consumers; seeding from the shared
  key silently flattens every pupil to tier 2. **Never naively migrated.**
- **Grades are a different category from names.** A shared per-pupil attainment store would be an origin-wide
  record of judgements about children. Any change is its own conversation, never a side effect of tidying.
- **`mbm_tt_evidence` is RETIRED-IN-PLACE** (**R-B04**) — it records that a deck reached its end screen, which
  is attendance at a slideshow, not a closed loop. Not built on, not promoted, not a candidate reader.

## Pseudonymisation is not anonymisation

Initials, first names and a class identifier together can identify a child in a small SEMH setting. **Treat
initials as potentially personal data.** The Loop Walk Logger's existing rule — *pupil initials only; no staff
names, ever* — is the correct floor and is preserved verbatim.

## The safeguarding firewall

Beside **every** free-text field on a QA or evidence tool:

> **Not for disclosures.** If a pupil tells you something that worries you, it goes to the DSL by the school's
> safeguarding route — never into this box.

And a state that records the **action** without the **content**:

> **Safeguarding handoff made ☐**

**The tick stores no detail.** It records that a route was used. Routine exports exclude it. This separates
protection from ordinary evidence, which is the point: a disclosure copied into a QA export is a safeguarding
failure wearing an evidence costume.

## Zero-egress tools — a promise that must be re-verified after every edit

`LundyLoop/2_leadership/Loop_Walk_Logger.html` promises that nothing is uploaded. At `74e6fee` that is **true by
construction**, measured, not assumed:

```
grep -cE 'fetch\(|XMLHttpRequest|sendBeacon|<form|action=|https?://' LundyLoop/2_leadership/Loop_Walk_Logger.html
→ 0
grep -oE 'localStorage\.[a-zA-Z]+' LundyLoop/2_leadership/Loop_Walk_Logger.html
→ getItem ×1, setItem ×1
```

**Any edit to this file re-runs that command and reports the result.** A promise verified once is a cached
claim (**R-G01**); the derivation is what keeps it true. Adding a font link, an analytics snippet, an icon CDN
or a `<form action>` would each break it silently — nothing would appear to change.

## What a local tool must never do

- collect a pupil's full name where initials serve;
- record staff names against a judgement;
- hold disclosure content;
- aggregate a pupil-owned closure mark into a list, column, total or tracker (**R-A09** — the absence is the
  control, and a second copy changes the artefact's species);
- send anything anywhere;
- persist data whose purpose has expired.

## Retention defaults — proposed, for the DPO/SLT to confirm

| record | default retention | then |
|---|---|---|
| Loop Walk observation | to the end of the current term | delete; the termly pattern is what carries forward, not the rows |
| QA coaching note | to the end of the current term | delete |
| Loop Passport (paper) | reviewed each term with the pupil | held under the SEND record's own retention |
| Safeguarding handoff tick | not exported; cleared with the term | the safeguarding record is the DSL's system, not this one |

**PENDING-LOCAL-APPROVAL (DPO/SLT).** These are proposals with a shape, not a policy. ICO retention specifics
are **SUPPLIED-BY-AUDIT** and unverified here — no egress. Review-by **1 September 2026**.
