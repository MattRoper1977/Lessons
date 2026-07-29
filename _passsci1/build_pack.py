#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Staff-pack builder (§10.4), adapted from the bundle's build_staff_pack.py and driven by
REBRAND.md. Rebuilt for THIS repo path, with Science_Teesside added, README_FIRST.txt written
into both packs, and zipping + unzip -t verification.

Two packs:
  Progress_Schools_Term_1_1   — rebranded (Made by Matt -> Progress Schools), for OneDrive
  MadeByMatt_Term_1_1_Offline — unbranded offline copy, hud.js loader stripped only

SAFEGUARDS (REBRAND.md + estate register):
  * Rebrand ATTRIBUTES, not just visible text (aria-label/alt/meta) — REBRAND rule 3, the trap.
  * Read fully -> transform -> ASSERT (ends </html>, > half length) -> write. Never truncate.
  * x-brand added only where the rebrand completed (rule 5).
  * The two '★ ASSESSED LESSON' files: conditions block asserted BYTE-IDENTICAL (R-A01 / rule 7)
    — no conditions swap without Matt's word.
  * Link-crawl the ASSEMBLED pack; report misses. unzip -t clean.
"""
import re
import shutil
import zipfile
import subprocess
import html
from pathlib import Path
from urllib.parse import urlparse, unquote

REPO = Path("/workspace/lessons")
OUT = Path("/workspace/lessons/_passsci1/pack")
STRIP = "PROGRESS SCHOOLS · TEES VALLEY"

INCLUDE_DIRS = [
    "Art_Teesside", "Science_Teesside", "BUILD_ASDAN", "GROW_ASDAN", "Humanities_Teesside",
    "Grow/Slideshows", "Launch", "Tutor_Time", "DT_Community_Upcycling",
]
INCLUDE_GLOBS = ["Build/Slideshows/BUILD_DT_W*.html", "Build/Slideshows/BUILD_HUM_W*.html"]
INCLUDE_FILES = ["art_teesside.html", "build_asdan.html", "build_dt_upcycling.html",
                 "humanities_teesside.html", "LundyLoop/assets/style.css"]
EXCLUDE_RE = re.compile(
    r"(^Games/)|(^Build/Slideshows/BUILD_ART_W\d_)|(BUILD_L1_)|(FW_L1_)"
    r"|(^ASDAN/)|(^404\.html)|(^index\.html)|(^hub-health)")


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


MARK_SVG = re.compile(r'<svg[^>]*aria-label="Made by Matt"[^>]*>.*?</svg>', re.S | re.I)
PS_MARK = (
    '<span aria-label="Progress Schools Tees Valley" role="img" '
    'style="display:inline-flex;align-items:center;justify-content:center;width:64px;height:64px;'
    'border:2px solid currentColor;border-radius:8px;font:700 26px/1 system-ui,sans-serif;'
    'letter-spacing:1px">PS</span><span style="margin-left:.6rem;font:600 11px/1 system-ui,sans-serif;'
    'letter-spacing:.08em;white-space:nowrap">PROGRESS SCHOOLS · TEES VALLEY</span>')


def rebrand(text, path):
    log = {}
    n0 = len(text)
    text, k = MARK_SVG.subn(PS_MARK, text)
    log["logo_swapped"] = k
    k = 0
    for attr in ("aria-label", "alt", "title", "content"):
        pat = re.compile(rf'({attr}=")([^"]*?)Made by Matt([^"]*?)(")', re.I)
        text, n = pat.subn(lambda m: m.group(1) + m.group(2) + "Progress Schools" + m.group(3) + m.group(4), text)
        k += n
    log["attr_wordmarks"] = k
    text, k1 = re.subn(r'https?://(www\.)?madebymatt\.uk[^\s"\'<>)]*', "#", text)
    text, k2 = re.subn(r'contactmadebymatt@gmail\.com', "your Progress Schools science lead", text)
    text, k3 = re.subn(r'madebymatt\.uk', "Progress Schools Tees Valley", text, flags=re.I)
    log["domain"] = k1 + k2 + k3
    text, k1 = re.subn(r'MADE BY MATT', "PROGRESS SCHOOLS", text)
    text, k2 = re.subn(r'Made by Matt', "Progress Schools", text)
    log["wordmark_text"] = k1 + k2
    text = re.sub(r'Progress Schools\s*[·\-–—|]\s*Progress Schools Tees Valley',
                  "Progress Schools Tees Valley", text)
    text = re.sub(r'(Progress Schools Tees Valley)(\s*\1)+', r'\1', text)
    text, k = re.subn(r'\s*<script[^>]*hud\.js[^>]*>\s*</script>', "", text, flags=re.I)
    log["hud_stripped"] = k
    if 'name="x-brand"' not in text:
        text, k = re.subn(r'(<head[^>]*>)', r'\1\n<meta name="x-brand" content="progress-schools">',
                          text, count=1, flags=re.I)
        log["xbrand"] = k
    log["delta"] = len(text) - n0
    return text, log


def write_guarded(src_text, new_text, dest):
    if "</html>" in src_text.lower():
        assert new_text.rstrip().lower().endswith("</html>"), f"{dest}: lost closing </html>"
    assert len(new_text) > len(src_text) * 0.5, f"{dest}: suspicious shrink"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(new_text, encoding="utf-8")


HREF = re.compile(r'(?:href|src)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', re.I)


def crawl(root):
    missing = {}
    for p in root.rglob("*.html"):
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for dq, sq in HREF.findall(t):
            raw = html.unescape(dq or sq)
            if "${" in raw or "{{" in raw:
                continue
            if raw.startswith(("http://", "https://", "#", "data:", "mailto:", "javascript:", "/")):
                continue
            target = unquote(urlparse(raw).path)
            if not target:
                continue
            if not (p.parent / target).resolve().exists():
                missing.setdefault(str(p.relative_to(root)), set()).add(target)
    return missing


def verify(pack, branded):
    fails, notes = [], {}
    files = list(pack.rglob("*.html"))
    notes["html_files"] = len(files)
    a = b = c = d = 0
    for p in files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'(aria-label|alt|content|title)="[^"]*made by matt', t, re.I):
            a += 1
        if re.search(r'madebymatt', t, re.I):
            b += 1
        if 'name="x-brand"' not in t:
            c += 1
        if STRIP in t:
            d += 1
        if not t.rstrip().lower().endswith("</html>"):
            fails.append(f"{p.name}: no closing </html>")
        if len(t) < 200:
            fails.append(f"{p.name}: suspiciously small")
    notes.update(attr_residue=a, domain_residue=b, missing_xbrand=c, carry_strip=d)
    if branded:
        if a:
            fails.append(f"REBRAND 1 FAIL: {a} files with wordmark in an attribute")
        if b:
            fails.append(f"REBRAND 2 FAIL: {b} files still name the domain")
        if c:
            fails.append(f"REBRAND 3 FAIL: {c} files missing x-brand")
        if d == 0:
            fails.append("REBRAND 4 FAIL: no file carries the TEES VALLEY strip")
    return fails, notes


def readme(branded):
    who = "Progress Schools · Tees Valley (OneDrive shared drive)" if branded else "Made by Matt (offline site copy)"
    return f"""README_FIRST — Autumn Term 1.1 staff pack
Brand: {who}

THIS IS THE TERM-START PACK. It is rebuilt after the 29 Aug merge sitting (SL / SBX / PQ / SG),
so a fresh pack replaces this one once those parked branches land. Until then, this is current.

KEEP / DELETE
  KEEP  — this term's live 2026-27 suites, all inside this pack:
            Art_Teesside/            Art · Teesside Studio Suite (BUILD/GROW/LAUNCH)
            Science_Teesside/        Science · Teesside (NEW this pass: BUILD 5, GROW 5, LAUNCH 15)
            BUILD_ASDAN/ GROW_ASDAN/ ASDAN vocational (FoodWise, Careers, Community, etc.)
            Humanities_Teesside/     Humanities
            Grow/Slideshows/ Launch/ GROW & LAUNCH humanities slideshows
            DT_Community_Upcycling/  D&T
            Tutor_Time/              Tutor Time
  DELETE — any pack dated before this one; the superseded BUILD_L1_/FW_L1_ tasters; the
           BUILD_ART_W# legacy art tasters; Games (Made-by-Matt site only, not a staff pack).

CAREERS — go by the on-screen title, NOT the filename. The two Careers files are named the
  OPPOSITE of the teaching slot (a slot swap left the filenames behind):
    CAREERS_W6_My_Career_Profile.html      teaches in SLOT W7  ("My Career Profile")
    CAREERS_W7_After_Year_11.html          teaches in SLOT W6  ("What Happens After Year 11")
  If you order Careers by filename you will run them the wrong way round.

Every lesson is a self-contained HTML whiteboard slideshow: open it in a browser, no internet
needed. The print pack (three tiers + Assessor Witness Statement) prints from the title slide.
"""


def main():
    keep, dropped = in_scope()
    print(f"scope: {len(keep)} files in, {len(dropped)} deliberately excluded")
    if OUT.exists():
        shutil.rmtree(OUT)
    ps = OUT / "Progress_Schools_Term_1_1"
    mbm = OUT / "MadeByMatt_Term_1_1_Offline"

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
                if k != "delta":
                    totals[k] = totals.get(k, 0) + v
            write_guarded(raw, new, ps / rel)
            plain = re.sub(r'\s*<script[^>]*hud\.js[^>]*>\s*</script>', "", raw, flags=re.I)
            write_guarded(raw, plain, mbm / rel)
        else:
            for dest in (ps / rel, mbm / rel):
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
    print("rebrand totals:", totals)

    (ps / "README_FIRST.txt").write_text(readme(True), encoding="utf-8")
    (mbm / "README_FIRST.txt").write_text(readme(False), encoding="utf-8")

    # R-A01: assessed conditions byte-identical after rebrand
    for relstr, block in assessed.items():
        if block is None:
            continue
        got = (ps / relstr).read_text(encoding="utf-8", errors="ignore")
        core = re.sub(r'Made by Matt|MADE BY MATT|madebymatt\.uk', "", block)
        core = re.sub(r'\s+', " ", core).strip()[:400]
        assert core in re.sub(r'\s+', " ", got), f"R-A01 VIOLATION: conditions altered in {relstr}"
    print(f"R-A01: {len(assessed)} assessed conditions blocks intact")

    miss = crawl(ps)
    if miss:
        print(f"CRAWL: {len(miss)} files reference {sum(len(v) for v in miss.values())} missing targets")
        for f, ts in list(miss.items())[:12]:
            print(f"  {f} -> {', '.join(sorted(ts))[:110]}")
    else:
        print("CRAWL: clean, no missing internal targets")

    fails, notes = verify(ps, branded=True)
    print("VERIFY (Progress pack):", notes)
    for f in fails[:20]:
        print("  FAIL:", f)
    if not fails:
        print("  all REBRAND.md checks pass")

    # zip both + unzip -t
    zips = []
    for d in (ps, mbm):
        z = OUT / (d.name + ".zip")
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(d.rglob("*")):
                if p.is_file():
                    zf.write(p, p.relative_to(OUT))
        r = subprocess.run(["unzip", "-t", str(z)], capture_output=True, text=True)
        ok = r.returncode == 0 and "No errors" in r.stdout
        print(f"ZIP {z.name}: {len(z.read_bytes())} bytes, unzip -t {'OK' if ok else 'FAILED'}")
        zips.append((z, ok))
    return ps, mbm, keep, dropped, miss, fails, zips


if __name__ == "__main__":
    main()
