#!/usr/bin/env python3
"""Plant a violation of every classic-v2 contract clause, show it fires, withdraw it.

TWO FIXTURES, BECAUSE THE CONTRACT NOW ADMITS TWO SHAPES (v1.1.0, ruled 2026-09-22).
A clause with two routes and one fixture is a clause with one route tested. The
battery therefore runs whole against a v1 deck -- one that carries its own Lundy
slide -- and again against a v2 deck, one ORDER HUM-T has transplanted, where the
loop lives in a panel on every stage the pupil works in. Both are REAL LANDED DECKS.

A contract nobody has seen fail is a list of sentences. This runs each clause in
reshell_classic_v2_contract.py against a deck that satisfies every clause, then
against the same deck with exactly one clause broken, and requires the verdict to
move. A clause that cannot be made to red has not been tested; a clause that reds
the good deck too is not specific and is reported separately.

THE BASE IS A REAL DECK, NOT A FIXTURE. It is the landed
BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html with its stage timings restored
-- the one clause it genuinely fails, because #271's reshell dropped nine
data-min values that summed to 40. Building the base from an invented fixture
would test the fixture. Building it from the real deck means every clause is
exercised against markup the estate actually ships.

DETERMINISM. --self-test runs the whole battery twice and compares the two
reports byte for byte. Nothing here may depend on a clock, a temp-file name, a
dict ordering or the order of a glob.

Usage:
  classic_v2_contract_selftest.py --self-test [--output report.json]
  classic_v2_contract_selftest.py --list-controls
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VERSION = "classic-v2-contract-selftest-v1.2.0"

_spec = importlib.util.spec_from_file_location(
    "contract", ROOT / "_sownb/vb/tools/reshell_classic_v2_contract.py")
contract = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(contract)

# THE TWO FIXTURES. v1 still carries its own Lundy slide; v2 is a deck the order
# transplanted, which carries none and panels every stage the pupil works in.
# THE v1 FIXTURE IS A SNAPSHOT, AND WHY (v1.2.0, ruled 2026-09-22, STOP-T5).
# ORDER HUM-T transplants W16 as batch 6b, which takes the v1 shape off the last deck
# that carried it: measured across the estate, 54 decks are recipe-shaped, 25 still have
# their own Lundy slide, and only W16 reaches 9/10 -- the rest red on lesson-config, on a
# missing working stage, and on timings no revision of theirs ever carried. With W16
# transplanted the v1 route had no base at all and this file refused outright.
# So the v1 base is the BYTES THE ESTATE SHIPPED for W16, snapshotted at the commit named
# below. It is not an invented fixture: every byte was served, and the claim is auditable --
#     git show <bytesFrom.commit>:<bytesFrom.deck> | sha256sum
# must equal the recorded digest, which --rebase verifies against git and every run checks.
# Freezing the live lesson as a fixture was refused; so was retiring the route.
V1_DECK = "Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html"
V1_FIXTURE = "_sownb/vb/evidence/a2r/fixtures/classic_v2_v1_base.html"
V1_BYTES_COMMIT = "cdc14919efc819ed56b3c2cdd97a0c567fd96e79"
FIXTURES = (
    ("v1", V1_FIXTURE),
    ("v2", "Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W3_Places_In_My_Community.html"),
)
# A fixture that is a snapshot takes its minutes from the deck the bytes came from; its own
# path has no history to walk. The minutes stay KEYED TO THE FIXTURE, as ruled.
MINUTES_DECK = {V1_FIXTURE: V1_DECK}
SNAPSHOT_OF = {V1_FIXTURE: (V1_DECK, V1_BYTES_COMMIT)}
MINUTES_RECORD = ROOT / "_sownb/vb/evidence/a2r/classic_v2_fixture_minutes.json"
SLIDE_RX = re.compile(r'<div class="slide(?: active)?"')


# THE TIMINGS ARE MEASURED, NOT TYPED. Until v1.1.0 this file carried the ten
# minutes as a literal, which is a fixture asserting itself: nothing checked that
# the numbers were ever the lesson's. They are read instead from the newest
# revision of THE DECK ITSELF that still carried them -- the revision before
# #271's reshell dropped them -- and recorded with the commit they came from, so
# the claim can be audited against git rather than believed.
def measure_minutes(rel: str) -> dict:
    """Walk the deck's own history for the last revision whose stage minutes
    still summed to the period. Refuses rather than inventing a table."""
    log = subprocess.run(["git", "log", "--format=%H", "--", rel], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout.split()
    for sha in log:
        blob = subprocess.run(["git", "show", f"{sha}:{rel}"], cwd=ROOT,
                              capture_output=True, text=True).stdout
        mins = [int(m) for m in re.findall(r'data-min="(\d+)"', blob)]
        if mins and sum(mins) == contract.PERIOD_MINUTES:
            subject = subprocess.run(["git", "log", "-1", "--format=%s", sha], cwd=ROOT,
                                     capture_output=True, text=True, check=True).stdout.strip()
            return {"sourceCommit": sha, "sourceSubject": subject,
                    "minutes": mins, "sum": sum(mins)}
    raise SystemExit(f"REFUSED: no revision of {rel} carries stage minutes summing to "
                     f"{contract.PERIOD_MINUTES}; a fixture may not invent them")


def snapshot_provenance(rel: str) -> dict:
    """Record where a snapshot fixture's bytes came from, CHECKED AGAINST GIT.

    The commit is not taken on trust: the blob at that commit is read back and must equal
    the fixture byte for byte, or the record is refused rather than written."""
    deck, commit = SNAPSHOT_OF[rel]
    blob = subprocess.run(["git", "show", f"{commit}:{deck}"], cwd=ROOT,
                          capture_output=True, check=True).stdout
    raw = (ROOT / rel).read_bytes()
    if blob != raw:
        raise SystemExit(f"REFUSED: {rel} is not the bytes of {deck} at {commit[:12]}")
    return {"deck": deck, "commit": commit,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "derivation": f"git show {commit}:{deck} | sha256sum"}


def rebase_record() -> dict:
    fixtures = {}
    for _, rel in FIXTURES:
        rec = measure_minutes(MINUTES_DECK.get(rel, rel))
        rec["minutesDeck"] = MINUTES_DECK.get(rel, rel)
        if rel in SNAPSHOT_OF:
            rec["bytesFrom"] = snapshot_provenance(rel)
        fixtures[rel] = rec
    record = {"tool": "classic_v2_contract_selftest.py --rebase",
              "period": contract.PERIOD_MINUTES,
              "note": ("each fixture's stage minutes, read from the newest revision of the deck "
                       "they belong to that still carried them; #271's reshell dropped them. A "
                       "snapshot fixture also records the commit its bytes came from, verified "
                       "against git when this record is written and checked on every run."),
              "fixtures": fixtures}
    MINUTES_RECORD.parent.mkdir(parents=True, exist_ok=True)
    MINUTES_RECORD.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n",
                              encoding="utf-8")
    return record


def load_minutes(rel: str) -> dict:
    if not MINUTES_RECORD.exists():
        raise SystemExit(f"REFUSED: {MINUTES_RECORD.name} is absent; run --rebase")
    rec = json.loads(MINUTES_RECORD.read_text())["fixtures"].get(rel)
    if not rec:
        raise SystemExit(f"REFUSED: {MINUTES_RECORD.name} carries no minutes for {rel}")
    if rec["sum"] != contract.PERIOD_MINUTES or sum(rec["minutes"]) != contract.PERIOD_MINUTES:
        raise SystemExit(f"REFUSED: recorded minutes for {rel} do not sum to the period")
    return rec


def fixture_integrity(rel: str, raw: str = None, prov: dict = None):
    """(ok, detail) for a fixture's bytes against their recorded digest.

    A live deck has no recorded digest and is its own authority; a SNAPSHOT has one, and if
    the bytes and the record disagree the fixture is no longer the thing it claims to be."""
    if prov is None:
        prov = load_minutes(rel).get("bytesFrom")
    if not prov:
        return True, "live deck, no recorded digest"
    if raw is None:
        raw = (ROOT / rel).read_text(encoding="utf-8")
    got = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return got == prov["sha256"], f"sha256 {got[:16]} vs recorded {prov['sha256'][:16]}"


def _stamp(raw: str, minutes) -> str:
    it = iter(minutes)

    def stamp(m):
        try:
            return m.group(0) + f' data-min="{next(it)}"'
        except StopIteration:
            return m.group(0)

    return SLIDE_RX.sub(stamp, raw)


def _passing_base(rel: str, minutes=None) -> str:
    """The real deck with its measured timings restored: every clause must pass.

    A classic shell carries one slide more than the n6 it was built from -- the
    title slide, which takes no teaching minutes -- so the measured table is
    padded with leading zeros to the deck's own slide count. The padding is
    derived from the deck, never typed, and zeros cannot move the sum."""
    raw = (ROOT / rel).read_text(encoding="utf-8")
    mins = list(load_minutes(rel)["minutes"] if minutes is None else minutes)
    pad = len(SLIDE_RX.findall(raw)) - len(mins)
    if pad < 0:
        raise SystemExit(f"REFUSED: {rel} has fewer slides than its recorded minutes")
    return _stamp(raw, [0] * pad + mins)


# Each mutation breaks exactly one clause. The mutation is a function so that a
# clause whose violation needs more than a string swap can still be expressed.
def _break_own_config(raw):
    return raw.replace('id="lesson-config"', 'id="lesson-config-removed"', 1)


def _break_donor_head(raw):
    """One running head names another lesson.

    THE HEAD IS FOUND, NOT TYPED. Until v1.1.0 this mutation searched for one
    fixture's own running head as a literal, so on any other deck it replaced
    nothing at all and the control reported PASS -> PASS. The second fixture found
    that on its first run -- exactly the way _break_surfaces was found to be doing
    nothing. A mutation that cannot fire is a clause that is not tested."""
    from lxml import html as _lh
    tree = _lh.fromstring(raw)
    heads = tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," print-head ")]')
    if not heads:
        raise SystemExit("REFUSED: the fixture carries no running head to mutate")
    head = heads[0]
    for child in list(head):
        head.remove(child)
    head.text = "BUILD Humanities · Week 99 · a lesson this deck is not"
    return _lh.tostring(tree, encoding="unicode", doctype="<!DOCTYPE html>")


def _break_two_modals(raw):
    return raw.replace('id="mbmTA"', 'id="mbmTA"', 1).replace(
        "</body>", '<div id="mbmTA"></div></body>', 1)


def _break_hud(raw):
    return raw.replace("hud.js", "hud-REMOVED.js")


def _break_lundy(raw):
    out = raw.replace('data-title="Lundy Loop"', 'data-title="Reflection"')
    out = out.replace('id="print-lundy"', 'id="print-reflection"')
    for word in ("Space", "Voice", "Audience", "Influence",
                 "space", "voice", "audience", "influence"):
        out = out.replace(word, "Aspect" if word[0].isupper() else "aspect")
    return out


def _break_tiers(raw):
    return raw.replace('id="print-scaffold-stretch"', 'id="print-scaffold-extra"').replace(
        'id="print-worksheet-stretch"', 'id="print-worksheet-extra"')


def _break_surfaces(raw):
    """Push past the 25-surface ceiling. Anchored on </body>, which every deck
    has, rather than on a closing-div pair that happens to differ per deck --
    the first version of this mutation silently did nothing and the control
    reported PASS -> PASS, which is how a selftest lies."""
    extra = "".join(
        f'<div class="print-section" id="print-padding-{i}"><p>padding</p></div>'
        for i in range(6))
    return raw.replace("</body>", extra + "</body>", 1)


def _break_timings(raw):
    return re.sub(r'\sdata-min="\d+"', "", raw)


def _break_root_blocks(raw):
    return raw.replace(":root{", ":root{--planted-second:1}\n:root{", 1)


def _break_print_inside_main(raw):
    """Move the print pack inside main, which is the double-count shape.

    Done on the tree, not with a regex over the text: #print-area is tens of
    kilobytes of nested markup and no regex reliably finds its closing tag."""
    from lxml import html as _lh
    tree = _lh.fromstring(raw)
    area = tree.xpath('//*[@id="print-area"]')
    main = tree.xpath("//main")
    if not area or not main:
        return raw
    node = area[0]
    node.getparent().remove(node)
    main[0].append(node)
    return _lh.tostring(tree, encoding="unicode", doctype="<!DOCTYPE html>")


MUTATIONS = [
    ("own-lesson-config-only", _break_own_config,
     "the deck's own lesson-config is removed, so coverage cannot be counted"),
    ("no-donor-running-head", _break_donor_head,
     "one running head names the DONOR's week and title instead of this lesson's"),
    ("exactly-one-target-modal", _break_two_modals,
     "a second TA modal is added, so one of them can never open"),
    ("hud-js-present", _break_hud,
     "the hud.js tag is renamed, making the route unreachable from the hub"),
    ("lundy-in-three-places", _break_lundy,
     "the Lundy slide, its print section and its four dimensions are all renamed away"),
    ("three-tier-print-pack", _break_tiers,
     "the stretch tier is renamed, leaving supported and standard only"),
    ("surfaces-in-range", _break_surfaces,
     "six padding print sections push the deck past the 25-surface ceiling"),
    ("stage-timings-carried", _break_timings,
     "every data-min is stripped, exactly as #271's reshell did"),
    ("one-root-block", _break_root_blocks,
     "a second :root block is planted, against the RUN12-A ruling"),
    ("print-pack-outside-main", _break_print_inside_main,
     "the print pack is moved inside main, where the word count would read it twice"),
]


def _evaluate_full(source: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "deck.html"
        p.write_text(source, encoding="utf-8")
        return {c["clause"]: c for c in contract.evaluate(p)}


def _evaluate(source: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "deck.html"
        p.write_text(source, encoding="utf-8")
        return {c["clause"]: c["status"] for c in contract.evaluate(p)}


def list_controls() -> list[str]:
    return ([cid for cid, _, _ in MUTATIONS] + [pid for pid, *_ in FIXTURE_PROOFS]
            + [pid for pid, *_ in INTEGRITY_PROOFS] + [ROUTE_CONTROL[0]])


# THE THREE PROOFS THE RULING NAMES. The clause battery proves each clause can be
# made to red on a deck of its own shape; these prove the two ROUTES are separate,
# and that the measured timing table is load-bearing rather than decorative.
def _drop_one_panel(raw: str) -> str:
    """A v2 deck one stage short. Done on the tree: the panel is nested markup and
    no regex reliably finds its closing tag."""
    from lxml import html as _lh
    tree = _lh.fromstring(raw)
    panels = tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," %s ")]'
                        % contract.LOOP_PANEL_CLASS)
    if not panels:
        raise SystemExit("REFUSED: the v2 fixture carries no panel to remove")
    panels[0].getparent().remove(panels[0])
    return _lh.tostring(tree, encoding="unicode", doctype="<!DOCTYPE html>")


def _rename_lundy_slide(raw: str) -> str:
    """A v1 deck without its own slide, and nothing else touched: the working stage
    and the print pack stay, so two of three remain and the clause must still red."""
    out = raw.replace('data-title="Lundy Loop"', 'data-title="Reflection"', 1)
    if out == raw:
        raise SystemExit("REFUSED: the v1 fixture carries no Lundy slide to rename")
    return out


FIXTURE_PROOFS = (
    ("v2-panel-missing", "v2", "lundy-in-three-places", _drop_one_panel, None,
     "one transplanted panel is removed, so a stage the pupil works in carries no loop"),
    ("v1-slide-renamed", "v1", "lundy-in-three-places", _rename_lundy_slide, None,
     "the deck's own Lundy slide is renamed away, leaving the stage and print pack"),
    ("v1-minutes-off-by-one", "v1", "stage-timings-carried", None, -1,
     "the measured table is stamped one minute short of the period"),
    ("v2-minutes-off-by-one", "v2", "stage-timings-carried", None, -1,
     "the measured table is stamped one minute short of the period"),
)


# THE THREE CONTROLS THE STOP-T5 RULING NAMES. Two red proofs on the snapshot's integrity,
# and one positive control that both routes are still reachable at base -- the v1 route
# through the fixture, the v2 route through the transplanted deck.
INTEGRITY_PROOFS = (
    ("v1-fixture-one-byte-altered", "v1",
     "one byte of the fixture is altered, so it is no longer the bytes the estate shipped"),
    ("v1-fixture-digest-mismatch", "v1",
     "the recorded digest is moved off the fixture's own bytes"),
)
ROUTE_CONTROL = ("both-routes-pass-at-base",
                 "the v1 route passes through the snapshot fixture (own slide) and the v2 "
                 "route through the transplanted deck (sound panels on every working stage)")


def integrity_proofs() -> list[dict]:
    out = []
    for pid, shape, description in INTEGRITY_PROOFS:
        rel = dict(FIXTURES)[shape]
        raw = (ROOT / rel).read_text(encoding="utf-8")
        prov = load_minutes(rel).get("bytesFrom")
        before_ok, detail = fixture_integrity(rel, raw, prov)
        if not prov:
            out.append({"proof": pid, "shape": shape, "deck": rel, "planted": description,
                        "fired": False, "detail": "no recorded digest to defend"})
            continue
        if pid.endswith("one-byte-altered"):
            altered = raw[:-1] + ("x" if raw[-1:] != "x" else "y")
            assert altered != raw and len(altered) == len(raw)
            after_ok, after_detail = fixture_integrity(rel, altered, prov)
        else:
            moved = dict(prov)
            moved["sha256"] = ("0" * 64) if prov["sha256"] != "0" * 64 else "f" * 64
            after_ok, after_detail = fixture_integrity(rel, raw, moved)
        out.append({"proof": pid, "shape": shape, "deck": rel, "planted": description,
                    "baseVerdict": "intact" if before_ok else "ALREADY BROKEN",
                    "mutatedVerdict": "intact" if after_ok else "refused",
                    "detail": after_detail, "fired": before_ok and not after_ok})
    return out


def route_control(sources: dict) -> dict:
    """Both routes reachable at base: v1 by its own slide, v2 by its panels."""
    cid = "lundy-in-three-places"
    v1 = _evaluate_full(sources["v1"])[cid]
    v2 = _evaluate_full(sources["v2"])[cid]
    v1_ok = v1["status"] == "PASS" and "own slide=True" in v1["evidence"]
    v2_ok = v2["status"] == "PASS" and "own slide=False" in v2["evidence"]
    return {"proof": ROUTE_CONTROL[0], "kind": "positive control", "planted": ROUTE_CONTROL[1],
            "v1": v1["evidence"], "v2": v2["evidence"], "fired": v1_ok and v2_ok}


def fixture_proofs(sources: dict, verdicts: dict) -> list[dict]:
    rel_of = dict(FIXTURES)
    out = []
    for pid, shape, clause_id, mutate, delta, description in FIXTURE_PROOFS:
        rel = rel_of[shape]
        if mutate is not None:
            src = mutate(sources[shape])
        else:
            mins = list(load_minutes(rel)["minutes"])
            mins[-1] += delta
            src = _passing_base(rel, mins)
        after = _evaluate(src)
        before = verdicts[shape]
        out.append({"proof": pid, "shape": shape, "deck": rel, "clause": clause_id,
                    "planted": description, "baseVerdict": before.get(clause_id),
                    "mutatedVerdict": after.get(clause_id),
                    "fired": before.get(clause_id) == "PASS" and after.get(clause_id) == "RED"})
    return out


def run() -> dict:
    declared = contract.list_controls()
    sources, verdicts, fixtures = {}, {}, []
    for shape, rel in FIXTURES:
        base_src = _passing_base(rel)
        base = _evaluate(base_src)
        sources[shape], verdicts[shape] = base_src, base
        order_ok = list(base.keys()) == declared
        base_reds = sorted(k for k, v in base.items() if v == "RED")
        results = []
        for cid, mutate, description in MUTATIONS:
            mutated = _evaluate(mutate(base_src))
            fired = base.get(cid) == "PASS" and mutated.get(cid) == "RED"
            collateral = sorted(k for k, v in mutated.items()
                                if v == "RED" and k != cid and base.get(k) == "PASS")
            results.append({
                "clause": cid, "planted": description,
                "baseVerdict": base.get(cid), "mutatedVerdict": mutated.get(cid),
                "fired": fired, "collateralReds": collateral,
            })
        rec = load_minutes(rel)
        fixtures.append({
            "shape": shape, "deck": rel,
            "minutes": rec["minutes"], "minutesFrom": rec["sourceCommit"],
            "clauseOrderMatchesContract": order_ok, "baseReds": base_reds,
            "controlsRun": len(results),
            "controlsFired": sum(1 for r in results if r["fired"]),
            "allListedControlsFired": (order_ok and not base_reds
                                       and all(r["fired"] for r in results)),
            "controls": results,
        })
    proofs = fixture_proofs(sources, verdicts)
    integrity = integrity_proofs()
    route = route_control(sources)
    intact = [{"fixture": rel, "ok": fixture_integrity(rel)[0], "detail": fixture_integrity(rel)[1]}
              for _, rel in FIXTURES]
    # ONE LINE PER LISTED CONTROL, COUNTED ONCE. A clause control counts as fired
    # only if it fired on EVERY fixture -- a clause that can be made to red on the
    # v1 deck and not on the v2 deck is a clause tested on one shape of deck.
    per_clause = {}
    for f in fixtures:
        for r in f["controls"]:
            per_clause.setdefault(r["clause"], []).append(r["fired"])
    fired = sorted([cid for cid, res in per_clause.items() if res and all(res)]
                   + [pr["proof"] for pr in proofs + integrity if pr["fired"]]
                   + ([route["proof"]] if route["fired"] else []))
    declared_controls = list_controls()
    return {
        "tool": "classic_v2_contract_selftest", "toolVersion": VERSION,
        "file": "_sownb/vb/tools/classic_v2_contract_selftest.py",
        "contractVersion": contract.VERSION,
        "baseDeckNote": ("two real landed decks, each with its own measured stage minutes "
                         "restored in memory so that every clause can start from PASS"),
        "clausesDeclared": len(declared),
        "controlsDeclared": len(declared_controls),
        "controlsFired": len(fired),
        "controlsNotFired": sorted(set(declared_controls) - set(fired)),
        "fixtures": fixtures,
        "fixtureIntegrity": intact,
        "fixtureProofs": proofs,
        "integrityProofs": integrity,
        "routeControl": route,
        "allListedControlsFired": (all(f["allListedControlsFired"] for f in fixtures)
                                   and all(p["fired"] for p in proofs + integrity)
                                   and route["fired"] and all(i["ok"] for i in intact)
                                   and len(fired) == len(declared_controls)),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--rebase", action="store_true",
                    help="re-measure each fixture's stage minutes from its own history")
    ap.add_argument("--output")
    a = ap.parse_args()

    if a.list_controls:
        for c in list_controls():
            print(c)
        return 0

    if a.rebase:
        record = rebase_record()
        print(f"re-measured {len(record['fixtures'])} fixture(s) into "
              f"{MINUTES_RECORD.relative_to(ROOT)}")
        for rel, rec in sorted(record["fixtures"].items()):
            print(f"  {rec['sourceCommit'][:12]}  {rec['minutes']} = {rec['sum']}  "
                  f"{Path(rel).name}")
        return 0

    first = json.dumps(run(), indent=1, sort_keys=True)
    second = json.dumps(run(), indent=1, sort_keys=True)
    deterministic = first == second
    report = json.loads(first)
    report["deterministic"] = deterministic
    report["runDigest"] = hashlib.sha256(first.encode()).hexdigest()

    print(f"classic-v2 contract selftest  [{VERSION}] against {contract.VERSION}")
    for f in report["fixtures"]:
        print(f"  {f['shape']} base: {Path(f['deck']).name}")
        print(f"       minutes {f['minutes']} from {f['minutesFrom'][:12]}")
        if f["baseReds"]:
            print(f"       BASE IS NOT CLEAN, so no clause starts from PASS: {f['baseReds']}")
        for r in f["controls"]:
            mark = "ok  " if r["fired"] else "FAIL"
            extra = f"  collateral={r['collateralReds']}" if r["collateralReds"] else ""
            print(f"    {mark} {r['clause']:26s} {r['baseVerdict']} -> {r['mutatedVerdict']}{extra}")
        print(f"       {f['controlsFired']} of {f['controlsRun']} clause mutations fired here; "
              f"clause order matches the contract: {f['clauseOrderMatchesContract']}")
    for pr in report["fixtureProofs"]:
        mark = "ok  " if pr["fired"] else "FAIL"
        print(f"  {mark} {pr['proof']:28s} {pr['shape']} {pr['clause']}  "
              f"{pr['baseVerdict']} -> {pr['mutatedVerdict']}")
    for i in report["fixtureIntegrity"]:
        print(f"  {'ok  ' if i['ok'] else 'FAIL'} fixture intact               "
              f"{Path(i['fixture']).name}  {i['detail']}")
    for pr in report["integrityProofs"]:
        mark = "ok  " if pr["fired"] else "FAIL"
        print(f"  {mark} {pr['proof']:28s} {pr['shape']} {pr['detail']}")
    r = report["routeControl"]
    print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['proof']:28s} positive control")
    print(f"  {report['controlsFired']}/{report['controlsDeclared']} listed controls fired"
          + (f"; not fired: {report['controlsNotFired']}" if report["controlsNotFired"] else ""))
    print(f"  deterministic (two runs byte-identical): {deterministic}  "
          f"digest {report['runDigest'][:16]}")

    ok = report["allListedControlsFired"] and deterministic
    if a.output:
        out = ROOT / a.output if not Path(a.output).is_absolute() else Path(a.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS" if ok else "MEASUREMENT INVALID")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
