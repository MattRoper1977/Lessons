#!/usr/bin/env python3
"""ORDER VB-RUN11F C2 RESHELL RECIPE: n6 deck -> classic chassis (v2).

Right content, right shell. Every pupil-facing sentence of the n6 deck is kept
verbatim (the containment gate proves before ⊆ after); only the shell changes.
The classic parts the n6 deck lacks (KO, Key Facts, WAGOLL, Scaffolding x3,
Independent Work x3 print sheets, Pens-down, Lundy slide + print section,
reference zone, feedback sheet) are AUTHORED from the deck's own text and its
traced workbook cell, and every authored block is listed in TRACE.md.

Usage: reshell.py <n6 deck> <classic donor> <out path> [--json trace.json]
"""
import html as H, json, pathlib, re, sys
from lxml import html as lh
src_path, donor_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
ROOT = pathlib.Path('/home/user/Lessons')
S = (ROOT/src_path).read_text(encoding='utf-8'); D = (ROOT/donor_path).read_text(encoding='utf-8')
tree = lh.fromstring(S); main = tree.xpath('//main')[0]
cfg = json.loads(tree.xpath('//script[@id="lesson-config"]')[0].text)
family = cfg['family']; lane, subject = family.split(' ', 1); week = cfg['week']; title = cfg['title']
TRACE = []
def T(block, source): TRACE.append({'block': block, 'authoredFrom': source})
def inner(el):  # serialised inner html of an element
    return (el.text or '') + ''.join(lh.tostring(c, encoding='unicode') for c in el)
def outer(el): return lh.tostring(el, encoding='unicode')
def txt(el): return ' '.join(el.text_content().split())
def esc(s): return H.escape(s, quote=False)
def is_staff(el): return el.get('data-mbm-guide') is not None or el.get('data-audience') == 'staff'
slides = {s.get('data-type'): s for s in main.xpath('./section[contains(@class,"slide")]')}
def kids(sec):  # direct children except .time/.tag/.lundy strip
    return [c for c in sec if not (c.tag == 'div' and c.get('class') in ('time',)) and not (c.tag == 'span' and c.get('class') == 'tag')]
def lundy_strip(sec):
    l = sec.xpath('./div[contains(concat(" ",normalize-space(@class)," ")," lundy ")]')
    return outer(l[0]) if l else ''
def h2(sec):
    h = sec.xpath('./h2'); return txt(h[0]) if h else ''
def guide(el):  # carry staff guidance with the classic key so the classic mechanism hides it
    return outer(el).replace('data-mbm-guide="staff"', 'data-mbm-guide="staff"', 1)
# ---- block renderers (n6 -> classic furniture) ----------------------------
def render_block(el):
    cls = el.get('class') or ''
    if el.tag == 'div' and 'lundy' == cls.strip(): return ''  # strip is placed separately, verbatim
    if el.tag == 'h2': return ''
    if is_staff(el):
        return f'<div data-mbm-guide="staff" class="li-box">{inner(el)}</div>' if el.tag == 'p' else outer(el)
    if 'hero-visual' in cls: return f'<div class="ilm" role="img">{inner(el)}</div>'
    if 'routes' in cls:
        out = ['<div class="content-grid routes3" style="height:auto;margin-top:10px">']
        col = {'supported': '#22c55e', 'standard': '#f97316', 'stretch': '#1e3a8a'}
        for r in el.xpath('./article'):
            tier = next((k for k in col if k in (r.get('class') or '')), 'standard')
            hh = r.xpath('./h3'); ps = r.xpath('./p')
            out.append(f'<div class="task-box"><h3 style="margin-top:0;color:{col[tier]}">{inner(hh[0]) if hh else tier.title()}</h3>' + ''.join(f'<p>{inner(p)}</p>' for p in ps) + '</div>')
        return ''.join(out) + '</div>'
    if 'evidence-gate' in cls:
        return f'<div class="task-box wedo-reveal" style="display:none"><h3 style="margin-top:0;color:var(--wedo-border)">Evidence check</h3>{inner(el)}</div>'
    if 'lundy-status' in cls: return f'<div class="ido-box">{inner(el)}</div>'
    if 'options' in cls or cls.strip() == 'grid':
        boxes = el.xpath('./div')
        n = min(max(len(boxes), 1), 3)
        return f'<div class="arrival-grid cols{n}">' + ''.join(f'<div class="task-box">{inner(b)}</div>' for b in boxes) + '</div>'
    if el.tag == 'div' and 'box' in cls.split():
        if 'model' in cls: return f'<div class="ido-box">{inner(el)}</div>'
        if 'task' in cls: return f'<div class="li-box">{inner(el)}</div>'
        return f'<div class="task-box">{inner(el)}</div>'
    if el.tag == 'p':
        if 'truth' in cls: return f'<div class="li-box" style="border-left:8px solid var(--sc-border)">{inner(el)}</div>'
        if 'access' in cls: return f'<div class="scaffold-box">{inner(el)}</div>'
        return f'<p>{inner(el)}</p>'
    if el.tag == 'div' and 'hero' in cls.split(): return ''  # title hero handled separately
    return outer(el)
def body_of(sec, skip_first_h2=True):
    return ''.join(render_block(c) for c in kids(sec))
# ---- title slide -----------------------------------------------------------
t = slides['title']; hero = t.xpath('.//div[@class="hero"]')[0]
hero_ps = [p for p in hero.xpath('./p')]
chips = [txt(c) for c in hero.xpath('.//div[@class="chips"]/span')]
ladder = hero.xpath('.//div[@class="ladder"]'); ladder_t = txt(ladder[0]) if ladder else ''
staff_cards = ''.join(outer(c) for c in hero.xpath('./div[@data-mbm-guide]'))
routes_html = render_block(t.xpath('./div[@class="routes"]')[0]) if t.xpath('./div[@class="routes"]') else ''
rest_title = ''.join(render_block(c) for c in kids(t) if not (c.tag == 'div' and (c.get('class') or '') in ('hero', 'routes')))

weeks = 8 if week <= 8 else 7
term = 'Aut 1' if week <= 8 else 'Aut 2' if week <= 15 else 'Spr 1' if week <= 21 else 'Spr 2'
wk_in = week if week <= 8 else week - 8 if week <= 15 else week - 15 if week <= 21 else week - 21
_logo = re.search(r'<svg[^>]*aria-label="Made by Matt".*?</svg>', D, re.S)
LOGO = '<div style="text-align:center;margin-top:10px">' + (_logo.group(0) if _logo else '') + '</div>'
tagcol = {'BUILD': '#E08A2E', 'GROW': '#3F7D6E', 'LAUNCH': '#7A5C9E'}[lane]
btns = ('<div class="scaffold-box" style="display:inline-block;margin-top:8px;text-align:left"><h3 style="margin-top:0">Teacher Print Tools — Week %d</h3><div style="display:flex;gap:14px;flex-wrap:wrap">'
        '<button onclick="printPack(\'supported\')" style="background:#22c55e;color:#fff;border:none;border-radius:8px;padding:8px 16px;font-weight:800;cursor:pointer">🖨 Supported pack</button>'
        '<button onclick="printPack(\'standard\')" style="background:#f97316;color:#fff;border:none;border-radius:8px;padding:8px 16px;font-weight:800;cursor:pointer">🖨 Standard pack</button>'
        '<button onclick="printPack(\'stretch\')" style="background:#1e3a8a;color:#fff;border:none;border-radius:8px;padding:8px 16px;font-weight:800;cursor:pointer">🖨 Stretch pack</button></div></div>') % week
title_slide = f'''<div class="slide active" data-title="Title"> {LOGO} <div style="text-align:center;margin-top:1%"><div class="animate-enter">
<span class="slide-tag tag-lesson" style="background:{tagcol};color:#fff">{lane} · Week {wk_in} of {weeks}</span>
<h1>{esc(title)}</h1>
<p style="font-size:1.1rem;color:var(--muted);margin:-8px 0 6px">{inner(hero_ps[0]) if hero_ps else esc(family)}</p>
<div data-mbm-guide="route" class="sow-strip">Progress SoW · {esc(subject)} {term} · 2026–27 · {lane} · Week {wk_in} · {esc(cfg["cells"][0])}</div>
{''.join(f'<div class="li-box" style="margin:10px auto;max-width:680px;text-align:left">{inner(p)}</div>' for p in hero_ps[1:])}
<div class="sc-v4" style="text-align:left;max-width:680px;margin:8px auto"><h3>Today at a Glance</h3>{''.join(outer(x) for x in hero.xpath('./div[@class="chips"]|./div[@class="ladder"]'))}</div>
{routes_html}
{staff_cards}
{btns}
</div></div>{lundy_strip(t)}</div>'''
T('Title: Today at a Glance', 'the n6 title hero ladder and chips, verbatim')
# ---- middle slides ---------------------------------------------------------
ASDAN = ('id="print-witness"' in D)
PREFIX = {'Arrival Task': 'Arrival Task – ', 'Starter': 'Starter: ', 'I Do': 'I Do: ', 'We Do': 'We Do: ', 'Exit Ticket': 'Exit Ticket — '}
if ASDAN: PREFIX = {'Arrival Task': 'Arrival Task – ', 'Starter': '', 'I Do': 'The Model — ', 'We Do': '', 'Exit Ticket': 'Exit Ticket — '}
def classic_slide(sec, tag, tagcls, label, extra='', sid=''):
    return f'<div class="slide" data-title="{label}"{" id=%s" % json.dumps(sid) if sid else ""}> <span class="slide-tag {tagcls}">{tag}</span> <h2>{PREFIX.get(tag, "")}{esc(h2(sec))}</h2> {extra}{body_of(sec)} {lundy_strip(sec)}</div>'
reveal_btns = ('<div style="text-align:right;margin:2px 0"><button class="ghost small" onclick="wedoReset(this)">🔄 Reset</button> <button class="ghost small" onclick="wedoReveal(this)">👁️ Reveal</button></div>')
arrival = classic_slide(slides['arrival'], 'Arrival Task', 'tag-arrival', 'Arrival', extra=rest_title, sid='arrival-slide')
starter = classic_slide(slides['starter'], 'Starter', 'tag-starter', 'Starter')
if ASDAN:
    st_ = slides['starter']
    starter = f'<div class="slide" data-title="Starter"> <span class="slide-tag tag-starter">Starter</span> <h2>Today at a Glance</h2> <div class="li-box"><strong>Key Question:</strong> {esc(h2(st_))}</div> {body_of(st_)} {lundy_strip(st_)}</div>'
    T('Starter: Today at a Glance', 'the ASDAN house starter heading; the deck\'s own starter question becomes the Key Question line, verbatim')
ido = classic_slide(slides['ido'], 'I Do', 'tag-ido', 'I Do 1')
wedo = classic_slide(slides['wedo'], 'We Do', 'tag-wedo', 'We Do 1', extra=reveal_btns if slides['wedo'].xpath('.//div[contains(@class,"evidence-gate")]') else '')
ido2 = classic_slide(slides['ido2'], 'I Do', 'tag-ido', 'I Do 2') if 'ido2' in slides else ''
if ASDAN and 'ido2' in slides:
    s2 = slides['ido2']
    ido2 = f'<div class="slide" data-title="I Do 2"> <span class="slide-tag tag-ido">I Do</span> <h2>Proving It — {esc(h2(s2))}</h2> {body_of(s2)} {lundy_strip(s2)}</div>'
wedo2 = classic_slide(slides['wedo2'], 'We Do', 'tag-wedo', 'We Do 2', extra=reveal_btns if slides['wedo2'].xpath('.//div[contains(@class,"evidence-gate")]') else '') if 'wedo2' in slides else ''
# Independent: timer with the n6 timing, WAGOLL from the deck's own finished example, Pens-down partner check
ind = slides['independent']; mins = int(ind.get('data-min') or 15)
ex = [b for b in ind.xpath('./div[@class="box"]') if 'finished' in txt(b).lower() or 'here is' in txt(b).lower()]
wagoll = f'<div class="ido-box"><h3 style="margin-top:0;color:var(--ido-border)">WAGOLL — what a good one looks like</h3>{inner(ex[0])}</div>' if ex else ''
if ex: T('Independent: WAGOLL', 'the deck\'s own "Here is a finished one" box, moved under a WAGOLL heading; no words changed')
timer = f'<div class="timer-widget"><div class="timer-display" id="timerDisplay">{mins:02d}:00</div><div class="timer-bar-bg"><div class="timer-bar-fill" id="timerBar" style="width:100%"></div></div><div class="timer-btns"><button class="timer-btn" onclick="startTimer()">▶ Start</button><button class="timer-btn" onclick="pauseTimer()">⏸ Pause</button><button class="timer-btn" onclick="resetTimer()">↺ Reset</button></div></div>'
pens = '<div class="task-box" style="border-color:var(--sc-border)"><h3 style="margin-top:0">⏸ Pens down — quick partner check!</h3><p>Half way through: stop, swap with a partner, and check one thing on the list above together. Then carry on.</p></div>'
T('Independent: Pens-down partner check', 'the classic mid-point check, worded from the deck\'s own "Check yourself" list; adult wording, not the learner\'s voice')
independent = f'<div class="slide" data-title="Independent"> <span class="slide-tag tag-independent">Independent Work</span> <h2>Independent Work — {esc(h2(ind))}</h2> {timer} {"".join(render_block(c) for c in kids(ind) if c is not (ex[0] if ex else None))} {pens} {wagoll} {lundy_strip(ind)}</div>'
# Lundy Loop slide: the four boxes carry the deck's own loop lines (word-bridge + strip sentence), verbatim
strip = ind.xpath('./div[contains(concat(" ",normalize-space(@class)," ")," lundy ")]')[0]
wbs = strip.xpath('.//div[@class="word-bridge"]') or main.xpath('.//div[@class="word-bridge"][.//b[text()="Space"]]')
wb_html = inner(wbs[0]) if wbs else ''
found = dict(re.findall(r'<b>(Space|Voice|Audience|Influence)</b>(.*?)(?=<b>|$)', wb_html, re.S))
parts = [(k, found.get(k, '')) for k in ('Space', 'Voice', 'Audience', 'Influence')]
strip_p = txt(strip.xpath('./p')[0]); strip_sent = {m.group(1): m.group(0).strip() for m in re.finditer(r'(SPACE|VOICE|AUDIENCE|INFLUENCE)[^.]*\.', strip_p)}
icons = {'Space': '🚪', 'Voice': '📣', 'Audience': '👥', 'Influence': '⭐'}
boxes = ''.join(f'<div class="lundy-box"><h3>{icons[k]} {k.upper()}</h3>' + (f'<p><b>{k}</b> {esc(H.unescape(re.sub("<[^>]+>", "", v)).strip())}</p>' if v.strip() else '') + f'<p>{esc(strip_sent.get(k.upper(), ""))}</p></div>' for k, v in parts)
exit_sec = slides['exit']
lundy_slide = f'<div class="slide" data-title="Lundy Loop"> <span class="slide-tag tag-lundy">Lundy Loop</span> <h2>Lundy Loop — Your Voice in This Lesson</h2> <div class="li-box"><strong>Why:</strong> {esc(strip_p)}</div> <div class="lundy-grid">{boxes}</div> {lundy_strip(exit_sec)}</div>'
T('Lundy Loop slide', 'the deck\'s own participation strip sentence and word-bridge, one box per word; the heading is the classic house heading')
complete = '<div class="task-box" style="border-color:var(--aspire-border)"><h3 style="margin-top:0;color:var(--aspire-text)">✅ Complete</h3><p>Hand in your record and tick the learner confirmation on your sheet. That is the lesson done.</p></div>'
T('Exit: Complete close marker', 'the classic house sequence ends with a Complete marker; adult wording, not the learner\'s voice')
exit_slide = f'<div class="slide" data-title="Exit" id="exit-slide"> <span class="slide-tag tag-exit">Exit Ticket</span> <h2>Exit Ticket — {esc(h2(exit_sec))}</h2> {body_of(exit_sec)} {complete} {lundy_strip(exit_sec)}</div>'
# ---- print area ------------------------------------------------------------
def lines(n=2): return "<div class='print-line'></div>" * n
def ptxt(el): return esc(txt(el))
pupil_boxes = lambda sec: [b for b in sec.xpath('.//div[contains(concat(" ",normalize-space(@class)," ")," box ")]') if not is_staff(b)]
# Key words: bold terms from I Do slides + word-bridge words; definitions from the sentence that carries them
kw = []
for sec in (slides.get('ido'), slides.get('ido2')):
    if sec is None: continue
    for b in sec.xpath('.//p//b'):
        w = txt(b)
        if 2 <= len(w) <= 24 and w not in [k for k, _ in kw]:
            par = b.getparent(); kw.append((w, txt(par)))
kw = kw[:8]
ko_rows = ''.join(f'<tr><td>{esc(w)}</td><td>{esc(d)}</td></tr>' for w, d in kw)
T('Knowledge Organiser key words', 'the emphasised terms of the I Do slides, each defined by the sentence that carries it, verbatim')
facts = [ptxt(b) for b in pupil_boxes(slides['arrival'])][:6]
T('Key Facts', 'the Arrival slide boxes, verbatim')
ko = f'''<div id="print-ko" class="print-section"><h1 style="text-align:center;font-size:1.6rem">Knowledge Organiser ({lane} W{week}): {esc(title)}</h1> <p style="text-align:center;margin:2px 0 10px"><strong>{esc(subject)} {term} · 2026–27 · Workbook outcome:</strong> {esc(cfg["outcomes"][0])}</p> <table class="ko-table"><tr><th>Key Word</th><th>Definition</th></tr>{ko_rows}</table> <h3>Key Facts</h3><ul>{"".join(f"<li>{f}</li>" for f in facts)}</ul></div>'''
arr = slides['arrival']
arrival_print = f'<div id="print-arrival" class="print-section"><h2>Arrival Task</h2><p><strong>{esc(h2(arr))}</strong></p>' + ''.join(f'<p>{i+1}) {ptxt(b)}</p>{lines(1)}' for i, b in enumerate(pupil_boxes(arr))) + '</div>'
st = slides['starter']
starter_print = f'<div id="print-starter" class="print-section"><h2>{esc(h2(st))}</h2>' + ''.join(f'<p>{ptxt(b)}</p>' for b in pupil_boxes(st)) + lines(2) + '</div>'
wd = slides['wedo']; wd2 = slides.get('wedo2')
wedo_print = f'<div id="print-wedo" class="print-section prevent-break"><h2>We Do 1: {esc(h2(wd))}</h2>' + ''.join(f'<p>{ptxt(b)}</p>' for b in pupil_boxes(wd)) + (f'<h2 style="margin-top:16px">We Do 2: {esc(h2(wd2))}</h2>' + ''.join(f'<p>{ptxt(b)}</p>' for b in pupil_boxes(wd2)) if wd2 is not None else '') + '</div>'
# Scaffolding x3: word bank = key words; sentence frames = the tier's own route sentence(s) from the Independent slide
routes = {('supported' if 'supported' in (r.get('class') or '') else 'standard' if 'standard' in (r.get('class') or '') else 'stretch'): ' '.join(txt(p) for p in r.xpath('./p')) for r in ind.xpath('.//div[@class="routes"]/article')}
bridge_words = [k for k, _ in parts]
scaff = ''
for tier, label in (('supported', 'Supported'), ('standard', 'Standard'), ('stretch', 'Stretch')):
    scaff += f'<div id="print-scaffold-{tier}" class="print-section"><h2>Scaffolding – {label}</h2><div class="scaffold-print-box"><h3>Word Bank</h3><p>{esc(", ".join([w for w, _ in kw] + bridge_words))}</p><h3>Your route</h3><p>{esc(routes.get(tier, ""))}</p><h3>Sentence frames</h3><p>"Who … what they do … so that …" | "… because …"</p></div></div>'
T('Scaffolding ×3', 'word bank = the key words and the four Lundy words; route text = the Independent slide route for that tier, verbatim; the sentence frames are the deck\'s own connectives')
pp = tree.xpath('//section[contains(@class,"print-pack")]')
pp_pages = pp[0].xpath('./section') if pp else []
# Reference zone: the I Do model boxes and the check-yourself list
ref_items = ''.join(f'<p>{ptxt(b)}</p>' for sec in (slides.get('ido'), slides.get('ido2')) if sec is not None for b in pupil_boxes(sec))
checks = ''.join(f'<li>{ptxt(b)}</li>' for b in ind.xpath('.//div[@class="grid"]/div'))
page1 = ''.join(outer(x) for x in (pp_pages[0] if pp_pages else []) if isinstance(x.tag, str) and x.tag not in ('table',) and not is_staff(x) and 'running-head' not in (x.get('class') or ''))
reference = f'<div id="print-reference" class="print-section"><h2>📘 Reference Zone &mdash; keep this beside your work</h2><div class="prevent-break"><h3>The model</h3>{ref_items}<h3>Check yourself</h3><ul>{checks}</ul><h3>From the lesson sheet</h3>{page1}</div></div>'
T('Reference Zone', 'the I Do model boxes and the Independent "Check yourself" list, verbatim')
# Worksheets x3: the n6 print pack's own route lines + the deck's record table, one sheet per tier
table = pp[0].xpath('.//table')[0] if pp and pp[0].xpath('.//table') else None
pr = {('supported' if 'supported' in (r.get('class') or '') else 'standard' if 'standard' in (r.get('class') or '') else 'stretch'): txt(r.xpath('./p')[0]) for r in (pp[0].xpath('.//div[contains(@class,"proute")]') if pp else [])}
confirm = ''.join(outer(x) for x in (pp_pages[1] if len(pp_pages) > 1 else []) if isinstance(x.tag, str) and x.tag in ('h2', 'ol', 'p', 'table') and not is_staff(x))
ws = ''
icons_t = {'supported': '🔢', 'standard': '📐', 'stretch': '🔗'}
for tier, label in (('supported', 'Supported'), ('standard', 'Standard'), ('stretch', 'Stretch')):
    ws += f'<div id="print-worksheet-{tier}" class="print-section"><h2>{icons_t[tier]} Independent Work – {label}</h2><div class="prevent-break"><p><strong>{esc(pr.get(tier, ""))}</strong></p><p>{esc(routes.get(tier, ""))}</p>' + (outer(table) if table is not None else '<table class="ko-table"><tr><th>What I did</th><th>Evidence I kept (photo / note / recording)</th><th>Witness initials</th></tr>' + '<tr><td style="height:40px">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>' * 4 + '</table>') + confirm + '</div></div>'
T('Independent Work ×3 print sheets', 'the n6 print pack\'s route line, record table and learner confirmation for each tier plus that tier\'s Independent route text, verbatim; differentiation is the route text itself')
ex_ps = [p for p in exit_sec.xpath('./p|./div/p') if not is_staff(p)]
exit_print = ''.join(f'<div class="{tier}-content"><h2>Exit Ticket – {label}</h2>' + ''.join(f'<p>{i+1}) {ptxt(p)}</p>{lines(1)}' for i, p in enumerate(ex_ps[:3])) + '</div>' for tier, label in (('supported', 'Supported'), ('standard', 'Standard'), ('stretch', 'Stretch')))
exit_print = f'<div id="print-exit" class="print-section">{exit_print}</div>'
lundy_print = f'<div class="print-section" id="print-lundy"><h2>Lundy Loop &mdash; this lesson</h2><p style="font-size:.95rem;color:#444">{esc(strip_p)}</p><table class="ko-table">' + ''.join(f'<tr><td style="width:22%;vertical-align:top"><strong>{k}</strong></td><td>{esc(H.unescape(re.sub("<[^>]+>", "", v)).strip()) or esc(strip_sent.get(k.upper(), ""))}</td></tr>' for k, v in parts) + '</table></div>'
T('Lundy Loop print section', 'the deck\'s own strip sentence and word-bridge lines, verbatim')
fi = D.find('<div id="print-feedback"'); fj = D.find('<script', fi)
feedback = re.sub(r'<h2 style="text-align:center">.*?</h2>', f'<h2 style="text-align:center">{esc(title)} &mdash; Feedback Sheet</h2>', D[fi:fj], count=1)  # feedback sheet, print-area close, cold-call modal
feedback = re.sub(r'<div class="print-head"[^>]*>.*?</div>', '', feedback, flags=re.S)  # a classic-v2 donor's own running head must not travel either
T('Feedback sheet', 'the classic donor\'s blank feedback template, retitled; no lesson words')
PH = f'<div class="print-head" style="font-size:.8rem;color:#555;border-bottom:1px solid #999;margin-bottom:8px">{esc(family)} · Week {week} · {esc(title)}</div>'
intro = witness = ''
if ASDAN:
    spark = txt(slides['starter'].xpath('./h2')[0]) if slides['starter'].xpath('./h2') else ''
    intro = f'<div id="print-intro" class="print-section"><h2>{esc(title)}</h2><p><strong>Name:</strong> ____________________ &nbsp; <strong>Class:</strong> __________ &nbsp; <strong>Date:</strong> <span id="print-date"></span></p><div class="rev-block"><h3>This week\'s spark</h3><p>{esc(spark)}</p><h3>ASDAN evidence</h3><p>{esc(cfg["outcomes"][0])}</p><p>{esc(" · ".join(cfg["outcomes"][1:]))}</p></div></div>'
    witness = f'<div id="print-witness" class="print-section"><h1 style="text-align:center;font-size:1.5rem;margin-bottom:2px">Assessor Witness Statement</h1><p style="text-align:center;margin:0 0 10px;font-size:.88rem"><strong>{esc(family)} W{week} &#183; {esc(title)}</strong><br>{esc(cfg["cells"][0])} &mdash; {esc(cfg["outcomes"][0])}</p><table style="width:100%;border-collapse:collapse;font-size:.93rem;margin-bottom:10px"><tr><td style="padding:7px 8px;border:1px solid #999;width:34%"><strong>Candidate name</strong></td><td style="padding:7px 8px;border:1px solid #999">&nbsp;</td></tr><tr><td style="padding:7px 8px;border:1px solid #999"><strong>Route taken</strong></td><td style="padding:7px 8px;border:1px solid #999">◆ Supported &nbsp; ▲ Standard &nbsp; ★ Stretch</td></tr><tr><td style="padding:7px 8px;border:1px solid #999"><strong>What I saw the candidate do</strong></td><td style="padding:7px 8px;border:1px solid #999;height:70px">&nbsp;</td></tr><tr><td style="padding:7px 8px;border:1px solid #999"><strong>Evidence kept (photo / note / recording)</strong></td><td style="padding:7px 8px;border:1px solid #999;height:44px">&nbsp;</td></tr><tr><td style="padding:7px 8px;border:1px solid #999"><strong>Assessor signature and date</strong></td><td style="padding:7px 8px;border:1px solid #999;height:44px">&nbsp;</td></tr></table></div>'
    T('Print: intro sheet and Assessor Witness Statement', 'the ASDAN house sheets; the spark is the deck\'s own starter question and the evidence lines are the traced cells\' outcomes verbatim; the witness table is blank furniture')
print_area = f'<div id="print-area">{ko}{intro}{arrival_print}{starter_print}{wedo_print}{scaff}{reference if not ASDAN else ""}{ws}{exit_print}{witness}{lundy_print}{feedback}'
print_area = re.sub(r'(<div (?:id="print-[a-z-]+" class="print-section[^"]*"|class="print-section" id="print-[a-z-]+")[^>]*>)', lambda m: m.group(1) + PH, print_area)
# ---- assemble --------------------------------------------------------------
head = D[:D.find('<body')]
head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)} · {esc(family)}</title>', head, count=1)
n6css = '''
/* n6 participation strip and route furniture, carried so the deck's own markup survives the reshell */
.slide .lundy{border:2px solid #dbe2ea;border-radius:13px;padding:10px 13px;margin:12px 0 0;background:#fff;font-size:.9rem}
.slide .lundy>.lundy-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;text-align:center;font-weight:900;margin:0 0 6px}
.slide .lundy .word-bridge{color:var(--muted);font-size:.85rem}
.slide .lundy p{margin:4px 0}
.ilm svg{width:100%;max-width:520px;height:auto;display:block;margin:0 auto}
.wedo-reveal{margin-top:10px}
.chips{display:flex;gap:7px;flex-wrap:wrap;margin:8px 0;justify-content:center}
.chips span{display:inline-block;border-radius:999px;padding:4px 10px;font-weight:800;background:#FFF4D6;font-size:.85rem}
.ladder{font-weight:700;font-size:.9rem;margin:6px 0}
.routes3{grid-template-columns:repeat(3,1fr)}.arrival-grid.cols1{grid-template-columns:1fr}.arrival-grid.cols2{grid-template-columns:repeat(2,1fr)}.arrival-grid.cols3{grid-template-columns:repeat(3,1fr)}
@media (max-width:720px){.routes3,.arrival-grid.cols2,.arrival-grid.cols3{grid-template-columns:1fr}}
.slide .scaffold-box{margin-top:8px}
</style>'''
head = head.replace('</style>', n6css, 1)
ctrl = D[D.find('<div class="controls">'):D.find('<div id="print-area"')]
scripts = D[D.find('<script', D.find('<div id="print-area"')):]
# A classic-v2 donor carries its own lesson-config; it must not travel. Run 14 found two decks with the donor's config
# (and its cells) ahead of their own, so the coverage reading credited the donor's cells to them.
scripts = re.sub(r'\s*<script[^>]*id="lesson-config"[^>]*>.*?</script>', '', scripts, flags=re.S)
body_end = ctrl + '%%PRINT%%' + scripts
# R4: fix the STATE. printPack = arm + print; on load and on beforeprint, if no tier is armed, arm the default (Standard),
# so a cold Ctrl+P prints the Standard pack instead of a blank page. Screen is untouched: #print-area stays display:none on screen.
m = None if '/* R4 default-Standard */' in body_end else re.search(r'function printPack\(level\)\{(.*?)window\.print\(\)\}', body_end, re.S)  # a donor already carrying R4 keeps it
assert (m is None) or 'window.print()' not in m.group(1), 'donor printPack shape changed'
r4 = m and ("function printArm(level){" + m.group(1) + "}"
      "function printPack(level){printArm(level);window.print()}"
      "(function(){function armed(){return /\\bprint-(supported|standard|stretch)\\b/.test(document.body.className)}"
      "function r4(){if(!armed())printArm('standard')}window.addEventListener('beforeprint',r4);"
      "if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',r4);else r4();})();/* R4 default-Standard */")
body_end = (body_end[:m.start()] + r4 + body_end[m.end():]) if m else body_end
# swap the donor's sort/match reveal for a generic reveal of the evidence box
body_end = body_end.replace('</body>', '''<script>function wedoReveal(b){var s=b.closest('.slide');s.querySelectorAll('.wedo-reveal').forEach(function(e){e.style.display='block'});}
function wedoReset(b){var s=b.closest('.slide');s.querySelectorAll('.wedo-reveal').forEach(function(e){e.style.display='none'});}</script>
<script id="lesson-config" type="application/json">''' + json.dumps({**cfg, 'chassis': 'classic-v2', 'reshelledFrom': src_path, 'contractScope': 'v2'}, ensure_ascii=False) + '</script>\n</body>', 1)
slides_html = ''.join([title_slide, arrival, starter, ido, wedo, ido2, wedo2, independent, lundy_slide, exit_slide])
out = head + '<body> <main id="lessonDeck" class="deck"><div class="slide-container">' + slides_html + '</div></main>' + body_end.replace('%%PRINT%%', print_area, 1)
out = '\n'.join(l.rstrip() for l in out.split('\n'))
assert out.count('id="lesson-config"') == 1, 'exactly one lesson-config must leave the recipe'
assert out.count('class="print-head"') == out.count(f'· Week {week} · {esc(title)}</div>'), 'every print head must be this deck\'s own'  # the donor carries trailing spaces; the shell copy does not
(ROOT/out_path).write_text(out, encoding='utf-8')
if '--json' in sys.argv:
    json.dump({'file': out_path, 'from': src_path, 'donor': donor_path, 'family': family, 'trace': TRACE}, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1, ensure_ascii=False)
print('wrote', out_path, len(out), 'bytes;', len(TRACE), 'authored blocks')
