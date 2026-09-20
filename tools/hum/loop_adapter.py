#!/usr/bin/env python3
"""ORDER HUM-T stage B — the loop transplant adapter.

Puts the science loop panel on every stage of a Humanities/RE deck that invites a
pupil response, filled from THAT STAGE'S OWN TEXT. Nothing is authored: the
response point quotes the stage's own task, the influence branch names the next
stage from the deck's own sequence, and the four Lundy sentences are the deck's own.

RULINGS IMPLEMENTED (STOP-T1)
  R1  triad on every stage that invites a pupil response; I Do stages (teacher
      modelling) carry NO panel, matching the 98 measure.
  R2  the staff code strip goes on the TA layer, never the pupil surface.
  R3  one staff-facing Earwig line at Exit, Feedback Policy body 12/13 verbatim.
  R4  Space conditions, Feedback Policy body 5 verbatim, in the TA brief.
  R5  RE response points are phrased from the source, never from a belief;
      safeguard sentences already present are left untouched.

THREE ADAPTERS, ONE CONTRACT
  quarantined (family A) the dedicated Lundy stage is redistributed into per-stage
                         panels and the emptied stage removed; nothing lost.
  ribbon      (family B) the static ribbon is replaced per stage.
  bare        (family C) panels are added where there is no Lundy furniture.

VB-RUN13 R0 / g27: no week is derived from a path.
"""
from __future__ import annotations
import hashlib, html as ihtml, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deck_dom import parse, stages, stage_name, is_ribbon, splice, Node  # noqa: E402

MODELLING_STAGES = {'ido', 'ido2'}          # teacher modelling: no panel (R1)
MARK = 'data-hum-t'

# Feedback & Marking Policy 2025/2026 (Pilot) Issue 1, BODY numbering.
POLICY_MODALITIES = {
    'BUILD':  'Point, sign, repeat after the adult, demonstrate, Earwig clip, choice board.',
    'GROW':   'Short edit in margin; verbal reply; tick off success criteria; student voice clip.',
    'LAUNCH': 'In-lesson edit; structured verbal response; for full essays, deferred edit.',
}
POLICY_SPACE = [
    'Regulation first. A dysregulated student cannot respond to feedback. Co-regulation, '
    'sensory tools and time take priority over the technical content of the feedback.',
    'No public comparison. No grade boards, no "look how X has improved."',
    'Permission to refuse. A student who declines to respond today is not punished — '
    'refusal is information.',
]
POLICY_EARWIG = ('30-second clip, photo, or one-line context note. Central tags only. '
                 'Listen / look before tagging (Audience).')
POLICY_CODES = [('VF', 'Verbal feedback given here'), ('WS', 'Worked with support'),
                ('I', 'Independent'), ('NS +', 'Next step — one specific thing'),
                ('E', 'Evidence on Earwig'), ('R', 'Responded — loop closed'),
                ('//', 'Self-edit point'), ('?', 'Read this back to me')]

DEFAULT_LUNDY_SENTENCES = ['SPACE stays available.', 'VOICE is received.',
                           'AUDIENCE names back exactly.',
                           'INFLUENCE changes one real next action.']


def esc(s: str) -> str:
    return ihtml.escape(s or '', quote=True)


HIDE_RULE_RX = re.compile(r'([^{}]*\.lundy(?:-strip)?[^{}]*)\{([^{}]*display\s*:\s*none[^{}]*)\}',
                          re.I)


def neutralise_ribbon_hiding(html: str):
    """Sixteen decks carry a DELIBERATE rule that hides the ribbon on every stage
    but title and exit, with the comment "Pupil voice is framed at arrival and
    revisited at the exit, without a repeated process banner competing with each
    model and practical task."

    That rule was written about the old ribbon, which was a banner. Ruling R1
    replaces the ribbon with a working loop that carries this stage's own task, so
    the rule must no longer reach it. The rule is NOT deleted — it keeps its force
    over any legacy ribbon — it is narrowed by :not(.hum-t-loop), which is the
    smallest change that honours both the old intent and the new ruling.

    Returns (html, number_of_selectors_narrowed).
    """
    count = 0

    def fix_rule(m):
        nonlocal count
        sel, body = m.group(1), m.group(2)
        parts = []
        for one in sel.split(','):
            if re.search(r'\.lundy(?:-strip)?(?![\w-])', one):
                one = re.sub(r'(\.lundy(?:-strip)?)(?![\w-])', r'\1:not(.hum-t-loop)', one)
                count += 1
            parts.append(one)
        return ','.join(parts) + '{' + body + '}'

    out = []
    last = 0
    for m in re.finditer(r'<style\b[^>]*>(.*?)</style>', html, re.S | re.I):
        css = m.group(1)
        new = HIDE_RULE_RX.sub(fix_rule, css)
        if new != css:
            out.append(html[last:m.start(1)]); out.append(new); last = m.end(1)
    out.append(html[last:])
    return ''.join(out), count


def family(doc: Node) -> str:
    st = stages(doc)
    ribbons = [n for n in doc.walk() if is_ribbon(n)]
    if any(stage_name(s) == 'lundy_stage' for s in st):
        return 'quarantined'
    return 'ribbon' if ribbons else 'bare'


def _loop_furniture(n: Node) -> bool:
    """Any element the estate has already marked as Lundy furniture.

    Four classes exist in the served decks: `lundy` (the ribbon), `lundy-grid`
    (inside it), `lundy-box` (the quarantined stage's definition boxes) and
    `lundy-status` — a STAFF note present on 18 decks that reads, for example,
    "SPACE: the evidence statement remains in the learner's chosen communication
    mode." Missing that class put a staff sentence into a pupil response point.
    """
    return any(c == 'lundy' or c.startswith('lundy-') for c in n.classes())


def _staff_or_ribbon(n: Node) -> bool:
    return (_loop_furniture(n) or n.attrs.get('data-mbm-guide') == 'staff'
            or 'ta-card' in n.classes())


# Furniture that is not the stage's task: controls, kickers, timers, chips.
CONTROL_TAGS = {'button', 'select', 'option', 'label', 'nav', 'svg', 'dialog', 'details'}
CONTROL_CLASSES = {'kicker', 'chip', 'badge', 'chips', 'controls', 'control', 'timer',
                   'tierbtn', 'tier', 'pill', 'tag', 'meta', 'slide-kicker', 'stage-kicker',
                   'eyebrow', 'toolbar', 'btnrow', 'btn', 'ghost', 'progress'}


def _furniture(n: Node) -> bool:
    if _staff_or_ribbon(n):
        return True
    if n.tag in CONTROL_TAGS:
        return True
    if n.attrs.get('aria-hidden') == 'true':
        return True
    return bool(n.classes() & CONTROL_CLASSES)


def pupil_text(stage: Node) -> str:
    """The stage's own pupil-facing text: ribbon and staff blocks removed."""
    return stage.inner_text(skip=_staff_or_ribbon)


def task_text(stage: Node) -> str:
    """Pupil text with controls, kickers, timers and chips removed as well —
    what is left is the stage's own instruction prose."""
    return stage.inner_text(skip=_furniture)


def short_stage_label(stage: Node, limit: int = 30) -> str:
    """A short name for this stage, for the audience sentence. The full heading
    ("We Do: Which ring? Everyone shows at once") reads as nonsense mid-sentence."""
    raw = (stage.attrs.get('data-title') or '').strip() or stage_heading(stage)
    raw = re.split(r'[:·\u00b7\u2013\u2014]', raw)[0].strip()
    raw = re.sub(r'^[^\w]+', '', raw)
    if not raw:
        raw = stage_name(stage).replace('_', ' ')
    return raw[:limit].rstrip()


def stage_heading(stage: Node) -> str:
    hs = stage.find(lambda n: n.tag in ('h2', 'h3'))
    for h in hs:
        t = h.inner_text().strip()
        if t:
            return t
    return (stage.attrs.get('data-title') or '').strip()


TASK_RX = re.compile(r'([A-Z][^.!?]{12,150}[.!?])')
NEXT_RX = re.compile(r'([^.!?]{0,90}\bwhat happens next\b[^.!?]{0,150}[.!?])', re.I)


def _headings(stage: Node):
    out = [(stage.attrs.get('data-title') or '').strip()]
    out += [h.inner_text().strip()
            for h in stage.find(lambda n: n.tag in ('h1', 'h2', 'h3', 'h4'))]
    # longest first, so a heading that contains another is removed whole
    return sorted({x for x in out if x}, key=len, reverse=True)


OBJECTIVE_RX = re.compile(
    r'(?:Workbook outcome|Learning outcome|Lesson outcome|Objective|Outcome|'
    r'By the end[^:]{0,30}|I can)\s*[:\-–]?\s*([^.!?]{10,160}[.!?]?)', re.I)


def stage_task(stage: Node, limit: int = 120) -> str:
    """The stage's own first instruction sentence — the thing a pupil is asked to do.
    The stage's own headings are stripped first so the task is the task, not the label."""
    txt = task_text(stage)
    # The overview stage is metadata, not an instruction: use the deck's OWN
    # stated objective where it has one.
    if stage_name(stage) == 'title':
        m = OBJECTIVE_RX.search(txt)
        if m:
            t = re.sub(r'\s+', ' ', m.group(1)).strip().rstrip('·-–—,')
            if len(t) > limit:
                t = t[:limit].rsplit(' ', 1)[0] + '…'
            return t
    for h in _headings(stage):
        txt = txt.replace(h, ' ')
    txt = re.sub(r'\s+', ' ', txt).strip()
    # strip leading furniture: timings, pathway/subject kickers, week labels, bullets
    noise = (r'^(?:We Do\s*\d?|I Do\s*\d?|Exit(?: Ticket)?|Arrival|Starter|Independent|'
             r'\d+\s*min(?:ute)?s?\b|GROW|BUILD|LAUNCH|Humanities|Science|RE\b|'
             r'Religious Education|Week\s*\d+|Offline|\d+\s*minutes?\b|Autumn\s*\d|Spring\s*\d|'
             r'Summer\s*\d|Progress SoW|Task|Work|Ticket|Start here|of\s*\d+|'
             r'[\u2000-\u3300\uD83C-\uDBFF\uDC00-\uDFFF]|[·\u00b7:\-–—.,()]|\s)+')
    txt = re.sub(noise, '', txt, flags=re.I).strip()
    best = None
    for m in TASK_RX.finditer(txt):
        cand = m.group(1).strip()
        if len(cand.split()) >= 4:
            best = cand
            break
    if not best:
        hs = _headings(stage)
        best = hs[-1] if hs else ''
    if len(best) > limit:
        best = best[:limit].rsplit(' ', 1)[0] + '…'
    return best


def stage_own_next(stage: Node) -> str:
    """The stage's OWN 'what happens next' sentence, where the deck has one."""
    m = NEXT_RX.search(pupil_text(stage))
    if not m:
        return ''
    t = re.sub(r'\s+', ' ', m.group(1)).strip()
    return t if len(t) <= 190 else t[:190].rsplit(' ', 1)[0] + '…'


def lundy_sentences(doc: Node):
    """The deck's OWN four Lundy sentences, taken from its existing furniture."""
    for n in doc.walk():
        if is_ribbon(n):
            t = n.inner_text()
            got = re.findall(r'((?:SPACE|VOICE|AUDIENCE|INFLUENCE)\b[^.]*\.)', t)
            if len(got) >= 4:
                return got[:4]
    return list(DEFAULT_LUNDY_SENTENCES)


def quarantined_definitions(doc: Node):
    """Family A: everything the dedicated Lundy stage says that is NOT the ribbon
    boilerplate. Carried once into the first panel so removing that stage loses
    nothing in a rendered-text diff (ruling 3)."""
    for s in stages(doc):
        if stage_name(s) == 'lundy_stage':
            txt = s.inner_text(skip=is_ribbon)
            heads = {h.inner_text().strip() for h in s.find(lambda n: n.tag in ('h1','h2','h3','h4'))}
            out, seen = [], set()
            for sent in re.split(r'(?<=[.!?])\s+', txt):
                sent = sent.strip()
                if len(sent) < 12 or sent in heads or sent in seen:
                    continue
                seen.add(sent)
                out.append(sent)
            return out
    return []


def build_panel(stage: Node, index: int, next_title: str, pathway: str,
                is_re: bool, sentences, definitions) -> str:
    task = stage_task(stage)
    head = short_stage_label(stage) or stage_heading(stage)
    modal = POLICY_MODALITIES.get((pathway or '').upper(), POLICY_MODALITIES['GROW'])
    if is_re:
        response = ('Say or show what the source says here: %s' % task)
    else:
        response = ('Say or show your answer here: %s' % task)
    audience = ('At %s, an adult receives it and names back what they heard, in your '
                'words. R goes on only after that.' % (short_stage_label(stage) or 'this stage'))
    own_next = stage_own_next(stage)
    if own_next:
        influence = 'What you said changes what happens next. %s' % own_next
    else:
        influence = ('What you said changes what happens next: %s' % (next_title or head))
    key = hashlib.sha256((task + '|' + (next_title or '')).encode()).hexdigest()[:12]
    steps = []
    labels = {'space': 'SPACE', 'voice': 'VOICE', 'audience': 'AUDIENCE', 'influence': 'INFLUENCE'}
    for i, (k, lab) in enumerate(labels.items()):
        state = 'available' if k == 'space' else 'waiting'
        steps.append('<div class="ls" data-lundy-step="%s" data-state="%s">%s</div>' % (k, state, lab))
    defs = ''
    if definitions:
        defs = ('<ul class="loop-defs">' +
                ''.join('<li>%s</li>' % esc(d) for d in definitions) + '</ul>')
    return (
      '<div class="lundy hum-t-loop" %s="1" data-loop-stage="%d" data-loop-stage-name="%s" '
      'data-loop-key="%s" aria-label="Lundy participation status">'
      '<div class="lundy-grid">%s</div>'
      '<p class="lundy-state" data-lundy-status>SPACE available · VOICE waiting · '
      'AUDIENCE waiting · INFLUENCE waiting</p>'
      '<p class="loop-line loop-response" data-loop-part="response">%s <span class="loop-modes">%s</span></p>'
      '<button type="button" data-action="lundy-voice">I have answered</button>'
      '<p class="loop-line loop-audience" data-loop-part="audience">%s</p>'
      '<button type="button" data-action="lundy-audience">Adult received this response</button>'
      '<p class="loop-line loop-influence" data-loop-part="influence">%s</p>'
      '<button type="button" data-action="lundy-influence">Agree what changes</button>'
      '<p class="loop-result" data-loop-result role="status" aria-live="polite">%s</p>'
      '%s</div>'
    ) % (MARK, index, esc(stage_name(stage)), key,
         ''.join(steps), esc(response), esc(modal), esc(audience), esc(influence),
         esc(' '.join(sentences)), defs)


LOOP_SCRIPT = """
<script data-hum-t-loop="1">
/* ORDER HUM-T: the panel refuses out-of-order operation. Feedback & Marking
   Policy body 3 ("All four conditions must be in order, or the cycle is broken")
   and body 7 ("R must not be added until Audience has happened"). */
(function(){
  var REFUSE_VOICE_FIRST = "Receive the pupil's Voice first. A response can be spoken, pointed, shown, signed, drawn or scribed exactly.";
  var REFUSE_AUDIENCE_NEXT = "Audience comes next. An adult must genuinely receive the response before choosing what changes.";
  function wire(panel){
    var state={voice:false,audience:false,influence:false};
    function step(name){return panel.querySelector('[data-lundy-step="'+name+'"]');}
    function say(msg){var r=panel.querySelector('[data-loop-result]'); if(r) r.textContent=msg;}
    function paint(){
      var m={space:'available',voice:state.voice?'done':'waiting',
             audience:state.audience?'done':(state.voice?'available':'waiting'),
             influence:state.influence?'done':(state.audience?'available':'waiting')};
      Object.keys(m).forEach(function(k){var e=step(k); if(e) e.setAttribute('data-state',m[k]);});
      var s=panel.querySelector('[data-lundy-status]');
      if(s) s.textContent='SPACE '+m.space+' · VOICE '+m.voice+' · AUDIENCE '+m.audience+' · INFLUENCE '+m.influence;
    }
    function on(action,fn){
      var b=panel.querySelector('[data-action="'+action+'"]');
      if(b) b.addEventListener('click',function(){fn(b);});
    }
    on('lundy-voice',function(b){ state.voice=true; b.disabled=true;
      say('Voice received. An adult now reads or watches it back.'); paint(); });
    on('lundy-audience',function(b){
      if(!state.voice){ say(REFUSE_VOICE_FIRST); return; }
      state.audience=true; b.disabled=true;
      say('Audience done — the adult named it back. R may go on now.'); paint(); });
    on('lundy-influence',function(b){
      if(!state.voice){ say(REFUSE_VOICE_FIRST); return; }
      if(!state.audience){ say(REFUSE_AUDIENCE_NEXT); return; }
      state.influence=true; b.disabled=true;
      say('Influence agreed — one real thing changes next.'); paint(); });
    paint();
  }
  function init(){
    var ps=document.querySelectorAll('.hum-t-loop');
    for(var i=0;i<ps.length;i++) wire(ps[i]);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
  else init();
})();
</script>
"""

LOOP_CSS = """
<style data-hum-t-loop-css="1">
.hum-t-loop .loop-line{margin:8px 0}
.hum-t-loop .loop-modes{display:block;font-size:.92em}
.hum-t-loop button{min-height:44px;min-width:44px;margin:4px 6px 4px 0;cursor:pointer}
.hum-t-loop button[disabled]{opacity:.6;cursor:default}
/* State is shown by weight and a mark, never by fading the text: a faded label
   fails colour contrast at 390px (measured 3.72 against the house panel). */
.hum-t-loop .ls{font-weight:600}
.hum-t-loop .ls[data-state="done"]{font-weight:900}
.hum-t-loop .ls[data-state="done"]::after{content:" \2713"}
.hum-t-loop .ls[data-state="available"]{font-weight:800}
.hum-t-loop .loop-defs{margin:6px 0 0;padding-left:1.1em}
.hum-t-loop .loop-result{margin:6px 0 0;min-height:1.2em}
</style>
"""


def ta_brief(is_exit: bool) -> str:
    """R2 + R4 (+ R3 at Exit) — staff layer only, never the pupil surface."""
    codes = ' · '.join('<b>%s</b> %s' % (esc(c), esc(m)) for c, m in POLICY_CODES)
    space = ''.join('<li>%s</li>' % esc(s) for s in POLICY_SPACE)
    earwig = ('<p class="ta-earwig"><b>Earwig, lean capture (E):</b> %s</p>' % esc(POLICY_EARWIG)) if is_exit else ''
    return (
      '<div class="ta-card hum-t-ta" %s="1" data-mbm-guide="staff">'
      '<p><b>Feedback codes (staff):</b> %s</p>'
      '<p><b>Space — the conditions that make response possible:</b></p><ul>%s</ul>'
      '%s'
      '<p class="ta-source">Feedback &amp; Marking Policy 2025/2026 (Pilot), Issue 1 — '
      'body sections 5, 11, 12 and 13, quoted.</p>'
      '</div>'
    ) % (MARK, codes, space, earwig)


class AlreadyAdapted(Exception):
    pass


def adapt(html: str, pathway: str, is_re: bool):
    # Running the adapter twice would double every panel and inject the script
    # twice. Refuse loudly rather than produce a deck with two loops per stage.
    if MARK in html:
        raise AlreadyAdapted('deck already carries %s panels — refusing to transplant twice' % MARK)
    html, narrowed = neutralise_ribbon_hiding(html)
    doc = parse(html)
    fam = family(doc)
    st = stages(doc)
    sentences = lundy_sentences(doc)
    definitions = quarantined_definitions(doc) if fam == 'quarantined' else []
    eligible = [s for s in st if stage_name(s) not in MODELLING_STAGES
                and stage_name(s) != 'lundy_stage']
    titles = [stage_heading(s) or (s.attrs.get('data-title') or '') for s in st]
    edits = []
    panels = 0
    for s in eligible:
        i = st.index(s)
        nxt = ''
        for j in range(i + 1, len(st)):
            if stage_name(st[j]) != 'lundy_stage':
                nxt = titles[j]
                break
        if not nxt:
            # last stage: fall back to the deck's own closing stage label
            nxt = titles[-1] if titles else (stage_heading(s) or '')
        # the removed stage's own words are carried ONCE, on the first panel
        panel = build_panel(s, i, nxt, pathway, is_re, sentences,
                            definitions if panels == 0 else [])
        ta = ta_brief(stage_name(s) in ('exit', 'complete'))
        close = html.rfind('</', s.start, s.end)
        edits.append((close, close, panel + ta))
        panels += 1
    # family A: remove the emptied dedicated Lundy stage (its definitions have
    # already been carried into every panel, so nothing is lost)
    dropped = [(s.start, s.end) for s in st if stage_name(s) == 'lundy_stage']
    for a, b in dropped:
        edits.append((a, b, ''))
    # remove every pre-existing ribbon that sits inside a stage, EXCEPT any that
    # sits inside a stage already being removed whole (that would overlap)
    for s in st:
        for r in s.find(is_ribbon):
            if r.attrs.get(MARK):
                continue
            if any(a <= r.start and r.end <= b for a, b in dropped):
                continue
            edits.append((r.start, r.end, ''))
    # inject the script + css once, before </body>
    b = html.rfind('</body>')
    if b < 0:
        b = len(html)
    edits.append((b, b, LOOP_CSS + LOOP_SCRIPT))
    out = splice(html, edits)
    return out, {'family': fam, 'panels': panels, 'hide_rules_narrowed': narrowed,
                 'stages_before': len(st), 'eligible': len(eligible),
                 'modelling_skipped': sum(1 for s in st if stage_name(s) in MODELLING_STAGES),
                 'lundy_stage_removed': sum(1 for s in st if stage_name(s) == 'lundy_stage'),
                 'ribbons_removed': sum(1 for s in st for r in s.find(is_ribbon)
                                        if not r.attrs.get(MARK)
                                        and not any(a <= r.start and r.end <= b for a, b in dropped))}
