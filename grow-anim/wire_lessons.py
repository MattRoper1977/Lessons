#!/usr/bin/env python3
"""Wire the GROW Animation Framework's teaching behaviours into the GROW lessons.

inject.py puts the LIBRARY into a lesson. This puts the TEACHING BEHAVIOURS in:
the story spine, the motion key, the progressive-reveal stage, the We-Do frame,
the misconception engine and the retrieval animation — each on the slide where
it belongs.

    python3 grow-anim/wire_lessons.py Science_Teesside/Grow/*.html
    python3 grow-anim/wire_lessons.py --check Science_Teesside/Grow/*.html

Everything inserted is wrapped in <!-- GROW-ANIM:WIRE:<slot>:BEGIN/END -->, so
re-running replaces rather than duplicates, and a block can be edited here once
and pushed out to every lesson. Existing lesson content is never removed — the
framework is added alongside it, so nothing a teacher already relies on moves.

It also applies PATCHES — small idempotent repairs to the lesson's own deck
code, listed and explained beside the patch table below.

Anchors are chosen to survive ordinary editing of the lessons:
  · after the slide's "Watch me think" li-box, where there is one
  · otherwise after the slide's <h2>
"""

import os
import re
import sys

STEM = re.compile(r'SCI_G_(W\d+)_')

# ---------------------------------------------------------------- per lesson
# Each lesson names the assets it teaches from and the words that go with them.
LESSONS = {
    "W3": {
        "story": "Why do we slip on ice?|Test rough and smooth ramps|Rough grips, smooth slides|"
                 "Friction acts between two rubbing surfaces|Choosing the right sole, tyre and brake",
        "ido1": {"asset": "friction", "overlays": "friction,heat",
                 "title": "Same block, same slope — one thing changed"},
        "wedo": {"asset": "friction",
                 "q": "Same block, same slope. Rough carpet or smooth ice — which one slides further?",
                 "options": "The carpet|The ice|Exactly the same",
                 "discuss": "Turn and talk. Say WHY, using the word <em>surface</em>.",
                 "explain": "More bumps to catch on means more friction, so the block on the carpet is held back "
                            "and the block on the ice keeps going.",
                 "check": "Write one sentence: “Friction is greater on ___ because ___.”"},
        "ido2": {"asset": "friction",
                 "claim": "Friction is just a nuisance — something that slows you down and wears things out."},
        "dual": {"panels": "friction:WHAT YOU SEE|forces:THE SCIENCE",
                 "script": "observe: show scene#1, blockA#1, blockB#1 :: Two blocks, two surfaces. That is what you actually see.\n"
                           "observe: show ground#2, person#2, box#2 :: And here is the same idea, drawn the way a scientist draws it.\n"
                           "notice: show rough#1, smooth#1 + overlay force#2 :: Rough one side, smooth the other. A push over here.\n"
                           "notice: overlay friction#1 + overlay friction#2 :: Friction, in BOTH pictures, doing exactly the same job.\n"
                           "explain: overlay heat#1 + overlay energy#2 :: And heat, in both. Rubbing always makes heat.\n"
                           "label: label grip#1 + label pair#2 :: One event. Two ways of showing it. Learn to read both."},
        "process": {"asset": "friction", "title": "Watch it again \u2014 what friction actually does"},
        "exit": {"asset": "friction", "stop": "2",
                 "cue": "Which surface has MORE friction? Say it out loud before I click."},
    },
    "W4": {
        "story": "How do you lift something far too heavy?|Try a lever, a pulley and a pair of gears|"
                 "Machines swap a small effort for a big one|Pivot, wheel or meshed teeth|"
                 "Choosing the right mechanism for the job",
        "ido1": {"asset": "lever", "overlays": "force,pressure",
                 "title": "A lever — where should you push?"},
        "wedo": {"asset": "pulley",
                 "q": "The rope runs over the wheel. Which way do you pull to make the load go UP?",
                 "options": "Pull down|Pull up|Pull sideways",
                 "discuss": "Show your partner with your hand first, then say why.",
                 "explain": "A pulley does not make the load lighter. It changes the DIRECTION of your effort — "
                            "and pulling down is far easier than lifting up.",
                 "check": "Label a pulley diagram with effort, load and the direction of the rope."},
        "ido2": {"asset": "gears",
                 "claim": "Two gears with their teeth locked together must turn the same way."},
        "dual": {"panels": "lever:WHAT YOU SEE|forces:THE SCIENCE",
                 "script": "observe: show ground#1, pivot#1, bar#1, load#1 :: A bar, a pivot and something heavy. What you see.\n"
                           "observe: show ground#2, person#2, box#2 :: And a plain push, drawn as forces.\n"
                           "notice: show hand#1 + overlay force#1 :: A small effort, a long way from the pivot.\n"
                           "notice: overlay force#2 :: The same kind of arrow. The same kind of force.\n"
                           "explain: overlay pressure#1 + overlay friction#2 :: A machine does not create force. It only moves it about.\n"
                           "label: label rule#1 + label push#2 :: A lever is a force diagram you can hold."},
        "process": {"asset": "pulley", "title": "Watch it again \u2014 how a pulley turns your pull round"},
        "exit": {"asset": "lever", "stop": "2",
                 "cue": "Name the part before it appears — pivot, effort or load?"},
    },
    "W5": {
        "story": "Does the surface really change how far it slides?|Set up three ramps and three cars|"
                 "Only one thing may be different|A fair test changes ONE variable|"
                 "Planning an investigation of your own",
        "ido1": {"asset": "fairtest", "overlays": "force",
                 "title": "Three rigs — only one of them is a fair test"},
        "wedo": {"asset": "fairtest",
                 "q": "Ramp C is rougher AND steeper. Its car stops sooner. What caused it?",
                 "options": "The surface|The height|You cannot tell",
                 "discuss": "Careful — two of these answers sound right. Argue it out.",
                 "explain": "Two variables changed at once, so no conclusion can be drawn about either of them. "
                            "That is exactly what makes a test unfair.",
                 "check": "List the variable you would change, and three you would keep the same."},
        "ido2": {"asset": "fairtest",
                 "claim": "A fair test just means taking turns and not cheating."},
        "dual": {"panels": "fairtest:THE INVESTIGATION|friction:WHAT WE ARE MEASURING",
                 "script": "observe: show ground#1, rigA#1, rigB#1 :: Two rigs, set up identically.\n"
                           "observe: show scene#2, blockA#2, blockB#2 :: And this is the thing we are actually testing.\n"
                           "notice: show surfB#1, varsame#1 + show rough#2, smooth#2 :: One variable changed \u2014 the surface. Everything else held.\n"
                           "think: pause \"So if the cars travel different distances, what caused it?\" :: Only one answer is allowed.\n"
                           "explain: label fair#1 + overlay friction#2 :: The surface. Because that is the ONLY thing we let change.\n"
                           "label: show rigC#1, varchange#1 + label unfair#1 :: Change two things and the investigation tells you nothing."},
        "process": {"asset": "friction", "title": "Watch it again \u2014 the thing your test is measuring"},
        "exit": {"asset": "fairtest", "stop": "2",
                 "cue": "Which variable changed here? Say it before the reveal."},
    },
    "W6": {
        "story": "Why does the Sun seem to cross the sky?|Model the Sun, the Earth and the planets|"
                 "The Earth spins as it orbits|Day, night and a year|"
                 "Predicting where a planet will be",
        "ido1": {"asset": "solarsystem", "overlays": "gravity",
                 "title": "Eight planets, one star"},
        "wedo": {"asset": "earthspin",
                 "q": "It is midnight here in Teesside. Where is the Sun right now?",
                 "options": "Switched off|Below the Earth|Shining on the other side",
                 "discuss": "Two of these are pictures people carry around. Only one is true.",
                 "explain": "The Sun never stops shining and never moves. We are on the shadow side of a "
                            "spinning planet — that is all night is.",
                 "check": "Draw the Sun, the Earth and a stick figure at midnight. Mark the lit side."},
        "ido2": {"asset": "solarsystem",
                 "claim": "The Sun goes round the Earth — you can watch it cross the sky every day."},
        "dual": {"panels": "earthspin:WHAT YOU SEE|solarsystem:THE MODEL",
                 "script": "observe: show sun#1, earth#1 :: From here it looks as though the Sun crosses the sky.\n"
                           "observe: show sun#2, orbits#2 :: Step back far enough and the picture changes completely.\n"
                           "notice: show night#1 + overlay light#1 :: Half the Earth lit, half in shadow. Always.\n"
                           "notice: pop earth#2, mars#2, venus#2, mercury#2 :: And the Earth is one of eight, going round.\n"
                           "think: pause \"Which of these two pictures is TRUE?\" :: Careful. It is a trick question.\n"
                           "explain: show you#1 + flow you#1 + flow earth#2 :: Both. One is what you see; one is what is happening.\n"
                           "label: label spin#1 + label star#2 :: A scientist has to be able to hold both at once."},
        "process": {"asset": "earthspin", "title": "Watch it again \u2014 one turn, one day and one night"},
        "exit": {"asset": "solarsystem", "stop": "2",
                 "cue": "Name the next planet out from the Sun before I click."},
    },
    "W7": {
        "story": "Why does the Moon change shape?|Model the Sun, the Earth and the Moon|"
                 "Half the Moon is lit all the time|Phases are the angle we see it from|"
                 "Reading a Moon calendar",
        "ido1": {"asset": "moonphases", "overlays": "light,field",
                 "title": "One month, one trip round the Earth"},
        "wedo": {"asset": "moonphases",
                 "q": "Does the Moon make its own light?",
                 "options": "Yes|No|Only when it is full",
                 "discuss": "Hands up first. Then say where the light comes from.",
                 "explain": "The Moon is a rock. The Sun lights exactly half of it, all the time — the same way "
                            "it lights half of the Earth.",
                 "check": "Draw the Moon at full and at new, and mark where the Sun is in each."},
        "ido2": {"asset": "moonphases",
                 "claim": "The phases are the Earth’s shadow falling across the Moon."},
        "dual": {"panels": "earthspin:WHAT YOU SEE|moonphases:THE MODEL",
                 "script": "observe: show sun#1, earth#1, night#1 :: Standing on Earth, at night.\n"
                           "observe: show sun#2, earth#2, orbit#2, moon#2 :: And the same moment, seen from outside.\n"
                           "notice: overlay light#1 + overlay light#2 :: Sunlight, arriving from one side, in both pictures.\n"
                           "think: pause \"So why does the Moon look a different shape each week?\" :: Predict before I show you.\n"
                           "notice: flow moon#2 + pop p0#2, p2#2, p4#2, p6#2 :: Because we see its lit half from a new angle every night.\n"
                           "explain: label lit#2 + label half#2 :: Nothing about the Moon changes. Only our view of it.\n"
                           "label: label spin#1 :: What you see, and what is happening. Both are worth knowing."},
        "process": {"asset": "moonphases", "title": "Watch it again \u2014 one orbit, one full set of phases"},
        "exit": {"asset": "moonphases", "stop": "2",
                 "cue": "Name the phase before it appears."},
    },
}

# --------------------------------------------------------------- the blocks
MOTION_KEY = (
    '<div class="li-box" style="margin-top:14px"><strong>🎬 How our animations talk to you.</strong> '
    'Every movement means the same thing in every science lesson this year — watch for them.</div>'
    '<div class="g-key"></div>')


def blocks(cfg):
    """slot -> html to insert. Order here is only for readability."""
    ido1, wedo, ido2, ex = cfg["ido1"], cfg["wedo"], cfg["ido2"], cfg["exit"]
    return {
        "story": '<div class="g-story" data-grow-story="%s"></div>' % cfg["story"],
        "key": MOTION_KEY,
        "ido1": (
            '<div class="g-stage g-lit" data-grow-asset="%s" data-grow-script="@teach"'
            ' data-grow-overlays="%s" data-grow-title="%s" data-grow-frame="wide"></div>'
            % (ido1["asset"], ido1["overlays"], ido1["title"])),
        "wedo": (
            '<div class="g-wedo" data-grow-asset="%s" data-grow-script="@teach"'
            ' data-grow-q="%s" data-grow-options="%s" data-grow-discuss="%s"'
            ' data-grow-explain="%s" data-grow-check="%s"></div>'
            % (wedo["asset"], esc(wedo["q"]), esc(wedo["options"]), esc(wedo["discuss"]),
               esc(wedo["explain"]), esc(wedo["check"]))),
        "ido2": (
            '<div class="g-misc" data-grow-asset="%s" data-grow-claim="%s"'
            ' data-grow-wrong="@wrong" data-grow-right="@right"></div>'
            % (ido2["asset"], esc(ido2["claim"]))),
        "exit": (
            '<div class="g-retrieve" data-grow-asset="%s" data-grow-script="@retrieve"'
            ' data-grow-stop="%s" data-grow-cue="%s"></div>'
            % (ex["asset"], ex["stop"], esc(ex["cue"]))),
        # Phase 8 — real world beside scientific model, driven by ONE script so
        # the two panels can never drift out of step.
        "dual": (
            '<div class="g-stage g-lit" data-grow-dual="%s" data-grow-frame="wide"'
            ' data-grow-script="%s"></div>'
            % (cfg["dual"]["panels"], esc(cfg["dual"]["script"]))),
        # Phase 5 — the process itself, left running as a reference pupils can
        # replay while they work.
        "process": (
            '<div class="g-stage g-lit" data-grow-asset="%s" data-grow-script="@process"'
            ' data-grow-title="%s" data-grow-frame="wide"></div>'
            % (cfg["process"]["asset"], esc(cfg["process"]["title"]))),
    }


def esc(s):
    return s.replace('"', '&quot;')


# slot -> (slide data-title, anchor mode)
SLOTS = [
    ("story", "Title", "h1"),
    ("key", "Today at a Glance", "h2"),
    ("ido1", "I Do 1", "libox"),
    ("wedo", "We Do 1", "h2"),
    ("ido2", "I Do 2", "libox"),
    ("dual", "We Do 2", "h2"),
    ("process", "Independent Work", "h2"),
    ("exit", "Exit Ticket", "h2"),
]

MARK_BEGIN = "<!-- GROW-ANIM:WIRE:%s:BEGIN -->"
MARK_END = "<!-- GROW-ANIM:WIRE:%s:END -->"

# ---------------------------------------------------------------- deck repair
# showSlide(i) moves the deck but never updates `currentSlide`, so anything that
# calls it directly leaves the progress bar, the slide counter and the next
# press of Next ▶ all pointing at the previous slide. Latent while only
# nextSlide/prevSlide called it — they set currentSlide first — but the moment
# any other code jumps straight to a slide, the deck silently desynchronises.
# One assignment fixes it, and is a no-op on the existing callers.
PATCHES = [
    ("function showSlide(i){slides.forEach(",
     "function showSlide(i){currentSlide=i;slides.forEach("),
]


def repair(html):
    """Idempotent one-line fixes to the lesson's own deck code."""
    for before, after in PATCHES:
        if after in html:
            continue
        html = html.replace(before, after)
    return html


def anchor_at(html, slide_title, mode):
    """Index just past the anchor inside the named slide, or None."""
    i = html.find('data-title="%s"' % slide_title)
    if i < 0:
        return None
    nxt = html.find('data-title="', i + 10)
    stop = nxt if nxt > 0 else len(html)
    if mode == "libox":
        j = html.find('class="li-box"', i)
        if 0 < j < stop:
            k = html.find("</div>", j)
            if 0 < k < stop:
                return k + len("</div>")
        mode = "h2"                       # a slide without a li-box falls back
    tag = "</h1>" if mode == "h1" else "</h2>"
    k = html.find(tag, i)
    if 0 < k < stop:
        return k + len(tag)
    return None


def wire(html, slot, body, slide_title, mode):
    begin, end = MARK_BEGIN % slot, MARK_END % slot
    wrapped = begin + body + end
    i = html.find(begin)
    if i >= 0:                            # already wired — replace in place
        j = html.find(end, i)
        if j < 0:
            raise SystemExit("unclosed WIRE:%s marker" % slot)
        return html[:i] + wrapped + html[j + len(end):], True
    at = anchor_at(html, slide_title, mode)
    if at is None:
        return html, False
    return html[:at] + wrapped + html[at:], True


def process(path, check_only):
    stem = STEM.search(os.path.basename(path))
    if not stem or stem.group(1) not in LESSONS:
        print("  skip    %s  (no wiring defined)" % path)
        return None
    cfg = LESSONS[stem.group(1)]
    with open(path, encoding="utf-8") as fh:
        original = fh.read()

    html, B, missed = repair(original), blocks(cfg), []
    for slot, slide_title, mode in SLOTS:
        html, ok = wire(html, slot, B[slot], slide_title, mode)
        if not ok:
            missed.append("%s→%s" % (slot, slide_title))

    for m in missed:
        print("  WARN    %s  no anchor for %s" % (path, m))
    if html == original:
        print("  ok      %s" % path)
        return not missed
    if check_only:
        print("  STALE   %s" % path)
        return False
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("  wired   %s  (%+d bytes, %d/%d slots)" % (path, len(html) - len(original),
                                                      len(SLOTS) - len(missed), len(SLOTS)))
    return not missed


def main(argv):
    check_only = "--check" in argv
    targets = [a for a in argv if not a.startswith("--")]
    if not targets:
        raise SystemExit(__doc__)
    results = [process(p, check_only) for p in targets]
    if False in results:
        raise SystemExit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
