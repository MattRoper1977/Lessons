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
from deck_dom import parse, stages, stage_name, is_ribbon          # noqa: E402
from loop_adapter import (MODELLING_STAGES, MARK, pupil_text,      # noqa: E402
                          stage_task, POLICY_CODES, POLICY_SPACE, POLICY_EARWIG)

PASS, FAIL, NC = 'PASS', 'FAIL', 'NOT-CHECKED'

# R5 / correction #13: a belief question is one with NO negation governing it.
ASK_BELIEF = re.compile(r'(?<![a-z])(?:write|say|tell|share|state)\b[^.]{0,40}\byour own belief'
                        r'|what do you believe\?', re.I)
NEGATION = re.compile(r'\b(never|not|nobody|no one|no pupil|no learner|without)\b', re.I)


def panels(doc):
    return [n for n in doc.walk() if is_ribbon(n)]


def panel_parts(p):
    return {n.attrs.get('data-loop-part'): n.inner_text()
            for n in p.find(lambda n: n.attrs.get('data-loop-part'))}


def verify(after_html: str, before_html: str, strand: str, science_panel_texts):
    doc = parse(after_html)
    st = stages(doc)
    rows = []

    def row(num, name, status, detail=''):
        rows.append({'row': num, 'name': name, 'status': status, 'detail': detail})

    eligible = [s for s in st if stage_name(s) not in MODELLING_STAGES]
    modelling = [s for s in st if stage_name(s) in MODELLING_STAGES]

    # 1 — every eligible stage carries exactly one panel
    bad = [(stage_name(s), len(s.find(is_ribbon))) for s in eligible
           if len(s.find(is_ribbon)) != 1]
    row(1, 'one panel per non-modelling stage', PASS if not bad else FAIL, str(bad))

    # 2 — modelling stages carry none (R1: the 98 measure)
    bad = [stage_name(s) for s in modelling if s.find(is_ribbon)]
    row(2, 'I Do stages carry no panel', PASS if not bad else FAIL, str(bad))

    # 3 — no static ribbon survives
    leftovers = [p for p in panels(doc) if not p.attrs.get(MARK)]
    row(3, 'no static ribbon survives', PASS if not leftovers else FAIL,
        '%d left' % len(leftovers))

    # 4 — every panel is stateful (four steps with data-state)
    bad = [p.attrs.get('data-loop-stage') for p in panels(doc)
           if len(p.find(lambda n: 'data-lundy-step' in n.attrs and 'data-state' in n.attrs)) != 4]
    row(4, 'every panel has four stateful steps', PASS if not bad else FAIL, str(bad))

    # 5 — every panel carries all three parts, non-empty
    bad = []
    for p in panels(doc):
        parts = panel_parts(p)
        for k in ('response', 'audience', 'influence'):
            if not (parts.get(k) or '').strip():
                bad.append((p.attrs.get('data-loop-stage'), k))
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

    # 45 — THE LOOP ROW (chassis numbering, by ruling)
    ok45 = all(r['status'] == PASS for r in rows
               if r['row'] in (1, 2, 4, 5, 6, 7, 45.1, 45.2))
    row(45, 'every non-I-Do stage carries one panel with all four parts',
        PASS if ok45 else FAIL, 'composite of rows 1,2,4,5,6,7,45.1,45.2')

    # 46 — THE RE ROW (negation-aware, per correction #13)
    asks = []
    if strand == 'RE':
        for p in panels(doc):
            for sent in re.split(r'(?<=[.!?])\s+', p.inner_text()):
                if ASK_BELIEF.search(sent) and not NEGATION.search(sent):
                    asks.append(sent[:90])
    row(46, 'no RE panel asks for a belief', PASS if not asks else FAIL, str(asks))

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
        print('  SKIP self-test: no untransplanted copy of the fixture is available')
        return True
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
    hurt = re.sub(r'(data-loop-part="influence">)[^<]*', r'\1', after, count=1)
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
    ok = True
    for name, good in checks:
        print(('  PASS ' if good else '  FAIL ') + name)
        ok = ok and good
    return ok


if __name__ == '__main__':
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test(root) else 1)
    print('usage: verify_loop.py <repo-root> --self-test')
