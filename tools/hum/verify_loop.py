#!/usr/bin/env python3
"""ORDER HUM-T — the loop acceptance battery.

Numbered rows, MERGED INTO THE CHASSIS CONTRACT numbering by ruling (STOP-T2):

    row 45  the loop panel row  (chassis 43/44 keep estate furniture and sibling nav)
    row 46  no RE panel asks for a belief
    rows 47+ reserved for the policy rows

The provenance check ("no panel text equals the science exemplar's") was numbered 37
in the order, but chassis row 37 is the pathway theme class. Rather than leave a
second collision it is folded into row 45, where it belongs: a panel whose words are
the exemplar's is not a panel filled from this deck.

Rows 38-42 and 45 are behavioural: chassis standing rule 5 says a static parse is
structurally unable to emit PASS for them, so they report NOT-CHECKED here and are
proved by the rendered harness (tools/hum/render_proof.cjs).
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deck_dom
from deck_dom import parse, stages, stage_name, is_ribbon          # noqa: E402
from loop_adapter import (MODELLING_STAGES, MARK, pupil_text,      # noqa: E402
                          stage_task, POLICY_CODES, POLICY_SPACE, POLICY_EARWIG, deck_config,
                          influence_options, INFLUENCE_OUTCOMES)

PASS, FAIL, NC = 'PASS', 'FAIL', 'NOT-CHECKED'

# R5 / correction #13: a belief question is one with NO negation governing it.
ASK_BELIEF = re.compile(r'(?<![a-z])(?:write|say|tell|share|state)\b[^.]{0,40}\byour own belief'
                        r'|what do you believe\?', re.I)
NEGATION = re.compile(r'\b(never|not|nobody|no one|no pupil|no learner|without)\b', re.I)


def pathway_of(panel):
    from loop_adapter import POLICY_MODALITIES
    modes = ' '.join(n.inner_text() for n in panel.find(lambda n: 'loop-modes' in n.classes()))
    for pw, text in POLICY_MODALITIES.items():
        if text[:24] in modes:
            return pw
    return 'GROW'


def panels(doc):
    return [n for n in doc.walk() if is_ribbon(n)]


def panel_parts(p):
    return {n.attrs.get('data-loop-part'): n.inner_text()
            for n in p.find(lambda n: n.attrs.get('data-loop-part'))}



def task_core(task: str, n: int = 24) -> str:
    """The first n characters of a stage's task with its trailing punctuation removed:
    the string rows 16 and 17 look for inside the panel's own text. A short task that
    ends in a full stop ("Pinpoint the place.") is quoted without it by the adapter,
    so the core is cut AFTER the strip, never before (batch 4 rebuild, 2026-09-21)."""
    return re.sub(r'[.!?\u2026\s]+$', '', task or '')[:n]


def declared_count(stage_list, names):
    """How many stages DECLARE one of `names`, read from the raw eyebrow label.

    STOP-C1 ruling 3 requires each "X stages carry no panel" row to assert its subset against the
    deck's own declaration before judging the contents, so that an empty subset cannot pass as a
    vacuous success. The declaration is taken from the eyebrow TEXT via deck_dom.EYEBROW_STAGE --
    the same source the identity oracle reads, but taken RAW, without the document-order
    disambiguation. That keeps the comparison honest in the direction that matters: if the oracle
    silently drops a stage from a subset, the declared count still sees it and the row goes RED.
    A deck that carries no eyebrows at all declares nothing and is judged as before.
    """
    want = set(names)
    seen = 0
    for s in stage_list:
        label = deck_dom.EYEBROW_STAGE.get(deck_dom.stage_eyebrow(s).lower())
        if label in want or (label in deck_dom.EYEBROW_ORDINAL
                             and deck_dom.EYEBROW_ORDINAL[label] in want):
            seen += 1
    return seen


PATHWAY_SEGMENT = re.compile(r'^(build|grow|launch)\s+science(\s+\S+)?$', re.I)


def _norm(s):
    return ' '.join((s or '').split()).strip()


def deck_title_heading(doc):
    """The deck's own title, as the HEAD <title> states it, minus the pathway marker."""
    titles = doc.find(lambda n: n.tag == 'title')
    head = [x for x in titles if any(a.tag == 'head' for a in x.ancestors())] or titles
    if not head:
        return ''
    segs = [_norm(x) for x in _norm(head[0].inner_text()).split('\u00b7')]
    return ' \u00b7 '.join(x for x in segs if not PATHWAY_SEGMENT.match(x)).lower()


def stage_heading(stage):
    hs = stage.find(lambda n: n.tag in ('h1', 'h2', 'h3'))
    return _norm(hs[0].inner_text()).lower() if hs else ''


def verify(after_html: str, before_html: str, strand: str, science_panel_texts):
    doc = parse(after_html)
    st = stages(doc)
    rows = []

    def row(num, name, status, detail=''):
        rows.append({'row': num, 'name': name, 'status': status, 'detail': detail})

    eligible = [s for s in st if stage_name(s) not in MODELLING_STAGES
                and stage_name(s) != 'title']                       # P1-1
    modelling = [s for s in st if stage_name(s) in MODELLING_STAGES]
    title_stages = [s for s in st if stage_name(s) == 'title']

    # 1 — every eligible stage carries exactly one panel
    bad = [(stage_name(s), len(s.find(is_ribbon))) for s in eligible
           if len(s.find(is_ribbon)) != 1]
    row(1, 'one panel per non-modelling, non-title stage', PASS if not bad else FAIL, str(bad))

    # 2 — modelling stages carry none (R1: the 98 measure)
    #
    # STOP-C1 ruling 3: AN EMPTY SET IS NOT A PASS. The subset is asserted against what the deck
    # DECLARES before its contents are judged. Measured before the fix, this row ran over an empty
    # modelling set on 31 of 31 SX3 decks -- every one of them declares one or two modelling stages
    # and the oracle found none -- so "I Do stages carry no panel" tested nothing at all across the
    # whole population, while row 1 simultaneously demanded a panel on each of those same stages
    # because an unnamed stage falls into `eligible` by default.
    declared_mod = declared_count(st, MODELLING_STAGES)
    bad = [stage_name(s) for s in modelling if s.find(is_ribbon)]
    row(2, 'I Do stages carry no panel',
        PASS if (len(modelling) == declared_mod and not bad) else FAIL,
        'declared=%d resolved=%d %s' % (declared_mod, len(modelling), bad))

    # 3 — no static ribbon survives
    leftovers = [p for p in panels(doc) if not p.attrs.get(MARK)]
    row(3, 'no static ribbon survives', PASS if not leftovers else FAIL,
        '%d left' % len(leftovers))

    # 4 — every panel is stateful (four steps with data-state)
    bad = [p.attrs.get('data-loop-stage') for p in panels(doc)
           if len(p.find(lambda n: 'data-lundy-step' in n.attrs and 'data-state' in n.attrs)) != 4]
    row(4, 'every panel has four stateful steps', PASS if not bad else FAIL, str(bad))

    # 5 — every panel carries all three parts, and EVERY part element is non-empty
    # (several influence lines under P1-2: a blank one among them is a blank one)
    bad = []
    for p in panels(doc):
        parts = panel_parts(p)
        for k in ('response', 'audience', 'influence'):
            if not (parts.get(k) or '').strip():
                bad.append((p.attrs.get('data-loop-stage'), k))
        for n in p.find(lambda n: n.attrs.get('data-loop-part')):
            if not n.inner_text().strip():
                bad.append((p.attrs.get('data-loop-stage'), n.attrs.get('data-loop-part') + ' (blank element)'))
    row(5, 'every panel carries response + audience + influence', PASS if not bad else FAIL, str(bad))

    # 6 — every panel carries the three controls the script drives
    bad = []
    for p in panels(doc):
        for a in ('lundy-voice', 'lundy-audience', 'lundy-influence'):
            if not p.find(lambda n: n.attrs.get('data-action') == a):
                bad.append((p.attrs.get('data-loop-stage'), a))
    row(6, 'every panel carries the three controls', PASS if not bad else FAIL, str(bad))

    # 7 — the order-enforcing script is present exactly once
    scripts = [n for n in doc.walk() if n.tag == 'script' and n.attrs.get('data-hum-t-loop')]
    row(7, 'order-enforcing script injected once', PASS if len(scripts) == 1 else FAIL,
        '%d found' % len(scripts))

    # 8 — the response point is drawn from THIS stage's own text
    bad = []
    for s in eligible:
        for p in s.find(is_ribbon):
            task = stage_task(s)
            core = re.sub(r'…$', '', task)[:40]
            resp = panel_parts(p).get('response', '')
            if core and core not in resp:
                bad.append(stage_name(s))
    row(8, 'response point quotes the stage\'s own task', PASS if not bad else FAIL, str(bad))

    # 9 — no two panels in a deck share a loop key (stage-specificity)
    keys = [p.attrs.get('data-loop-key') for p in panels(doc)]
    row(9, 'each panel is keyed to its own stage', PASS if len(set(keys)) == len(keys) else FAIL,
        '%d keys, %d unique' % (len(keys), len(set(keys))))

    # 10 — the TA brief carries the codes and the Space conditions (R2/R4), staff-only
    tas = [n for n in doc.walk() if n.attrs.get(MARK) and 'ta-card' in n.classes()]
    staff_ok = all(n.attrs.get('data-mbm-guide') == 'staff' for n in tas)
    text = ' '.join(n.inner_text() for n in tas)
    have_codes = all(c in text for c, _ in POLICY_CODES)
    have_space = all(sp.split('.')[0] in text for sp in POLICY_SPACE)
    row(10, 'TA brief carries codes + Space, staff-only',
        PASS if (tas and staff_ok and have_codes and have_space) else FAIL,
        'blocks=%d staff_only=%s codes=%s space=%s' % (len(tas), staff_ok, have_codes, have_space))

    # 11 — the code STRIP never reaches the pupil surface (R2).
    # Single letters (I, E, R) and punctuation (//, ?) are ordinary pupil text, so
    # the test is the strip's own shape: the unambiguous codes standing together.
    pupil = ' '.join(pupil_text(s) for s in st)
    strip_rx = re.compile(r'\bVF\b.{0,160}?\bWS\b|\bWS\b.{0,160}?\bNS\b', re.S)
    leaked = bool(strip_rx.search(pupil))
    singles = [c for c in ('VF', 'WS') if re.search(r'(?<![A-Za-z])%s(?![A-Za-z])' % c, pupil)]
    row(11, 'no staff code strip on the pupil surface',
        PASS if not (leaked or singles) else FAIL,
        'strip=%s singles=%s' % (leaked, singles))

    # 12 — the Earwig line appears once, at Exit, on the TA layer (R3)
    ew = [n for n in doc.walk() if POLICY_EARWIG[:28] in ' '.join(n.text)]
    exit_ta = [n for n in tas if POLICY_EARWIG[:28] in n.inner_text()]
    row(12, 'Earwig line staff-side at the closing stage',
        PASS if exit_ta else FAIL, '%d staff blocks carry it' % len(exit_ta))

    # 45p — PROVENANCE (part of row 45): no panel text equals the science exemplar's
    clash = []
    for p in panels(doc):
        t = re.sub(r'\s+', ' ', p.inner_text()).strip()
        if t in science_panel_texts:
            clash.append(p.attrs.get('data-loop-stage'))
    row(45.1, 'provenance: no panel text equals the science exemplar\'s',
        PASS if not clash else FAIL, str(clash))

    # 45.2 — THE ACT IS NAMED (row 45 part 4). Every control that advances the loop
    # carries a visible label. The verification pass found the science exemplar
    # feeding VOICE from unlabelled lesson controls: the pupil acts and nothing says
    # the act was their Voice.
    unnamed = []
    for p in panels(doc):
        for n in p.find(lambda n: n.attrs.get('data-action', '').startswith('lundy-')):
            if not n.inner_text().strip():
                unnamed.append((p.attrs.get('data-loop-stage'), n.attrs.get('data-action')))
    # and nothing OUTSIDE a panel may advance the loop
    outside = [n.attrs.get('data-action') for n in doc.walk()
               if n.attrs.get('data-action', '').startswith('lundy-')
               and not any(is_ribbon(a) for a in n.ancestors())]
    row(45.2, 'the act is named: every loop control is labelled, and none sits outside a panel',
        PASS if not (unnamed or outside) else FAIL,
        'unlabelled=%s outside=%s' % (unnamed[:3], outside[:3]))

    # 14 — P1-1: the Title stage carries no panel (it is metadata, not a response point)
    #
    # STOP-C1 ruling 3: AN EMPTY SET IS NOT A PASS -- and note that a blanket "empty is RED" would
    # be wrong, which is why this compares against the DECLARED count rather than against zero.
    # Measured before the fix, this row ran over an empty title set on 8 of 31 SX3 decks (the 7-
    # and 13-stage shapes, whose Opening carries data-timer="2" rather than "0", so the timer route
    # missed it) while genuinely being 0/0 on three others. Only the declared comparison separates
    # those two cases.
    declared_title = declared_count(st, {'title'})
    bad = [stage_name(s) for s in title_stages if s.find(is_ribbon)]
    row(14, 'P1-1: the Title stage carries no panel',
        PASS if (len(title_stages) == declared_title and not bad) else FAIL,
        'declared=%d resolved=%d %s' % (declared_title, len(title_stages), bad))

    # 15 — P1-3: every panel sits inside a CLOSED "Feedback loop" disclosure of its own
    bad = []
    for p in panels(doc):
        d = next((a for a in p.ancestors() if a.tag == 'details'), None)
        if d is None:
            bad.append((p.attrs.get('data-loop-stage'), 'no disclosure')); continue
        if 'open' in d.attrs:
            bad.append((p.attrs.get('data-loop-stage'), 'open by default')); continue
        sm = d.find(lambda n: n.tag == 'summary')
        if not sm or sm[0].inner_text().strip() != 'Feedback loop':
            bad.append((p.attrs.get('data-loop-stage'), 'summary != Feedback loop'))
    if '@media print{.loop-disclosure{display:none}}' not in after_html:
        bad.append(('deck', 'print does not exclude the disclosure'))
    if 'openOnTaskUse' not in after_html:
        bad.append(('deck', 'no task-use opener in the loop script'))
    row(15, 'P1-3: every panel behind a collapsed "Feedback loop" disclosure; opens on tap or task use; print excludes it',
        PASS if not bad else FAIL, str(bad))

    # 16 — P1-2 (RULED 2026-09-21): the four response outcomes, one influence line each,
    # each naming its outcome and its canonical move and carrying THIS stage's task (the
    # core row 8 proves), each with its own labelled control; no two lines identical
    bad = []
    want = [k for k, _, _ in INFLUENCE_OUTCOMES]
    for s in eligible:
        core = task_core(stage_task(s))
        for p in s.find(is_ribbon):
            lines = [n for n in p.find(lambda n: n.attrs.get('data-loop-part') == 'influence')]
            texts = [re.sub(r'\s+', ' ', n.inner_text()).strip() for n in lines]
            keys = [n.attrs.get('data-loop-option', '') for n in lines]
            ctl = [n for n in p.find(lambda n: n.attrs.get('data-action') == 'lundy-influence')]
            ctls = [n.attrs.get('data-next-move', '') for n in ctl]
            ctl_labels = [re.sub(r'\s+', ' ', n.inner_text()).strip() for n in ctl]
            if keys != want:
                bad.append((stage_name(s), 'lines %s != the four outcomes %s' % (keys, want))); continue
            if len(set(texts)) != len(texts):
                bad.append((stage_name(s), 'influence lines not distinct')); continue
            if ctls != want or ctl_labels != [lab for _, lab, _ in INFLUENCE_OUTCOMES]:
                bad.append((stage_name(s), 'controls %s != outcomes %s' % (ctls, want))); continue
            for (k, label, move), t in zip(INFLUENCE_OUTCOMES, texts):
                if not t.startswith(label + ' \u2192 ' + move):
                    bad.append((stage_name(s), 'a line does not name its outcome and move: %r' % t[:50])); break
                if k != 'explained' and core and core not in t:
                    bad.append((stage_name(s), 'a line does not carry this stage\'s task: %r' % t[:50])); break
    row(16, 'P1-2 (ruled): four outcome lines per panel, each naming its move for this stage\'s task, each with its own control',
        PASS if not bad else FAIL, str(bad))

    # 17 — P1-4: VOICE names the stage's task, on the step and on its control
    bad = []
    for s in eligible:
        core = task_core(stage_task(s))
        for p in s.find(is_ribbon):
            step = p.find(lambda n: n.attrs.get('data-lundy-step') == 'voice')
            ctl = p.find(lambda n: n.attrs.get('data-action') == 'lundy-voice')
            st_ok = bool(step) and core and core in step[0].inner_text()
            ct_ok = bool(ctl) and core and core in ctl[0].inner_text()
            if not (st_ok and ct_ok):
                bad.append((stage_name(s), 'step=%s control=%s' % (st_ok, ct_ok)))
    row(17, 'P1-4: VOICE names the stage\'s task on the step and its control',
        PASS if not bad else FAIL, str(bad))

    # 45 — THE LOOP ROW (chassis numbering, by ruling); the P1 rows join the composite
    ok45 = all(r['status'] == PASS for r in rows
               if r['row'] in (1, 2, 4, 5, 6, 7, 14, 15, 16, 17, 45.1, 45.2))
    row(45, 'every non-I-Do stage carries one panel with all four parts',
        PASS if ok45 else FAIL, 'composite of rows 1,2,4,5,6,7,14,15,16,17,45.1,45.2')

    # 46 — THE RE ROW (negation-aware, per correction #13)
    asks = []
    if strand == 'RE':
        for p in panels(doc):
            for sent in re.split(r'(?<=[.!?])\s+', p.inner_text()):
                if ASK_BELIEF.search(sent) and not NEGATION.search(sent):
                    asks.append(sent[:90])
    row(46, 'no RE panel asks for a belief', PASS if not asks else FAIL, str(asks))

    # 47 — STOP-C1 ruling 6: NO PANEL ON THE STAGE THAT CARRIES THE DECK TITLE HEADING.
    #
    # This row does not read a stage NAME, and that is the whole point of it. Rows 1, 2 and 14 all
    # key off stage_name(); when the oracle mis-names a stage they mis-fire together, and the
    # adversarial review demonstrated exactly that by running loop_adapter.adapt() with a proposed
    # oracle patched in: on the three LAUNCH decks whose title is still MERGED into stage 0, that
    # stage was named 'arrival', so it was eligible, so the adapter placed a pupil-response panel
    # on the slide holding the lesson's own <h1> -- and row 14 passed with detail [] over a
    # title_stages of length ZERO. A panel there is wrong whatever the oracle believes.
    #
    # The deck title is taken from the HEAD <title>, minus whichever segment is the pathway marker.
    # Three format variations are real and each one broke a naive predicate before it was measured:
    #   - the title can carry more than one separator ("BUILD Science . Give a rock a job . Classic"),
    #     so splitting on the LAST one yields "Classic" and misses 3 decks;
    #   - the exemplars reverse the order ("Day and Night: Sky Shift . GROW Science"), so splitting
    #     on the FIRST one misses 2 more -- hence dropping the segment that IS the pathway, by
    #     pattern, rather than trusting position;
    #   - the pathway segment can carry a week code ("BUILD Science W8A . ...").
    # Two further hazards: a document holds several <title> nodes because inline SVGs carry their
    # own, so the head one is selected by ancestry; and the exemplars have no <h1> inside any stage
    # at all, so the heading probe accepts h1/h2/h3. Measured well-defined on all 34 decks of the
    # three exemplars plus the SX3 31: exactly one stage per deck, always stage 0.
    title_stage = [s for s in st if deck_title_heading(doc) and stage_heading(s) == deck_title_heading(doc)]
    bad = [stage_name(s) for s in title_stage if s.find(is_ribbon)]
    row(47, 'no panel on the stage carrying the deck title heading',
        PASS if not bad else FAIL, str(bad))

    # 13 — nothing lost: every sentence of the source deck survives somewhere.
    # (Numbered in the adapter's own low range: 45 is the chassis loop row.)
    # The ribbon is REPLACED by ruling R1, so its own boilerplate is not "lost".
    # Every other sentence the deck had must still be there.
    #
    # Sentences are taken PER BLOCK ELEMENT. Splitting the whole concatenated
    # document would invent sentences that span two elements ("Here is a finished
    # one:" + the next block) and then report them lost when a block between them
    # is removed by ruling. That is a fault in the instrument, not in the deck.
    BLOCK = {'p', 'li', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'figcaption',
             'caption', 'summary', 'blockquote', 'dd', 'dt'}

    def block_sentences(h):
        d = parse(h)
        out = set()
        for n in d.walk():
            if n.tag not in BLOCK:
                continue
            if is_ribbon(n) or any(is_ribbon(a) for a in n.ancestors()):
                continue
            for x in re.split(r'(?<=[.!?])\s+', n.inner_text(skip=is_ribbon)):
                x = x.strip()
                if len(x) > 25:
                    out.add(x)
        return out

    before_s = block_sentences(before_html)
    after_t = parse(after_html).inner_text()
    lost = sorted(x for x in before_s if x not in after_t)
    row(13, 'rendered-text diff: nothing lost', PASS if not lost else FAIL,
        '%d sentences absent: %s' % (len(lost), lost[:3]))

    # behavioural rows — proved in the browser, never here
    for n, nm in ((38, 'audience refused before voice'),
                  (39, 'influence refused before audience'),
                  (40, 'panel reaches INFLUENCE when driven in order'),
                  (41, 'every panel is reachable at 390px'),
                  (42, 'the deck\'s own controls are not double-driven')):
        row(n, nm, NC, 'behavioural — rendered harness')

    return sorted(rows, key=lambda r: r['row'])


def science_texts(root: Path):
    out = set()
    p = root / 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W9A_Rock_Evidence_Explore.html'
    if p.exists():
        for n in panels(parse(p.read_text(errors='replace'))):
            out.add(re.sub(r'\s+', ' ', n.inner_text()).strip())
    return out


def self_test(root: Path):
    """Red-proofs: each planted fault must turn its row FAIL."""
    from loop_adapter import adapt
    # PURE CONTROLS FIRST. The fixture-driven part of this self-test can SKIP when no
    # untransplanted copy of the fixture is reachable, and a self-test that skips everything
    # proves nothing. These need no fixture, so they run and are reported either way.
    pure = []
    # --- R3 Earwig furniture, ruled 2026-09-22 on the four Soil/Blackout decks.
    # The line is TA-layer furniture quoted from the policy, so the adapter supplies it wherever
    # the deck HAS a TA layer. These controls pin that rule at its own boundary, because the four
    # held decks name no closing stage at all and so could never satisfy row 12 before.
    from loop_adapter import earwig_stages
    for name, names, eligible, want in (
        ('R3: a named exit that is eligible carries the line',
         ['title', 'arrival', 'exit'], {1, 2}, {2}),
        ('R3: a named exit keeps its place even when it is not last',
         ['exit', 'arrival', 'independent'], {0, 1, 2}, {0}),
        ('R3: a deck naming NO closing stage puts it on the last ELIGIBLE stage',
         ['ido', 'independent', 'lundy_stage', 'unnamed'], {1, 3}, {3}),
        ('R3: it never lands on a stage that gets no TA card',
         ['independent', 'lundy_stage'], {0}, {0}),
        ('R3: a named exit that is not eligible falls back to the last eligible stage',
         ['exit', 'independent'], {1}, {1}),
        ('R3 RED PROOF: a deck with no eligible stage gets no line, so row 12 FAILs and it is HELD',
         ['title'], set(), set()),
    ):
        pure.append((name, earwig_stages(names, eligible) == want))

    # --- STOP-C1/C2 SCIENCE IDENTITY, ruled 2026-09-22. Pure controls: they build their own
    # documents, so they need no fixture and can never skip. Each one pins a clause of the ruling
    # at the boundary where it could silently stop holding.
    from deck_dom import EYEBROW_STAGE, EYEBROW_ORDINAL_BASE

    NEUTRAL = 'the next part of the work'
    # A phrase the STAGE_NAMES word table claims for 'arrival'. Used to make an EARLIER route win,
    # which is the only way the oracle and the declaration can disagree once the eyebrow runs last.
    CLAIMED = 'start with what you know'

    def _sci(rows, head_title='Photosynthesis today'):
        out = ['<html><head><title>%s</title></head><body>' % head_title]
        for i, (lab, heading, panel) in enumerate(rows):
            out.append('<section class="slide" data-timer="5">'
                       '<span class="slide-tag tag-x">%s</span>'
                       '<h2 id="title-a%d">%s</h2>%s</section>'
                       % (lab, i, heading, '<div class="lundy">p</div>' if panel else ''))
        return ''.join(out) + '</body></html>'

    def _names(labels):
        return [stage_name(x) for x in stages(parse(_sci([(l, NEUTRAL, False) for l in labels])))]

    def _row(html, n):
        return next(x['status'] for x in verify(html, html, '', set()) if x['row'] == n)

    # C1 -- every label the generator emits resolves, and resolves to the ruled name. The two
    # ordinal labels are excluded here and tested by C3/C4, where their ruled behaviour lives.
    solo = {lab: _names([lab])[0] for lab in EYEBROW_STAGE
            if EYEBROW_STAGE[lab] not in EYEBROW_ORDINAL_BASE}
    pure.append(('C1: every ruled eyebrow label resolves to its ruled name (%d labels)'
                 % len(solo),
                 all(solo[lab] == EYEBROW_STAGE[lab] for lab in solo)))
    # C2 RED PROOF -- a label outside the generator's emitted vocabulary is never a quiet pass.
    pure.append(('C2 RED PROOF: an eyebrow text outside the emitted set names the stage "unnamed"',
                 _names(['Zzz Quux Nonmatching']) == ['unnamed']))
    # C3 -- the conflation the eyebrow alone cannot settle, resolved by DECLARED ORDER.
    pure.append(('C3: the second "I do" and "We do" in document order are ido2 / wedo2',
                 _names(['I do', 'We do', 'I do', 'We do'])
                 == ['ido', 'wedo', 'ido2', 'wedo2']))
    pure.append(('C3: an explicit "I do 2" after its "I do" is honoured as declared',
                 _names(['I do', 'I do 2', 'We do', 'We do 2'])
                 == ['ido', 'ido2', 'wedo', 'wedo2']))
    # C4 RED PROOF -- label and order contradicting each other is RED, not a silent choice.
    pure.append(('C4 RED PROOF: an "I do 2" declared before any "I do" is RED for that deck',
                 _names(['I do 2', 'I do']) == ['unnamed', 'ido']))
    pure.append(('C4 RED PROOF: the same holds for "We do 2" before any "We do"',
                 _names(['We do 2', 'We do']) == ['unnamed', 'wedo']))
    # C5 -- THE PLACEMENT. The eyebrow runs LAST, so a stage an earlier route already names is
    # never renamed by it. This is what keeps 2123 Humanities stages at 0 names changed.
    pure.append(('C5: the eyebrow never overrides a name an earlier route already gave',
                 [stage_name(x) for x in
                  stages(parse(_sci([('I do', CLAIMED, False)])))] == ['arrival']))

    # C6/C7 RED PROOFS -- an empty set is not a pass (STOP-C2 ruling 3). The subset is asserted
    # against what the deck DECLARES before its contents are judged. Both rows passed with an
    # empty bad-list on the very decks whose stages they were meant to be testing.
    d_ok = _sci([('Opening', NEUTRAL, False), ('I do', NEUTRAL, False), ('Exit', NEUTRAL, True)])
    d_title_lost = _sci([('Opening', CLAIMED, False), ('I do', NEUTRAL, False),
                         ('Exit', NEUTRAL, True)])
    d_mod_lost = _sci([('Opening', NEUTRAL, False), ('I do', CLAIMED, True),
                       ('Exit', NEUTRAL, True)])
    pure.append(('C6: row 14 passes when the declared title stage is the one resolved',
                 _row(d_ok, 14) == PASS))
    pure.append(('C6 RED PROOF: row 14 FAILs when a declared title stage resolves to something '
                 'else, instead of passing over an empty set',
                 _row(d_title_lost, 14) == FAIL))
    pure.append(('C7: row 2 passes when the declared modelling stage is the one resolved',
                 _row(d_ok, 2) == PASS))
    pure.append(('C7 RED PROOF: row 2 FAILs when a declared modelling stage resolves to something '
                 'else, instead of passing over an empty set',
                 _row(d_mod_lost, 2) == FAIL))

    # C8 RED PROOF -- the harm case the split exists to prevent, and the check that would have
    # caught the three merged decks: no pupil-response panel may land on the slide that carries
    # the lesson's own title heading.
    d47_ok = _sci([('Opening', 'Photosynthesis today', False), ('Exit', NEUTRAL, True)])
    d47_bad = _sci([('Opening', 'Photosynthesis today', True), ('Exit', NEUTRAL, True)])
    pure.append(('C8: row 47 passes when the deck-title slide carries no panel',
                 _row(d47_ok, 47) == PASS))
    pure.append(('C8 RED PROOF: row 47 FAILs when a panel lands on the slide carrying the deck '
                 'title heading',
                 _row(d47_bad, 47) == FAIL))

    # --- SECOND FIXTURE, ruled 2026-09-21. The fixture-driven battery below takes its only
    # fixture from a NINE-stage deck that types its own stages
    # title/arrival/starter/ido/wedo/ido2/wedo2/independent/exit -- the single shape on which
    # identity-by-data-type and identity-by-declaration agree stage for stage. Measured: with a
    # pre-transplant fixture supplied, that battery is 35 PASS under BOTH oracles, so it could
    # never have caught the ruling-5 defect; and since #613 transplanted its fixture on main it
    # SKIPS 29 of its 35 checks outright. This fixture exists so the two readings can DISAGREE
    # inside the battery, and it is pure: it needs no untransplanted copy of anything, so it
    # runs on every invocation rather than skipping with the rest.
    #
    # The bytes are a snapshot of a deck the estate really ships, not an invented fixture, and
    # the claim is auditable rather than asserted -- re-checked on every run, not at pin time:
    #     git show AUT1_BYTES_COMMIT:AUT1_DECK | sha256sum   ==   AUT1_SHA256
    AUT1_FIXTURE = 'tools/hum/fixtures/aut1_twelve_stage_v1_base.html'
    AUT1_DECK = 'Humanities_Teesside/Teaching_Packs/BUILD/HTML/BUILD_Humanities_W3.html'
    AUT1_BYTES_COMMIT = 'aed400da53a7e85b7e501b78e1e9c564bab24bad'
    AUT1_SHA256 = 'ab9f6abd62ef33df3bad621267aec70a5ccad6f765de71d623e55f13f0a5e2c5'
    import hashlib, subprocess
    fx = root / AUT1_FIXTURE
    raw = fx.read_bytes() if fx.exists() else b''
    pure.append(('AUT1 fixture: the snapshot is present and matches its pinned digest',
                 bool(raw) and hashlib.sha256(raw).hexdigest() == AUT1_SHA256))
    try:
        g = subprocess.run(['git', '-C', str(root), 'show',
                            AUT1_BYTES_COMMIT + ':' + AUT1_DECK], capture_output=True)
        prov = g.returncode == 0 and hashlib.sha256(g.stdout).hexdigest() == AUT1_SHA256
        note = '' if prov else (' -- git bytes differ from the snapshot' if g.returncode == 0
                                else ' -- git could not produce the object')
    except Exception as exc:                                    # noqa: BLE001
        prov, note = False, ' -- %s' % type(exc).__name__
    pure.append(('AUT1 fixture: git show %s:%s still equals the snapshot%s'
                 % (AUT1_BYTES_COMMIT[:8], AUT1_DECK.rsplit('/', 1)[-1], note), prov))

    if raw:
        fst = stages(parse(raw.decode('utf-8', 'replace')))
        declared = [stage_name(s) for s in fst]
        typed = [(s.attrs.get('data-type') or '').strip() or 'unnamed' for s in fst]

        def _split(names):
            return ([n for n in names if n not in MODELLING_STAGES and n != 'title'],
                    [n for n in names if n in MODELLING_STAGES],
                    [n for n in names if n == 'title'])
        de, dm, dt = _split(declared)
        te, tm, tt = _split(typed)
        pure.append(('AUT1 fixture: it is the twelve-stage Autumn 1 shape the rule was written for',
                     len(fst) == 12))
        # What the deck says about ITSELF if identity came from the type attribute. Recorded as
        # the defect being guarded against, never as an expectation of this oracle.
        pure.append(('AUT1 fixture: identity by data-type would give eligible 4 / modelling 7 / title 1',
                     (len(te), len(tm), len(tt)) == (4, 7, 1)))
        pure.append(('AUT1 fixture: identity by DECLARATION gives eligible 10 / modelling 1 / title 1',
                     (len(de), len(dm), len(dt)) == (10, 1, 1)))
        # THE RED PROOF, and the reason a second fixture was ruled. Six stages this deck types
        # "ido" declare themselves otherwise in their own headings. If stage_name ever returns
        # data-type again, `declared` collapses onto `typed`, `moved` drops to zero and this
        # line FAILs -- which the nine-stage fixture structurally cannot do.
        moved = [(i, typed[i], declared[i]) for i in range(len(fst))
                 if typed[i] in MODELLING_STAGES and declared[i] not in MODELLING_STAGES]
        pure.append(('AUT1 RED PROOF: six stages typed "ido" declare themselves otherwise, so '
                     'identity by data-type would withhold six pupil-response panels',
                     len(moved) == 6 and all(t == 'ido' for _i, t, _d in moved)))
        pure.append(('AUT1 fixture: the one stage that really is I Do keeps its name',
                     dm == ['ido']))
        pure.append(('AUT1 fixture: the oracle names every stage of it',
                     'unnamed' not in declared))

    for name, good in pure:
        print(('  PASS ' if good else '  FAIL ') + name)

    rec = json.loads((root / 'tools/catalogue/HUMANITIES_STRAND.json').read_text())
    rel = 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_Humanities_W4_Explore_Hanukkah_And_The_Theme_Of_Light.html'
    src = root / rel
    r = next(x for x in rec['lessons'] if x['path'].endswith(src.name))
    # The fixture must be the UNTRANSPLANTED deck. Once a build has run, the
    # working tree holds the adapted bytes, so read the pristine ones from git.
    before = None
    try:
        import subprocess
        out = subprocess.run(['git', '-C', str(root), 'show', 'origin/main:' + rel],
                             capture_output=True)
        if out.returncode == 0 and out.stdout:
            before = out.stdout.decode('utf-8', 'replace')
    except Exception:
        pass
    if before is None:
        before = src.read_text(errors='replace')
    if MARK in before:
        print('  SKIP the fixture-driven rows: no untransplanted copy of the fixture is available')
        return all(good for _n, good in pure)
    after, _ = adapt(before, r['pathway'], r['strand'] == 'RE')
    sci = science_texts(root)

    def status(h, row_no, strand=r['strand']):
        return next(x['status'] for x in verify(h, before, strand, sci) if x['row'] == row_no)

    checks = []
    base = verify(after, before, r['strand'], sci)
    checks.append(('clean deck: no FAIL in any static row',
                   not [x for x in base if x['status'] == FAIL]))
    # plant: drop one panel (cut it by its real element extent, not by a regex)
    d0 = parse(after)
    first = sorted([n for n in d0.walk() if n.attrs.get(MARK) and 'lundy' in n.classes()],
                   key=lambda n: n.start)[0]
    dropped = after[:first.start] + after[first.end:]
    checks.append(('row 1 fails when a panel is removed', status(dropped, 1) == FAIL))
    checks.append(('row 45 fails with it too', status(dropped, 45) == FAIL))
    # plant: blank an influence line
    hurt = re.sub(r'(data-loop-part="influence"[^>]*>)[^<]*', r'\1', after, count=1)
    checks.append(('row 5 fails when an influence line is blanked', status(hurt, 5) == FAIL))
    checks.append(('row 45 fails with it', status(hurt, 45) == FAIL))
    # plant: remove the order-enforcing script
    hurt = after.replace('data-hum-t-loop="1"', 'data-broken="1"', 1)
    checks.append(('row 7 fails when the script is removed', status(hurt, 7) == FAIL))
    # plant: a panel filled from the WRONG stage
    ps = [m.start() for m in re.finditer(r'<div class="lundy hum-t-loop"', after)]
    a_start, a_end = ps[1], ps[2]
    b_start, b_end = ps[2], ps[3]
    swapped = after[:a_start] + after[b_start:b_end] + after[a_end:b_start] + after[a_start:a_end] + after[b_end:]
    checks.append(('row 8 fails when two panels are swapped between stages',
                   status(swapped, 8) == FAIL))
    # plant: a belief question in a panel on an RE deck
    hurt = after.replace('data-loop-part="response">Say or show what the source says here:',
                         'data-loop-part="response">Write your own belief about this:', 1)
    checks.append(('row 46 fails when a panel asks for a belief', status(hurt, 46) == FAIL))
    # P1 red proofs
    hurt = after.replace('<details class="loop-disclosure" data-hum-t-disclosure="1">',
                         '<details class="loop-disclosure" data-hum-t-disclosure="1" open>', 1)
    checks.append(('row 15 fails when a disclosure is open by default', status(hurt, 15) == FAIL))
    hurt = after.replace('<summary>Feedback loop</summary>', '<summary>Loop</summary>', 1)
    checks.append(('row 15 fails when the summary is not "Feedback loop"', status(hurt, 15) == FAIL))
    hurt = after.replace('<details class="loop-disclosure" data-hum-t-disclosure="1"><summary>Feedback loop</summary>', '', 1)
    hurt = hurt.replace('</div></details>', '</div>', 1)
    checks.append(('row 15 fails when a panel has no disclosure', status(hurt, 15) == FAIL))
    hurt = re.sub(r'(data-lundy-step="voice" data-state="waiting">)VOICE · [^<]*', r'\1VOICE', after, count=1)
    checks.append(('row 17 fails when the VOICE step drops the task', status(hurt, 17) == FAIL))
    hurt = re.sub(r'(data-action="lundy-voice">)I have answered: [^<]*', r'\1I have answered', after, count=1)
    checks.append(('row 17 fails when the VOICE control drops the task', status(hurt, 17) == FAIL))
    from loop_adapter import voice_label
    from loop_adapter import influence_options
    short = 'Pinpoint the place.'
    checks.append(('row 16 core matches the adapter\'s quoting of a short task ending in a full stop',
                   all(task_core(short) in line for k, _, line in influence_options(short, 'Next') if k != 'explained')))
    long_word = 'Inherited → Complete a belief-and-belonging task and map-skills check'
    checks.append(('VOICE label keeps the 24-character core when a long word straddles the cut',
                   long_word[:24] in voice_label(long_word) and len(voice_label(long_word)) <= 41))
    checks.append(('VOICE label still cuts at a word boundary when one falls after the core',
                   voice_label('Sort the four sources into fact, opinion and evidence cards') ==
                   'Sort the four sources into fact,…'))
    m2 = re.search(r'<p class="loop-line loop-influence" data-loop-part="influence"[^>]*>[^<]*</p>', after)
    hurt = after[:m2.start()] + m2.group(0) + m2.group(0) + after[m2.end():]
    checks.append(('row 16 fails when an influence line is duplicated', status(hurt, 16) == FAIL))
    hurt = re.sub(r'<button type="button" data-next-move="with-support" data-action="lundy-influence">[^<]*</button>', '', after, count=1)
    checks.append(('row 16 fails when an outcome loses its control', status(hurt, 16) == FAIL))
    hurt = after.replace('data-loop-option="with-support">Did it with support → same task, new example',
                         'data-loop-option="with-support">Did it independently → same task, new example', 1)
    checks.append(('row 16 fails when a line does not name its outcome', status(hurt, 16) == FAIL))
    hurt = re.sub(r'(data-loop-option="needs-help">Not yet / needs help → reduce the prompt: )[^<]*', r'\1wait.', after, count=1)
    checks.append(('row 16 fails when a line drops this stage\'s task', status(hurt, 16) == FAIL))
    hurt = after.replace('@media print{.loop-disclosure{display:none}}', '', 1)
    checks.append(('row 15 fails when print no longer excludes the disclosure', status(hurt, 15) == FAIL))
    hurt = after.replace('openOnTaskUse', 'noTaskOpen')
    checks.append(('row 15 fails when the task-use opener is removed', status(hurt, 15) == FAIL))
    tdoc = parse(after)
    tstage = next((x for x in stages(tdoc) if stage_name(x) == 'title'), None)
    if tstage is not None:
        panel_html = re.search(r'<details class="loop-disclosure".*?</details>', after, re.S).group(0)
        close = after.rfind('</', tstage.start, tstage.end)
        hurt = after[:close] + panel_html + after[close:]
        checks.append(('row 14 fails when the Title stage carries a panel', status(hurt, 14) == FAIL))
    # plant: the science exemplar's own panel text
    if sci:
        one = sorted(sci)[0]
        hurt = re.sub(r'(<div class="lundy hum-t-loop"[^>]*>).*?(</div>)',
                      lambda m: m.group(1) + one + m.group(2), after, count=1, flags=re.S)
        checks.append(('row 45.1 fails on science-identical panel text', status(hurt, 45.1) == FAIL))
    # running the adapter twice must refuse, not double the panels
    from loop_adapter import AlreadyAdapted
    try:
        adapt(after, r['pathway'], r['strand'] == 'RE')
        twice_ok = False
    except AlreadyAdapted:
        twice_ok = True
    checks.append(('a second transplant on the same deck is refused', twice_ok))
    # a lundy-status staff note must not reach a pupil response point
    from loop_adapter import stage_task
    lead = ('<section class="slide" data-type="wedo"><h2>We Do</h2>'
            '<div class="lundy-status"><p>SPACE: the evidence statement remains in the '
            'learner\'s chosen communication mode.</p></div>'
            '<p>Sort the six statement cards into two piles.</p></section>')
    st2 = [n for n in parse(lead).walk() if n.tag == 'section'][0]
    got = stage_task(st2)
    checks.append(('a lundy-status staff note is not taken as the pupil task',
                   'evidence statement' not in got and 'statement cards' in got))
    # the obsolete hiding rule must no longer reach the new panel
    from loop_adapter import neutralise_ribbon_hiding
    rule = ('<style>.mbm-classroom .slide[data-classroom-phase]'
            ':not([data-classroom-phase="title"])>.lundy,'
            '.mbm-classroom .slide[data-classroom-phase]'
            ':not([data-classroom-phase="title"])>.lundy-strip{display:none}</style>')
    narrowed, n = neutralise_ribbon_hiding(rule)
    checks.append(('the ribbon-hiding rule is narrowed, not deleted',
                   n == 2 and ':not(.hum-t-loop)' in narrowed and 'display:none' in narrowed))
    keep = '<style>.lundy{border:1px solid #ccc;padding:10px}</style>'
    kept, nk = neutralise_ribbon_hiding(keep)
    checks.append(('a .lundy rule that does not hide is untouched', kept == keep and nk == 0))
    # plant: drop a sentence from the deck
    a_sent = 'Six statement cards are on your table.'
    if a_sent in after:
        checks.append(('row 13 fails when a sentence is dropped',
                       status(after.replace(a_sent, ''), 13) == FAIL))

    ok = all(good for _n, good in pure)
    for name, good in checks:
        print(('  PASS ' if good else '  FAIL ') + name)
        ok = ok and good
    return ok


if __name__ == '__main__':
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test(root) else 1)
    print('usage: verify_loop.py <repo-root> --self-test')
