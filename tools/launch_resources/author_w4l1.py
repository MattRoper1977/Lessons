#!/usr/bin/env python3
"""CX2 §3 · author the LAUNCH W4L1 Diffusion candidate from the committed source.

Bounded like tools/grow_resources/author_w3a_arrival.py: the input is the source
blob at BASE (never the working copy), every edit anchors on an exact string that
must occur exactly once, and the whole file is regenerated on every run, so the
tool is idempotent by construction. Content comes from the three JSON tables
beside this script; nothing in the lesson text is composed here.

What it does, in order (docs/orders/LESSON_STANDARD_2026-27.md):
  chassis   §3.2 demonstrated repairs, proved by tools/launch_resources/focus_probe.cjs
            before and after: a slide transition focuses the new slide's heading;
            the deck's key handler never fires from a focused control; the TA Brief
            and Cold Call overlays get dialog semantics, focus inside on open, Escape
            and the close button return focus to the opener.
  arrival   A.25.2 item 1: four questions in each of Supported / Standard / Stretch,
            2×2 cards, print questions and separately revealable answers.
  organiser A.25.2 item 3: an on-screen organiser dialog reachable from every stage
            with Tier 2 / Tier 3 labels, a captioned particle model, and a printable
            counterpart.
  feedback  A.25.3: the standalone Lundy stage and its print sheet go; one optional
            help prompt sits inside We Do 2; staff notes carry the fuller guidance,
            the B2 feedback card (LAUNCH variant), the B4 destination link and the
            B3 response modes.
  exit      A.25.2 item 7: two small checks per tier with answers revealed after an
            attempt, a print sheet per route, continuation by name only.
  timing    40 minutes kept: arrival 4, glance 1, I Do 4, We Do 4, I Do 3, We Do 5,
            independent 15, exit 4 (the three minutes of the removed stage go to
            arrival, We Do 2 and exit).

    python3 tools/launch_resources/author_w4l1.py [--root .] [--check]
"""
from pathlib import Path
import argparse, hashlib, html, json, re, subprocess

BASE = '3a14e9c4d57832fed87ed588ef6f0ae4fd3d6064'
REL = 'Science_Teesside/Launch/SCI_L_W4_L1_Diffusion.html'
HERE = Path(__file__).resolve().parent
esc = html.escape


def once(text, anchor, name):
    n = text.count(anchor)
    assert n == 1, '%s: anchor occurs %d times: %r' % (name, n, anchor[:80])


def replace_once(text, old, new, name):
    once(text, old, name)
    return text.replace(old, new)


def slide_span(text, title):
    start = text.index('<div class="slide" data-title="%s"' % title)
    nxt = re.compile(r'<div class="slide(?: active)?" data-title=').search(text, start + 10)
    end = nxt.start() if nxt else text.index('<div class="controls">', start)
    return start, end


def balanced(text, anchor, tag='div'):
    i = text.index(anchor)
    # an anchor that IS the opening tag starts the span itself; an attribute anchor sits inside it
    start = i if text.startswith('<' + tag, i) else text.rfind('<' + tag, 0, i)
    depth = 0; j = start
    while j < len(text):
        if text.startswith('<' + tag, j) and text[j + 1 + len(tag)] in ' >':
            depth += 1; j += 1
        elif text.startswith('</' + tag + '>', j):
            depth -= 1; j += len(tag) + 3
            if depth == 0:
                return start, j
        else:
            j += 1
    raise AssertionError(anchor)


def build(root):
    src = subprocess.check_output(['git', '-C', str(root), 'show', BASE + ':' + REL]).decode()
    arrival = json.loads((HERE / 'W4L1_ARRIVAL.json').read_text())
    org = json.loads((HERE / 'W4L1_ORGANISER_EXIT.json').read_text())
    fb = json.loads((HERE / 'W4L1_FEEDBACK.json').read_text())
    t = src

    # ---------------------------------------------------------------- chassis
    t = replace_once(t,
        "function showSlide(i){slides.forEach((s,j)=>s.classList.toggle('active',j===i));updateProgress();}",
        "function showSlide(i){\n  if(!Number.isInteger(i)||i<0||i>=slides.length)return;\n  const changed=!slides[i].classList.contains('active');\n"
        "  currentSlide=i;slides.forEach((s,j)=>s.classList.toggle('active',j===i));updateProgress();\n"
        "  if(changed){\n    const heading=slides[i].querySelector('h1,h2,h3');\n    if(heading){heading.setAttribute('tabindex','-1');heading.focus();}\n  }\n}", 'showSlide')
    t = replace_once(t,
        "document.addEventListener('keydown',e=>{const tag=(e.target&&e.target.tagName)||'';if(tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT')return;if(tag==='BUTTON'&&e.key===' ')return;if(document.querySelector('.v4-modal-overlay.visible')||document.querySelector('.lesson-complete-overlay.visible')||document.querySelector('.midpoint-overlay.visible'))return;if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();nextSlide()}if(e.key==='ArrowLeft'){e.preventDefault();prevSlide()}});",
        "document.addEventListener('keydown',e=>{\n  if(e.defaultPrevented||!(e.target instanceof Element))return;\n  const heading=e.target.matches('h1,h2,h3,h4,h5,h6');\n"
        "  const control=e.target.closest('button,input,textarea,select,a,summary,details,video,audio,[contenteditable=\"true\"],[role=\"button\"],[role=\"slider\"],[tabindex]');\n"
        "  if(control&&!(control===e.target&&heading))return;\n  if(e.target!==document.body&&e.target.closest('.slide')&&e.target.matches(':focus')&&!heading)return;\n"
        "  if(document.querySelector('dialog[open]')||document.querySelector('.v4-modal-overlay.visible')||document.querySelector('.lesson-complete-overlay.visible')||document.querySelector('.midpoint-overlay.visible'))return;\n"
        "  if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();nextSlide()}\n  if(e.key==='ArrowLeft'){e.preventDefault();prevSlide()}\n});", 'keydown guard')
    # overlay dialogs: semantics, focus in, focus back
    helpers = ("function _mbmModalOpened(m,opener){m._mbmOpener=opener;const box=m.querySelector('.v4-modal');if(!box)return;box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');"
               "const h=box.querySelector('h3');if(h&&!h.id){h.id=m.id+'-title';}if(h)box.setAttribute('aria-labelledby',h.id);"
               "const focusables=()=>[...box.querySelectorAll('button,[href],input,select,textarea,[tabindex]:not([tabindex=\"-1\"])')].filter(el=>!el.disabled);"
               "const first=focusables()[0];if(first)first.focus({preventScroll:true});"
               "if(!m._mbmTrap){m._mbmTrap=true;m.addEventListener('keydown',ev=>{if(ev.key!=='Tab')return;const f=focusables();if(!f.length)return;const a=f[0],z=f[f.length-1];if(ev.shiftKey&&document.activeElement===a){ev.preventDefault();z.focus();}else if(!ev.shiftKey&&document.activeElement===z){ev.preventDefault();a.focus();}});}}\n"
               "function _mbmModalClose(id){const m=document.getElementById(id);if(!m)return;const was=m.classList.contains('visible');m.classList.remove('visible');const o=m._mbmOpener;if(was&&o&&o.isConnected)o.focus({preventScroll:true});}\n")
    t = replace_once(t, "function showTABrief(){", helpers + "function showTABrief(){", 'modal helpers')
    for mid in ('ta-modal', 'cc-modal'):
        t = replace_once(t, "modal.onclick=function(e){if(e.target.id==='%s')modal.classList.remove('visible')};" % mid,
                         "modal.onclick=function(e){if(e.target.id==='%s')_mbmModalClose('%s')};" % (mid, mid), mid + ' overlay click')
        t = replace_once(t, "onclick=\"document.getElementById(\\'%s\\').classList.remove(\\'visible\\')\"" % mid,
                         "onclick=\"_mbmModalClose(\\'%s\\')\"" % mid, mid + ' got-it button')
    # the open path of each overlay: the single add('visible') inside its own function body
    for fn in ('showTABrief', 'showColdCall'):
        f_start = t.index('function %s(){' % fn); f_end = t.index('function ', f_start + 10)
        body = t[f_start:f_end]
        assert body.count("modal.classList.add('visible')") == 1, fn + ' open path'
        body = body.replace("modal.classList.add('visible')", "const opener=document.activeElement;modal.classList.add('visible');_mbmModalOpened(modal,opener)")
        t = t[:f_start] + body + t[f_end:]
    t = replace_once(t, "document.addEventListener('keydown',function(e){if(e.key==='Escape'){['ta-modal','cc-modal','cc-edit-modal','lc-overlay','mp-overlay'].forEach(id=>{const m=document.getElementById(id);if(m)m.classList.remove('visible');});}});",
                     "document.addEventListener('keydown',function(e){if(e.key==='Escape'){['ta-modal','cc-modal','cc-edit-modal','lc-overlay','mp-overlay'].forEach(id=>_mbmModalClose(id));}});", 'Escape restores focus')

    # the I Do 1 model SVG sits inside a div that already carries role="img" and the full description;
    # the inner svg had role="img" with no name of its own (axe svg-img-alt, serious)
    t = replace_once(t, '<svg viewBox="0 0 640 300" width="100%" role="img"', '<svg viewBox="0 0 640 300" width="100%" aria-hidden="true" focusable="false"', 'I Do 1 svg name')

    # ---------------------------------------------------------------- timings
    t = replace_once(t, '<div class="slide" data-title="Arrival Task" data-timer="3"', '<div class="slide" data-title="Arrival Task" data-timer="4"', 'arrival timer')
    t = replace_once(t, '<div class="slide" data-title="We Do 2" data-timer="4"', '<div class="slide" data-title="We Do 2" data-timer="5"', 'we do 2 timer')
    t = replace_once(t, '<div class="slide" data-title="Exit Ticket" data-timer="3"', '<div class="slide" data-title="Exit Ticket" data-timer="4"', 'exit timer')
    old_plan = '40-minute session: Arrival 3; overview 1; I Do 1 4; We Do 1 4; I Do 2 3; We Do 2 4; independent work 15; feedback and next step 3; exit 3.'
    new_plan = '40-minute session: Arrival 4; overview 1; I Do 1 4; We Do 1 4; I Do 2 3; We Do 2 5; independent work 15; exit 4.'
    assert t.count(old_plan) >= 1, 'session plan text'
    t = t.replace(old_plan, new_plan)

    # ---------------------------------------------------------------- remove the standalone Lundy stage
    a, b = slide_span(t, 'Lundy Loop'); t = t[:a] + t[b:]
    a, b = balanced(t, 'id="print-lundy"'); t = t[:a] + t[b:]
    t = replace_once(t, "['ko','intro','glance','arrival','wedo','exit','witness','lundy','feedback'].forEach(id=>{const el=document.getElementById('print-'+id);if(el)el.classList.add('visible')});",
                     "['ko','intro','glance','arrival','wedo','w4l1-exit'].forEach(id=>{const el=document.getElementById('print-'+id);if(el)el.classList.add('visible')});", 'pupil pack list')

    # ---------------------------------------------------------------- arrival
    def cards(route, answers=False):
        key = 'answers' if answers else 'questions'
        return ''.join('<div class="task-box"><h3>%d. %s</h3></div>' % (i + 1, esc(q)) for i, q in enumerate(route[key]))
    controls = ''.join('<button type="button" class="ghost small" data-arrival-route="%s" aria-pressed="%s" onclick="setLaunchArrival(\'%s\')">%s</button>'
                       % (k, str(k == 'supported').lower(), k, esc(r['label'])) for k, r in arrival['routes'].items())
    screen = ('<div class="slide" data-title="Arrival Task" data-timer="4" id="arrival-slide"><span class="slide-tag tag-arrival">🚪 Arrival · four quick questions</span>'
              '<h2>Arrival task — pick your tier</h2><p class="launch-arrival-response">%s</p><p class="launch-arrival-access">%s</p>'
              '<div class="level-toggle" role="group" aria-label="Arrival route">%s</div>' % (esc(arrival['response']), esc(arrival['access']), controls))
    for k, r in arrival['routes'].items():
        hidden = '' if k == 'supported' else ' hidden'
        screen += ('<div id="arrival-%s" class="arrival-grid"%s>%s<div class="launch-arrival-actions"><button type="button" class="ghost small" onclick="printLaunchSheet(\'print-arrival\',\'%s\')">Print %s arrival</button>'
                   '<details class="launch-arrival-answers"><summary>Show %s arrival answers</summary><p>%s</p><ol>%s</ol>'
                   '<button type="button" class="ghost small" onclick="printLaunchSheet(\'print-arrival-answers\',\'%s\')">Print %s staff answers</button></details></div></div>'
                   % (k, hidden, cards(r), k, esc(r['label']), esc(r['label']), esc(arrival['staff']), ''.join('<li>%s</li>' % esc(x) for x in r['answers']), k, esc(r['label'])))
    screen += '</div>'
    a, b = slide_span(t, 'Arrival Task'); t = t[:a] + screen + t[b:]

    def arrival_print(answers=False):
        sid = 'print-arrival-answers' if answers else 'print-arrival'
        out = '<div id="%s" class="print-section launch-arrival-print"><h2>Diffusion arrival%s</h2><p>%s</p><p>%s</p>' % (
            sid, ' — staff answers' if answers else '', esc(arrival['staff'] if answers else arrival['response']), esc(arrival['access']))
        for k, r in arrival['routes'].items():
            out += '<div class="%s-content"><h3>%s</h3><div class="launch-arrival-paper-grid">' % (k, esc(r['label']))
            for i, q in enumerate(r['questions']):
                out += '<div class="launch-arrival-paper-card"><p><strong>%d. %s</strong></p>%s</div>' % (
                    i + 1, esc(q), ('<p>%s</p>' % esc(r['answers'][i])) if answers else '<div class="launch-arrival-space" aria-hidden="true"></div>')
            out += '</div></div>'
        return out + '</div>'
    a, b = balanced(t, 'id="print-arrival"'); t = t[:a] + arrival_print() + arrival_print(True) + t[b:]

    # ---------------------------------------------------------------- organiser dialog + print-ko
    vocab_rows = ''.join('<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' % (esc(w), esc(tier), esc(m)) for w, tier, m in org['vocabulary'])
    model_svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 220" width="100%" role="img" aria-labelledby="launch-ko-model-title">'
                 '<title id="launch-ko-model-title">Particle model of diffusion across a membrane: many particles on the left, few on the right, net movement arrow pointing right</title>'
                 '<rect x="10" y="20" width="300" height="180" fill="#e8f1f8" stroke="#4d82a0" stroke-width="3"/><rect x="330" y="20" width="300" height="180" fill="#f7f4ec" stroke="#4d82a0" stroke-width="3"/>'
                 '<line x1="320" y1="14" x2="320" y2="206" stroke="#7a5c9e" stroke-width="6" stroke-dasharray="14 8"/>'
                 + ''.join('<circle cx="%d" cy="%d" r="9" fill="#1e3a8a"/>' % (x, y) for x in range(40, 300, 40) for y in range(45, 200, 38))
                 + ''.join('<circle cx="%d" cy="%d" r="9" fill="#1e3a8a"/>' % (x, y) for x, y in ((380, 70), (470, 140), (560, 60), (600, 170)))
                 + '<path d="M250 110 H400 M370 90 L400 110 L370 130" fill="none" stroke="#c2410c" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
                 '<text x="160" y="212" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" fill="#1e3a8a">high concentration</text>'
                 '<text x="480" y="212" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" fill="#1e3a8a">low concentration</text>'
                 '<text x="325" y="12" text-anchor="middle" font-family="Arial,sans-serif" font-size="15" fill="#7a5c9e">membrane</text></svg>')
    ko_body = ('<p><strong>Learning objective:</strong> %s</p><h3>Success criteria</h3><ul>%s</ul>'
               '<div class="launch-ko-table-wrap" role="region" aria-label="Diffusion vocabulary" tabindex="0"><table class="ko-table"><caption>Key words, with their tier</caption><thead><tr><th scope="col">Word</th><th scope="col">Tier</th><th scope="col">Meaning</th></tr></thead><tbody>%s</tbody></table></div>'
               '<h3>Key ideas</h3><ul>%s</ul><figure class="launch-ko-model">%s<figcaption>%s</figcaption></figure><h3>Examples</h3><ul>%s</ul>'
               % (esc(org['objective']), ''.join('<li>%s</li>' % esc(s) for s in org['success']), vocab_rows,
                  ''.join('<li>%s</li>' % esc(f) for f in org['facts']), model_svg, esc(org['model_caption']), ''.join('<li>%s</li>' % esc(e) for e in org['examples'])))
    dialog = ('<dialog id="launch-ko-dialog" aria-labelledby="launch-ko-heading"><form method="dialog" class="launch-ko-close"><button class="ghost small">Close organiser</button></form>'
              '<h2 id="launch-ko-heading" tabindex="-1">Diffusion knowledge organiser</h2>%s<p><button type="button" class="ghost small" onclick="printSection(\'ko\',\'standard\')">Print A4 organiser</button></p></dialog>' % ko_body)
    t = replace_once(t, '<div class="controls">', dialog + '<div class="controls">', 'organiser dialog placement')
    a, b = balanced(t, 'id="print-ko"')
    t = t[:a] + ('<div id="print-ko" class="print-section"><h1 style="text-align:center;font-size:1.55rem">Knowledge Organiser — Discover: Diffusion</h1>'
                 '<p style="text-align:center;margin:2px 0 8px"><strong>LAUNCH · Edexcel GCSE Biology 1BI0 Foundation · Paper 1 · Topic 1</strong></p>%s</div>' % ko_body) + t[b:]
    # organiser access from every stage: after the first heading of each slide
    access = '<div class="launch-ko-access"><button type="button" class="ghost small" onclick="openLaunchKO(this)">Knowledge organiser</button></div>'
    cont = t.index('<div class="slide-container"')
    ctrl = t.index('<div class="controls">', cont)
    body = t[cont:ctrl]
    body, n = re.subn(r'(<div class="slide(?: active)?" data-title="[^"]+"[^>]*>(?:(?!</h[12]>).)*?</h[12]>)', lambda m: m.group(1) + access, body, flags=re.S)
    assert n == 9, 'organiser access buttons: %d' % n
    t = t[:cont] + body + t[ctrl:]

    # ---------------------------------------------------------------- one optional help prompt inside We Do 2
    prompt = '<details class="launch-help-prompt" id="launch-help-a"><summary>%s</summary><p>%s</p></details>' % (esc(fb['prompt_title']), esc(fb['prompt_body']))
    t = replace_once(t, '<p id="match-fb" style="text-align:center;font-weight:800;min-height:1.2rem;margin:6px 0"></p>',
                     '<p id="match-fb" style="text-align:center;font-weight:800;min-height:1.2rem;margin:6px 0"></p>' + prompt, 'help prompt placement')

    # ---------------------------------------------------------------- exit: two checks per tier
    routes = org['routes']
    toggle = '<div role="group" aria-label="Exit route" class="level-toggle">' + ''.join(
        '<button type="button" class="ghost small" data-launch-exit-route="%s" aria-pressed="%s" onclick="setLaunchExit(\'%s\')">%s</button>' % (k, str(k == 'supported').lower(), k, esc(r['label']))
        for k, r in routes.items()) + '</div>'
    def exit_panel(k, r):
        out = '<div id="launch-exit-%s"%s>' % (k, '' if k == 'supported' else ' hidden')
        for i, q in enumerate(r['questions']):
            if 'options' in r:
                out += '<fieldset><legend>%d. %s</legend>%s</fieldset>' % (i + 1, esc(q), ''.join(
                    '<label class="launch-exit-choice"><input type="radio" name="launch-exit-%s-%d" value="%s"> %s</label>' % (k, i, esc(o), esc(o)) for o in r['options'][i]))
            else:
                out += '<div class="task-box"><p><strong>%d. %s</strong></p><label class="launch-exit-field"><span>Your answer (optional; say, sign, draw or use paper instead)</span><textarea rows="2"></textarea></label></div>' % (i + 1, esc(q))
        out += ('<button type="button" class="ghost small" onclick="printLaunchSheet(\'print-w4l1-exit\',\'%s\')">Print %s exit</button> '
                '<details class="launch-exit-explanations"><summary>Compare %s answers after your attempt</summary><ol>%s</ol><p>Use these with an adult. Your response is not automatically marked.</p>'
                '<button type="button" class="ghost small" onclick="printLaunchSheet(\'print-w4l1-exit-answers\',\'%s\')">Print staff exit answers</button></details></div>'
                % (k, esc(r['label']), esc(r['label']), ''.join('<li>%s</li>' % esc(x) for x in r['answers']), k))
        return out
    exit_slide = ('<div class="slide" data-title="Exit Ticket" data-timer="4" id="exit-slide"><span class="slide-tag tag-exit">🎫 Exit · two small checks</span><h2>Before you go</h2>'
                  '<p class="launch-exit-intro">%s</p>%s%s<p class="launch-next-lesson"><strong>Next lesson:</strong> %s</p></div>'
                  % (esc(org['exit_intro']), toggle, ''.join(exit_panel(k, r) for k, r in routes.items()), esc(org['next_lesson'])))
    a, b = balanced(t, '<div class="slide" data-title="Exit Ticket"')
    assert b < t.index('<div class="controls">', a), 'exit slide precedes the controls'
    t = t[:a] + exit_slide + t[b:]

    def exit_print(answers=False):
        sid = 'print-w4l1-exit-answers' if answers else 'print-w4l1-exit'
        out = '<div id="%s" class="print-section launch-exit-print"><h2>Diffusion exit%s</h2><p>%s</p>' % (sid, ' — staff answers' if answers else '', esc(org['staff'] if answers else org['exit_intro']))
        for k, r in routes.items():
            out += '<div class="%s-content"><h3>%s</h3>' % (k, esc(r['label']))
            for i, q in enumerate(r['questions']):
                opts = (' <em>(%s)</em>' % esc(' / '.join(r['options'][i]))) if 'options' in r else ''
                out += '<p><strong>%d. %s</strong>%s</p>%s' % (i + 1, esc(q), opts, ('<p>%s</p>' % esc(r['answers'][i])) if answers else "<div class='print-line'></div><div class='print-line'></div>")
            out += '</div>'
        return out + '<p><strong>Next lesson:</strong> %s</p></div>' % esc(org['next_lesson'])
    a, b = balanced(t, 'id="print-exit"'); t = t[:a] + exit_print() + exit_print(True) + t[b:]

    # ---------------------------------------------------------------- staff notes: feedback card, participation, destination link
    codes = ''.join('<tr><td class="mk-code">%s</td><td>%s</td></tr>' % (esc(c), esc(m)) for c, m in fb['codes'])
    sections = ''.join('<h4>%s</h4><p>%s</p>' % (esc(h), esc(p)) for h, p in fb['staff_sections'])
    card_body = ('<p class="mk-small">Staff copy — not for pupil books. Codes live in books, never on pupil slides or printouts.</p>'
                 '<p class="mk-lead">%s</p><h4>Codes</h4><table class="ko-table mk-codetable"><tbody>%s</tbody></table><p class="mk-small mk-summary">%s</p>%s'
                 '<p class="mk-small mk-prov">%s</p><p class="mk-small">Optional staff video link: <a href="%s" target="_blank" rel="noopener noreferrer">the explainer clip named in the science pack</a> (opens in a new tab; never embedded or autoplayed on a pupil surface).</p>'
                 % (esc(fb['launch_line']), codes, esc(fb['summary_line']), sections, esc(fb['policy_line']), esc(fb['video_url'])))
    staff_details = '<details class="launch-staff-notes"><summary>Staff notes · feedback, participation, real-world link</summary>%s<p><button type="button" class="ghost small" onclick="printSection(\'teacher-feedback\',\'standard\')">Print staff card, A4</button></p></details>' % card_body
    t = replace_once(t, '<details data-main-session-plan="launch-40">', staff_details + '<details data-main-session-plan="launch-40">', 'staff notes placement')
    t = replace_once(t, '<div id="print-witness" class="print-section">',
                     '<div id="print-teacher-feedback" class="print-section launch-staff-print"><h2>%s</h2>%s</div><div id="print-witness" class="print-section">' % (esc(fb['staff_title']), card_body), 'staff print card')

    # ---------------------------------------------------------------- scripts for the new controls + CSS + noscript
    script = ("\n<script>\nfunction setLaunchArrival(route){['supported','standard','stretch'].forEach(k=>{document.getElementById('arrival-'+k).hidden=k!==route;});"
              "document.querySelectorAll('[data-arrival-route]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.arrivalRoute===route)));}\n"
              "function setLaunchExit(route){['supported','standard','stretch'].forEach(k=>{document.getElementById('launch-exit-'+k).hidden=k!==route;});"
              "document.querySelectorAll('[data-launch-exit-route]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.launchExitRoute===route)));}\n"
              "function printLaunchSheet(id,level){document.body.classList.remove('print-supported','print-standard','print-stretch');if(level)document.body.classList.add('print-'+level);"
              "document.querySelectorAll('.print-section').forEach(el=>el.classList.remove('visible'));const el=document.getElementById(id);if(el)el.classList.add('visible');if(typeof _stampAndMark==='function')_stampAndMark();window.print();}\n"
              "let launchKOReturn=null;\nfunction openLaunchKO(button){const dialog=document.getElementById('launch-ko-dialog');if(dialog.open)return;launchKOReturn=button;dialog.showModal();dialog.scrollTop=0;document.getElementById('launch-ko-heading').focus({preventScroll:true});}\n"
              "document.getElementById('launch-ko-dialog').addEventListener('close',()=>{if(launchKOReturn&&launchKOReturn.isConnected)launchKOReturn.focus({preventScroll:true});});\n"
              "</script>\n")
    t = replace_once(t, '</body>', script + '</body>', 'script placement')
    css = ('<style id="launch-w4l1-css">.launch-ko-access{margin:2px 0 8px}.launch-arrival-response,.launch-arrival-access,.launch-exit-intro{font-size:.98rem;margin:4px 0}'
           '#launch-ko-dialog{max-width:min(92vw,820px);max-height:88vh;overflow:auto;border:2px solid #7a5c9e;border-radius:16px;padding:18px 22px;background:#fff;color:#1a1a1a}#launch-ko-dialog::backdrop{background:rgba(20,20,40,.55)}'
           '.launch-ko-close{text-align:right}.launch-ko-table-wrap{overflow-x:auto}.launch-ko-model svg{max-width:640px;display:block;margin:0 auto}'
           '.launch-help-prompt{margin:8px auto;max-width:720px;background:#fef9c3;border:2px solid #ca8a04;border-radius:10px;padding:6px 10px}.launch-help-prompt summary{font-weight:800;cursor:pointer}'
           '.launch-exit-choice{display:inline-block;margin:4px 12px 4px 0}.launch-exit-field span{display:block;font-size:.9rem}.launch-exit-field textarea{width:100%;max-width:520px}'
           '#exit-slide fieldset{border:1px solid #94a3b8;border-radius:8px;margin:6px 0;padding:6px 10px}.launch-staff-notes{text-align:left;max-width:760px;margin:8px auto}.launch-staff-notes summary{font-weight:800;cursor:pointer}'
           '.mk-codetable td{padding:3px 8px}.mk-code{font-weight:900;white-space:nowrap}.mk-small{font-size:.9rem}.mk-lead{font-weight:700}'
           '.launch-arrival-paper-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.launch-arrival-paper-card{border:1px solid #94a3b8;border-radius:6px;padding:6px}.launch-arrival-space{height:30mm}'
           '.slide{overflow-x:hidden}.title-dots{overflow:hidden}.sort-bin{min-width:0}.sort-bin-head,.sort-bin{overflow-wrap:anywhere}'
           '/* the model diagram labels are absolutely positioned and were nowrap: at 200% text on a phone they ran past the slide edge */.sci .sci-label,.ilm .sci-label{white-space:normal;max-width:44%;line-height:1.15;text-align:center}'
           'button[style*="#22c55e"]{background:#15803d!important}button[style*="#f97316"]{background:#c2410c!important}.task-box h3[style*="#22c55e"]{color:#166534!important}.task-box h3[style*="#f97316"]{color:#9a3412!important}'
           '/* contrast: the same deeper shades Friction measured (4.5:1 on the slide panel) */.sc-v4 h3{color:#7a5a12!important}#auto-timer,#auto-timer .at-btn{color:#8a5622}'
           '@media print{.launch-ko-access,.launch-help-prompt,.launch-staff-notes{display:none!important}.launch-arrival-print .print-section,.launch-exit-print{page-break-inside:avoid}}</style>')
    noscript = ('<noscript><style>body{overflow:auto!important}.slide-container{display:block!important;height:auto!important;width:auto!important;padding:16px 0 24px!important}'
                '.slide{display:flex!important;height:auto!important;max-height:none!important;overflow:visible!important;margin:0 auto 24px!important;animation:none!important}'
                '#arrival-standard,#arrival-stretch,#launch-exit-standard,#launch-exit-stretch,#exit-standard,#exit-stretch{display:block!important}[hidden].arrival-grid,#launch-exit-standard[hidden],#launch-exit-stretch[hidden]{display:block!important}'
                '#print-area{display:block!important;padding:0!important}#print-area .print-section{display:none!important}#print-area #print-ko{display:block!important;width:92%;margin:0 auto 24px;padding:24px;background:#fff;border-radius:20px}'
                '.controls,.progress-wrap,.progress-label,.level-toggle,.launch-ko-access,.js-only,button[onclick],#auto-timer,#cold-call-btn,.xp-wrap,.midpoint-overlay,.v4-modal-overlay,.lesson-complete-overlay{display:none!important}'
                '.nojs-note{width:92%;margin:12px auto;padding:12px 16px;background:#fef9c3;border:2px solid #eab308;border-radius:12px;font-size:1rem;line-height:1.4}</style>'
                '<p class="nojs-note" role="note">JavaScript is off in this browser. All nine stages of the 40-minute lesson are shown below in order, every arrival and exit route is open, and the knowledge organiser is at the end of the page. Timers, the organiser pop-up and print buttons need JavaScript; use the pupil and teacher PDFs for printing.</p></noscript>')
    t = replace_once(t, '</head>', css + '</head>', 'css placement')
    t = replace_once(t, '<div class="slide-container"', noscript + '<div class="slide-container"', 'noscript placement')
    return t


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', type=Path, default=Path('.'))
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    root = args.root.resolve(); out = root / REL
    text = build(root)
    digest = hashlib.sha256(text.encode()).hexdigest()
    if args.check:
        current = hashlib.sha256(out.read_bytes()).hexdigest()
        print('candidate', digest, 'on disk', current, 'MATCH' if digest == current else 'DIFFERS')
        raise SystemExit(0 if digest == current else 1)
    out.write_text(text)
    print('written', REL, len(text.encode()), 'bytes', digest)
