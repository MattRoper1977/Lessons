#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LSG-1 A6 — the ONE specimen lab: W5L2 Osmosis Core Practical.

Approved BSG/GSG pattern: predict-commit -> test -> freeze -> explain.
Button-only. Identity by border-pattern + glyph + word, never colour alone.
Zero matchMedia, zero storage, zero network, no declared motion. Print pack,
witness block and the written closure line all asserted byte-identical.

EARNING THE PLACE — derived, not assumed. W5L2's live We Do 2 is a
"Percentage-change lab": two number inputs and a Calculate button. It computes
ONE percentage change from two typed masses. Three things the LO needs are
absent from it:
  * a button-only route - the only way into the live widget is typing numbers
  * a prediction before the result
  * the comparison ACROSS the concentration series, which is where the pattern
    (gain -> no change -> loss) and the zero-crossing actually live
The lab is added BESIDE the live widget, which still takes the pupils' own
measurements. Nothing is removed.

This is a SPECIMEN. It stops here pending Matt's written sign-off; the other
fourteen wait for a close order and will each face the earn-the-place question.
"""
import re, os

P = ("/home/user/Lessons/Science_Teesside/Launch/v3_40min/"
     "SCI_L_W5L2_Osmosis_Core_Practical_Explore.html")
CLOSE_BLOCK = r'<div class="close">.*?(?:<div class="pline"[^>]*></div>){2}</div>'

CSS = """
/* ===== LSG-1 A6 specimen: W5L2 Osmosis lab ===== */
.oslab{border:2px solid #7A5C9E;border-radius:14px;padding:12px 14px;background:#faf8fd;margin:10px 0}
.oslab h3{margin:0 0 4px;color:#4b3b6b}
.os-step{font-weight:800;color:#2b2140;margin:9px 0 4px;font-size:.95rem}
.os-row{display:flex;gap:8px;flex-wrap:wrap}
.os-btn{background:#fff;color:#2b2140;border:3px solid #94a3b8;border-radius:10px;padding:9px 13px;font-weight:800;font-size:.95rem;cursor:pointer;display:flex;align-items:center;gap:7px;box-shadow:none}
.os-btn .os-glyph{font-size:1.15rem}
.os-btn.i0{border-style:solid}.os-btn.i1{border-style:dashed}.os-btn.i2{border-style:dotted}
.os-btn.picked{border-color:#7A5C9E;background:#ece6f7;color:#2b2140}
.os-btn.tested{border-color:#2b2140;background:#eef2f7;color:#2b2140}
.os-say{margin:7px 0 0;font-size:.92rem;color:#334155;font-weight:700}
.os-stage{border:2px solid #cbd5e1;border-radius:12px;background:#fff;padding:11px;margin:8px 0;min-height:62px}
.os-stage .os-name{font-weight:800;font-size:1.05rem;color:#2b2140}
.os-frozen{border-left:6px solid #2b2140;background:#f8fafc;border-radius:10px;padding:9px 11px;margin:8px 0;font-size:.9rem}
.os-frozen ol{margin:5px 0 0 18px;padding:0}
.os-frozen li{margin:3px 0}
.os-glitch{border:2px solid #b55f25;background:#fff4e6;border-radius:12px;padding:10px 12px;margin:9px 0}
.os-glitch b{color:#9a3412}
.os-foot{font-size:.84rem;color:#64748b;margin:8px 0 0}
@media print{.oslab{display:none}}
"""

JS = """
/* ===== LSG-1 A6 specimen: W5L2 Osmosis lab =====
   predict-commit -> test -> freeze -> explain. The prediction is received and
   never marked; the pupil finds out by testing. Nothing is stored, scored or
   counted, and this layer queries no media API. */
var osLab={tested:[]};
var osData=[
 {g:'\\u25B2',n:'Pure water',
  t:'Water is more concentrated outside than inside the cells, so water moves IN. The piece gains mass \\u2014 typically about +18%.'},
 {g:'\\u25CE',n:'Matching concentration',
  t:'The solution matches the cell contents. Water moves both ways equally, so there is no net movement. Mass barely changes \\u2014 close to 0%.'},
 {g:'\\u2733',n:'Strong sugar solution',
  t:'Water is more concentrated inside the cells than outside, so water moves OUT. The piece loses mass \\u2014 typically about \\u221215%.'}
];
function osPredict(btn){
 var box=document.getElementById('oslab-W5L2');
 var all=box.querySelectorAll('.os-predict .os-btn');
 for(var i=0;i<all.length;i++){all[i].classList.remove('picked');all[i].setAttribute('aria-pressed','false')}
 btn.classList.add('picked');btn.setAttribute('aria-pressed','true');
 document.getElementById('os-say').textContent=
  'Prediction received: '+btn.dataset.label+'. Nothing is marked. Test the three solutions and find out.';
}
function osTest(btn){
 var k=Number(btn.dataset.i),d=osData[k];
 btn.classList.add('tested');
 document.getElementById('os-stage').innerHTML=
  '<div class="os-name">'+d.g+' '+d.n+'</div><p style="margin:5px 0 0">'+d.t+'</p>';
 if(osLab.tested.indexOf(k)<0){
  osLab.tested.push(k);
  var li=document.createElement('li');li.textContent=d.n+' \\u2014 '+d.t;
  document.getElementById('os-list').appendChild(li);
 }
 var done=osLab.tested.length;
 document.getElementById('os-note').textContent= done<3
  ? 'Tested '+done+' of three. Each result stays on the list so you can compare them.'
  : 'All three are frozen on the list. Between the gain and the loss there is a concentration where the mass does not change \\u2014 that is the one that matches the inside of the cells, and it is what your own graph is looking for.';
}
function osGlitch(btn){
 document.getElementById('os-glitch-result').textContent=
  btn.dataset.fix==='1'
   ? 'Repaired. Sugar does not move into the potato. The membrane is partially permeable: it lets water through and holds sugar back. The mass changes because WATER moves, and it moves towards the more concentrated solution.'
   : 'Kept as it stands. Check it against your frozen list first: if sugar were moving in, what would you expect to happen in the strong sugar solution?';
}
"""

WIDGET = """<div class="oslab" id="oslab-W5L2">
<h3>\U0001F9EA Osmosis prediction lab</h3>
<p style="margin:0">The calculator above works out one percentage change from your own two masses. This lab is button-only, and it holds all three solutions side by side so you can see the pattern.</p>
<div class="os-step">Step 1 · Predict, before you test</div>
<p style="margin:0 0 5px">A potato piece goes into <b>strong sugar solution</b>. What happens to its mass?</p>
<div class="os-row os-predict">
<button class="os-btn i0" data-label="It gains mass" type="button" aria-pressed="false" onclick="osPredict(this)"><span class="os-glyph">▲</span>It gains mass</button>
<button class="os-btn i1" data-label="It stays the same" type="button" aria-pressed="false" onclick="osPredict(this)"><span class="os-glyph">◎</span>It stays the same</button>
<button class="os-btn i2" data-label="It loses mass" type="button" aria-pressed="false" onclick="osPredict(this)"><span class="os-glyph">✳</span>It loses mass</button>
</div>
<p class="os-say" id="os-say" aria-live="polite">Choose one. Say it, point to it, or press it. Nothing here is right or wrong yet.</p>
<div class="os-step">Step 2 · Test each solution</div>
<div class="os-row">
<button class="os-btn i0" data-i="0" type="button" onclick="osTest(this)"><span class="os-glyph">▲</span>Test pure water</button>
<button class="os-btn i1" data-i="1" type="button" onclick="osTest(this)"><span class="os-glyph">◎</span>Test matching concentration</button>
<button class="os-btn i2" data-i="2" type="button" onclick="osTest(this)"><span class="os-glyph">✳</span>Test strong sugar</button>
</div>
<div class="os-stage" id="os-stage" aria-live="polite">Press a solution to see which way the water moves.</div>
<div class="os-frozen"><b>Frozen results — these stay on the page</b>
<ol id="os-list"></ol>
<p style="margin:6px 0 0" id="os-note" aria-live="polite">Nothing tested yet.</p></div>
<div class="os-step">Step 3 · Explain</div>
<div class="os-glitch"><b>SCIENCE GLITCH:</b> “The potato gains mass because sugar moves into it.”
<div class="os-row" style="margin-top:7px">
<button class="os-btn i0" data-fix="0" type="button" onclick="osGlitch(this)">Keep the claim</button>
<button class="os-btn i1" data-fix="1" type="button" onclick="osGlitch(this)">Repair it</button>
</div>
<p class="os-say" id="os-glitch-result" aria-live="polite">Use your frozen list as the evidence. Decide, then say why.</p></div>
<p class="os-foot">Every step is a button, and each solution carries a shape and a word as well as its colour. Say it, point to it or have an adult press it — the route does not change the Biology. The percentages are typical values for comparison; your own results are the ones that count.</p>
</div>"""


def main():
    s = open(P, encoding="utf-8").read()
    assert "oslab-W5L2" not in s, "specimen already present"

    guard = dict(
        closure=len(re.findall(r'What I said, and what it changed', s)),
        close=re.search(CLOSE_BLOCK, s, re.S).group(0),
        witness=re.search(r'<div id="print-witness".*?(?=</div>\s*</div>\s*<script|$)',
                          s, re.S).group(0),
        printpack=re.search(r'<div class="printpack">.*?(?=<script)', s, re.S).group(0),
        tiers=tuple(len(re.findall(t, s)) for t in ("Supported", "Standard", "Stretch")),
    )

    anchor = ('<button style="margin-top:8px" onclick="calcMag(\'W5L2\',\'pct\')">'
              'Calculate % change</button><p class="note">Percentage change = '
              '(final − initial) ÷ initial × 100.</p></div>')
    assert s.count(anchor) == 1, "We Do 2 anchor not unique"
    s = s.replace(anchor, anchor + WIDGET, 1)
    s = s.replace("</style>", CSS + "</style>", 1)
    i = s.rfind("</script>")
    s = s[:i] + JS + s[i:]

    assert len(re.findall(r'What I said, and what it changed', s)) == guard["closure"] == 2
    assert re.search(CLOSE_BLOCK, s, re.S).group(0) == guard["close"], "close block altered"
    assert re.search(r'<div id="print-witness".*?(?=</div>\s*</div>\s*<script|$)',
                     s, re.S).group(0) == guard["witness"], "witness altered"
    assert re.search(r'<div class="printpack">.*?(?=<script)', s, re.S).group(0) \
        == guard["printpack"], "print pack altered"
    assert tuple(len(re.findall(t, s)) for t in ("Supported", "Standard", "Stretch")) \
        == guard["tiers"], "tier counts changed"
    assert not re.search(r'matchMedia|localStorage|fetch\(|<form', s), "prohibited API"

    open(P, "w", encoding="utf-8").write(s)
    print("A6 specimen installed in SCI_L_W5L2_Osmosis_Core_Practical_Explore.html")
    print("  closure, close block, witness, print pack and tiers all asserted unchanged")


if __name__ == "__main__":
    main()
