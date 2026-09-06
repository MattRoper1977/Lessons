#!/usr/bin/env python3
"""PROP-1 protected-surface gate.

_eca1/tools/protected.js hashes CONTEXT WINDOWS anchored at protected markers
(e.g. the witness stream is a 700-char tail from "Assessor Witness Statement").
A ruled PROP-1 edit landing inside such a window shifts the hash without touching
the protected string itself. Those deltas are legitimate but must never be silent:
each one is named, with its row id and the ruling that authorises it, in
_prop1/PROTECTED_DELTAS.tsv. Anything not on that list fails the gate.

Also asserts the marker COUNT per stream is unchanged - a count move means a
protected string was added or deleted, which no PROP-1 row authorises.
"""
import subprocess, sys, os, collections

ROOT = subprocess.run(["git","rev-parse","--show-toplevel"],capture_output=True,text=True).stdout.strip()
ALLOW = os.path.join(ROOT,"_prop1/PROTECTED_DELTAS.tsv")

def allowed():
    out = {}
    if not os.path.exists(ALLOW): return out
    for ln in open(ALLOW,encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln.strip() or ln.startswith("#"): continue
        f, stream, rows, ruling = ln.split("\t",3)
        out[(f,stream)] = (rows,ruling)
    return out

r = subprocess.run(["node","_eca1/tools/protected.js","verify"],cwd=ROOT,capture_output=True,text=True)
lines = [l for l in r.stdout.splitlines() if l.startswith(("LOST","NEW"))]
if not lines:
    print("protected: IDENTICAL - no deltas"); sys.exit(0)

ok = allowed()
seen = collections.defaultdict(lambda: {"LOST":[], "NEW":[]})
for l in lines:
    kind = l.split()[0]
    f, stream, n, h = l.split(None,1)[1].split("\t")
    seen[(f,stream)][kind].append((int(n),h))

bad = []
for (f,stream),d in sorted(seen.items()):
    lc = [n for n,_ in d["LOST"]]; nc = [n for n,_ in d["NEW"]]
    if lc != nc:
        bad.append(f"{f}\t{stream}\tMARKER COUNT MOVED {lc} -> {nc}"); continue
    if (f,stream) not in ok:
        bad.append(f"{f}\t{stream}\tUNAUTHORISED window shift (not in PROTECTED_DELTAS.tsv)"); continue
    rows,ruling = ok[(f,stream)]
    print(f"AUTHORISED  {f}\t{stream}\tcount={lc[0]} unchanged\trows={rows}\t{ruling}")

if bad:
    print("\nPROTECTED GATE FAIL:")
    for b in bad: print("  "+b)
    sys.exit(1)
print(f"\nprotected: {len(seen)} window shift(s), all authorised; every marker count unchanged")
