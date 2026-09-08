#!/usr/bin/env python3
"""RX3 readback generator: every line from rx3_results.json (numbers measured by the _rx3/ scripts), no narrative. ≤32 lines."""
import json, sys
r = json.load(open(sys.argv[1]))
L = [f"1 {r['token']}",
     f"2 mains: Site S2 {r['S2']} · Lessons L1 {r['L1']} · Apps A1 {r['A1']} · Games {r['games']}",
     f"3 #316: {r['p316']} · A1 {r['A1_note']}",
     f"4 Lumins: {r['lumins']}"]
for i, fam in enumerate(r['families'], start=5):
    L.append(f"{i} {fam}")
L += [f"11 images: {r['images']}",
      f"12 recommended: {r['recommended']}",
      f"13 P3b: {r['p3b']}",
      f"14 pins: {r['pins']}",
      f"15 publisher runs: {r['runs']}",
      f"16 hub gate: {r['hub_gate']}",
      f"17 M1 hosting: {r['m1']}",
      f"18 M2 phone check: {r['m2']}",
      f"19 M3: {r['m3']}",
      f"20 M4 Supabase: {r['m4']}",
      f"21 reversals: {r['reversals']}"]
L += [f"{22 + i} {x}" for i, x in enumerate(r.get('extra', []))]
L.append(r['token'])
assert len(L) <= 32, len(L)
print('\n'.join(L))
