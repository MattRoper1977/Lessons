#!/usr/bin/env python3
"""§2 APPLY — three changes plus the version strings, nothing else.

Every replacement asserts it matched EXACTLY ONCE. A pattern that matches
twice, or not at all, stops the patch rather than silently doing something
else (R0.23: a pattern prints its scope and match set before acting).
"""
import sys, hashlib, shutil

SRC, DST = sys.argv[1], sys.argv[2]
shutil.copyfile(SRC, DST)
s = open(DST, encoding='utf-8').read()

edits = []


def sub(label, old, new):
    global s
    n = s.count(old)
    print(f"  [{label}] matches={n}", end=' ')
    if n != 1:
        print("*** NOT EXACTLY ONE — STOPPING ***")
        sys.exit(2)
    s = s.replace(old, new, 1)
    print("applied")
    edits.append(label)


print("APPLYING:")

# ---- change 1: the URL-only strip -------------------------------------------
sub("1 shareableState + syncHash",
    'function syncHash(){\n'
    '  try{const token=base64urlEncode(serialisableState());',

    '/* THE URL IS A BROADCAST SURFACE.\n'
    '   syncHash() runs on 119 bench interactions and both the pupil-name and\n'
    '   reflection fields update state on every keystroke, so anything left in\n'
    '   `state` sits in the address bar for the whole session — browser history,\n'
    '   bookmarks, screen shares, a projector at the front of a classroom, and\n'
    '   any copied URL. Share is the loudest exit, not the only one.\n\n'
    '   serialisableState() is deliberately NOT changed: exportEvidence() calls\n'
    '   it too, and the evidence JSON legitimately carries the name because it is\n'
    '   a local download named after the pupil. Private in the URL, present in\n'
    '   the local download. The strip belongs here and only here.\n\n'
    '   The version tag is bumped on the URL payload alone, so a future reader\n'
    '   can tell a pre-fix link from a post-fix one. The export keeps "0.4". */\n'
    'function shareableState(){\n'
    '  const copy=serialisableState();\n'
    '  delete copy.pupil; delete copy.notes;\n'
    '  copy.version="0.4p1";\n'
    '  return copy;\n'
    '}\n'
    'function syncHash(){\n'
    '  try{const token=base64urlEncode(shareableState());')

# ---- change 2: neutralise links already minted ------------------------------
sub("2 loadHash deletes + accept 0.4p1",
    'const incoming=base64urlDecode(m[1]);if(!incoming||!["0.2","0.3","0.4"].includes(incoming.version))return false;',

    'const incoming=base64urlDecode(m[1]);if(!incoming||!["0.2","0.3","0.4","0.4p1"].includes(incoming.version))return false;'
    '/* Links minted before the privacy patch still carry a name and notes.\n'
    '       Accepting them keeps the experiment resumable; deleting these two\n'
    '       fields stops an old link from repopulating a pupil identity. */'
    'delete incoming.pupil;delete incoming.notes;')

# ---- change 3: make the guarantee visible -----------------------------------
sub("3 toast names the guarantee",
    'toast("Resumable lab link copied.");',
    'toast("Lab link copied \\u2014 the pupil\\u2019s name and notes are not included.");')

# ---- version strings (§0.5) --------------------------------------------------
sub("v label: <title>",
    '<title>Virtual Science Laboratory PRO v0.4 — Chemistry & Biology</title>',
    '<title>Virtual Science Laboratory PRO v0.4-privacy1 — Chemistry & Biology</title>')

sub("v label: <h1>",
    '<h1>Virtual Science Laboratory PRO v0.4</h1>',
    '<h1>Virtual Science Laboratory PRO v0.4-privacy1</h1>')

sub("v label: footer",
    'Prototype v0.4 · zero dependency',
    'Prototype v0.4-privacy1 · zero dependency')

# ---- header comment stating the version reasoning (§0.5) ---------------------
sub("header comment",
    '<!doctype html>\n',
    '<!doctype html>\n'
    '<!--\n'
    '  Virtual Science Laboratory PRO — v0.4-privacy1\n'
    '\n'
    '  NOT v0.4.1. In this estate "v0.4.1" means the patch order ran: P1-P9, all\n'
    '  six V-findings and three N-findings. Only P2 has run. Calling this v0.4.1\n'
    '  would guarantee a future reader concludes V1, V3, V4, V5, V6 and N1-N3 are\n'
    '  fixed when they are not.\n'
    '\n'
    '  What changed, and only this: the pupil name and reflection notes no longer\n'
    '  travel in the URL. They remain in the print pack and the evidence JSON\n'
    '  export, which are local and deliberate.\n'
    '\n'
    '  P2 IS HALF-IMPLEMENTED. phaseAnswers and drawing strokes are still in the\n'
    '  URL payload. They are the same principle at lower severity — not\n'
    '  identifying — and stripping strokes would make the reload cost far worse:\n'
    '  a lost drawing is lost work, a lost name is one retype. Their own change.\n'
    '\n'
    '  RELOAD COST, ACCEPTED: this file has zero storage APIs and the URL was the\n'
    '  only persistence, so a reload now loses the typed name and notes. Storage\n'
    '  was deliberately NOT added — on a shared classroom machine localStorage\n'
    '  would leave a pupil name for whoever sits down next. Print or Export\n'
    '  before reloading; both still carry the fields.\n'
    '\n'
    '  RESIDUE THAT CANNOT BE FIXED: links already minted, bookmarks already\n'
    '  saved and screenshots already taken are unrecoverable. This stops new\n'
    '  ones; it does not reach the old ones.\n'
    '\n'
    '  STILL NOT DEPLOYABLE. V1 still rewards the procedure it teaches against,\n'
    '  V5 still marks "the glowing splint does not relight" as correct, and N1\n'
    '  still deletes a pupil\'s oldest drawing stroke without a word.\n'
    '-->\n')

open(DST, 'w', encoding='utf-8').write(s)
b = open(DST, 'rb').read()
print(f"\n  edits applied: {len(edits)}")
print(f"  output: {DST}")
print(f"  bytes:  {len(b)}")
print(f"  lines:  {b.decode('utf-8').count(chr(10))}")
print(f"  sha256: {hashlib.sha256(b).hexdigest()}")
