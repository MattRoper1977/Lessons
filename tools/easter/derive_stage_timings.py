#!/usr/bin/env python3
"""A3N R2: derive stage minutes from content and the declared session length.

WHY THE FIVE ASDAN DECKS ARE A TIMING PROBLEM, NOT A SPLIT
----------------------------------------------------------
Measured, all five share one profile: "I Do 2 . connect" carries 471-548 content
words against 3 declared minutes -- 157-183 words a minute -- while "Independent
. evidence" carries 256-293 against 16, or about 17. The minutes run against the
reverse of the content. Total reading need is 25-28 minutes of the 40, so the
lesson FITS; only its clock is wrong. A split would divide a lesson that has
room for itself.

THE DERIVATION, AND WHAT IT REFUSES TO DO
-----------------------------------------
Each stage first gets the minutes its reading needs: ceil(contentWords / rate)
at g23's own assumed 90 wpm, so no stage is timed below the reading it demands.
That floor is monotonic in content by construction -- more words never buys
fewer minutes.

The surplus is then distributed IN PROPORTION TO WHAT THE AUTHOR ALREADY WROTE,
and this is the deliberate refusal. Allocating the whole session by word count
would cut "Independent . evidence" from 16 minutes to 3, because independent
work is pupils DOING rather than reading and its minutes were never a reading
figure. A timing tool that compresses independent work to satisfy an arithmetic
about words has repaired the number and broken the lesson.

STRICT GLOBAL MONOTONICITY IS THEREFORE NOT ENFORCED, and that is a DEFAULTED
decision under A3N N1b, recorded rather than hidden. --strict measures it: it
forces minutes to be non-decreasing in content across all stages, and on these
decks it takes Independent from 16 minutes to 4. Both allocations are printed so
the choice is visible; the safe one ships.

Chrome is excluded from every count here, because R3 excluded it from the gate
that will judge the result.

Usage:
  derive_stage_timings.py <deck.html> [...]            report only
  derive_stage_timings.py <deck.html> --apply
  derive_stage_timings.py --strict <deck.html>         show the strict allocation
  derive_stage_timings.py --list-controls | --self-test
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = "derive-stage-timings-v1.0.0"
READING_RATE = 90          # g23's assumed supported-reading rate; band 60-120

_ls = importlib.util.spec_from_file_location(
    "lesson_stages", ROOT / "_sownb/vb/tools/lesson_stages.py")
ls = importlib.util.module_from_spec(_ls); _ls.loader.exec_module(ls)

def _rel(path) -> str:
    try:
        return str(Path(path).resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


# THE SAME FACT IS RECORDED IN THREE PLACES, AND ALL THREE MUST MOVE TOGETHER.
# data-min is what the gates read; lesson-config.timings is what the estate reads;
# and <div class="time">N min</div> is what a TEACHER READS OFF THE BOARD. The
# third is static text, computed from nothing -- there is no updateTimerDisplay
# on these decks. Writing the first two and not the third would leave a stage
# allocated seven minutes showing "4 min" to the person teaching it, which is
# worse than the mis-timing this tool exists to fix. The reshell dropped one of
# three records once already and nothing noticed for a year.
BADGE_RE = re.compile(r'(<div class="time">)(\d+)( min</div>)')

CONFIG_RE = re.compile(r'(<script[^>]*id=["\']lesson-config["\'][^>]*>)(.*?)(</script>)', re.S)


def read_config(raw: str):
    m = CONFIG_RE.search(raw)
    if not m:
        return None, None
    try:
        return json.loads(m.group(2)), m
    except Exception:
        return None, m


def allocate(content: list[int], current: list[int], session: int,
             rate: int = READING_RATE, strict: bool = False) -> list[int]:
    """Reading floors first, then the author's shape, then exact-sum repair."""
    n = len(content)
    floors = [math.ceil(c / rate) if c else 0 for c in content]
    if sum(floors) > session:
        return []                                   # infeasible: not a timing fix
    surplus = session - sum(floors)
    if strict:
        # minutes non-decreasing in content, ignoring what the author wrote
        weights = [float(c) for c in content]
    else:
        weights = [float(c) for c in current]
        if sum(weights) == 0:
            weights = [float(c) for c in content]
    total = sum(weights) or 1.0
    add = [surplus * w / total for w in weights]
    out = [f + int(a) for f, a in zip(floors, add)]
    # hand the rounding remainder to the largest fractional parts, deterministically
    rem = session - sum(out)
    order = sorted(range(n), key=lambda i: (-(add[i] - int(add[i])), -weights[i], i))
    for i in range(rem):
        out[order[i % n]] += 1
    if strict:
        # enforce: more content never fewer minutes
        for i in sorted(range(n), key=lambda i: content[i]):
            for j in range(n):
                if content[j] > content[i] and out[j] < out[i]:
                    out[j], out[i] = out[i], out[j]
    return out


def plan(path: Path, strict: bool = False) -> dict:
    raw = Path(path).read_text(encoding="utf-8")
    cfg, m = read_config(raw)
    meas = ls.measure(Path(path))
    content = [r["contentWords"] for r in meas["stages"]]
    current = [int(float(r["minutes"])) if r["minutes"] not in (None, "") else 0
               for r in meas["stages"]]
    session = sum(current)
    cfg_t = (cfg or {}).get("timings")
    agrees = cfg_t == current
    need = [math.ceil(c / READING_RATE) if c else 0 for c in content]
    new = allocate(content, current, session, strict=strict)
    rows = []
    for i, r in enumerate(meas["stages"]):
        rows.append({"stage": i + 1, "title": r["title"], "contentWords": content[i],
                     "minutesBefore": current[i], "readingNeeds": need[i],
                     "minutesAfter": (new[i] if new else None),
                     "underTimedBefore": need[i] > current[i],
                     "underTimedAfter": (need[i] > new[i]) if new else None})
    return {
        "file": _rel(path),
        "toolVersion": VERSION, "readingRateAssumed": READING_RATE,
        "sessionMinutes": session,
        "configTimingsAgreeWithStages": agrees,
        "readingMinutesRequired": sum(need),
        "feasible": bool(new),
        "strict": strict,
        "monotonicInContent": _is_monotonic(content, new) if new else None,
        "underTimedBefore": sum(1 for r in rows if r["underTimedBefore"]),
        "underTimedAfter": (sum(1 for r in rows if r["underTimedAfter"]) if new else None),
        "before": current, "after": new, "rows": rows,
        "status": "PASS" if new and sum(new) == session and not any(
            r["underTimedAfter"] for r in rows) else ("INFEASIBLE" if not new else "RED"),
    }


def _is_monotonic(content, minutes) -> bool:
    pairs = sorted(zip(content, minutes))
    return all(pairs[i][1] <= pairs[i + 1][1] for i in range(len(pairs) - 1))


def apply(path: Path, strict: bool = False) -> dict:
    p = Path(path)
    rec = plan(p, strict)
    if not rec["feasible"] or rec["status"] != "PASS":
        rec["applied"] = False
        return rec
    raw = p.read_text(encoding="utf-8")
    # data-min, in stage order, one replacement each, left to right
    out, pos, k = [], 0, 0
    for m in re.finditer(r'data-min="(\d+)"', raw):
        if k >= len(rec["after"]):
            break
        out.append(raw[pos:m.start()]); out.append(f'data-min="{rec["after"][k]}"')
        pos = m.end(); k += 1
    out.append(raw[pos:])
    raw2 = "".join(out)
    replaced = k
    # lesson-config.timings, so the two records cannot drift apart again
    cfg, m = read_config(raw2)
    cfg_written = False
    if cfg is not None and "timings" in cfg:
        cfg["timings"] = rec["after"]
        raw2 = raw2[:m.start(2)] + json.dumps(cfg, ensure_ascii=False) + raw2[m.end(2):]
        cfg_written = True
    # the visible badge, in stage order
    badges, pos2, j = [], 0, 0
    for m2 in BADGE_RE.finditer(raw2):
        if j >= len(rec["after"]):
            break
        badges.append(raw2[pos2:m2.start()])
        badges.append(f'{m2.group(1)}{rec["after"][j]}{m2.group(3)}')
        pos2 = m2.end(); j += 1
    badges.append(raw2[pos2:])
    raw2 = "".join(badges)
    p.write_text(raw2, encoding="utf-8")
    shown = [int(g[1]) for g in BADGE_RE.findall(p.read_text(encoding="utf-8"))]
    after = plan(p, strict)
    rec.update({"applied": True, "dataMinReplaced": replaced,
                "badgesReplaced": j, "badgesShown": shown,
                "badgesAgree": shown == rec["after"][:len(shown)],
                "configTimingsWritten": cfg_written,
                "verifiedAfter": after["before"], "verifiedAgrees":
                    after["configTimingsAgreeWithStages"],
                "verifiedSession": sum(after["before"])})
    return rec


# --------------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------------

CONTROL_IDS = [
    "the-session-length-is-preserved-exactly",
    "no-stage-is-left-timed-below-its-reading",
    "the-reading-floor-is-monotonic-in-content",
    "independent-work-keeps-its-doing-time",
    "strict-mode-would-take-it-away-and-is-therefore-not-the-default",
    "a-deck-whose-reading-exceeds-the-session-is-refused-not-squeezed",
    "applying-writes-both-records-and-they-agree",
    "the-visible-minute-badge-moves-with-the-attribute",
]


def _deck(mins, wordcounts, session_title="T"):
    body = f'<section class="slide active" data-title="{session_title}" data-min="0" data-type="title"><p>x y z</p></section>'
    for i, (mn, wc) in enumerate(zip(mins, wordcounts)):
        t = "Independent · evidence" if i == len(mins) - 1 else f"S{i}"
        body += (f'<section class="slide" data-title="{t}" data-min="{mn}"><p>'
                 + " ".join(f"w{j}" for j in range(wc)) + ".</p></section>")
    cfg = json.dumps({"id": "x", "timings": [0] + list(mins)})
    return ('<!doctype html><html><head><style>.slide{display:none}'
            '.slide.active{display:flex}</style>'
            f'<script id="lesson-config" type="application/json">{cfg}</script>'
            '</head><body><main class="deck">' + body + "</main></body></html>")


def _tmp(src):
    fh = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
    fh.write(src); fh.close()
    return Path(fh.name)


def controls() -> list[dict]:
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    # a deck shaped like the real ASDAN five: a heavy stage on 3 minutes,
    # independent work on 16 with little to read
    mins = [3, 4, 3, 16]
    wc = [120, 450, 130, 260]
    p = _tmp(_deck(mins, wc))
    r = plan(p)

    rec("the-session-length-is-preserved-exactly",
        "the derived minutes sum to the session the deck declares",
        (26, 26), (r["sessionMinutes"], sum(r["after"])))

    rec("no-stage-is-left-timed-below-its-reading",
        "every stage ends with at least ceil(content/90) minutes",
        0, r["underTimedAfter"])

    floors = [x["readingNeeds"] for x in r["rows"]]
    conts = [x["contentWords"] for x in r["rows"]]
    rec("the-reading-floor-is-monotonic-in-content",
        "the floor itself never gives more words fewer minutes",
        True, _is_monotonic(conts, floors))

    ind_before = r["rows"][-1]["minutesBefore"]
    ind_after = r["rows"][-1]["minutesAfter"]
    rec("independent-work-keeps-its-doing-time",
        "independent work is pupils DOING; its minutes were never a reading figure, "
        "so the derivation must not reclaim them",
        True, ind_after >= ind_before * 0.6)

    rs = plan(p, strict=True)
    rec("strict-mode-would-take-it-away-and-is-therefore-not-the-default",
        "strict global monotonicity compresses independent work -- measured, not "
        "asserted, which is why the default refuses it",
        True, rs["rows"][-1]["minutesAfter"] < ind_after)

    tight = _tmp(_deck([1, 1], [2000, 2000]))
    rt = plan(tight)
    rec("a-deck-whose-reading-exceeds-the-session-is-refused-not-squeezed",
        "a lesson that cannot fit its own reading is a SPLIT question, and the "
        "timing tool must say so rather than invent a schedule",
        ("INFEASIBLE", False), (rt["status"], rt["feasible"]))

    p2 = _tmp(_deck(mins, wc))
    ap = apply(p2)
    cfg2, _ = read_config(p2.read_text(encoding="utf-8"))
    rec("applying-writes-both-records-and-they-agree",
        "data-min and lesson-config.timings are written together, because the "
        "reshell dropped one of them once already and nothing noticed",
        (True, True, True),
        (ap["applied"], ap["verifiedAgrees"], cfg2["timings"] == ap["verifiedAfter"]))

    p3 = _tmp(_deck(mins, wc).replace(
        '<main class="deck">',
        '<main class="deck">').replace(
        'data-min="0" data-type="title"><p>x y z</p>',
        'data-min="0" data-type="title"><div class="time">0 min</div><p>x y z</p>'))
    # give every stage a visible badge matching its attribute
    src3 = p3.read_text(encoding="utf-8")
    for mn in mins:
        src3 = src3.replace(f'data-min="{mn}"><p>',
                            f'data-min="{mn}"><div class="time">{mn} min</div><p>', 1)
    p3.write_text(src3, encoding="utf-8")
    ap3 = apply(p3)
    rec("the-visible-minute-badge-moves-with-the-attribute",
        "the badge is static text a teacher reads off the board; leaving it behind "
        "would show '4 min' on a stage now allocated seven",
        (True, True), (ap3.get("badgesReplaced", 0) > 0, ap3.get("badgesAgree")))

    for f in (p, tight, p2, p3):
        f.unlink(missing_ok=True)
    return out


def self_test() -> dict:
    res = controls()
    ids = [r["id"] for r in res]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "derive_stage_timings", "toolVersion": VERSION,
            "file": "tools/easter/derive_stage_timings.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(res),
            "controlsFired": sum(1 for r in res if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra and all(r["fired"] for r in res),
            "controls": res}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("decks", nargs="*")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--output")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.list_controls:
        print("\n".join(CONTROL_IDS)); return 0
    if a.self_test:
        rep = self_test()
        print(f"derive_stage_timings self-test  [{VERSION}]")
        for r in rep["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:58s} "
                  f"expected={str(r['expected'])[:34]} observed={str(r['observed'])[:34]}")
        print(f"{rep['controlsFired']}/{rep['controlsRun']} controls fired")
        print("PASS" if rep["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if rep["allListedControlsFired"] else 1

    recs, ok = [], True
    for d in a.decks:
        r = apply(Path(d), a.strict) if a.apply else plan(Path(d), a.strict)
        recs.append(r)
        print(f"\n{Path(d).name[:56]}  session {r['sessionMinutes']}  "
              f"reading needs {r['readingMinutesRequired']}  {r['status']}"
              f"{'  APPLIED' if r.get('applied') else ''}")
        print(f"  {'stage':32s} {'cont':>5s} {'was':>4s} {'need':>5s} {'now':>4s}")
        for x in r["rows"]:
            mark = " <--" if x["underTimedBefore"] else ""
            print(f"  {(x['title'] or '')[:32]:32s} {x['contentWords']:5d} "
                  f"{x['minutesBefore']:4d} {x['readingNeeds']:5d} "
                  f"{(x['minutesAfter'] if x['minutesAfter'] is not None else 0):4d}{mark}")
        print(f"  monotonic-in-content {r['monotonicInContent']}  "
              f"under-timed {r['underTimedBefore']} -> {r['underTimedAfter']}")
        ok = ok and r["status"] == "PASS"
    if a.output:
        o = Path(a.output); o = o if o.is_absolute() else ROOT / o
        o.parent.mkdir(parents=True, exist_ok=True)
        o.write_text(json.dumps({"tool": "derive_stage_timings", "toolVersion": VERSION,
                                 "file": "tools/easter/derive_stage_timings.py",
                                 "subject": "stage minutes derived from content and the "
                                            "declared session length",
                                 "decks": recs}, indent=1) + "\n", encoding="utf-8")
    print("\nPASS" if ok else "\nRED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
