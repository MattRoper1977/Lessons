#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contact sheet for all 25 science lessons (SCI-3 §2): per lesson a thumbnail of the title slide,
the illuminator, and page 1 of the standard print pack. Plus the cheap render-only assertions that
only a render can see:
  - illuminator NOT clipped by its viewBox (content getBBox within 0..640 x 0..300)
  - no label pill overlapping another (white .lbl/clip rects; >55% area overlap flagged)
  - print page 1 (print-ko) not blank and not absurdly overflowing

Geometry is measured under reduced-motion (transform:none) = the true resting state (the state the
RM gate cares about), so ilmPop scale-overshoot cannot distort getBBox. Thumbnails use that same
resting render. Output: shots/contact/science_contact_sheet.{html,png} + a printed PASS/FLAG table.
"""
import sys
import base64
import pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE / "inputs"))
OUT = HERE / "out"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

MODS = ["content_build", "content_grow",
        "content_launch_t1", "content_launch_t2", "content_launch_t3",
        "content_launch_t4", "content_launch_t5"]


def lessons():
    out = []
    for m in MODS:
        mod = __import__(m)
        for L in mod.LESSONS:
            out.append((mod.PATHWAY, L["week"], L["slug"], L["title"]))
    return out


BBOX_JS = """() => {
  const svg = document.querySelector('.ilm svg');
  if (!svg) return {err:'no svg'};
  let bb; try { bb = svg.getBBox(); } catch(e) { return {err:String(e)}; }
  const vb = (svg.getAttribute('viewBox')||'0 0 640 300').split(/\\s+/).map(Number);
  // label pills = rects that are white-filled with a coloured stroke (the _lbl / clip boxes)
  const rects = [...svg.querySelectorAll('rect')].filter(r => {
    const f=(r.getAttribute('fill')||'').toLowerCase();
    return f==='#fff' || f==='#ffffff';
  }).map(r => ({x:+r.getAttribute('x'), y:+r.getAttribute('y'),
                w:+r.getAttribute('width'), h:+r.getAttribute('height')}))
    .filter(r => r.w>40 && r.h>=16 && r.h<40);  // label-pill shaped only
  let overlaps=0;
  for (let i=0;i<rects.length;i++) for (let j=i+1;j<rects.length;j++){
    const a=rects[i], b=rects[j];
    const ox=Math.max(0, Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x));
    const oy=Math.max(0, Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y));
    const inter=ox*oy, minA=Math.min(a.w*a.h, b.w*b.h);
    if (minA>0 && inter/minA > 0.55) overlaps++;
  }
  return {bx:bb.x, by:bb.y, bw:bb.width, bh:bb.height, vbw:vb[2], vbh:vb[3], overlaps, nlabels:rects.length};
}"""

PRINT_JS = """() => {
  printPack('standard');
  const ko = document.getElementById('print-ko');
  if (!ko) return {err:'no print-ko'};
  const txt = (ko.innerText||'').trim();
  const r = ko.getBoundingClientRect();
  return {len: txt.length, h: r.height};
}"""


def main():
    rows, flags = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        for pathway, week, slug, title in lessons():
            url = f"file://{OUT}/{slug}.html"
            imgs = {}
            # resting-state render (reduced motion) for geometry + thumbnails
            pg = b.new_page(viewport={"width": 900, "height": 620})
            pg.emulate_media(reduced_motion="reduce")
            pg.goto(url); pg.wait_for_timeout(250)
            imgs["title"] = pg.screenshot()
            pg.evaluate("showSlide(3)"); pg.wait_for_timeout(350)
            geo = pg.evaluate(BBOX_JS)
            el = pg.query_selector(".ilm")
            imgs["ilm"] = (el or pg).screenshot()
            pg.close()
            # print page 1
            pg = b.new_page(viewport={"width": 820, "height": 640})
            pg.add_init_script("window.print=()=>{}")
            pg.goto(url); pg.emulate_media(media="print")
            pr = pg.evaluate(PRINT_JS)
            ko = pg.query_selector("#print-ko")
            imgs["print"] = (ko or pg).screenshot()
            pg.close()
            # assertions
            issues = []
            if "err" in geo:
                issues.append(f"illuminator:{geo['err']}")
            else:
                clip = (geo["bx"] < -1 or geo["by"] < -1
                        or geo["bx"] + geo["bw"] > geo["vbw"] + 1
                        or geo["by"] + geo["bh"] > geo["vbh"] + 1)
                if clip:
                    issues.append(f"CLIPPED bbox=({geo['bx']:.0f},{geo['by']:.0f},"
                                  f"{geo['bx']+geo['bw']:.0f},{geo['by']+geo['bh']:.0f}) vb={geo['vbw']}x{geo['vbh']}")
                if geo["overlaps"] > 0:
                    issues.append(f"{geo['overlaps']} label-pill overlap(s)")
            if "err" in pr:
                issues.append(f"print:{pr['err']}")
            else:
                if pr["len"] < 200:
                    issues.append(f"print p1 BLANK/thin ({pr['len']} chars)")
                if pr["h"] > 1600:
                    issues.append(f"print p1 OVERFLOW ({pr['h']:.0f}px)")
            status = "PASS" if not issues else "FLAG: " + "; ".join(issues)
            print(f"  [{'PASS' if not issues else 'FLAG'}] {pathway} W{week} {slug}: {status if issues else ''}")
            if issues:
                flags.append((slug, issues))
            uri = lambda p: "data:image/png;base64," + base64.b64encode(p).decode()
            badge = ("#16a34a", "PASS") if not issues else ("#b91c1c", "FLAG")
            rows.append(
                f'<tr><td class="lab">{pathway} W{week}<br><b>{title.split(": ",1)[-1]}</b>'
                f'<br><span style="color:{badge[0]};font-weight:800">{badge[1]}</span>'
                + (f'<br><span style="font-size:10px;color:#b91c1c">{"; ".join(issues)}</span>' if issues else "")
                + f'</td><td><img src="{uri(imgs["title"])}"></td>'
                f'<td><img src="{uri(imgs["ilm"])}"></td><td><img src="{uri(imgs["print"])}"></td></tr>')
        b.close()
    html = ("<!doctype html><meta charset=utf-8><title>Science contact sheet (25)</title>"
            "<style>body{font:14px system-ui;margin:18px;background:#f8fafc}h1{font-size:18px}"
            "table{border-collapse:collapse}td{border:1px solid #cbd5e1;padding:6px;vertical-align:top;background:#fff}"
            "img{width:290px;display:block}.lab{width:150px;font-size:12px}th{font-size:12px;padding:6px}</style>"
            "<h1>Science · Teesside — all 25 lessons (resting-state render)</h1>"
            "<p>Per lesson: title slide · illuminator · print pack page 1 (standard). Render-only "
            "assertions: illuminator not clipped by viewBox · no label-pill overlap · print p1 not "
            "blank/overflowing.</p>"
            "<table><tr><th>Lesson</th><th>Title slide</th><th>Illuminator</th><th>Print p.1</th></tr>"
            + "".join(rows) + "</table>")
    (HERE / "shots/contact").mkdir(parents=True, exist_ok=True)
    (HERE / "shots/contact/science_contact_sheet.html").write_text(html, encoding="utf-8")
    print(f"\nCONTACT SHEET: 25 lessons rendered. FLAGS: {len(flags)}")
    for slug, iss in flags:
        print(f"  {slug}: {'; '.join(iss)}")
    return flags


if __name__ == "__main__":
    main()
