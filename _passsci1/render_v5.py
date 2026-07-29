#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Science v5 renderer — built on the DEPLOYED single-file chassis
(BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html), measured not assumed.

It consumes the AUTHORED content-spec schema exactly as delivered:
  week slug title sow lo sc[3] ko_vocab[5] ko_facts[4+] misconceptions[3]
  arrival{3 tiers} glance[3] ido1{heading,think,illuminator} wedo1{heading,prompt,items}
  ido2{heading,model,capture} wedo2{heading,pills[6],wagoll} independent{3 tiers}
  lundy{space,voice,audience,influence} exit{3 tiers} exit_key[3] witness[3]
  ta_rule ta_notes[2] coldcall[3] uas

Deviations from the supplied engine.py (all forced by measuring the real donor; each
is a documented finding — engine.py's 'blocks 0 and 1 reusable verbatim' is FALSE):
  D1  block 0 carries `const _wagollText='...'` -> content-bound, injected per lesson.
  D2  block 0 `printPack([...])` array omits glance+lundy -> patched so witness AND
      lundy AND the Today-at-a-Glance sheet print in all three tier packs (MASTER §6).
  D3  We Do 2 is a SORT not a MATCH when categories repeat -> a keyboard-reachable
      sort widget is appended; registerXP still counts `.match-pill` so XP != 0 / no NaN.
  D4  Slide 3 is 'Today at a Glance', not 'Starter' (MASTER §2).
  D5  We Do 1 card count is per-lesson (not hardcoded 8); script2 threshold follows it.
"""
import re
import json
import pathlib
import importlib.util

REPO = pathlib.Path("/workspace/lessons")
DONOR = REPO / "BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html"

# ---------------------------------------------------------------- donor splice
_src = DONOR.read_text(encoding="utf-8")
assert _src.rstrip().endswith("</html>"), "donor does not end </html>"

_HEAD_END = _src.index("</head>")
_BODY_OPEN = _src.index("<body")
_BODY_OPEN_END = _src.index(">", _BODY_OPEN) + 1
_SC_START = _src.index('<div class="slide-container">')
_CTRL_START = _src.index('<div class="controls"')
_PRINT_START = _src.index('<div id="print-area">')
_BODY_END = _src.index("</body>")

HEAD = _src[:_HEAD_END]                       # everything up to (not incl) </head>
PRE_DECK = _src[_BODY_OPEN_END:_SC_START]     # anything between <body> and the deck
CONTROLS = _src[_CTRL_START:_PRINT_START]     # the .controls furniture (NOT verbatim: §2)
# §2 widening: CONTROLS is NOT content-free. The lesson-complete overlay embeds the
# donor's title, subtitle and success criteria. Patched per lesson in build_controls().
assert "Food Groups — banked!" in CONTROLS, "controls overlay title anchor moved"

_blocks = list(re.finditer(r"<script[^>]*>.*?</script>", _src, re.S))
assert len(_blocks) == 4, f"expected 4 script blocks, found {len(_blocks)}"
SCRIPT0 = _blocks[0].group(0)   # base widgets + printPack + _wagollText  (D1,D2)
SCRIPT1 = _blocks[1].group(0)   # XP + _ccQuestions + _taBriefs + pickTarget override
SCRIPT3 = _blocks[3].group(0)   # hud loader (verbatim)
TAIL = _src[_BODY_END:]         # </body></html> (block 3 already precedes </body>)

TIERS = [("supported", "#22c55e", "◆", "Supported"),
         ("standard", "#f97316", "▲", "Standard"),
         ("stretch", "#1e3a8a", "★", "Stretch")]
LUNDY = [("Space", "#4D82A0", "\U0001F6E1"), ("Voice", "#C9803B", "\U0001F5E3"),
         ("Audience", "#5B9E5B", "\U0001F442"), ("Influence", "#D8A63B", "⚙")]
BIN_ICONS = ["●", "■", "▲", "◆", "○", "□"]  # ● ■ ▲ ◆ ○ □
PL = "<div class='print-line'></div>"


# ---------------------------------------------------------------- small helpers
def _attr(s):
    """Escape a string for use inside a double-quoted HTML attribute."""
    return (s.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))


def build_controls(L, M):
    """Patch the lesson-complete overlay so no FoodWise content ships into science (§2)."""
    c = CONTROLS
    c = c.replace("<h2>Food Groups — banked!</h2>", f'<h2>{L["title"]} — banked!</h2>')
    c = c.replace("<p>The Eatwell Guide ✅</p>", f'<p>{M["PATHWAY"]} {M["STRAND"]} · Week {L["week"]} ✅</p>')
    sc_spans = "".join(f"<span><strong>✓</strong> {s}</span>" for s in L["sc"])
    c2 = re.sub(r'<div class="lc-summary">.*?</div>', f'<div class="lc-summary">{sc_spans}</div>',
                c, count=1, flags=re.S)
    assert c2 != c, "lc-summary not replaced"
    # mid-point peer-check overlay also embeds the donor's success criteria
    sc0, sc1 = (L["sc"] + L["sc"])[0], (L["sc"] + L["sc"])[1]
    mp_new = (f'<div class="mp-prompt">📣 Show your partner where you’re up to. Check together '
              f'against today’s success: <strong>{sc0}</strong> and <strong>{sc1}</strong>. '
              f'If something’s missing, help them add it — kindly.</div>')
    c3 = re.sub(r'<div class="mp-prompt">.*?</div>', mp_new, c2, count=1, flags=re.S)
    assert c3 != c2, "mp-prompt not replaced"
    # Assert the DONOR-UNIQUE anchors are gone (not any food word — W6's own title is
    # 'Building a Balanced Plate' and its SC legitimately says 'food groups').
    donor_anchors = ["Food Groups — banked!", "The Eatwell Guide", "name the main food groups",
                     "sort foods into the right groups", "Balanced-Plate Gallery",
                     "Next lesson: A Balanced Plate"]
    left = [a for a in donor_anchors if a in c3]
    assert not left, f"donor residue left in controls: {left}"
    return c3


def load_module(path):
    spec = importlib.util.spec_from_file_location(pathlib.Path(path).stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _bin_label(answer):
    """Bin/category label = the phrase before the first em-dash or middot separator."""
    for sep in (" — ", " · "):
        if sep in answer:
            return answer.split(sep, 1)[0].strip()
    return answer.strip()


def _slug_cat(label):
    return "c_" + re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def classify_wedo2(pills):
    """Return ('sort', bins) if categories repeat, else ('match', None)."""
    cats = [_bin_label(a) for _, a in pills]
    uniq = list(dict.fromkeys(cats))
    if len(uniq) < len(pills):
        return "sort", uniq
    return "match", None


# ---------------------------------------------------------------- slide builders
def s_title(L, M):
    c = M["COLOUR"]
    sc = "".join(f"<li>{x}</li>" for x in L["sc"])
    btns = "".join(
        f'<button onclick="printPack(\'{k}\')" style="background:{col};color:#fff;border:none;'
        f'border-radius:8px;padding:8px 15px;font-weight:800;cursor:pointer">{ic} {lb} pack</button>'
        for k, col, ic, lb in TIERS)
    dots = _src[_src.index('<div class="title-dots"'):_src.index("</div>", _src.index('<div class="title-dots"')) + 6]
    return (
        f'<div class="slide active" data-title="Title" data-timer="1" data-no-autostart="true">{dots}'
        f'<div class="title-stage" style="text-align:center;margin-top:0"><div class="animate-enter">'
        f'<span class="slide-tag tag-lesson" style="background:{c};color:#fff">{M["PATHWAY"]} · {M["STRAND"]} · Week {L["week"]}</span>'
        f'<h1>{L["title"]}</h1>'
        f'<p style="font-size:1.05rem;color:var(--muted);margin:-6px 0 4px">{L["sow"]}</p>'
        f'<div><span class="sow-strip">{M["SPINE"]}</span><span class="award-strip">{M["AWARD"]}</span></div>'
        f'<div class="li-box" style="margin:8px auto;max-width:680px;text-align:left">'
        f'<strong>\U0001F3AF Learning Objective:</strong> {L["lo"]}</div>'
        f'<div class="sc-v4"><h3 style="color:var(--sc-border)">✅ Success Criteria</h3><ul>{sc}</ul></div>'
        f'<div class="asp-v4"><strong>\U0001F517 Assessment link:</strong> {L["uas"]}</div>'
        f'<div class="scaffold-box" style="display:inline-block;margin-top:6px;text-align:left">'
        f'<h3 style="margin-top:0">\U0001F5A8 Teacher print tools</h3>'
        f'<div style="display:flex;gap:12px;flex-wrap:wrap">{btns}</div></div></div></div></div>')


def s_arrival(L):
    a = L["arrival"]
    out = ""
    for n, (k, col, ic, lb) in enumerate(TIERS):
        style = "" if n == 0 else ' style="display:none"'
        out += (f'<div id="arrival-{k}" class="arrival-grid"{style}>'
                f'<div class="task-box animate-enter"><h3>{ic} {lb}</h3><p>{a[k]}</p></div></div>')
    tg = "".join(f'<button onclick="switchLevel(\'arrival\',\'{k}\')" style="background:{col}">{ic} {lb}</button>'
                 for k, col, ic, lb in TIERS)
    return (f'<div class="slide" data-title="Arrival Task" data-timer="4" id="arrival-slide">'
            f'<span class="slide-tag tag-arrival">\U0001F6AA Arrival · start this as you come in</span>'
            f'<h2>Arrival task — pick your tier</h2>'
            f'<div class="level-toggle">{tg}</div>{out}</div>')


def s_glance(L):
    """Slide 3 = Today at a Glance (NOT Starter). glance = 3 short phrases."""
    cards = "".join(
        f'<div class="task-box"><h3 style="margin-top:0">{i+1}.</h3><p>{g}</p></div>'
        for i, g in enumerate(L["glance"]))
    return (f'<div class="slide" data-title="Today at a Glance" data-timer="2">'
            f'<span class="slide-tag tag-starter">\U0001F5FA️ Today at a Glance</span>'
            f'<h2>Three things we do today</h2>'
            f'<div class="content-grid" style="height:auto;grid-template-columns:repeat(3,1fr);gap:14px">{cards}</div></div>')


def s_ido1(L, M, ilm):
    d = L["ido1"]
    defs = "".join(f"<li><strong>{t}</strong> — {v}</li>" for t, v in L["ko_vocab"][:4])
    mw, mr = L["misconceptions"][0]
    return (f'<div class="slide" data-title="I Do 1" data-timer="5">'
            f'<span class="slide-tag tag-ido">\U0001F469‍\U0001F3EB I Do · watch me think</span>'
            f'<h2>{d["heading"]}</h2>'
            f'<div class="li-box"><strong>\U0001F9E0 Watch me think:</strong> {d["think"]}</div>'
            f'<div class="ilm" role="img" aria-label="{_attr(ilm["alt"])}">{ilm["svg"]}'
            f'<p class="ilm-cap">{ilm["cap"]}</p></div>'
            f'<div class="scaffold-box" style="margin-top:10px"><h3 style="margin-top:0">\U0001F4D6 Key definitions</h3>'
            f'<ul>{defs}</ul></div>'
            f'<div class="li-box" style="margin-top:10px"><strong>❌ Common mistake:</strong> {mw}<br>'
            f'<strong>✅ Actually:</strong> {mr}</div></div>')


def s_wedo1(L):
    """Work it out before you tap: N cards, tap to reveal the answer (pres mechanic)."""
    d = L["wedo1"]
    items = d["items"]
    n = len(items)
    cards = "".join(
        f'<div class="pres-card" data-id="t{i}" tabindex="0" role="button" '
        f'onclick="presTap(this)" onkeydown="if(event.key===\'Enter\'||event.key===\' \'){{event.preventDefault();presTap(this)}}">'
        f'{q}</div>' for i, (q, _a) in enumerate(items))
    return (f'<div class="slide" data-title="We Do 1" data-timer="6">'
            f'<span class="slide-tag tag-wedo">\U0001F91D We Do · together</span><h2>{d["heading"]}</h2>'
            f'<div class="li-box"><strong>{d["prompt"]}</strong>'
            f'<span style="float:right;font-weight:900">Found <span id="pres-num">0</span>/{n}</span></div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0" id="pres-pills">{cards}</div>'
            f'<div id="pres-caps" style="max-width:820px;margin:0 auto"></div>'
            f'<p id="pres-msg" class="pres-msg" style="text-align:center;font-weight:800;min-height:1.1rem;margin:4px 0"></p>'
            f'<div style="text-align:center;margin-top:6px"><button class="ghost small" onclick="presReset()">↺ Reset</button></div></div>')


def s_ido2(L, M):
    """Evidence loop: model + the capture instruction + the assessor witness panel."""
    d = L["ido2"]
    c = M["COLOUR"]
    obs = "".join(f'<li>{o}</li>' for o in L["witness"])
    return (f'<div class="slide" data-title="I Do 2" data-timer="4">'
            f'<span class="slide-tag tag-ido">\U0001F469‍\U0001F3EB I Do 2 · the evidence loop</span>'
            f'<h2>{d["heading"]}</h2>'
            f'<div class="li-box"><strong>\U0001F9E0 Watch me think:</strong> {d["model"]}</div>'
            f'<div class="wit-panel" style="margin-top:14px;border:2px solid {c};border-left:8px solid {c};'
            f'border-radius:12px;background:{c}14;padding:14px 16px">'
            f'<p style="margin:0 0 6px;font-size:.72rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase">'
            f'Assessor witness · what the adult is watching for</p>'
            f'<ul style="margin:0 0 8px;padding-left:20px">{obs}</ul>'
            f'<p style="margin:0;font-size:.94rem"><strong>\U0001F4F8 Capture:</strong> {d["capture"]}</p></div></div>')


def s_wedo2(L, M, two_period=False):
    d = L["wedo2"]
    pills = d["pills"]
    mode, bins = classify_wedo2(pills)
    wag = d["wagoll"]
    if mode == "sort":
        n = len(pills)
        item_html = "".join(
            f'<div class="match-pill" tabindex="0" role="button" data-cat="{_slug_cat(_bin_label(a))}" '
            f'onclick="sortSelect(this)" onkeydown="sortKey(event,this)">{q}</div>'
            for q, a in pills)
        bin_html = "".join(
            f'<div class="sort-bin" tabindex="0" role="button" data-cat="{_slug_cat(b)}" '
            f'onclick="sortDrop(this)" onkeydown="sortKey(event,this)">'
            f'<div class="sort-bin-head">{BIN_ICONS[i % len(BIN_ICONS)]} {b}</div>'
            f'<div class="sort-bin-items"></div></div>'
            for i, b in enumerate(bins))
        controls = ('<button class="ghost small" onclick="resetSort()">↺ Reset</button> '
                    '<button class="ghost small" onclick="revealSort()">✅ Check</button>')
        board = (
            f'<div style="text-align:center;margin-bottom:8px" id="kw-pills">{item_html}</div>'
            f'<div class="sort-bins" style="display:grid;grid-template-columns:repeat({len(bins)},1fr);gap:10px">{bin_html}</div>')
        counter = f'Sorted <span id="match-score">0</span>/{n}'
        blurb = "Put each card in the right bin."
    else:
        item_html = "".join(
            f'<div class="match-pill" onclick="selectKW(this,\'m{i}\')">{q}</div>'
            for i, (q, _a) in enumerate(pills))
        tgts = "".join(
            f'<div class="match-target" data-correct="m{i}" onclick="pickTarget(this)">{a}</div>'
            for i, (_q, a) in enumerate(pills))
        controls = ('<button class="ghost small" onclick="resetMatch()">↺ Reset</button> '
                    '<button class="ghost small" onclick="revealMatch()">✅ Check</button>')
        board = (
            f'<div style="text-align:center;margin-bottom:8px" id="kw-pills">{item_html}</div>'
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">{tgts}</div>')
        counter = f'Matched <span id="match-score">0</span>/{len(pills)}'
        blurb = "Match each card to the right answer."
    return (f'<div class="slide" data-title="We Do 2" data-timer="6" id="wedo2">'
            f'<span class="slide-tag tag-wedo">\U0001F91D We Do 2 · sort, then write</span><h2>{d["heading"]}</h2>'
            f'<div class="li-box"><strong>Sort, don’t guess.</strong> {blurb}'
            f'<span style="float:right;font-weight:900">{counter}</span></div>'
            f'<div style="text-align:right;margin:2px 0">{controls}</div>'
            f'{board}'
            f'<p id="match-fb" style="text-align:center;font-weight:800;min-height:1.2rem;margin:6px 0"></p>'
            f'<div style="text-align:center"><button class="ghost small" onclick="startWagoll()">✍️ Build the WAGOLL</button> '
            f'<button class="ghost small" onclick="skipWagoll()">⏭ Show all</button></div>'
            f'<div id="wagoll-panel" class="scaffold-box" style="margin-top:8px"><div id="wagoll-tags"></div>'
            f'<p id="wagoll-text"></p></div>'
            + (f'<div class="period-break" style="margin-top:14px;text-align:center;font-weight:800;'
               f'color:{M["COLOUR"]};border-top:2px dashed {M["COLOUR"]};padding-top:8px">'
               f'⏸ End of Period 1 — Period 2 picks up at Independent Work</div>' if two_period else "")
            + '</div>')


def s_indep(L, M, two_period=False):
    d = L["independent"]
    boxes = "".join(
        f'<div class="task-box"><h3 style="margin-top:0;color:{col}">{ic} {lb}</h3><p>{d[k]}</p></div>'
        for k, col, ic, lb in TIERS)
    p2 = (f'<div class="period-break" style="margin:4px 0 10px;text-align:center;font-weight:800;'
          f'color:{M["COLOUR"]};border-bottom:2px dashed {M["COLOUR"]};padding-bottom:8px">'
          f'▶ Period 2 — extended independent work: this is where the practical, the evidence and the '
          f'loop closure get made</div>' if two_period else "")
    return (f'<div class="slide" data-title="Independent Work" data-timer="15">'
            f'<span class="slide-tag tag-independent">✏️ Independent Work</span><h2>Your turn — pick your tier</h2>'
            f'{p2}'
            f'<div class="li-box"><strong>15 minutes.</strong> Choose the tier your adult rings for you.</div>'
            f'<div class="timer-widget"><div class="timer-display" id="timerDisplay">15:00</div>'
            f'<div class="timer-bar-bg"><div class="timer-bar-fill" id="timerBar" style="width:100%"></div></div>'
            f'<div class="timer-btns"><button class="timer-btn" onclick="startTimer()">▶ Start</button>'
            f'<button class="timer-btn" onclick="pauseTimer()">⏸ Pause</button>'
            f'<button class="timer-btn" onclick="resetTimer()">↺ Reset</button></div></div>'
            f'<div class="content-grid" style="height:auto;margin-top:8px;grid-template-columns:repeat(3,1fr)">{boxes}</div></div>')


def s_lundy(L):
    d = L["lundy"]
    boxes = "".join(
        f'<div class="lundy-box" style="border-color:{c};background:{c}14">'
        f'<h3 style="color:{c}">{ic} {z}</h3><p>{d[z.lower()]}</p></div>' for z, c, ic in LUNDY)
    return (f'<div class="slide" data-title="Lundy Loop" data-timer="4">'
            f'<span class="slide-tag tag-lundy">\U0001F501 Lundy Loop</span><h2>Where what you say changes something</h2>'
            f'<div class="li-box"><strong>This is where your voice changes what happens next.</strong></div>'
            f'<div class="lundy-grid">{boxes}</div></div>')


def s_exit(L):
    """Exit slide. Answers live behind the staff 'Answers (staff)' toggle ONLY (show-ans).
    exit_key[i] pairs with tier i. Print pack carries NO answers (MASTER §6)."""
    d = L["exit"]
    keys = L["exit_key"]
    out = ""
    for n, (k, col, ic, lb) in enumerate(TIERS):
        style = "" if n == 0 else ' style="display:none"'
        out += (f'<div id="exit-{k}" class="arrival-grid"{style}>'
                f'<div class="task-box"><h3>{ic} {lb}</h3><p>{d[k]}</p>'
                f'<p class="answer">{keys[n]}</p></div></div>')
    tg = "".join(f'<button onclick="switchLevel(\'exit\',\'{k}\')" style="background:{col}">{ic} {lb}</button>'
                 for k, col, ic, lb in TIERS)
    return (f'<div class="slide" data-title="Exit Ticket" data-timer="4" id="exit-slide">'
            f'<span class="slide-tag tag-exit">\U0001F3AB Exit Ticket</span><h2>Before you go</h2>'
            f'<div class="level-toggle">{tg}<button class="ghost" '
            f'onclick="document.getElementById(\'exit-slide\').classList.toggle(\'show-ans\')">\U0001F441 Answers (staff)</button></div>{out}</div>')


# ---------------------------------------------------------------- print pack
# The canonical ll-g:loop-mark ring-one strip, byte-identical to the deployed estate
# standard (BUILD_ASDAN/Community_Project/COMM_W6...). Enforced by LL-INST-09
# (loop_mark_print_gate.py): it lives in print-feedback, uses .lm-strip + .lm-g glyph
# spans (glyph-loss safe), and carries the fixed vocabulary the gate asserts. Do NOT
# re-author this text — the sentinel and the gate both depend on it being verbatim.
LOOP_MARK_STRIP = (
    '<!-- ll-g:loop-mark v1 --><strong>How I answered it &mdash; ring one:</strong>'
    '<span class="lm-opts">'
    '<span class="lm-opt"><span class="lm-g">&#128073;</span>pointed</span>'
    '<span class="lm-opt"><span class="lm-g">&#128483;</span>said it</span>'
    '<span class="lm-opt"><span class="lm-g">&#9995;</span>showed</span>'
    '<span class="lm-opt"><span class="lm-g">&#128444;</span>picture</span>'
    '<span class="lm-opt"><span class="lm-g">&#128257;</span>tried again</span>'
    '<span class="lm-opt"><span class="lm-g">&#127916;</span>filmed</span></span>'
    '<span class="lm-note">Nothing yet is a real answer &mdash; leave it blank. Pass is always allowed.</span>'
    '<span class="lm-note">Filmed or photographed: work, not faces, unless consent is filed.</span>'
    '<span class="lm-r"><strong>R</strong> &mdash; adult initials that they received it: ____________</span>')


def print_pack(L, M, two_period=False):
    c = M["COLOUR"]
    period_note = (
        '<div style="border:1px solid #999;border-left:6px solid #333;background:#f4f4f5;'
        'border-radius:8px;padding:8px 12px;margin:8px 0;font-size:.9rem">'
        '<strong>Teacher note — two periods.</strong> This one deck runs across BOTH weekly '
        '40-minute periods. Period 1 ends after We Do 2 (Title → Arrival → Today at a Glance → '
        'I Do 1 → We Do 1 → I Do 2 → We Do 2). Period 2 (Independent Work → Lundy → Exit) is the '
        'extended window where the practical, the witness evidence and the loop closure are made. '
        'This single print pack covers both periods — do not reprint.</div>' if two_period else "")
    # KO
    vt = "".join(f"<tr><td>{t}</td><td>{v}</td></tr>" for t, v in L["ko_vocab"])
    facts = "".join(f"<li>{f}</li>" for f in L["ko_facts"])
    sc = "".join(f"<li>{s}</li>" for s in L["sc"])
    ko = (f'<div id="print-ko" class="print-section">'
          f'<h1 style="text-align:center;font-size:1.55rem">Knowledge Organiser — {L["title"]}</h1>'
          f'<p style="text-align:center;margin:2px 0 8px"><strong>{M["PATHWAY"]} · {M["SPINE"]} · Week {L["week"]}</strong></p>'
          f'<table class="ko-table"><tr><th>Key word</th><th>What it means</th></tr>{vt}</table>'
          f'<h2 style="margin-top:12px">Key facts</h2><ul>{facts}</ul>'
          f'<h2 style="margin-top:12px">Success criteria</h2><ul>{sc}</ul></div>')
    # intro
    intro = (f'<div id="print-intro" class="print-section"><h2>{L["title"]}</h2>'
             f'<p><strong>Name:</strong> ____________________ &nbsp; <strong>Tier ringed by adult:</strong> '
             f'◆ Supported ▲ Standard ★ Stretch &nbsp; <strong>Date:</strong> <span id="print-date"></span></p>'
             f'<div class="rev-block"><h3>Learning objective</h3><p>{L["lo"]}</p>'
             f'<h3>Today at a glance</h3><ul>{"".join(f"<li>{g}</li>" for g in L["glance"])}</ul></div>'
             f'{period_note}</div>')
    # glance sheet (was 'starter' in donor)
    glance = (f'<div id="print-glance" class="print-section"><h2>Today at a Glance</h2>'
              f'<ol>{"".join(f"<li>{g}</li>" for g in L["glance"])}</ol>{PL}{PL}</div>')
    # arrival (all tiers, tier-hidden by body.print-<tier>)
    a = L["arrival"]
    arr = '<div id="print-arrival" class="print-section"><h2>Arrival task</h2>'
    for k, _, _, _ in TIERS:
        arr += f'<div class="{k}-content"><p>{a[k]}</p>{PL}{PL}</div>'
    arr += "</div>"
    # we do (sort/match items -> blank; then WAGOLL model). NO answer key printed.
    mode, bins = classify_wedo2(L["wedo2"]["pills"])
    verb = "Sort each card into the right group" if mode == "sort" else "Match each card"
    wd = (f'<div id="print-wedo" class="print-section prevent-break"><h2>We Do — {verb}</h2>'
          + "".join(f'<p>{q} &rarr; ______________________________</p>' for q, _a in L["wedo2"]["pills"])
          + f'<h2 style="margin-top:14px">WAGOLL</h2><p>{L["wedo2"]["wagoll"]}</p></div>')
    # scaffolding (per tier): sentence stem = ta_rule opener; word bank = ko vocab terms
    bank = ", ".join(t for t, _ in L["ko_vocab"])
    scaf = ""
    for k, col, ic, lb in TIERS:
        extra = ""
        if k == "supported":
            extra = (f'<div style="border:1px solid #999;border-left:6px solid {c};background:{c}14;'
                     f'border-radius:8px;padding:10px 12px;margin:8px 0 12px;font-size:.9rem">'
                     f'<strong>Adult notes — access &amp; sensory</strong><br>{M["SENSORY"]}</div>')
        scaf += (f'<div id="print-scaffold-{k}" class="print-section"><h2>Scaffolding — {ic} {lb}</h2>{extra}'
                 f'<div class="scaffold-print-box"><h3>Sentence stems</h3>'
                 f'<p>{L["ido2"]["model"]}</p>'
                 f'<h3>Word bank</h3><p>{bank}</p></div></div>')
    # worksheets (per tier): the independent task
    work = ""
    for k, col, ic, lb in TIERS:
        work += (f'<div id="print-worksheet-{k}" class="print-section"><h2>Independent Work — {ic} {lb}</h2>'
                 f'<div class="prevent-break"><p><strong>Task:</strong> {L["independent"][k]}</p>'
                 + PL * 6 + '</div></div>')
    # exit (STANDARD questions only, NO answers on any print surface)
    ex = ('<div id="print-exit" class="print-section"><h2>Exit Ticket</h2>'
          f'<p>{L["exit"]["standard"]}</p>{PL}{PL}</div>')
    # witness statement (must print in all three tier packs)
    w = L["witness"]
    rows = "".join(
        f'<tr><td style="padding:7px 8px;border:1px solid #999;width:34%"><strong>{x}</strong></td>'
        f'<td style="padding:7px 8px;border:1px solid #999">{y}</td></tr>' for x, y in
        [("Pupil", "____________________"),
         ("Lesson", f'{L["title"]} — {M["PATHWAY"]} Science · Week {L["week"]}'),
         ("Date", "____________________")])
    tier_cells = "".join(
        f'<td style="padding:9px;border:2px solid #333;width:33.3%;text-align:center">'
        f'<strong>{ic} {lb}</strong></td>' for k, col, ic, lb in TIERS)
    obs = "".join(f'<p style="margin:0 0 5px">☐ {o}</p>' for o in w)
    wit = (f'<div id="print-witness" class="print-section">'
           f'<h1 style="text-align:center;font-size:1.5rem;margin-bottom:2px">Assessor Witness Statement</h1>'
           f'<p style="text-align:center;margin:0 0 10px;font-size:.88rem"><strong>{M["AWARD"]}</strong><br>'
           f'AQA UAS unit code: TBC (Cheryl). Records what was observed, and at which level of independence.</p>'
           f'<table style="width:100%;border-collapse:collapse;font-size:.93rem;margin-bottom:10px">{rows}</table>'
           f'<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">Observed in this lesson</p>{obs}'
           f'<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">Assessor comment</p>'
           f'<div style="border:1px solid #999;height:26px;margin-bottom:5px"></div>'
           f'<div style="border:1px solid #999;height:26px;margin-bottom:5px"></div>'
           f'<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">Ring the tier the pupil actually worked at</p>'
           f'<table style="width:100%;border-collapse:collapse;font-size:.88rem"><tr>{tier_cells}</tr></table>'
           f'<p style="margin:8px 0 0;font-size:.82rem">Assessor name ______________ Role ____________ '
           f'Signature ______________ Date ________</p></div>')
    # lundy
    lun = ('<div id="print-lundy" class="print-section"><h2>Lundy Loop</h2>'
           + "".join(f'<p><strong>{z}:</strong> {L["lundy"][z.lower()]}</p>' for z, _, _ in LUNDY)
           + f'<p><strong>What I said:</strong></p>{PL}<p><strong>What changed because of it:</strong></p>{PL}</div>')
    # feedback — carries the canonical ll-g:loop-mark strip (LL-INST-09 requires it here)
    fb = (f'<div id="print-feedback" class="print-section">'
          f'<h2 style="text-align:center">{L["title"]} — Feedback Sheet</h2>'
          f'<p style="font-size:.95rem;color:#444">Keep with your portfolio.</p>'
          f'<table class="ko-table"><tr><td style="width:50%"><strong>Pupil name:</strong></td><td><strong>Date:</strong></td></tr>'
          f'<tr><td colspan="2"><strong>WWW (What Went Well):</strong>{PL}{PL}</td></tr>'
          f'<tr><td colspan="2"><strong>EBI (Even Better If):</strong>{PL}{PL}</td></tr>'
          f'<tr><td><strong>Level worked at:</strong> Supported / Standard / Stretch</td>'
          f'<td><strong>Evidence filed:</strong> Yes / Not yet</td></tr>'
          f'<tr><td colspan="2"><strong>Pupil response — my next step:</strong> '
          f'<span class="lm-own">Ring this yourself &mdash; an adult may write your words if you ask.</span>{PL}</td></tr>'
          f'<tr><td colspan="2" class="lm-strip">{LOOP_MARK_STRIP}</td></tr></table></div>')
    return ('<div id="print-area">' + ko + intro + glance + arr + wd + scaf + work
            + ex + wit + lun + fb + '</div>')


# ---------------------------------------------------------------- content-bound JS
def _replace_js_object(src, decl, new_json):
    """Replace `const NAME = {...};` (balanced braces) with new JSON. `decl` is the text
    up to and including the `=` (e.g. 'const _ccQuestions ='). Robust to nested braces,
    strings-with-braces are not expected in these two donor objects. Returns (new_src, old)."""
    start = src.index(decl)
    brace = src.index("{", start)
    depth = 0
    i = brace
    while i < len(src):
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    assert depth == 0, f"unbalanced braces for {decl!r}"
    end = src.index(";", i) + 1
    varname = decl.split("=")[0].strip()          # 'const _ccQuestions'
    new_stmt = varname + " = " + new_json + ";"
    return src[:start] + new_stmt + src[end:], src[start:end]


def build_script0(L):
    """Patch printPack section list (D2) and inject per-lesson _wagollText (D1)."""
    s = SCRIPT0
    old_arr = "['ko','intro','arrival','starter','wedo','exit','witness','feedback']"
    new_arr = "['ko','intro','glance','arrival','wedo','exit','witness','lundy','feedback']"
    assert old_arr in s, "printPack section array not found in block 0"
    s = s.replace(old_arr, new_arr)
    wag = L["wedo2"]["wagoll"]
    new_wag = "const _wagollText=" + json.dumps(wag, ensure_ascii=False) + ";"
    s2 = re.sub(r"const _wagollText=(['\"])(?:\\.|(?!\1).)*\1;", new_wag, s, count=1)
    assert s2 != s and "const _wagollText=" in s2, "failed to inject _wagollText"
    return s2


def _cc(L):
    """coldcall = [(slideTitle, question)]; chassis wants {title:{F,M,H}}. Author gave
    one question per key slide -> mirror it across F/M/H (no invented tier variants)."""
    out = {}
    for title, q in L["coldcall"]:
        out[title] = {"F": q, "M": q, "H": q}
    return out


def _ta(L, two_period=False):
    """TA brief per slide title, EACH opening with the lesson's single rule (MASTER §6)."""
    rule = L["ta_rule"]
    p1_end = " BREAK POINT: Period 1 ends after this slide." if two_period else ""
    p2_start = (" This is where Period 2 begins — the extended window where the evidence gets made."
                if two_period else "")
    roles = {
        "Title": "Set the room, name the objective, keep the pace gentle.",
        "Arrival Task": "Round the room, pass allowed — this is the settle.",
        "Today at a Glance": "Three things, read once. No new teaching here.",
        "I Do 1": "Pupils watch the model — you watch the pupils. Note who is ready to go solo.",
        "We Do 1": "Let them answer before the reveal. Wait time is the intervention.",
        "I Do 2": "This is the evidence slide — line up your camera on the working, not faces.",
        "We Do 2": "Deliberate wrong cards are in the set. A wrong sort is data, not a fail." + p1_end,
        "Independent Work": "Rings the tier, then steps back." + p2_start + " " + " ".join(L["ta_notes"]),
        "Lundy Loop": "Capture one real thing a pupil says and what it changes.",
        "Exit Ticket": "Answers are staff-side only. Never show the key to a pupil.",
    }
    return {t: rule + " " + role for t, role in roles.items()}


def build_script1(L, two_period=False):
    """Inject _ccQuestions + _taBriefs (D-content), then append the sort widget (D3)."""
    s = SCRIPT1
    s, _ = _replace_js_object(s, "const _ccQuestions =", json.dumps(_cc(L), ensure_ascii=False))
    s, _ = _replace_js_object(s, "const _taBriefs=", json.dumps(_ta(L, two_period), ensure_ascii=False))
    # append sort widget before the closing </script>
    assert s.rstrip().endswith("</script>")
    s = s[:s.rindex("</script>")] + SORT_WIDGET_JS + "</script>"
    return s


def build_script2(L):
    """_pres captions from We Do 1 items (N cards), registerXP(match-pill), print date."""
    items = L["wedo1"]["items"]
    n = len(items)
    pres = {f"t{i}": {"text": a} for i, (_q, a) in enumerate(items)}
    body = (
        "const _pres=" + json.dumps(pres, ensure_ascii=False) + ";\n"
        "let _presDone=[];function presTap(el){var id=el.getAttribute('data-id');var p=_pres[id];"
        "if(!p||_presDone.indexOf(id)>=0)return;_presDone.push(id);el.classList.add('done');"
        "try{playDing()}catch(e){}try{gainXP()}catch(e){}var c=document.createElement('div');"
        "c.className='pres-cap';c.innerHTML='<strong>'+el.textContent+':</strong> '+p.text;"
        "document.getElementById('pres-caps').appendChild(c);"
        "document.getElementById('pres-num').textContent=_presDone.length;"
        "if(_presDone.length===" + str(n) + "){var m=document.getElementById('pres-msg');"
        "if(m)m.textContent='\\u2705 All found \\u2014 every card talked about.';}}"
        "function presReset(){_presDone=[];document.querySelectorAll('#pres-pills .pres-card')"
        ".forEach(function(c){c.classList.remove('done')});document.getElementById('pres-caps').innerHTML='';"
        "document.getElementById('pres-num').textContent='0';var m=document.getElementById('pres-msg');"
        "if(m)m.textContent='';}window._pres=_pres;window.presTap=presTap;window.presReset=presReset;\n"
        "registerXP(document.querySelectorAll('.match-pill').length);\n"
        "var _pd=document.getElementById('print-date');"
        "if(_pd)_pd.textContent=new Date().toLocaleDateString('en-GB');\n")
    return "<script>\n" + body + "</script>"


# ---- the keyboard-reachable SORT widget (D3). #match-fb gets icon + WORD feedback. ----
SORT_WIDGET_JS = (
    "\n/* SORT variant of We Do 2: n items -> k category bins, keyboard reachable. */\n"
    "var _sortSel=null,_sortScore=0;\n"
    "function _sortFb(msg,col){var fb=document.getElementById('match-fb');if(fb){fb.textContent=msg;fb.style.color=col;}}\n"
    "function sortSelect(el){if(el.classList.contains('placed'))return;_sortSel=el;"
    "document.querySelectorAll('#wedo2 #kw-pills .match-pill').forEach(function(p){p.classList.remove('selected')});"
    "el.classList.add('selected');_sortFb('\\u261D Now tap the bin it belongs in','var(--muted)');}\n"
    "function sortDrop(bin){if(!_sortSel){_sortFb('\\u261D Pick a card first','var(--muted)');return;}"
    "var pill=_sortSel;if(pill.getAttribute('data-cat')===bin.getAttribute('data-cat')){"
    "pill.classList.add('placed');pill.classList.remove('selected');"
    "var chip=document.createElement('span');chip.className='sort-chip';chip.textContent=pill.textContent;"
    "bin.querySelector('.sort-bin-items').appendChild(chip);_sortScore++;"
    "var ms=document.getElementById('match-score');if(ms)ms.textContent=_sortScore;"
    "try{playDing()}catch(e){}try{gainXP()}catch(e){}_sortFb('\\u2705 Correct \\u2014 right bin','var(--success)');"
    "_sortSel=null;}else{bin.classList.add('wrong');setTimeout(function(){bin.classList.remove('wrong')},450);"
    "try{playBuzz()}catch(e){}_sortFb('\\u274C Not that bin \\u2014 try again','var(--error)');}}\n"
    "function sortKey(ev,el){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();"
    "if(el.classList.contains('sort-bin'))sortDrop(el);else sortSelect(el);}}\n"
    "function resetSort(){_sortSel=null;_sortScore=0;var ms=document.getElementById('match-score');if(ms)ms.textContent='0';"
    "document.querySelectorAll('#wedo2 #kw-pills .match-pill').forEach(function(p){p.classList.remove('selected','placed')});"
    "document.querySelectorAll('#wedo2 .sort-bin-items').forEach(function(b){b.innerHTML='';});_sortFb('','');}\n"
    "function revealSort(){document.querySelectorAll('#wedo2 #kw-pills .match-pill').forEach(function(p){"
    "if(p.classList.contains('placed'))return;var cat=p.getAttribute('data-cat');"
    "var bin=document.querySelector('#wedo2 .sort-bin[data-cat=\"'+cat+'\"]');"
    "if(bin){var chip=document.createElement('span');chip.className='sort-chip';chip.textContent=p.textContent;"
    "bin.querySelector('.sort-bin-items').appendChild(chip);}p.classList.add('placed');});"
    "var pills=document.querySelectorAll('#wedo2 #kw-pills .match-pill').length;_sortScore=pills;"
    "var ms=document.getElementById('match-score');if(ms)ms.textContent=pills;"
    "_sortFb('\\u2705 All sorted \\u2014 check the bins','var(--success)');}\n"
    "window.sortSelect=sortSelect;window.sortDrop=sortDrop;window.sortKey=sortKey;"
    "window.resetSort=resetSort;window.revealSort=revealSort;\n")

# CSS for the sort widget + keyboard focus (injected into <head>, reused styled classes).
SORT_WIDGET_CSS = (
    "\n<style id=\"sci-sort-css\">"
    ".sort-bin{border:2px dashed #cbd5e1;border-radius:12px;padding:10px;background:#fff;"
    "min-height:96px;transition:all .15s;cursor:pointer}"
    ".sort-bin:hover{border-color:var(--task-border);background:#fefce8}"
    ".sort-bin.wrong{border:2px solid var(--error);background:rgba(220,38,38,.10);animation:shake .4s}"
    ".sort-bin-head{font-weight:900;font-size:.9rem;margin-bottom:6px;text-align:center;color:#334155}"
    ".sort-bin-items{display:flex;flex-wrap:wrap;gap:5px;justify-content:center}"
    ".sort-chip{background:rgba(34,197,94,.14);border:1.5px solid var(--success);color:#166534;"
    "border-radius:8px;padding:3px 8px;font-weight:800;font-size:.82rem}"
    ".sort-bin:focus-visible,.match-pill:focus-visible{outline:3px solid var(--ido-border);outline-offset:2px}"
    "@media print{.sort-bin,.sort-chip{border-color:#000}}"
    "</style>")


# ---------------------------------------------------------------- top level
def render_lesson(mod, lesson, illuminators):
    M = {k: getattr(mod, k) for k in
         ("STRAND", "PATHWAY", "COLOUR", "SPINE", "AWARD", "THEME", "SLOT_WEEKS", "SENSORY")}
    ilm_fn = illuminators.get(lesson["slug"])
    ilm = ilm_fn() if ilm_fn else dict(
        alt="Illuminator pending.", cap="Illuminator pending.",
        svg='<svg viewBox="0 0 640 200" role="img" xmlns="http://www.w3.org/2000/svg">'
            '<text x="320" y="105" text-anchor="middle" font-size="16" fill="#94a3b8" '
            'font-family="system-ui,sans-serif">illuminator to be authored</text></svg>')

    two_period = M["PATHWAY"] in ("BUILD", "GROW")   # §5: LAUNCH is one lesson per period

    head = HEAD.replace("BUILD ASDAN · FoodWise M1 W1 · Food Groups",
                        f'{M["PATHWAY"]} {M["STRAND"]} W{lesson["week"]} · {lesson["title"]}')
    head = head.replace("#5B9E5B", M["COLOUR"])
    head = head + SORT_WIDGET_CSS

    deck = ('<div class="slide-container">'
            + s_title(lesson, M) + s_arrival(lesson) + s_glance(lesson)
            + s_ido1(lesson, M, ilm) + s_wedo1(lesson) + s_ido2(lesson, M)
            + s_wedo2(lesson, M, two_period) + s_indep(lesson, M, two_period)
            + s_lundy(lesson) + s_exit(lesson)
            + '</div>')

    return (head + "</head>" + "<body>" + PRE_DECK + deck + build_controls(lesson, M)
            + print_pack(lesson, M, two_period)
            + build_script0(lesson) + build_script1(lesson, two_period) + build_script2(lesson)
            + SCRIPT3 + TAIL)


if __name__ == "__main__":
    import sys
    illum = load_module(str(pathlib.Path(__file__).parent / "illuminators.py"))
    modname = sys.argv[1] if len(sys.argv) > 1 else "content_build"
    week = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    mod = load_module(str(pathlib.Path(__file__).parent / "inputs" / (modname + ".py")))
    lesson = next(l for l in mod.LESSONS if l["week"] == week)
    html = render_lesson(mod, lesson, illum.ILLUMINATORS)
    outdir = pathlib.Path(__file__).parent / "out"
    outdir.mkdir(exist_ok=True)
    outp = outdir / (lesson["slug"] + ".html")
    outp.write_text(html, encoding="utf-8")
    print(f"wrote {outp} ({len(html)} bytes, donor {len(_src)} bytes)")
