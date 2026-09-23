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

P1 SHAPE (Matt Roper, overnight order 2026-09-21; applied to batches not yet built,
batches already built land as-is and are re-cut in a follow-on batch). The reading is
mine and is recorded for correction:
  P1-1  no Title-stage panel: the overview stage is metadata, not a response point.
  P1-2  RULED 2026-09-21: four response outcomes, one influence line each, phrased for
        the stage's task (not yet / needs help -> reduce the prompt; with support -> same
        task, new example; independently -> explain a reason; and explained -> move on).
  P1-3  the panel sits inside a collapsed "Feedback loop" disclosure per stage, opened
        by the pupil or adult with a real tap on its summary.
  P1-4  VOICE names the stage's task: the VOICE step and the "I have answered" control
        carry the task the response point quotes, not the bare word.

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
    'BUILD':  'Point, sign, repeat after the adult, demonstrate, evidence clip, choice board.',
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
                ('E', "Evidence on the school's digital evidence platform"), ('R', 'Responded — loop closed'),
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
# 'science-meta' and 'slide-tag' are the Science chassis's own names for the meta line and the
# stage chip. The match is on exact class names, so without them the deck-constant line
# "GCSE BIOLOGY FOUNDATION · W14 · LESSON 1 · 4 MINUTES" (and the Grow "You do" chip) was read
# as the stage's task on 61 of PASS C batch 1's 64 panels, and every VOICE control in a deck
# named the same header instead of its stage's task (P1-4).
CONTROL_TAGS = {'button', 'select', 'option', 'label', 'nav', 'svg', 'dialog', 'details'}
CONTROL_CLASSES = {'kicker', 'chip', 'badge', 'chips', 'controls', 'control', 'timer',
                   'tierbtn', 'tier', 'pill', 'tag', 'slide-tag', 'meta', 'science-meta',
                   'slide-kicker', 'stage-kicker',
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


CONFIG_RX = re.compile(r'<script[^>]*id="lesson-config"[^>]*>(.*?)</script>', re.S)


def deck_config(html: str) -> dict:
    """The deck's own lesson-config, when it carries one (48 of the 73 do)."""
    m = CONFIG_RX.search(html)
    if not m:
        return {}
    try:
        cfg = json.loads(m.group(1))
    except ValueError:
        return {}
    return cfg if isinstance(cfg, dict) else {}


INFLUENCE_OUTCOMES = (
    # key, the pupil's response outcome (the control's label), the ruled next move
    ('needs-help', 'Not yet / needs help', 'reduce the prompt'),
    ('with-support', 'Did it with support', 'same task, new example'),
    ('independent', 'Did it independently', 'explain a reason'),
    ('explained', 'Did it and explained', 'move on'),
)


def influence_options(task: str, next_title: str = '', own_next: str = ''):
    """P1-2 (RULING, Matt Roper 2026-09-21): the four response outcomes are the
    canonical influence outcomes, one line each, phrased for THIS stage's task:
    not yet / needs help -> reduce the prompt; did it with support -> same task, new
    example; did it independently -> explain a reason; did it and explained -> move on.
    Nothing is authored here: the outcome and the move are the ruling's words, the
    task is the stage's own (the one row 8 proves), and the fourth line's destination
    is the deck's own 'what happens next' sentence or its own next stage. The four
    prefixes differ, so no two lines in one panel can be identical (row 16 reds on a
    repeat all the same)."""
    t = (task or '').strip().rstrip('.!?\u2026')
    if own_next:
        move_on = 'Did it and explained \u2192 move on. %s' % own_next
    elif next_title:
        move_on = 'Did it and explained \u2192 move on: %s' % next_title
    else:
        move_on = 'Did it and explained \u2192 move on to the next stage.'
    lines = {
        'needs-help': ('Not yet / needs help \u2192 reduce the prompt: take the first step of '
                       '\u201c%s\u201d with the smallest prompt that works, then wait.' % t),
        'with-support': ('Did it with support \u2192 same task, new example: \u201c%s\u201d again '
                         'with a fresh example and one prompt fewer.' % t),
        'independent': ('Did it independently \u2192 explain a reason: ask why for \u201c%s\u201d '
                        'and take the reason in the pupil\u2019s own mode.' % t),
        'explained': move_on,
    }
    return [(k, label, lines[k]) for k, label, _ in INFLUENCE_OUTCOMES]


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


VOICE_LABEL_LIMIT = 40
VOICE_LABEL_CORE = 24   # verify_loop row 17 looks for the task's first 24 characters


def voice_label(task: str) -> str:
    """The task as the VOICE step and its control name it: at most 40 characters,
    cut at a word boundary where one falls after the 24-character core the
    verifier proves, and at the hard limit otherwise (a long word straddling
    the cut must not shorten the label below the core: correction #14)."""
    if len(task) <= VOICE_LABEL_LIMIT:
        return task
    cut = task[:VOICE_LABEL_LIMIT]
    soft = cut.rsplit(' ', 1)[0]
    return (soft if len(soft) >= VOICE_LABEL_CORE else cut) + '…'


def build_panel(stage: Node, index: int, next_title: str, pathway: str,
                is_re: bool, sentences, definitions, cfg=None) -> str:
    cfg = cfg or {}
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
    moves = influence_options(task, next_title or head, own_next)
    influence_lines = ''.join(
        '<p class="loop-line loop-influence" data-loop-part="influence" data-loop-option="%s">%s</p>'
        % (esc(k), esc(line)) for k, _, line in moves)
    branch = ('<div class="branch" aria-label="What the pupil did: choose the outcome, and the next move follows">' +
              ''.join('<button type="button" data-next-move="%s" data-action="lundy-influence">%s</button>'
                      % (esc(k), esc(label)) for k, label, _ in moves) + '</div>')
    key = hashlib.sha256((task + '|' + (next_title or '')).encode()).hexdigest()[:12]
    voice_task = voice_label(task)
    steps = []
    labels = {'space': 'SPACE', 'voice': 'VOICE · %s' % voice_task, 'audience': 'AUDIENCE',
              'influence': 'INFLUENCE'}
    for i, (k, lab) in enumerate(labels.items()):
        state = 'available' if k == 'space' else 'waiting'
        steps.append('<div class="ls" data-lundy-step="%s" data-state="%s">%s</div>' % (k, state, esc(lab)))
    defs = ''
    if definitions:
        defs = ('<ul class="loop-defs">' +
                ''.join('<li>%s</li>' % esc(d) for d in definitions) + '</ul>')
    return (
      '<details class="loop-disclosure" data-hum-t-disclosure="1">'
      '<summary>Feedback loop</summary>'
      '<div class="lundy hum-t-loop" %s="1" data-loop-stage="%d" data-loop-stage-name="%s" '
      'data-loop-key="%s" aria-label="Lundy participation status">'
      '<div class="lundy-grid">%s</div>'
      '<p class="lundy-state" data-lundy-status>SPACE available · VOICE waiting · '
      'AUDIENCE waiting · INFLUENCE waiting</p>'
      '<p class="loop-line loop-response" data-loop-part="response">%s <span class="loop-modes">%s</span></p>'
      '<button type="button" data-action="lundy-voice">I have answered: %s</button>'
      '<p class="loop-line loop-audience" data-loop-part="audience">%s</p>'
      '<button type="button" data-action="lundy-audience">Adult received this response</button>'
      '%s'
      '%s'
      '<p class="loop-result" data-loop-result role="status" aria-live="polite">%s</p>'
      '%s</div></details>'
    ) % (MARK, index, esc(stage_name(stage)), key,
         ''.join(steps), esc(response), esc(modal), esc(voice_task), esc(audience), influence_lines,
         branch, esc(' '.join(sentences)), defs)


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
    var moves=panel.querySelectorAll('[data-action="lundy-influence"]');
    for(var k=0;k<moves.length;k++){ (function(b){ b.addEventListener('click',function(){
      if(!state.voice){ say(REFUSE_VOICE_FIRST); return; }
      if(!state.audience){ say(REFUSE_AUDIENCE_NEXT); return; }
      state.influence=true; state.move=b.getAttribute('data-next-move')||'';
      for(var j=0;j<moves.length;j++) moves[j].disabled=true;
      say('Influence agreed — '+(b.textContent||'').trim()+': one real thing changes next.'); paint(); }); })(moves[k]); }
    paint();
  }
  /* P1-3: the disclosure opens on a real tap of its summary OR when the stage's own
     task is used (a control, field or chip of the stage outside the disclosure). */
  function openOnTaskUse(d){
    var stage=d.parentElement;
    while(stage && !(stage.classList && stage.classList.contains('slide'))) stage=stage.parentElement;
    if(!stage) return;
    function used(ev){
      var t=ev.target; if(!t || !t.closest || d.contains(t)) return;
      if(t.closest('button,input,select,textarea,[role="button"],[data-chip],.chip')) d.open=true;
    }
    stage.addEventListener('click',used,true);
    stage.addEventListener('input',used,true);
    stage.addEventListener('change',used,true);
  }
  function init(){
    var ps=document.querySelectorAll('.hum-t-loop');
    for(var i=0;i<ps.length;i++) wire(ps[i]);
    var ds=document.querySelectorAll('details.loop-disclosure');
    for(var j=0;j<ds.length;j++) openOnTaskUse(ds[j]);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
  else init();
})();
</script>
"""

# The CSS escape for the tick is written "\\2713" because this is a Python string: a single
# backslash made "\\271" an octal escape, and the page showed " \u00b93" where the tick belongs.
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
.hum-t-loop .ls[data-state="done"]::after{content:" \\2713"}
.hum-t-loop .ls[data-state="available"]{font-weight:800}
.hum-t-loop .loop-defs{margin:6px 0 0;padding-left:1.1em}
.hum-t-loop .loop-result{margin:6px 0 0;min-height:1.2em}
.hum-t-loop .branch{display:flex;flex-wrap:wrap;gap:4px}
.loop-disclosure{margin:10px 0}
.loop-disclosure>summary{cursor:pointer;min-height:44px;display:flex;align-items:center;font-weight:700}
@media print{.loop-disclosure{display:none}}
</style>
"""


def earwig_stages(names: list[str], eligible: set) -> set:
    """Pure. Which stage indexes carry the R3 Earwig line, by the ruling of 2026-09-22 on the
    four Soil/Blackout decks: the line is TA-LAYER FURNITURE quoted from the policy, not
    authoring, so the adapter supplies it where the deck has a TA layer.

    A deck that NAMES its closing stage keeps the behaviour it already had -- the named exit or
    complete stage carries the line, wherever it sits. A deck that names no closing stage at all
    (the four held decks run ... independent, lundy_stage, unnamed) had no TA layer carrying the
    line and so could never pass verifier row 12; its LAST stage carries it instead. Nothing that
    already had the line loses it, and nothing gains it twice.

    A deck with no stages at all gets no TA layer, so row 12 still FAILs and the deck is HELD by
    name -- which is the ruled outcome, not a gap."""
    named = {i for i, n in enumerate(names) if n in ('exit', 'complete') and i in eligible}
    if named:
        return named
    return {max(eligible)} if eligible else set()


def ta_brief(is_exit: bool) -> str:
    """R2 + R4 (+ R3 at Exit) — staff layer only, never the pupil surface."""
    codes = ' · '.join('<b>%s</b> %s' % (esc(c), esc(m)) for c, m in POLICY_CODES)
    space = ''.join('<li>%s</li>' % esc(s) for s in POLICY_SPACE)
    earwig = ((EVIDENCE_LABEL + ' %s</p>') % esc(POLICY_EARWIG)) if is_exit else ''
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


# No product name on any public page (ruling 2026-09-23, CX2-b §2). The TA layer is served on
# madebymatt.uk, so it is public. Decks already transplanted cannot be re-run through adapt()
# (AlreadyAdapted), and re-running from their pre-transplant bytes would drag in unrelated
# drift, so retext() rewrites ONLY the strings this module itself emitted, in place: each retired
# fragment is rebuilt exactly as the earlier ta_brief()/build_panel() wrote it (same esc()), and
# replaced with what the current constants write. Nothing else in the deck is touched.
EVIDENCE_LABEL = ('<p class="ta-evidence"><b>Evidence capture (E) — the school&#x27;s digital evidence '
                  'platform:</b>')
PRODUCT_NAME_RX = re.compile(r'\bEarwig\b', re.I)
RETIRED_TA_FRAGMENTS = [
    # (name, old fragment as previously emitted, fragment the current constants emit)
    ('code E', '<b>E</b> %s' % esc('Evidence on Earwig'),
     '<b>E</b> %s' % esc(dict(POLICY_CODES)['E'])),
    ('BUILD modality', esc('Point, sign, repeat after the adult, demonstrate, Earwig clip, choice board.'),
     esc(POLICY_MODALITIES['BUILD'])),
    ('evidence label', '<p class="ta-earwig"><b>Earwig, lean capture (E):</b>', EVIDENCE_LABEL),
]


class ProductNameRemains(Exception):
    pass


def retext(html: str):
    """Pure. Rewrite this module's own retired TA-layer strings in an already-transplanted deck.
    Returns (html, {fragment name: count}). Refuses a deck that is not transplanted, and refuses
    if the product name survives anywhere after the rewrite -- a name this mode did not write is
    reported, never silently left or silently edited."""
    if MARK not in html:
        raise ValueError('not a transplanted deck (no %s): retext only rewrites its own strings' % MARK)
    counts = {}
    for name, old, new in RETIRED_TA_FRAGMENTS:
        counts[name] = html.count(old)
        html = html.replace(old, new)
    left = [m.start() for m in PRODUCT_NAME_RX.finditer(html)]
    if left:
        raise ProductNameRemains('%d product-name occurrence(s) not written by this module, first at %d: %r'
                                 % (len(left), left[0], html[max(0, left[0] - 40):left[0] + 40]))
    return html, counts


def adapt(html: str, pathway: str, is_re: bool):
    # Running the adapter twice would double every panel and inject the script
    # twice. Refuse loudly rather than produce a deck with two loops per stage.
    if MARK in html:
        raise AlreadyAdapted('deck already carries %s panels — refusing to transplant twice' % MARK)
    html, narrowed = neutralise_ribbon_hiding(html)
    doc = parse(html)
    cfg = deck_config(html)
    fam = family(doc)
    st = stages(doc)
    sentences = lundy_sentences(doc)
    definitions = quarantined_definitions(doc) if fam == 'quarantined' else []
    eligible = [s for s in st if stage_name(s) not in MODELLING_STAGES
                and stage_name(s) not in ('lundy_stage', 'title')]   # P1-1
    titles = [stage_heading(s) or (s.attrs.get('data-title') or '') for s in st]
    edits = []
    panels = 0
    # R3 furniture: which stages carry the Earwig line. Computed over the ELIGIBLE stages,
    # because a TA card is emitted only where a panel is -- so the line can only land where the
    # deck actually has a TA layer (ruling of 2026-09-22).
    earwig_at = earwig_stages([stage_name(x) for x in st], {st.index(x) for x in eligible})
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
                            definitions if panels == 0 else [], cfg)
        ta = ta_brief(i in earwig_at)
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


def _retext_self_test() -> int:
    """RED and GREEN controls for retext(), run on a minimal transplanted deck."""
    ok = True
    def control(name, passed):
        nonlocal ok; ok = ok and passed
        print(('GREEN ' if passed else 'RED   ') + name)
    old = ('<div %s="1"><p>%s</p>%s<p>%s</p></div>' % (MARK, RETIRED_TA_FRAGMENTS[0][1],
           RETIRED_TA_FRAGMENTS[2][1], RETIRED_TA_FRAGMENTS[1][1]))
    new, counts = retext(old)
    control('every retired fragment is rewritten once', counts == {n: 1 for n, _, _ in RETIRED_TA_FRAGMENTS})
    control('no product name survives', not PRODUCT_NAME_RX.search(new))
    control('idempotent: a rewritten deck rewrites to itself', retext(new)[0] == new)
    try:
        retext(old + '<p>Upload it to Earwig later.</p>'); control('RED: a planted extra name is refused', False)
    except ProductNameRemains:
        control('RED: a planted extra name is refused', True)
    try:
        retext('<p>%s</p>' % RETIRED_TA_FRAGMENTS[0][1]); control('RED: a deck this module never transplanted is refused', False)
    except ValueError:
        control('RED: a deck this module never transplanted is refused', True)
    return 0 if ok else 1


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='loop_adapter in-place modes (the transplant itself runs via build_all.py)')
    ap.add_argument('--retext', nargs='*', metavar='DECK', help='rewrite this module\'s retired TA-layer strings in place')
    ap.add_argument('--retext-self-test', action='store_true')
    a = ap.parse_args()
    if a.retext_self_test:
        sys.exit(_retext_self_test())
    total = {}
    for p in a.retext or []:
        with open(p, encoding='utf-8', newline='') as fh:   # newline='': bytes other than the strings stay identical
            src = fh.read()
        out, counts = retext(src)
        for k, v in counts.items():
            total[k] = total.get(k, 0) + v
        if out != src:
            with open(p, 'w', encoding='utf-8', newline='') as fh:
                fh.write(out)
    print(json.dumps({'decks': len(a.retext or []), 'rewritten': total}))
