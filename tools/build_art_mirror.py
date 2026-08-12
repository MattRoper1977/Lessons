#!/usr/bin/env python3
"""Progress Schools ART OneDrive mirror pack.

One zip whose single top-level folder is `Art/`, mirroring the Art folder of
Matt's OneDrive so it can be dragged onto the drive's `Art` and merged.

This does NOT reimplement the rebrand. It imports the proven primitives from
tools/build_staff_pack.py (the PACK-4 mirror builder) and supplies three things
that are specific to an Art-only pack:

  1. scope     -- the Art suite only, current lessons only
  2. geometry  -- repo paths -> `Art/...` drive paths
  3. gates     -- Art-specific cardinality and the x-brand string this pack wants

Everything that has already been proven -- the logo loader and its SHA gate, the
last-</body> credit insertion, the guarded write, the link rewriter, the crawl --
is reused rather than retyped.

Usage:
    python3 tools/build_art_mirror.py --logo PATH --repo PATH --out DIR

The logo binary never enters git. It is passed in and hash-checked.
"""
import os, sys, re, html, json, shutil, zipfile, subprocess
from pathlib import Path
from collections import defaultdict
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_staff_pack as bsp

# The x-brand marker this pack is specified to carry. The full-drive builder
# writes content="progress-schools"; the Art mirror is asked for the long form,
# so the marker is normalised after the shared rebrand runs.
X_BRAND = "Progress Schools Tees Valley — internal copy"
X_BRAND_META = f'<meta name="x-brand" content="{X_BRAND}">'

# ---------------------------------------------------------------- scope
# Derived from the repo, cross-checked against the drive screenshots. Every
# entry is resolved to a REAL repo filename -- no truncated screenshot name is
# ever written to disk as-is.

ART_TEESSIDE_SUBS = ("Build", "Grow", "Launch")

# Art_Teesside/ root pages that belong at the drive's Art/ root.
ART_ROOT_PAGES = [
    "Arts_Partnership_Log.html",
    "House_Standard_and_Safety.html",
    "Spring2_Printable_Weekly_Evidence_Pack.html",
    "Spring2_Scheme_of_Work.html",
    "Summer1_Printable_Weekly_Evidence_Pack.html",
    "Summer1_Scheme_of_Work.html",
    "Summer2_Printable_Weekly_Evidence_Pack.html",
    "Summer2_Scheme_of_Work.html",
]

# The visual-learning runtime. These are ASSETS, not pages: the 31 lesson decks
# load all three. Shipping the decks without them is the dead-loader failure.
VISUAL_LEARNING = [
    "art-visual-learning.css",
    "art-visual-learning.js",
    "art-visual-payloads.js",
]
# README.md sits beside them in the repo and is NOT on the drive (the drive's
# visual-learning folder holds exactly three files). Documentation, not runtime.
VISUAL_LEARNING_EXCLUDED = ["README.md"]

# Pages that live outside Art_Teesside/ but land inside Art/ on the drive.
LAUNCH_EXTRAS = [
    "Launch/Art_L1_Colours_Lines_Like_Me_v5.html",
    "Launch/Art_L2_My_Identity_Picture_v5.html",
    "Launch/index.html",
]
ART_HUB = "art_teesside.html"          # repo root -> Art/art_teesside.html

# The superseded legacy lessons. They are interleaved with the current suite on
# the drive and must NOT ship; the placement guide names each one so Matt can
# clear them by hand after the merge.
LEGACY_STRAYS = {
    "Art/Grow": [
        "GROW_ART_W1_Art_Battle_Tasters.html",
        "GROW_ART_W2_Level_Up_Portrait.html",
        "GROW_ART_W3_Plan_The_Portrait.html",
        "GROW_ART_W4_Create_The_Piece.html",
        "GROW_ART_W5_Review_And_Improve.html",
        "GROW_ART_W6_Artist_Research.html",
        "GROW_ART_W7_Share_The_Portfolio.html",
        "GROW_ART_W8_Festival_Sounds.html",
    ],
    "Art/Launch": [
        "LAUNCH_ART_W1_Gallery_Detectives.html",
        "LAUNCH_ART_W2_Symbolism_Self_Portrait.html",
        "LAUNCH_ART_W3_Practitioner_Research.html",
        "LAUNCH_ART_W4_Refine_With_Feedback.html",
        "LAUNCH_ART_W5_Plan_The_Experience.html",
        "LAUNCH_ART_W6_Experience_The_Event.html",
        "LAUNCH_ART_W7_Begin_The_Review.html",
        "LAUNCH_ART_W8_Complete_The_Review.html",
    ],
    # In the repo at Build/Slideshows/ but NOT visible in the drive's Build
    # listing. Named anyway so the guide is complete if a copy does exist.
    "Art/Build (repo-only, not seen on the drive)": [
        "BUILD_ART_W1_Technique_Tasters.html",
        "BUILD_ART_W2_Level_It_Up.html",
        "BUILD_ART_W3_Plan_This_Is_Me.html",
        "BUILD_ART_W4_Make_It.html",
        "BUILD_ART_W5_Star_And_A_Step.html",
        "BUILD_ART_W6_Meet_An_Artist.html",
        "BUILD_ART_W7_Show_And_Tell.html",
        "BUILD_ART_W8_Festival_Sounds.html",
    ],
}

# What the drive screenshots show, per folder, as RESOLVED repo filenames.
# The build asserts the assembled tree equals this set. A repo file that matches
# no screenshot entry -- or a screenshot entry with no repo file -- is reported
# as UNMAPPED rather than silently dropped.
SCREENSHOT_EXPECT = {
    "Art": [
        "art_teesside.html", "Arts_Partnership_Log.html", "House_Standard_and_Safety.html",
        "index.html",
        "Spring2_Printable_Weekly_Evidence_Pack.html", "Spring2_Scheme_of_Work.html",
        "Summer1_Printable_Weekly_Evidence_Pack.html", "Summer1_Scheme_of_Work.html",
        "Summer2_Printable_Weekly_Evidence_Pack.html", "Summer2_Scheme_of_Work.html",
    ],
    "Art/Build": [
        "Autumn2_Printable_Weekly_Evidence_Pack.html", "Autumn2_Scheme_of_Work.html",
        "Autumn2_Studio_Session_Run_Sheets.html",
        "BUILD_ART_A2_W1_Surface_Hunt.html", "BUILD_ART_A2_W2_Arts_Inspiration.html",
        "BUILD_ART_A2_W3_Stencil_Lab.html", "BUILD_ART_A2_W4_Audience_Week.html",
        "BUILD_ART_A2_W5_Layer_and_Combine.html", "BUILD_ART_A2_W6_Resolve_and_Edition.html",
        "BUILD_ART_A2_W7_Bank_It_and_Plan_the_Teach.html",
        "BUILD_ART_W1_The_Local_Canvas.html",
        "BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html",
        "BUILD_ART_W3_Industrial_Surface_Skills_Lab.html",
        "BUILD_ART_W4_Build_the_Brief.html", "BUILD_ART_W5_Critique_Test_and_Redirect.html",
        "BUILD_ART_W6_Resolve_the_Artwork.html", "BUILD_ART_W7_Curate_the_Showcase.html",
        "BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html",
        "Printable_BUILD_Weekly_Evidence_Pack.html", "Scheme_of_Work.html",
        "Spring1_Printable_Weekly_Evidence_Pack.html", "Spring1_Scheme_of_Work.html",
        "START_HERE.html",
    ],
    "Art/Grow": [
        "GROW_ART_W1_The_Local_Canvas.html",
        "GROW_ART_W2_Studio_Skills_and_Safe_Practice.html",
        "GROW_ART_W3_Independent_Studio_Challenge.html",
        "GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html",
        "GROW_ART_W5_Practitioner_Career_and_Inspiration.html",
        "GROW_ART_W6_Plan_and_Rehearse_the_Skill_Share.html",
        "GROW_ART_W7_Deliver_the_Skill_Share_and_Curate.html",
        "GROW_ART_W8_Reflect_Audit_and_Close_the_Loop.html",
        "Printable_GROW_Evidence_Lundy_and_LAUNCH_Pack.html",
        "Scheme_of_Work.html", "START_HERE.html",
    ],
    "Art/Launch": [
        "Art_L1_Colours_Lines_Like_Me_v5.html", "Art_L2_My_Identity_Picture_v5.html",
        "index.html",
        "LAUNCH_ART_W1_Frame_the_Local_Challenge.html",
        "LAUNCH_ART_W2_Practice_Careers_and_Pathways.html",
        "LAUNCH_ART_W3_Implement_and_Critically_Develop.html",
        "LAUNCH_ART_W4_Arts_Experience_Attend_Analyse_and_Share.html",
        "LAUNCH_ART_W5_Design_the_Leadership_Project.html",
        "LAUNCH_ART_W6_Pilot_Lead_and_Adapt.html",
        "LAUNCH_ART_W7_Deliver_and_Curate_the_Arts_Project.html",
        "LAUNCH_ART_W8_Review_Influence_and_Portfolio_Audit.html",
        "Printable_LAUNCH_Evidence_and_Lundy_Pack.html",
        "Scheme_of_Work.html", "START_HERE.html",
    ],
    "Art/visual-learning": list(VISUAL_LEARNING),
}
# Art/index.html has no repo source: it is the pack's generated front door.
GENERATED = {"Art/index.html"}


def art_scope(repo: Path):
    """Return [(repo_rel, dest_rel)], mechanically, plus what was excluded."""
    pairs, dropped = [], []
    at = repo / "Art_Teesside"

    for sub in ART_TEESSIDE_SUBS:
        for p in sorted((at / sub).glob("*.html")):
            pairs.append((f"Art_Teesside/{sub}/{p.name}", f"Art/{sub}/{p.name}"))

    for name in ART_ROOT_PAGES:
        assert (at / name).exists(), f"missing Art_Teesside/{name}"
        pairs.append((f"Art_Teesside/{name}", f"Art/{name}"))

    for name in VISUAL_LEARNING:
        p = at / "visual-learning" / name
        assert p.exists(), f"missing visual-learning/{name}"
        pairs.append((f"Art_Teesside/visual-learning/{name}",
                      f"Art/visual-learning/{name}"))
    for name in VISUAL_LEARNING_EXCLUDED:
        dropped.append((f"Art_Teesside/visual-learning/{name}",
                        "documentation, not runtime; not present on the drive"))

    for rel in LAUNCH_EXTRAS:
        assert (repo / rel).exists(), f"missing {rel}"
        pairs.append((rel, "Art/Launch/" + Path(rel).name))

    assert (repo / ART_HUB).exists(), f"missing {ART_HUB}"
    pairs.append((ART_HUB, f"Art/{ART_HUB}"))

    # everything in the Art estate that is deliberately NOT shipped
    for p in sorted(at.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(repo))
        if rel in {r for r, _ in pairs}:
            continue
        if rel.startswith("Art_Teesside/visual-learning/"):
            continue                       # already recorded above
        why = ("build/QA tooling, not a lesson" if "/tools/" in rel
               else "working note, not a lesson page")
        dropped.append((rel, why))
    for folder, names in LEGACY_STRAYS.items():
        for n in names:
            dropped.append((f"(legacy) {folder}/{n}", "superseded 2025-26 lesson"))

    # destination collision guard
    seen = {}
    for r, d in pairs:
        if d in seen:
            raise AssertionError(f"DESTINATION COLLISION: {seen[d]} and {r} both -> {d}")
        seen[d] = r
    return pairs, dropped


# ---------------------------------------------------------------- rebrand
# The Made-by-Matt monogram favicon. It is a base64 SVG data URI, so it carries
# no text and the residue sweep -- which reads text -- cannot see it. Three pages
# under Launch/ ship it, which would have put Matt's personal mark in the browser
# tab of a Progress Schools pack. Matched on the decoded path data, not on the
# base64 string, so a re-encoding of the same artwork still matches.
MONOGRAM_PATH = "M26 76 L26 30 L50 55 L74 30 L74 76"
SVG_DATA_URI = re.compile(r'data:image/svg\+xml;base64,([A-Za-z0-9+/=]+)')


def swap_monogram_favicon(text, mark_uri):
    """Replace the Made-by-Matt monogram favicon with the Progress Schools mark.

    The mark is the P from the supplied lockup, embedded as-is -- not recoloured,
    not redrawn. Returns (text, n_replaced)."""
    import base64 as _b64
    n = [0]

    def one(m):
        try:
            svg = _b64.b64decode(m.group(1)).decode("utf-8", "ignore")
        except Exception:
            return m.group(0)
        if MONOGRAM_PATH not in svg:
            return m.group(0)
        n[0] += 1
        return mark_uri

    return SVG_DATA_URI.sub(one, text), n[0]


# The shared rebrand rewrites Matt's contact address to a Progress Schools
# referral. Two things then need correcting for an Art pack:
#   * the referral names the science lead -- wrong subject for this pack;
#   * it is left inside href="mailto:...", so the anchor is a dead link to an
#     address that is not an address.
# There is no Progress Schools mailbox to substitute, so the anchor is unwrapped
# to plain text rather than pointed at an invented one.
DEAD_MAILTO = re.compile(r'<a\s+href="mailto:([^"@]*)"([^>]*)>(.*?)</a>', re.S | re.I)


def fix_contact(text):
    text, k1 = re.subn(r'your Progress Schools science lead',
                       "your Progress Schools Art lead", text)
    text, k2 = DEAD_MAILTO.subn(lambda m: f'<span{m.group(2)}>{m.group(3)}</span>', text)
    return text, k1, k2


def art_rebrand(text, rel, mark_html, mark_uri):
    """The shared mirror rebrand, then this pack's corrections."""
    new, log = bsp.mirror_rebrand(text, rel, mark_html)
    # normalise whatever x-brand marker ended up in the file to the long form
    new, n = re.subn(r'<meta\s+name="x-brand"\s+content="[^"]*"\s*/?>',
                     X_BRAND_META, new, flags=re.I)
    if not n:
        new, n = re.subn(r'(<head[^>]*>)', r'\1\n' + X_BRAND_META, new,
                         count=1, flags=re.I)
    log["xbrand"] = 1 if n else 0
    new, k = swap_monogram_favicon(new, mark_uri)
    log["favicon_swapped"] = k
    new, k1, k2 = fix_contact(new)
    log["contact_subject"] = k1
    log["dead_mailto_unwrapped"] = k2
    return new, log


# ---------------------------------------------------------------- front door
def write_art_index(pack: Path, logo_uri, logo_size):
    """Generate Art/index.html -- the pack's front door at the Art/ root.

    No repo file maps to it (the drive shows one; the repo's root index.html is
    the whole-estate hub and is out of scope for an Art-only pack), so it is
    authored here and its links are written for depth Art/."""
    art = pack / "Art"
    groups = defaultdict(list)
    for p in sorted(art.rglob("*.html"), key=lambda x: str(x).lower()):
        d = str(p.relative_to(art))
        if d == "index.html":
            continue
        groups["Art/" + d.split("/")[0] if "/" in d else "Art (top level)"].append(d)
    w, h = logo_size
    rows = []
    for top in sorted(groups, key=str.lower):
        rows.append(f'<section><h2>{html.escape(top)}'
                    f'<span class="n">{len(groups[top])} pages</span></h2><ul>')
        for d in groups[top]:
            label = d.rsplit("/", 1)[-1][:-5].replace("_", " ")
            href = "/".join(quote(s) for s in d.split("/"))
            rows.append(f'<li><a href="{href}">{html.escape(label)}</a></li>')
        rows.append("</ul></section>")
    doc = f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{X_BRAND_META}
<title>Progress Schools · Art · Teesside Studio Suite</title>
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
footer{{text-align:center;color:var(--mut);font-size:.7rem;padding:18px}}
</style></head><body>
<header>
<span class="chip"><img src="{logo_uri}" width="{w}" height="{h}" alt="Progress Schools"></span>
<div class="strip">{bsp.STRIP}</div>
<h1>Art — Teesside Studio Suite</h1>
<p class="sub">{sum(len(v) for v in groups.values())} pages · BUILD Explore · GROW Bronze · LAUNCH Silver · nothing loads from the internet</p>
</header>
<main>
{chr(10).join(rows)}
</main>
<footer>{bsp.CREDIT}</footer>
</body></html>
"""
    (art / "index.html").write_text(doc, encoding="utf-8")
    return sum(len(v) for v in groups.values())


# ---------------------------------------------------------------- guide
def write_placement_guide(pack: Path, counts, total, external_deps):
    L = []
    add = L.append
    add("=" * 74)
    add("PROGRESS SCHOOLS · ART — ONEDRIVE MIRROR PACK")
    add("=" * 74)
    add("")
    add("WHAT THIS IS")
    add("")
    add("  One folder, `Art`, shaped exactly like the `Art` folder already on your")
    add("  OneDrive. Every page is rebranded to Progress Schools. Nothing loads from")
    add("  the internet.")
    add("")
    add("HOW TO PLACE IT")
    add("")
    add("  1. Unzip. You get a single folder called  Art")
    add("  2. Drag that `Art` folder onto your OneDrive, on top of the existing `Art`.")
    add("  3. Windows will ask what to do with the folder — choose MERGE")
    add("     (\"Merge the folders\"), and then REPLACE the files when prompted.")
    add("  4. Nothing outside `Art` is touched.")
    add("")
    add("  The zip mirrors the drive's shape, so every link between two pages in this")
    add("  pack still resolves after the merge.")
    add("")
    add("WHAT IS IN IT")
    add("")
    for folder in sorted(counts):
        add(f"  {folder + '/':<26} {counts[folder]:>3} files")
    add(f"  {'TOTAL':<26} {total:>3} files")
    add("")
    add("-" * 74)
    add("")
    add("AFTER THE MERGE — STRAY LESSONS TO CLEAR")
    add("")
    add("  Your drive currently has last year's Art lessons sitting alongside this")
    add("  year's, in the same folders. This pack ships NONE of them, so the merge")
    add("  will leave them exactly where they are. Delete each one, or move it into")
    add("  _Legacy_2025-26, so staff cannot open the wrong lesson:")
    add("")
    # Grow and Launch first: those are the strays actually visible on the drive.
    # The Build set is listed last, immediately followed by the caveat that
    # explains why it may not be there at all.
    for folder in ("Art/Grow", "Art/Launch"):
        add(f"  {folder}/")
        for n in LEGACY_STRAYS[folder]:
            add(f"      {n}")
        add("")
    build_key = "Art/Build (repo-only, not seen on the drive)"
    add("  Art/Build/  — only if present:")
    for n in LEGACY_STRAYS[build_key]:
        add(f"      {n}")
    add("")
    add("  (These Build entries exist in the source repository but were NOT")
    add("   visible in your drive's Build folder. If your Build folder does not")
    add("   contain them, there is nothing to do there.)")
    add("")
    add("-" * 74)
    add("")
    add("_Legacy_2025-26 IS UNTOUCHED BY DESIGN")
    add("")
    add("  The pack deliberately contains no `_Legacy_2025-26` folder. A merge")
    add("  therefore cannot add to, overwrite or reorder anything in your archive.")
    add("")
    add("EXTERNAL DEPENDENCIES")
    add("")
    if external_deps:
        for d in external_deps:
            add(f"  * {d}")
    else:
        add("  None. Every stylesheet, script and page this pack loads is inside the")
        add("  `Art` folder itself. The Art suite was checked specifically for the")
        add("  LundyLoop stylesheet dependency that affects other subject packs —")
        add("  no Art page references it, so nothing outside `Art` is required.")
    add("")
    add("VIEWING THE PAGES")
    add("")
    add("  * OneDrive's web preview may ignore linked CSS and JavaScript. A lesson")
    add("    opened in the browser preview can look unstyled and its interactive")
    add("    panels may not appear. This is a preview limitation, not a broken file.")
    add("  * To see a page as pupils will: sync the folder (or download the file)")
    add("    and open it in Edge or Chrome from your own machine.")
    add("  * Start at  Art/index.html  or  Art/art_teesside.html")
    add("")
    add("PUPIL DATA")
    add("")
    add("  These pages store nothing on a server. Anything a teacher types into a")
    add("  cold-call list or an evidence tracker is saved in that browser, on that")
    add("  machine only — it does not travel with the file and it is not in this")
    add("  zip. Copying a page to another machine does not carry the data with it.")
    add("")
    add("=" * 74)
    (pack / "Art" / "PLACEMENT_GUIDE.txt").write_text("\n".join(L) + "\n",
                                                      encoding="utf-8")


# ---------------------------------------------------------------- validation
def residue_sweep(pack: Path, whitelist: bool):
    """Count pages carrying Made-by-Matt residue.

    whitelist=True  -> the single canonical credit element is removed first.
    whitelist=False -> nothing is removed; every page should hit exactly once,
                       which is what proves the whitelist is anchored on the
                       credit element and is not masking real residue."""
    hits, detail = 0, []
    for p in sorted(pack.rglob("*.html")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        s = t.replace(">" + bsp.CREDIT + "<", "><", 1) if whitelist else t
        if bsp.PERSONAL_RESIDUE.search(s):
            hits += 1
            detail.append(str(p.relative_to(pack)))
    return hits, detail


def inline_js_check(pack: Path):
    bad = []
    for p in sorted(pack.rglob("*.html")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        for mm in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', t, re.S | re.I):
            body = mm.group(1).strip()
            if not body or (body.startswith("{") and body.endswith("}")):
                continue
            r = subprocess.run(["node", "--check", "-"], input=body, text=True,
                               capture_output=True)
            if r.returncode != 0:
                err = next((l for l in r.stderr.splitlines() if "Error" in l), "unknown")
                bad.append(f"{p.relative_to(pack)}: {err[:110]}")
                break
    return bad


def js_asset_check(pack: Path):
    bad = []
    for p in sorted(pack.rglob("*.js")):
        r = subprocess.run(["node", "--check", str(p)], capture_output=True, text=True)
        if r.returncode != 0:
            bad.append(f"{p.relative_to(pack)}: syntax error")
    return bad


def walk_counts(pack: Path, plus_root=0):
    """Per-folder file counts, walked. `plus_root` accounts for files that will
    be written into Art/ after this walk (the guide and the manifest), so the
    numbers printed inside them describe the finished tree, not a stale one."""
    by_folder = defaultdict(int)
    for f in sorted(pack.rglob("*")):
        if f.is_file():
            by_folder[os.path.dirname(str(f.relative_to(pack)))] += 1
    by_folder["Art"] += plus_root
    return dict(by_folder), sum(by_folder.values())


# ---------------------------------------------------------------- main
def main():
    import argparse, hashlib
    ap = argparse.ArgumentParser()
    ap.add_argument("--logo", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    repo, out = Path(a.repo).resolve(), Path(a.out).resolve()
    bsp.REPO = repo

    print("=" * 70)
    print("PROGRESS SCHOOLS ART MIRROR")
    print("=" * 70)

    # ---- logo (SHA-gated inside load_logo; no fallback exists)
    (lock_uri, lock_size), (mark_uri, mark_size) = bsp.load_logo(a.logo)
    print(f"logo OK  lockup {lock_size}  mark {mark_size}  "
          f"({len(lock_uri)} b64 chars, {len(lock_uri)*3//4/1024:.1f} KB)")
    mark_html = bsp.logo_html(lock_uri, lock_size)

    # ---- scope + geometry
    pairs, dropped = art_scope(repo)
    fwd = {r: d for r, d in pairs}
    print(f"scope: {len(pairs)} files in, {len(dropped)} deliberately excluded")

    if out.exists():
        shutil.rmtree(out)
    pack = out / "pack"
    (pack / "Art").mkdir(parents=True)

    # ---- assemble
    totals, logo_pages, avl_fails, avl_seen, rewrites = defaultdict(int), 0, [], 0, 0
    for rel, dest in pairs:
        src = repo / rel
        target = pack / dest
        if src.suffix != ".html":
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
            continue
        raw = src.read_text(encoding="utf-8", errors="ignore")
        new, log = art_rebrand(raw, rel, mark_html, mark_uri)
        if log.get("logo_swapped"):
            logo_pages += 1
        else:
            # pages that never carried a drawn mark: the hub and the two
            # position-dependent front doors get one, so a staff member landing
            # there sees the school's mark rather than an unbranded page.
            if rel in (ART_HUB, "Launch/index.html"):
                new, _n = bsp.brand_header(new, mark_html)
        new, n = bsp.rewrite_links(new, rel, fwd, dest_override=dest)
        rewrites += n
        if bsp.avl_blocks(raw):
            avl_seen += 1
            f = bsp.check_avl_preserved(raw, new, rel)
            if f:
                avl_fails.append(f)
        for k, v in log.items():
            if k != "delta":
                totals[k] += v
        bsp.write_guarded(raw, new, target)      # read->transform->assert->write
    print(f"rebrand: {dict(totals)}")
    print(f"link rewrites: {rewrites}")
    print(f"AVL: {avl_seen} decks carry a marker pair, "
          f"{'all preserved byte-for-byte' if not avl_fails else str(len(avl_fails)) + ' ALTERED'}")

    # ---- generated front door + guide (authored BEFORE verification, so the
    #      sweeps and gates cover them too)
    listed = write_art_index(pack, lock_uri, lock_size)
    print(f"generated Art/index.html: {listed} pages listed")

    # Counts are computed once, for the FINISHED tree: everything walked now,
    # plus the guide and the manifest that are still to be written into Art/.
    # A guide that counts the tree before itself understates the zip it describes.
    counts, total_files = walk_counts(pack, plus_root=2)
    write_placement_guide(pack, counts, total_files, [])

    # ---- validation
    fails = []
    html_files = sorted((pack / "Art").rglob("*.html"))
    n_html = len(html_files)

    # cardinality vs the screenshots -> UNMAPPED both ways
    unmapped = []
    got = defaultdict(set)
    for f in html_files:
        rel = str(f.relative_to(pack))
        got[os.path.dirname(rel)].add(os.path.basename(rel))
    for f in (pack / "Art" / "visual-learning").iterdir():
        got["Art/visual-learning"].add(f.name)
    for folder, expect in SCREENSHOT_EXPECT.items():
        have = got.get(folder, set())
        for miss in sorted(set(expect) - have):
            unmapped.append(f"screenshot entry with no shipped file: {folder}/{miss}")
        for extra in sorted(have - set(expect)):
            if f"{folder}/{extra}" in GENERATED:
                continue
            unmapped.append(f"shipped file matching no screenshot entry: {folder}/{extra}")
    for folder in sorted(set(got) - set(SCREENSHOT_EXPECT)):
        unmapped.append(f"shipped folder not in the screenshots: {folder}")
    fails += unmapped

    # residue, both ways
    on, on_d = residue_sweep(pack, whitelist=True)
    off, off_d = residue_sweep(pack, whitelist=False)
    if on:
        fails.append(f"RESIDUE (whitelist on) = {on}, expected 0: {on_d[:5]}")
    if off != n_html:
        fails.append(f"RESIDUE (whitelist off) = {off}, expected {n_html} "
                     "(one credit per page) - the whitelist is not anchored")

    # per-page gates
    nocredit = multicredit = noxb = tiny = notclosed = strip = 0
    for p in html_files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        c = t.count(bsp.CREDIT)
        if c == 0:
            nocredit += 1
        elif c > 1:
            multicredit += 1
        if X_BRAND_META not in t:
            noxb += 1
        if bsp.STRIP in t:
            strip += 1
        if len(t) < 200:
            tiny += 1
        if not t.rstrip().lower().endswith("</html>"):
            notclosed += 1
    if nocredit:    fails.append(f"{nocredit} pages missing the credit")
    if multicredit: fails.append(f"{multicredit} pages carry the credit more than once")
    if noxb:        fails.append(f"{noxb} pages missing the x-brand meta")
    if tiny:        fails.append(f"{tiny} pages truncated or empty")
    if notclosed:   fails.append(f"{notclosed} pages do not end </html>")
    if not strip:   fails.append("no page carries the TEES VALLEY strip")

    # hud.js, both forms
    hud = 0
    for p in html_files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'hud\.js', t, re.I) or bsp.HUD_DYNAMIC.search(t):
            hud += 1
    if hud: fails.append(f"{hud} pages still reference hud.js")

    # document.write discipline: none in the Art set, and none may appear
    dw = [str(p.relative_to(pack)) for p in html_files
          if re.search(r'document\s*\.\s*write\s*\(', p.read_text(encoding="utf-8", errors="ignore"))]
    if dw: fails.append(f"document.write present in {len(dw)} pages: {dw[:3]}")

    # crawl closure, each file from its own location
    miss = bsp.crawl(pack)
    if miss:
        fails.append(f"CRAWL: {sum(len(v) for v in miss.values())} unresolved targets")
        for f, ts in list(miss.items())[:10]:
            print("  BROKEN:", f, "->", sorted(ts)[:4])
    ref_fails = bsp.check_avl_refs(pack)
    fails += avl_fails + ref_fails

    # syntax
    js = inline_js_check(pack) + js_asset_check(pack)
    fails += js

    # the Made-by-Matt monogram favicon must be gone, and no mailto may be dead
    mono = dead = 0
    import base64 as _b64
    for p in html_files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        for m in SVG_DATA_URI.finditer(t):
            try:
                if MONOGRAM_PATH in _b64.b64decode(m.group(1)).decode("utf-8", "ignore"):
                    mono += 1
            except Exception:
                pass
        for m in re.finditer(r'href="mailto:([^"]*)"', t):
            if "@" not in m.group(1):
                dead += 1
    if mono: fails.append(f"{mono} Made-by-Matt monogram favicons still ship")
    if dead: fails.append(f"{dead} dead mailto: links (address is not an address)")

    # no pupil data: only page/runtime/text file types may ship
    ALLOWED = {".html", ".js", ".css", ".txt"}
    strays = [str(p.relative_to(pack)) for p in (pack / "Art").rglob("*")
              if p.is_file() and p.suffix.lower() not in ALLOWED]
    if strays: fails.append(f"unexpected file types in the pack: {strays[:5]}")

    # logo honesty
    visible = sum(1 for p in html_files
                  if 'alt="Progress Schools"' in p.read_text(encoding="utf-8", errors="ignore"))
    meta_only = n_html - visible

    # manifest, walked. Its own row and the guide's are already accounted for
    # by walk_counts(plus_root=2), so the printed total IS the zip's entry count.
    rows = [(str(f.relative_to(pack)), f.stat().st_size)
            for f in sorted((pack / "Art").rglob("*")) if f.is_file()]
    by_folder = counts
    if sum(by_folder.values()) != len(rows) + 1:
        fails.append(f"manifest cardinality does not close: "
                     f"{sum(by_folder.values())} counted vs {len(rows) + 1} on disk")

    print("\n" + "-" * 70)
    print(f"pages            : {n_html}")
    print(f"files in tree    : {total_files}")
    print(f"residue on/off   : {on} / {off}  (expect 0 / {n_html})")
    print(f"x-brand missing  : {noxb}")
    print(f"hud.js refs      : {hud}")
    print(f"crawl broken     : {sum(len(v) for v in miss.values())}")
    print(f"inline+asset JS  : {len(js)} syntax errors")
    print(f"logo visible     : {visible} of {n_html} pages ({meta_only} meta/credit only)")
    print(f"AVL loaders      : {'all resolve in-pack' if not ref_fails else 'BROKEN'}")
    print("-" * 70)
    for f in fails[:25]:
        print("  FAIL:", f)
    if not fails:
        print("  ALL CHECKS PASS")

    assert not fails, f"{len(fails)} checks failed - refusing to package"

    # ---- manifest file, then zip
    man = ["PROGRESS SCHOOLS ART MIRROR - MANIFEST", "",
           "Walked from the assembled tree, never typed. The per-folder counts",
           "below sum to the total, and the total is the zip's entry count.", ""]
    for folder in sorted(by_folder):
        man.append(f"{folder + '/':<30} {by_folder[folder]:>3} files")
    man.append("")
    man.append(f"{'TOTAL':<30} {total_files:>3} files")
    man.append("")
    man.append("-" * 70)
    man.append("")
    for rel, size in rows:
        man.append(f"{size:>9}  {rel}")
    man.append(f"{'(this file)':>9}  Art/MANIFEST.txt")
    (pack / "Art" / "MANIFEST.txt").write_text("\n".join(man) + "\n", encoding="utf-8")

    zpath = out / "Progress_Schools_Art_Mirror.zip"
    n = 0
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted((pack / "Art").rglob("*")):
            if f.is_file():
                z.write(f, str(Path("Art") / f.relative_to(pack / "Art")))
                n += 1
    assert n == total_files, f"zip has {n} entries but the manifest states {total_files}"
    print(f"\nPACKAGED {zpath.name}: {n} entries, {zpath.stat().st_size/1024/1024:.2f} MB")

    report = {
        "pages": n_html, "files": n, "logo_visible": visible, "logo_meta_only": meta_only,
        "residue_on": on, "residue_off": off, "hud": hud, "rewrites": rewrites,
        "by_folder": dict(by_folder), "unmapped": unmapped,
        "avl_decks": avl_seen, "excluded": len(dropped),
    }
    (out / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["by_folder"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
