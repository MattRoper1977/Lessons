#!/usr/bin/env python3
"""Science v5 generator — matches the deployed chassis exactly."""
import re, json, pathlib

REPO = pathlib.Path("/home/claude/repo")
DONOR = REPO / "BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html"
_src = DONOR.read_text(encoding="utf-8")

_HEAD_END = _src.index("</head>")
_BODY_OPEN_END = _src.index(">", _src.index("<body")) + 1
_SC_START = _src.index('<div class="slide-container">')
_PRINT_START = _src.index('<div id="print-area">')
_BODY_END = _src.index("</body>")

HEAD = _src[:_HEAD_END]
PRE_DECK = _src[_BODY_OPEN_END:_SC_START]
CONTROLS = _src[_src.index('<div class="controls"'):_PRINT_START]
_blocks = list(re.finditer(r"<script[^>]*>.*?</script>", _src, re.S))
SCRIPT0 = _blocks[0].group(0)
SCRIPT1 = _blocks[1].group(0)
SCRIPT3 = _blocks[3].group(0) if len(_blocks) > 3 else ""
TAIL = _src[_BODY_END:]

TIERS = [("supported", "#22c55e", "\u25c6", "Supported"),
         ("standard", "#f97316", "\u25b2", "Standard"),
         ("stretch", "#1e3a8a", "\u2605", "Stretch")]
LUNDY = [("Space", "#4D82A0", "\U0001F6E1"), ("Voice", "#C9803B", "\U0001F5E3"),
         ("Audience", "#5B9E5B", "\U0001F442"), ("Influence", "#D8A63B", "\u2699")]
PL = "<div class='print-line'></div>"


def _dots(c):
    seed = [(54, 21, 27, 21), (15, 64, 24, 23), (23, 26, 19, 15),
            (25, 62, 21, 15), (5, 59, 20, 30), (67, 20, 30, 18)]
    cols = ["#4D82A0", "#C9803B", c, "#D8A63B", "#4D82A0", "#C9803B"]
    out = [f'<span class="title-dot" style="left:{l}%;top:{t}%;width:{w}px;height:{h}px;background:{cols[i]};'
           f'opacity:.2;animation-duration:{5+i}s;animation-delay:{i*0.3:.1f}s"></span>'
           for i, (l, t, w, h) in enumerate(seed)]
    return f'<div class="title-dots" aria-hidden="true">{"".join(out)}</div>'


LOGO = ('<div style="text-align:center;margin-top:8px"><svg width="64" height="64" viewBox="0 0 100 100" '
        'aria-label="Made by Matt"><circle cx="50" cy="50" r="47" fill="none" stroke="#1e3a8a" stroke-width="3.4"/>'
        '<g transform="translate(0 2)"><path d="M28 71 L28 37 L50 59 L72 37 L72 71" fill="none" stroke="#1e3a8a" '
        'stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><path d="M50 22.5 L51.48 28.52 L57.5 30 '
        'L51.48 31.48 L50 37.5 L48.52 31.48 L42.5 30 L48.52 28.52 Z" fill="#F2A24A"/></g></svg></div>')


def s_title(L):
    c = L["colour"]
    sc = "".join(f"<li>{x}</li>" for x in L["sc"])
    btns = "".join(f'<button onclick="printPack(\'{k}\')" style="background:{col};color:#fff;border:none;'
                   f'border-radius:8px;padding:8px 15px;font-weight:800;cursor:pointer">{ic} {lb} pack</button>'
                   for k, col, ic, lb in TIERS)
    return (f'<div class="slide active" data-title="Title" data-timer="1" data-no-autostart="true">{_dots(c)}{LOGO}'
            f'<div class="title-stage" style="text-align:center;margin-top:0"><div class="animate-enter">'
            f'<span class="slide-tag tag-lesson" style="background:{c};color:#fff">{L["tag"]}</span>'
            f'<h1>{L["hero"]}</h1>'
            f'<p style="font-size:1.05rem;color:var(--muted);margin:-6px 0 4px">{L["sub"]}</p>'
            f'<div><span class="sow-strip">{L["sowline"]}</span><span class="award-strip">{L["accreditation"]}</span></div>'
            f'<div class="li-box" style="margin:8px auto;max-width:660px;text-align:left">'
            f'<strong>\U0001F3AF Learning Objective:</strong> {L["lo"]}</div>'
            f'<div class="sc-v4"><h3 style="color:var(--sc-border)">\u2705 Success Criteria</h3><ul>{sc}</ul></div>'
            f'<div class="asp-v4"><strong>\u2b50 Aspire:</strong> {L["aspire"]}</div>'
            f'<div class="scaffold-box" style="display:inline-block;margin-top:6px;text-align:left">'
            f'<h3 style="margin-top:0">\U0001F5A8 Teacher print tools</h3>'
            f'<div style="display:flex;gap:12px;flex-wrap:wrap">{btns}</div></div></div></div></div>')


def s_arrival(L):
    a = L["arrival"]
    out = ""
    for n, (k, col, ic, lb) in enumerate(TIERS):
        style = "" if n == 0 else ' style="display:none"'
        cells = "".join(
            f'<div class="task-box animate-enter{f" anim-delay-{i}" if i else ""}"><h3>{i+1}.</h3><p>{q}</p>'
            f'<p class="answer">{ans}</p></div>' for i, (q, ans) in enumerate(a[k]))
        out += f'<div id="arrival-{k}" class="arrival-grid"{style}>{cells}</div>'
    tg = "".join(f'<button onclick="switchLevel(\'arrival\',\'{k}\')" style="background:{col}">{ic} {lb}</button>'
                 for k, col, ic, lb in TIERS)
    return (f'<div class="slide" data-title="Arrival Task" data-timer="4" id="arrival-slide">'
            f'<span class="slide-tag tag-arrival">\U0001F6AA Arrival \u00b7 start this as you come in</span>'
            f'<h2>{a["heading"]}</h2>'
            f'<button class="ghost small" style="position:absolute;top:18px;right:20px;z-index:200" '
            f'onclick="document.getElementById(\'arrival-slide\').classList.toggle(\'show-ans\')">\U0001F441 Answers (staff)</button>'
            f'<div class="level-toggle">{tg}</div>{out}</div>')


def s_starter(L):
    s = L["starter"]
    cards = "".join(f'<div class="product-card"><div class="icon" aria-hidden="true">{c["icon"]}</div>'
                    f'<h4>{c["t"]}</h4><p>{c["b"]}</p><span class="country-badge">{c["badge"]}</span></div>'
                    for c in s["cards"])
    return (f'<div class="slide" data-title="Starter" data-timer="4">'
            f'<span class="slide-tag tag-starter">\U0001F525 Starter</span><h2>{s["heading"]}</h2>'
            f'<div class="li-box"><strong>Talk first:</strong> {s["prompt"]}</div>'
            f'<div class="product-grid">{cards}</div>'
            f'<p style="text-align:center;color:var(--muted);margin-top:8px">{s["hint"]}</p></div>')


def s_ido1(L):
    d = L["ido1"]
    defs = "".join(f"<li><strong>{t}</strong> \u2014 {v}</li>" for t, v in L["vocab"][:4])
    return (f'<div class="slide" data-title="I Do 1" data-timer="5">'
            f'<span class="slide-tag tag-ido">\U0001F469\u200D\U0001F3EB I Do \u00b7 watch me think</span>'
            f'<h2>{d["heading"]}</h2>'
            f'<div class="li-box"><strong>\U0001F9E0 Watch me think:</strong> {d["think"]}</div>'
            f'<div class="ilm" role="img" aria-label="{d["ilm"]["alt"]}">{d["ilm"]["svg"]}'
            f'<p class="ilm-cap">{d["ilm"]["cap"]}</p></div>'
            f'<div class="scaffold-box" style="margin-top:10px"><h3 style="margin-top:0">\U0001F4D6 Key Definitions</h3>'
            f'<ul>{defs}</ul></div>'
            f'<div class="li-box" style="margin-top:10px"><strong>\u274c Common mistake:</strong> {d["miscWrong"]}<br>'
            f'<strong>\u2705 Actually:</strong> {d["miscRight"]}</div></div>')


def s_wedo1(L):
    d = L["wedo1"]
    cards = "".join(f'<div class="pres-card" data-id="t{i}" onclick="presTap(this)">{c["label"]}</div>'
                    for i, c in enumerate(d["cards"]))
    return (f'<div class="slide" data-title="We Do 1" data-timer="6">'
            f'<span class="slide-tag tag-wedo">\U0001F91D We Do \u00b7 together</span><h2>{d["heading"]}</h2>'
            f'<div class="li-box"><strong>Together:</strong> {d["intro"]}'
            f'<span style="float:right;font-weight:900">Found <span id="pres-num">0</span>/8</span></div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0" id="pres-pills">{cards}</div>'
            f'<div id="pres-caps" style="max-width:820px;margin:0 auto"></div>'
            f'<p id="pres-msg" class="pres-msg" style="text-align:center;font-weight:800;min-height:1.1rem;margin:4px 0"></p>'
            f'<div style="text-align:center;margin-top:6px"><button class="ghost small" onclick="presReset()">\u21ba Reset</button></div></div>')


def s_ido2(L):
    d = L["ido2"]
    c = L["colour"]
    steps = "".join(f'<div class="v5-step"><h3>{s["t"]}</h3><p>{s["b"]}</p></div>' for s in d["steps"])
    obs = " ".join(f"<strong>{o}</strong>" for o in d["observables"])
    return (f'<div class="slide" data-title="I Do 2" data-timer="4">'
            f'<span class="slide-tag tag-ido">\U0001F469\u200D\U0001F3EB I Do 2 \u00b7 the evidence loop</span>'
            f'<h2>{d["heading"]}</h2>'
            f'<div class="li-box"><strong>\U0001F9E0 Watch me think:</strong> {d["think"]}</div>'
            f'<div class="v5-step-controls"><button onclick="v5RevealNext(this.closest(\'.slide\'))">\u25b6 Reveal next</button>'
            f'<span class="v5-step-label"></span></div><div class="v5-steps">{steps}</div>'
            f'<div class="wit-panel" style="margin-top:14px;border:2px solid {c};border-left:8px solid {c};'
            f'border-radius:12px;background:{c}14;padding:14px 16px">'
            f'<p style="margin:0 0 6px;font-size:.72rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase">'
            f'Assessor witness \u00b7 what the adult is watching for</p>'
            f'<p style="margin:0 0 8px">{obs}</p>'
            f'<p style="margin:0;font-size:.94rem">{d["witnote"]}</p></div></div>')


def s_wedo2(L):
    d = L["wedo2"]
    pills = "".join(f'<div class="match-pill" onclick="selectKW(this,\'m{i}\')">{p[0]}</div>'
                    for i, p in enumerate(d["pairs"]))
    tgts = "".join(f'<div class="match-target" data-correct="m{i}" onclick="pickTarget(this)">{d["pairs"][i][1]}</div>'
                   for i in d["order"])
    tags = "".join(f'<span class="wagoll-tag" data-trigger="{t}">{t}</span>' for t in d["wagollTags"])
    return (f'<div class="slide" data-title="We Do 2" data-timer="6" id="wedo2">'
            f'<span class="slide-tag tag-wedo">\U0001F91D We Do 2 \u00b7 match, then write</span><h2>{d["heading"]}</h2>'
            f'<div class="li-box"><strong>Sort, don\u2019t guess.</strong> {d["intro"]} {d.get("warn","")}'
            f'<span style="float:right;font-weight:900">Matched <span id="match-score">0</span>/6</span></div>'
            f'<div style="text-align:right;margin:2px 0"><button class="ghost small" onclick="resetMatch()">\u21ba Reset</button> '
            f'<button class="ghost small" onclick="revealMatch()">\u2705 Check</button></div>'
            f'<div style="text-align:center;margin-bottom:8px" id="kw-pills">{pills}</div>'
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">{tgts}</div>'
            f'<p id="match-fb" style="text-align:center;font-weight:800;min-height:1.2rem;margin:6px 0"></p>'
            f'<div style="text-align:center"><button class="ghost small" onclick="startWagoll()">\u270d\ufe0f Build the WAGOLL</button> '
            f'<button class="ghost small" onclick="skipWagoll()">\u23ed Show all</button></div>'
            f'<div id="wagoll-panel" class="scaffold-box" style="margin-top:8px"><div id="wagoll-tags">{tags}</div>'
            f'<p id="wagoll-text"></p></div></div>')


def s_indep(L):
    d = L["independent"]
    boxes = "".join(f'<div class="task-box"><h3 style="margin-top:0;color:{col}">{ic} {lb}</h3>'
                    f'<p><strong>Task:</strong> {d[k]["task"]}</p><p><strong>Show me:</strong> {d[k]["show"]}</p></div>'
                    for k, col, ic, lb in TIERS)
    return (f'<div class="slide" data-title="Independent Work" data-timer="15">'
            f'<span class="slide-tag tag-independent">\u270f\ufe0f Independent Work</span><h2>{d["heading"]}</h2>'
            f'<div class="li-box"><strong>Your turn:</strong> {d["intro"]}</div>'
            f'<div class="timer-widget"><div class="timer-display" id="timerDisplay">15:00</div>'
            f'<div class="timer-bar-bg"><div class="timer-bar-fill" id="timerBar" style="width:100%"></div></div>'
            f'<div class="timer-btns"><button class="timer-btn" onclick="startTimer()">\u25b6 Start</button>'
            f'<button class="timer-btn" onclick="pauseTimer()">\u23f8 Pause</button>'
            f'<button class="timer-btn" onclick="resetTimer()">\u21ba Reset</button></div></div>'
            f'<div class="content-grid" style="height:auto;margin-top:8px;grid-template-columns:repeat(3,1fr)">{boxes}</div></div>')


def s_lundy(L):
    d = L["lundy"]
    boxes = "".join(f'<div class="lundy-box" style="border-color:{c};background:{c}14">'
                    f'<h3 style="color:{c}">{ic} {z}</h3><p>{d[z.lower()]}</p></div>' for z, c, ic in LUNDY)
    return (f'<div class="slide" data-title="Lundy Loop" data-timer="4">'
            f'<span class="slide-tag tag-lundy">\U0001F501 Lundy Loop</span><h2>{d["heading"]}</h2>'
            f'<div class="li-box"><strong>This is where what you say changes something.</strong> {d["intro"]}</div>'
            f'<div class="lundy-grid">{boxes}</div></div>')


def s_exit(L):
    d = L["exit"]
    out = ""
    for n, (k, col, ic, lb) in enumerate(TIERS):
        style = "" if n == 0 else ' style="display:none"'
        qs = "".join(f'<div class="task-box"><h3>{i+1}.</h3><p>{q}</p><p class="answer">{a}</p></div>'
                     for i, (q, a) in enumerate(d[k]))
        out += f'<div id="exit-{k}" class="arrival-grid"{style}>{qs}</div>'
    tg = "".join(f'<button onclick="switchLevel(\'exit\',\'{k}\')" style="background:{col}">{ic} {lb}</button>'
                 for k, col, ic, lb in TIERS)
    return (f'<div class="slide" data-title="Exit Ticket" data-timer="4" id="exit-slide">'
            f'<span class="slide-tag tag-exit">\U0001F3AB Exit Ticket</span><h2>{d["heading"]}</h2>'
            f'<div class="li-box"><strong>Before you go:</strong> {d["intro"]}</div>'
            f'<div class="level-toggle">{tg}<button class="ghost" '
            f'onclick="document.getElementById(\'exit-slide\').classList.toggle(\'show-ans\')">\U0001F441 Answers (staff)</button></div>{out}</div>')


def print_pack(L):
    vt = "".join(f"<tr><td>{t}</td><td>{d}</td></tr>" for t, d in L["vocab"])
    sc = "".join(f"<li>{s}</li>" for s in L["sc"])
    ring = ('<!-- ll-g:loop-mark v1 --><strong>How I answered it &mdash; ring one:</strong>'
            '<span class="lm-opts"><span class="lm-opt">\u25c6 on my own</span>'
            '<span class="lm-opt">\u25b2 with a prompt</span>'
            '<span class="lm-opt">\u2605 with an adult</span></span>'
            '<span class="lm-note">All three are real science. Ringing one records how today went, nothing more.</span>')
    ko = (f'<div id="print-ko" class="print-section">'
          f'<h1 style="text-align:center;font-size:1.55rem">Knowledge Organiser \u2014 {L["hero"]}</h1>'
          f'<p style="text-align:center;margin:2px 0 8px"><strong>{L["koline"]}</strong></p>'
          f'<table class="ko-table"><tr><th>Key word</th><th>What it means</th></tr>{vt}</table>'
          f'<h2 style="margin-top:12px">Key idea</h2><p>{L["keyidea"]}</p>'
          f'<h2 style="margin-top:12px">Success criteria</h2><ul>{sc}</ul>'
          f'<div class="rev-block">{ring}</div></div>')
    intro = (f'<div id="print-intro" class="print-section"><h2>{L["hero"]}</h2>'
             f'<p><strong>Name:</strong> ____________________ <strong>Tier ringed by adult:</strong> '
             f'\u25c6 Supported \u25b2 Standard \u2605 Stretch <strong>Date:</strong> <span id="print-date"></span></p>'
             f'<div class="rev-block"><h3>Learning objective</h3><p>{L["lo"]}</p>'
             f'<h3>Remember from last week</h3><p>{L["recall"]}</p></div></div>')
    a = L["arrival"]
    arr = '<div id="print-arrival" class="print-section"><h2>Arrival</h2>'
    for k, _, _, _ in TIERS:
        arr += f'<div class="{k}-content">' + "".join(f"<p>{i+1}. {q}</p>{PL}" for i, (q, _) in enumerate(a[k])) + "</div>"
    arr += "</div>"
    st = (f'<div id="print-starter" class="print-section"><h2>Starter</h2>'
          f'<p><strong>{L["starter"]["heading"]}</strong> {L["starter"]["prompt"]}</p>{PL}{PL}</div>')
    wd = (f'<div id="print-wedo" class="print-section prevent-break"><h2>We Do \u2014 match the pairs</h2>'
          f'<p>{L["wedo2"]["intro"]}</p>'
          + "".join(f'<p>{k} &rarr; ______________________________</p>' for k, _ in L["wedo2"]["pairs"])
          + f'<h2 style="margin-top:14px">WAGOLL</h2><p>{L["wedo2"]["wagollPrint"]}</p></div>')
    scaf = ""
    for k, col, ic, lb in TIERS:
        t = L["independent"][k]
        extra = ""
        if k == "supported":
            extra = (f'<div style="border:1px solid #999;border-left:6px solid {L["colour"]};background:{L["colour"]}14;'
                     f'border-radius:8px;padding:10px 12px;margin:8px 0 12px;font-size:.9rem">'
                     f'<strong>Adult notes \u2014 access &amp; sensory</strong><br>{L["sensory"]}</div>')
        scaf += (f'<div id="print-scaffold-{k}" class="print-section"><h2>Scaffolding \u2014 {ic} {lb}</h2>{extra}'
                 f'<div class="scaffold-print-box"><h3>Sentence stems</h3><p>{t["scaffold"]}</p>'
                 f'<h3>Word bank</h3><p>{t["bank"]}</p></div></div>')
    work = ""
    for k, col, ic, lb in TIERS:
        t = L["independent"][k]
        work += (f'<div id="print-worksheet-{k}" class="print-section"><h2>Independent Work \u2014 {ic} {lb}</h2>'
                 f'<div class="prevent-break"><p><strong>Task:</strong> {t["task"]}</p>'
                 f'<p><strong>Show me:</strong> {t["show"]}</p>' + PL * t.get("lines", 6) + '</div></div>')
    ex = ('<div id="print-exit" class="print-section"><h2>Exit Ticket</h2>'
          + "".join(f"<p>{i+1}. {q}</p>{PL}" for i, (q, _) in enumerate(L["exit"]["standard"])) + "</div>")
    w = L["witness"]
    rows = "".join(f'<tr><td style="padding:7px 8px;border:1px solid #999;width:34%"><strong>{x}</strong></td>'
                   f'<td style="padding:7px 8px;border:1px solid #999">{y}</td></tr>' for x, y in
                   [("Pupil", "____________________"),
                    ("Lesson", f'{L["hero"]} \u2014 {L["pathway"]} Science {L["sowweek"]}'),
                    ("Date", "____________________")])
    tier_cells = "".join(f'<td style="padding:9px;border:2px solid #333;width:33.3%;text-align:center">'
                         f'<strong>{ic} {lb}</strong><br><span style="font-size:.82rem">{w["tiers"][k]}</span></td>'
                         for k, col, ic, lb in TIERS)
    obs = "".join(f'<p style="margin:0 0 5px">\u2610 {o}</p>' for o in w["observables"])
    wit = (f'<div id="print-witness" class="print-section">'
           f'<h1 style="text-align:center;font-size:1.5rem;margin-bottom:2px">Assessor Witness Statement</h1>'
           f'<p style="text-align:center;margin:0 0 10px;font-size:.88rem"><strong>{L["accreditation"]}</strong><br>'
           f'Records what was observed, and at which level of independence.</p>'
           f'<table style="width:100%;border-collapse:collapse;font-size:.93rem;margin-bottom:10px">{rows}</table>'
           f'<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">Observed in this lesson</p>{obs}'
           f'<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">Assessor comment</p>'
           f'<div style="border:1px solid #999;height:26px;margin-bottom:5px"></div>'
           f'<div style="border:1px solid #999;height:26px;margin-bottom:5px"></div>'
           f'<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">Ring the tier the pupil actually worked at</p>'
           f'<table style="width:100%;border-collapse:collapse;font-size:.88rem"><tr>{tier_cells}</tr></table>'
           f'<p style="margin:8px 0 0;font-size:.82rem">Assessor name ______________ Role ____________ '
           f'Signature ______________ Date ________</p></div>')
    lun = ('<div id="print-lundy" class="print-section"><h2>Lundy Loop</h2>'
           + "".join(f'<p><strong>{z}:</strong> {L["lundy"][z.lower()]}</p>' for z, _, _ in LUNDY)
           + f'<p><strong>What I said:</strong></p>{PL}<p><strong>What changed because of it:</strong></p>{PL}</div>')
    fb = (f'<div id="print-feedback" class="print-section"><h2>Feedback</h2>'
          f'<p><strong>What went well:</strong></p>{PL}<p><strong>My next step:</strong></p>{PL}</div>')
    return '<div id="print-area">' + ko + intro + arr + st + wd + scaf + work + ex + wit + lun + fb + '</div>'


def script2(L):
    pres = {f"t{i}": {"text": c["text"]} for i, c in enumerate(L["wedo1"]["cards"])}
    body = ("const _pres=" + json.dumps(pres, ensure_ascii=False) + ";\n"
            "let _presDone=[];function presTap(el){var id=el.getAttribute('data-id');var p=_pres[id];"
            "if(!p||_presDone.indexOf(id)>=0)return;_presDone.push(id);el.classList.add('done');"
            "try{playDing()}catch(e){}try{gainXP()}catch(e){}var c=document.createElement('div');"
            "c.className='pres-cap';c.innerHTML=p.text;document.getElementById('pres-caps').appendChild(c);"
            "document.getElementById('pres-num').textContent=_presDone.length;"
            "if(_presDone.length===8){var m=document.getElementById('pres-msg');"
            "if(m)m.textContent='\\u2705 All found \\u2014 every card talked about.';}}"
            "function presReset(){_presDone=[];document.querySelectorAll('#pres-pills .pres-card')"
            ".forEach(function(c){c.classList.remove('done')});document.getElementById('pres-caps').innerHTML='';"
            "document.getElementById('pres-num').textContent='0';var m=document.getElementById('pres-msg');"
            "if(m)m.textContent='';}window._pres=_pres;window.presTap=presTap;window.presReset=presReset;\n"
            "registerXP(document.querySelectorAll('.match-pill').length);\n"
            "var _pd=document.getElementById('print-date');"
            "if(_pd)_pd.textContent=new Date().toLocaleDateString('en-GB');\n")
    return "<script>\n" + body + "</script>"


def build(L):
    head = HEAD.replace("BUILD ASDAN \u00b7 FoodWise M1 W1 \u00b7 Food Groups", L["doctitle"])
    head = head.replace("#5B9E5B", L["colour"])
    deck = ('<div class="slide-container">' + s_title(L) + s_arrival(L) + s_starter(L) + s_ido1(L) +
            s_wedo1(L) + s_ido2(L) + s_wedo2(L) + s_indep(L) + s_lundy(L) + s_exit(L) + '</div>')
    sc1 = re.sub(r"const _ccQuestions = \{.*?\n\};",
                 "const _ccQuestions = " + json.dumps(L["cc"], ensure_ascii=False) + ";",
                 SCRIPT1, count=1, flags=re.S)
    sc1 = re.sub(r"const _taBriefs=\{.*?\};",
                 "const _taBriefs=" + json.dumps(L["taBriefs"], ensure_ascii=False) + ";",
                 sc1, count=1, flags=re.S)
    return (head + "</head>" + "<body>" + PRE_DECK + deck + CONTROLS + print_pack(L) +
            SCRIPT0 + sc1 + script2(L) + SCRIPT3 + TAIL)
