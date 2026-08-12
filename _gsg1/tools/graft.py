#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSG-1 Phase A graft — applies A1/A2/A4/A5 to the ten LIVE GROW lessons.

Everything below is hand-written into the live chassis idiom. Nothing is
copy-pasted from a pack file (the pack carries 20 bare matchMedia; see
AMBER-INPUT-1). The pack is the source of WORDING and MECHANISM only.

Invariants this script must not break, asserted by gates.py afterwards:
  - print pack, witness statement, Oak links, tier routes, word banks untouched
  - no storage / network / form / external asset / matchMedia introduced
  - the ratified GROW closure ADDS to the existing 'Next I will ___' line
"""
import re, sys, os, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import L

LIVE = "/home/user/Lessons/Science_Teesside/Grow/v3_40min"

# ---------------------------------------------------------------- CSS -------
# No transitions, no animations, no colour-only cues. The chassis already
# carries a global prefers-reduced-motion kill rule, so these static surfaces
# are RM-safe by construction (gate 12).
CSS = """
/* ===== GSG-1 graft layer (arrival 3+1, model limits, WORD HELP, GROW close) ===== */
.retr-grid{display:grid;gap:8px;margin:8px 0}
.retr-q{border:2px solid #cbd5e1;border-left:6px solid var(--grow);border-radius:12px;padding:10px 12px;background:#fbfdfc}
.retr-q.lead{border-left-color:#f97316;background:#fff8f1}
.retr-head{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-weight:900;color:#215e53;font-size:.92rem;margin-bottom:4px}
.retr-q.lead .retr-head{color:#9a3412}
.retr-badge{background:#10233f;color:#fff;border-radius:999px;padding:3px 9px;font-size:.76rem;font-weight:900}
.retr-q.lead .retr-badge{background:#9a3412}
.retr-ask{font-size:1.06rem;font-weight:800;margin:2px 0 6px}
.retr-route{font-size:.86rem;color:#334155;margin:0;line-height:1.5}
.retr-route b{color:#215e53}
.retr-declare{background:#fff7ed;border-left:5px solid #f97316;padding:9px 12px;border-radius:10px;margin:6px 0;font-size:.92rem}
.model-limit{border:2px solid #cbd5e1;border-radius:12px;margin:9px 0;overflow:hidden}
.model-limit .ml-row{padding:9px 12px;font-size:.95rem}
.model-limit .ml-yes{background:#eef8f4;border-bottom:2px solid #cbd5e1}
.model-limit .ml-no{background:#fff4e6}
.model-limit b{display:block;margin-bottom:2px}
.model-limit .ml-yes b{color:#215e53}
.model-limit .ml-no b{color:#9a3412}
.wordhelp{border:2px solid #cbd5e1;border-radius:12px;padding:10px 12px;background:#f8fafc;margin:9px 0}
.wordhelp h4{margin:0 0 6px;font-size:.95rem;color:#215e53}
.wh-row{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin:5px 0}
.wh-term{font-weight:900;font-size:1.02rem}
.wh-btn{background:#10233f;color:#fff;border:0;border-radius:999px;padding:4px 10px;font-size:.78rem;font-weight:800;cursor:pointer}
.wh-bridge{font-size:.9rem;color:#334155;margin:0 0 0 2px}
.wh-bridge[hidden]{display:none}
.wh-fade{font-size:.82rem;color:#64748b;margin:7px 0 0}
.speak-btn{background:#215e53;color:#fff;border:0;border-radius:999px;padding:5px 11px;font-size:.8rem;font-weight:800;cursor:pointer;margin:6px 0 0}
.speak-btn[hidden]{display:none}
.commit-box{border:2px solid var(--grow);border-radius:12px;padding:11px 13px;background:#f0faf6;margin:9px 0}
.commit-box h4{margin:0 0 7px;font-size:1rem;color:#215e53}
.commit-opts{display:flex;gap:7px;flex-wrap:wrap}
.commit-opt{background:#fff;border:2px solid #cbd5e1;border-radius:10px;padding:8px 12px;font-weight:800;font-size:.93rem;cursor:pointer}
.commit-opt.chosen{border-color:var(--grow);background:#dff2ea}
.commit-state{margin:8px 0 0;font-size:.9rem;color:#334155;font-weight:700}
.commit-note{margin:5px 0 0;font-size:.82rem;color:#64748b}
.grow-close{border:2px solid var(--grow);border-radius:12px;padding:11px 13px;background:#f0faf6;margin:9px 0}
.grow-close h4{margin:0 0 5px;font-size:1rem;color:#215e53}
.grow-close textarea{width:100%;min-height:64px;border:2px solid #cbd5e1;border-radius:10px;padding:8px;font:inherit;font-size:.98rem;box-sizing:border-box}
.grow-close .gc-note{font-size:.84rem;color:#64748b;margin:6px 0 0}
.gc-routes{font-size:.86rem;color:#334155;margin:6px 0 0}
@media print{
 .retr-q{border:1px solid #aaa;border-left:4px solid #333;background:#fff;padding:6px 8px}
 .speak-btn,.wh-btn,.commit-opt{display:none!important}
 .wh-bridge[hidden]{display:inline!important}
}
"""

# ----------------------------------------------------------------- JS -------
# Feature-detected, pupil-activated, silent degradation. No matchMedia.
# No storage, no network, no form. Nothing here scores or counts anything.
JS = """
/* ===== GSG-1 graft layer ===== */
/* Speech: pupil-activated only, never automatic. Silently removes itself
   where the browser has no speech synthesis. */
function gsgSpeak(btn){
 var host=btn.closest('[data-speak-host]');if(!host)return;
 var t=host.getAttribute('data-speak-text')||host.textContent||'';
 if(!('speechSynthesis' in window)||typeof SpeechSynthesisUtterance==='undefined')return;
 try{
  if(window.speechSynthesis.speaking){window.speechSynthesis.cancel();btn.textContent=btn.dataset.idle||'🔊 Read this aloud';return}
  var u=new SpeechSynthesisUtterance(t.replace(/\\s+/g,' ').trim());
  u.lang='en-GB';u.rate=.9;
  u.onend=function(){btn.textContent=btn.dataset.idle||'🔊 Read this aloud'};
  btn.dataset.idle=btn.dataset.idle||btn.textContent;
  btn.textContent='⏹ Stop reading';
  window.speechSynthesis.speak(u);
 }catch(e){}
}
(function(){
 var ok=('speechSynthesis' in window)&&(typeof SpeechSynthesisUtterance!=='undefined');
 if(ok)return;
 var b=document.querySelectorAll('.speak-btn');
 for(var i=0;i<b.length;i++){b[i].hidden=true}
})();
/* WORD HELP: the formal term is always the dominant text. The bridge stays
   hidden until a pupil asks for it, so the scaffold fades by request. */
function gsgWord(btn){
 var row=btn.closest('.wh-row');if(!row)return;
 var br=row.querySelector('.wh-bridge');if(!br)return;
 var open=!br.hidden;
 br.hidden=open;
 btn.setAttribute('aria-expanded',String(!open));
 btn.textContent=open?'word help':'hide help';
}
/* Starter commit: receives a prediction. It does NOT mark it. There is no
   correct answer here and nothing is counted, stored or scored — the reveal
   happens through the teaching that follows. */
function gsgCommit(btn){
 var box=btn.closest('.commit-box');if(!box)return;
 var opts=box.querySelectorAll('.commit-opt');
 for(var i=0;i<opts.length;i++){opts[i].classList.remove('chosen');opts[i].setAttribute('aria-pressed','false')}
 btn.classList.add('chosen');btn.setAttribute('aria-pressed','true');
 var st=box.querySelector('.commit-state');
 if(st)st.textContent='Prediction received: "'+(btn.textContent||'').trim()+'". Hold onto it — we find out by testing, not by being told.';
}
"""

SPEAK = ('<button class="speak-btn" type="button" onclick="gsgSpeak(this)" '
         'aria-label="Read these instructions aloud">🔊 Read this aloud</button>')


def esc_attr(t):
    return (t.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))


# ------------------------------------------------------------- builders -----
def build_retr(d, tier):
    """One tier's worth of the 3 retrieval questions + the lead-in."""
    key = {"Supported": "sup", "Standard": "std", "Stretch": "stg"}[tier]
    other = {"Supported": ("Standard", "std"), "Standard": ("Stretch", "stg"),
             "Stretch": ("Supported", "sup")}[tier]
    out = ['<div class="retr-grid">']
    for q in d["r"] + [d["lead"]]:
        lead = " lead" if q["badge"] == "Lead-in" else ""
        ask = q[key]
        # every question carries a stated non-reading route AND a tier step
        route = ('<p class="retr-route"><b>Non-reading route:</b> point to it, say it, '
                 'show it, or have an adult scribe your exact words. '
                 '<b>Next step up:</b> ' + other[0] + ' — ' + q[other[1]] + '</p>')
        out.append(
            '<div class="retr-q%s"><div class="retr-head">'
            '<span class="retr-badge">%s</span> %s</div>'
            '<p class="retr-ask">%s</p>%s</div>'
            % (lead, q["badge"], q["when"], ask, route))
    out.append("</div>")
    return "".join(out)


def build_arrival_panels(d):
    parts = []
    for i, tier in enumerate(("Supported", "Standard", "Stretch")):
        glyph = {"Supported": "◆", "Standard": "▲", "Stretch": "★"}[tier]
        on = " on" if i == 0 else ""
        parts.append(
            '<div class="tier%s" data-tier="%s" data-tier-panel="arrival">'
            '<div class="task-box" data-speak-host data-speak-text="%s">'
            '<b>%s %s — three retrieval questions and one lead-in</b>%s%s</div></div>'
            % (on, tier,
               esc_attr(" ".join(q[{"Supported": "sup", "Standard": "std",
                                    "Stretch": "stg"}[tier]]
                                 for q in d["r"] + [d["lead"]])),
               glyph, tier, build_retr(d, tier), SPEAK))
    return "".join(parts)


def build_model_limit(d):
    return ('<div class="model-limit"><div class="ml-row ml-yes">'
            '<b>✔ What this model helps us see</b>It %s.</div>'
            '<div class="ml-row ml-no"><b>✘ What this model does not show</b>It leaves out %s.</div>'
            '</div>' % (d["helps"], d["hides"]))


def build_wordhelp(d):
    rows = "".join(
        '<div class="wh-row"><span class="wh-term">%s</span>'
        '<button class="wh-btn" type="button" aria-expanded="false" '
        'onclick="gsgWord(this)">word help</button>'
        '<span class="wh-bridge" hidden>%s</span></div>' % (t, b)
        for t, b in d["words"])
    return ('<div class="wordhelp"><h4>📖 WORD HELP</h4>%s'
            '<p class="wh-fade">Use the scientific word first. Ask for help only when '
            'you need it. <b>TA fade route:</b> model the word, then prompt for it, '
            'then wait for it — drop a step as soon as the pupil no longer needs it.</p>'
            '</div>' % rows)


def build_commit(d):
    opts = "".join(
        '<button class="commit-opt" type="button" aria-pressed="false" '
        'onclick="gsgCommit(this)">%s</button>' % o for o in d["commit"]["opts"])
    return ('<div class="commit-box"><h4>🎯 Commit to a prediction</h4>'
            '<p style="margin:0 0 7px">%s</p><div class="commit-opts">%s</div>'
            '<p class="commit-state">Choose one. Say it, point to it, or press it.</p>'
            '<p class="commit-note">Nothing here is right or wrong yet, and nothing is '
            'marked, scored or stored. A prediction is worth having even when it turns '
            'out differently — that is what makes the test worth running.</p></div>'
            % (d["commit"]["q"], opts))


GROW_CLOSE = (
    '<div class="grow-close" data-speak-host data-speak-text="What I said, and what it '
    'changed. Write one line about what you said today and what changed because of it.">'
    '<h4>✍ GROW written close — the pupil writes this line</h4>'
    '<p style="margin:0 0 6px;font-size:1.08rem"><b>“What I said, and what it changed:”</b></p>'
    '<textarea aria-label="What I said, and what it changed" rows="3" '
    'placeholder="Write your own line here, or an adult writes down your exact words."></textarea>'
    '<p class="gc-note"><b>No adult initial is required.</b> The adult is the audience for '
    'this line, not its signatory. There is no signature, initial, tick or receipt mark — '
    'the line is closed by being written and received.</p>'
    '<p class="gc-routes"><b>If writing is the barrier:</b> say it and an adult scribes your '
    'exact words · point to what changed and say it aloud · record it in the school’s '
    'own workflow · draw it and caption it in one spoken sentence. '
    'The line is never removed, and the route never lowers the Science.</p>' + SPEAK + '</div>')

PRINT_CLOSE = (
    '<div class="print-box"><b>GROW written close — the pupil writes this line:</b><br/>'
    '“What I said, and what it changed:”<br/>'
    '________________________________________________________________<br/>'
    '________________________________________________________________</div>'
    '<p style="font-size:.85rem"><b>No adult initial is required.</b> The adult is audience '
    'for this line, not signatory — no signature, initial or receipt mark. If writing is the '
    'barrier, an adult scribes the pupil’s exact words.</p>')


# ------------------------------------------------------------ transform -----
def transform(code, d, s):
    orig = s

    # ---- A2: arrival rebuilt to 3 retrieval + 1 lead-in -------------------
    pat = (r'<div class="tier on" data-tier="Supported" data-tier-panel="arrival">'
           r'\s*<div class="task-box"><b>◆ Supported</b><p>.*?</p></div></div>'
           r'<div class="tier" data-tier="Standard" data-tier-panel="arrival">'
           r'\s*<div class="task-box"><b>▲ Standard</b><p>.*?</p></div></div>'
           r'<div class="tier" data-tier="Stretch" data-tier-panel="arrival">'
           r'\s*<div class="task-box"><b>★ Stretch</b><p>.*?</p></div></div>')
    s, n = re.subn(pat, lambda m: build_arrival_panels(d), s, count=1, flags=re.S)
    assert n == 1, "%s: arrival tier trio not replaced" % code

    # declaration of a substituted retrieval, on the slide itself
    if d["declare"]:
        s, n = re.subn(r'(<div class="entry-route")',
                       '<div class="retr-declare">%s</div>\\1' % d["declare"],
                       s, count=1)
        assert n == 1, "%s: declaration not inserted" % code

    # arrival rule line reflects the new shape
    s = s.replace(
        '<b>Rule:</b> Arrival retrieves. Do not teach today’s new concept here.',
        '<b>Rule:</b> Arrival retrieves three times and then leads in. '
        'R1 is last lesson, R2 is the previous week, R3 is older material, and the '
        'lead-in opens today without teaching today’s concept.')

    # ---- A5: judgement-free commit device on the Starter ------------------
    s, n = re.subn(
        r'(<div class="task-box"><h3>🔍 Bridge into today</h3><p[^>]*>.*?</p></div>)',
        lambda m: m.group(1) + build_commit(d), s, count=1, flags=re.S)
    assert n == 1, "%s: starter commit not inserted" % code

    # ---- A4: model-limitation pair on the FIRST I Do ----------------------
    s, n = re.subn(r'(<div class="model-steps" id="steps-[^"]*">)',
                   lambda m: build_model_limit(d) + m.group(1), s, count=1)
    assert n == 1, "%s: model-limit pair not inserted" % code

    # ---- A4: WORD HELP + speech on the Independent slide ------------------
    def indep(m):
        blk = m.group(0)
        anchor = '<div class="scaffold-box"'
        if anchor in blk:
            blk = blk.replace(anchor, build_wordhelp(d) + anchor, 1)
        else:
            blk = blk.replace('</section>', build_wordhelp(d) + '</section>', 1)
        return blk
    s, n = re.subn(r'<section class="slide"[^>]*data-type="independent".*?</section>',
                   indep, s, count=1, flags=re.S)
    assert n == 1, "%s: WORD HELP not inserted on independent" % code

    # ---- A1: the ratified GROW written close, ADDED beside 'Next I will' --
    s, n = re.subn(r'(<div class="close-line">.*?</div>)',
                   lambda m: m.group(1) + GROW_CLOSE, s, count=1, flags=re.S)
    assert n == 1, "%s: GROW close not inserted on exit" % code

    # ---- A1 print counterpart, additive to the existing closure box -------
    s, n = re.subn(
        r'(<div class="print-box"><b>ONE closure line[^<]*</b><br/>Next I will _+</div>)',
        lambda m: m.group(1) + PRINT_CLOSE, s, count=1)
    assert n == 1, "%s: GROW close not inserted in print pack" % code

    # ---- A2 print counterpart: the arrival retrieval set ------------------
    prows = "".join(
        '<p style="margin:3px 0"><b>%s · %s:</b> %s</p><div class="print-line"></div>'
        % (q["badge"], q["when"], q["std"]) for q in d["r"] + [d["lead"]])
    # two live wordings exist: 'Arrival — what you already know:' (W3A, the
    # baseline-adjacent file) and 'Arrival retrieval:' (the other nine).
    s, n = re.subn(
        r'(<p><b>Arrival[^<]*</b>[^<]*</p>)',
        lambda m: m.group(1) + prows, s, count=1)
    assert n == 1, "%s: arrival print rows not inserted" % code

    # ---- A4 print counterpart: model pair + WORD HELP ---------------------
    pml = ('<div class="print-box"><b>What this model helps us see:</b> It %s.<br/>'
           '<b>What this model does not show:</b> It leaves out %s.</div>'
           % (d["helps"], d["hides"]))
    pwh = ('<div class="print-box"><b>WORD HELP</b><br/>%s</div>'
           % "<br/>".join('<b>%s</b> — %s' % (t, b) for t, b in d["words"]))
    s, n = re.subn(r'(<h3>Evidence can be</h3>)',
                   lambda m: pml + pwh + m.group(1), s, count=1)
    assert n == 1, "%s: print model/wordhelp not inserted" % code

    # ---- CSS + JS ---------------------------------------------------------
    s, n = re.subn(r'</style>', CSS + '</style>', s, count=1)
    assert n == 1
    idx = s.rfind('</script>')
    assert idx > 0
    s = s[:idx] + JS + s[idx:]

    assert s != orig
    return s


def main():
    for code, d in L.items():
        p = os.path.join(LIVE, d["file"])
        s = open(p, encoding="utf-8").read()
        out = transform(code, d, s)
        open(p, "w", encoding="utf-8").write(out)
        print("grafted %-42s %7d -> %7d bytes" % (d["file"], len(s), len(out)))


if __name__ == "__main__":
    main()
