# -*- coding: utf-8 -*-
"""PEQ-YEAR-3 §7 — prove the UAS applied/excluded counts, with exclusions named.

Counts every `AQA UAS` occurrence in every tracked file, buckets each file by the
rule that decides its fate, and reports qualified vs bare inside each bucket.

    python3 _passpq/tools/uas_census.py            report
    python3 _passpq/tools/uas_census.py --gate     report, then assert the invariants

WHY A CENSUS AND NOT A GREP
---------------------------
"UAS wording applied" is only meaningful next to what was deliberately NOT touched.
Two standing holds (OPEN_ITEMS 17, OPEN_ITEMS 43) forbid edits to 154 of the files
that carry the defect, so a bare count of qualified sites looks like poor coverage
when it is in fact full coverage of everything in reach. The buckets are the point.

THE ONE TRAP
------------
Count the qualifier string itself, never a guessed shape of the site it sits on.
An earlier version matched `AQA UAS <optional shape> (unit unconfirmed` and silently
undercounted by five, because the estate carries wordings this pass did not author
(`AQA UAS enterprise evidence (unit unconfirmed)`). A shape-matching regex fails
closed-looking: it reports a smaller number, which reads as "some were missed"
rather than "the regex was wrong".
"""
import subprocess, re, io, os, sys, collections

files = subprocess.run(["git","ls-files"],capture_output=True,text=True,check=True).stdout.split()
UAS = "AQA UAS"
# Count the qualifier itself, not a guessed shape of the site it sits on. The
# estate carries wordings this pass did not author ("AQA UAS enterprise evidence
# (unit unconfirmed)"), and a shape-matching regex silently undercounts them.
# Both canonical spellings, plus the one recorded §4-B deviation.
QUAL = re.compile(r"\(unit unconfirmed|— unit unconfirmed\)")

# NAMED EXCEPTIONS - sites that carry "AQA UAS" and are deliberately NOT qualified.
# Recorded so a future sweep does not rediscover them as anomalies and "fix" them.
NAMED_EXCEPTIONS = {
    ("index.html", "AQA UAS ALIGNED"):
        "an awarding-body ALIGNMENT stamp, not a unit-code claim. It says the estate's "
        "material is aligned to the AQA UAS framework, which is true and is a different "
        "assertion from 'this unit code is confirmed'. Q-003 governs the latter. Ruled "
        "at the PEQ-YEAR-3 close-out: leave it exactly as it is.",
}


def bucket(path):
    if path.startswith("Science_Teesside/"):
        return "EXCLUDED · Science_Teesside — OPEN_ITEMS 17 byte-pristine hold"
    if "_Estate_v3/" in path or path.endswith("_Estate_v3"):
        return "EXCLUDED · *_Estate_v3 test copies — OPEN_ITEMS 43"
    if path.startswith("quality/") or path.startswith("_close/") or path.startswith("_passpq/"):
        return "RECORD · registers, this pass's docs (quoting the defect is the point)"
    if path.endswith((".py",".mjs",".js",".json")) and path != "resources.json":
        return "TOOLING · gates, generators, content modules"
    return "CONTENT"

rows=[]
for f in files:
    if not os.path.isfile(f):
        continue
    try:
        t = io.open(f, encoding="utf-8", errors="strict").read()
    except Exception:
        continue
    n = t.count(UAS)
    if not n:
        continue
    q = len(QUAL.findall(t))
    rows.append((bucket(f), f, n, q, n-q))

agg = collections.defaultdict(lambda: [0,0,0,0])   # files, occ, qualified, bare
for b,f,n,q,bare in rows:
    a=agg[b]; a[0]+=1; a[1]+=n; a[2]+=q; a[3]+=bare

print(f"{'bucket':<62}{'files':>6}{'occ':>7}{'qual':>7}{'bare':>7}")
print("-"*89)
for b in sorted(agg):
    a=agg[b]
    print(f"{b:<62}{a[0]:>6}{a[1]:>7}{a[2]:>7}{a[3]:>7}")
tot=[sum(a[i] for a in agg.values()) for i in range(4)]
print("-"*89)
print(f"{'TOTAL':<62}{tot[0]:>6}{tot[1]:>7}{tot[2]:>7}{tot[3]:>7}")

print("\n== named exceptions (carry AQA UAS, deliberately unqualified) ==")
for (f, s), why in NAMED_EXCEPTIONS.items():
    present = s in io.open(f, encoding="utf-8").read() if os.path.isfile(f) else False
    print(f"  {'present' if present else 'ABSENT '}  {f}: {s!r}")
    print(f"           {why}")

print("\n== CONTENT bucket, per file ==")
for b,f,n,q,bare in sorted(rows):
    if b!="CONTENT":
        continue
    mark = "APPLIED " if q else "        "
    print(f"  {mark}{f:<74} occ {n:>3}  qual {q:>3}  bare {bare:>3}")


if "--gate" in sys.argv:
    problems = []
    def check(label, got, want):
        if got != want:
            problems.append(f"{label}: {got}, expected {want}")
        print(f"  {'ok  ' if got == want else 'RED '}{label}: {got}")

    print("\n== gate ==")
    # The two byte-pristine holds. A qualifier appearing inside either is the
    # signal that a sweep reached past its ruling.
    check("Science_Teesside qualified sites (hold: OPEN_ITEMS 17)",
          agg["EXCLUDED · Science_Teesside — OPEN_ITEMS 17 byte-pristine hold"][2], 0)
    check("*_Estate_v3 qualified sites (hold: OPEN_ITEMS 43)",
          agg["EXCLUDED · *_Estate_v3 test copies — OPEN_ITEMS 43"][2], 0)
    # PEQ-YEAR-3 §5 applied 88 sites across 19 content surfaces: the 18 staff-facing
    # HTML files and resources.json. Both numbers are recorded in
    # quality/toolkits/PROPOSED_uas_claim_qualifier.md and must move together with it.
    check("content surfaces carrying a qualifier", sum(1 for b,_,_,q,_ in rows if b == "CONTENT" and q), 19)
    check("content qualifier sites", agg["CONTENT"][2], 88)
    if problems:
        print("\n[FAIL] UAS census: " + "; ".join(problems))
        raise SystemExit(1)
    print("\n[PASS] UAS census: holds intact, applied counts match the record")
