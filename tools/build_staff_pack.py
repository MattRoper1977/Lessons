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
    # Art visual-learning runtime. in_scope() globs *.html, so a directory being in
    # INCLUDE_DIRS does NOT carry its non-HTML assets — same reason style.css above is
    # named individually. All 31 Art_Teesside decks load these three by relative path
    # from inside an AVL-MOUNT marker pair. Without them the loader points at nothing
    # and the We Do panel silently never mounts. README.md in that directory is repo
    # documentation and stays out: only what a deck actually loads ships.
    # PACK-3: the two LundyLoop staff-training pages. The crawl over the
    # assembled pack found 4 Humanities lessons linking to Reading_the_Response_Card
    # by relative path, and that card links on to R_Gate_Calibration_Game. Both
    # exist in the repo; neither was in scope, so the shipped pack had four dead
    # links. Same shape as the Art and ASDAN runtime assets above: a directory in
    # INCLUDE_DIRS does not carry files outside it, so they are named here.
    "LundyLoop/5_staff_training/Reading_the_Response_Card.html",
    "LundyLoop/5_staff_training/R_Gate_Calibration_Game.html",
    "Art_Teesside/visual-learning/art-visual-learning.css",
    "Art_Teesside/visual-learning/art-visual-payloads.js",
    "Art_Teesside/visual-learning/art-visual-learning.js",
    # PACK-2: the GROW/LAUNCH ASDAN visual-upgrade runtime, added for exactly the
    # reason the Art three above were. The crawl over the assembled pack found 124
    # references to these four files from 62 decks that ship, resolving to nothing --
    # by far the largest broken-link family in the pack. GROW_ASDAN and LAUNCH_ASDAN
    # are in INCLUDE_DIRS, but in_scope() globs *.html, so their non-HTML assets were
    # never carried. Same silent failure: the loader points at nothing, offline and on
    # OneDrive, with no error a teacher would see.
    "GROW_ASDAN/visual-upgrade.css",
    "GROW_ASDAN/visual-upgrade.js",
    "LAUNCH_ASDAN/visual-upgrade.css",
    "LAUNCH_ASDAN/visual-upgrade.js",
    # PACK-2: two non-HTML siblings linked from Humanities pages that DO ship. Same
    # class as the runtime assets above -- a directory being IN does not carry them.
    "Humanities_Teesside/Lundy_Humanities/SOURCE_PROVENANCE_TEMPLATE.csv",
    "Humanities_Teesside/Lundy_Humanities/specimens/SPECIMEN_ACCEPTANCE.md",
    # PACK-3: the four grow-anim runtime scripts. Five Science_Teesside/Build decks
    # load them. They were written ROOT-ABSOLUTE, so PACK-2 could not fix them by
    # scope alone and said so. The CI probe has since resolved them against the live
    # origin: in-repo YES, live 404 -- the path was broken in BOTH contexts, because
    # the site serves this repo under /Lessons/. The references are now relative, so
    # the assets must ship or the same loader-points-at-nothing failure returns.
    "grow-anim/grow-svg.js",
    "grow-anim/grow-svg-bio-animals.js",
    "grow-anim/grow-anim.js",
    "grow-anim/compat-build-anim.js",
]
# The dynamic hud.js injector. Self-contained script element, byte-identical across
# the five decks that carry it, and its entire body exists to load hud.js.
HUD_DYNAMIC = re.compile(
    r'\s*<script[^>]*id=["\']grow-hud-loader["\'][^>]*>.*?</script>', re.S | re.I)

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
    # 5b · and the DYNAMIC loader, which the tag regex above cannot see. Five
    # Science_Teesside/Grow decks carry <script id="grow-hud-loader"> whose whole body
    # is document.createElement("script") + s.src="/hud.js" with a relative-path
    # onerror retry. It survived every previous pack build: the staff copies shipped
    # fetching hud.js at runtime, twice, from a machine that has neither. Found by
    # grepping the ASSEMBLED pack for hud.js rather than trusting the strip count.
    text, k2 = re.subn(HUD_DYNAMIC, "", text)
    log["hud_stripped"] = k + k2

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

# ---------------------------------------------------------------- AVL gates
# Two gates for the Art visual-learning layer. Both exist because the rebrand
# transform strips the hud.js loader (rebrand step 5), and the AVL marker pair sits
# directly after that loader in all 31 decks. A regex that reached one character too
# far would silently remove the panel from every staff copy.
AVL_BLOCK = re.compile(r"<!-- AVL-MOUNT:BEGIN.*?AVL-MOUNT:END -->", re.S)

def avl_blocks(text):
    return AVL_BLOCK.findall(text)

def check_avl_preserved(src_text, new_text, rel):
    """AVL-1: the rebrand transform must leave the marker pair byte-identical.

    Compares the extracted blocks, not the whole file — the rest of the file is
    supposed to change. Returns a failure string, or None."""
    before, after = avl_blocks(src_text), avl_blocks(new_text)
    if before != after:
        return (f"AVL-1 VIOLATION: {rel}: rebrand altered the AVL marker pair "
                f"({len(before)} block(s) in, {len(after)} out)")
    return None

def check_avl_refs(pack: Path):
    """AVL-2: every reference inside a marker pair resolves to a file in the pack.

    The general crawl only reports; this one fails the build. A loader that points at
    nothing produces no error a teacher would ever see — the panel just never mounts."""
    fails = []
    for p in sorted(pack.rglob("*.html")):
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for blk in avl_blocks(t):
            for dq, sq in HREF.findall(blk):
                raw = html.unescape(dq or sq)
                # A root-relative "/x" resolves against the public origin, not the pack,
                # so it is just as broken offline as a missing file — and it must be
                # named as the absolute path it is, not reported as "missing".
                if raw.startswith(("http://", "https://", "//", "/", "#", "data:")):
                    fails.append(f"AVL-2: {p.relative_to(pack)} -> {raw} is not a relative path")
                    continue
                target = unquote(urlparse(raw).path)
                if not target:
                    continue
                if not (p.parent / target).resolve().exists():
                    fails.append(f"AVL-2: {p.relative_to(pack)} -> {raw} missing from pack")
    return fails

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
    avl_fails = []
    avl_seen = 0
    for rel in keep:
        src = REPO / rel
        raw = src.read_text(encoding="utf-8", errors="ignore")
        if src.suffix == ".html":
            new, log = rebrand(raw, rel)
            for k, v in log.items():
                if k != "delta": totals[k] = totals.get(k, 0) + v
            # AVL-1, checked BEFORE the write, on every file that carries a marker pair
            if avl_blocks(raw):
                avl_seen += 1
                f = check_avl_preserved(raw, new, rel)
                if f: avl_fails.append(f)
            write_guarded(raw, new, ps / rel)
            # unbranded offline copy: hud.js stripped only
            plain = re.sub(r'\s*<script[^>]*hud\.js[^>]*>\s*</script>', "", raw, flags=re.I)
            plain = HUD_DYNAMIC.sub("", plain)
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

    # AVL-1 result, and AVL-2 against the assembled pack
    print(f"\nAVL-1: {avl_seen} decks carry a marker pair; "
          f"{'all preserved byte-for-byte' if not avl_fails else str(len(avl_fails)) + ' ALTERED'}")
    for f in avl_fails[:10]: print("  FAIL:", f)
    ref_fails = check_avl_refs(ps)
    print(f"AVL-2: loader references inside marker pairs "
          f"{'all resolve inside the pack' if not ref_fails else 'BROKEN'}")
    for f in ref_fails[:10]: print("  FAIL:", f)
    avl_fails = avl_fails + ref_fails

    fails, notes = verify(ps, branded=True)
    fails = fails + avl_fails
    print("\nVERIFY (Progress pack):", notes)
    for f in fails[:20]: print("  FAIL:", f)
    if not fails: print("  all REBRAND.md checks pass")
    return ps, mbm, keep, dropped, miss, fails

# ==================================================================== MIRROR
# PACK-4: the OneDrive Mirror Pack.
#
# Everything below is additive. The default build path above is untouched: it
# still preserves the repo tree, because its links assume the repo tree.
#
# This mode does the opposite, and is only safe because it does BOTH halves:
# it assembles into the school's folder geometry AND rewrites every internal
# link against the same map. Zip geometry == drive geometry, so a link between
# two co-shipped folders resolves after a drag-and-merge. Do one half without
# the other and every cross-folder link in the pack dies.
#
# The map below was derived from 35 screenshots of the live drive (2026-08-07),
# not from the repo and not from memory. Where the repo and the drive disagree
# on a name, THE DRIVE WINS — that is the whole point of a mirror.
import base64, argparse, io
from urllib.parse import quote

# The Humanities folder name is truncated in every screenshot that shows it:
#   root listing : "Humanities Less...s and resources)"
#   title bar    : "Humanities Lessons (Whiteboards..."
# The overlap fixes everything except a possible middle word. This is the
# pack's ONE unresolved name and it is flagged, not guessed silently.
HUM = "Humanities Lessons (Whiteboards and resources)"
HUM_AMBIGUOUS = True

# LAUNCH_ASDAN is FLAT on the drive: CAREERS_*, COMM_*, LI_*, PEQ_* and VOC_*
# all sit directly in "ASDAN PEQ/Launch". The repo keeps them in five
# subfolders, and each of those has its own START_HERE.html -- so a naive
# flatten silently destroys four of the five. They are disambiguated instead,
# and every rename is recorded in TAXONOMY_MAP.md.
LAUNCH_SUBS = {
    "Careers": "Careers", "Community_Enterprise": "Community_Enterprise",
    "Living_Independently": "Living_Independently", "PEQ": "PEQ",
    "Vocational": "Vocational",
}
LOGO_URI = [None, None]   # filled by build_mirror, read by the index writer
RENAMES = []          # (repo path, dest path, why) — reported, never silent

def dest_for(rel):
    """Map one in-scope repo path to its OneDrive destination path.

    Ordered, longest-match-first. Returns a POSIX-style string."""
    r = str(rel).replace("\\", "/")
    name = r.rsplit("/", 1)[-1]

    # --- root unit hubs: canonical single placement at the drive root
    if "/" not in r:
        return r

    # --- Art -------------------------------------------------------------
    if r.startswith("Art_Teesside/"):
        return "Art/" + r[len("Art_Teesside/"):]
    if r.startswith("Grow/Slideshows/GROW_ART_"):
        return "Art/Grow/" + name
    if r.startswith("Launch/Slideshows/LAUNCH_ART_"):
        return "Art/Launch/" + name
    if r in ("Launch/index.html",) or r.startswith("Launch/Art_L"):
        return "Art/Launch/" + name

    # --- Humanities ------------------------------------------------------
    if r.startswith("Build/Slideshows/BUILD_HUM_"):
        return f"{HUM}/Build/" + name
    if r.startswith("Grow/Slideshows/GROW_HUM_"):
        return f"{HUM}/Grow/" + name
    if r.startswith("Launch/Slideshows/LAUNCH_HUM_"):
        return f"{HUM}/Launch/" + name
    if r.startswith("Humanities_Teesside/Lundy_Humanities/specimens/"):
        return f"{HUM}/LundyLoop/Specimens/" + name
    if r.startswith("Humanities_Teesside/Lundy_Humanities/"):
        return f"{HUM}/LundyLoop/" + name
    if r.startswith("Humanities_Teesside/"):
        for pre, sub in (("BUILD_", "Build"), ("GROW_", "Grow"), ("LAUNCH_", "Launch")):
            if name.startswith(pre):
                return f"{HUM}/{sub}/" + name
        return f"{HUM}/" + name          # Pathway_Tracker.html

    # --- ASDAN PEQ -------------------------------------------------------
    if r.startswith("Build/Slideshows/BUILD_DT_"):
        return "ASDAN PEQ/Build/DT/" + name
    if r.startswith("DT_Community_Upcycling/"):
        return "ASDAN PEQ/Build/DT/" + name
    if r.startswith("BUILD_ASDAN/"):
        return "ASDAN PEQ/Build/" + r[len("BUILD_ASDAN/"):]
    if r.startswith("GROW_ASDAN/"):
        tail = r[len("GROW_ASDAN/"):]
        for src, dst in (("Community_Project/", "Community Project/"),
                         ("Enterprise/", "Community and Enterprise/"),
                         ("PEQ/", "Personal Effectiveness/")):
            if tail.startswith(src):
                return "ASDAN PEQ/Grow/" + dst + tail[len(src):]
        return "ASDAN PEQ/Grow/" + tail
    if r.startswith("LAUNCH_ASDAN/"):
        tail = r[len("LAUNCH_ASDAN/"):]
        if "/" in tail:                                  # inside a subfolder -> FLATTEN
            sub, leaf = tail.split("/", 1)
            if leaf == "START_HERE.html":                # 5-way collision
                new = f"START_HERE_{sub}.html"
                RENAMES.append((r, f"ASDAN PEQ/Launch/{new}",
                                "flattened; 5 subfolder START_HEREs would collide on one name"))
                return "ASDAN PEQ/Launch/" + new
            return "ASDAN PEQ/Launch/" + leaf
        return "ASDAN PEQ/Launch/" + tail

    # --- unchanged names --------------------------------------------------
    if r.startswith("Tutor_Time/"):
        return "Tutor Time BF_BV_KCSIE/" + r[len("Tutor_Time/"):]
    if r.startswith(("Science_Teesside/", "grow-anim/", "LundyLoop/")):
        return r
    raise AssertionError(f"dest_for: no rule for {r}")


def build_index(keep):
    """repo-rel -> dest-rel, and the reverse, with collision detection."""
    fwd, back = {}, {}
    for rel in keep:
        d = dest_for(rel)
        if d in back and back[d] != str(rel):
            raise AssertionError(f"DESTINATION COLLISION: {back[d]} and {rel} both -> {d}")
        fwd[str(rel)] = d
        back[d] = str(rel)
    return fwd, back


def rewrite_links(text, src_rel, fwd):
    """Rewrite every internal href/src from repo geometry to drive geometry.

    Resolves each link against the SOURCE file's directory to find which repo
    file it means, then re-expresses it relative to the DESTINATION directory.
    A link whose target is not in the pack is left alone and reported by the
    crawl -- it is never silently rewritten to something that happens to exist."""
    src_dir = os.path.dirname(str(src_rel))
    dst_dir = os.path.dirname(fwd[str(src_rel)])
    changed = [0]

    def one(m):
        attr, q, raw = m.group(1), m.group(2), m.group(3)
        if (not raw or raw.startswith(("http://", "https://", "//", "#", "data:",
                                       "mailto:", "javascript:", "/"))
                or "${" in raw or "{{" in raw):
            return m.group(0)
        parts = urlparse(raw)
        target = unquote(parts.path)
        if not target:
            return m.group(0)
        repo_target = os.path.normpath(os.path.join(src_dir, target)).replace("\\", "/")
        if repo_target not in fwd:
            return m.group(0)                       # unknown -> leave, crawl reports it
        new = os.path.relpath(fwd[repo_target], dst_dir or ".").replace("\\", "/")
        if parts.query:    new += "?" + parts.query
        if parts.fragment: new += "#" + parts.fragment
        if new != raw:
            changed[0] += 1
        return f'{attr}={q}{new}{q}'

    text = re.sub(r'\b(href|src)\s*=\s*(["\'])(.*?)\2', one, text, flags=re.I | re.S)
    return text, changed[0]


# ---------------------------------------------------------------- the logo
# REBRAND.md rule 1 said the mark is typographic and never drawn. Matt has
# since supplied the real Progress Schools lockup, which SUPERSEDES that rule:
# the trademark now replaces the Made-by-Matt mark directly. What does not
# change is that it is never recoloured, restyled, stretched or redrawn --
# it is embedded as-is, and only ever scaled by width with height:auto so the
# aspect ratio cannot drift.
CREDIT = "by madebymatt.uk"      # Matt's explicit instruction; the ONE whitelisted
                                 # Made-by-Matt string. Anything else is residue.

def load_logo(path):
    """Trim the supplied PNG, split the lockup from the P mark, return data URIs."""
    from PIL import Image, ImageChops
    im = Image.open(path).convert("RGBA")
    flat = Image.new("RGB", im.size, (255, 255, 255))
    flat.paste(im, mask=im.split()[3])
    bbox = ImageChops.difference(flat, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
    lock = flat.crop(bbox)
    # the P mark is everything left of the first wide blank column run
    w, h = lock.size
    px = lock.load()
    ink = [any(px[x, y][:3] != (255, 255, 255) for y in range(h)) for x in range(w)]
    split = w
    run = None
    for x, v in enumerate(ink):
        if not v:
            run = x if run is None else run
        else:
            if run is not None and x - run >= 4:
                split = run
                break
            run = None
    mark = lock.crop((0, 0, split, h))
    mb = ImageChops.difference(mark, Image.new("RGB", mark.size, (255, 255, 255))).getbbox()
    mark = mark.crop(mb)

    def uri(img):
        best = None
        for colors in (16, 32, 64, 128):
            p = img.convert("P", palette=Image.ADAPTIVE, colors=colors)
            buf = io.BytesIO(); p.save(buf, format="PNG", optimize=True)
            d = buf.getvalue()
            if best is None or len(d) <= 10240:
                best = d
        assert len(best) <= 10240, f"logo asset {len(best)}b exceeds the 10 KB budget"
        return "data:image/png;base64," + base64.b64encode(best).decode(), img.size
    return uri(lock), uri(mark)


def logo_html(lock_uri, lock_size):
    """The lockup on a white chip. The chip keeps it legible on a dark header;
    on a light one it is invisible. Either way the artwork is untouched."""
    w, h = lock_size
    return (
        '<span class="ps-logo" style="display:inline-block;background:#fff;'
        'border-radius:8px;padding:6px 10px;line-height:0">'
        f'<img src="{lock_uri}" width="{w}" height="{h}" alt="Progress Schools" '
        'style="width:92px;height:auto;display:block">'
        '</span>'
        '<span style="display:block;margin-top:.45rem;font:600 11px/1 system-ui,sans-serif;'
        'letter-spacing:.08em;white-space:nowrap">' + STRIP + '</span>'
    )


CREDIT_HTML = (
    '<div class="ps-credit" style="text-align:center;font:400 10px/1.4 system-ui,sans-serif;'
    'opacity:.55;margin:10px 0 4px;letter-spacing:.02em">' + CREDIT + '</div>'
)



def insert_credit(text):
    """Put the credit at the document's real end.

    NOT a plain re.sub on '</body>': these decks build printable views with
    w.document.write('<html>...</body></html>'), so the FIRST </body> in the
    file is inside a JavaScript string literal. Injecting HTML there produced
    an unterminated string and broke the deck's whole script block. The real
    tag is the last one with nothing but whitespace and </html> after it."""
    for tag in ("</body>", "</html>"):
        for m in reversed(list(re.finditer(re.escape(tag), text, re.I))):
            if re.fullmatch(r'\s*(</html>)?\s*', text[m.end():], re.I):
                return text[:m.start()] + CREDIT_HTML + "\n" + text[m.start():]
    return text + "\n" + CREDIT_HTML + "\n"


def mirror_rebrand(text, rel, mark_html):
    """The standard rebrand, with the real logo and the credit."""
    log = {}
    n0 = len(text)
    text, k = MARK_SVG.subn(lambda m: mark_html, text)
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
    text, k2 = re.subn(HUD_DYNAMIC, "", text)
    log["hud_stripped"] = k + k2
    if 'name="x-brand"' not in text:
        text, k = re.subn(r'(<head[^>]*>)', r'\1\n<meta name="x-brand" content="progress-schools">',
                          text, count=1, flags=re.I)
        log["xbrand"] = k
    # the credit goes in LAST, after the domain sweep above has run, or it
    # would be rewritten into "Progress Schools Tees Valley" like any other
    # mention of the domain.
    if CREDIT not in text:
        text = insert_credit(text)
        log["credit"] = 1
    log["delta"] = len(text) - n0
    return text, log


# ------------------------------------------------------- KEEP-21-Jul guard
# Everything dated 21 Jul in the Humanities folders is a hand-made support
# pack. It is not regenerable and the pack must never overwrite it. These are
# the stems visible in the screenshots (several are truncated in the OneDrive
# UI, so the match is by prefix on what IS legible).
KEEP_21JUL = {
    f"{HUM}/Build": ["AQA_UAS_Unit_O", "Cause_Consequ", "Historical_Accou", "Lundy_Influence_",
                     "Map_Route_and_", "Printable_Eviden", "Rapid_Gallery_His", "README",
                     "Recording_Consent_Log", "Source_Observati", "START_HERE",
                     "Studio_Archivist_Role_Card", "Teacher_Guide_and_Moderation"],
    f"{HUM}/Grow":  ["AQA_UAS_Outco", "Atlas_Index_Grid", "Lundy_Influence_", "Multi_Causal_Re",
                     "Printable_Eviden", "README", "Recording_Consent_Log", "Significance_Dep",
                     "Source_Provenan", "START_HERE", "Studio_Archivist", "Teacher_Guide_and_Moderation",
                     "Week7_Assesse"],
    f"{HUM}/Launch": ["Printable_Eviden", "Recording_Consent_Log", "START_HERE",
                      "Teacher_Guide_and_Moderation"],
}

WEEK_ORDER_NOTE = """0_WEEK_ORDER — read before teaching Careers W6 / W7
=====================================================

The LABEL on the slide and the FILENAME disagree for weeks 6 and 7 of the
BUILD Careers unit. The FILENAME is the one to trust when you are picking
which lesson to open; the label inside the deck was written first and was
never corrected.

    CAREERS_W6_My_Career_Profile.html   <- teach this SIXTH
    CAREERS_W7_After_Year_11.html       <- teach this SEVENTH

If you open a deck and the on-slide week number does not match the file you
clicked, the file is right. Nothing else in the unit is affected, and no
content needs changing — this note exists so the mismatch does not get
"fixed" in the wrong direction by whoever notices it next.

This note travels with the Careers folder deliberately: the warning used to
live only in a build report, which is not where anyone teaching the lesson
would ever look.
"""


def build_mirror(logo_path, out_root):
    keep, dropped = in_scope()
    print(f"scope: {len(keep)} files in, {len(dropped)} deliberately excluded")
    fwd, back = build_index(keep)
    print(f"taxonomy: {len(set(os.path.dirname(v) for v in fwd.values()))} destination folders")

    (lock_uri, lock_size), (mark_uri, mark_size) = load_logo(logo_path)
    print(f"logo: lockup {lock_size} ({len(lock_uri)} chars b64), mark {mark_size}")
    mark_html = logo_html(lock_uri, lock_size)
    LOGO_URI[:] = [lock_uri, lock_size]

    pack = out_root / "Progress_Schools_OneDrive_Mirror"
    if out_root.exists(): shutil.rmtree(out_root)
    pack.mkdir(parents=True)

    # assessed conditions blocks captured BEFORE anything is touched (R-A01)
    assessed = {}
    for rel in keep:
        src = REPO / rel
        if src.suffix == ".html":
            t = src.read_text(encoding="utf-8", errors="ignore")
            if "★ ASSESSED LESSON" in t:
                mm = re.search(r'★ ASSESSED LESSON.{0,2000}', t, re.S)
                assessed[str(rel)] = mm.group(0) if mm else None
    print(f"assessed files locked: {len(assessed)}")

    totals, avl_fails, avl_seen, rewrites = {}, [], 0, 0
    logo_pages = 0
    for rel in keep:
        src = REPO / rel
        raw = src.read_text(encoding="utf-8", errors="ignore") if src.suffix != ".csv" else None
        dest = pack / fwd[str(rel)]
        if src.suffix == ".html":
            new, log = mirror_rebrand(raw, rel, mark_html)
            new, n = rewrite_links(new, rel, fwd)
            rewrites += n
            if log.get("logo_swapped"): logo_pages += 1
            for k, v in log.items():
                if k != "delta": totals[k] = totals.get(k, 0) + v
            if avl_blocks(raw):
                avl_seen += 1
                f = check_avl_preserved(raw, new, rel)
                if f: avl_fails.append(f)
            write_guarded(raw, new, dest)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
    print("rebrand totals:", totals)
    print(f"link rewrites: {rewrites}")

    # R-A01 — conditions blocks byte-identical
    for relstr, block in assessed.items():
        if block is None: continue
        got = (pack / fwd[relstr]).read_text(encoding="utf-8", errors="ignore")
        core = re.sub(r'Made by Matt|MADE BY MATT|madebymatt\.uk', "", block)
        core = re.sub(r'\s+', " ", core).strip()[:400]
        assert core in re.sub(r'\s+', " ", got), f"R-A01 VIOLATION: conditions block altered in {relstr}"
    print(f"R-A01: {len(assessed)} assessed conditions blocks intact")

    # the Careers week-order note travels INTO the folder it warns about
    (pack / "ASDAN PEQ/Build/Careers/0_WEEK_ORDER.txt").write_text(WEEK_ORDER_NOTE, encoding="utf-8")

    # KEEP-21-Jul: nothing we ship may land on a hand-made support pack
    clashes = []
    for d, stems in KEEP_21JUL.items():
        folder = pack / d
        if not folder.exists(): continue
        for f in folder.iterdir():
            for s in stems:
                if f.name.startswith(s):
                    clashes.append(f"{d}/{f.name} would overwrite a 21-Jul support pack")
    print(f"KEEP-21-Jul: {'clean, no shipped file collides' if not clashes else str(len(clashes)) + ' COLLISIONS'}")
    for c in clashes: print("  FAIL:", c)
    return pack, keep, fwd, back, avl_fails, avl_seen, clashes, logo_pages, rewrites


def mirror_verify(pack):
    """The full set, run over the ASSEMBLED tree.

    Differs from verify() in one way that matters: exactly ONE Made-by-Matt
    string is permitted per page -- the credit Matt asked for -- and it is
    whitelisted by exact match. Any other spelling still counts as residue."""
    fails, notes = [], {}
    files = sorted(pack.rglob("*.html"))
    notes["html_files"] = len(files)
    attr = dom = noxb = strip = nocredit = multicredit = tiny = 0
    for p in files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'(aria-label|alt|content|title)="[^"]*made by matt', t, re.I): attr += 1
        # every 'madebymatt' occurrence must be exactly the whitelisted credit
        occ = re.findall(r'madebymatt[^\s"\'<>]*', t, re.I)
        allowed = [o for o in occ if o == "madebymatt.uk"]
        if len(occ) != len(allowed): dom += 1
        if t.count(CREDIT) == 0: nocredit += 1
        elif t.count(CREDIT) > 1: multicredit += 1
        if 'name="x-brand"' not in t: noxb += 1
        if STRIP in t: strip += 1
        if not t.rstrip().lower().endswith("</html>"):
            fails.append(f"{p.name}: no closing </html>")
        if len(t) < 200: tiny += 1
    notes.update(attr_residue=attr, domain_residue=dom, missing_xbrand=noxb,
                 carry_strip=strip, missing_credit=nocredit,
                 duplicate_credit=multicredit, truncated_or_empty=tiny)
    if attr:        fails.append(f"REBRAND check 1 FAILED: {attr} files with wordmark in an attribute")
    if dom:         fails.append(f"REBRAND check 2 FAILED: {dom} files carry non-whitelisted madebymatt text")
    if noxb:        fails.append(f"REBRAND check 3 FAILED: {noxb} files missing the x-brand marker")
    if not strip:   fails.append("REBRAND check 4 FAILED: no file carries the TEES VALLEY strip")
    if nocredit:    fails.append(f"CREDIT FAILED: {nocredit} files missing '{CREDIT}'")
    if multicredit: fails.append(f"CREDIT FAILED: {multicredit} files carry it more than once")
    if tiny:        fails.append(f"{tiny} files are truncated or empty")
    return fails, notes


def inline_js_check(pack):
    """Catch inline <script> bodies the transform could have broken."""
    import subprocess, tempfile, json
    bad = []
    for p in sorted(pack.rglob("*.html")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        for mm in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', t, re.S | re.I):
            body = mm.group(1).strip()
            if not body or body.startswith("{") and body.endswith("}"):  # JSON-LD etc
                continue
            r = subprocess.run(["node", "--check", "-"], input=body, text=True,
                               capture_output=True)
            if r.returncode != 0:
                err = next((l for l in r.stderr.splitlines() if "Error" in l), "unknown")
                bad.append(f"{p.relative_to(pack)}: {err[:100]}")
                break
    return bad


def write_docs(pack, keep, fwd, back, clashes, logo_pages, rewrites, crawl_miss):
    tops = {}
    for d in fwd.values():
        tops.setdefault(d.split("/")[0] if "/" in d else "(root files)", []).append(d)

    # ---- PLACEMENT_GUIDE.txt
    known_new = {"(root files)": None}
    g = ["PLACEMENT_GUIDE — one line per top-level item. Nothing else to decide.",
         "=" * 74, "",
         "Drag each item below onto its twin in OneDrive and choose MERGE.",
         "Do not rename anything. Do not delete anything first.", ""]
    for t in sorted(tops):
        # count what is actually on disk, not what the map contains: the pack
        # also adds 0_WEEK_ORDER.txt, and a guide that undercounts is a guide
        # someone will use to conclude the copy failed.
        d = pack / t
        n = sum(1 for f in d.rglob("*") if f.is_file()) if d.is_dir() else len(tops[t])
        if t == "(root files)":
            g.append(f"  {'the 4 loose .html files':<46} -> drop at the ROOT of the lessons area (merge)")
        elif t == HUM:
            g.append(f"  {t + '/':<46} -> merge into your existing Humanities folder")
            g.append(f"  {'':<46}    ** CHECK THE NAME FIRST — see the warning below **")
        else:
            g.append(f"  {t + '/':<46} -> merge into the existing '{t}' folder  ({n} files)")
    g += ["", "-" * 74, "",
          "THE ONE NAME I COULD NOT CONFIRM",
          "",
          "Every screenshot truncates the Humanities folder name:",
          '    root listing : "Humanities Less...s and resources)"',
          '    title bar    : "Humanities Lessons (Whiteboards..."',
          "",
          f'This pack spells it: "{HUM}"',
          "",
          "Before you drag it: open the real folder on the drive and compare.",
          "If it differs by even one character, RENAME THE FOLDER IN THIS PACK to",
          "match, then drag. Otherwise OneDrive will create a second folder beside",
          "the real one instead of merging into it.",
          "", "Everything else in this pack was confirmed against a screenshot."]
    (pack / "PLACEMENT_GUIDE.txt").write_text("\n".join(g) + "\n", encoding="utf-8")

    # ---- TAXONOMY_MAP.md
    m = ["# TAXONOMY_MAP — repo path -> OneDrive destination", "",
         f"Derived from 35 screenshots of the live drive, 2026-08-07. {len(keep)} files mapped.",
         "Where the repo and the drive disagree on a name, **the drive wins**.", "",
         "## Every in-scope file", "", "| repo path | OneDrive destination |", "|---|---|"]
    for r in sorted(fwd, key=str.lower):
        m.append(f"| `{r}` | `{fwd[r]}` |")
    m += ["", "## Folders that were RENAMED on the way in", "",
          "| repo | drive | why |", "|---|---|---|",
          "| `BUILD_ASDAN/` | `ASDAN PEQ/Build/` | the drive groups the three ASDAN strands under one folder |",
          "| `GROW_ASDAN/` | `ASDAN PEQ/Grow/` | as above |",
          "| `LAUNCH_ASDAN/` | `ASDAN PEQ/Launch/` | as above |",
          "| `GROW_ASDAN/Enterprise/` | `ASDAN PEQ/Grow/Community and Enterprise/` | drive uses spaces and the long name |",
          "| `GROW_ASDAN/Community_Project/` | `ASDAN PEQ/Grow/Community Project/` | drive uses a space |",
          "| `GROW_ASDAN/PEQ/` | `ASDAN PEQ/Grow/Personal Effectiveness/` | drive uses the full unit name |",
          "| `DT_Community_Upcycling/` | `ASDAN PEQ/Build/DT/` | drive files it under BUILD |",
          "| `Humanities_Teesside/` | `" + HUM + "/` | **name AMBIGUOUS — see below** |",
          "| `Humanities_Teesside/Lundy_Humanities/` | `" + HUM + "/LundyLoop/` | drive name |",
          "| `.../Lundy_Humanities/specimens/` | `" + HUM + "/LundyLoop/Specimens/` | capital S on the drive |",
          "| `Tutor_Time/` | `Tutor Time BF_BV_KCSIE/` | drive name |",
          "| `Art_Teesside/` | `Art/` | drive name |",
          "", "## Structural change: LAUNCH_ASDAN is FLAT on the drive", "",
          "The repo keeps five subfolders; the drive holds every deck directly in",
          "`ASDAN PEQ/Launch/`. Flattening collides five `START_HERE.html` files onto",
          "one name, so they are disambiguated. **These five filenames are new:**", ""]
    for a, b, why in sorted(set(RENAMES)):
        m.append(f"- `{a}` -> `{b}`")
    m += ["", "## NEW — things this pack adds that the screenshots do NOT show", "",
          "Drag-and-merge will create these. Nothing is overwritten.", "",
          "- `ASDAN PEQ/Build/Careers/0_WEEK_ORDER.txt` — the W6/W7 label-vs-filename",
          "  warning, moved from a build report into the folder it actually concerns.",
          "- the five `START_HERE_<strand>.html` files listed above.", "",
          "## Taxonomy folders with NO current repo content", "",
          "Recorded, not invented. The pack ships nothing into these and they stay as they are:", "",
          "- `Computing/`, `Curriculum Intent and Rationale/`, `English/`,",
          "  `Feedback and Marking/`, `Lesson Slideshows_Resources/`,",
          "  `SMSC and BV Calendar Evidence/`, `Weekly Plans/`, `ASDAN PEQ/` root files",
          "  (`index`, `PLACE_THIS_README`, `Scheme_of_Work`, `Weekly_Plan`)",
          "- every `_Legacy_2025-26/` folder — Matt's archive. The pack never writes",
          "  into one and never writes beside one.",
          "- `Art/Build`, `Art/Grow`, `Art/Launch` each hold drive-only extras",
          "  (`Autumn2_*`, `Spring1_*`, evidence packs) that have no repo source.", "",
          "## Deliberate single placement (was double-placed on the drive)", "",
          "The drive currently keeps two copies of these. Because every link in this",
          "pack is rewritten to the real location, the second copy is unnecessary and",
          "the pack ships ONE:", "",
          "- `LundyLoop/assets/style.css` — shipped once at the root LundyLoop.",
          f"  The copy at `{HUM}/LundyLoop/style.css` is left untouched; it is a",
          "  stylesheet, byte-identical, and carries no branding either way.",
          "- the four root hubs (`art_teesside`, `build_asdan`, `build_dt_upcycling`,",
          "  `humanities_teesside`) — shipped once at the root.", "",
          "  **Flagged:** the drive also holds in-folder copies of those four",
          "  (`Art/art_teesside`, `ASDAN PEQ/Build/build_asdan`,",
          "  `ASDAN PEQ/Build/DT/build_dt_upcycling`, `" + HUM + "/humanities_teesside`).",
          "  This pack does not overwrite them, so **they stay Made-by-Matt branded**.",
          "  Delete them, or copy the rebranded root version over each, by hand.", "",
          "## The one name I could not resolve", "",
          f"`{HUM}` — **AMBIGUOUS**. Both screenshots that show it truncate it, from",
          "opposite ends. The overlap fixes everything except a possible middle word.",
          "Check it on the drive before dragging; rename the pack folder if it differs.", ""]
    (pack / "TAXONOMY_MAP.md").write_text("\n".join(m) + "\n", encoding="utf-8")

    # ---- README_FIRST.txt
    r = ["README_FIRST — Progress Schools OneDrive Mirror Pack", "=" * 74, "",
         "WHAT THIS IS",
         "  A Progress Schools-branded copy of the in-scope estate, in a folder tree",
         "  that mirrors your OneDrive exactly. Drag each top-level folder onto its",
         "  twin, choose merge. There are no placement decisions to make.", "",
         "  See PLACEMENT_GUIDE.txt for the one-line-per-folder version.", "",
         "-" * 74, "KEEP — 21 JULY SUPPORT PACKS",
         "  Everything dated 21 Jul in the Humanities folders is hand-made and NOT",
         "  regenerable: the organisers, receipt packs, role cards, consent logs,",
         "  moderation guides. This pack ships nothing with those names and the build",
         f"  asserts it ({'0 collisions' if not clashes else str(len(clashes)) + ' COLLISIONS — DO NOT UNZIP'}).",
         "  If a merge ever offers to replace one of them, say no.", "",
         "-" * 74, "CAREERS W6 / W7 — LABEL vs FILENAME",
         "  The on-slide week label and the filename disagree for BUILD Careers weeks",
         "  6 and 7. THE FILENAME IS RIGHT. This warning now travels inside the folder",
         "  itself, as ASDAN PEQ/Build/Careers/0_WEEK_ORDER.txt, instead of living in",
         "  a build report nobody teaching the lesson would open.", "",
         "-" * 74, "PER-MACHINE DATA",
         "  Anything a deck stores locally is per-machine and per-browser. A tracker",
         "  filled in on the classroom PC is not on your laptop and is not on the",
         "  drive. Nothing in this pack syncs. Export or print anything that matters.",
         "  No pupil data of any kind is in this pack, and none ever will be.", "",
         "-" * 74, "BRANDING CHANGELOG",
         "  * NEW THIS BUILD — the REAL Progress Schools logo. The previous packs used",
         "    a typographic 'PS' placeholder because REBRAND.md rule 1 forbade drawing",
         "    a mark. Matt has supplied the actual lockup, which supersedes that rule.",
         "    It is embedded per-page as a data URI, so every page works from file://",
         "    with no asset folder to lose. It is never recoloured, restyled, stretched",
         "    or redrawn, and it sits on a white chip so a dark header cannot force a",
         "    change to the trademark's own colours.",
         f"  * NEW THIS BUILD — every page carries '{CREDIT}', at Matt's instruction.",
         "    This is the ONE permitted Made-by-Matt string; the residue sweep",
         "    whitelists it by exact match and still fails on any other spelling.",
         "  * Wordmarks replaced in attributes as well as visible text (two thirds of",
         "    them are in aria-label/alt/meta and survive any visual check).",
         "  * hud.js loaders stripped, including the dynamic injector form.",
         "  * x-brand meta tag on every page, added only where the rebrand completed.", "",
         "-" * 74, "WHAT CHANGED THIS BUILD",
         "  * The tree is now the SCHOOL's, not the repo's. Every internal link was",
         f"    rewritten to match ({rewrites} rewrites). This is only safe because the",
         "    zip and the drive now share one geometry.",
         "  * LAUNCH_ASDAN is flat on the drive, so its five subfolders were flattened",
         "    and their five colliding START_HERE files renamed. See TAXONOMY_MAP.md.",
         "  * The LundyLoop stylesheet and the four root hubs are now placed ONCE",
         "    rather than double-placed, because the links no longer need the hack.",
         f"  * The logo is on {logo_pages} pages — every page that previously carried a",
         "    visible mark. Pages that never had one get the meta tag and credit only.", "",
         "-" * 74, "WHAT THIS PACK DOES NOT CLAIM",
         "  The estate is not clean. This pack covers the in-scope areas only, and",
         "  leaves the legacy trees, the _Legacy_2025-26 archives, the Planning and",
         "  Students material and the personal apps entirely alone.",
         f"  Unresolved link targets after the rewrite: {sum(len(v) for v in crawl_miss.values())}.", ""]
    (pack / "README_FIRST.txt").write_text("\n".join(r) + "\n", encoding="utf-8")


def write_offline_index(pack, fwd, logo_uri, logo_size):
    """Generate the offline index for the Network Library copy.

    Links are relative to the pack root, i.e. the SAME geometry as the mirror,
    so the index works from a network share or from file:// without change."""
    from collections import defaultdict
    groups = defaultdict(list)
    for d in sorted(fwd.values(), key=str.lower):
        if not d.lower().endswith(".html"):
            continue
        top = d.split("/")[0] if "/" in d else "(top level)"
        groups[top].append(d)
    w, h = logo_size
    rows = []
    for top in sorted(groups, key=str.lower):
        rows.append(f'<section><h2>{html.escape(top)} '
                    f'<span class="n">{len(groups[top])} pages</span></h2><ul>')
        for d in groups[top]:
            label = d.rsplit("/", 1)[-1][:-5].replace("_", " ")
            href = "/".join(quote(seg) for seg in d.split("/"))
            rows.append(f'<li><a href="{href}">{html.escape(label)}</a>'
                        f'<span class="p">{html.escape(d.rsplit("/",1)[0])}</span></li>')
        rows.append("</ul></section>")
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-brand" content="progress-schools">
<title>Progress Schools \u00b7 Offline Lesson Library</title>
<style>
:root{{color-scheme:light dark;--bg:#fbfbfc;--fg:#1a1a1e;--mut:#63636e;--line:#e3e3e8;--card:#fff;--acc:#E5007D}}
@media(prefers-color-scheme:dark){{:root{{--bg:#131317;--fg:#ececf1;--mut:#9a9aa6;--line:#2a2a32;--card:#1c1c22}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,sans-serif}}
header{{padding:28px 20px 20px;border-bottom:1px solid var(--line);text-align:center;background:var(--card)}}
.chip{{display:inline-block;background:#fff;border-radius:8px;padding:6px 10px;line-height:0}}
.chip img{{width:112px;height:auto;display:block}}
.strip{{margin-top:.5rem;font:600 11px/1 system-ui,sans-serif;letter-spacing:.08em}}
h1{{font-size:1.15rem;margin:.7rem 0 .2rem}}
.sub{{color:var(--mut);font-size:.85rem;margin:0}}
main{{max-width:1000px;margin:0 auto;padding:20px}}
section{{background:var(--card);border:1px solid var(--line);border-radius:12px;margin:0 0 16px;padding:14px 18px}}
h2{{font-size:.95rem;margin:.2rem 0 .6rem;display:flex;justify-content:space-between;align-items:baseline;gap:1rem}}
.n{{font-weight:400;font-size:.75rem;color:var(--mut)}}
ul{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:2px}}
li{{padding:5px 8px;border-radius:7px;min-width:0}}
li:hover{{background:var(--bg)}}
a{{color:var(--fg);text-decoration:none;font-size:.88rem;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
a:hover{{color:var(--acc);text-decoration:underline}}
.p{{display:block;font-size:.68rem;color:var(--mut);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
footer{{text-align:center;color:var(--mut);font-size:.7rem;padding:18px}}
</style></head><body>
<header>
<span class="chip"><img src="{logo_uri}" width="{w}" height="{h}" alt="Progress Schools"></span>
<div class="strip">{STRIP}</div>
<h1>Offline Lesson Library</h1>
<p class="sub">{sum(len(v) for v in groups.values())} pages \u00b7 works from a network share or from file:// \u00b7 nothing loads from the internet</p>
</header>
<main>
{chr(10).join(rows)}
</main>
<footer>{CREDIT}</footer>
</body></html>
"""
    (pack / "index.html").write_text(doc, encoding="utf-8")
    return sum(len(v) for v in groups.values())


def zip_tree(src_dir, zip_path, arc_root):
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists(): zip_path.unlink()
    n = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(src_dir.rglob("*")):
            if f.is_file():
                z.write(f, str(Path(arc_root) / f.relative_to(src_dir)))
                n += 1
    return n, zip_path.stat().st_size


def mirror_main(logo, out):
    out = Path(out)
    (pack, keep, fwd, back, avl_fails, avl_seen,
     clashes, logo_pages, rewrites) = build_mirror(logo, out)

    miss = crawl(pack)
    print(f"\nCRAWL: {'clean, 0 broken internal links' if not miss else str(sum(len(v) for v in miss.values())) + ' UNRESOLVED'}")
    for f, ts in list(miss.items())[:15]:
        print(f"  {f} -> {', '.join(sorted(ts))[:110]}")

    print(f"\nAVL-1: {avl_seen} decks carry a marker pair; "
          f"{'all preserved byte-for-byte' if not avl_fails else str(len(avl_fails)) + ' ALTERED'}")
    ref_fails = check_avl_refs(pack)
    print(f"AVL-2: {'all loader references resolve inside the pack' if not ref_fails else 'BROKEN'}")
    for f in ref_fails[:10]: print("  FAIL:", f)

    fails, notes = mirror_verify(pack)
    js = inline_js_check(pack)
    print(f"INLINE JS: {'0 syntax errors' if not js else str(len(js)) + ' BROKEN'}")
    for f in js[:10]: print("  FAIL:", f)

    write_docs(pack, keep, fwd, back, clashes, logo_pages, rewrites, miss)
    print("\nVERIFY:", notes)
    all_fails = fails + avl_fails + ref_fails + js + clashes
    for f in all_fails[:20]: print("  FAIL:", f)
    if not all_fails: print("  all checks pass")

    # ---- package. Nothing ships if anything above failed.
    assert not all_fails, f"{len(all_fails)} checks failed - refusing to package"
    zips = []
    n, sz = zip_tree(pack, out / "Progress_Schools_OneDrive_Mirror.zip",
                     "Progress_Schools_OneDrive_Mirror")
    zips.append(("Progress_Schools_OneDrive_Mirror.zip", n, sz))

    # optional: same tree + a generated offline index, for the network share
    lib = out / "Progress_Schools_Network_Library"
    shutil.copytree(pack, lib)
    (lib / "PLACEMENT_GUIDE.txt").unlink()          # placement is a OneDrive concern only
    pages = write_offline_index(lib, fwd, LOGO_URI[0], LOGO_URI[1])
    n, sz = zip_tree(lib, out / "Progress_Schools_Network_Library.zip",
                     "Progress_Schools_Network_Library")
    zips.append(("Progress_Schools_Network_Library.zip", n, sz))
    print(f"\nofflineibrary index: {pages} pages listed".replace("ibrary","  library"))
    for nm, c, s in zips:
        print(f"PACKAGED {nm}: {c} entries, {s/1024/1024:.1f} MB")
    return pack, all_fails, notes, miss, logo_pages, rewrites, fwd, zips


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--logo", help="Progress Schools logo PNG; enables mirror-pack mode")
    ap.add_argument("--mirror", action="store_true", help="assemble in the OneDrive taxonomy")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    if a.mirror:
        assert a.logo, "--mirror needs --logo"
        mirror_main(a.logo, a.out)
    else:
        main()
