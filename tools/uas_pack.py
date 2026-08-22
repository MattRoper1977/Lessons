#!/usr/bin/env python3
"""§9.3b - place the AQA UAS Register into the pack under the pointer-first ruling.

    python3 tools/uas_pack.py PACK_DIR --site SITE_REPO --logo PATH [--writable]

THE RULING THIS IMPLEMENTS
--------------------------
The Register is a DATA-HOLDING tool. Two writable instances of a pupil-record app
cannot be reconciled: the share copy and the live app are different origins, so
they never sync, each machine gets its own database, and every staff member who
copies the folder forks the record again. So the default deliverable is a
Progress-branded LAUNCHER that opens the live app, plus the offline copy beside it,
banner-marked REFERENCE / TRAINING ONLY.

A fully writable offline copy ships only if the two gates pass AND THE OWNER HAS
SAID YES IN WRITING. Gates passing is not permission - --writable exists so the
decision is explicit and recorded, and it refuses without --owner-said-yes.

WHAT THE GATES ACTUALLY MEASURED (tools/uas_probe.mjs)
------------------------------------------------------
  storage-origin  PASS on file:// - IndexedDB opened, wrote, and the value
                  survived a reload
  offline census  PASS - 0 external origins at runtime with the network blocked.
                  All six libraries that used to come from cdnjs are vendored:
                  jsPDF, PDF.js + worker, Tesseract + worker + core wasm + the eng
                  language data. Measured at runtime, because a <script src> grep
                  misses the wasm, the worker and the language data - which is most
                  of what the OCR path loads.
  empty register  PASS - proven by LOADING the copy and reading the store:
                  uas_register {evidence 0, marks 0, pupils 0, sessions 0, units 0,
                  kv 0}, localStorage 0 keys.

AND THE CAVEAT THAT MATTERS MORE THAN THE PASSES
------------------------------------------------
The storage probe ran in headless Chromium against a LOCAL ext4 path. Staff will
open this from a OneDrive-synced folder or a UNC share, which is precisely where
Chrome gives an opaque origin and IndexedDB fails or silently discards. That
environment could not be tested here. A pass measured somewhere staff will never
open it is not evidence about where they will, and it is not a reason to weaken
the ruling.
"""
from __future__ import annotations

import argparse
import base64
import re
import sys
from pathlib import Path

DEST = "ASDAN PEQ/UAS Register"
LIVE = "https://madebymatt.uk/uas/app.html"

BANNER = """<div style="position:sticky;top:0;z-index:99999;background:#8B0000;color:#fff;
padding:14px 18px;font:700 15px/1.45 system-ui,sans-serif;text-align:center;
border-bottom:4px solid #fff">
REFERENCE / TRAINING ONLY &mdash; DO NOT ENTER PUPIL EVIDENCE HERE.<br>
<span style="font-weight:400;font-size:13px">This is an offline copy on the school
network. Anything typed here is saved <b>only in this browser on this machine</b>,
is not the record, and will not reach anyone else. The record of truth is the live
register at <b>madebymatt.uk/uas/app.html</b>.</span></div>"""


def strip_hud(text):
    """Every loader form, not just the one a <script src> grep finds."""
    n = 0
    text, k = re.subn(r'\s*<script[^>]*hud\.js[^>]*>\s*</script>', "", text, flags=re.I)
    n += k
    text, k = re.subn(r'\s*<script[^>]*id=["\']grow-hud-loader["\'][^>]*>.*?</script>',
                      "", text, flags=re.S | re.I)
    n += k
    return text, n


def write_checked(path, text):
    """§9.6 write discipline: never open for writing before the output is proven."""
    assert text.strip(), f"{path}: refusing to write an empty file"
    if path.suffix.lower() == ".html":
        assert text.rstrip().endswith("</html>"), f"{path}: output does not end </html>"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def launcher(mark_uri):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-brand" content="Progress Schools">
<title>AQA UAS Register &mdash; Progress Schools</title>
<style>
 body{{margin:0;background:#f4f4f7;color:#1b2140;
      font:16px/1.55 system-ui,"Segoe UI",sans-serif}}
 .wrap{{max-width:760px;margin:0 auto;padding:2.4rem 1.2rem 3rem}}
 .chip{{display:inline-flex;align-items:center;justify-content:center;background:#fff;
       padding:10px 14px;border-radius:10px;border:1px solid #dcdce6}}
 .chip img{{display:block;height:52px;width:auto}}
 h1{{font-size:1.5rem;margin:1.4rem 0 .3rem}}
 .go{{display:inline-block;margin:1.1rem 0;padding:.85rem 1.5rem;background:#29235b;
     color:#fff;text-decoration:none;border-radius:8px;font-weight:700}}
 .go:hover{{background:#3a3280}}
 .card{{background:#fff;border:1px solid #dcdce6;border-radius:10px;
       padding:1rem 1.2rem;margin:1rem 0}}
 .warn{{border-left:5px solid #8B0000}}
 code{{background:#ececf2;padding:.1rem .3rem;border-radius:4px}}
 footer{{margin-top:2rem;font-size:.82rem;color:#5b5b73}}
</style></head><body><div class="wrap">

<span class="chip"><img src="{mark_uri}" alt="Progress Schools"></span>
<h1>AQA UAS Register</h1>
<p>PROGRESS SCHOOLS &middot; TEES VALLEY</p>

<a class="go" href="{LIVE}">Open the live register &rarr;</a>

<div class="card warn">
<p><b>Use the live register. It is the record of truth.</b></p>
<p>The offline copy in this folder &mdash; <code>app_REFERENCE_ONLY.html</code> &mdash;
is for looking at and for training. <b>Do not enter pupil evidence into it.</b> It
saves into the browser on whichever machine opens it, it does not sync anywhere,
and nobody else will ever see what is typed there.</p>
</div>

<div class="card">
<p><b>Why there is only one writable copy.</b> This tool holds pupil records. A copy
on a shared drive is a different origin from the live app, so the two can never sync.
Every machine that opened a writable copy would build its own separate register, and
every person who copied the folder would fork the record again. One register, online,
is the only version of this that stays true.</p>
</div>

<div class="card">
<p><b>Things that are true of the live register too, and catch people out:</b></p>
<ul>
<li>Data is stored <b>per machine and per browser</b>. Nothing syncs between them.</li>
<li>Clearing browser data <b>wipes it</b>.</li>
<li><b>Export a backup before any machine reimage.</b></li>
</ul>
</div>

<footer>PROGRESS SCHOOLS &middot; TEES VALLEY &mdash; internal pack. See
<code>0_ABOUT_THIS_TOOL.txt</code> in this folder.<br>
<span>by madebymatt.uk</span></footer>
</div></body></html>
"""


ABOUT = """AQA UAS REGISTER - what is in this folder, and which one to use
================================================================================

index.html                  The launcher. START HERE. It opens the live register.
app_REFERENCE_ONLY.html     An offline copy. LOOK, DO NOT TYPE.
0_STAFF_ONLY_cover_for_settings_upload/
                            The Progress evidence-pack cover image, for uploading
                            into the live register's Settings. Staff only.

WHICH ONE DO I USE?
  The live one, at madebymatt.uk/uas/app.html. Always. The launcher opens it.

WHY IS THE OFFLINE COPY MARKED "DO NOT ENTER PUPIL EVIDENCE"?
  Because it would work, and that is the problem. It would save what you typed -
  into the browser on that one machine, where nobody else can see it, and where it
  is not part of the record. Two writable copies of a pupil register cannot be
  reconciled: they are different origins, they never sync, and every person who
  copies this folder forks the record again.

WHAT WORKS OFFLINE IN THE COPY
  All of it, as far as loading goes. The six libraries this tool used to fetch from
  the internet at runtime - the PDF writer, the PDF reader and its worker, and the
  OCR engine with its worker, its wasm core and its English language data - are all
  packaged inside. Measured with the network switched off: zero outside requests.

  So register entry, PDF export, outcome-sheet reading and photo OCR all load
  without the internet. That is about the SOFTWARE. It says nothing about whether
  what you type is kept, which is the paragraph above.

ONE THING WE COULD NOT TEST
  Whether the browser will keep data at all when this file is opened from a
  OneDrive folder or a network share. Chrome treats some of those as an origin with
  no storage, and when it does, what you type is discarded with no error and no
  warning. We could only test a local disk, where it worked. That gap is another
  reason this copy is marked reference-only.

DATA, WHEREVER YOU ARE
  - Stored per machine AND per browser. Nothing syncs.
  - Clearing browser data wipes it.
  - Export a backup before any machine reimage.

This copy was packed EMPTY and that was checked by opening it and reading the
store, not by reading the file: 0 pupils, 0 sessions, 0 evidence items, 0 marks,
0 units, 0 saved settings.
"""

COVER_NOTE = """PROGRESS SCHOOLS EVIDENCE-PACK COVER - staff only
================================================================================

1. Open the live register (madebymatt.uk/uas/app.html) and go to Settings.
2. Upload cover.png there. It is stored on that machine only, so it has to be
   done once per machine.
"""

RULING = """RULINGS CARRIED BY THIS PACK
================================================================================

1. THE UAS REGISTER IS IN THIS PACK BY OWNER OVERRIDE.
   The estate's standing dual-branding rule is that the registers are
   Made-by-Matt-only and never enter a Progress-branded pack. The owner overrode
   that for this pack, and the override is recorded here rather than assumed.

   IT LICENSES THIS TOOL ONLY. Not the ASDAN Register at asdan/app.html, not the
   Moderation Lab, not any other app, and no games. The ASDAN Register is
   genuinely dependency-free and would pack cleanly under the same override and the
   same three gates - but that is a question to ask, not an assumption to make.

2. THE REGISTER SHIPS AS A LAUNCHER PLUS A REFERENCE-ONLY COPY.
   Both technical gates passed:
     storage-origin   IndexedDB opened, wrote, survived a reload on file://
     offline census   0 external origins at runtime, network blocked
     empty register   0 records, proven by loading the copy and reading its store

   It still ships reference-only, for two reasons:

   a. The written owner consent that the ruling requires alongside those gates has
      not been given. Gates passing is not permission.
   b. The storage gate was measured in headless Chromium against a local disk.
      Staff will open this from OneDrive or a UNC share, which is exactly where
      Chrome gives an opaque origin and silently discards what is typed. That
      environment could not be tested here, and a pass measured somewhere staff
      will never open it is not evidence about where they will.

3. NOTHING WAS COMMITTED TO THE SITE REPOSITORY.
   MattRoper1977.github.io was cloned read-only to take this copy. 0 commits,
   0 pushes, 0 branches, 0 pull requests.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pack")
    ap.add_argument("--site", required=True)
    ap.add_argument("--logo", required=True)
    ap.add_argument("--writable", action="store_true")
    ap.add_argument("--owner-said-yes", action="store_true")
    a = ap.parse_args()

    if a.writable and not a.owner_said_yes:
        sys.exit("HARD STOP: --writable needs --owner-said-yes.\n"
                 "  Both technical gates passing is not permission. The ruling requires\n"
                 "  the owner's yes in writing alongside them, and it has not been given.")

    pack, site = Path(a.pack), Path(a.site)
    src = site / "uas" / "app.html"
    if not src.is_file():
        sys.exit(f"HARD STOP: no register at {src}")

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import logo_master
    res = logo_master.derive(a.logo)
    mark_data, _sha, _size, _n, _c, ok = res["mark"]
    assert ok, "the logo failed its colour-shift gate"
    mark_uri = "data:image/png;base64," + base64.b64encode(mark_data).decode()
    lock_data, _s2, logo_size, _n2, _c2, ok2 = res["lockup"]
    assert ok2, "the lockup failed its colour-shift gate"
    logo_uri = "data:image/png;base64," + base64.b64encode(lock_data).decode()

    dest = pack / DEST
    raw = src.read_text(encoding="utf-8")
    original_len = len(raw)

    # The copy goes through the SAME rebrand every other page in the pack goes
    # through - imported, never re-implemented - so it carries the x-brand marker,
    # the strip, exactly one credit and no residue, and is gated by mirror_verify
    # alongside everything else. Writing it out by hand would have made the one
    # file holding pupil records the one file nothing checked.
    import build_staff_pack as bsp
    bsp.LOGO_URI[:] = [logo_uri, logo_size]
    bsp.LOGO_HTML[0] = bsp.logo_html(logo_uri, logo_size)
    text, rebrand_log = bsp.mirror_rebrand(raw, DEST + "/app_REFERENCE_ONLY.html",
                                           bsp.LOGO_HTML[0])
    text = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + BANNER, text, count=1)
    text, stripped = strip_hud(text)
    assert len(text) >= original_len * 0.5, "the transform shrank the register by half"
    assert text.rstrip().endswith("</html>"), "the register no longer ends </html>"
    assert "REFERENCE / TRAINING ONLY" in text, "the banner did not land"

    # The vendored libraries the register loads at runtime. Shipping the page
    # without them is the "deck without its loader" defect: the copy opens, looks
    # complete, and its PDF export and OCR are dead. The offline census did not
    # catch it - a worker that fails to load from file:// is not an EXTERNAL origin,
    # so a census counting external origins reports a clean zero either way. The
    # link crawl over the assembled tree is what found it.
    import shutil as _sh
    vend_src = site / "uas" / "vendor"
    assert vend_src.is_dir(), f"HARD STOP: no vendored libraries at {vend_src}"
    vend_dst = dest / "vendor"
    if vend_dst.exists():
        _sh.rmtree(vend_dst)
    _sh.copytree(vend_src, vend_dst)
    vend_files = sorted(q for q in vend_dst.rglob("*") if q.is_file())
    vend_bytes = sum(q.stat().st_size for q in vend_files)
    # The personal-name census skips this tree, because the author credits inside
    # these libraries are MIT attribution rather than staff data. That exclusion is
    # only safe if the tree is exactly what the site repo holds, so prove it here
    # rather than trusting the copy.
    import hashlib as _hl
    for q in vend_files:
        rel_q = q.relative_to(vend_dst)
        a = _hl.sha256((vend_src / rel_q).read_bytes()).hexdigest()
        b = _hl.sha256(q.read_bytes()).hexdigest()
        assert a == b, f"vendored file differs from source: {rel_q}: {a} != {b}"

    write_checked(dest / "app_REFERENCE_ONLY.html", text)
    write_checked(dest / "index.html", launcher(mark_uri))
    write_checked(dest / "0_ABOUT_THIS_TOOL.txt", ABOUT)
    write_checked(dest / "0_STAFF_ONLY_cover_for_settings_upload" / "0_HOW_TO_USE.txt",
                  COVER_NOTE)
    (dest / "0_STAFF_ONLY_cover_for_settings_upload" / "cover.png").write_bytes(
        res["lockup"][0])
    write_checked(pack / "_Pack_Notes" / "RULINGS.txt", RULING)

    print(f"UAS Register placed at {DEST}/")
    print(f"  index.html                  launcher -> {LIVE}")
    print(f"  app_REFERENCE_ONLY.html     {len(text)} B, hud loaders stripped: {stripped}")
    print(f"      rebrand              {dict(rebrand_log) if rebrand_log else 'no changes'}")
    print(f"  vendor/                     {len(vend_files)} file(s), "
          f"{vend_bytes/1048576:.1f} MB - jsPDF, PDF.js + worker, Tesseract + worker "
          f"+ wasm core + eng data")
    print(f"  0_ABOUT_THIS_TOOL.txt")
    print(f"  0_STAFF_ONLY_cover_for_settings_upload/cover.png + 0_HOW_TO_USE.txt")
    print(f"  _Pack_Notes/RULINGS.txt     the override and the reference-only ruling")
    print(f"\nverdict: LAUNCHER + REFERENCE-ONLY COPY (not writable)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
