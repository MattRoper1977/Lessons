# P2 FieldOps FINISH v2 — §READBACK

ROLLBACK_LESSONS `efdbfb4` → merge **`92f1c16`** · ROLLBACK_APPS `6a8ae06` → merge **`a50376a`**

## §0 ground truth — all five verified

Labs byte-identical to `tools/fieldops/staging/` ×4 · Studio sha `6678059f…`
byte-identical to staging · `CONVENTIONS_EXEMPTION_fieldops.md` names both paths ·
`Science_Teesside/Build/FieldOps/` = **0 files** (phantom, not created).

## §1 the defect — fixed, and the reason it survived

**The prefix, derived not assumed.** `tools/verify_served.mjs:79` declares
`LESSONS_ORIGIN = 'https://madebymatt.uk/Lessons'` — so Lessons is **`/Lessons`-
prefixed, not root-mounted** — corroborated by the one recorded live pin in the
estate, `madebymatt.uk/Lessons/resources.json`. Joined to `PLACED`
(`tools/verify_fieldops_served.mjs:74`), exactly as `verify_served.mjs` itself
builds lab URLs. **This corrects the phone-check URL in my own earlier report,
which omitted `/Lessons`.**

**T16** (`tools/fieldops/build.mjs`) rewrites the four engine entries to
`https://madebymatt.uk/Lessons/Science_Teesside/Build/v4_fieldops/<lab>`. The
mission payload is untouched — `buildMission()` does `info.file + '#mission=' +
b64url(m)` and a hash appends to an absolute URL identically; `.file` has exactly
one reader.

**Why a green harness shipped a 404.** `split_transport.mjs` proved the
*file-import* transport (`setInputFiles` on `#missionFile`) and **constructed the
lab URL itself**, so the one string the launch route depends on was never read by
any test. The governing prompt asked for "one per transport: URL-hash and file
import"; only one existed.

| row | proves |
|---|---|
| **S4a** | the Launch anchor carries the live Lessons URL with `#mission=` intact |
| **S4b** | following it opens the right lab **on the other origin**, HTTP 200, title + question populated |
| **S4c** | CONTROL — the pre-T16 bare filename **still 404s** on the Apps origin |
| **S2c** | CONTROL — a **tampered** capsule is refused by the same import path that accepts a good one |
| S1a/b, S2a/b, S3/S3b | unchanged, still pass |

S4 serves the two trees on two real local ports and intercepts the *production*
URL, fulfilling it from the Lessons tree — so the shipped string is what is
tested, not a rewrite invented for the test. **0 split-transport failures.**
Fixtures authored by the harness and declared as such (the pack's twelve samples
were never shipped).

Controls `T16` (release 0/4 absolute → staging 4/4) and `T16-derive` (the join
still equals what `build.mjs` writes, else red) are **matched pairs**; the suite
holds **0 failures, 1 declared-unreachable by design (C24)**.

**Labs carry no back-link to the Studio — RATIFIED**, recorded in the exemption
doc: a pupil surface has no use for the teacher's minting tool. NAV-1 remains
their one way out (S3/S3b).

## §2 visibility

- **Lessons**: 4 entries under the **existing** `Science · Teesside` chip
  (**63 → 67**), `type: "pupil"`, every description saying *instrument*, not
  lesson. Appended in the file's own formatting — **92 insertions, 0 deletions**
  (a first attempt reformatted all 11k lines and was reverted).
- **Apps**: Studio added to `apps.json` under Teacher tools beside the Maker Lab.
  The homepage renders from `apps.json` at runtime (`fetch("apps.json")` →
  `render()`), so the count is **derived and no constant was touched**:
  **Teacher tools 13 → 14, total studios 38 → 39**. 7 insertions, 0 deletions.

## §3 deploy state — my earlier claim corrected

"Apps Pages had no visible run" was **my measurement artifact**, not a defect: I
had queried only the last three runs. Apps Pages exists and had already deployed
successfully — `pages build and deployment`, `6a8ae06`, success, 2026-08-18
20:52. There is no custom Pages workflow in Apps (GitHub's built-in builder), so
none was created.

## §4 gates

sweep exit **0**, planted-stale `qa-record` control **fires**, self-test PASS ·
**sweep universe**: selector `/(^|\/)(evidence|qa)\//` + `.out|json|txt|md|log` —
the only changed file inside it is `tools/fieldops/evidence/split_transport.out`,
which parsed with **0 rows matching no form** (labels 99 → 103, still 0 stale) ·
`node --check` ×3 · Studio + 4 labs **boot clean, 0 duplicate ids** · sentinels
**50/123 set-identical** · PROTECTED **IDENTICAL 736** · food census unchanged ·
**nothing under `v3_40min/` or `Science_Teesside/Launch/`** touched · merges
`--no-ff` by local git (the API route was not needed).

## Live check

**raw-pin NOT RUN — network blocked** (HTTP 000 on both origins; `api.github.com`
returns 200 from the same shell). Phone-check URLs:

1. `https://madebymatt.uk/Lessons/Science_Teesside/Build/v4_fieldops/` — one lab
   boots, Calm works, pupil text does **not** survive a refresh.
2. `https://mattroper1977.github.io/Matt-s-Apps-/FieldOps_Teacher_Studio.html` —
   the card is now on the Apps homepage; forge a mission, press **Launch
   mission**, confirm it opens the lab on madebymatt.uk with the title carried
   across, then export a capsule from the lab and import it back to the Evidence
   Desk.

Owner-held: staff-pack rebuild (unblocked); ranked PROPOSED table at
`_sca1close/PROPOSED_RANKED.md`.
