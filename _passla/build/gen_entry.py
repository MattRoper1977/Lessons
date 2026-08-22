# -*- coding: utf-8 -*-
"""Entry-point generator for the LAUNCH ASDAN suite: hub + per-strand START_HERE +
Scheme of Work page. Regenerated from the lesson content modules (Pathway-Tracker
principle), never hand-edited. Mirrors GROW's measured entry-point inventory, but
CLEAN of GROW's drift (no 'Delivering a Project', no 'registration via UAS
coordinator', no L2 registration). PEQ year-target framing lives at hub/START_HERE
level only."""
import os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
import gen  # for PALETTES

ROOT = gen.ROOT
OUT = os.path.join(ROOT, "LAUNCH_ASDAN")

def E(s): return html.escape(str(s), quote=False)
def blurb(L):
    s = L['success'][0]
    return s[5:].strip() if s.lower().startswith("i can ") else s

MATT = ('<div style="text-align:center;margin:14px 0"><svg width="56" height="56" viewBox="0 0 100 100">'
 '<circle cx="50" cy="50" r="47" fill="none" stroke="#1e3a8a" stroke-width="3.4"/>'
 '<g transform="translate(0 2)"><path d="M28 71 L28 37 L50 59 L72 37 L72 71" fill="none" stroke="#1e3a8a" '
 'stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
 '<path d="M50 22.5 L51.48 28.52 L57.5 30 L51.48 31.48 L50 37.5 L48.52 31.48 L42.5 30 L48.52 28.52 Z" fill="#F2A24A"/></g></svg></div>')

def page_head(title, col):
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
      '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
      f'<title>{E(title)}</title><style>\n'
      "body{font-family:'Segoe UI',system-ui,sans-serif;background:#faf7f0;color:#1f2937;margin:0;padding:24px}\n"
      ".wrap{max-width:900px;margin:0 auto} h1{text-align:center;margin:6px 0 2px}\n"
      ".sub{text-align:center;color:#64748b;font-weight:700;margin:0 0 14px}\n"
      f".card{{display:block;background:#fff;border:2px solid {col}33;border-left:8px solid {col};border-radius:12px;padding:12px 16px;margin:10px 0;text-decoration:none;color:#1f2937}}\n"
      f".card:hover{{border-color:{col}}} .card b{{color:{col}}}\n"
      "table{width:100%;border-collapse:collapse;font-size:.9rem} th,td{border:1px solid #e2e8f0;padding:6px 8px;text-align:left;vertical-align:top}\n"
      "th{background:#f1f5f9} h2{margin-top:26px}\n"
      ".bank{background:#fef9ec;border-left:5px solid #C08A3E;padding:8px 12px;border-radius:8px;font-size:.92rem}\n"
      f".note{{background:{col}14;border-radius:10px;padding:10px 14px;font-size:.92rem;margin-top:14px}}\n"
      "ul{margin:6px 0 0 18px}\n"
      f"h1{{color:{col}}}\n"
      "</style></head><body><div class=\"wrap\">"+MATT)

# strand meta: key, product line, folder, note (short course/PEQ framing)
def strand_note(key):
    if key=="PEQ":
        return ("\U0001f3c5 Personal Effectiveness · works toward <b>PEQ Level 1 Award / Extended Award / "
                "Certificate</b> across the year (E3–L1 only in 2026/27). This Autumn 1 module completes "
                "<b>Communication skills (ComSk1)</b>. Every lesson ends with Documentarian photo + annotation "
                "+ witness tick; the Stretch tier is written to an L2 evidence standard (stretch language only, "
                "no L2 registration). PEQ candidates are registered with ASDAN and their units are entered.")
    return ("\U0001f3c5 Banks the named ASDAN short course + AQA UAS. Every lesson ends with Documentarian photo "
            "+ annotation + witness tick; Supported / Standard / Stretch tiers throughout.")

def start_here(mod):
    key = mod.STRAND_KEY; col = gen.PALETTES[key]['lo']; folder = mod.FOLDER
    lessons = mod.LESSONS
    # product line from title_full prefix
    product = lessons[0]['subtitle'].split(' · ',2)[-1]
    cards=""
    for L in lessons:
        cards += (f'<a class="card" href="{E(L["filename"])}"><b>Week {L["week"]}</b> · {E(L["title_short"])}'
                  f'<br><span style="font-size:.88rem;color:#64748b">{E(blurb(L))}</span></a>')
    title = product
    return (page_head(title, col)
      + f'<h1>{E(product)}</h1><p class="sub">LAUNCH Pathway · ASDAN Studio · Autumn 1 · 2026–27</p>'
      + cards
      + f'<div class="note">{strand_note(key)}</div>'
      + '<p style="text-align:center"><a href="../LAUNCH_ASDAN_Hub.html" '
      + f'style="color:{col};font-weight:800">&larr; Back to the LAUNCH ASDAN hub</a></p>'
      + '</div></body></html>')

def hub(mods):
    col = gen.PALETTES['PEQ']['lo']
    cards=""
    for mod in mods:
        k=mod.STRAND_KEY; c=gen.PALETTES[k]['lo']; product=mod.LESSONS[0]['subtitle'].split(' · ',2)[-1]
        n=len(mod.LESSONS)
        if k=="PEQ":
            summ="6 lessons · W1–6 · Autumn 1 · completes Communication skills (ComSk1); works toward PEQ L1 Award / Extended Award / Certificate across the year"
        else:
            summ=f"{n} lessons · W1–{n} · Autumn 1 · banks the ASDAN short course + AQA UAS"
        cards += (f'<a class="card" style="border-left-color:{c}" href="{E(mod.FOLDER)}/START_HERE.html">'
                  f'<b style="color:{c}">{E(product)}</b><br>'
                  f'<span style="font-size:.88rem;color:#64748b">{E(summ)}</span></a>')
    note = ('The five ASDAN strands run in parallel across Autumn 1. <b>Personal Effectiveness</b> is the PEQ spine: '
            'this half-term completes <b>Communication skills (ComSk1)</b>, and the full-year strand homes all six '
            'Level 1 units, so the pathway works toward a PEQ <b>L1 Award / Extended Award / Certificate</b> '
            '(E3–L1 only in 2026/27; L2 is stretch language only, never a registration). The other four strands '
            'bank ASDAN short courses (Careers &amp; Experiencing Work, Living Independently, Hospitality / Gardening, '
            'Community / Active Citizenship) with AQA UAS, and give the PEQ skills real contexts to be evidenced in. '
            'Every lesson runs the v5 studio chassis with the printable Assessor Witness Statement.')
    return (page_head("LAUNCH ASDAN · the full term", col)
      + '<h1>LAUNCH ASDAN · the full term</h1>'
      + '<p class="sub">LAUNCH Pathway · ASDAN Studio · Autumn 1 · 2026–27</p>'
      + cards + f'<div class="note">{note}</div></div></body></html>')

def scheme(mods):
    col = gen.PALETTES['PEQ']['lo']
    out = [page_head("LAUNCH ASDAN · Scheme of Work · Aut 1", col),
      '<h1>LAUNCH ASDAN · Scheme of Work</h1>',
      '<p class="sub">Autumn 1 · 2026–27 · five ASDAN strands</p>',
      '<div class="note"><b>The design in one paragraph.</b> Five ASDAN strands run across Autumn 1 on the v5 studio '
      'chassis: 3-tier arrival and exit, I-Do → We-Do → Independent (15:00, Supported/Standard/Stretch), '
      'Lundy artefact slide, evidence loop (photo · annotation · witness), full print pack off the title slide. '
      '<b>Personal Effectiveness</b> completes <b>Communication skills (ComSk1)</b> this half-term and works toward a '
      'PEQ <b>L1 Award / Extended Award / Certificate</b> across the year (E3–L1 only; Stretch tier written to an '
      'L2 evidence standard, so moving a flying pupil up is a registration decision, not a re-teach — no L2 '
      'registration is claimed here). The other four strands bank ASDAN short courses + AQA UAS.</div>']
    for mod in mods:
        k=mod.STRAND_KEY; c=gen.PALETTES[k]['lo']; product=mod.LESSONS[0]['subtitle'].split(' · ',2)[-1]
        out.append(f'<h2 style="color:{c}">{E(product)}</h2>')
        if k=="PEQ":
            out.append('<p class="bank">Works toward PEQ Level 1 (Award / Extended Award / Certificate; E3–L1 only in '
                       '2026/27). Autumn 1 completes Communication skills (ComSk1). Stretch tier written to an L2 evidence '
                       'standard — stretch language only, never an L2 registration. Registered with ASDAN; units entered.</p>')
        else:
            out.append('<p class="bank">Banks the ASDAN short course named per week + AQA UAS. Off-site / practical work runs '
                       'under the school’s Trips &amp; Visits and health-and-safety policies.</p>')
        rows=""
        for L in mod.LESSONS:
            rows += (f'<tr><td><b>W{L["week"]}</b></td><td><b>{E(L["title_short"])}</b></td>'
                     f'<td>{E(L["success"][0])}</td><td>{E(L["banks"])}</td></tr>')
        out.append('<table><tr><th>Wk</th><th>Lesson</th><th>Core outcome</th><th>Banks</th></tr>'+rows+'</table>')
    out.append('<div class="note"><b>Before-teaching checklist:</b> Trips &amp; Visits booking for any off-site community or '
      'vocational work · display space claimed for the strand boards. PEQ cohort registered with ASDAN and units entered; '
      'IQA before any EQA sampling. <b>No L2 registration in 2026/27.</b></div>')
    out.append('<p style="text-align:center"><a href="LAUNCH_ASDAN_Hub.html" '
      f'style="color:{col};font-weight:800">&larr; Back to the LAUNCH ASDAN hub</a></p>')
    out.append('</div></body></html>')
    return "".join(out)

def build():
    import content_peq, content_careers, content_living, content_vocational, content_community
    mods=[content_peq, content_careers, content_living, content_vocational, content_community]
    written=[]
    for mod in mods:
        p=os.path.join(OUT, mod.FOLDER, "START_HERE.html")
        open(p,"w",encoding="utf-8").write(start_here(mod)); written.append(p)
    p=os.path.join(OUT,"LAUNCH_ASDAN_Hub.html"); open(p,"w",encoding="utf-8").write(hub(mods)); written.append(p)
    p=os.path.join(OUT,"Scheme_of_Work.html"); open(p,"w",encoding="utf-8").write(scheme(mods)); written.append(p)
    return written

if __name__=="__main__":
    for p in build(): print("wrote", os.path.relpath(p, ROOT), os.path.getsize(p),"b")
