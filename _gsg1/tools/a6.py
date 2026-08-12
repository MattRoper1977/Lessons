#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSG-1 A6 — the ONE specimen lab: W4A Mechanism Hunt.

Transplanted into the LIVE W4A We Do 2 in chassis idiom, on the BSG-1 lab
pattern: predict-commit -> test -> freeze -> explain. Button-only. Identity is
carried by a shape glyph AND a word, never by colour. Zero matchMedia, zero
storage, zero network, no animation (the chassis' global reduced-motion rule
covers it and nothing here declares motion anyway). The print pack is untouched.

ADDED BESIDE the existing lever pivot explorer, which is live content and is not
removed. W4A is about levers, pulleys AND gears; the live widget covers only the
lever, which is why this is the lesson with the real gap.

Content source: the pack's lessonConfig lab spec (three mechanisms and what each
changes) and its SCIENCE GLITCH repair device. NOT ported: the pack's
seven-rung prompt ladder - that would be a seventh wording of the WT-DS ladder
and is RED under this pass. Nothing is copy-pasted; this is hand-written.

This is a SPECIMEN. It stops here pending Matt's written sign-off.
"""
import re

P = "/home/user/Lessons/Science_Teesside/Grow/v3_40min/SCI_G_W4A_Mechanisms_Explore.html"

CSS = """
/* ===== GSG-1 A6 specimen: W4A Mechanism Hunt ===== */
.mhunt{border:2px solid var(--grow);border-radius:14px;padding:12px 14px;background:#f7fcfa;margin:10px 0}
.mhunt h3{margin:0 0 4px;color:#215e53}
.mh-step{font-weight:900;color:#10233f;margin:9px 0 4px;font-size:.95rem}
.mh-row{display:flex;gap:8px;flex-wrap:wrap}
.mh-btn{background:#fff;color:#10233f;border:3px solid #94a3b8;border-radius:10px;padding:9px 13px;font-weight:900;font-size:.95rem;cursor:pointer;display:flex;align-items:center;gap:7px;box-shadow:none}
.mh-btn .mh-glyph{font-size:1.15rem}
.mh-btn[data-m="lever"]{border-style:solid}
.mh-btn[data-m="pulley"]{border-style:dashed}
.mh-btn[data-m="gears"]{border-style:dotted}
.mh-btn.picked{border-color:var(--grow);background:#dff2ea;color:#10233f}
.mh-btn.tested{border-color:#10233f;background:#eef2f7;color:#10233f}
.mh-say{margin:7px 0 0;font-size:.92rem;color:#334155;font-weight:700}
.mh-stage{border:2px solid #cbd5e1;border-radius:12px;background:#fff;padding:11px;margin:8px 0;min-height:64px}
.mh-stage .mh-name{font-weight:900;font-size:1.05rem;color:#10233f}
.mh-frozen{border-left:6px solid #10233f;background:#f8fafc;border-radius:10px;padding:9px 11px;margin:8px 0;font-size:.9rem}
.mh-frozen ol{margin:5px 0 0 18px;padding:0}
.mh-frozen li{margin:3px 0}
.mh-glitch{border:2px solid #b55f25;background:#fff4e6;border-radius:12px;padding:10px 12px;margin:9px 0}
.mh-glitch b{color:#9a3412}
@media print{.mhunt{display:none}}
"""

JS = """
/* ===== GSG-1 A6 specimen: W4A Mechanism Hunt =====
   predict-commit -> test -> freeze -> explain. Nothing is marked, scored or
   stored. The prediction is received, never graded: the pupil finds out by
   testing, which is the whole point of predicting first. */
var gsgMh={pred:null,tested:[]};
var gsgMhData={
 lever :{glyph:'\\u25B2',name:'LEVER',
   change:'Turns around a pivot. It can cut the effort you need, but the effort end has to move further.'},
 pulley:{glyph:'\\u25CE',name:'PULLEY',
   change:'A fixed pulley changes the direction of your pull. You can pull down to lift something up.'},
 gears :{glyph:'\\u2733',name:'GEARS',
   change:'Meshed gears pass turning from one wheel to another. They can change speed, direction or turning force.'}
};
function gsgMhPredict(btn){
 var box=document.getElementById('mhunt-W4A'),m=btn.dataset.m;
 var all=box.querySelectorAll('.mh-predict .mh-btn');
 for(var i=0;i<all.length;i++){all[i].classList.remove('picked');all[i].setAttribute('aria-pressed','false')}
 btn.classList.add('picked');btn.setAttribute('aria-pressed','true');
 gsgMh.pred=m;
 document.getElementById('mh-say').textContent=
  'Prediction received: '+gsgMhData[m].name+'. Nothing is marked. Test all three and find out.';
}
function gsgMhTest(btn){
 var m=btn.dataset.m,d=gsgMhData[m];
 btn.classList.add('tested');
 document.getElementById('mh-stage').innerHTML=
  '<div class="mh-name">'+d.glyph+' '+d.name+'</div><p style="margin:5px 0 0">'+d.change+'</p>';
 if(gsgMh.tested.indexOf(m)<0){
  gsgMh.tested.push(m);
  var li=document.createElement('li');
  li.textContent=d.name+' \\u2014 '+d.change;
  document.getElementById('mh-list').appendChild(li);
 }
 var done=gsgMh.tested.length;
 document.getElementById('mh-frozen-note').textContent= done<3
  ? 'Tested '+done+' of the three. Each result stays on the list so you can compare them.'
  : 'All three are on the list and they stay there. Now compare them: which one changed the DIRECTION of a force, and which one changed how BIG it needed to be?';
}
function gsgMhGlitch(btn){
 document.getElementById('mh-glitch-result').textContent=
  btn.dataset.fix==='1'
   ? 'Repaired. A lever does not make new energy. It trades a smaller effort for a longer distance moved \\u2014 you get the force you need, and you pay for it in movement.'
   : 'Kept as it stands. Check it against your frozen list before you settle on that: if a lever made extra energy, what would you expect the effort end to do?';
}
"""

WIDGET = """<div class="mhunt" id="mhunt-W4A">
<h3>\U0001F50E Mechanism Hunt</h3>
<p style="margin:0">Three mechanisms. Each one changes something about a force. Find out which does what.</p>
<div class="mh-step">Step 1 · Predict, before you test</div>
<p style="margin:0 0 5px">Which one changes the <b>direction</b> of a pull?</p>
<div class="mh-row mh-predict">
<button class="mh-btn" data-m="lever" type="button" aria-pressed="false" onclick="gsgMhPredict(this)"><span class="mh-glyph">▲</span>LEVER</button>
<button class="mh-btn" data-m="pulley" type="button" aria-pressed="false" onclick="gsgMhPredict(this)"><span class="mh-glyph">◎</span>PULLEY</button>
<button class="mh-btn" data-m="gears" type="button" aria-pressed="false" onclick="gsgMhPredict(this)"><span class="mh-glyph">✳</span>GEARS</button>
</div>
<p class="mh-say" id="mh-say" aria-live="polite">Choose one. Say it, point to it, or press it. Nothing here is right or wrong yet.</p>
<div class="mh-step">Step 2 · Test each one</div>
<div class="mh-row">
<button class="mh-btn" data-m="lever" type="button" onclick="gsgMhTest(this)"><span class="mh-glyph">▲</span>Test LEVER</button>
<button class="mh-btn" data-m="pulley" type="button" onclick="gsgMhTest(this)"><span class="mh-glyph">◎</span>Test PULLEY</button>
<button class="mh-btn" data-m="gears" type="button" onclick="gsgMhTest(this)"><span class="mh-glyph">✳</span>Test GEARS</button>
</div>
<div class="mh-stage" id="mh-stage" aria-live="polite">Press a mechanism to see what it changes.</div>
<div class="mh-frozen"><b>Frozen results — these stay on the page</b>
<ol id="mh-list"></ol>
<p style="margin:6px 0 0" id="mh-frozen-note" aria-live="polite">Nothing tested yet.</p></div>
<div class="mh-step">Step 3 · Explain</div>
<div class="mh-glitch"><b>SCIENCE GLITCH:</b> “A lever creates extra energy.”
<div class="mh-row" style="margin-top:7px">
<button class="mh-btn" data-fix="0" type="button" onclick="gsgMhGlitch(this)">Keep the claim</button>
<button class="mh-btn" data-fix="1" type="button" onclick="gsgMhGlitch(this)">Repair it</button>
</div>
<p class="mh-say" id="mh-glitch-result" aria-live="polite">Use your frozen list as the evidence. Decide, then say why.</p></div>
<p style="font-size:.84rem;color:#64748b;margin:8px 0 0">Every step is a button, and each mechanism carries a shape and its name as well as its colour. Say it, point to it or have an adult press it — the route does not change the Science.</p>
</div>"""


def main():
    s = open(P, encoding="utf-8").read()
    assert "mhunt-W4A" not in s, "specimen already present"

    # add BESIDE the live lever explorer inside We Do 2 - nothing is removed
    anchor = ('<div class="widget-feedback" aria-live="polite" id="wf-W4A">'
              'Move the pivot and describe the gain <b>and</b> the trade-off.</div></div>')
    assert s.count(anchor) == 1, "We Do 2 anchor not unique"
    s = s.replace(anchor, anchor + WIDGET, 1)

    s = s.replace("</style>", CSS + "</style>", 1)
    i = s.rfind("</script>")
    s = s[:i] + JS + s[i:]

    open(P, "w", encoding="utf-8").write(s)
    print("A6 specimen installed in SCI_G_W4A_Mechanisms_Explore.html")


if __name__ == "__main__":
    main()
