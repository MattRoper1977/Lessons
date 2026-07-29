#!/usr/bin/env python3
"""
AT-INST-02 - Art Teesside co-occurrence assertions.

WHY THIS EXISTS. AT-INST-01 asks "is a banned string present?". It cannot see
this estate's characteristic fault, which is not a false statement but two
true-looking halves that cannot both hold. R1 found seven files carrying
"BUILD - Explore" and "Bronze Part A" inches apart on the same header strip.
Seven human reviews passed them, because whichever half you looked at was
correct. Every string an absence check hunts for is legitimately there.

So this instrument asserts on PAIRS, not presences.

  C1  award level disagreeing between chassis layers within one file
  C2  term or week disagreeing between strip, badge and print mirror
  C3  kit vocabulary co-present with a kit disavowal in the same file
  C4  a Part described as both banked and open in the same file
  C5  a route whose scheme of work disavows kit that its own lessons teach

WHAT THIS STRUCTURALLY CANNOT DETECT
  * C3 is within-file only. C5 was added for route scope after C3 returned zero
    at a baseline where the estate demonstrably carries a live contradiction: the
    within-file question was the wrong question. C5 is folder-scoped; a
    contradiction spanning two folders (D-PRESS-01: BUILD denies the press,
    GROW teaches it) is reported separately as the estate headline.
  * Contradictions carried in prose rather than in the chassis. C1 reads only the
    declared header layers, deliberately: a GROW lesson may legitimately mention
    Silver as a next step, and treating that as a conflict would manufacture the
    false-positive family this register exists to prevent.
  * C4 is APPROXIMATE, not literal. It matches status words inside a window near
    a Part token. Read every C4 hit before quoting it.
"""
import re, sys, glob, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEVELS = ("Explore", "Bronze", "Silver", "Gold")

# Pairings that are legitimate and must not be reported. Exact strings.
DECLARED_PAIRS = [
    ("C3", "Build/Autumn2_Scheme_of_Work.html", "names the press in order to refuse it"),
    ("C3", "Build/START_HERE.html", "names the press in order to refuse it"),
]
DISAVOWALS = ["no press, no rollers", "No press, no rollers", "is off the table",
              "there is no press", "no printing inks"]
KIT = (r"press corner|inking bench|inking queue|inking slab|printing ink|ink load|relief print"
       r"|\brollers?\b|\bbrayer\b|\blino\b|pre-cut plate|plate wear|re-inked|pull an edition")


def layers(s):
    """Award level / term / week as CLAIMED by each chassis layer."""
    out = {}
    m = re.search(r'sow-strip.>([^<]*)', s)
    if m:
        t = m.group(1)
        out["strip"] = {"term": (re.search(r'Aut\w*\s*(\d)', t) or [None, None])[1],
                        "week": (re.search(r'Week\s*(\d+)', t) or [None, None])[1]}
    m = re.search(r'(?:BUILD|GROW|LAUNCH) · (\w+) · Week (\d+) of \d+ · (\w+)\s*(\d)?', s)
    if m:
        out["badge"] = {"level": m.group(1), "week": m.group(2), "term": m.group(4)}
    m = re.search(r'Trinity Arts Award (\w+)', s)
    if m:
        out["footer"] = {"level": m.group(1)}
    lv = set(re.findall(r'award-strip.>[^<]*?(' + "|".join(LEVELS) + r')\b', s))
    if lv:
        out["awardstrip"] = {"level": sorted(lv)}
    m = re.search(r'Teacher Print Tools — Week (\d+)', s)
    if m:
        out["printmirror"] = {"week": m.group(1)}
    return out


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))
    findings = collections.defaultdict(list)

    for path in files:
        s = open(path, encoding="utf-8", errors="replace").read()
        rel = os.path.relpath(path, ROOT)
        L = layers(s)

        # C1 - award level across chassis layers
        lv = set()
        for k in ("badge", "footer"):
            if k in L and L[k].get("level") in LEVELS:
                lv.add(L[k]["level"])
        for v in L.get("awardstrip", {}).get("level", []):
            lv.add(v)
        if len(lv) > 1:
            findings["C1_award_level"].append((rel, " vs ".join(sorted(lv)) + f"   layers={ {k: v.get('level') for k, v in L.items() if v.get('level')} }"))

        # C2 - term / week across layers
        wk = {k: L[k]["week"] for k in ("strip", "badge", "printmirror") if k in L and L[k].get("week")}
        tm = {k: L[k]["term"] for k in ("strip", "badge") if k in L and L[k].get("term")}
        if len(set(wk.values())) > 1:
            findings["C2_week"].append((rel, str(wk)))
        if len(set(tm.values())) > 1:
            findings["C2_term"].append((rel, str(tm)))

        # C3 - kit vocabulary beside a kit disavowal, same file
        if any(d in s for d in DISAVOWALS):
            if any(p[0] == "C3" and p[1] == rel for p in DECLARED_PAIRS):
                pass
            elif re.search(KIT, s, re.I):
                hits = collections.Counter(h.lower() for h in re.findall(KIT, s, re.I))
                findings["C3_kit_beside_disavowal"].append((rel, str(dict(hits))))

        # C4 - a Part both banked and open (APPROXIMATE)
        for lvl in LEVELS:
            for part in "ABCDE":
                tok = f"{lvl} Part {part}"
                for m in re.finditer(re.escape(tok), s):
                    w = s[max(0, m.start() - 130):m.end() + 130]
                    done = re.search(r'\bbanked\b|\bcomplete[d]?\b|signed off', w, re.I)
                    open_ = re.search(r"\bstill (?:to|open)\b|\boutstanding\b|\bnot yet\b|\bopen\b", w, re.I)
                    if done and open_:
                        findings["C4_part_status"].append((rel, f"{tok}: '{done.group(0)}' + '{open_.group(0)}'"))
                        break

    print(f"Art Teesside co-occurrence assertions - {len(files)} HTML files\n")
    order = ["C1_award_level", "C2_term", "C2_week", "C3_kit_beside_disavowal", "C4_part_status"]
    total = 0
    for key in order:
        rows = findings.get(key, [])
        total += len(rows)
        print(f"{key:<26}{len(rows):>4} finding(s)")
        for rel, why in rows[:25]:
            print(f"      {rel}\n          {why}")

    # C5 - route scope: a folder whose disavowal is contradicted by its own lessons
    print()
    routes = collections.defaultdict(lambda: {"disavow": [], "kit": []})
    estate_disavow, estate_kit = [], []
    for path in files:
        s2 = open(path, encoding="utf-8", errors="replace").read()
        rel = os.path.relpath(path, ROOT)
        folder = rel.split(os.sep)[0] if os.sep in rel else "(root)"
        d = any(x in s2 for x in DISAVOWALS)
        live = collections.Counter(h.lower() for h in re.findall(KIT, s2, re.I))
        if d:
            routes[folder]["disavow"].append(rel); estate_disavow.append(rel)
        if live and not d:
            routes[folder]["kit"].append((rel, dict(live))); estate_kit.append((rel, dict(live)))
    c5 = 0
    for folder, v in sorted(routes.items()):
        if v["disavow"] and v["kit"]:
            c5 += len(v["kit"])
            print(f"C5_route_contradiction   {folder}: disavowed in {len(v['disavow'])} file(s), taught in {len(v['kit'])}")
            for rel, hits in v["kit"]:
                print(f"      {rel}\n          {hits}")
    if not c5:
        print("C5_route_contradiction      0 finding(s)")
    total += c5
    print(f"\nESTATE HEADLINE  kit disavowed in {len(estate_disavow)} file(s); "
          f"taught in {len(estate_kit)} file(s) carrying no disavowal.")
    for rel, hits in estate_kit:
        print(f"      {rel}  {hits}")

    r6 = c6_scheme_mapping()
    print("\nC6_scheme_mapping")
    for rel, why in r6["agree"]:
        print(f"   AGREE     {rel}  ({why})")
    for rel, why in r6["disagree"]:
        print(f"   DISAGREE  {rel}  {why}")
        total += len(why)
    for rel in r6["unmapped"]:
        print(f"   UNMAPPED  {rel}  (declares no per-week award section)")

    print(f"\nTOTAL {total}")
    print(f"declared legitimate pairings: {len(DECLARED_PAIRS)}")
    return 0 if total == 0 else 1


# ---------------------------------------------------------------- C6
def c6_scheme_mapping():
    """
    C6 - does each scheme of work declare its own Part/Unit shape per week, and
    does that declaration agree with the two sources that are the record: the
    lesson badge and the pack evidence locator?

    Specified on CATEGORY, not phrasing (standing rule 9): the question is
    "does this scheme state, per week, which award section the week evidences,
    and do the three sources agree", not "does the string 'Part B' appear".
    A scheme that states nothing is reported as unmapped, which is a finding in
    its own right and is how GROW's gap was visible as 22 / 14 / 23 / 0.
    """
    out = {"disagree": [], "unmapped": [], "agree": []}
    tiers = {"Grow": "Grow", "Build": "Build", "Launch": "Launch"}
    for folder in tiers:
        d = os.path.join(ROOT, folder)
        if not os.path.isdir(d):
            continue
        # source 1 - lesson badges
        badge = {}
        for f in sorted(glob.glob(os.path.join(d, "*_ART_*W[0-9]*.html"))):
            w = re.search(r"_W(\d)_", os.path.basename(f))
            if not w:
                continue
            m = re.search(r'award-strip">[^<]*?((?:Part|Unit) [A-E0-9]+)', open(f, encoding="utf-8", errors="replace").read())
            if m:
                badge[int(w.group(1))] = m.group(1)
        # source 2 - pack locator
        locator = {}
        for f in glob.glob(os.path.join(d, "*Pack*.html")):
            s = open(f, encoding="utf-8", errors="replace").read()
            i = s.find("LOCP=")
            if i < 0:
                continue
            seg = s[i:s.find("];", i) + 2]
            for pm in re.finditer(r'"p":\s*"((?:Part|Unit) [A-E0-9]+)[^"]*".*?"rows":\s*\[(.*?)\]', seg, re.S):
                for wk in re.findall(r"Week (\d)", pm.group(2)):
                    locator.setdefault(int(wk), set()).add(pm.group(1))
        # source 3 - the scheme's own declaration
        for sow in sorted(glob.glob(os.path.join(d, "*Scheme_of_Work.html"))):
            s = open(sow, encoding="utf-8", errors="replace").read()
            rel = os.path.relpath(sow, ROOT)
            declared = {int(w): p for w, p in
                        re.findall(r"<h2>Week (\d):[^<]*</h2>\s*<p><b>Arts Award:</b>[^<]*?((?:Part|Unit) [A-E0-9]+)", s)}
            if not declared:
                out["unmapped"].append(rel)
                continue
            bad = []
            for w, p in sorted(declared.items()):
                b, l = badge.get(w), locator.get(w)
                if b and b != p:
                    bad.append(f"W{w}: scheme={p} badge={b}")
                if l and p not in l:
                    bad.append(f"W{w}: scheme={p} locator={sorted(l)}")
            (out["disagree"] if bad else out["agree"]).append((rel, bad or f"{len(declared)} weeks agree"))
    return out


if __name__ == "__main__":
    sys.exit(main())
