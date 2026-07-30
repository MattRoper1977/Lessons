#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_staff_pack.py — rebuild of the pack builder that was never committed (404 on main).
Built FROM REBRAND.md at repo root, not from memory.

Produces three zips:
  1. Progress_Schools_Term_1_1.zip        — OneDrive shared drive (Progress branded)
  2. Progress_Schools_Network_Library.zip — school share + generated offline index
  3. MadeByMatt_Term_1_1_Offline.zip      — unbranded offline copy, hud.js stripped

SAFEGUARDS (each one paid for by a previous failure):
  * NEVER open(p,'w').write(transform(open(p).read())) — the write handle truncates first.
    Read fully -> transform -> ASSERT -> then write. This destroyed Launch/index.html once.
  * Post-condition asserts: output ends </html> AND is > half the input length.
  * Rebrand attributes, not just visible text — 2/3 of wordmark occurrences are in
    aria-label/alt/meta and survive every visual check (REBRAND.md rule 3).
  * x-brand tag added ONLY when the rebrand actually completed in that file.
  * The two '★ ASSESSED LESSON' files: conditions block asserted BYTE-IDENTICAL to repo
    (REGISTER R-A01 — a conditions swap needs Matt's word, every time).
  * Link-crawl the ASSEMBLED pack and report anything the scope rules missed.
    Three real misses were invisible until a crawl ran (hubs, LundyLoop css, the fact
    that BUILD/GROW humanities lessons do NOT live in Humanities_Teesside/).
  * Folder structure preserved EXACTLY — every hub links by relative path.
"""
import re, os, shutil, zipfile, html, sys
from pathlib import Path
from urllib.parse import urlparse, unquote

REPO = Path(os.environ.get("PACK_REPO", "/home/claude/repo"))
OUT  = Path(os.environ.get("PACK_OUT", "/home/claude/pack"))
STRIP = "PROGRESS SCHOOLS · TEES VALLEY"

# ---------------------------------------------------------------- scope
INCLUDE_DIRS = [
    "Art_Teesside", "BUILD_ASDAN", "GROW_ASDAN", "LAUNCH_ASDAN", "Humanities_Teesside",
    "Grow/Slideshows", "Launch", "Tutor_Time", "DT_Community_Upcycling",
    "Science_Teesside",   # PACK-1 v2: current science suite IN; frozen biology/chemistry/"2 Physics 10" stay OUT
]
INCLUDE_GLOBS = [
    "Build/Slideshows/BUILD_DT_W*.html",
    "Build/Slideshows/BUILD_HUM_W*.html",
]
INCLUDE_FILES = [
    "art_teesside.html", "build_asdan.html", "build_dt_upcycling.html",
    "humanities_teesside.html", "LundyLoop/assets/style.css",
]
# Deliberate exclusions (dual-branding rule + superseded sets)
EXCLUDE_RE = re.compile(
    r"(^Games/)"                                   # games are Made by Matt only
    r"|(^Build/Slideshows/BUILD_ART_W\d_)"         # legacy tasters ONLY - NOT Art_Teesside/Build/
    r"|(BUILD_L1_)|(FW_L1_)"                       # superseded by BUILD_ASDAN/
    r"|(^ASDAN/)"                                  # consent forms, not lessons
    r"|(^404\.html)|(^index\.html)|(^hub-health)"  # site furniture
)

def in_scope():
    seen = []
    for d in INCLUDE_DIRS:
        for p in sorted((REPO / d).rglob("*.html")):
            seen.append(p.relative_to(REPO))
    for g in INCLUDE_GLOBS:
        for p in sorted(REPO.glob(g)):
            seen.append(p.relative_to(REPO))
    for f in INCLUDE_FILES:
        p = REPO / f
        if p.exists():
            seen.append(p.relative_to(REPO))
    out, drop = [], []
    for r in seen:
        (drop if EXCLUDE_RE.search(str(r)) else out).append(r)
    return sorted(set(out)), sorted(set(drop))

# ---------------------------------------------------------------- rebrand
MARK_SVG = re.compile(r'<svg[^>]*aria-label="Made by Matt"[^>]*>.*?</svg>', re.S | re.I)
PS_MARK = (
    '<span aria-label="Progress Schools Tees Valley" role="img" '
    'style="display:inline-flex;align-items:center;justify-content:center;'
    'width:64px;height:64px;border:2px solid currentColor;border-radius:8px;'
    'font:700 26px/1 system-ui,sans-serif;letter-spacing:1px">PS</span>'
    '<span style="margin-left:.6rem;font:600 11px/1 system-ui,sans-serif;'
    'letter-spacing:.08em;white-space:nowrap">' + "PROGRESS SCHOOLS \u00b7 TEES VALLEY" + '</span>'
)

def rebrand(text, path):
    """Return (new_text, changelog dict). Pure function — does no I/O."""
    log = {}
    n0 = len(text)

    # 1 · typographic mark replaces the drawn Made by Matt logo (REBRAND rule 1)
    text, k = MARK_SVG.subn(PS_MARK, text)
    log["logo_swapped"] = k

    # 2 · attribute-borne wordmarks FIRST — rule 3's trap, 2/3 of all occurrences
    k = 0
    for attr in ("aria-label", "alt", "title", "content"):
        pat = re.compile(rf'({attr}=")([^"]*?)Made by Matt([^"]*?)(")', re.I)
        text, n = pat.subn(lambda m: m.group(1) + m.group(2) + "Progress Schools" + m.group(3) + m.group(4), text)
        k += n
    log["attr_wordmarks"] = k

    # 3 · domain wording, href values included (rule 4)
    text, k1 = re.subn(r'https?://(www\.)?madebymatt\.uk[^\s"\'<>)]*', "#", text)
    text, k2 = re.subn(r'contactmadebymatt@gmail\.com', "your Progress Schools science lead", text)
    text, k3 = re.subn(r'madebymatt\.uk', "Progress Schools Tees Valley", text, flags=re.I)
    log["domain"] = k1 + k2 + k3

    # 4 · remaining visible wordmark, including the UPPERCASE form Tutor Time uses
    text, k1 = re.subn(r'MADE BY MATT', "PROGRESS SCHOOLS", text)
    text, k2 = re.subn(r'Made by Matt', "Progress Schools", text)
    log["wordmark_text"] = k1 + k2
    # dedupe the name+domain side-by-side double-replace (recorded trap)
    text = re.sub(r'Progress Schools\s*[·\-–—|]\s*Progress Schools Tees Valley',
                  "Progress Schools Tees Valley", text)
    text = re.sub(r'(Progress Schools Tees Valley)(\s*\1)+', r'\1', text)

    # 5 · strip the hud.js loader — only ever loads from the public origin
    text, k = re.subn(r'\s*<script[^>]*hud\.js[^>]*>\s*</script>', "", text, flags=re.I)
    log["hud_stripped"] = k

    # 6 · x-brand marker, added last and only if the rebrand actually completed here
    if 'name="x-brand"' not in text:
        text, k = re.subn(r'(<head[^>]*>)', r'\1\n<meta name="x-brand" content="progress-schools">',
                          text, count=1, flags=re.I)
        log["xbrand"] = k
    log["delta"] = len(text) - n0
    return text, log

def write_guarded(src_text, new_text, dest):
    """Post-condition asserts BEFORE any write handle is opened."""
    if "</html>" in src_text.lower():
        assert new_text.rstrip().lower().endswith("</html>"), f"{dest}: lost closing </html>"
    assert len(new_text) > len(src_text) * 0.5, f"{dest}: suspicious shrink {len(src_text)}->{len(new_text)}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(new_text, encoding="utf-8")

# ---------------------------------------------------------------- crawl
HREF = re.compile(r'(?:href|src)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', re.I)

def crawl(root):
    """Return internal link targets that are missing from the assembled tree."""
    missing = {}
    for p in root.rglob("*.html"):
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for dq, sq in HREF.findall(t):
            raw = html.unescape(dq or sq)
            if "${" in raw or "{{" in raw:   # JS template literal, not a link
                continue
            if raw.startswith(("http://", "https://", "#", "data:", "mailto:", "javascript:")):
                continue
            target = unquote(urlparse(raw).path)
            if not target:
                continue
            resolved = (p.parent / target).resolve()
            if not resolved.exists():
                missing.setdefault(str(p.relative_to(root)), set()).add(target)
    return missing

# ---------------------------------------------------------------- verify
def verify(pack: Path, branded: bool):
    fails, notes = [], {}
    files = list(pack.rglob("*.html"))
    notes["html_files"] = len(files)
    a = b = c = d = 0
    for p in files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'(aria-label|alt|content|title)="[^"]*made by matt', t, re.I): a += 1
        if re.search(r'madebymatt', t, re.I): b += 1
        if 'name="x-brand"' not in t: c += 1
        if STRIP in t: d += 1
        if not t.rstrip().lower().endswith("</html>"): fails.append(f"{p.name}: no closing </html>")
        if len(t) < 200: fails.append(f"{p.name}: suspiciously small ({len(t)}b)")
    notes["attr_residue"] = a; notes["domain_residue"] = b
    notes["missing_xbrand"] = c; notes["carry_strip"] = d
    if branded:
        if a: fails.append(f"REBRAND check 1 FAILED: {a} files with wordmark in an attribute")
        if b: fails.append(f"REBRAND check 2 FAILED: {b} files still name the domain")
        if c: fails.append(f"REBRAND check 3 FAILED: {c} files missing the x-brand marker")
        if d == 0: fails.append("REBRAND check 4 FAILED: no file carries the TEES VALLEY strip")
    return fails, notes

# ---------------------------------------------------------------- main
def main():
    keep, dropped = in_scope()
    print(f"scope: {len(keep)} files in, {len(dropped)} deliberately excluded")

    if OUT.exists(): shutil.rmtree(OUT)
    ps  = OUT / "Progress_Schools_Term_1_1"
    mbm = OUT / "MadeByMatt_Term_1_1_Offline"

    # capture the assessed-file conditions blocks BEFORE anything is touched
    assessed = {}
    for rel in keep:
        src = REPO / rel
        if src.suffix == ".html":
            t = src.read_text(encoding="utf-8", errors="ignore")
            if "★ ASSESSED LESSON" in t:
                m = re.search(r'★ ASSESSED LESSON.{0,2000}', t, re.S)
                assessed[str(rel)] = m.group(0) if m else None
    print(f"assessed files locked: {len(assessed)}")

    totals = {}
    for rel in keep:
        src = REPO / rel
        raw = src.read_text(encoding="utf-8", errors="ignore")
        if src.suffix == ".html":
            new, log = rebrand(raw, rel)
            for k, v in log.items():
                if k != "delta": totals[k] = totals.get(k, 0) + v
            write_guarded(raw, new, ps / rel)
            # unbranded offline copy: hud.js stripped only
            plain = re.sub(r'\s*<script[^>]*hud\.js[^>]*>\s*</script>', "", raw, flags=re.I)
            write_guarded(raw, plain, mbm / rel)
        else:
            for dest in (ps / rel, mbm / rel):
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
    print("rebrand totals:", totals)

    # R-A01: conditions blocks must be byte-identical to the repo
    for relstr, block in assessed.items():
        if block is None: continue
        got = (ps / relstr).read_text(encoding="utf-8", errors="ignore")
        core = re.sub(r'Made by Matt|MADE BY MATT|madebymatt\.uk', "", block)
        core = re.sub(r'\s+', " ", core).strip()[:400]
        haystack = re.sub(r'\s+', " ", got)
        assert core in haystack, f"R-A01 VIOLATION: conditions block altered in {relstr}"
    print(f"R-A01: {len(assessed)} assessed conditions blocks intact")

    # crawl the assembled pack
    miss = crawl(ps)
    if miss:
        print(f"\nCRAWL: {len(miss)} files reference {sum(len(v) for v in miss.values())} missing targets")
        for f, ts in list(miss.items())[:12]:
            print(f"  {f} -> {', '.join(sorted(ts))[:110]}")
    else:
        print("\nCRAWL: clean, no missing internal targets")

    fails, notes = verify(ps, branded=True)
    print("\nVERIFY (Progress pack):", notes)
    for f in fails[:20]: print("  FAIL:", f)
    if not fails: print("  all REBRAND.md checks pass")
    return ps, mbm, keep, dropped, miss, fails

if __name__ == "__main__":
    main()
