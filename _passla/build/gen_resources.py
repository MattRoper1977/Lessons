# -*- coding: utf-8 -*-
"""Standalone Resources_and_Tools.html for GROW then LAUNCH (Matt's overview pick,
Option A). Regenerated from the lesson material, never hand-invented:
 - GROW: kit lists lifted from GROW_ASDAN/Scheme_and_Resources.html (its own file).
 - LAUNCH: per-strand resource blocks composed from the authored lesson tasks.
LAUNCH is built last (after its lessons exist)."""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
import gen

ROOT = gen.ROOT
def E(s): return html.escape(str(s), quote=False)

HEAD = ('<!doctype html><html lang="en-GB"><head><meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
 '<title>{title}</title><style>\n'
 "body{{font-family:'Segoe UI',system-ui,sans-serif;color:#111;max-width:920px;margin:0 auto;padding:28px;line-height:1.5}}\n"
 "h1{{color:{col};margin:.2em 0}}h2{{color:#333;border-bottom:2px solid {col};padding-bottom:4px;margin-top:26px}}\n"
 ".sub{{color:#666;margin:0 0 8px}}\n"
 ".setup{{background:#f6f2fa;border-left:6px solid {col};border-radius:9px;padding:12px 16px;margin:12px 0}}\n"
 ".warn{{background:#fdf1f1;border-left:6px solid #C0684A;border-radius:9px;padding:12px 16px;margin:12px 0}}\n"
 ".slot{{border:1.4px solid #ccc;border-radius:10px;padding:12px 16px;margin:12px 0;page-break-inside:avoid}}\n"
 ".slot h3{{margin:.1em 0 .4em}}.slot p{{margin:5px 0;font-size:13.5px}}\n"
 "ul{{margin:6px 0 0 18px}} li{{font-size:13.5px}}\n"
 "@media print{{body{{padding:8mm}}}}</style></head><body>\n")

def slot(col, title, body):
    return f'<div class="slot" style="border-left:6px solid {col}"><h3 style="color:{col}">{title}</h3><p>{body}</p></div>'

# ---------------------------------------------------------------- GROW
def build_grow():
    src = open(os.path.join(ROOT,"GROW_ASDAN","Scheme_and_Resources.html"),encoding="utf-8").read()
    # each strand: <h2 style="color:HEX">NAME <span...>· day</span></h2> ... <p><b>Kit list:</b></p><ul>...</ul>
    heads = re.findall(r'<h2 style="color:(#[0-9A-Fa-f]{6})">(.*?)</h2>', src)
    kits  = re.findall(r'<p><b>Kit list:</b></p><ul>(.*?)</ul>', src, re.S)
    col = "#4C9A6F"
    out = [HEAD.format(title="Resources &amp; Tools List — GROW ASDAN &middot; Made by Matt", col=col),
      '<h1>Resources &amp; Tools List — GROW ASDAN</h1>',
      '<p class="sub">Made by Matt · Autumn 1 · 2026–27 · three interlocking ASDAN strands · one setup sheet</p>',
      '<div class="setup"><b>One standalone kit sheet for the GROW ASDAN term.</b> The lists below are the same kit named '
      'in the Scheme of Work, gathered here as a single shopping-and-setup page. Every strand runs the v5 studio chassis, '
      'so the shared evidence kit (tablet, witness slips, print packs, display boards) covers all three.</div>']
    for i,(hcol,hname) in enumerate(heads):
        name = re.sub(r'<[^>]+>','',hname).strip()
        kit = kits[i] if i < len(kits) else ""
        out.append(f'<h2 style="color:{hcol}">{E(name)}</h2><ul>{kit}</ul>')
    out.append('<h2>Shared evidence kit (all strands)</h2><p>One tablet for the Documentarian role (photos show work, not '
      'faces, unless consent is filed) · printed witness-statement slips · the full print pack off each title slide · '
      'display space for the term-long Lundy artefact boards (headlines only, never rankings).</p>')
    out.append('<p style="color:#666;font-size:12px;margin-top:18px">Made by Matt · Photos show work, not faces, unless '
      'consent is filed · PEQ registered with ASDAN before assessment counts · Level 1 in 2026/27 (Stretch tier written to '
      'an L2 evidence standard; no L2 registration).</p></body></html>')
    return "".join(out)

# ---------------------------------------------------------------- LAUNCH
# Per-strand resources, composed from the authored lesson tasks (grounded in the lessons).
LAUNCH_RES = {
 "PEQ": ("Six-skill self-assessment cards + PEQ word cards (communication, listening, planning, review) · "
   "the <b>Effectiveness Board</b> display (headlines only, never rankings) · SMART communication-plan sheets + "
   "audience-question cards · feedback (WWW/EBI) slips · sentence-starter strips + L1 command-word mats."),
 "Careers": ("Strengths / interests / sector cards + local-job photo cards · the <b>Careers Board</b> display · "
   "CV and job-application templates · prepared employer-question sheets · pathway and labour-market info cards · "
   "SMART careers-target sheets."),
 "Living_Independently": ("Routine / organisation cards + planner templates · home-safety checklist + hazard cards · "
   "care-symbol cards + sorting trays · cleaning-product label cards (with gloves as PPE) · appointment / document "
   "record templates · <b>Eatwell Guide</b> mat or poster + food picture cards (<b>allergy list checked first — every "
   "food session</b>) + <b>practice money</b> and practice price labels (never family finances) · the Independence Board."),
 "Vocational": ("PPE — goggles, gloves, aprons, sturdy footwear · hand-tool and kitchen/garden-tool sets with a "
   "sign-out tray (count out, count back) · instruction / step cards · team-role cards · task-standard checklists · "
   "the Vocational Board display."),
 "Community_Enterprise": ("Community photo / survey kit + camera or tablet · needs-map display + evidence pins · "
   "project-plan sheets (step · owner · date) + role cards · partner-approach templates · <b>practice money</b> and "
   "price labels for the enterprise (project money only) · the Community Board (need → plan → deliver → promote)."),
}

def build_launch():
    import content_peq, content_careers, content_living, content_vocational, content_community
    mods=[content_peq, content_careers, content_living, content_vocational, content_community]
    col = gen.PALETTES['PEQ']['lo']
    out=[HEAD.format(title="Resources &amp; Tools List — LAUNCH ASDAN &middot; Made by Matt", col=col),
      '<h1>Resources &amp; Tools List — LAUNCH ASDAN</h1>',
      '<p class="sub">Made by Matt · Autumn 1 · 2026–27 · five ASDAN strands · one shopping-and-setup sheet</p>',
      '<div class="setup"><b>One standalone kit sheet for the LAUNCH ASDAN term.</b> Each block lists the resources the '
      'strand’s six lessons actually use, drawn from the lesson tasks themselves. The shared evidence kit (tablet, '
      'witness slips, print packs, display boards) covers all five strands.</div>']
    for mod in mods:
        k=mod.STRAND_KEY; c=gen.PALETTES[k]['lo']
        product=mod.LESSONS[0]['subtitle'].split(' · ',2)[-1]
        out.append(slot(c, E(product), LAUNCH_RES[k]))
    out.append('<h2>Shared evidence kit (all strands)</h2><p>One tablet for the Documentarian role · printed '
      'witness-statement slips (Assessor §4 + Learner §5) · the full print pack off each title slide · display space for '
      'the term-long Lundy artefact boards (headlines only, never rankings) · a photo-printing route for annotated '
      'portfolio evidence.</p>')
    out.append('<div class="warn"><b>Standing checks:</b> photos show work, not faces, unless consent is filed · the '
      'allergy list is checked before any food session · money content is <b>practice money only</b>, never family '
      'finances · tools are counted out and back every session · off-site community or vocational work runs under the '
      'Trips &amp; Visits and health-and-safety policies.</div>')
    out.append('<p style="color:#666;font-size:12px;margin-top:18px">Made by Matt · PEQ registered with ASDAN before '
      'assessment counts; Autumn 1 completes Communication skills (ComSk1) and works toward a PEQ L1 Award / Extended '
      'Award / Certificate across the year (E3–L1 only; Stretch tier written to an L2 evidence standard, no L2 '
      'registration).</p></body></html>')
    return "".join(out)

def build():
    written=[]
    g=os.path.join(ROOT,"GROW_ASDAN","Resources_and_Tools.html")
    open(g,"w",encoding="utf-8").write(build_grow()); written.append(g)
    l=os.path.join(ROOT,"LAUNCH_ASDAN","Resources_and_Tools.html")   # LAUNCH last
    open(l,"w",encoding="utf-8").write(build_launch()); written.append(l)
    return written

if __name__=="__main__":
    for p in build(): print("wrote", os.path.relpath(p,ROOT), os.path.getsize(p),"b")
