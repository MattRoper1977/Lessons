#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSG-1 CLOSE §2 — the remaining We Do labs, on the approved W4A pattern.

predict-commit -> test -> freeze -> explain. Button-only. Identity by
border-pattern + glyph + word, never colour alone. Zero matchMedia, zero
storage, zero network, no declared motion. Print pack, witness and tier
surfaces byte-untouched: the widget lands inside the We Do 2 slide only, and
the CSS hides it in print.

EARNING THE PLACE — derived per lesson from the live We Do widget against the
lesson's own LO, not assumed. W7A is deliberately NOT built: its live phase
explorer covers its LO ("explain why the Moon appears to change shape") exactly,
button-only, already judgement-free. W7B shares that byte-identical widget but
its LO also demands "distinguish phases from eclipses", which the widget never
mentions - so W7B has a real gap and W7A does not.

Nothing is copy-pasted from the pack. Its engines are a design reference only.
"""
import re, os, sys

LIVE = "/home/user/Lessons/Science_Teesside/Grow/v3_40min"

GLYPH = ["▲", "◎", "✳", "◆"]          # ▲ ◎ ✳ ◆
STYLE = ["solid", "dashed", "dotted", "double"]

CSS = """
/* ===== GSG-1 We Do lab (approved W4A pattern) ===== */
.gsglab{border:2px solid var(--grow);border-radius:14px;padding:12px 14px;background:#f7fcfa;margin:10px 0}
.gsglab h3{margin:0 0 4px;color:#215e53}
.gl-step{font-weight:900;color:#10233f;margin:9px 0 4px;font-size:.95rem}
.gl-row{display:flex;gap:8px;flex-wrap:wrap}
.gl-btn{background:#fff;color:#10233f;border:3px solid #94a3b8;border-radius:10px;padding:9px 13px;font-weight:900;font-size:.95rem;cursor:pointer;display:flex;align-items:center;gap:7px;box-shadow:none}
.gl-btn .gl-glyph{font-size:1.15rem}
.gl-btn.i0{border-style:solid}.gl-btn.i1{border-style:dashed}
.gl-btn.i2{border-style:dotted}.gl-btn.i3{border-style:double}
.gl-btn.picked{border-color:var(--grow);background:#dff2ea;color:#10233f}
.gl-btn.tested{border-color:#10233f;background:#eef2f7;color:#10233f}
.gl-say{margin:7px 0 0;font-size:.92rem;color:#334155;font-weight:700}
.gl-stage{border:2px solid #cbd5e1;border-radius:12px;background:#fff;padding:11px;margin:8px 0;min-height:62px}
.gl-stage .gl-name{font-weight:900;font-size:1.05rem;color:#10233f}
.gl-frozen{border-left:6px solid #10233f;background:#f8fafc;border-radius:10px;padding:9px 11px;margin:8px 0;font-size:.9rem}
.gl-frozen ol{margin:5px 0 0 18px;padding:0}
.gl-frozen li{margin:3px 0}
.gl-glitch{border:2px solid #b55f25;background:#fff4e6;border-radius:12px;padding:10px 12px;margin:9px 0}
.gl-glitch b{color:#9a3412}
.gl-foot{font-size:.84rem;color:#64748b;margin:8px 0 0}
@media print{.gsglab{display:none}}
"""

JS_TMPL = """
/* ===== GSG-1 We Do lab: %(code)s =====
   predict-commit -> test -> freeze -> explain. Nothing is marked, scored or
   stored. The prediction is received, never graded: the reveal comes from
   testing, which is the whole reason for predicting first. */
var gsgLab_%(code)s={tested:[],data:%(data)s};
function gsgLabPredict_%(code)s(btn){
 var box=document.getElementById('gsglab-%(code)s');
 var all=box.querySelectorAll('.gl-predict .gl-btn');
 for(var i=0;i<all.length;i++){all[i].classList.remove('picked');all[i].setAttribute('aria-pressed','false')}
 btn.classList.add('picked');btn.setAttribute('aria-pressed','true');
 document.getElementById('gl-say-%(code)s').textContent=
  'Prediction received: '+btn.dataset.label+'. Nothing is marked. Test them and find out.';
}
function gsgLabTest_%(code)s(btn){
 var k=Number(btn.dataset.i),d=gsgLab_%(code)s.data[k];
 btn.classList.add('tested');
 document.getElementById('gl-stage-%(code)s').innerHTML=
  '<div class="gl-name">'+d.g+' '+d.n+'</div><p style="margin:5px 0 0">'+d.t+'</p>';
 if(gsgLab_%(code)s.tested.indexOf(k)<0){
  gsgLab_%(code)s.tested.push(k);
  var li=document.createElement('li');li.textContent=d.n+' \\u2014 '+d.t;
  document.getElementById('gl-list-%(code)s').appendChild(li);
 }
 var done=gsgLab_%(code)s.tested.length,total=gsgLab_%(code)s.data.length;
 document.getElementById('gl-note-%(code)s').textContent= done<total
  ? 'Tested '+done+' of '+total+'. Each result stays on the list so you can compare them.'
  : %(alldone)s;
}
function gsgLabGlitch_%(code)s(btn){
 document.getElementById('gl-glitch-%(code)s').textContent=
  btn.dataset.fix==='1' ? %(repair)s : %(keep)s;
}
"""


def js_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


LABS = {}

LABS["W3A"] = dict(
    file="SCI_G_W3A_Friction_Explore.html",
    gap=("live Surface explorer shows one surface at a time and holds nothing; it "
         "never asks for a prediction and never touches the helpful/unhelpful "
         "judgement that is half the LO"),
    title="\U0001F9EA Grip Decision Lab",
    intro="The live explorer shows one surface at a time. This lab holds all three "
          "side by side so you can decide where friction helps and where it gets in the way.",
    q="Which surface will let the block travel <b>furthest</b>?",
    opts=["Rough", "Medium", "Smooth"],
    items=[
        ("Rough", "High friction. The block stops soonest. A designer ADDS this to a "
                  "stair tread, a shoe sole or a brake pad."),
        ("Medium", "Middling friction. The block travels further than on rough, less "
                   "than on smooth. Most everyday floors sit here."),
        ("Smooth", "Low friction. The block travels furthest. A designer CUTS friction "
                   "here for a slide, a drawer runner or a skate."),
    ],
    alldone="All three are frozen on the list. Now decide: name one place a designer "
            "would ADD friction, and one place they would cut it.",
    glitch="Friction is always a problem.",
    repair="Repaired. Friction is not good or bad on its own. The same force that slows "
           "a slide is what lets you walk, brake and hold a pencil. A designer adds it or "
           "cuts it depending on the job.",
    keep="Kept as it stands. Check it against your frozen list first: if friction were "
         "always a problem, what would happen when you tried to walk or stop?",
)

LABS["W3B"] = dict(
    file="SCI_G_W3B_Friction_Do.html",
    gap=("live Results interpreter is reachable ONLY by typing three numbers - there is "
         "no button route into it at all - and it asks for no prediction before the data"),
    title="\U0001F50E Surface Evidence Lab",
    intro="A button-only route into the same comparison, for anyone who cannot enter the "
          "numbers. The results interpreter above still takes your own measurements.",
    q="Which surface will grip the most?",
    opts=["Carpet", "Wood", "Smooth plastic"],
    items=[
        ("Carpet", "Three repeats: 21, 23, 22 cm. Short distances, close together. "
                   "High friction, and the repeats agree."),
        ("Wood", "Three repeats: 44, 45, 43 cm. Middling distances, close together. "
                 "Less friction than carpet."),
        ("Smooth plastic", "Three repeats: 68, 91, 70 cm. Long distances, but one "
                           "reading does not fit the other two."),
    ],
    alldone="All three are frozen on the list. Compare them: which surface gripped most, "
            "and which set of repeats would you want to run again before you trusted it?",
    glitch="One reading is enough to be sure.",
    repair="Repaired. One reading can be a fluke. Repeats show whether a result holds, and "
           "the odd plastic reading is exactly the kind of thing a single measurement hides.",
    keep="Kept as it stands. Look at the plastic repeats on your frozen list before you "
         "settle on that: which single reading would you have taken?",
)

LABS["W4B"] = dict(
    file="SCI_G_W4B_Mechanisms_Do.html",
    gap=("live Lever pivot explorer is a slider showing one position at a time and holds "
         "nothing; the LO is about using EVIDENCE from several pivot positions, which "
         "needs them held side by side"),
    title="\U0001F529 Pivot Evidence Lab",
    intro="The slider above shows one pivot position at a time. This lab freezes all three "
          "so you can use them as evidence.",
    q="Where should the pivot go for the <b>least effort</b>?",
    opts=["Near the load", "In the middle", "Near your hands"],
    items=[
        ("Near the load", "Least effort needed. But the effort end has to travel the "
                          "furthest to lift the load the same height."),
        ("In the middle", "Middling effort, middling distance. Effort and movement are "
                          "roughly balanced."),
        ("Near your hands", "Most effort needed. But the effort end barely moves to lift "
                            "the load the same height."),
    ],
    alldone="All three are frozen on the list. Now use them as evidence: state what you "
            "gain and what you pay for it as the pivot moves towards the load.",
    glitch="Moving the pivot gives you free extra force.",
    repair="Repaired. Nothing is free. Moving the pivot towards the load cuts the effort "
           "you need and charges you in distance moved. Your frozen list shows both halves "
           "of that trade.",
    keep="Kept as it stands. Check your frozen list first: when the effort got smaller, "
         "what happened to the distance?",
)

LABS["W5A"] = dict(
    file="SCI_G_W5A_Fair_Test_Explore.html",
    gap=("live Repair the method covers only the CHANGE arm - three checkboxes about what "
         "changes - while the LO names change, measure AND keep the same, and the unit "
         "is never asked for anywhere in the widget"),
    title="\U0001F4CF Measure and Unit Lab",
    intro="The repair tool above fixes what CHANGES. This lab does the other arm: what you "
          "will measure, and in what unit.",
    q="Our question is: does surface affect how far the trolley rolls? What should we "
      "<b>measure</b>?",
    opts=["Distance rolled", "Ramp height", "Time of day"],
    items=[
        ("Distance rolled", "Measured in centimetres (cm). It changes when the surface "
                            "changes, so it can answer our question. This is the dependent "
                            "variable."),
        ("Ramp height", "Measured in centimetres (cm). We decided to keep it the same, so "
                        "measuring it checks our control - it does not answer the question."),
        ("Time of day", "Measured in minutes. Nothing in our question depends on it, so "
                        "measuring it tells us nothing about surface."),
    ],
    alldone="All three are frozen on the list. Now say your plan in one line: I will change "
            "___, I will measure ___ in ___, and I will keep ___ the same.",
    glitch="A number on its own is enough to record.",
    repair="Repaired. A number with no unit means nothing - 45 could be centimetres, "
           "seconds or millimetres. Every measurement you record carries its unit.",
    keep="Kept as it stands. Test it: write 45 on the board and ask someone what it means.",
)

LABS["W5B"] = dict(
    file="SCI_G_W5B_Fair_Test_Do.html",
    gap=("live Repeat-and-mean lab is reachable ONLY by typing nine numbers - no button "
         "route exists - and it computes means without ever asking the pupil to JUDGE "
         "which set of repeats is trustworthy, which is the LO's 'decide what the data shows'"),
    title="\U0001F9ED Trust the Repeat Lab",
    intro="A button-only route into the judgement the mean cannot make for you. The tool "
          "above still calculates from your own nine readings.",
    q="Which set of three repeats would you <b>trust most</b>?",
    opts=["Set A", "Set B", "Set C"],
    items=[
        ("Set A", "62, 63, 62 cm. The repeats agree closely. The mean of 62.3 cm describes "
                  "all three readings well."),
        ("Set B", "58, 91, 60 cm. Two agree and one does not. The mean of 69.7 cm describes "
                  "none of the three readings. Investigate the odd one - do not delete it."),
        ("Set C", "40, 66, 88 cm. The repeats spread widely. A mean of 64.7 cm hides how "
                  "little the readings agree. Something in the method is not controlled."),
    ],
    alldone="All three are frozen on the list. Now decide what your own data shows: does "
            "your mean describe your repeats, or hide them?",
    glitch="Always delete a reading that does not fit.",
    repair="Repaired. An odd reading is information. Investigate it - was the release "
           "different, the surface rucked, the measurement misread? You may repeat it, and "
           "you say what you did. You never silently delete it.",
    keep="Kept as it stands. Ask yourself what Set B's odd reading might have been telling "
         "you about the method before you throw it away.",
)

LABS["W6A"] = dict(
    file="SCI_G_W6A_Earth_And_Planets_Explore.html",
    gap=("live Planet order challenge covers the ORDER arm thoroughly and is already "
         "button-only and non-scoring, but the LO also says 'explain gravity's role' and "
         "gravity appears nowhere in that widget"),
    title="\U0001F30C Gravity and Motion Lab",
    intro="The order challenge above covers where the planets are. This lab covers why they "
          "stay there.",
    q="If the Sun's gravity switched off, what would a planet do?",
    opts=["Fly off in a straight line", "Stop where it is", "Spiral into the Sun"],
    items=[
        ("Fly off in a straight line", "This is what would happen. A moving planet keeps "
                                       "moving in a straight line unless a force bends its "
                                       "path. Gravity is that force."),
        ("Stop where it is", "It would not stop. Nothing removes a planet's motion - there "
                             "is almost no friction in space to slow it down."),
        ("Spiral into the Sun", "It would not fall inward either. Falling towards the Sun "
                                "is what gravity does; take gravity away and nothing pulls "
                                "it in."),
    ],
    alldone="All three are frozen on the list. Now explain an orbit in one sentence using "
            "both parts: the planet's forward motion, and the Sun's gravity pulling inward.",
    glitch="Planets orbit because there is no gravity in space.",
    repair="Repaired. It is the opposite. Gravity is exactly what makes an orbit - it bends "
           "the planet's straight-line motion into a closed path. With no gravity there "
           "would be no orbit at all.",
    keep="Kept as it stands. Check it against your frozen list: what did the planet do when "
         "gravity was switched off?",
)

LABS["W6B"] = dict(
    file="SCI_G_W6B_Earth_And_Planets_Do.html",
    gap=("live Orbit viewer shows four orbital positions, but the LO is about building a "
         "model that is 'accurate for its purpose' - the scale trade-off that decision "
         "rests on is not in the widget"),
    title="\U0001F4D0 Honest Model Lab",
    intro="The orbit viewer above shows the movement. This lab is about the decision you "
          "have to make before you build: what your model is allowed to get wrong.",
    q="Our model cannot be true to size and true to distance at the same time. Which "
      "should we choose?",
    opts=["True to size", "True to distance", "It depends on the purpose"],
    items=[
        ("True to size", "Planets in the right proportions. But if Earth is a 1 cm bead, "
                         "Neptune sits about 1.2 km away - the distances will not fit on "
                         "any page."),
        ("True to distance", "Orbits spaced correctly. But at that scale the planets shrink "
                             "to specks you cannot see, let alone label."),
        ("It depends on the purpose", "This is the scientist's answer. A model built to "
                                      "show ORDER can distort size and distance. A model "
                                      "built to show scale must give up fitting on a page."),
    ],
    alldone="All three are frozen on the list. Now state your model's purpose, and say "
            "exactly what you are choosing to get wrong to serve it.",
    glitch="A good model gets everything right.",
    repair="Repaired. Every model is wrong somewhere on purpose - that is what makes it a "
           "model and not the thing itself. A good model is honest about where, and says so "
           "on its label.",
    keep="Kept as it stands. Check your frozen list: was there any option that got size and "
         "distance both right?",
)

LABS["W7B"] = dict(
    file="SCI_G_W7B_The_Moon_Do.html",
    gap=("live Phase explorer is BYTE-IDENTICAL to W7A's and covers phases only; W7B's LO "
         "adds 'distinguish phases from eclipses', and the word eclipse appears nowhere in "
         "that widget"),
    title="\U0001F311 Phase or Eclipse Lab",
    intro="The phase explorer above shows the phases. This lab is about telling them apart "
          "from eclipses, which look related and are not.",
    q="What makes a Moon phase?",
    opts=["Earth's shadow on the Moon", "Which lit part we can see", "Clouds"],
    items=[
        ("Phase", "Which lit part we can see. The Sun always lights half the Moon. As the "
                  "Moon orbits, we see more or less of that lit half. No shadow is involved."),
        ("Lunar eclipse", "Earth's shadow really does fall on the Moon. This happens only "
                          "at Full Moon, and only when Sun, Earth and Moon line up closely."),
        ("Solar eclipse", "The Moon's shadow falls on Earth. This happens only at New Moon, "
                          "and only when the line-up is close enough."),
    ],
    alldone="All three are frozen on the list. Now say the difference in one line: a phase "
            "is about what we can SEE, an eclipse is about a SHADOW.",
    glitch="A Full Moon should give an eclipse every month.",
    repair="Repaired. The Moon's orbit is tilted by about five degrees, so at most Full "
           "Moons it passes above or below Earth's shadow instead of through it. That tilt "
           "is why eclipses are rare rather than monthly.",
    keep="Kept as it stands. If that were true we would see a lunar eclipse every month - "
         "check your frozen list for what an eclipse actually needs.",
)

UNBUILT = {
    "W7A": ("SCI_G_W7A_The_Moon_Explore.html",
            "The live Phase explorer covers W7A's LO - 'explain why the Moon appears to "
            "change shape as it orbits Earth' - directly and completely. It is already "
            "button-only, already states that the effect is viewing geometry and not "
            "Earth's shadow, and already carries no score. A second lab here would "
            "duplicate a widget that is doing its job. AMBER-UNBUILT by design."),
}


def build_widget(code, L):
    opts = "".join(
        '<button class="gl-btn i%d" data-label="%s" type="button" aria-pressed="false" '
        'onclick="gsgLabPredict_%s(this)"><span class="gl-glyph">%s</span>%s</button>'
        % (i, o, code, GLYPH[i], o) for i, o in enumerate(L["opts"]))
    tests = "".join(
        '<button class="gl-btn i%d" data-i="%d" type="button" onclick="gsgLabTest_%s(this)">'
        '<span class="gl-glyph">%s</span>Test %s</button>'
        % (i, i, code, GLYPH[i], n) for i, (n, _) in enumerate(L["items"]))
    return (
      '<div class="gsglab" id="gsglab-%s">\n' % code +
      '<h3>%s</h3>\n' % L["title"] +
      '<p style="margin:0">%s</p>\n' % L["intro"] +
      '<div class="gl-step">Step 1 · Predict, before you test</div>\n' +
      '<p style="margin:0 0 5px">%s</p>\n' % L["q"] +
      '<div class="gl-row gl-predict">%s</div>\n' % opts +
      '<p class="gl-say" id="gl-say-%s" aria-live="polite">Choose one. Say it, point to it, '
      'or press it. Nothing here is right or wrong yet.</p>\n' % code +
      '<div class="gl-step">Step 2 · Test each one</div>\n' +
      '<div class="gl-row">%s</div>\n' % tests +
      '<div class="gl-stage" id="gl-stage-%s" aria-live="polite">Press one to see what it '
      'does.</div>\n' % code +
      '<div class="gl-frozen"><b>Frozen results — these stay on the page</b>\n'
      '<ol id="gl-list-%s"></ol>\n'
      '<p style="margin:6px 0 0" id="gl-note-%s" aria-live="polite">Nothing tested yet.</p>'
      '</div>\n' % (code, code) +
      '<div class="gl-step">Step 3 · Explain</div>\n' +
      '<div class="gl-glitch"><b>SCIENCE GLITCH:</b> “%s”\n' % L["glitch"] +
      '<div class="gl-row" style="margin-top:7px">'
      '<button class="gl-btn i0" data-fix="0" type="button" onclick="gsgLabGlitch_%s(this)">'
      'Keep the claim</button>'
      '<button class="gl-btn i1" data-fix="1" type="button" onclick="gsgLabGlitch_%s(this)">'
      'Repair it</button></div>\n' % (code, code) +
      '<p class="gl-say" id="gl-glitch-%s" aria-live="polite">Use your frozen list as the '
      'evidence. Decide, then say why.</p></div>\n' % code +
      '<p class="gl-foot">Every step is a button, and each option carries a shape and a word '
      'as well as its colour. Say it, point to it or have an adult press it — the route '
      'does not change the Science.</p>\n</div>')


def install(code):
    L = LABS[code]
    p = os.path.join(LIVE, L["file"])
    s = open(p, encoding="utf-8").read()
    assert "gsglab-%s" % code not in s, "%s: lab already present" % code

    print_before = re.search(r'<div class="print-pack">.*?</div>\s*<script>', s, re.S).group(0)
    wit_before = re.search(r'<div id="print-witness".*?</div></div>', s, re.S).group(0)
    tiers_before = tuple(s.count(t) for t in ("Supported", "Standard", "Stretch"))

    # land inside We Do 2, immediately after the live widget's feedback line
    m = re.search(r'<div class="widget-feedback"[^>]*id="wf-%s"[^>]*>.*?</div></div>' % code,
                  s, re.S)
    assert m, "%s: We Do 2 widget anchor not found" % code
    assert s.count(m.group(0)) == 1, "%s: anchor not unique" % code
    s = s.replace(m.group(0), m.group(0) + build_widget(code, L), 1)

    data = "[" + ",".join(
        "{g:%s,n:%s,t:%s}" % (js_str(GLYPH[i]), js_str(n), js_str(t))
        for i, (n, t) in enumerate(L["items"])) + "]"
    js = JS_TMPL % dict(code=code, data=data,
                        alldone=js_str(L["alldone"]),
                        repair=js_str(L["repair"]), keep=js_str(L["keep"]))

    s = s.replace("</style>", CSS + "</style>", 1)
    i = s.rfind("</script>")
    s = s[:i] + js + s[i:]

    # invariants, asserted before the file is written
    assert re.search(r'<div class="print-pack">.*?</div>\s*<script>', s, re.S).group(0) \
        == print_before, "%s: print pack changed" % code
    assert re.search(r'<div id="print-witness".*?</div></div>', s, re.S).group(0) \
        == wit_before, "%s: witness changed" % code
    assert tuple(s.count(t) for t in ("Supported", "Standard", "Stretch")) == tiers_before, \
        "%s: tier counts changed" % code
    assert "matchMedia" not in s, "%s: matchMedia introduced" % code

    open(p, "w", encoding="utf-8").write(s)
    print("installed %-8s %-44s gap: %s" % (code, L["file"], L["gap"][:60] + "..."))


if __name__ == "__main__":
    for c in sys.argv[1:]:
        install(c)
