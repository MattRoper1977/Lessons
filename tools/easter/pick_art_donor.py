#!/usr/bin/env python3
"""A3N-2 s1a -- pick the chassis donor for Art, by measured gate margin.

WHY THIS TOOL EXISTS
--------------------
Art has 71 plans in EASTER_TARGETS.json, 19 of them cover-taught, and no
gate-readable deck of its own. Every Art deck in the estate is one of two
shapes, and a control below asserts it rather than assuming it:

  * an 11-stage classic deck with no `id="lesson-config"` (Art_Teesside/*,
    *_Estate_v3/Art_Teesside/*), so the week is not readable and g19/g16 have
    nothing to bind to;
  * a 9-stage OUTSTANDING_V3 Spring2 deck, which has per-stage data-min but
    still no lesson-config and no guide toggle.

"No Art family has a gate-readable donor" is therefore true. s1 rules it a
solvable authoring task: strip a green deck from ANOTHER family down to its
chassis and author Art onto that.

THE CHASSIS SIGNATURE IS DERIVED, NOT LISTED
--------------------------------------------
A hand-written list of "what a chassis must have" is a list of what the author
remembered. The first revision of this tool carried one, and it was wrong in
four places at once: it looked for `hud.js` (in 524 files in this estate and in
NOT ONE deck that has passed the full stack this campaign), for `tier-1..3`
(this estate names its print tiers supported/standard/stretch), for a
`running-head` class that only some decks carry, and it applied g26 as a hard
filter when g26 is scope=new and does not bind a live deck at all. It returned
ZERO candidates from a corpus of 136 and the zero looked like a finding.

So the signature is now INTERSECTED from a reference set of decks that have
been through the whole gate stack green -- classes, ids and data-attributes
present in EVERY one of them. What every green deck has is the chassis; what
only some have is that deck's furniture. The reference set is a file with a
recorded digest, not a list typed into this source.

WHAT "MARGIN" MEANS HERE, AND WHAT IT DOES NOT
----------------------------------------------
s1a says "nearest-green ... chosen by measured gate margin". Stated plainly so
it can be argued with: the margin below ranks a deck by how comfortably it
clears the gates AS SHIPPED. Most of that headroom is a property of its
CONTENT, and s1b strips every word of content out. The margin is therefore a
PROXY -- a deck that clears the gates comfortably was built on furniture the
gates can read -- and the inference is indirect. It is not hidden here, and it
is not the filter. The filter is the derived signature above, which is the part
that survives the strip.

PATHWAY IS NOT COSMETIC. g26 derives the pathway from the ROUTE and reds a deck
whose pupil Flesch-Kincaid sits outside that pathway's band. A single
pathway-neutral chassis would make g26 return NOT-APPLICABLE -- a fail-open on
the one gate that reads the pupil register. So this picks one donor PER
PATHWAY, and a donor route must carry `/BUILD_`, `/GROW_` or `/LAUNCH_`.

    python3 tools/easter/pick_art_donor.py --reference <file>
    python3 tools/easter/pick_art_donor.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

VERSION = "pick-art-donor-v2.0.0-signature-derived"
ROOT = Path(__file__).resolve().parents[2]
PATHWAYS = ("BUILD", "GROW", "LAUNCH")
DEFAULT_REFERENCE = ROOT / "tools/easter/GREEN_REFERENCE_DECKS.json"
SKIP_DIRS = {".git", "node_modules", "vendor", "audit-output", "tools/fixtures"}


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


stages = _load("lesson_stages", "_sownb/vb/tools/lesson_stages.py")
g18 = _load("g18_v2_family_floor", "_sownb/vb/tools/g18_v2_family_floor.py")
g26 = _load("g26_reading_band", "_sownb/vb/tools/g26_reading_band.py")
feb = _load("g18_measurement", "_sownb/feb/tools/g18_measurement.py")


def digest(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _rel(path) -> str:
    p = Path(path).resolve()
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


# --------------------------------------------------------------------------
# the signature, intersected from decks known green
# --------------------------------------------------------------------------
def markers_of(raw: str) -> set:
    out = set()
    for m in re.finditer(r'class="([^"]+)"', raw):
        out.update("." + t for t in m.group(1).split())
    out.update("#" + i for i in re.findall(r'id="([^"]+)"', raw))
    out.update(re.findall(r"\s(data-[a-z0-9\-]+)=", raw))
    return out


# WHAT THE STRIP SUPPLIES, AND WHAT THE DONOR MUST ALREADY HAVE.
#
# Order A3N-3 §2. The first filter required a lesson-config of every candidate,
# and that dropped every one of the estate's forty-two nine-stage Art decks --
# the whole reason "no Art family has a gate-readable donor" was ever written
# down. It was the wrong requirement: strip_to_chassis WRITES a fresh
# lesson-config into the chassis, so needing one in the donor asked for
# something the pipeline supplies for itself.
#
# The distinction is derivable rather than listed: a marker belongs here when
# strip_to_chassis puts it into the chassis regardless of the donor. Everything
# else is furniture the strip preserves and cannot invent, so the donor must
# carry it -- and a deck lacking THOSE is excluded for a reason that is true of
# the deck, not an artifact of how the filter was written.
SUPPLIED_BY_STRIP = {"#lesson-config"}


def signature(reference_paths: list[str]) -> set:
    common = None
    for rel in reference_paths:
        s = markers_of((ROOT / rel).read_text(encoding="utf-8", errors="replace"))
        common = s if common is None else (common & s)
    if not common:
        raise SystemExit("SIGNATURE INVALID: the reference decks share no markers")
    return common


def has_signature(raw: str, sig: set) -> tuple[bool, list]:
    """Missing markers, split into what matters and what the strip supplies."""
    have = markers_of(raw)
    missing = sorted((sig - have) - SUPPLIED_BY_STRIP)
    return (not missing), missing


def missing_all(raw: str, sig: set) -> list:
    """Every marker absent, including the ones the strip supplies, so the report
    can show the whole picture rather than only the part that counts."""
    return sorted(sig - markers_of(raw))


# --------------------------------------------------------------------------
# family, derived from the route and cross-checked against FEB
# --------------------------------------------------------------------------
SUBJECTS = (("ASDAN", "ASDAN"), ("SCIENCE", "Science"), ("SCI_", "Science"),
            ("HUMANITIES", "Humanities"), ("HUM_", "Humanities"), ("ART", "Art"))


def family_of(rel: str) -> str | None:
    pw = g26.pathway_of("/" + rel)
    if pw is None:
        return None
    u = rel.upper()
    for token, subject in SUBJECTS:
        if token in u:
            return f"{pw} {subject}"
    return None


def feb_family_of(rel: str) -> str | None:
    for family, patterns in feb.BASELINES.items():
        for pattern in patterns:
            if any(_rel(p) == rel for p in ROOT.glob(pattern)):
                return family
    return None


# --------------------------------------------------------------------------
DECK_SHAPED = ('class="deck"', 'class="deck ', 'id="lessonDeck"', "slide-container")


def corpus(sig: set) -> list[dict]:
    """EVERY deck-shaped file, with the reason it was dropped if it was.

    A3N-3 §2: a selector that narrows a candidate set must print its exclusions
    with reasons BEFORE the set is used. The first version returned only the
    files that survived, so the forty-two nine-stage Art decks it dropped were
    invisible and "no Art family has a gate-readable donor" read as a finding
    rather than as a filter artifact.

    Measurement still stops at the first disqualifying marker, because
    stages.measure costs about two seconds a deck and there are six hundred of
    them. That is a stated bound, not a silent one: every row says how far it
    got, so a row with `measured: false` is a row nobody has weighed rather than
    a row that failed.
    """
    out = []
    for path in sorted(ROOT.rglob("*.html")):
        rel = _rel(path)
        if any(rel == d or rel.startswith(d + "/") for d in SKIP_DIRS):
            continue
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if not any(t in raw for t in DECK_SHAPED):
            continue
        ok, missing = has_signature(raw, sig)
        out.append({"file": rel, "signatureComplete": ok,
                    "signatureMissing": missing,
                    "missingIncludingSuppliedByStrip": missing_all(raw, sig),
                    "measured": ok})
    return out


def measure_candidate(rel: str) -> dict:
    path = ROOT / rel
    raw = path.read_text(encoding="utf-8", errors="replace")
    fam = family_of(rel)
    row = {"file": rel, "family": fam, "febFamily": feb_family_of(rel),
           "pathway": g26.pathway_of("/" + rel), "sha256": digest(path)}
    m = stages.measure(path)
    row.update(stageCount=m["stageCount"], contentWords=m["contentWords"],
               chromeWords=m["chromeWords"], shell=m["shell"])
    row["dataMin"] = len(re.findall(r"data-min=", raw))
    row["rootBlocks"] = raw.count(":root")

    scored_as = row["febFamily"] or fam
    g18row = g18.score(rel, scored_as)
    floor = g18row["bindingFloor"]
    row["g18"] = {"words": g18row["candidateWords"], "floor": floor,
                  "floorSource": g18row["bindingFloorSource"],
                  "verdict": g18row["bindingVerdict"],
                  "thin": len(g18row["thinSlides"])}
    row["marginFloor"] = round((g18row["candidateWords"] - floor) / floor, 3) if floor else None

    bnds, scope_new, modes = g26.bands()
    m26 = g26.measure(path)
    j26 = g26.judge(m26, bnds, row["pathway"], modes)
    lo, hi = bnds.get(row["pathway"], (None, None))
    fkv = m26.get("pupilFK")
    row["g26"] = {"pupilFK": fkv, "band": [lo, hi], "verdict": j26["verdict"],
                  "scopeNew": scope_new, "binding": False}
    row["marginBand"] = round((hi - fkv) / hi, 3) if (fkv is not None and hi) else None
    return row


def margin(row: dict):
    """The binding margin is the WORST of the measured margins, because a deck
    is only as green as its nearest red. A None margin is not infinite headroom
    -- it disqualifies the row."""
    parts = [row.get("marginFloor"), row.get("marginBand")]
    if any(p is None for p in parts):
        return None
    return min(parts)


def is_candidate(row: dict) -> tuple[bool, list]:
    """Every exclusion carries a reason, and the reasons are facts about the
    file. A3N-3 §2: a selector that narrows a set must print what it dropped."""
    why = []
    for m in row.get("signatureMissing", []):
        why.append(f"no {m} (furniture the strip preserves and cannot invent)")
    if row["stageCount"] != 9:
        why.append(f"{row['stageCount']} stages, not 9")
    if row["dataMin"] < row["stageCount"]:
        why.append(f"data-min on {row['dataMin']} of {row['stageCount']} stages")
    if row["rootBlocks"] != 1:
        why.append(f"{row['rootBlocks']} :root blocks")
    if row["pathway"] is None:
        why.append("pathway not derivable from route")
    if row["g18"]["verdict"] != "PASS":
        why.append(f"g18 RED ({row['g18']['words']}w vs floor {row['g18']['floor']})")
    if margin(row) is None:
        why.append("a margin could not be measured")
    return (not why), why


def pick(reference_paths: list[str]) -> dict:
    sig = signature(reference_paths)
    scanned = corpus(sig)
    rows = []
    for entry in scanned:
        if not entry["measured"]:
            rows.append({**entry, "candidate": False,
                         "excludedBecause": [
                             f"no {m} (furniture the strip preserves and cannot invent)"
                             for m in entry["signatureMissing"]]})
            continue
        r = measure_candidate(entry["file"])
        r.update(entry)
        ok, why = is_candidate(r)
        r["candidate"], r["excludedBecause"], r["margin"] = ok, why, margin(r)
        rows.append(r)
    chosen = {}
    for pw in PATHWAYS:
        pool = [r for r in rows if r.get("candidate") and r.get("pathway") == pw]
        pool.sort(key=lambda r: (-r["margin"], r["file"]))
        chosen[pw] = {
            "pick": pool[0] if pool else None,
            "poolSize": len(pool),
            "runnersUp": [{"file": r["file"], "family": r["family"],
                           "margin": r["margin"], "marginFloor": r["marginFloor"],
                           "marginBand": r["marginBand"]} for r in pool[1:4]]}
    excluded = [r for r in rows if not r.get("candidate")]
    return {"tool": VERSION, "signature": sorted(sig),
            "signatureSize": len(sig),
            "suppliedByStrip": sorted(SUPPLIED_BY_STRIP),
            "reference": reference_paths,
            "deckShapedScanned": len(scanned),
            "signatureComplete": sum(1 for r in scanned if r["signatureComplete"]),
            "candidates": sum(1 for r in rows if r.get("candidate")),
            "excludedCount": len(excluded),
            "chosen": chosen, "rows": rows}


# --------------------------------------------------------------------------
def controls(reference_paths: list[str] | None = None) -> list[dict]:
    out = []
    ref = reference_paths or json.loads(DEFAULT_REFERENCE.read_text())["decks"]

    def rec(cid, claim, expect, actual):
        out.append({"id": cid, "claim": claim, "expected": expect, "actual": actual,
                    "verdict": "PASS" if expect == actual else "RED"})

    sig = signature(ref)

    rec("margin-is-the-worst-gate-not-the-mean",
        "a deck at 0.01 on one gate ranks below a deck at 0.30 on both",
        True, margin({"marginFloor": 2.0, "marginBand": 0.01})
        < margin({"marginFloor": 0.30, "marginBand": 0.30}))

    rec("an-unmeasured-margin-disqualifies",
        "a row with a None margin returns None, not a number",
        None, margin({"marginFloor": 0.5, "marginBand": None}))

    rec("pathway-comes-off-the-route",
        "tools/donors/ART_DONOR_v1/LAUNCH_chassis.html reads as LAUNCH",
        "LAUNCH", g26.pathway_of("/tools/donors/ART_DONOR_v1/LAUNCH_chassis.html"))
    rec("a-pathway-neutral-route-is-not-silently-accepted",
        "a route with no pathway token returns None, which excludes the row",
        None, g26.pathway_of("/tools/donors/ART_DONOR_v1/chassis.html"))

    # The signature must be DERIVED and must actually bite. Removing any one
    # marker from a real green deck must make that deck fail the signature --
    # otherwise the marker is decoration in the intersection.
    probe = ROOT / ref[0]
    raw = probe.read_text(encoding="utf-8", errors="replace")
    rec("a-reference-deck-matches-the-signature-it-helped-derive",
        f"{Path(ref[0]).name} carries every marker in the intersection",
        True, has_signature(raw, sig)[0])
    # Seeded on a marker the STRIP DOES NOT SUPPLY, because #lesson-config is
    # now excused -- and excusing it is the whole repair, so the control has to
    # test the part that still bites.
    broken = raw.replace('id="n6m-guide-js"', 'id="n6m-guide-j5"')
    rec("the-signature-fires-when-a-marker-is-removed",
        "a deck missing the guide toggle fails the signature; the guide toggle is "
        "furniture the strip preserves and cannot invent",
        (False, ["#n6m-guide-js"]), has_signature(broken, sig))
    rec("the-marker-the-strip-supplies-is-not-required-of-a-donor",
        "a deck with no lesson-config is NOT excluded for that alone; "
        "strip_to_chassis writes one",
        True, "#lesson-config" not in has_signature(
            raw.replace('id="lesson-config"', 'id="lesson-conf1g"'), sig)[1])

    # The four things v1 got wrong, pinned so they cannot come back.
    rec("hud-js-is-not-part-of-this-chassis",
        "no deck in the reference set loads hud.js, so it is not a chassis marker",
        0, sum(1 for r in ref
               if "hud.js" in (ROOT / r).read_text(encoding="utf-8", errors="replace")))
    rec("g26-is-scope-new-and-does-not-bind-a-live-deck",
        "the contract scopes the reading band to new work",
        True, g26.bands()[1])

    # THE PREMISE s1 RESTS ON, restated once it stopped being true.
    #
    # This control used to read "zero Art decks carry a lesson-config". That was
    # measured and correct when the donor was chosen, and batch 3 then authored
    # gate-readable Art decks and turned it red -- correctly. A control that
    # goes red because the work succeeded is not a control, it is a countdown.
    # The durable claim is the one underneath it: every gate-readable Art deck
    # in this estate is one THIS campaign authored, and so still no PRE-EXISTING
    # Art deck could have served as the donor.
    art = sorted(ROOT.glob("Art_Teesside/**/*.html")) + \
        sorted(ROOT.glob("*_Estate_v3/Art_Teesside/*.html"))
    readable = [p for p in art if 'id="lesson-config"'
                in p.read_text(encoding="utf-8", errors="replace")]
    inherited = [_rel(p) for p in readable
                 if '"planId"' not in p.read_text(encoding="utf-8", errors="replace")]
    rec("no-art-deck-this-campaign-did-not-write-is-gate-readable",
        "every gate-readable Art deck carries a planId, so none pre-dates this work",
        [], inherited)

    # Route-derived family must agree with FEB wherever FEB has an opinion.
    disagree = []
    for family, patterns in feb.BASELINES.items():
        for pattern in patterns:
            for p in ROOT.glob(pattern):
                rel = _rel(p)
                mine = family_of(rel)
                if mine is not None and mine != family:
                    disagree.append((rel, mine, family))
    # THE MUST-NOT-EXCLUDE CONTROL, Order A3N-3 §2, naming the eighteen.
    #
    # The Spring2 OUTSTANDING_V3 Art decks -- six per pathway -- are the decks
    # the first filter dropped, and dropping them is what made "no Art family
    # has a gate-readable donor" look true. They are named here by path so that
    # no future edit can exclude them again without this control saying so, and
    # so that whatever reason IS given for them has to be a fact about the file.
    eighteen = sorted(_rel(q) for q in ROOT.glob(
        "Art_Teesside/*/Spring2_2026-27/*_OUTSTANDING_V3.html"))
    bad = []
    for relp in eighteen:
        raw = (ROOT / relp).read_text(encoding="utf-8", errors="replace")
        _ok, miss = has_signature(raw, sig)
        # Not an artifact: every reason given must be a marker the file really
        # lacks, and must not be one the strip supplies for itself.
        for m in miss:
            if m in SUPPLIED_BY_STRIP:
                bad.append((relp, f"excluded for {m}, which the strip supplies"))
            elif m in markers_of(raw):
                bad.append((relp, f"excluded for {m}, which the file has"))
    rec("the-eighteen-spring2-art-decks-are-never-excluded-by-an-artifact",
        f"each of the {len(eighteen)} OUTSTANDING_V3 Art decks is dropped only for "
        f"furniture it genuinely lacks and the strip cannot invent",
        (18, []), (len(eighteen), bad[:4]))

    rec("route-derived-family-agrees-with-feb-where-feb-has-an-opinion",
        "no deck in a FEB baseline pattern is given a different family here",
        [], disagree[:5])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference", default=str(DEFAULT_REFERENCE))
    ap.add_argument("--output")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--show-excluded", type=int, default=0)
    a = ap.parse_args()

    ref_file = Path(a.reference)
    if not ref_file.is_file():
        raise SystemExit(f"PROVENANCE REFUSAL: reference set {a.reference!r} is not a "
                         f"readable file. Every input must be traceable to a digest.")
    ref_doc = json.loads(ref_file.read_text())
    ref = ref_doc["decks"]

    if a.list_controls:
        for c in controls(ref):
            print(c["id"])
        return 0
    if a.self_test:
        cs = controls(ref)
        for c in cs:
            print(f"{c['verdict']:4s} {c['id']}: {c['claim']}")
            if c["verdict"] == "RED":
                print(f"       expected {c['expected']!r} got {c['actual']!r}")
        red = [c for c in cs if c["verdict"] == "RED"]
        print(f"{len(cs) - len(red)}/{len(cs)} controls PASS")
        return 1 if red else 0

    res = pick(ref)
    res["referenceFile"] = {"path": str(ref_file), "sha256": digest(ref_file)}
    print(f"{res['tool']}  signature {res['signatureSize']} markers from "
          f"{len(ref)} green reference decks "
          f"({len(res['suppliedByStrip'])} of them supplied by the strip and so "
          f"not required of a donor: {', '.join(res['suppliedByStrip'])})")
    print(f"reference {ref_file}  sha256 {res['referenceFile']['sha256'][:16]}")
    print(f"deck-shaped files scanned {res['deckShapedScanned']}, "
          f"signature-complete {res['signatureComplete']}, "
          f"candidates {res['candidates']}, excluded {res['excludedCount']}\n")
    for pw in PATHWAYS:
        c = res["chosen"][pw]
        print(f"--- {pw} ({c['poolSize']} candidates) ---")
        p = c["pick"]
        if p is None:
            print("    NO CANDIDATE")
            continue
        print(f"    PICK  {p['file']}")
        print(f"          family {p['family']}  margin {p['margin']}  "
              f"(floor {p['marginFloor']}, band {p['marginBand']})")
        print(f"          g18 {p['g18']['words']}w vs floor {p['g18']['floor']} "
              f"[{p['g18']['floorSource']}]")
        print(f"          g26 pupil FK {p['g26']['pupilFK']} in band {p['g26']['band']}"
              f"  stages {p['stageCount']}  data-min {p['dataMin']}  :root {p['rootBlocks']}")
        print(f"          sha256 {p['sha256'][:16]}")
        for r in c["runnersUp"]:
            print(f"    next  {r['margin']:.3f}  {r['file']}")
        print()
    # EVERY EXCLUSION, WITH ITS REASON, BEFORE THE SET IS USED (A3N-3 §2).
    ex = [x for x in res["rows"] if not x.get("candidate")]
    shown = ex if a.show_excluded in (0, None) else ex[:a.show_excluded]
    print(f"--- excluded, {len(ex)} of {res['deckShapedScanned']} deck-shaped files ---")
    for r in shown:
        print(f"    {r['file']}")
        for w in r["excludedBecause"]:
            print(f"        -> {w}")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\nwrote {a.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
