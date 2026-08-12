#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LSG-1C A6 — the remaining fourteen We Do labs, one per lesson.

Approved pattern = the W5L2 specimen (la6.py), signed off by Matt 2026-08-12:
predict-commit -> test -> freeze -> explain. Button-only. Identity by
border-pattern + glyph + word, never colour alone. Zero media-API queries,
zero storage, zero network, no declared motion (RM STATIC). Print pack,
witness block, the written closure line and (W6L1) the word bank all asserted
byte-identical BEFORE the write, per transplant.

Class family: `.sclab` / `.sc-*` — one lab per file, so ids and function names
repeat safely across files and never inside one. W5L2 keeps its own `.oslab`.

Design references: the REBUILT INPUT-2 pack's science-labs/ (sums 85/85 OK).
Mechanisms consulted; NO pack markup bytes are copied — every lab below is
hand-written. Computing labs port the matching rule from lab-logic.mjs and run
their fixture subset at load as in-lab gate assertions: a failure REPLACES the
lab with a visible notice and throws (never a silent bare catch — see the
temporal-dead-zone history in CLAUDE.md). All function/var declarations are
`function`/`var`, defined before first use, called only via onclick or after
definition at the bottom of the file's single JS block.

Earn-the-place is stated per lab in LABS[...]["earn"], derived from the live
widget's markup, not assumed (the GSG-1 W7A/W7B precedent).
"""
import re, os, sys, json

REPO = "/home/user/Lessons"
DIR = os.path.join(REPO, "Science_Teesside/Launch/v3_40min")
CLOSE_BLOCK = r'<div class="close">.*?(?:<div class="pline"[^>]*></div>){2}</div>'

GROW_BLEED = r'\bfriction\b|\blevers?\b|\bpulleys?\b|\bgears?\b|\bMoon\b|\bplanets?\b|surface[- ]test'
FOOD = (r"chocolate|sweets?|biscuit|crisps|sugary|takeaway|junk food|"
        r"fizzy drink|calorie|diet plan|weight loss|slimming|BMI|"
        r"healthy weight|obes|fat kid|treat food")

CSS_TMPL = """
/* ===== LSG-1C A6: %(id)s %(name)s ===== */
.sclab{border:2px solid #7A5C9E;border-radius:14px;padding:12px 14px;background:#faf8fd;margin:10px 0}
.sclab h3{margin:0 0 4px;color:#4b3b6b}
.sc-step{font-weight:800;color:#2b2140;margin:9px 0 4px;font-size:.95rem}
.sc-row{display:flex;gap:8px;flex-wrap:wrap}
.sc-btn{background:#fff;color:#2b2140;border:3px solid #94a3b8;border-radius:10px;padding:9px 13px;font-weight:800;font-size:.95rem;cursor:pointer;display:flex;align-items:center;gap:7px;box-shadow:none}
.sc-btn .sc-glyph{font-size:1.15rem}
.sc-btn.i0{border-style:solid}.sc-btn.i1{border-style:dashed}.sc-btn.i2{border-style:dotted}
.sc-btn.picked{border-color:#7A5C9E;background:#ece6f7;color:#2b2140}
.sc-btn.tested{border-color:#2b2140;background:#eef2f7;color:#2b2140}
.sc-say{margin:7px 0 0;font-size:.92rem;color:#334155;font-weight:700}
.sc-stage{border:2px solid #cbd5e1;border-radius:12px;background:#fff;padding:11px;margin:8px 0;min-height:62px}
.sc-stage .sc-name{font-weight:800;font-size:1.05rem;color:#2b2140}
.sc-frozen{border-left:6px solid #2b2140;background:#f8fafc;border-radius:10px;padding:9px 11px;margin:8px 0;font-size:.9rem}
.sc-frozen ol{margin:5px 0 0 18px;padding:0}
.sc-frozen li{margin:3px 0}
.sc-glitch{border:2px solid #b55f25;background:#fff4e6;border-radius:12px;padding:10px 12px;margin:9px 0}
.sc-glitch b{color:#9a3412}
.sc-foot{font-size:.84rem;color:#64748b;margin:8px 0 0}
@media print{.sclab{display:none}}
"""

GLYPHS = ["▲", "◎", "✳"]  # ▲ ◎ ✳ — shape + word + border, never colour alone

FOOT_STD = ("Every step is a button, and each option carries a shape and a word "
            "as well as its colour. Say it, point to it or have an adult press "
            "it — the route does not change the Biology.")


def markup(L):
    pb = "\n".join(
        '<button class="sc-btn i%d" data-label="%s" type="button" aria-pressed="false" '
        'onclick="scPredict(this)"><span class="sc-glyph">%s</span>%s</button>'
        % (i, o, GLYPHS[i], o) for i, o in enumerate(L["predict_opts"]))
    tb = "\n".join(
        '<button class="sc-btn i%d" data-i="%d" type="button" onclick="scTest(this)">'
        '<span class="sc-glyph">%s</span>%s</button>'
        % (i, i, GLYPHS[i], o) for i, o in enumerate(L["test_btns"]))
    return """<div class="sclab" id="sclab-%(id)s">
<h3>%(emoji)s %(title)s</h3>
<p style="margin:0">%(intro)s</p>
<div class="sc-step">Step 1 · Predict, before you test</div>
<p style="margin:0 0 5px">%(pq)s</p>
<div class="sc-row sc-predict">
%(pb)s
</div>
<p class="sc-say" id="sc-say" aria-live="polite">Choose one. Say it, point to it, or press it. Nothing here is right or wrong yet.</p>
<div class="sc-step">Step 2 · %(step2)s</div>
<div class="sc-row">
%(tb)s
</div>
<div class="sc-stage" id="sc-stage" aria-live="polite">%(stagehint)s</div>
<div class="sc-frozen"><b>Frozen results — these stay on the page</b>
<ol id="sc-list"></ol>
<p style="margin:6px 0 0" id="sc-note" aria-live="polite">Nothing tested yet.</p></div>
<div class="sc-step">Step 3 · Explain</div>
<div class="sc-glitch"><b>SCIENCE GLITCH:</b> “%(claim)s”
<div class="sc-row" style="margin-top:7px">
<button class="sc-btn i0" data-fix="0" type="button" onclick="scGlitch(this)">Keep the claim</button>
<button class="sc-btn i1" data-fix="1" type="button" onclick="scGlitch(this)">Repair it</button>
</div>
<p class="sc-say" id="sc-glitch-result" aria-live="polite">Use your frozen list as the evidence. Decide, then say why.</p></div>
<p class="sc-foot">%(foot)s</p>
</div>""" % dict(L, pb=pb, tb=tb,
                 foot=L.get("foot", FOOT_STD),
                 stagehint=L.get("stagehint", "Press one to test it."))


def js(L):
    return """
/* ===== LSG-1C A6: %(id)s %(name)s =====
   predict-commit -> test -> freeze -> explain. The prediction is received and
   never marked; the pupil finds out by testing. Nothing is stored, scored or
   counted, and this layer queries no media API. */
%(extra)s
var scLab={tested:[]};
var scData=%(data)s;
function scPredict(btn){
 var box=document.getElementById('sclab-%(id)s');
 var all=box.querySelectorAll('.sc-predict .sc-btn');
 for(var i=0;i<all.length;i++){all[i].classList.remove('picked');all[i].setAttribute('aria-pressed','false')}
 btn.classList.add('picked');btn.setAttribute('aria-pressed','true');
 document.getElementById('sc-say').textContent=
  'Prediction received: '+btn.dataset.label+'. Nothing is marked. Test all three and find out.';
}
function scTest(btn){
 var k=Number(btn.dataset.i),d=scData[k];
 btn.classList.add('tested');
 document.getElementById('sc-stage').innerHTML=
  '<div class="sc-name">'+d.g+' '+d.n+'</div><p style="margin:5px 0 0">'+d.t+'</p>';
 if(scLab.tested.indexOf(k)<0){
  scLab.tested.push(k);
  var li=document.createElement('li');li.textContent=d.n+' \\u2014 '+d.t;
  document.getElementById('sc-list').appendChild(li);
 }
 var done=scLab.tested.length;
 document.getElementById('sc-note').textContent= done<3
  ? 'Tested '+done+' of three. Each result stays on the list so you can compare them.'
  : %(note3)s;
}
function scGlitch(btn){
 document.getElementById('sc-glitch-result').textContent=
  btn.dataset.fix==='1' ? %(repair)s : %(keep)s;
}
%(fixjs)s""" % dict(L,
                    extra=L.get("extra_js", ""),
                    data=L["data_js"],
                    note3=json.dumps(L["note3"]),
                    repair=json.dumps("Repaired. " + L["repair"]),
                    keep=json.dumps("Kept as it stands. " + L["keep"]),
                    fixjs=fixture_js(L))


def fixture_js(L):
    if "fixtures" not in L:
        return ""
    checks = ",\n  ".join(L["fixtures"])
    return """
function scFixGate(){
 /* in-lab gate assertions: the ported rule must reproduce its fixture file.
    A failure is VISIBLE (lab replaced + thrown), never swallowed. */
 var t=[
  %s
 ];
 var n=0,i;for(i=0;i<t.length;i++)if(t[i])n++;
 var box=document.getElementById('sclab-%s');
 box.setAttribute('data-fixtures',n+'/'+t.length);
 if(n<t.length){
  box.innerHTML='<p class="sc-say">This lab failed its own formula check ('+n+'/'+t.length+'). Tell your teacher \\u2014 the rest of the lesson is unaffected.</p>';
  throw new Error('%s lab fixtures failed: '+n+'/'+t.length);
 }
}
scFixGate();
""" % (checks, L["id"], L["id"])


# ---------------------------------------------------------------------------
# The fourteen labs. "earn" = derived from the live widget's markup.
# ---------------------------------------------------------------------------
LABS = {}

LABS["W3L1"] = dict(
    id="W3L1", file="SCI_L_W3L1_Microscopy_Introduce.html",
    name="microscope lens lab", emoji="\U0001F52C", title="Microscope lens lab",
    earn=("Live We Do widget = one 'Reveal model meaning' button (setLab): no lens "
          "comparison, no prediction, no frozen record. The LO's magnification-vs-"
          "resolution split only shows ACROSS lenses. Lab earns its place."),
    intro=("The model above reveals one explanation. This lab is button-only. It "
           "compares three lenses on the same onion cells, so you can see what "
           "magnification changes — and what it cannot."),
    pq="You switch from the ×4 lens to the ×40 lens. What do you see?",
    predict_opts=["Bigger and always sharper", "Bigger, but detail has a limit", "No change"],
    step2="Test each lens", test_btns=["Test ×4 lens", "Test ×10 lens", "Test ×40 lens"],
    stagehint="Press a lens to see the same cells through it.",
    data_js="""[
 {g:'\\u25B2',n:'\\u00d74 objective',
  t:'Total magnification \\u00d740 (eyepiece \\u00d710 \\u00d7 objective \\u00d74). Many whole cells, a wide view. Good for finding the specimen.'},
 {g:'\\u25CE',n:'\\u00d710 objective',
  t:'Total magnification \\u00d7100. Fewer cells, each one larger. The cell wall lines are clear.'},
 {g:'\\u2733',n:'\\u00d740 objective',
  t:'Total magnification \\u00d7400. One cell almost fills the view. It is bigger \\u2014 but how much detail you see is set by resolution, not by more magnification.'}
]""",
    note3=("All three are frozen on the list. Magnification makes the image bigger. "
           "Resolution decides how much detail the image can hold. A light microscope "
           "runs out of resolution before it runs out of magnification."),
    claim="More magnification always shows more detail.",
    repair=("Magnification makes the image bigger. Resolution is the power to show two "
            "close points as separate. Past the resolution limit, more magnification "
            "just makes a bigger blur."),
    keep="Check the frozen ×40 result: the image is bigger — did the detail keep up with it?",
)

LABS["W3L2"] = dict(
    id="W3L2", file="SCI_L_W3L2_Calculating_Magnification_Explore.html",
    name="unit bridge lab", emoji="\U0001F4CF", title="Unit bridge lab",
    earn=("Live We Do widget = a bare two-input calculator (calcMag 'Image ÷ actual'): "
          "no unit work at all, and the LO is 'using consistent units'. The unit "
          "bridge is exactly what the widget lacks. Lab earns its place."),
    intro=("The calculator above divides your two numbers. This lab is button-only. "
           "It shows the unit step that must happen first — and every number on it "
           "is worked out live by the same rule you use on paper."),
    pq="1 mm is the same length as how many micrometres (µm)?",
    predict_opts=["1000 µm", "100 µm", "10 µm"],
    step2="Test each working",
    test_btns=["Convert 36 mm", "Magnify: 50 mm over 50 µm", "Convert 90 µm"],
    extra_js="""var scUM={mm:1000,um:1};
function scConv(v,f,t){var x=Number(v);if(!isFinite(x)||!(f in scUM)||!(t in scUM))return NaN;return x*scUM[f]/scUM[t]}
function scMag(img,act){var i=Number(img),a=Number(act);if(!(i>0)||!(a>0))return NaN;return i/a}""",
    data_js="""[
 {g:'\\u25B2',n:'Convert 36 mm',
  t:'36 mm \\u00d7 1000 = '+scConv(36,'mm','um')+' \\u00b5m. Same length \\u2014 the unit is smaller, so the number is bigger.'},
 {g:'\\u25CE',n:'Image 50 mm, actual 50 \\u00b5m',
  t:'Match units first: 50 mm = '+scConv(50,'mm','um')+' \\u00b5m. Then '+scConv(50,'mm','um')+' \\u00f7 50 = \\u00d7'+scMag(scConv(50,'mm','um'),50)+'. Magnification has no unit.'},
 {g:'\\u2733',n:'Convert 90 \\u00b5m',
  t:'90 \\u00f7 1000 = '+scConv(90,'um','mm')+' mm. Same length \\u2014 the unit is bigger, so the number is smaller.'}
]""",
    note3=("All three are frozen. The rule is one line: make the units match, then "
           "divide image by actual. The bridge is ×1000 from mm to µm, and ÷1000 back."),
    claim="50 mm ÷ 50 µm = ×1, because 50 ÷ 50 = 1.",
    repair=("The units did not match, so the division was not fair. 50 mm is 50,000 µm. "
            "50,000 ÷ 50 = ×1000. Match the units first, every time."),
    keep="Check the frozen middle result: what happened to 50 mm before it was divided?",
    fixtures=["scConv(36,'mm','um')===36000",
              "scConv(90,'um','mm')===0.09",
              "scMag(2000,20)===100"],
    fixture_names=["36 mm converts to 36,000 µm", "90 µm converts to 0.09 mm",
                   "magnification = image / actual"],
)

LABS["W3L3"] = dict(
    id="W3L3", file="SCI_L_W3L3_Magnification_Lab_Do.html",
    name="working check lab", emoji="\U0001F50E", title="Working check lab",
    earn=("Live We Do widget = the same bare calculator as W3L2 — the GSG-1 "
          "byte-identical-widget precedent, so the LO decides: W3L3's LO is "
          "'independently solve AND CHECK... communicate my method'. Checking a "
          "working and naming its error type is absent from the widget. Distinct "
          "lab from W3L2's (bridge vs diagnosis). Lab earns its place."),
    intro=("The calculator above gives one answer. This lab is button-only. Three "
           "pupils answered the same question — image 40 mm wide, actual size 80 µm "
           "— and a checker built from the class rule diagnoses each answer live."),
    pq="Which answer is right?",
    predict_opts=["×500", "×0.5", "×5000"],
    step2="Test each answer",
    test_btns=["Check ×500", "Check ×0.5", "Check ×5000"],
    extra_js="""var scUM={mm:1000,um:1};
function scConv(v,f,t){var x=Number(v);if(!isFinite(x)||!(f in scUM)||!(t in scUM))return NaN;return x*scUM[f]/scUM[t]}
function scMag(img,act){var i=Number(img),a=Number(act);if(!(i>0)||!(a>0))return NaN;return i/a}
function scDiag(iv,iu,av,au,ans){
 var iU=scConv(iv,iu,'um'),aU=scConv(av,au,'um'),exp=scMag(iU,aU),g=Number(ans);
 if(!(isFinite(iU)&&isFinite(aU)&&isFinite(exp)&&isFinite(g)))return{type:'missing',msg:'Enter valid positive values and an answer.'};
 var r=g/exp;
 if(Math.abs(r-1)<=.015)return{type:'correct',msg:'The relationship, units and arithmetic are consistent.'};
 var direct=scMag(Number(iv),Number(av));
 if(isFinite(direct)&&Math.abs(g/direct-1)<=.015&&iu!==au)return{type:'unit',msg:'The lengths were divided before their units matched.'};
 var rev=scMag(aU,iU);
 if(Math.abs(g/rev-1)<=.015)return{type:'rearrangement',msg:'The image-size and actual-size relationship has been reversed.'};
 var pows=[10,100,1000,.1,.01,.001],p;
 for(p=0;p<pows.length;p++)if(Math.abs(r-pows[p])<=.02*Math.max(1,Math.abs(pows[p])))return{type:'unit',msg:'The answer differs by a power of ten. Check the mm \\u2194 \\u00b5m conversion.'};
 return{type:'arithmetic',msg:'The unit route and relationship may be right; recheck substitution and arithmetic.'};
}""",
    data_js="""[
 {g:'\\u25B2',n:'\\u00d7500',
  t:'CORRECT. 40 mm = '+scConv(40,'mm','um')+' \\u00b5m. '+scConv(40,'mm','um')+' \\u00f7 80 = \\u00d7'+scMag(scConv(40,'mm','um'),80)+'. The checker says: '+scDiag(40,'mm',80,'um',500).msg},
 {g:'\\u25CE',n:'\\u00d70.5',
  t:'UNIT ERROR. 40 was divided by 80 before the units matched. The checker says: '+scDiag(40,'mm',80,'um',0.5).msg},
 {g:'\\u2733',n:'\\u00d75000',
  t:'TEN-TIMES ERROR. The checker says: '+scDiag(40,'mm',80,'um',5000).msg}
]""",
    note3=("All three are frozen. Checking is a method, not a feeling: match the "
           "units, divide image by actual, then ask whether the size of the answer "
           "makes sense."),
    claim="Magnification has no unit, so units do not matter.",
    repair=("The ANSWER has no unit — but the two lengths must share a unit before "
            "you divide. No unit on the answer is earned by matching units in the working."),
    keep="Check the frozen ×0.5 result: where exactly did that working go wrong?",
    fixtures=["scDiag(40,'mm',80,'um',500).type==='correct'",
              "scDiag(40,'mm',80,'um',0.5).type==='unit'",
              "scMag(40000,80)===500"],
    fixture_names=["magnification diagnostic accepts correct fixture",
                   "magnification diagnostic identifies direct mixed-unit division",
                   "magnification = image / actual"],
)

LABS["W4L1"] = dict(
    id="W4L1", file="SCI_L_W4L1_Diffusion_Introduce.html",
    name="diffusion rate lab", emoji="\U0001FAE7", title="Diffusion rate lab",
    earn=("Live We Do widget = one 'Reveal model meaning' button: no factor "
          "comparison, and the LO names 'factors affecting rate'. One-factor-at-a-"
          "time testing is the missing mechanism. Lab earns its place."),
    intro=("The model above reveals one explanation. This lab is button-only. It "
           "changes one factor at a time and works out a rate index live, so you can "
           "see which change speeds diffusion up."),
    pq=("Which change speeds up diffusion the most here: doubling the concentration "
        "difference, a little warming, or doubling the distance?"),
    predict_opts=["Doubling the difference", "A little warming", "Doubling the distance"],
    step2="Test one factor at a time",
    test_btns=["Double the difference", "Warm it up", "Double the distance"],
    extra_js="""function scRate(o){
 o=o||{};
 var g=Math.max(0,Number(o.gradient!==undefined?o.gradient:1));
 var t=Math.max(.1,Number(o.temperature!==undefined?o.temperature:1));
 var d=Math.max(.1,Number(o.distance!==undefined?o.distance:1));
 var a=Math.max(.1,Number(o.area!==undefined?o.area:1));
 return (g*t*a)/d;
}""",
    data_js="""[
 {g:'\\u25B2',n:'Concentration difference doubled',
  t:'Rate index '+scRate({}).toFixed(1)+' \\u2192 '+scRate({gradient:2}).toFixed(1)+'. A steeper gradient means faster net movement.'},
 {g:'\\u25CE',n:'Temperature raised',
  t:'Rate index '+scRate({}).toFixed(1)+' \\u2192 '+scRate({temperature:1.5}).toFixed(1)+'. Warmer particles move faster, so they spread faster.'},
 {g:'\\u2733',n:'Distance doubled',
  t:'Rate index '+scRate({}).toFixed(1)+' \\u2192 '+scRate({distance:2}).toFixed(1)+'. A longer path slows net movement down.'}
]""",
    note3=("All three are frozen. Steeper gradient — faster. Warmer — faster. Longer "
           "distance — slower. Every exchange surface in Biology is built around "
           "these three."),
    claim="Particles move to where they are needed because the body tells them to.",
    repair=("Particles move at random and nobody tells them anything. There are more "
            "of them on the crowded side, so more happen to cross from there. That is "
            "why NET movement runs down the gradient."),
    keep="Check the frozen results: did any factor work by giving particles instructions?",
    fixtures=["scRate({gradient:2})>scRate({})",
              "scRate({temperature:2})>scRate({})",
              "scRate({distance:2})<scRate({})"],
    fixture_names=["diffusion index rises with gradient", "diffusion index rises with temperature",
                   "diffusion index falls with distance"],
)

LABS["W4L2"] = dict(
    id="W4L2", file="SCI_L_W4L2_Diffusion_Lungs_Explore.html",
    name="alveolus evidence lab", emoji="\U0001FAC1", title="Alveolus evidence lab",
    earn=("Live We Do widget = one 'Reveal model meaning' button: no feature-by-"
          "feature evidence, and the LO says 'use evidence to explain rapid gas "
          "exchange'. Feature-at-a-time testing with a live index is the missing "
          "evidence engine. Lab earns its place."),
    intro=("The model above reveals one explanation. This lab is button-only. It "
           "changes one alveolus feature at a time and works out an exchange index "
           "live, so the explanation is built from evidence."),
    pq="Which feature does most for FAST gas exchange in the alveolus?",
    predict_opts=["Huge surface area", "Very thin walls", "Rich blood supply"],
    step2="Test each feature",
    test_btns=["Double the surface area", "Halve the wall thickness", "Speed up the blood"],
    extra_js="""function scGx(o){
 o=o||{};
 var a=Math.max(.01,Number(o.area!==undefined?o.area:1));
 var th=Math.max(.1,Number(o.thickness!==undefined?o.thickness:1));
 var v=Math.max(.01,Number(o.ventilation!==undefined?o.ventilation:1));
 var b=Math.max(.01,Number(o.bloodFlow!==undefined?o.bloodFlow:1));
 return a*v*b/th;
}""",
    data_js="""[
 {g:'\\u25B2',n:'Surface area doubled',
  t:'Exchange index '+scGx({}).toFixed(1)+' \\u2192 '+scGx({area:2}).toFixed(1)+'. Millions of alveoli give more room for oxygen to cross at once.'},
 {g:'\\u25CE',n:'Wall thickness halved',
  t:'Exchange index '+scGx({}).toFixed(1)+' \\u2192 '+scGx({thickness:0.5}).toFixed(1)+'. One cell thick means a short diffusion path.'},
 {g:'\\u2733',n:'Blood flow doubled',
  t:'Exchange index '+scGx({}).toFixed(1)+' \\u2192 '+scGx({bloodFlow:2}).toFixed(1)+'. Fresh blood carries oxygen away, which keeps the gradient steep.'}
]""",
    note3=("All three are frozen — and each one multiplied the index. The alveolus "
           "does not pick one feature: it stacks surface area, a short path and a "
           "steep gradient together."),
    claim="Oxygen crosses into the blood because the lungs push it through the wall.",
    repair=("Nothing pushes it. Oxygen is more concentrated in the alveolus air than "
            "in the blood, so it diffuses down that gradient. Breathing and blood flow "
            "keep the gradient steep — that is their whole job."),
    keep="Which frozen result kept the GRADIENT steep, and why does that matter?",
    fixtures=["scGx({area:2})>scGx({})", "scGx({thickness:2})<scGx({})"],
    fixture_names=["gas exchange index rises with surface area",
                   "gas exchange index falls with wall thickness"],
)

LABS["W4L3"] = dict(
    id="W4L3", file="SCI_L_W4L3_Diffusion_Explanation_Do.html",
    name="explanation chain lab", emoji="\U0001F9F1", title="Explanation chain lab",
    earn=("Live We Do widget = a static command-word grid (four cards, no "
          "interaction beyond reading). The LO is 'construct... explanations "
          "linking direction, gradient and adaptations' — the widget names the "
          "shape but cannot rehearse the chain. Lab earns its place."),
    intro=("The decoder above shows what EXPLAIN demands. This lab is button-only. "
           "One question — explain why oxygen moves from the alveolus into the blood "
           "— and three candidate sentences, each frozen with what it contributes."),
    pq="Which sentence should an EXPLAIN answer be built around?",
    predict_opts=["The WHAT sentence", "The BECAUSE sentence", "The FEATURE sentence"],
    step2="Test each sentence",
    test_btns=["Test the WHAT sentence", "Test the BECAUSE sentence", "Test the FEATURE sentence"],
    data_js="""[
 {g:'\\u25B2',n:'\\u201cOxygen moves into the blood.\\u201d',
  t:'The WHAT sentence states the direction. On its own it only DESCRIBES. An explain answer needs it \\u2014 as the start, not the whole.'},
 {g:'\\u25CE',n:'\\u201c\\u2026because oxygen is more concentrated in the alveolus than in the blood.\\u201d',
  t:'The BECAUSE sentence carries the cause: net movement runs down that concentration gradient. This is the line that turns describing into explaining.'},
 {g:'\\u2733',n:'\\u201cAlveoli have very thin walls.\\u201d',
  t:'The FEATURE sentence adds the adaptation: a thin wall makes the diffusion path short. Link it with \\u201cso\\u201d and the chain is complete.'}
]""",
    note3=("All three are frozen. Chain them: WHAT happens → BECAUSE of the gradient "
           "→ SO the adaptation speeds it up. Direction, gradient, adaptation — that "
           "is the GCSE explain shape."),
    claim="The oxygen spreads out because it wants to reach the blood.",
    repair=("Particles do not want anything. Oxygen moves at random; net movement "
            "runs down the concentration gradient. Swap “wants to” for “because there "
            "are more oxygen molecules in the alveolus than in the blood”."),
    keep="Does any frozen sentence need a particle to make a choice?",
)

LABS["W5L1"] = dict(
    id="W5L1", file="SCI_L_W5L1_Osmosis_Introduce.html",
    name="membrane gate lab", emoji="\U0001F6AA", title="Membrane gate lab",
    earn=("Live We Do widget = one 'Reveal model meaning' button. The LO is 'define "
          "osmosis and explain how water movement depends on a partially permeable "
          "membrane' — the membrane's selectivity and the crossing counts are the "
          "definition's working parts, absent from the widget. The rebuilt INPUT-2 "
          "map closes the old W5L1 gap with membrane_reasoning_lab; distinct from "
          "the W5L2 specimen (no potato, no mass — membrane and net movement only). "
          "Lab earns its place."),
    intro=("The model above reveals one explanation. This lab is button-only. It "
           "counts water crossings through a partially permeable membrane in three "
           "set-ups, so the definition of osmosis comes from evidence, not from "
           "being told."),
    pq="A cell sits in PURE WATER. Which way is the net water movement?",
    predict_opts=["Into the cell", "No net movement", "Out of the cell"],
    step2="Test each set-up",
    test_btns=["Test pure water outside", "Test matching solution", "Test strong solution outside"],
    data_js="""[
 {g:'\\u25B2',n:'Pure water outside',
  t:'In one count: 9 water crossings in, 3 out \\u2014 net movement IN. The solute stayed put: its particles are too large for the membrane.'},
 {g:'\\u25CE',n:'Matching solution',
  t:'6 crossings in, 6 out \\u2014 NO net movement. Water still crosses both ways; the two directions cancel.'},
 {g:'\\u2733',n:'Strong solution outside',
  t:'3 in, 9 out \\u2014 net movement OUT, towards the more concentrated solution. The solute never crossed.'}
]""",
    note3=("All three are frozen. That is the definition, built from evidence: "
           "osmosis is the net movement of water across a partially permeable "
           "membrane, from dilute towards concentrated. The membrane lets water "
           "through and holds the solute back."),
    claim="The membrane lets everything through, so anything can cross.",
    repair=("Partially permeable means partly: small water molecules pass, larger "
            "solute particles do not. If everything crossed, both sides would even "
            "out with no net water movement — your frozen list says otherwise."),
    keep="In the frozen results, did the solute ever cross?",
    foot=(FOOT_STD + " The crossing counts are fixed example numbers, the same for "
          "every pupil."),
)

LABS["W5L3"] = dict(
    id="W5L3", file="SCI_L_W5L3_Osmosis_Data_Do.html",
    name="anomaly and zero lab", emoji="\U0001F4C9", title="Anomaly and zero lab",
    earn=("Live We Do widget = the plotting studio for the class's OWN five values: "
          "it graphs and shows a zero line, but holds no anomaly decision and no "
          "worked interpolation — and the LO says 'estimate the no-net-change "
          "concentration and evaluate method'. A fixed practice data set with a "
          "planted anomaly rehearses exactly the two missing moves, beside the "
          "widget that then takes the real data. Lab earns its place."),
    intro=("The studio above plots your own class results. This lab is button-only. "
           "It carries one fixed practice data set — the same numbers for every "
           "pupil, generated by a seeded rule ported from the fixture file — so "
           "anomaly decisions can be practised before you touch real data."),
    pq=("Somewhere between gaining and losing mass there is a concentration with NO "
        "change. In this data set, where will it sit?"),
    predict_opts=["Near 0.2 mol dm⁻³", "Near 0.5 mol dm⁻³", "Near 0.8 mol dm⁻³"],
    step2="Work the data set",
    test_btns=["Show the mean results", "Find the odd result", "Estimate zero change"],
    stagehint="Work left to right: means, then the odd result, then the estimate.",
    extra_js="""function scPct(a,b){var s=Number(a),e=Number(b);if(!(s>0)||!isFinite(e))return NaN;return((e-s)/s)*100}
function scMean(v){var c=[],i;for(i=0;i<v.length;i++){var x=Number(v[i]);if(isFinite(x))c.push(x)}
 if(!c.length)return NaN;var s=0;for(i=0;i<c.length;i++)s+=c[i];return s/c.length}
function scSeeded(seed){var st=(Number(seed)>>>0)||1;return function(){st=(1664525*st+1013904223)>>>0;return st/4294967296}}
function scOsmData(seed){
 /* seeded and deterministic ON PURPOSE: every pupil sees the same numbers */
 var rand=scSeeded(seed===undefined?20260812:seed);
 var cs=[0,0.2,0.4,0.6,0.8,1.0],out=[],r,i;
 for(r=0;r<cs.length;r++){
  var c=cs[r],bases=[3.04,3.08,3.02],initial=[],fin=[];
  for(i=0;i<3;i++)initial.push(bases[i]+(rand()-.5)*.08+r*.01+i*.005);
  var expected=15-c*31;
  for(i=0;i<3;i++){var pct=expected+(rand()-.5)*3.2;if(c===0.6&&i===2)pct+=8.5;fin.push(initial[i]*(1+pct/100))}
  var reps=[];
  for(i=0;i<3;i++)reps.push({initial:+initial[i].toFixed(2),final:+fin[i].toFixed(2),included:true,flagged:(c===0.6&&i===2)});
  out.push({concentration:c,repeats:reps});
 }
 return out;
}
function scZero(pts){
 var s=pts.slice().sort(function(a,b){return a.x-b.x}),i;
 for(i=0;i<s.length-1;i++){var a=s[i],b=s[i+1];
  if(a.y===0)return a.x;
  if((a.y>0&&b.y<0)||(a.y<0&&b.y>0))return a.x+(0-a.y)*(b.x-a.x)/(b.y-a.y)}
 return NaN; /* honest simplification vs the fixture module: no regression
                fallback is ported because this data always crosses zero */
}
function scRowPcts(row){var out=[],i;for(i=0;i<row.repeats.length;i++){var q=row.repeats[i];out.push(scPct(q.initial,q.final))}return out}
function scMeansText(excludeFlagged){
 var d=scOsmData(),bits=[],r;
 for(r=0;r<d.length;r++){
  var ps=scRowPcts(d[r]),use=[],i;
  for(i=0;i<ps.length;i++)if(!(excludeFlagged&&d[r].repeats[i].flagged))use.push(ps[i]);
  var m=scMean(use);
  bits.push(d[r].concentration.toFixed(1)+': '+(m>=0?'+':'')+m.toFixed(1)+'%');
 }
 return bits.join(' \\u00b7 ');
}
function scZeroEst(){
 var d=scOsmData(),pts=[],r;
 for(r=0;r<d.length;r++){
  var ps=scRowPcts(d[r]),use=[],i;
  for(i=0;i<ps.length;i++)if(!d[r].repeats[i].flagged)use.push(ps[i]);
  pts.push({x:d[r].concentration,y:scMean(use)});
 }
 return scZero(pts);
}
function scOddText(){
 var d=scOsmData(),row=d[3],ps=scRowPcts(row),all=scMean(ps),inc=scMean([ps[0],ps[1]]);
 return 'The 0.6 row hides a repeat far from its partners: '+ps.map(function(p){return (p>=0?'+':'')+p.toFixed(1)+'%'}).join(', ')+
  ' \\u2014 the third does not fit. It stays on the record and comes OUT of the mean. Excluded, the 0.6 mean moves from '+
  (all>=0?'+':'')+all.toFixed(1)+'% to '+(inc>=0?'+':'')+inc.toFixed(1)+'%.';
}""",
    data_js="""[
 {g:'\\u25B2',n:'Means from three repeats each',
  t:scMeansText(false)+'. Read along the line: gains shrink into losses as concentration rises. One value looks bent out of shape.'},
 {g:'\\u25CE',n:'The odd result',
  t:scOddText()},
 {g:'\\u2733',n:'Zero-change estimate',
  t:'Straight-line estimate between the last gain and the first loss: zero change near '+scZeroEst().toFixed(2)+' mol dm\\u207b\\u00b3. An estimate read from a pattern, not a magic answer.'}
]""",
    note3=("All three are frozen. Keep every raw value on the record, exclude the "
           "odd one from the mean and say why, then read the zero crossing from the "
           "pattern. Now do exactly this with your own class results in the studio "
           "above."),
    claim="An odd result should be rubbed out so the graph looks right.",
    repair=("An anomaly is kept on the record, excluded from the mean, and explained "
            "— maybe that piece was not dried before weighing. Deleting data is not "
            "evaluating; showing your decision is."),
    keep="If the odd repeat vanished, how would anyone check your decision?",
    foot=(FOOT_STD + " The practice numbers are seeded, so they are identical for "
          "every pupil; your own class data belongs in the studio above."),
    fixtures=["Math.abs(scPct(3.00,3.54)-18)<1e-9",
              "Math.abs(scPct(3.00,2.55)+15)<1e-9",
              "scMean([2,4,6])===4",
              "Math.abs(scZero([{x:0.4,y:2.6},{x:0.6,y:-3.6}])-0.48387096774193544)<1e-12",
              "JSON.stringify(scOsmData())===JSON.stringify(scOsmData())",
              "scOsmData()[3].repeats[2].flagged===true"],
    fixture_names=["positive percentage change", "negative percentage change",
                   "mean uses included values",
                   "zero interpolation between positive and negative points",
                   "deterministic osmosis data repeats exactly",
                   "deterministic dataset retains a flagged unusual repeat"],
)

LABS["W6L1"] = dict(
    id="W6L1", file="SCI_L_W6L1_Active_Transport_Introduce.html",
    name="against the gradient lab", emoji="\U0001F50B", title="Against the gradient lab",
    earn=("Live We Do widget = one 'Reveal model meaning' button. The LO is 'explain "
          "active transport as movement against a concentration gradient using "
          "energy from respiration' — the against-vs-down contrast and the energy "
          "bill are absent from the widget. (This file's word bank is protected "
          "byte-identical; the lab is separate markup.) Lab earns its place."),
    intro=("The model above reveals one explanation. This lab is button-only. It "
           "tests three real movements into and out of cells, and freezes which of "
           "them need energy."),
    pq=("Soil water holds LESS nitrate than a root cell already has. Can the root "
        "still take more nitrate in?"),
    predict_opts=["Yes — by spending energy", "No — never", "Only if the soil changes"],
    step2="Test each movement",
    test_btns=["Oxygen into blood", "Water into a root", "Nitrate into a root"],
    data_js="""[
 {g:'\\u25B2',n:'Oxygen into the blood',
  t:'DOWN its gradient, across the exchange surface, no energy needed. Diffusion.'},
 {g:'\\u25CE',n:'Water into a root hair',
  t:'Down its gradient, across a partially permeable membrane, no energy needed. Osmosis.'},
 {g:'\\u2733',n:'Nitrate into a root hair',
  t:'AGAINST its gradient \\u2014 from dilute soil into a richer cell. This cannot happen by chance. The cell pays with energy from respiration. Active transport.'}
]""",
    note3=("All three are frozen. Down the gradient is free. Against the gradient "
           "costs energy — and the energy comes from respiration. That is why cells "
           "doing active transport are packed with mitochondria."),
    claim="Active transport is free, because cells never run out of energy.",
    repair=("Active transport spends energy released by respiration. Starve a root "
            "of oxygen and its respiration slows — and so does its nitrate uptake. "
            "The bill is real, and the evidence shows it being paid."),
    keep="Which frozen movement stops when respiration stops?",
)

LABS["W6L2"] = dict(
    id="W6L2", file="SCI_L_W6L2_Root_Hairs_And_Gut_Explore.html",
    name="uptake evidence lab", emoji="\U0001F331", title="Uptake evidence lab",
    earn=("Live We Do widget = one 'Reveal model meaning' button. The LO is "
          "'interpret evidence linking uptake to respiration' — there is no "
          "evidence to interpret anywhere in the widget. Three testable pieces of "
          "evidence are the missing mechanism. Lab earns its place."),
    intro=("The model above reveals one explanation. This lab is button-only. It "
           "tests three pieces of evidence about a root hair cell, and freezes what "
           "each one proves."),
    pq=("Soil nitrate measures LOWER than nitrate inside the root hair cell. Can "
        "diffusion alone explain the root taking nitrate in?"),
    predict_opts=["Yes — easily", "No — something must pay", "The evidence cannot say"],
    step2="Test each piece of evidence",
    test_btns=["Test the concentrations", "Test the oxygen link", "Test the cell shape"],
    data_js="""[
 {g:'\\u25B2',n:'The concentrations',
  t:'Inside is already higher than the soil. Diffusion only nets INTO a cell down a gradient \\u2014 this gradient points the wrong way. Diffusion alone cannot explain the uptake.'},
 {g:'\\u25CE',n:'The oxygen link',
  t:'Drop the oxygen around the roots and mineral uptake falls with it. Less oxygen means less respiration, so less energy \\u2014 the uptake is being paid for. That is the active-transport signature.'},
 {g:'\\u2733',n:'The cell shape',
  t:'The long root hair adds surface area, so exchange is faster whatever the process. The gut villus plays the same trick. Shape speeds transport; it does not choose the direction.'}
]""",
    note3=("All three are frozen. The gradient rules out diffusion alone; the oxygen "
           "link shows energy being spent; the shape only speeds things up. Read "
           "together, the evidence says: active transport, powered by respiration — "
           "in the root hair, and for glucose in the gut when its gradient runs the "
           "wrong way too."),
    claim="Roots absorb minerals by diffusion, because soil is full of them.",
    repair=("The measurements say the soil is the DILUTE side. Movement into the "
            "richer cell runs against the gradient, so it needs active transport, "
            "paid for by respiration. Evidence beats a story every time."),
    keep="Check the frozen concentrations: which side was richer?",
)

LABS["W6L3"] = dict(
    id="W6L3", file="SCI_L_W6L3_Compare_Transport_Do.html",
    name="transport decision lab", emoji="⚖️", title="Transport decision lab",
    earn=("Live We Do widget = one 'Reveal model meaning' button. The LO is 'choose "
          "the correct process from evidence' in unfamiliar cases — the widget "
          "holds no scenario and no decision rule. Lab earns its place; the "
          "decision rule is ported and runs live."),
    intro=("The model above reveals one explanation. This lab is button-only. Three "
           "unfamiliar scenarios: for each one the evidence is read, and a ported "
           "decision rule names the process live."),
    pq="Which single clue settles the process fastest?",
    predict_opts=["What the substance is", "Which way it moves", "Whether energy is spent"],
    step2="Test each scenario",
    test_btns=["Seaweed and iodide", "Muscle and carbon dioxide", "Raisin in water"],
    extra_js="""function scClassify(o){
 var s=String(o.substance||'').toLowerCase(),d=String(o.direction||'').toLowerCase();
 var m=Boolean(o.membrane),e=Boolean(o.energy);
 if(s==='water'&&m&&d==='down')return 'osmosis';
 if(d==='against'&&e)return 'active transport';
 if(d==='down'&&!e)return 'diffusion';
 return 'insufficient evidence';
}""",
    data_js="""[
 {g:'\\u25B2',n:'Seaweed hoards iodide',
  t:'Iodide moves into the cells AGAINST a huge gradient, and energy is spent. The rule says: '+scClassify({substance:'iodide',direction:'against',membrane:true,energy:true}).toUpperCase()+'.'},
 {g:'\\u25CE',n:'Carbon dioxide leaves a muscle',
  t:'A working muscle makes carbon dioxide, so it is high inside and low in the blood. It crosses down the gradient, no energy spent. The rule says: '+scClassify({substance:'carbon dioxide',direction:'down',membrane:true,energy:false}).toUpperCase()+'.'},
 {g:'\\u2733',n:'A raisin swells in water',
  t:'Water crosses the raisin\\u2019s membrane towards the concentrated inside, down its own gradient, no energy spent. Water + membrane + down. The rule says: '+scClassify({substance:'water',direction:'down',membrane:true,energy:false}).toUpperCase()+'.'}
]""",
    note3=("All three are frozen. The decision is a route, not a guess: water "
           "crossing a membrane? Osmosis. Against the gradient with energy spent? "
           "Active transport. Down the gradient for free? Diffusion."),
    claim="If a substance crosses a membrane, that is osmosis.",
    repair=("Osmosis is the net movement of WATER across a partially permeable "
            "membrane. Carbon dioxide crossed a membrane in your frozen list and the "
            "rule still said diffusion. The substance, direction and energy decide — "
            "not the membrane alone."),
    keep="Check the frozen muscle result: a membrane was crossed. What did the rule say?",
    fixtures=["scClassify({substance:'carbon dioxide',direction:'down',membrane:true,energy:false})==='diffusion'",
              "scClassify({substance:'water',direction:'down',membrane:true,energy:false})==='osmosis'",
              "scClassify({substance:'iodide',direction:'against',membrane:true,energy:true})==='active transport'"],
    fixture_names=["transport classification: diffusion", "transport classification: osmosis",
                   "transport classification: active transport"],
)

LABS["W7L1"] = dict(
    id="W7L1", file="SCI_L_W7L1_Topic_1_Round_Up_Introduce.html",
    name="connection lab", emoji="\U0001F517", title="Connection lab",
    earn=("Live We Do widget = the retrieval map: four click-to-reveal definition "
          "cards. It covers 'retrieve'; the LO also says 'CONNECT the key "
          "concepts', and no link between any two cards exists in the widget. The "
          "lab tests the links; the map keeps the definitions. Lab earns its place."),
    intro=("The map above checks single ideas one at a time. This lab is "
           "button-only. It tests the LINKS between the ideas — the connections are "
           "where Topic 1 questions live."),
    pq="Which pair of Topic 1 ideas is most tightly linked?",
    predict_opts=["Diffusion and osmosis", "Osmosis and the core practical",
                  "Active transport and respiration"],
    step2="Test each connection",
    test_btns=["Diffusion ↔ osmosis", "Osmosis ↔ core practical",
               "Active transport ↔ respiration"],
    data_js="""[
 {g:'\\u25B2',n:'Diffusion \\u2194 osmosis',
  t:'Both passive, both net movement down a gradient. The difference that earns the answer: osmosis is water only, across a partially permeable membrane.'},
 {g:'\\u25CE',n:'Osmosis \\u2194 the core practical',
  t:'Percentage change in mass IS the osmosis evidence: gain in dilute solution, loss in concentrated, zero at the matching concentration.'},
 {g:'\\u2733',n:'Active transport \\u2194 respiration',
  t:'Against-the-gradient movement is paid for by energy from respiration. No respiration, no active transport \\u2014 which is why the two are tested together.'}
]""",
    note3=("All three are frozen. Retrieval opens the boxes; connection joins them. "
           "An answer that walks a link — idea, difference, evidence — says more "
           "than a list of definitions ever can."),
    claim="Osmosis is just diffusion, so one definition covers both.",
    repair=("They share “passive” and “down a gradient” — that is the link. But "
            "osmosis is the net movement of water across a partially permeable "
            "membrane. GCSE questions ask for the difference as often as the link."),
    keep=("Your frozen first connection lists a link AND a difference. Which half "
          "would this claim throw away?"),
)

LABS["W7L2"] = dict(
    id="W7L2", file="SCI_L_W7L2_Command_Words_Explore.html",
    name="answer shape lab", emoji="\U0001F5DD️", title="Answer shape lab",
    earn=("Live We Do widget = the command-word decoder: four static cards naming "
          "each word's demand. The LO is 'shape my Biology answer accordingly' — "
          "the widget never shows one piece of Biology changing shape under "
          "different words. That transformation is the lab. Lab earns its place."),
    intro=("The decoder above names the command words. This lab is button-only. It "
           "puts the SAME result — potato pieces lost mass in strong solution and "
           "gained mass in pure water — through three command words, so you can "
           "watch the answer change shape while the facts stay still."),
    pq="Which command word demands the word “because”?",
    predict_opts=["DESCRIBE", "EXPLAIN", "COMPARE"],
    step2="Test each command word",
    test_btns=["Shape a DESCRIBE answer", "Shape an EXPLAIN answer", "Shape a COMPARE answer"],
    data_js="""[
 {g:'\\u25B2',n:'DESCRIBE',
  t:'State the pattern, data in: \\u201cMass fell in the strong solution and rose in pure water.\\u201d No reason given \\u2014 none was asked for.'},
 {g:'\\u25CE',n:'EXPLAIN',
  t:'The pattern plus BECAUSE: \\u201c\\u2026because water moved out by osmosis, down its gradient, across the partially permeable membrane.\\u201d The cause is the point.'},
 {g:'\\u2733',n:'COMPARE',
  t:'Both sides, one balance word: \\u201cBoth pieces changed mass, whereas the direction differed \\u2014 loss in strong solution, gain in pure water.\\u201d Both + whereas.'}
]""",
    note3=("All three are frozen. Same potato, same data — three different answers. "
           "Read the command word first, pick the shape, then spend the Biology."),
    claim="A good fact earns credit whatever the command word says.",
    repair=("Your frozen list shows one fact wearing three shapes. A describe-shaped "
            "answer to an EXPLAIN question leaves the “because” unsaid — and the "
            "“because” was the question. The command word sets the shape."),
    keep="Check the frozen DESCRIBE and EXPLAIN results: same fact — same shape?",
)

LABS["W7L3"] = dict(
    id="W7L3", file="SCI_L_W7L3_Exam_Practice_Do.html",
    name="evidence paper lab", emoji="\U0001F4DD", title="Evidence paper lab",
    earn=("Live We Do widget = one 'Reveal model meaning' button. The LO is "
          "'independently apply Topic 1... and use feedback to improve one "
          "response' — the widget offers nothing to apply to and no feedback "
          "loop. Three GCSE-shaped items with frozen shape-checks, ending in a "
          "directed repair of the pupil's own written answer. These are teaching "
          "answer shapes; nothing official is claimed. Lab earns its place."),
    intro=("The model above reveals one explanation. This lab is button-only. Three "
           "GCSE-shaped items: commit to a shape first, then test each item and "
           "freeze its checklist. The last step sends you back to your own page."),
    pq="Item 1 asks you to CALCULATE. What must the answer show?",
    predict_opts=["Working and the answer", "The answer alone", "A definition"],
    step2="Test each item",
    test_btns=["Item 1 · Calculate", "Item 2 · Explain", "Item 3 · Compare"],
    data_js="""[
 {g:'\\u25B2',n:'Item 1 \\u00b7 Calculate',
  t:'An image is 30 mm wide; the real cell is 60 \\u00b5m wide. Shape check: convert (30 mm = 30,000 \\u00b5m), divide (30,000 \\u00f7 60), state (\\u00d7500). Working shown IS the shape \\u2014 an answer alone cannot be checked.'},
 {g:'\\u25CE',n:'Item 2 \\u00b7 Explain',
  t:'Why does a plant wilt in salty soil? Shape check: WHAT (water leaves the cells) + BECAUSE (net movement out by osmosis, towards the concentrated soil water) + SO (cells soften and the plant droops).'},
 {g:'\\u2733',n:'Item 3 \\u00b7 Compare',
  t:'Diffusion and active transport. Shape check: BOTH (move substances across membranes) + WHEREAS (diffusion runs down the gradient for free; active transport runs against it using energy from respiration).'}
]""",
    note3=("All three are frozen. Now the real work: pick ONE answer from your own "
           "page today, hold it against its frozen shape, and improve it in "
           "writing. One honest repair beats three new attempts."),
    claim="Once an answer is written, improving it is cheating.",
    repair=("Improving your own answer against a checklist is the whole skill this "
            "lesson practises. The record keeps both versions — first try and repair "
            "— and the repair is where the learning shows."),
    keep="Then what would feedback ever be for?",
)


# ---------------------------------------------------------------------------
def validate_scanners():
    grow = open(os.path.join(REPO, "Science_Teesside/Grow/v3_40min/"
                             "SCI_G_W3A_Friction_Explore.html"), encoding="utf-8").read()
    assert re.search(GROW_BLEED, grow, re.I), "GROW-bleed scanner failed its known positive (friction)"
    assert re.search(GROW_BLEED, "the Moon orbits", re.I), "GROW-bleed scanner failed on Moon"
    assert not re.search(GROW_BLEED, "surface area of the alveolus", re.I), \
        "GROW-bleed scanner must not hit 'surface area'"
    assert re.search(FOOD, "a bar of chocolate", re.I), "food scanner failed its known positive"


def apply(key):
    L = LABS[key]
    path = os.path.join(DIR, L["file"])
    s = open(path, encoding="utf-8").read()
    assert 'sclab-' + L["id"] not in s, "lab already present in " + L["file"]

    # protections captured BEFORE the write (the lab.py precedent)
    guard = dict(
        closure=len(re.findall(r'What I said, and what it changed', s)),
        close=re.search(CLOSE_BLOCK, s, re.S).group(0),
        witness=re.search(r'<div id="print-witness".*?(?=</div>\s*</div>\s*<script|$)',
                          s, re.S).group(0),
        printpack=re.search(r'<div class="printpack">.*?(?=<script)', s, re.S).group(0),
        tiers=tuple(len(re.findall(t, s)) for t in ("Supported", "Standard", "Stretch")),
        wordbank=len(re.findall(r'(?i)word[ -]?bank', s)),
        oak=len(re.findall(r'thenational\.academy', s)),
        bleed=len(re.findall(GROW_BLEED, s, re.I)),
        food=len(re.findall(FOOD, s, re.I)),
    )
    assert guard["closure"] == 2, "pre-state closure != 2"
    assert guard["bleed"] == 0, "pre-state GROW-bleed census not clean"
    assert guard["food"] == 0, "pre-state food census not clean"

    # insertion point: after the live widget, before its participation strip —
    # the same seat the W5L2 specimen occupies
    w = s.find('<div class="widget">')
    assert w >= 0, "no live widget found"
    p = s.find('<div class="participation">', w)
    assert p > w, "no participation strip after the widget"
    s = s[:p] + markup(L) + s[p:]
    s = s.replace("</style>", CSS_TMPL % L + "</style>", 1)
    i = s.rfind("</script>")
    s = s[:i] + js(L) + s[i:]

    # protections asserted AFTER, against the captured bytes
    assert len(re.findall(r'What I said, and what it changed', s)) == 2
    assert re.search(CLOSE_BLOCK, s, re.S).group(0) == guard["close"], "close block altered"
    assert re.search(r'<div id="print-witness".*?(?=</div>\s*</div>\s*<script|$)',
                     s, re.S).group(0) == guard["witness"], "witness altered"
    assert re.search(r'<div class="printpack">.*?(?=<script)', s, re.S).group(0) \
        == guard["printpack"], "print pack altered"
    assert tuple(len(re.findall(t, s)) for t in ("Supported", "Standard", "Stretch")) \
        == guard["tiers"], "tier counts changed"
    assert len(re.findall(r'(?i)word[ -]?bank', s)) == guard["wordbank"], "word bank changed"
    assert len(re.findall(r'thenational\.academy', s)) == guard["oak"], "Oak URL count changed"
    assert len(re.findall(GROW_BLEED, s, re.I)) == 0, "GROW-bleed census failed after transplant"
    assert len(re.findall(FOOD, s, re.I)) == 0, "food census failed after transplant"
    assert not re.search(r'matchMedia|localStorage|sessionStorage|fetch\(|<form|XMLHttpRequest',
                         s), "prohibited API in emitted file"
    assert "animation:" not in CSS_TMPL and "transition:" not in CSS_TMPL, "motion declared"

    open(path, "w", encoding="utf-8").write(s)
    nfix = len(L.get("fixtures", []))
    print("LSG-1C A6 %s installed in %s" % (L["id"], L["file"]))
    print("  earn-the-place: %s" % L["earn"])
    print("  in-lab fixture assertions: %d%s"
          % (nfix, "" if not nfix else " (" + "; ".join(L["fixture_names"]) + ")"))
    print("  closure, close block, witness, print pack, tiers, word bank, Oak count,")
    print("  GROW-bleed 0, food 0 — all asserted; no motion declared")


if __name__ == "__main__":
    validate_scanners()
    for k in sys.argv[1:]:
        apply(k)
