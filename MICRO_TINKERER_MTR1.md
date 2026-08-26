# Micro-Tinkerer — MTR-1 close

Order: `DEPLOY.md` §8, `mbm-micro-tinkerer-release-2026-08-26-MTR`. Run 2026-08-26.

---

## §0 · Expected outcome, stated up front

`CLICK_EFFECTIVE` is **NOT-DONE**, so **§MTR-5 is HELD and this release is partial.**
That is the order's own predicted result, and it is the correct one.

What the order did not predict, and what this run establishes by measurement, is
that **§MTR-0's first estate fact is false**, and that **§MTR-4's write and
§MTR-5's write both land in repositories this session cannot write.** The
machine-doable half — §MTR-1 — is done and proven. The rest is prepared to the
point of being a paste, with the proof already run.

| limb | outcome |
|---|---|
| MTR-0 readback | **DONE** — one of three estate facts contradicted, see below |
| MTR-1 PWA | **DONE** — shipped, 15/15, three positive controls |
| MTR-2 endpoint | **HELD** — no Worker is deployed; nothing to inject |
| MTR-3 two-phone | **UNMEASURED** — Matt's, not the agent's |
| MTR-4 Games record | **PAYLOAD PROVEN, WRITE OUT OF SCOPE** |
| MTR-5 site publish | **SKIPPED-BY-GATE** — hash printed below |
| MTR-6 copy | **REPORT-ONLY** — not composed |

---

## §MTR-0 · Readback and pins

Three estate facts govern the release. Each was established, not assumed.

### Fact 1 — "Site and Games are ruleset-protected. PR only." — **CONTRADICTED**

The two required-status-check ids the order gives as established fact, site
`21475918` and Games `21475919`, **appear nowhere in any of the three
repositories** — not in a worktree, and not anywhere in Lessons' full history
(`git log --all -S`). Their only occurrence in the supplied material is
`DEPLOY.md:148` itself.

The estate's own measured instrument reads `protected=False`, `enforcement=off`,
`required contexts=0`, `rulesets=0` across all five repositories, and 11 of 101
sampled merged PRs merged over a red check. The estate's own register carries the
ruleset clicks as **still outstanding and Matt's alone**, item 5 on the standing
remaining-items list as of 2026-08-25 — one day before this order.

The estate names required checks **by job-name string**, never by numeric id.

**This does not change the working method.** Everything below still goes through
a PR. Nothing was pushed directly to any `main`. The correction matters because a
premise stated as established fact was not, and because a limb that "cannot push
directly" for the stated reason in fact can — which is a different risk.

### Fact 2 — the mirror leg is deadlocked and blocks this release — **ESTABLISHED, and worse than stated**

- The leg is in the **site** repo: `.github/workflows/agx1-live-verify.yml`,
  job `Fetch the live estate and compare to raw-at-SHA` (line 32), step
  `Shelf mirror equals the served canonical, byte for byte` (line 255).
- The job checks out at `ref: main`, so **the deployed tree is the subject of the
  gate, deliberately not the PR branch** — which is the mechanical reason a PR
  inherits a red it did not cause.
- It fires on **every** pull request to main with **no `paths:` filter**. A
  Micro-Tinkerer site PR will run it. Expected, not a finding.
- PRs **#191** and **#192** both exist in the site repo, both open, both held on
  it. #192 records `CLICK_EFFECTIVE` as NOT-DONE.

**Second, independent red, not in the order.** The shelf mirror is stale *right
now*, regardless of any Pages deploy:

```
canonical  MattRoper1977/Games/games.json                  f4aab9ab…  28,805 bytes
mirror     site data/source-manifests/games.json           4b3787eb…  28,722 bytes
```

The drift is exactly six `desc` lines — the child-voice rewrites that landed in
Games #41 — and nothing else. `render_games_manifest_mirror.py --check` exits 1
today, and both halves of the mirror-guard pair red. **The deploy click alone
will not clear this leg.** Regenerating the mirror is a separate, prior fix.

X-D1 stands: nothing here demotes, disables or `continue-on-error`s that check.

### Fact 3 — `games.json` has a single writer and it is Matt — **ESTABLISHED**

Corroborated independently by the search index's own provenance note:
*"single-writer authoritative manifest since the two-driving-games house rule."*
No tool in the Games repo generates `games.json`; the workflows validate it.

**No delegated write was made.** Z-D3 requires the delegation quoted verbatim in
the commit message, and this session has no such quotation from Matt — the order
text is a third-party document supplied to the session, not Matt's own words
authorising a write. A quiet hand-edit is exactly what the guard exists to stop,
so the record below is a *payload*, not a commit.

### Readback rows

| row | value |
|---|---|
| `MAIN_TIP` (Lessons) | `288f84543ccef2884de62e6002b4b814360249c1` |
| Site tip | `cb435f4bbdbdc1f45096bf4623464409c166b9fc` |
| Games tip | `43b29f79231115740abc9ffc3c2bee64743aa8d8` |
| Workflow vs the 20,047-byte before-image | **exact.** `agx1-live-verify.yml` is 20047 bytes; sha256 `50702afefaff149767ec77b88440554c4b363d350943c6b6c412bf7b2d6ce6b3`. It is the only file of that size in the estate. |
| `CLICK_EFFECTIVE` | **NOT-DONE.** The token exists nowhere in any of the three repos under any name; the state is carried in PR #192's body. |
| `data/pathway-exclusions.json` exists and carries the arcade class | **yes.** Site repo. `"excludedCategories": ["game"]`, ruled `2026-08-26, Order FC-Z, Z-D2`. |
| `signalEndpoint` non-empty | **no.** Empty, which is the supported single-player state. |

---

## §MTR-1 · PWA — **RULING: SHIPPED**

The registration at line 732 pointed at a `sw.js` that did not exist, and there
was no manifest and no `<link rel="manifest">` anywhere in the file. Because the
Install button unhides only on `beforeinstallprompt`, and Chromium does not fire
that without an installable manifest, **the button could never appear in any
version** — confirmed from the game file's own side, not taken from the order.

Landed:

```
Games/microtinkerer/index.html            the game
Games/microtinkerer/sw.js                 cache-first, versioned cache, skipWaiting OFF
Games/microtinkerer/manifest.webmanifest  name, 192/512 icons, standalone, #17151c
tools/microtinkerer/verify_pwa.mjs        the gate
tools/microtinkerer/run.sh                how to run it
tools/verify_games_hygiene.mjs            census widened — see below
```

`index.html` differs from the supplied v1.2.0 file by **exactly three lines**:
the manifest link, the version constant, and one `&` → `&amp;`. Nothing else was
touched.

**A subdirectory game escaped a gate, and that is now closed.**
`verify_games_hygiene.mjs` enumerated `Games/*.html` with a top-level
`readdirSync`, so the first game to need siblings was invisible to it. Measured,
not assumed: a probe copy placed where the gate *could* see it came back

```
FAIL  H2 Micro_Tinkerer…: no raw markup ampersands (1: <h2>Comfort & access</h2>)
```

— a real defect in the supplied file that would have shipped uncaught. The
ampersand is fixed, and the census now descends one level (`Games/vendor` holds
no `.html`, so nothing else is newly in scope). The gate goes from 90 gates over
30 files to **93 over 31**, the game is judged and passes all three, and
`--self-test` still reports `CAN-FAIL PROVEN`.

**Proof, both legs the order names:**

```
[PASS] service worker registration resolves · .../Games/microtinkerer/
[PASS] GET ./sw.js returns 200 on the served path
[PASS] the manifest fetches 200 and parses · HTTP 200
[PASS] every declared icon resolves 200
[PASS] the game boots on a first, online load
[PASS] a second load completes with the network offline
[PASS] the game BOOTS with the network offline
[PASS] the offline document was served by the service worker
15/15 passed
```

**A gate that cannot go red cannot be trusted when it goes green.** Three
controls, all run:

| control | result |
|---|---|
| v1.2.0 exactly as supplied (no `sw.js`) | exit **3 INCONCLUSIVE** — refuses to pass |
| a service worker that cannot install | exit **1**, naming the file |
| no site tree to resolve icons against | exit **3 INCONCLUSIVE**, not a silent skip |

The second control found a defect **in the gate**: an unraced
`await navigator.serviceWorker.ready` never settles when installation fails, so
the gate hung instead of naming the file. Fixed with a deadline before the gate
was committed — this repo's own rule, that a hang is worse than a failure.

**"An install button that appears but cannot install is worse than no button."**
That risk is structural, not incidental: the button ships with the HTML `hidden`
attribute and the one line that unhides it (L670) runs only on
`beforeinstallprompt`. The browser decides. The gate asserts the button is still
hidden after a normal load, so a regression that unhides it unconditionally
fails. The button's gate was not touched.

**Icons.** The manifest points at the four icons the site already serves
(`/assets/icons/app-icon-{192,512}.png` and the maskable pair). All four resolve
200 in the gate. No new binary was added to `Games/` — deliberately, given this
repo's single-file rule. Game-specific art is a swap whenever it exists.

**Departure from `CLAUDE.md` worth Matt's eye.** `Games/*.html` are single
self-contained files. Micro-Tinkerer's `index.html` still is one — it plays from
`file://`, and the service worker is guarded off there. But it now sits in a
directory with two siblings. `Games/vendor/` already establishes that sibling
files exist in this tree, and neither sibling is external: no CDN, no webfont, no
image. Say the word and it reverts to a flat file with the registration and the
button deleted instead, which is the other half of the order's ruling.

---

## §MTR-2 · Endpoint injection — **HELD**

No Worker is deployed, so there is no URL to inject and nothing to prove.
`signalEndpoint` stays `""`, which disables multiplayer cleanly — verified, not
assumed: L664 disables `#btn-host`, `#btn-join` and `#join-code`, and relabels
the host button to `Multiplayer not configured`.

Both proofs the order requires are still outstanding, and **neither is a
`/health` 200**:

1. `GET /health` returns `{"ok":true,…}`, **and**
2. a WebSocket upgrade to `/ws?mode=create` returns a `welcome` frame carrying a
   six-character room.

**The client protocol was checked against the supplied Worker** and they agree on
`welcome`, `msg`, `send`, `checkpoint`, `peer_join`, `host_migrate`,
`relay_unavailable`, `offer`/`answer`/`ice`. Two real defects in
`src/worker.js`, both small:

1. **`peer_left` is handled but never sent.** The host handles
   `p.kind==='peer_left'` by dropping that client, but nothing in the game or the
   Worker ever emits it. `departed()` broadcasts only on host departure. A guest
   leaving mid-round is invisible to signalling; the host finds out only when the
   peer connection state changes. Fix, in `departed()`, before the host check:
   ```js
   for (const p of remaining) this.post(p.ws, { t:'msg', from:'server', payload:{ kind:'peer_left', peer: gone } });
   ```
2. **A relay refusal can be swallowed.** In `webSocketMessage`, the
   `relay_unavailable` notice goes back to the **sender**, but it is gated on
   `if (target)` — the *recipient* existing. A sender addressing a peer that has
   left gets silence instead of a refusal. Drop the `socketFor`/`if (target)`
   pair; post the notice unconditionally.

Neither is fixed here: the Worker is not in any repository this session touches.

---

## §MTR-3 · Two-phone test — **UNMEASURED**

Not done, and not doable by this session. No limb above claims multiplayer works.

---

## §MTR-4 · The Games record — **PAYLOAD PROVEN, WRITE OUT OF SCOPE**

The canonical shelf is `MattRoper1977/Games/games.json`. This session can write
only `MattRoper1977/Lessons`. The record is therefore prepared and proven, not
committed.

**The FC-Z trap is real and is handled by class.** `pathway-exclusions.json`
excludes `"excludedCategories": ["game"]`, and the class is stamped by
`build_mbm_search_index.py` on every record read from the games manifest — so a
shelf record is in the arcade class by construction and cannot be text-matched
into a teaching pathway. Verified, not assumed: all 64 current `category: "game"`
entries carry `pathway: null`.

One correction to the order: `pathway-exclusions.json` records that **nine**
arcade records were already misfiled, and its own note anticipates "the tenth and
eleventh". Micro-Tinkerer would be the **tenth**, not the ninth.

**The record:**

```json
{
  "icon": "🔦",
  "title": "Micro-Tinkerer: The Giant's Study",
  "desc": "You are six centimetres tall on a teacher's desk, and the Mega Teacher is sweeping the room with a torch. Hide for forty-five seconds, then last out the hunt: the beam only catches what it actually falls on, and being caught fills a meter rather than ending your round, so getting back into cover saves you. Tip the angle lamp to blind the search, spill the PVA to slow it, ride the desk fan's updraft or topple a line of hardcovers into a bridge. In Battery Escape you recover three AA cells and fly out on the toy plane at the window. Plays offline.",
  "href": "/Lessons/Games/microtinkerer/index.html",
  "tag": "Hide & seek",
  "hue": "#FFD45B",
  "featured": false,
  "hero": false,
  "art": "/assets/cards/micro-tinkerer.svg"
}
```

Every field is a decision, not a default:

- `tag: "Hide & seek"` is an existing tag, so nothing is minted — and it takes
  that tag off the validator's single-use "check this was intended" list.
- `hero: false` is mandatory. Exactly one hero is enforced; Off-Brand holds it.
- `hue` is the game's own accent, `--gold: #ffd45b`.
- `collection` is omitted — the three in use (RPG, Shooter, Sports) do not fit.
- No `NEW ·` title prefix: that marker is a separate declared record and may only
  follow production, never lead it.
- Nothing is added to any curation set. `verify_new_games_uncurated.mjs` requires
  a newly-arrived game to hold no rail slot, take or badge — curation is earned.
- The description is written to the FC-R standard: what the player does and what
  the game does back, in the reader's words. Every clause is traceable to the
  artefact, and no internal plumbing appears — no latency, no draw loop, no
  physics tick. 551 characters, inside the shelf's current 556 maximum.

**Proof — the estate's own validator, run on the proposed 55-record shelf:**

```
proposed shelf, real Lessons tree : exit=0
  ok  exactly one hero — currently "Off-Brand"
  ok  no duplicate ids / slugs / titles / hrefs
  ok  every entry carries all required fields
  ok  30 Lessons href(s) resolve to real files in the Lessons tree
  ok  art present on all 55 entries
  PASS: games.json satisfies the manifest contract (55 entries)

CONTROL — same shelf, game file removed : exit=1
  FAIL: unresolvable href(s):
      "Micro-Tinkerer: The Giant's Study" -> missing target: /Lessons/Games/microtinkerer/index.html
```

The control matters: it proves the href leg is live *for this record*, so the
green above is not vacuous.

**Delta cap (Z-D2 §Z2.4) — measured:**

```
records before/after                 54 -> 55   (exactly one added)
pre-existing records byte-identical  54 of 54
title / strap unchanged              yes
formatting round-trip                json.dumps(ensure_ascii=False, indent=2) + newline — exact
```

**Two things must land before that record is written, and both are site-repo:**

1. **`/assets/cards/micro-tinkerer.svg` does not exist.** No check resolves `art`
   to a file — the only tool that touches it is a negative-control fixture — so
   CI will stay green and the card will render broken. This is the failure mode
   most likely to reach a visitor.
2. **A 55th `TAXONOMY` row in `games/index.html`.** The arcade page holds a
   hand-declared row per href, currently 54 rows against 54 records, exact
   parity. A shelf record with no row is a hard red, not a missing label.
   Proposed row:
   ```js
   {href:"/Lessons/Games/microtinkerer/index.html",          genre:"Action & Survival",feels:["thinky","quick-go"]},
   ```
   Both values are existing vocabulary, so nothing is minted: `feels` is a closed
   set of seven (`fast`, `quick-go`, `long-haul`, `thinky`, `gravity`, `calm`,
   `together`) and `Action & Survival` is an existing genre. `together` is
   deliberately omitted — it becomes apt the day multiplayer is switched on, not
   before.

So §MTR-4 is **coupled to §MTR-5's repository**, which the order treats as
independent. The shelf record cannot safely land ahead of the site change.

---

## §MTR-5 · Site publish — **SKIPPED-BY-GATE**

`CLICK_EFFECTIVE` is **NOT-DONE**, so this section does not open. Per §XC2, the
gate is reported with the workflow hash as proof:

```
gate            CLICK_EFFECTIVE = NOT-DONE
workflow        mattroper1977.github.io/.github/workflows/agx1-live-verify.yml
bytes           20047        (matches the order's before-image exactly)
sha256          50702afefaff149767ec77b88440554c4b363d350943c6b6c412bf7b2d6ce6b3
job             "Fetch the live estate and compare to raw-at-SHA"   (line 32)
step            "Shelf mirror equals the served canonical, byte for byte"  (line 255)
status          SKIPPED-BY-GATE
```

A green site PR while the click is outstanding would be a finding about the
check, not permission to merge.

**The hud.js declination — the register was located.** It is
`mattroper1977.github.io/data/hud-coverage.json`, and its `excluded` list holds
**exactly twelve** entries, matching the order's count. Not MEASUREMENT INVALID.

The declination is warranted on measurement, not assertion: the game requests
**pointer lock** on canvas click, renders through **WebGL2 with a WebGL1
fallback** and a custom post-processing chain, and its own `#hud` is
`position:fixed; inset:0` — it already occupies exactly the region an injected
`hud.js` would claim. Entry, ready to add as the thirteenth:

```json
{
  "route": "/Lessons/Games/microtinkerer/index.html",
  "verifier": "tools/microtinkerer/verify_pwa.mjs",
  "gates": ["offline: the game boots from its own service worker with the network down"],
  "note": "Full-screen WebGL with pointer lock and its own inset:0 HUD. The injected control bar would fight both the lock and the HUD's own region. Declared-declined on the same basis as the 2026-08-10 twelve; the consequence is the status quo for this game, not a regression."
}
```

Not written: it is a site-repo file, and §MTR-5 is held.

Untouched and not re-raised, as instructed: the `/games/` 44px exemption, the R4
discovery-route line, R7 (no hand-editing generated output), routes-serve-200.
Note for whoever opens §MTR-5: the estate has **no numbered R1–R7 list** on disk
— only citations by number — and `/games/` is **not** in the routes-serve-200
route set today.

---

## §MTR-6 · Copy Matt owns — **REPORT-ONLY, NOT COMPOSED**

Neither sentence was written. Same rule that closed Section 19: composing them to
unblock a section is the failure, not the fix.

1. The framing line for a game about hiding from a hunting teacher, sitting
   beside SEMH resources under Matt's name.
2. The page-level plain-English multiplayer note.

**One thing sentence 2 must not inherit.** The v1.2.0 footer — the miniature the
order points at — reads *"no … external runtime dependencies"* and says
multiplayer *"contacts a small server"*. Multiplayer also contacts **two
third-party STUN hosts**, `stun.cloudflare.com` and `stun.l.google.com`
(line 598), which that sentence does not mention. In the shipped state the claim
is true, because multiplayer is off and nothing is contacted. The moment an
endpoint is set it is incomplete — and it is exactly the sentence the ICO
children's-code note in §5.2 turns on. Worth a phrase, not a rewrite.

---

## §MTR-7 · Close

Four items, and no fifth:

1. **The Cloudflare deploy clicks.** No Worker exists. §MTR-2 and §MTR-3 are held
   behind this.
2. **The relay decision** (§4): public with relay off, a second school-only
   Worker with `RELAY: "on"`, or single-player public only.
3. **The TURN decision** (§7): without it, a minority behind symmetric NAT will
   not connect.
4. **The two sentences** in §MTR-6.

### Raised by this run, outside the order

- **Fact 1 of §MTR-0 is false** — no repository in the estate is ruleset-protected,
  and the clicks that would make it so are still on Matt's list.
- **The mirror leg is red for a second reason** the deploy click will not fix:
  the shelf mirror is six descriptions behind the canonical.
- **§MTR-4 is coupled to §MTR-5's repository** via card art and the TAXONOMY row.
- **Two Worker defects**, both with one-line fixes (§MTR-2).
- **The version constant read `1.1.0`** in a file named v1_2_0, and it is that
  constant, not the build record, that renders in the footer. Fixed here — it is
  read in three places and compared in none, so the change is cosmetic.
- **`verify_games_hygiene.mjs` could not see a game in a subdirectory.** Closed,
  with the defect it would have caught fixed in the same commit.
- **"Label as such" is thinner on a phone than it reads.** With no endpoint, only
  `#btn-host` gains visible text. `#btn-join` still reads "Join LAN" and the code
  box still says "ROOM CODE"; their only explanation is a `title` tooltip, which
  does not surface on touch — the primary target. Two greyed controls with no
  stated reason. Not changed; it is a copy decision.
