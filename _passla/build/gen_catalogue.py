# -*- coding: utf-8 -*-
"""Append the LAUNCH ASDAN suite to resources.json, mirroring the GROW ASDAN
convention EXACTLY (derived, not invented):
 - catalogue 30 lessons (type 'lesson') + 5 START_HERE + hub (type 'teacher') = 36;
 - leave Scheme_of_Work.html and Resources_and_Tools.html UNCATALOGUED (as GROW does);
 - keys file+desc canonical; desc from each lesson's own blurb + banks (no invention);
 - subject 'LAUNCH Vocational & PfA' (sibling of GROW's); keywords [asdan,launch,pfa,<strand>];
 - APPEND at end (surgical; append-only union-safe with pending SBX).
Idempotent: refuses to double-append if LAUNCH_ASDAN entries already present."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RJ = os.path.join(ROOT, "resources.json")

# strand descriptor + keyword slug, per folder
STRAND = {
 "PEQ":                 ("Personal Effectiveness (PEQ L1)", "peq"),
 "Careers":             ("Employability & Careers",         "careers"),
 "Living_Independently":("Independent Living",              "independent living"),
 "Vocational":          ("Vocational Skills",               "vocational"),
 "Community_Enterprise":("Community & Enterprise",          "community enterprise"),
}

def slug(s):
    return re.sub(r'-+','-', re.sub(r'[^a-z0-9]+','-', s.lower())).strip('-')

def blurb(L):
    s = L['success'][0]
    b = s[5:].strip() if s.lower().startswith("i can ") else s
    return b[0].upper()+b[1:]

def build_entries():
    import content_peq, content_careers, content_living, content_vocational, content_community
    mods = [content_peq, content_careers, content_living, content_vocational, content_community]
    entries=[]
    for mod in mods:
        k = mod.STRAND_KEY; desc_strand, kwslug = STRAND[k]
        kw = ["asdan","launch","pfa",kwslug]
        fam = f"LAUNCH ASDAN · {desc_strand.split(' (')[0]}"
        for L in mod.LESSONS:
            f = f"LAUNCH_ASDAN/{mod.FOLDER}/{L['filename']}"
            entries.append({
                "id": slug(f"launch-asdan-{mod.FOLDER}-w{L['week']}-{L['title_short']}"),
                "title": f"LAUNCH ASDAN W{L['week']}: {L['title_short']} ({desc_strand})",
                "type": "lesson",
                "subject": "LAUNCH Vocational & PfA",
                "year": "2026-27",
                "file": f,
                "desc": f"{blurb(L)} — v5 studio lesson with full print pack. {L['banks']}.",
                "family": fam,
                "keywords": kw,
            })
        # START_HERE (type teacher) — one per strand
        entries.append({
            "id": slug(f"launch-asdan-hub-{mod.FOLDER}"),
            "title": f"LAUNCH ASDAN: {desc_strand} — START HERE",
            "type": "teacher",
            "subject": "LAUNCH Vocational & PfA",
            "year": "2026-27",
            "file": f"LAUNCH_ASDAN/{mod.FOLDER}/START_HERE.html",
            "desc": f"{desc_strand.split(' (')[0]} strand hub — 6 lessons, W1-6.",
            "family": fam,
            "keywords": kw,
        })
    # pathway hub (type teacher)
    entries.append({
        "id": "launch-asdan-hub",
        "title": "LAUNCH ASDAN — the full term (hub)",
        "type": "teacher",
        "subject": "LAUNCH Vocational & PfA",
        "year": "2026-27",
        "file": "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html",
        "desc": "Five ASDAN strands: PEQ L1 (Communication complete), Careers, Independent Living, Vocational, Community & Enterprise.",
        "family": "LAUNCH ASDAN",
        "keywords": ["asdan","launch","pfa"],
    })
    return entries

def main():
    raw = open(RJ, encoding="utf-8").read()
    data = json.loads(raw)
    assert isinstance(data, list), "resources.json is not a list"
    before = len(data)
    if any(isinstance(e,dict) and 'LAUNCH_ASDAN' in str(e.get('file','')) for e in data):
        print("LAUNCH_ASDAN entries already present — refusing to double-append."); return
    entries = build_entries()
    assert len(entries)==36, f"expected 36 LAUNCH entries, built {len(entries)}"
    for e in entries:
        assert os.path.isfile(os.path.join(ROOT, e['file'])), "missing file "+e['file']
        assert 'Scheme_of_Work' not in e['file'] and 'Resources_and_Tools' not in e['file'], "must not catalogue "+e['file']
        assert 'Delivering a Project' not in e['desc'] and 'registration via UAS' not in e['desc'], "drift in desc"
    # SURGICAL TEXT APPEND: keep existing 411 entries byte-for-byte; insert before final ']'.
    # Each entry serialized indent=1 then +1 leading space per line (list-item level).
    def ser(e):
        body = json.dumps(e, ensure_ascii=False, indent=1)
        return "\n".join(" "+ln for ln in body.split("\n"))
    block = ",\n" + ",\n".join(ser(e) for e in entries)
    i = raw.rstrip().rfind("]")
    head = raw[:i].rstrip()               # ends with the last existing entry's '}'
    assert head.endswith("}"), "unexpected resources.json tail"
    out = head + block + "\n]\n"
    # ASSERT post-condition BEFORE writing: parses, count exact, existing prefix intact
    parsed = json.loads(out)
    assert len(parsed) == before + 36, f"count {len(parsed)} != {before}+36"
    assert parsed[:before] == data, "existing entries changed — not a surgical append"
    assert out.startswith(raw[:i].rstrip()[:2000]), "prefix drift"
    open(RJ,"w",encoding="utf-8").write(out)
    print(f"resources.json: {before} -> {len(parsed)} entries (+36 LAUNCH: 30 lesson + 6 teacher). Existing {before} byte-preserved.")

if __name__=="__main__":
    main()
