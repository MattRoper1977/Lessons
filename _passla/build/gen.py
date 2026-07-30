# -*- coding: utf-8 -*-
"""
Pass LA v5 generator.

Carries the GROW ASDAN v5 chassis FAITHFULLY: the <style> block and the engine
<script> functions are lifted VERBATIM from the donor lesson. Only content-bearing
regions (slides, print-area, overlays, the four JS content objects) and the strand
palette are authored fresh, per brief §5.

Read -> transform -> ASSERT post-conditions -> write (brief §6). Never opens a write
handle before the asserts pass.
"""
import os, re, sys, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DONOR = os.path.join(ROOT, "GROW_ASDAN", "PEQ", "PEQ_W1_Knowing_Myself.html")

SLIDE_TITLES = ["Title","Arrival Task","Starter","I Do 1","We Do 1","I Do 2",
                "We Do 2","Independent Work","Lundy Loop","Exit Ticket"]

# ---- banned strings (zero-count gate, brief §6) ----
BANNED = [
    "ASDAN Studio \u00b7 ASDAN Studio",
    "Delivering a Project",
    "ll-g:loop-mark",
]
# L2 registration/banking phrases that must never appear (L2 = stretch language only)
L2_BANNED = [
    "register at level 2","register at l2","level 2 registration","l2 registration",
    "registered for level 2","banked at level 2","banks level 2","level 2 award",
    "level 2 certificate","level 2 extended award",
]
YT_PATTERNS = [r"youtube\.com", r"youtu\.be", r"youtube-nocookie", r'data-yt', r"ytimg"]

# ---------------------------------------------------------------------------
# Chassis extraction (verbatim from donor)
# ---------------------------------------------------------------------------
def load_chassis():
    d = open(DONOR, encoding="utf-8").read()
    css = d[d.index("<style>")+len("<style>"): d.index("</style>")]
    # body-top: from just after <body> to the slide-container
    body_open = d.index("</style></head><body>") + len("</style></head><body>")
    sc = d.index('<div class="slide-container">')
    body_top = d[body_open:sc]
    # body-mid: controls + progress-wrap + progress-label (between slide-container close and overlays)
    controls = d.index('<div class="controls">')
    lc = d.index('<div class="lesson-complete-overlay"')
    body_mid = d[controls:lc]
    # scripts: from first <script> to end (engine + content + hud)
    scripts = d[d.index("<script>"):]
    return css, body_top, body_mid, scripts

CSS, BODY_TOP, BODY_MID, SCRIPTS = load_chassis()

# ---------------------------------------------------------------------------
# Per-strand palettes (calm, muted; strand identity colour dominant).
# Each: primary strand hue + harmonised in-hue accents + a warm sand for task/independent.
# ---------------------------------------------------------------------------
PALETTES = {
    "PEQ": dict(  # deep orchid
        lo="#8E4F82", lo_bg="#efe3ec", ido="#7C4372", ido_bg="#f0e6ee",
        wedo="#A76A9B", wedo_bg="#f3e9f1", task="#B8935A", task_bg="#f7f0e2",
        sc="#B8935A", sc_bg="#f9f3e6", asp="#8E4F82", asp_bg="#f0e7ee", asp_text="#5c3354",
        ilm="#8E4F82", ilm_bg="#efe3ec", ilm_text="#5c3354",
    ),
    "Careers": dict(  # indigo-violet
        lo="#5A548F", lo_bg="#e6e5f0", ido="#4A4576", ido_bg="#e8e7f1",
        wedo="#7A74AD", wedo_bg="#ebeaf4", task="#B8935A", task_bg="#f7f0e2",
        sc="#B8935A", sc_bg="#f9f3e6", asp="#5A548F", asp_bg="#e7e6f0", asp_text="#3a3660",
        ilm="#5A548F", ilm_bg="#e6e5f0", ilm_text="#3a3660",
    ),
    "Living_Independently": dict(  # moss-olive
        lo="#6F8A46", lo_bg="#e9eede", ido="#5C7439", ido_bg="#eaefe0",
        wedo="#8AA662", wedo_bg="#edf1e4", task="#B8935A", task_bg="#f7f0e2",
        sc="#B8935A", sc_bg="#f9f3e6", asp="#6F8A46", asp_bg="#e9eede", asp_text="#455a2b",
        ilm="#6F8A46", ilm_bg="#e9eede", ilm_text="#455a2b",
    ),
    "Vocational": dict(  # bronze
        lo="#96603C", lo_bg="#f0e6dd", ido="#7E4F30", ido_bg="#f1e8df",
        wedo="#B07E54", wedo_bg="#f4ece2", task="#8AA662", task_bg="#edf1e4",
        sc="#8AA662", sc_bg="#eef2e6", asp="#96603C", asp_bg="#f0e6dd", asp_text="#5f3d25",
        ilm="#96603C", ilm_bg="#f0e6dd", ilm_text="#5f3d25",
    ),
    "Community_Enterprise": dict(  # dusty rose-red
        lo="#A65A5A", lo_bg="#f2e4e4", ido="#8C4747", ido_bg="#f2e7e7",
        wedo="#C07E7E", wedo_bg="#f5eaea", task="#B8935A", task_bg="#f7f0e2",
        sc="#B8935A", sc_bg="#f9f3e6", asp="#A65A5A", asp_bg="#f2e4e4", asp_text="#6d3a3a",
        ilm="#A65A5A", ilm_bg="#f2e4e4", ilm_text="#6d3a3a",
    ),
}

def palette_override(p):
    """A :root + literal-colour override appended after the donor CSS (source order wins)."""
    return f"""
/* ===== Pass LA strand palette override ===== */
:root{{--lo-bg:{p['lo_bg']};--lo-border:{p['lo']};--lo-text:#0f172a;--ido-bg:{p['ido_bg']};--ido-border:{p['ido']};--wedo-bg:{p['wedo_bg']};--wedo-border:{p['wedo']};--task-bg:{p['task_bg']};--task-border:{p['task']};--btn-bg:{p['lo']};--btn-hover:{p['ido']};--sc-border:{p['sc']};--sc-bg:{p['sc_bg']};--aspire-bg:{p['asp_bg']};--aspire-border:{p['asp']};--aspire-text:{p['asp_text']}}}
.slide{{border-top-color:{p['lo']}}}
h1{{color:{p['lo_text'] if 'lo_text' in p else '#0f172a'}}}
.ilm{{background:{p['ilm_bg']};border-color:{p['ilm']}}}
.ilm-cap{{color:{p['ilm_text']}}}
.award-strip{{background:{p['sc_bg']};border-color:{p['sc']};color:{p['asp_text']}}}
.tag-lesson{{background:{p['lo']}!important;color:#fff!important}}
"""

def title_dots(p):
    cols = [p['lo'], p['ido'], p['wedo'], p['task'], p['lo'], p['ido']]
    pos = [("43%","55%","24px","20px","5s","0.0s"),("20%","20%","19px","17px","6s","0.3s"),
           ("5%","62%","28px","22px","7s","0.6s"),("66%","49%","22px","24px","8s","0.9s"),
           ("15%","56%","19px","24px","9s","1.2s"),("58%","41%","15px","25px","10s","1.5s")]
    out=[]
    for (l,t,w,h,dur,dl),c in zip(pos,cols):
        out.append(f'<span class="title-dot" style="left:{l};top:{t};width:{w};height:{h};background:{c};opacity:.2;animation-duration:{dur};animation-delay:{dl}"></span>')
    return "".join(out)

# constant "Made by Matt" mark (verbatim from donor)
MATT_SVG = ('<svg width="64" height="64" viewBox="0 0 100 100" aria-label="Made by Matt">'
    '<circle cx="50" cy="50" r="47" fill="none" stroke="#1e3a8a" stroke-width="3.4"/>'
    '<g transform="translate(0 2)"><path d="M28 71 L28 37 L50 59 L72 37 L72 71" fill="none" '
    'stroke="#1e3a8a" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M50 22.5 L51.48 28.52 L57.5 30 L51.48 31.48 L50 37.5 L48.52 31.48 L42.5 30 L48.52 28.52 Z" '
    'fill="#F2A24A"/></g></svg>')

# constant witness panel body on I Do 2 (verbatim from donor)
WITNESS_PANEL = ('<div class="wit-panel" style="margin-top:14px;border:2px solid var(--lo-border);'
 'border-left:8px solid var(--lo-border);border-radius:12px;background:var(--lo-bg);padding:14px 16px">'
 '<p style="margin:0 0 6px;font-size:.72rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--aspire-text)">For the moderator, not just the folder</p>'
 '<p style="margin:0 0 8px"><strong>A tick says it happened. A witness statement says what <em>you</em> did.</strong> '
 'Before the photo is filed, the adult writes one sentence naming the thing they actually saw you do &#8212; and rings whether you did it '
 '<strong>Supported</strong>, <strong>Standard</strong> or <strong>Stretch</strong>.</p>'
 '<p style="margin:0;font-size:.94rem">That ring is the part that counts. It is the difference between &#8220;the class did this&#8221; and '
 '&#8220;this candidate did it, at this level, with this much help.&#8221; The witness sheet prints with every pack.</p></div>')

def E(s):
    """HTML-escape text content (not markup we intend)."""
    return html.escape(str(s), quote=False)

# ---------------------------------------------------------------------------
# Slide builders
# ---------------------------------------------------------------------------
def build_title(L, p):
    dots = title_dots(p)
    succ = "".join(f"<li>{E(x)}</li>" for x in L['success'])
    return (
    f'<div class="slide active" data-title="Title" data-timer="1" data-no-autostart="true">'
    f'<div class="title-dots" aria-hidden="true">{dots}</div>'
    f'<div style="text-align:center;margin-top:8px">{MATT_SVG}</div>'
    f'<div class="title-stage" style="text-align:center;margin-top:0"><div class="animate-enter">'
    f'<span class="slide-tag tag-lesson">{E(L["tag_lesson"])}</span>'
    f'<h1>{E(L["title_short"])}</h1>'
    f'<p style="font-size:1.05rem;color:var(--muted);margin:-6px 0 4px">{E(L["subtitle"])}</p>'
    f'<div><span class="sow-strip">{E(L["sow_strip"])}</span>'
    f'<span class="award-strip">\U0001f3c5 Banks: {E(L["banks"])}</span></div>'
    f'<div class="li-box" style="margin:8px auto;max-width:660px;text-align:left"><strong>Spark:</strong> {E(L["spark"])}</div>'
    f'<div class="sc-v4"><h3 style="color:var(--sc-border)">Success looks like</h3><ul>{succ}</ul></div>'
    f'<div class="asp-v4"><strong>Aspire</strong> \u00b7 {E(L["aspire"])}</div>'
    f'<div class="scaffold-box" style="display:inline-block;margin-top:6px;text-align:left"><h3 style="margin-top:0">Teacher Print Tools \u2014 Week {L["week"]}</h3>'
    f'<div style="display:flex;gap:12px;flex-wrap:wrap">'
    f'<button onclick="printPack(\'supported\')" style="background:#22c55e;color:#fff;border:none;border-radius:8px;padding:8px 15px;font-weight:800;cursor:pointer">\U0001f5a8 Supported pack</button>'
    f'<button onclick="printPack(\'standard\')" style="background:#f97316;color:#fff;border:none;border-radius:8px;padding:8px 15px;font-weight:800;cursor:pointer">\U0001f5a8 Standard pack</button>'
    f'<button onclick="printPack(\'stretch\')" style="background:#1e3a8a;color:#fff;border:none;border-radius:8px;padding:8px 15px;font-weight:800;cursor:pointer">\U0001f5a8 Stretch pack</button>'
    f'</div></div></div></div></div>')

def _tier_boxes(items, delayed=True):
    out=[]
    for i,(h3,pp,ans) in enumerate(items):
        dl = "" if i==0 else f" anim-delay-{i}"
        out.append(f'<div class="task-box animate-enter{dl}"><h3>{E(h3)}</h3><p>{E(pp)}</p><p class="answer">{E(ans)}</p></div>')
    return "".join(out)

def build_arrival(L):
    a=L['arrival']
    return (
    '<div class="slide" data-title="Arrival Task" data-timer="4" id="arrival-slide">'
    '<span class="slide-tag tag-arrival">Retrieval Quiz</span>'
    '<h2>Arrival Task \u2013 What Do You Already Know?</h2>'
    '<button class="ghost small" style="position:absolute;top:18px;right:20px;z-index:200" onclick="document.getElementById(\'arrival-slide\').classList.toggle(\'show-ans\')">\U0001f441\ufe0f Reveal Answers</button>'
    '<div class="level-toggle"><button onclick="switchLevel(\'arrival\',\'supported\')" style="background:#22c55e">\U0001f91d With support</button><button onclick="switchLevel(\'arrival\',\'standard\')" style="background:#f97316">\U0001f464 On your own</button><button onclick="switchLevel(\'arrival\',\'stretch\')" style="background:#1e3a8a">\U0001f680 Take it further</button></div>'
    f'<div id="arrival-supported" class="arrival-grid">{_tier_boxes(a["supported"])}</div>'
    f'<div id="arrival-standard" class="arrival-grid" style="display:none">{_tier_boxes(a["standard"])}</div>'
    f'<div id="arrival-stretch" class="arrival-grid" style="display:none">{_tier_boxes(a["stretch"])}</div>'
    '</div>')

def build_starter(L):
    s=L['starter']
    return (
    '<div class="slide" data-title="Starter" data-timer="4">'
    '<span class="slide-tag tag-starter">Starter</span>'
    '<h2>Today at a Glance</h2>'
    f'<div class="li-box"><strong>Key Question:</strong> {E(s["key_q"])}</div>'
    '<div class="content-grid" style="grid-template-columns:repeat(4,1fr)">'
    f'<div class="ido-box"><h3 style="margin-top:0">\U0001f4a1 Big Idea</h3><p>{E(s["big_idea"])}</p></div>'
    f'<div class="ido-box"><h3 style="margin-top:0">\U0001f3b2 Today We Play</h3><p>{E(s["game"])}</p></div>'
    f'<div class="ido-box"><h3 style="margin-top:0">\U0001f9f1 The Wall Grows</h3><p>{E(s["wall"])}</p></div>'
    f'<div class="ido-box"><h3 style="margin-top:0">\U0001f3c5 It Banks</h3><p>{E(s["banks_short"])}</p></div>'
    '</div>'
    '<p style="text-align:center;color:var(--muted);margin-top:8px">Talk first, then we play \u2014 every voice counts here.</p>'
    '</div>')

def _v5steps(steps):
    inner="".join(f'<div class="v5-step"><h3>{E(h)}</h3><p>{E(t)}</p></div>' for h,t in steps)
    return ('<div class="v5-step-controls"><button onclick="v5RevealNext(this.closest(\'.slide\'))">Reveal next step \u25b8</button>'
            '<span class="v5-step-label">Step 0 of 3</span></div>'
            f'<div class="v5-steps">{inner}</div>')

def build_ido1(L):
    d=L['ido1']
    return (
    '<div class="slide" data-title="I Do 1" data-timer="5">'
    '<span class="slide-tag tag-ido">I Do</span>'
    f'<h2>{E(d["heading"])}</h2>'
    f'<div class="li-box"><strong>Key Idea:</strong> {E(d["key_idea"])}</div>'
    f'<div class="ilm" role="img" aria-label="{E(d["ilm_alt"])}">{d["ilm_svg"]}<p class="ilm-cap">\U0001f440 {E(d["ilm_cap"])}</p></div>'
    f'{_v5steps(d["steps"])}'
    '</div>')

def build_wedo1(L):
    w=L['wedo1']
    pills="".join(f'<div class="pres-card" data-id="t{i}" onclick="presTap(this)">{E(x)}</div>' for i,x in enumerate(w['words']))
    return (
    '<div class="slide" data-title="We Do 1" data-timer="6">'
    '<span class="slide-tag tag-wedo">We Do</span>'
    f'<h2>{E(w["heading"])}</h2>'
    f'<div class="li-box"><strong>How it works:</strong> {E(w["how"])}<span style="float:right;font-weight:900">Found: <span id="pres-num">0</span>/8</span></div>'
    f'<div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0" id="pres-pills">{pills}</div>'
    '<div id="pres-caps" style="max-width:820px;margin:0 auto"></div>'
    '<p id="pres-msg" class="pres-msg" style="text-align:center;font-weight:800;min-height:1.1rem;margin:4px 0"></p>'
    '<div style="text-align:center;margin-top:6px"><button class="ghost small" onclick="presReset()">\U0001f504 Reset</button></div>'
    '</div>')

def build_ido2(L):
    d=L['ido2']
    return (
    '<div class="slide" data-title="I Do 2" data-timer="4">'
    '<span class="slide-tag tag-ido">I Do</span>'
    f'<h2>{E(d["heading"])}</h2>'
    f'<div class="li-box"><strong>Key Idea:</strong> {E(d["key_idea"])}</div>'
    f'{_v5steps(d["steps"])}'
    f'{WITNESS_PANEL}'
    '</div>')

def build_wedo2(L):
    w=L['wedo2']
    pills="".join(f'<div class="match-pill" onclick="selectKW(this,\'m{i}\')">{E(x)}</div>' for i,x in enumerate(w['pills']))
    targets="".join(f'<div class="match-target" data-correct="m{ci}" onclick="pickTarget(this)">{E(txt)}</div>' for txt,ci in w['targets'])
    tags="".join(f'<span class="wagoll-tag" data-trigger="{E(trig)}">{E(lab)}</span>' for trig,lab in w['wagoll_tags'])
    return (
    '<div class="slide" data-title="We Do 2" data-timer="6" id="wedo2">'
    '<span class="slide-tag tag-wedo">We Do</span>'
    f'<h2>{E(w["heading"])}</h2>'
    '<div class="li-box"><strong>Step 1:</strong> Tap a card, then its partner. <strong>Step 2:</strong> Watch the WAGOLL write itself. <span style="float:right;font-weight:900">Score: <span id="match-score">0</span>/6</span></div>'
    '<div style="text-align:right;margin:2px 0"><button class="ghost small" onclick="resetMatch()">\U0001f504 Reset</button> <button class="ghost small" onclick="revealMatch()">\U0001f441\ufe0f Reveal</button></div>'
    f'<div style="text-align:center;margin-bottom:8px" id="kw-pills">{pills}</div>'
    f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">{targets}</div>'
    '<p id="match-fb" style="text-align:center;font-weight:800;min-height:1.2rem;margin:6px 0"></p>'
    '<div style="text-align:center"><button class="ghost small" onclick="startWagoll()">\u270d\ufe0f Show me a WAGOLL</button> <button class="ghost small" onclick="skipWagoll()">\u23e9 Skip to full text</button></div>'
    f'<div id="wagoll-panel" class="scaffold-box" style="margin-top:8px"><div id="wagoll-tags">{tags}</div><p id="wagoll-text"></p></div>'
    '</div>')

_TIER_SUP = "\U0001f91d With support"
_TIER_STD = "\U0001f464 On your own"
_TIER_STR = "\U0001f680 Take it further"

def build_independent(L):
    ind=L['independent']
    def box(colour, head, task, steps):
        return (f'<div class="task-box"><h3 style="margin-top:0;color:{colour}">{head}</h3>'
                f'<p><strong>Task:</strong> {E(task)}</p><p><strong>Steps:</strong> {E(steps)}</p></div>')
    return (
    '<div class="slide" data-title="Independent Work" data-timer="15">'
    '<span class="slide-tag tag-independent">Independent Work</span>'
    '<h2>Independent Work \u2014 Studio Time</h2>'
    f'<div class="li-box"><strong>Instructions:</strong> Work at your level. Evidence goes in your ASDAN portfolio \u2014 Documentarian photo + annotation + witness tick \u2014 {E(L["banks"])}.</div>'
    '<div class="timer-widget"><div class="timer-display" id="timerDisplay">15:00</div><div class="timer-bar-bg"><div class="timer-bar-fill" id="timerBar" style="width:100%"></div></div><div class="timer-btns"><button class="timer-btn" onclick="startTimer()">\u25b6 Start</button><button class="timer-btn" onclick="pauseTimer()">\u23f8 Pause</button><button class="timer-btn" onclick="resetTimer()">\u21ba Reset</button></div></div>'
    '<div class="content-grid" style="height:auto;margin-top:8px;grid-template-columns:repeat(3,1fr)">'
    f'{box("#22c55e",_TIER_SUP,ind["supported"][0],ind["supported"][1])}'
    f'{box("#f97316",_TIER_STD,ind["standard"][0],ind["standard"][1])}'
    f'{box("#1e3a8a",_TIER_STR,ind["stretch"][0],ind["stretch"][1])}'
    '</div></div>')

def build_lundy(L, p):
    ld=L['lundy']
    return (
    '<div class="slide" data-title="Lundy Loop" data-timer="4">'
    '<span class="slide-tag tag-lundy">Lundy Loop</span>'
    '<h2>Lundy Loop \u2014 Your Voice on the Wall</h2>'
    f'<div class="li-box"><strong>Why:</strong> {E(ld["why"])}</div>'
    '<div class="lundy-grid">'
    f'<div class="lundy-box" style="border-color:{p["lo"]};background:{p["lo"]}14"><h3 style="color:{p["lo"]}">\U0001f6aa SPACE</h3><p>{E(ld["space"])}</p></div>'
    f'<div class="lundy-box" style="border-color:{p["ido"]};background:{p["ido"]}14"><h3 style="color:{p["ido"]}">\U0001f4e3 VOICE</h3><p>{E(ld["voice"])}</p></div>'
    f'<div class="lundy-box" style="border-color:{p["wedo"]};background:{p["wedo"]}14"><h3 style="color:{p["wedo"]}">\U0001f465 AUDIENCE</h3><p>{E(ld["audience"])}</p></div>'
    f'<div class="lundy-box" style="border-color:{p["task"]};background:{p["task"]}14"><h3 style="color:{p["task"]}">\u2b50 INFLUENCE</h3><p>{E(ld["influence"])}</p></div>'
    '</div></div>')

def build_exit(L):
    e=L['exit']
    def boxes(items):
        return "".join(f'<div class="task-box"><h3>{i+1}.</h3><p>{E(pp)}</p><p class="answer">{E(ans)}</p></div>' for i,(pp,ans) in enumerate(items))
    return (
    '<div class="slide" data-title="Exit Ticket" data-timer="4" id="exit-slide">'
    '<span class="slide-tag tag-exit">Exit Ticket</span>'
    '<h2>Exit Ticket</h2>'
    '<div class="li-box"><strong>Instructions:</strong> Answer independently. Own words \u2014 no wall-peeking.</div>'
    '<div class="level-toggle"><button onclick="switchLevel(\'exit\',\'supported\')" style="background:#22c55e">\U0001f91d With support</button><button onclick="switchLevel(\'exit\',\'standard\')" style="background:#f97316">\U0001f464 On your own</button><button onclick="switchLevel(\'exit\',\'stretch\')" style="background:#1e3a8a">\U0001f680 Take it further</button><button class="ghost" onclick="document.getElementById(\'exit-slide\').classList.toggle(\'show-ans\')">\U0001f441\ufe0f Answers</button></div>'
    f'<div id="exit-supported" class="arrival-grid">{boxes(e["supported"])}</div>'
    f'<div id="exit-standard" class="arrival-grid" style="display:none">{boxes(e["standard"])}</div>'
    f'<div id="exit-stretch" class="arrival-grid" style="display:none">{boxes(e["stretch"])}</div>'
    '</div>')

def build_overlays(L):
    c=L['complete']
    summ="".join(f'<span><strong>\u2713</strong> {E(x)}</span>' for x in c['summary'])
    lc=(f'<div class="lesson-complete-overlay" id="lc-overlay" onclick="if(event.target.id===\'lc-overlay\')hideLessonComplete()">'
    f'<div class="lesson-complete-modal"><div class="lc-stars"><span>\U0001f3c5</span><span>\U0001f4f8</span><span>\u270d\ufe0f</span></div>'
    f'<h2>{E(c["h2"])}</h2><p>{E(c["p"])}</p><div class="lc-summary">{summ}'
    f'<span style="margin-top:8px;font-style:italic;color:var(--ido-border)">Next lesson: {E(c["next"])}</span></div>'
    f'<button onclick="hideLessonComplete()">Onwards! \U0001f680</button></div></div>')
    mp=(f'<div class="midpoint-overlay" id="mp-overlay"><div class="midpoint-modal"><span class="mp-tag">\u23f8 MID-POINT PEER CHECK</span>'
    f'<h2>Pens down \u2014 quick partner check!</h2><div class="mp-prompt">{L["midpoint"]}</div>'
    f'<p class="mp-sub">2 minutes max. Then I\u2019ll resume the timer.</p>'
    f'<button onclick="resumeFromMidpoint()">\u25b6 Resume Independent Work</button></div></div>')
    return lc+mp

# ---------------------------------------------------------------------------
# Print area (15 .print-section, derived from the same content -> stays in agreement)
# ---------------------------------------------------------------------------
PL = '<div class="print-line"></div>'

def build_print(L):
    ko=L['ko']
    rows="".join(f'<tr><td>{E(w)}</td><td>{E(d)}</td></tr>' for w,d in ko['rows'])
    facts="".join(f'<li>{E(x)}</li>' for x in ko['facts'])
    a=L['arrival']; e=L['exit']; ind=L['independent']; wit=L['witness']
    def qlines(items):  # items of (prompt, ...) -> numbered prompts + print lines
        return "".join(f'<p>{i+1}) {E(x[0] if isinstance(x,tuple) else x)}</p>{PL}' for i,x in enumerate(items))
    arrival_sup="".join(f'<p>{i+1}) {E(b[0])} {E(b[1])}</p>{PL}' for i,b in enumerate(a['supported']))
    arrival_std="".join(f'<p>{i+1}) {E(b[1])}</p>{PL}' for i,b in enumerate(a['standard']))
    arrival_str="".join(f'<p>{i+1}) {E(b[1])}</p>{PL}' for i,b in enumerate(a['stretch']))
    exit_sup="".join(f'<p>{i+1}) {E(b[0])}</p>{PL}' for i,b in enumerate(e['supported']))
    exit_std="".join(f'<p>{i+1}) {E(b[0])}</p>{PL}' for i,b in enumerate(e['standard']))
    exit_str="".join(f'<p>{i+1}) {E(b[0])}</p>{PL}' for i,b in enumerate(e['stretch']))
    words=", ".join(L['wedo1']['words'])
    match_words=" \u00b7 ".join(L['wedo2']['pills'])
    match_defs=" \u00b7 ".join(E(t) for t,_ in L['wedo2']['targets'])
    wb=" &middot; ".join(L['ko']['wordbank'])
    starters="".join(f'<p>{E(s)}</p>' for s in L['scaffold']['starters'])
    return (
    '<div id="print-area">'
    # KO
    f'<div id="print-ko" class="print-section"><h1 style="text-align:center;font-size:1.55rem">{E(ko["title"])}</h1>'
    f'<p style="text-align:center;margin:2px 0 8px"><strong>{E(ko["subtitle"])}</strong></p>'
    f'<table class="ko-table"><tr><th>Key Word</th><th>Definition</th></tr>{rows}</table>'
    f'<h2 style="margin-top:12px">Key Facts</h2><ul>{facts}</ul></div>'
    # intro
    f'<div id="print-intro" class="print-section"><h2>{E(L["title_short"])}</h2>'
    f'<p><strong>Name:</strong> ____________________ &nbsp; <strong>Class:</strong> __________ &nbsp; <strong>Date:</strong> <span id="print-date"></span></p>'
    f'<div class="rev-block"><h3>This week\u2019s spark</h3><p>{E(L["spark"])}</p>'
    f'<h3>ASDAN evidence</h3><p>Documentarian photo + annotation + witness tick \u2014 {E(L["banks"])}.</p></div></div>'
    # arrival
    f'<div id="print-arrival" class="print-section"><h2>Arrival Task</h2>'
    f'<div class="supported-content">{arrival_sup}</div>'
    f'<div class="standard-content">{arrival_std}</div>'
    f'<div class="stretch-content">{arrival_str}</div></div>'
    # starter
    f'<div id="print-starter" class="print-section"><h2>Today at a Glance</h2>'
    f'<p><strong>Key Question:</strong> {E(L["starter"]["key_q"])}</p>{PL}{PL}</div>'
    # wedo
    f'<div id="print-wedo" class="print-section prevent-break"><h2>We Do 1: {E(L["wedo1"]["heading"])}</h2><p>{E(words)}</p>'
    f'<h2 style="margin-top:14px">We Do 2: {E(L["wedo2"]["heading"])}</h2><p>Draw lines to match:</p>'
    f'<p>{E(match_words)}</p><p>{match_defs}</p></div>'
    # scaffold supported (Access & sensory notes)
    f'<div id="print-scaffold-supported" class="print-section"><h2>Scaffolding \u2013 Supported</h2>'
    '<div style="border:1px solid #999;border-left:6px solid var(--lo-border);background:var(--lo-bg);border-radius:8px;padding:10px 12px;margin:8px 0 12px;font-size:.9rem">'
    '<strong>Access &amp; sensory notes (staff)</strong><br>'
    f'&#183; <strong>The supported task today is:</strong> {E(ind["supported"][0])}<br>'
    '&#183; <strong>Fine motor:</strong> offer the chunky-grip pen, and accept a card sort or a spoken answer scribed by an adult &#8212; the judgement is the evidence, not the handwriting.<br>'
    '&#183; <strong>Sensory:</strong> offer the write-it-first option before any share-aloud; nobody is put on the spot cold.<br>'
    '&#183; <strong>Cognitive load:</strong> a completed small piece beats a half-done large one at moderation. Cut the target, never the thinking.<br>'
    '&#183; <strong>Ring the level honestly</strong> on the witness sheet. Supported with the work finished is a stronger portfolio entry than Standard with it abandoned.'
    '</div>'
    f'<div class="scaffold-print-box"><h3>Sentence starters</h3>{starters}'
    f'<h3>Word bank</h3><p>{wb}</p></div></div>'
    # scaffold standard
    f'<div id="print-scaffold-standard" class="print-section"><h2>Scaffolding \u2013 Standard</h2>'
    f'<div class="scaffold-print-box"><h3>Frame</h3><p>{E(L["scaffold"]["frame"])}</p></div></div>'
    # scaffold stretch
    f'<div id="print-scaffold-stretch" class="print-section"><h2>Scaffolding \u2013 Stretch</h2>'
    f'<div class="scaffold-print-box"><h3>Stretch prompts</h3><p>{E(L["scaffold"]["stretch"])}</p></div></div>'
    # worksheets
    f'<div id="print-worksheet-supported" class="print-section"><h2>Independent Work \u2013 Supported</h2>'
    f'<div class="prevent-break"><p><strong>Task:</strong> {E(ind["supported"][0])}</p><p>Work here (an adult can scribe):</p>{PL}{PL}{PL}</div></div>'
    f'<div id="print-worksheet-standard" class="print-section"><h2>Independent Work \u2013 Standard</h2>'
    f'<div class="prevent-break"><p><strong>Task:</strong> {E(ind["standard"][0])}</p>{PL}{PL}{PL}{PL}'
    '<p><strong>Evidence check:</strong> photo &#9744; &nbsp; annotation &#9744; &nbsp; witness &#9744;</p></div></div>'
    f'<div id="print-worksheet-stretch" class="print-section"><h2>Independent Work \u2013 Stretch</h2>'
    f'<div class="prevent-break"><p><strong>Task:</strong> {E(ind["stretch"][0])}</p>'
    f'<p><strong>Stretch (L2 standard):</strong> {E(L["aspire"])}</p>{PL}{PL}{PL}{PL}</div></div>'
    # exit
    f'<div id="print-exit" class="print-section">'
    f'<div class="supported-content"><h2>Exit Ticket \u2013 Supported</h2>{exit_sup}</div>'
    f'<div class="standard-content"><h2>Exit Ticket \u2013 Standard</h2>{exit_std}</div>'
    f'<div class="stretch-content"><h2>Exit Ticket \u2013 Stretch</h2>{exit_str}</div></div>'
    # witness (§1-5); ring boxes worded from THIS lesson's Independent tiers
    f'<div id="print-witness" class="print-section">'
    '<h1 style="text-align:center;font-size:1.5rem;margin-bottom:2px">Assessor Witness Statement</h1>'
    f'<p style="text-align:center;margin:0 0 10px;font-size:.88rem"><strong>{E(wit["header"])}</strong><br>{E(ko["subtitle"])}</p>'
    '<table style="width:100%;border-collapse:collapse;font-size:.93rem;margin-bottom:10px">'
    '<tr><td style="padding:7px 8px;border:1px solid #999;width:34%"><strong>Candidate name</strong></td><td style="padding:7px 8px;border:1px solid #999">&nbsp;</td></tr>'
    '<tr><td style="padding:7px 8px;border:1px solid #999"><strong>Date of activity</strong></td><td style="padding:7px 8px;border:1px solid #999">&nbsp;</td></tr>'
    f'<tr><td style="padding:7px 8px;border:1px solid #999"><strong>Activity witnessed</strong></td><td style="padding:7px 8px;border:1px solid #999">{E(L["title_short"])}</td></tr></table>'
    '<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">1 &#183; What I actually saw this candidate do</p>'
    '<p style="margin:0 0 6px;font-size:.84rem;font-style:italic">Name the observable action, not the worksheet. Write what a stranger would have seen from the doorway.</p>'
    '<div style="border:1px solid #999;height:26px;margin-bottom:5px"></div><div style="border:1px solid #999;height:26px;margin-bottom:5px"></div><div style="border:1px solid #999;height:26px;margin-bottom:5px"></div>'
    '<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">2 &#183; Level the candidate worked at &#8212; ring ONE</p>'
    '<table style="width:100%;border-collapse:collapse;font-size:.88rem"><tr>'
    f'<td style="padding:9px;border:2px solid #333;width:33.3%;text-align:center"><strong>SUPPORTED</strong><br><span style="font-size:.82rem">{E(ind["supported"][0])}</span></td>'
    f'<td style="padding:9px;border:2px solid #333;width:33.3%;text-align:center"><strong>STANDARD</strong><br><span style="font-size:.82rem">{E(ind["standard"][0])}</span></td>'
    f'<td style="padding:9px;border:2px solid #333;width:33.3%;text-align:center"><strong>STRETCH</strong><br><span style="font-size:.82rem">{E(ind["stretch"][0])}</span></td>'
    '</tr></table>'
    '<p style="margin:6px 0 0;font-size:.82rem">Prompts given (if any): <span style="border-bottom:1px solid #999;display:inline-block;width:60%">&nbsp;</span></p>'
    '<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">3 &#183; Evidence attached</p>'
    '<p style="margin:0;font-size:.9rem">&#9744; Dated photograph &nbsp;&nbsp; &#9744; Candidate&#8217;s written annotation &nbsp;&nbsp; &#9744; Completed sheet &nbsp;&nbsp; &#9744; Other: <span style="border-bottom:1px solid #999;display:inline-block;width:26%">&nbsp;</span></p>'
    '<p style="margin:14px 0 4px;font-weight:800;font-size:.95rem">4 &#183; Assessor declaration</p>'
    '<p style="margin:0 0 8px;font-size:.88rem">I confirm the work described above was produced by the named candidate, and that the level ringed reflects the support actually given on the day.</p>'
    '<table style="width:100%;border-collapse:collapse;font-size:.9rem">'
    '<tr><td style="padding:10px 8px;border:1px solid #999;width:50%">Assessor name (print)<br><br></td><td style="padding:10px 8px;border:1px solid #999">Role<br><br></td></tr>'
    '<tr><td style="padding:10px 8px;border:1px solid #999">Signature<br><br></td><td style="padding:10px 8px;border:1px solid #999">Date<br><br></td></tr></table>'
    '<p style="margin:14px 0 4px;font-weight:800;font-size:.95rem">5 &#183; Learner confirmation</p>'
    '<p style="margin:0 0 8px;font-size:.88rem">I confirm this is my own work.</p>'
    '<table style="width:100%;border-collapse:collapse;font-size:.9rem">'
    '<tr><td style="padding:10px 8px;border:1px solid #999;width:50%">Learner name (print)<br><br></td><td style="padding:10px 8px;border:1px solid #999">Signature<br><br></td></tr>'
    '<tr><td style="padding:10px 8px;border:1px solid #999">Date<br><br></td><td style="padding:10px 8px;border:1px solid #999">&nbsp;</td></tr></table>'
    '<p style="margin:8px 0 0;font-size:.78rem;text-align:center">One statement per candidate per session. File it with the photo, not instead of it.</p>'
    '</div>'
    # lundy
    '<div class="print-section" id="print-lundy"><h2>Lundy Loop &mdash; this lesson</h2>'
    '<p style="font-size:.95rem;color:#444">Space &rarr; Voice &rarr; Audience &rarr; Influence. The adult&rsquo;s first job is Space: regulate before you educate.</p>'
    '<table class="ko-table">'
    f'<tr><td style="width:22%;vertical-align:top"><strong>Space</strong></td><td>{E(L["lundy"]["space"])}</td></tr>'
    f'<tr><td style="width:22%;vertical-align:top"><strong>Voice</strong></td><td>{E(L["lundy"]["voice"])}</td></tr>'
    f'<tr><td style="width:22%;vertical-align:top"><strong>Audience</strong></td><td>{E(L["lundy"]["audience"])}</td></tr>'
    f'<tr><td style="width:22%;vertical-align:top"><strong>Influence</strong></td><td>{E(L["lundy"]["influence"])}</td></tr></table>'
    '<p style="font-size:.95rem;margin:.5rem 0 0"><strong>Closing the loop:</strong> this one ends on paper &mdash; your own hand, or your words scribed by an adult. Pass is always allowed.</p>'
    f'<p style="font-size:.9rem;color:#444;margin:.4rem 0 .2rem">What I said, and what it changed:</p>{PL}{PL}</div>'
    # feedback
    f'<div id="print-feedback" class="print-section"><h2 style="text-align:center">{E(L["title_short"])} \u2014 Feedback Sheet</h2>'
    '<p style="font-size:.95rem;color:#444">Keep with your ASDAN portfolio.</p>'
    '<table class="ko-table"><tr><td style="width:50%"><strong>Pupil name:</strong></td><td><strong>Date:</strong></td></tr>'
    f'<tr><td colspan="2"><strong>WWW (What Went Well):</strong>{PL}{PL}</td></tr>'
    f'<tr><td colspan="2"><strong>EBI (Even Better If):</strong>{PL}{PL}</td></tr>'
    '<tr><td><strong>Level worked at:</strong> Supported / Standard / Stretch</td><td><strong>ASDAN evidence filed:</strong> Yes / Not yet</td></tr>'
    f'<tr><td colspan="2"><strong>Pupil response \u2014 my next step:</strong>{PL}</td></tr></table></div>'
    '</div>')

# ---------------------------------------------------------------------------
# JS content blocks
# ---------------------------------------------------------------------------
def js_escape(s):
    return str(s).replace("\\","\\\\").replace("'","\\'").replace("\n"," ")

def content_scripts(L):
    scripts = SCRIPTS
    # _ccQuestions (multi-line object) -> span replace
    ccq_lines=[]
    for t in SLIDE_TITLES:
        F,M,H = L['cc'][t]
        ccq_lines.append(f'"{t}":{{F:"{js_escape(F)}",M:"{js_escape(M)}",H:"{js_escape(H)}"}}')
    ccq = "const _ccQuestions = {\n" + ",\n".join(ccq_lines) + "\n};"
    i = scripts.index("const _ccQuestions = {")
    j = scripts.index("\n};", i) + len("\n};")
    scripts = scripts[:i] + ccq + scripts[j:]
    # _taBriefs (single line) -> regex line replace
    ta = "const _taBriefs={" + ", ".join(f'"{t}": "{js_escape(L["ta"][t])}"' for t in SLIDE_TITLES) + "};"
    scripts = re.sub(r"const _taBriefs=\{.*", lambda m: ta, scripts, count=1)
    # _pres (single line) -> 8 defs
    pres = "const _pres={" + ",".join(f"t{i}:{{text:'{js_escape(d)}'}}" for i,d in enumerate(L['wedo1']['defs'])) + "};"
    scripts = re.sub(r"const _pres=\{.*?\};", lambda m: pres, scripts, count=1, flags=re.S)
    # _wagollText (single line)
    wg = "const _wagollText='" + js_escape(L['wedo2']['wagoll']) + "';"
    scripts = re.sub(r"const _wagollText=.*", lambda m: wg, scripts, count=1)
    return scripts

# ---------------------------------------------------------------------------
# Assemble + assert + write
# ---------------------------------------------------------------------------
def render(L):
    p = PALETTES[L['strand_key']]
    slides = (build_title(L,p)+build_arrival(L)+build_starter(L)+build_ido1(L)+build_wedo1(L)
              +build_ido2(L)+build_wedo2(L)+build_independent(L)+build_lundy(L,p)+build_exit(L))
    head = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<title>{E(L["title_full"])}</title>\n<style>{CSS}{palette_override(p)}</style></head><body>\n')
    body = (BODY_TOP + '<div class="slide-container">' + slides + '</div>'
            + BODY_MID + build_overlays(L) + build_print(L) + '\n' + content_scripts(L))
    return head + body

def assert_lesson(h, L):
    def need(cond,msg):
        if not cond: raise AssertionError(f"[{L['filename']}] {msg}")
    need(h.count('data-title="')>=10, "fewer than 10 slides")
    need(h.count('class="slide"')+h.count('class="slide active"')==10, "slide count != 10")
    _ps = h.count('class="print-section')
    need(_ps==15, "print-section count "+str(_ps)+" != 15")
    need('id="print-witness"' in h, "no print-witness")
    for s in ["4 &#183; Assessor declaration","5 &#183; Learner confirmation"]:
        need(s in h, f"witness missing '{s}'")
    # §5 confined to #print-area, no on-screen copy
    need(h.count("Learner confirmation")==1, "learner confirmation appears more than once (on-screen leak)")
    for b in BANNED:
        need(b not in h, f"BANNED string present: {b}")
    low=h.lower()
    for b in L2_BANNED:
        need(b not in low, f"L2 registration phrase present: {b}")
    for pat in YT_PATTERNS:
        need(re.search(pat, h, re.I) is None, f"YouTube marker present: {pat}")
    need("\U0001f3ac" not in h, "clapper emoji present (use eyes not clapper)")
    # _ccQuestions keys == slide titles
    for t in SLIDE_TITLES:
        need(f'"{t}":{{F:' in h, f"_ccQuestions missing key {t}")
    # XP totals: pres-cards (8) + match-pills (6)
    need(h.count('class="pres-card"')==8, "pres-card count != 8")
    need(h.count('class="match-pill"')==6, "match-pill count != 6")
    need(h.count('class="match-target"')==6, "match-target count != 6")
    # illuminator + reduced motion present
    need('class="ilm"' in h, "no illuminator")
    need("prefers-reduced-motion" in h, "no reduced-motion rule")
    # tag_lesson must not double 'ASDAN Studio'
    need("ASDAN Studio \u00b7 ASDAN Studio" not in h, "doubled ASDAN Studio label")
    return True

def write_lesson(L, outdir):
    h = render(L)
    assert_lesson(h, L)              # ASSERT before opening a write handle (brief §6)
    path = os.path.join(outdir, L['filename'])
    with open(path, "w", encoding="utf-8") as f:
        f.write(h)
    return path, len(h)

if __name__ == "__main__":
    print("gen.py loaded OK; chassis sizes:",
          "css", len(CSS), "body_top", len(BODY_TOP), "body_mid", len(BODY_MID), "scripts", len(SCRIPTS))
