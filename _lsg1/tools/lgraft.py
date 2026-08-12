#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LSG-1 Phase A graft — A2/A5 onto the fifteen LIVE LAUNCH lessons.

Hand-written into the live LAUNCH chassis idiom (`box task`, `box scaf`,
`note`, `tier(...)`, `proute`, `pline`). Nothing is copy-pasted from a pack
file: the pack carries 30 bare matchMedia (AMBER-INPUT-1), so it is a quarry
for wording and mechanism only.

PROTECTED AND ASSERTED BEFORE EVERY WRITE — the pass fails closed if any move:
  * the written closure line, 2 per file, byte-identical
  * the `.close` block and its no-signature framing
  * the assessor witness block, byte-identical
  * print-family marker count, tier counts, word-bank count
  * zero matchMedia / storage / network / form / external assets
"""
import re, os, sys, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lcontent import L

LIVE = "/home/user/Lessons/Science_Teesside/Launch/v3_40min"

CLOSE_BLOCK = r'<div class="close">.*?(?:<div class="pline"[^>]*></div>){2}</div>'

PRINT_FAMILY = (r'\bpp\b|\bproute\b|\bpline\b|\bpidline\b|\bpentry\b|'
                r'printpack|print-section|print-witness|printTier|afterprint|'
                r'data-print-tier|data-tier')

# ---------------------------------------------------------------- CSS -------
# No animation, no transition. The chassis' global reduced-motion rule covers
# inherited motion; this layer declares none, so its RM classification is STATIC.
CSS = """
/* ===== LSG-1 graft layer (3+1 arrival, model limits, WORD HELP, commit) ===== */
.lretr{display:grid;gap:8px;margin:8px 0}
.lq{border:2px solid #cbd5e1;border-left:6px solid #7A5C9E;border-radius:12px;padding:10px 12px;background:#fbfbfd}
.lq.lead{border-left-color:#f97316;background:#fff8f1}
.lq-head{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-weight:800;color:#4b3b6b;font-size:.92rem;margin-bottom:4px}
.lq.lead .lq-head{color:#9a3412}
.lq-badge{background:#2b2140;color:#fff;border-radius:999px;padding:3px 9px;font-size:.76rem;font-weight:800}
.lq.lead .lq-badge{background:#9a3412}
.lq-ask{font-size:1.05rem;font-weight:700;margin:2px 0 6px}
.lq-route{font-size:.86rem;color:#334155;margin:0;line-height:1.5}
.lq-route b{color:#4b3b6b}
.lq-declare{background:#fff7ed;border-left:5px solid #f97316;padding:9px 12px;border-radius:10px;margin:6px 0;font-size:.92rem}
.lmodel{border:2px solid #cbd5e1;border-radius:12px;margin:9px 0;overflow:hidden}
.lmodel .lm-row{padding:9px 12px;font-size:.95rem}
.lmodel .lm-yes{background:#f2eefa;border-bottom:2px solid #cbd5e1}
.lmodel .lm-no{background:#fff4e6}
.lmodel b{display:block;margin-bottom:2px}
.lmodel .lm-yes b{color:#4b3b6b}
.lmodel .lm-no b{color:#9a3412}
.lword{border:2px solid #cbd5e1;border-radius:12px;padding:10px 12px;background:#f8fafc;margin:9px 0}
.lword h4{margin:0 0 6px;font-size:.95rem;color:#4b3b6b}
.lw-row{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin:5px 0}
.lw-term{font-weight:800;font-size:1.02rem}
.lw-btn{background:#2b2140;color:#fff;border:0;border-radius:999px;padding:4px 10px;font-size:.78rem;font-weight:700;cursor:pointer}
.lw-bridge{font-size:.9rem;color:#334155;margin:0 0 0 2px}
.lw-bridge[hidden]{display:none}
.lw-fade{font-size:.82rem;color:#64748b;margin:7px 0 0}
.lspeak{background:#4b3b6b;color:#fff;border:0;border-radius:999px;padding:5px 11px;font-size:.8rem;font-weight:700;cursor:pointer;margin:6px 0 0}
.lspeak[hidden]{display:none}
.lcommit{border:2px solid #7A5C9E;border-radius:12px;padding:11px 13px;background:#f6f3fb;margin:9px 0}
.lcommit h4{margin:0 0 7px;font-size:1rem;color:#4b3b6b}
.lc-opts{display:flex;gap:7px;flex-wrap:wrap}
.lc-opt{background:#fff;color:#2b2140;border:2px solid #cbd5e1;border-radius:10px;padding:8px 12px;font-weight:700;font-size:.93rem;cursor:pointer;box-shadow:none}
.lc-opt.chosen{border-color:#7A5C9E;background:#ece6f7;color:#2b2140}
.lc-state{margin:8px 0 0;font-size:.9rem;color:#334155;font-weight:700}
.lc-note{margin:5px 0 0;font-size:.82rem;color:#64748b}
@media print{
 .lq{border:1px solid #aaa;border-left:4px solid #333;background:#fff;padding:6px 8px}
 .lspeak,.lw-btn,.lc-opt{display:none!important}
 .lw-bridge[hidden]{display:inline!important}
}
"""

# ----------------------------------------------------------------- JS -------
JS = """
/* ===== LSG-1 graft layer =====
   Speech is pupil-activated only and never automatic; it removes itself where
   the browser has no synthesis. WORD HELP keeps the formal Biology term
   dominant and hides the bridge until it is asked for. The commit device
   receives a prediction and does not mark it. Nothing here is stored, scored
   or counted, and this layer queries no media API at all. */
function lsgSpeak(btn){
 var host=btn.closest('[data-speak-host]');if(!host)return;
 var t=host.getAttribute('data-speak-text')||host.textContent||'';
 if(!('speechSynthesis' in window)||typeof SpeechSynthesisUtterance==='undefined')return;
 try{
  if(window.speechSynthesis.speaking){window.speechSynthesis.cancel();btn.textContent=btn.dataset.idle||'🔊 Read this aloud';return}
  var u=new SpeechSynthesisUtterance(t.replace(/\\s+/g,' ').trim());
  u.lang='en-GB';u.rate=.9;
  btn.dataset.idle=btn.dataset.idle||btn.textContent;
  u.onend=function(){btn.textContent=btn.dataset.idle};
  btn.textContent='⏹ Stop reading';
  window.speechSynthesis.speak(u);
 }catch(e){}
}
(function(){
 var ok=('speechSynthesis' in window)&&(typeof SpeechSynthesisUtterance!=='undefined');
 if(ok)return;
 var b=document.querySelectorAll('.lspeak');
 for(var i=0;i<b.length;i++){b[i].hidden=true}
})();
function lsgWord(btn){
 var row=btn.closest('.lw-row');if(!row)return;
 var br=row.querySelector('.lw-bridge');if(!br)return;
 var open=!br.hidden;
 br.hidden=open;
 btn.setAttribute('aria-expanded',String(!open));
 btn.textContent=open?'word help':'hide help';
}
function lsgCommit(btn){
 var box=btn.closest('.lcommit');if(!box)return;
 var o=box.querySelectorAll('.lc-opt');
 for(var i=0;i<o.length;i++){o[i].classList.remove('chosen');o[i].setAttribute('aria-pressed','false')}
 btn.classList.add('chosen');btn.setAttribute('aria-pressed','true');
 var st=box.querySelector('.lc-state');
 if(st)st.textContent='Prediction received: "'+(btn.textContent||'').trim()+'". Hold onto it — we find out by testing and reasoning, not by being told.';
}
"""

SPEAK = ('<button class="lspeak" type="button" onclick="lsgSpeak(this)" '
         'aria-label="Read these instructions aloud">🔊 Read this aloud</button>')

TIERKEY = {"Supported": "sup", "Standard": "std", "Stretch": "stg"}
NEXTTIER = {"Supported": ("Standard", "std"), "Standard": ("Stretch", "stg"),
            "Stretch": ("Supported", "sup")}


def esc(t):
    return (t.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))


def build_retr(d, tier):
    k = TIERKEY[tier]
    nt, nk = NEXTTIER[tier]
    out = ['<div class="lretr">']
    for q in d["r"] + [d["lead"]]:
        lead = " lead" if q["badge"] == "Lead-in" else ""
        out.append(
            '<div class="lq%s"><div class="lq-head"><span class="lq-badge">%s</span> %s</div>'
            '<p class="lq-ask">%s</p>'
            '<p class="lq-route"><b>Non-reading route:</b> point to it, say it, or show it. '
            'An adult can scribe your exact words. <b>Next step up:</b> %s — %s</p></div>'
            % (lead, q["badge"], q["when"], q[k], nt, q[nk]))
    out.append("</div>")
    return "".join(out)


def build_arrival(d):
    parts = []
    for i, tier in enumerate(("Supported", "Standard", "Stretch")):
        glyph = {"Supported": "◆", "Standard": "▲", "Stretch": "★"}[tier]
        on = "tier on" if i == 0 else "tier "
        spoken = " ".join(q[TIERKEY[tier]] for q in d["r"] + [d["lead"]])
        parts.append(
            '<div class="%s" data-tier-panel="arrival" data-tier="%s">'
            '<div class="box task" data-speak-host data-speak-text="%s">'
            '<b>%s %s — three retrieval questions and one lead-in</b>%s%s</div></div>'
            % (on, tier, esc(spoken), glyph, tier, build_retr(d, tier), SPEAK))
    return "".join(parts)


def build_model(d):
    return ('<div class="lmodel"><div class="lm-row lm-yes">'
            '<b>✔ What this model helps us see</b>It %s.</div>'
            '<div class="lm-row lm-no"><b>✘ What this model does not show</b>It leaves out %s.</div>'
            '</div>' % (d["helps"], d["hides"]))


def build_word(d):
    rows = "".join(
        '<div class="lw-row"><span class="lw-term">%s</span>'
        '<button class="lw-btn" type="button" aria-expanded="false" '
        'onclick="lsgWord(this)">word help</button>'
        '<span class="lw-bridge" hidden>%s</span></div>' % (t, b)
        for t, b in d["words"])
    return ('<div class="lword"><h4>📖 WORD HELP</h4>%s'
            '<p class="lw-fade">Use the Biology word first. Ask for help only when you need '
            'it. <b>TA fade route:</b> model the word. Then prompt for it. Then wait for it. '
            'Drop a step as soon as the pupil no longer needs it.</p></div>' % rows)


def build_commit(d):
    opts = "".join('<button class="lc-opt" type="button" aria-pressed="false" '
                   'onclick="lsgCommit(this)">%s</button>' % o
                   for o in d["commit"]["opts"])
    return ('<div class="lcommit"><h4>🎯 Commit to a prediction</h4>'
            '<p style="margin:0 0 7px">%s</p><div class="lc-opts">%s</div>'
            '<p class="lc-state">Choose one. Say it, point to it, or press it.</p>'
            '<p class="lc-note">Nothing here is right or wrong yet, and nothing is marked, '
            'scored or stored. A prediction is still worth having when it turns out '
            'differently — that is what makes the test worth running.</p></div>'
            % (d["commit"]["q"], opts))


def transform(code, d, s):
    # ---- capture every protected surface BEFORE touching anything -----------
    guard = dict(
        closure=len(re.findall(r'What I said, and what it changed', s)),
        # The close block ends at its own closing tag, immediately after its two
        # ruled .pline rows. Capturing as far as the NEXT sibling instead made
        # the guard fire on an insertion that never touched the block - a false
        # positive on the most protected surface in the pass, caught because the
        # transform fails closed.
        close_block=re.search(CLOSE_BLOCK, s, re.S).group(0),
        witness=re.search(r'<div id="print-witness".*?(?=</div>\s*</div>\s*<script|$)',
                          s, re.S).group(0),
        pfam=len(re.findall(PRINT_FAMILY, s)),
        tiers=tuple(len(re.findall(t, s)) for t in ("Supported", "Standard", "Stretch")),
        wbank=len(re.findall(r'(?i)word[ -]?bank', s)),
        nosig=len(re.findall(r'(?i)no adult (signature|initial)|No signature|no initials', s)),
    )

    # ---- A2 · arrival rebuilt to 3 retrieval + 1 lead-in -------------------
    pat = (r'<div class="tier on" data-tier-panel="arrival" data-tier="Supported">'
           r'<div class="box task"><b>◆ Supported</b><p>.*?</p></div></div>'
           r'<div class="tier " data-tier-panel="arrival" data-tier="Standard">'
           r'<div class="box task"><b>▲ Standard</b><p>.*?</p></div></div>'
           r'<div class="tier " data-tier-panel="arrival" data-tier="Stretch">'
           r'<div class="box task"><b>★ Stretch</b><p>.*?</p></div></div>')
    s, n = re.subn(pat, lambda m: build_arrival(d), s, count=1, flags=re.S)
    assert n == 1, "%s: arrival tier trio not replaced" % code

    if d["declare"]:
        s, n = re.subn(r'(<div class="entry-route")',
                       '<div class="lq-declare">%s</div>\\1' % d["declare"], s, count=1)
        assert n == 1, "%s: declaration not inserted" % code

    s = s.replace(
        '<div class="note">Arrival retrieves. It does not teach today’s new concept.</div>',
        '<div class="note">Arrival retrieves three times, then leads in. R1 is last lesson, '
        'R2 is the previous week, R3 is older material, and the lead-in opens today without '
        'teaching today’s concept.</div>')

    # ---- A5 · judgement-free commit on the Starter -------------------------
    m = re.search(r'<section class="slide"[^>]*data-type="starter".*?</section>', s, re.S)
    assert m, "%s: starter not found" % code
    blk = m.group(0)
    anchor = '<div class="participation">'
    assert anchor in blk, "%s: starter participation anchor missing" % code
    s = s.replace(blk, blk.replace(anchor, build_commit(d) + anchor, 1), 1)

    # ---- A5 · model-limitation pair on the FIRST I Do -----------------------
    # The I Do slide carries no `participation` block in this chassis (verified
    # 0/15); `science-gate` is the anchor that IS uniform across all four slide
    # types, 15/15. Anchoring on the wrong one failed closed before any write.
    gate_anchor = '<div class="science-gate">'
    m = re.search(r'<section class="slide"[^>]*data-type="ido".*?</section>', s, re.S)
    assert m, "%s: ido not found" % code
    blk = m.group(0)
    assert gate_anchor in blk, "%s: ido science-gate anchor missing" % code
    s = s.replace(blk, blk.replace(gate_anchor, build_model(d) + gate_anchor, 1), 1)

    # ---- A5 · WORD HELP + speech on Independent ----------------------------
    m = re.search(r'<section class="slide"[^>]*data-type="independent".*?</section>', s, re.S)
    assert m, "%s: independent not found" % code
    blk = m.group(0)
    assert anchor in blk, "%s: independent participation anchor missing" % code
    s = s.replace(blk, blk.replace(anchor, build_word(d) + SPEAK + anchor, 1), 1)

    # ---- A5 · speech on Exit, WITHOUT touching the close block -------------
    m = re.search(r'<section class="slide"[^>]*data-type="exit".*?</section>', s, re.S)
    blk = m.group(0)
    tail = '<div class="participation">'
    assert tail in blk, "%s: exit participation anchor missing" % code
    speak_exit = ('<div data-speak-host data-speak-text="Exit. Answer the question for your '
                  'tier. An adult receives your response and gives one next step. Then write '
                  'the closure line: what I said, and what it changed.">' + SPEAK + '</div>')
    s = s.replace(blk, blk.replace(tail, speak_exit + tail, 1), 1)

    # ---- print counterparts: arrival rows, model pair, WORD HELP -----------
    prows = "".join(
        '<p style="margin:3px 0"><b>%s · %s:</b> %s</p><div class="pline"></div>'
        % (q["badge"], q["when"], q["std"]) for q in d["r"] + [d["lead"]])
    s, n = re.subn(r'(<p><b>(?:Arrival|Retrieval)[^<]*</b>[^<]*</p>)',
                   lambda m: m.group(1) + prows, s, count=1)
    assert n == 1, "%s: print arrival rows not inserted" % code

    pml = ('<div class="box scaf"><b>What this model helps us see:</b> It %s.<br/>'
           '<b>What this model does not show:</b> It leaves out %s.</div>'
           % (d["helps"], d["hides"]))
    pwh = ('<div class="box scaf"><b>WORD HELP</b><br/>%s</div>'
           % "<br/>".join('<b>%s</b> — %s' % (t, b) for t, b in d["words"]))
    s, n = re.subn(r'(<h3>Evidence target</h3>)', lambda m: pml + pwh + m.group(1),
                   s, count=1)
    assert n == 1, "%s: print model/wordhelp not inserted" % code

    # ---- CSS + JS ----------------------------------------------------------
    s, n = re.subn(r'</style>', CSS + '</style>', s, count=1)
    assert n == 1
    i = s.rfind('</script>')
    assert i > 0
    s = s[:i] + JS + s[i:]

    # ---- PROTECTED SURFACES: assert AFTER, fail closed ---------------------
    assert len(re.findall(r'What I said, and what it changed', s)) == guard["closure"] == 2, \
        "%s: CLOSURE LINE COUNT CHANGED" % code
    assert re.search(CLOSE_BLOCK, s, re.S).group(0) == guard["close_block"], \
        "%s: CLOSE BLOCK ALTERED" % code
    assert re.search(r'<div id="print-witness".*?(?=</div>\s*</div>\s*<script|$)',
                     s, re.S).group(0) == guard["witness"], "%s: WITNESS ALTERED" % code
    assert len(re.findall(PRINT_FAMILY, s)) >= guard["pfam"], "%s: print family shrank" % code
    assert tuple(len(re.findall(t, s)) for t in ("Supported", "Standard", "Stretch")) \
        >= guard["tiers"], "%s: tier counts shrank" % code
    assert len(re.findall(r'(?i)word[ -]?bank', s)) >= guard["wbank"], \
        "%s: word bank shrank" % code
    assert len(re.findall(r'(?i)no adult (signature|initial)|No signature|no initials', s)) \
        == guard["nosig"], "%s: no-signature framing changed" % code
    for bad, lbl in ((r'matchMedia', 'matchMedia'),
                     (r'localStorage|sessionStorage|indexedDB', 'storage'),
                     (r'fetch\(|XMLHttpRequest|sendBeacon|WebSocket', 'network'),
                     (r'<form|form-action', 'form'),
                     (r'href="assets/|src="assets/', 'external asset')):
        assert not re.search(bad, s), "%s: %s introduced" % (code, lbl)
    return s


def main():
    codes = sys.argv[1:] or list(L.keys())
    for code in codes:
        d = L[code]
        p = os.path.join(LIVE, d["file"])
        s = open(p, encoding="utf-8").read()
        out = transform(code, d, s)
        open(p, "w", encoding="utf-8").write(out)
        print("grafted %-46s %7d -> %7d bytes" % (d["file"], len(s), len(out)))


if __name__ == "__main__":
    main()
