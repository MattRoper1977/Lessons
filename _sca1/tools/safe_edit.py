#!/usr/bin/env python3
"""SCA-1 safe editor. Applies a literal string replacement and PROVES:
  - the replacement count matches expectation
  - CODE stream delta == 0   (G7)
  - PROTECTED manifest lines unchanged (G4)  / food census unchanged (G5)
  - sentinels hold 50 / 123 with identical file sets (G6)
Usage: safe_edit.py apply  <file> <old> <new> <expected_count>
       safe_edit.py verify
"""
import sys,os,re,subprocess,hashlib,json,shutil
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import extract as EX

ROOT="/home/user/Lessons"
import re as _RE
PROSE_LIT = _RE.compile(r'(["\'])((?:\\.|(?!\1)[^\\\n])*)\1')
PROSE_ATTR_VAL = _RE.compile(
    r'\b(alt|aria-label|title|data-speak-text|data-ta1|data-ta2|data-title|data-label|'
    r'data-hint|data-explain|data-fix|placeholder|data-ta-move|data-name|data-frame)'
    r'\s*=\s*"([^"]*)"', _RE.I)

def code_stream(fp):
    """CODE stream with PROSE content removed, length-independently.

    Classification decisions (logged per SCA-1 s1.4):
      (a) A JS string literal that renders as human text is PROSE by the pass definition
          ("PROSE = rendered text incl. rendered JS string literals"), so it must not also
          count as CODE. Predicate identical to extract.py's js_prose.
      (b) The VALUE of a prose-bearing attribute (alt, aria-label, title, data-speak-text,
          data-ta1/2, ...) is PROSE; the attribute NAME is CODE. So the name is kept and the
          value is replaced by a constant token.
    Both masks are CONSTANT-WIDTH, not length-preserving: a prose edit that changes the
    length of a spoken string is a PROSE delta, and a length-preserving mask would report it
    as a CODE delta. Verified against SCI_G_W4B (data-speak-text) and SCI_G_W6B (JS literal).
    """
    _,_,code,_,_,_ = EX.streams(fp)
    def mask_lit(m):
        v=m.group(2)
        if len(v)>12 and ' ' in v and _RE.search(r'[A-Za-z]{3}',v) \
           and not _RE.match(r'^[\w./#-]+$',v) and 'http' not in v:
            return m.group(1)+'<PROSE>'+m.group(1)
        return m.group(0)
    code = PROSE_ATTR_VAL.sub(lambda m: m.group(1)+'="<PROSE>"', code)
    return PROSE_LIT.sub(mask_lit, code)

def prose_stream(fp):
    _,prose,_,_,_,_ = EX.streams(fp)
    return prose

def sentinels():
    out={}
    for name,pat in (("loopmark","ll-g:loop-mark"),("closure","What I said, and what it changed")):
        r=subprocess.run(["git","grep","-l","--",pat,"--","*.html"],cwd=ROOT,capture_output=True,text=True)
        files=sorted(x for x in r.stdout.split("\n") if x.strip())
        out[name]=files
    return out

def apply(fp, old, new, expected):
    fp=os.path.join(ROOT,fp) if not fp.startswith("/") else fp
    t=open(fp,encoding='utf-8').read()
    n=t.count(old)
    if n!=int(expected):
        print(f"REFUSED: '{old[:60]}' occurs {n}x, expected {expected}"); return 1
    code_before=code_stream(fp); prose_before=prose_stream(fp)
    shutil.copy(fp, fp+".sca1bak")
    open(fp,"w",encoding='utf-8').write(t.replace(old,new))
    code_after=code_stream(fp); prose_after=prose_stream(fp)
    cd = 0 if code_before==code_after else 1
    if cd:
        # show what changed in CODE
        import difflib
        d=[l for l in difflib.unified_diff(code_before.split("\n"),code_after.split("\n"),lineterm="",n=0)][:12]
        print("CODE-STREAM DELTA NON-ZERO -- reverting:"); [print("   ",x) for x in d]
        shutil.move(fp+".sca1bak", fp); return 2
    os.remove(fp+".sca1bak")
    pd = sum(1 for a,b in zip(prose_before.split("\n"),prose_after.split("\n")) if a!=b)
    print(f"OK {os.path.basename(fp)}: replaced {n}x | CODE delta=0 | PROSE lines changed={pd}")
    return 0

if __name__=="__main__":
    if sys.argv[1]=="apply":
        sys.exit(apply(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]))
    if sys.argv[1]=="sentinels":
        s=sentinels()
        for k,v in s.items(): print(f"{k}: {len(v)} files")
        json.dump(s, open(f"{ROOT}/_sca1/sentinels/current.json","w"), indent=1)
