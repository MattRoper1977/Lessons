"""SX3-2 — render a pack lesson into its pathway's W8-W13 exemplar shell.

ORDER SX3-2 ruling R-CH: the chassis target is the live W8-W13 exemplar FOR THE DECK'S OWN
PATHWAY, measured, not a generic label. The three are not the same shell:

    BUILD   Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html      classroom
    GROW    Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html      review
    LAUNCH  Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html review

So this does NOT re-implement furniture and does NOT use chassis/shell.py's render_shell,
which emits `classic` and would fail R-CH on all three pathways. It TRANSPLANTS: it parses
the exemplar, keeps every structural element and id exactly as the exemplar has them, and
replaces only the content-bearing regions with the pack's own content.

Everything the parity instrument in _sx3/CHASSIS_CONTRACT.md names therefore survives by
construction; what changes is the lesson, not the shell.
"""
from __future__ import annotations

import copy
import json
import os
import re
from urllib.parse import unquote
from pathlib import Path

from lxml import etree
from lxml import html as LH

ROOT = Path(__file__).resolve().parents[4]

EXEMPLAR = {
    'BUILD':  'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html',
    'GROW':   'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html',
    'LAUNCH': 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html',
}

ROUTES = ('supported', 'standard', 'stretch')


def load_exemplar(pathway: str):
    """Parse the pathway's exemplar. The tree is the contract; callers mutate a copy."""
    path = ROOT / EXEMPLAR[pathway.upper()]
    return LH.fromstring(path.read_bytes()), path


def depth_prefix(target_rel: str) -> str:
    """'../' x (folder depth below the Lessons root), derived from the deck's ACTUAL path.

    Contract amendment A2: derived, never copied. Science_Teesside/Grow/X.html is two levels
    down and takes '../../'; the exemplars sit three levels down and take '../../../'.
    """
    return '../' * (len(Path(target_rel).parts) - 1)


def resolve_or_fail(target_rel: str, href: str) -> Path:
    """A2: prove the relative href by resolving it inside the checkout. No resolve, no ship."""
    base = (ROOT / target_rel).parent
    candidate = (base / href.split('?', 1)[0].split('#', 1)[0]).resolve()
    if not candidate.is_file():
        raise FileNotFoundError('A2: %r from %r does not resolve to a file' % (href, target_rel))
    return candidate


def set_back_links(doc, pathway: str, target_rel: str) -> list:
    """A2: rewrite every '← Lessons' anchor to this deck's own depth, then prove each one."""
    pathway = pathway.upper()
    prefix = depth_prefix(target_rel)
    proved = []
    for a in doc.xpath('//a'):
        if '← Lessons' not in (a.text_content() or ''):
            continue
        classes = (a.get('class') or '').split()
        if 'way-home' in classes:
            href = 'START_HERE.html'
        elif pathway == 'BUILD':
            href = prefix + 'index.html?subject=Science&pathway=BUILD'
        else:
            href = prefix + 'index.html'
        a.set('href', href)
        resolve_or_fail(target_rel, href)
        proved.append((a.get('class'), href))
    return proved


def replace_children(node, markup: str, protect=()) -> None:
    """Swap a container's children for parsed markup, keeping the container itself intact.

    Any descendant whose id the surviving shell scripts reach for is kept and re-attached
    first: the exemplar's own code owns those nodes, and clearing them is what left
    showTABrief() writing to null.
    """
    kept = [e for e in node.iter() if e is not node and e.get('id') in protect]
    for child in list(node):
        node.remove(child)
    node.text = None
    for child in kept:
        node.append(child)
    holder = LH.fragment_fromstring('<div>' + markup + '</div>')
    for child in holder:
        node.append(child)


def set_text(node, value: str) -> None:
    for child in list(node):
        node.remove(child)
    node.text = value


def by_id(doc, identifier: str):
    found = doc.xpath('//*[@id=$i]', i=identifier)
    return found[0] if found else None


ID_PATTERNS = (
    r"(?:byId|getElementById)\(\s*['\"]([A-Za-z0-9_-]+)['\"]",
    r"(?:querySelector(?:All)?|\$\$?)\(\s*['\"]#([A-Za-z0-9_-]+)",
)


CLASS_PATTERN = r"(?:querySelector(?:All)?|\$\$?)\(\s*['\"]\.([A-Za-z][A-Za-z0-9_-]*)['\"]"


def script_classes(body: str) -> set:
    """Single-class selectors a script reaches for — $('.frame'), querySelector('.deck')."""
    return set(re.findall(CLASS_PATTERN, body or ''))


def script_ids(body: str) -> set:
    """Every element id a script reaches for, however it spells the lookup.

    byId('x'), getElementById('x'), querySelector('#x'), $('#x'), $$('#x'). Missing one of
    these spellings is what let a lesson-specific script survive and throw on load.
    """
    found = set()
    for pattern in ID_PATTERNS:
        found |= set(re.findall(pattern, body or ''))
    return found


PRINT_MAP = {
    # candidates are tried in order and span all three dialects' page-key vocabularies
    'print-organiser': ['organiser'],
    'print-arrival-supported': ['arrival-A-supported', 'arrival-supported'],
    'print-arrival-standard': ['arrival-A-standard', 'arrival-standard'],
    'print-arrival-stretch': ['arrival-A-stretch', 'arrival-stretch'],
    'print-arrival-answers-supported': ['arrival-A-supported-answers', 'arrival-answers-supported', 'answers-supported'],
    'print-arrival-answers-standard': ['arrival-A-standard-answers', 'arrival-answers-standard', 'answers-standard'],
    'print-arrival-answers-stretch': ['arrival-A-stretch-answers', 'arrival-answers-stretch', 'answers-stretch'],
    'print-exit-supported': ['exit-A-supported', 'exit-supported'],
    'print-exit-standard': ['exit-A-standard', 'exit-standard'],
    'print-exit-stretch': ['exit-A-stretch', 'exit-stretch'],
    'print-task-supported-1': ['independent-supported', 'task-supported'],
    'print-task-standard-1': ['independent-standard', 'task-standard'],
    'print-task-stretch-1': ['independent-stretch', 'task-stretch'],
    'print-task-supported-2': ['arrival-B-supported', 'pupil-supported', 'evidence-record', 'lab-guide'],
    'print-task-standard-2': ['arrival-B-standard', 'pupil-standard', 'evidence-record', 'lab-guide'],
    'print-task-stretch-2': ['arrival-B-stretch', 'pupil-stretch', 'evidence-record', 'lab-guide'],
    'print-shared': ['activity-cards', 'cards', 'evidence', 'model-pieces', 'sources'],
    'print-answers': ['all-answers', 'answers-A-standard', 'answers-standard', 'independent-answers', 'activity-answers'],
    'print-marking': ['staff-feedback', 'staff'],
    'print-staff': ['staff-A', 'staff-1', 'staff'],
    'print-first-back': [],
}

DIALOG_MAP = {
    'word-dialog': 'words',
    'ta-dialog': 'staff',
    'organiser-dialog': 'organiser',
    'tools-dialog': 'tools',
}


def _opens_dialog(action, dialog_id):
    """Which data-action opens which exemplar dialog, read from the shell's own naming."""
    return {'pause': 'pause-dialog', 'cold-call': 'cold-call-dialog', 'tools': 'tools-dialog',
            'organiser': 'organiser-dialog', 'words': 'word-dialog',
            'ta': 'ta-dialog'}.get(action) == dialog_id


def transplant(pathway, content, target_rel, title=None, spine_week=None, had_guide=None,
               prior=None):
    """Put one pack lesson inside its pathway exemplar. Returns (html, report)."""
    pathway = pathway.upper()
    doc, exemplar_path = load_exemplar(pathway)
    # Contract row 42. The exemplar binds its controls PER ELEMENT
    # ( querySelectorAll('[data-action]').forEach(b => b.addEventListener(...)) ); the pack
    # ships a DOCUMENT-level delegated handler for the same attribute plus its own
    # openDialog(). Both therefore drove every exemplar control: a TA click opened the dialog
    # from the shell, then the pack's handler ran openDialog('ta-dialog'), found a dialog
    # already open and closed it — and the exemplar's close handler strips .mbm-guide-on,
    # which its CSS needs to show the TA brief at all. Tag the exemplar's own controls here,
    # before a single pack node is inserted, so the set is exact and nothing is matched by
    # name; the emitted script then keeps the pack's delegated handler off them.
    for shell_control in doc.xpath('//*[@data-action]'):
        shell_control.set('data-sx3-shell', '1')
    # Contract row 44: the exemplar's own sibling navigation is the exemplar's CONTENT, not
    # chassis. "Next · W8L2 · Amylase and pH" is simply wrong on a W13 deck, and because W8L2
    # sits in the same folder the A2 dead-link sweep kept it — it resolves, it is just untrue.
    # The published pack gate agrees: it refuses a release pack whose lessons link to a file
    # outside the declared pack ("Unresolved navigation in the release pack"). Tag the
    # exemplar's anchors here, before any pack node exists, so the pack's own cross-links
    # between its paired lessons are never touched.
    for shell_link in doc.xpath('//a[@href]'):
        shell_link.set('data-sx3-shell-link', '1')
    report = {'omitted': [], 'filled': [], 'pathway': pathway,
              'exemplar': str(exemplar_path.relative_to(ROOT))}
    heading = title or content.get('title') or ''
    shell_refs = set()
    for node in doc.xpath('//script[not(@src)]'):
        body = node.text or ''
        shell_refs |= script_ids(body)

    for node in doc.xpath('//title'):
        node.text = '%s Science · %s' % (pathway, heading) if heading else (node.text or '')
    for node in doc.xpath('//meta[@name="description"]'):
        if heading:
            node.set('content', heading)

    # slides: the exemplar's own attribute set, the pack's own bodies
    deck = doc.xpath('//main[@id="lessonDeck"]')[0]
    for child in list(deck):
        deck.remove(child)
    deck.text = None
    for index, slide in enumerate(content['slides'], 1):
        section = LH.fragment_fromstring('<section>%s</section>' % slide['html'])
        section.set('class', 'slide science-slide')
        section.set('id', 'slide-%d' % index)
        section.set('data-title', slide.get('title') or '')
        section.set('data-timer', str(slide.get('timer') or '0'))
        section.set('data-type', slide.get('type') or '')
        if slide.get('teacher'):
            section.set('data-teacher', slide['teacher'])
            section.set('data-ta1', slide['teacher'])
        deck.append(section)
    report['slides'] = len(content['slides'])

    # The exemplar's shell script owns an arrival root and an exit root, each carrying its own
    # controls (route switch, reveal, print, print-answers). Hand-writing that markup kept
    # missing one — [data-exit-print] was the last. So CLONE the exemplar's own root and swap
    # only the cells: whatever controls it carries survive by construction, for every deck.
    exemplar_doc = LH.fromstring(exemplar_path.read_bytes())

    def cell_markup(kind, cells):
        if kind == 'arrival':
            return ''.join(
                '<article class="arrival-cell" style="--arrival-order:%d"><h3>%s</h3><p>%s</p>'
                '<p class="arrival-hint">%s</p>'
                '<p class="arrival-answer" data-arrival-answer hidden>%s</p></article>'
                % (i, c['title'], c['question'], c['help'], c['answer'])
                for i, c in enumerate(cells))
        return ''.join(
            '<article class="question-card"><h3>%s</h3><p class="question-prompt">%s</p>'
            '<div class="question-help">%s</div>'
            '<p class="exit-answer" data-exit-answer hidden>%s</p></article>'
            % (c['title'], c['question'], c['help'], c['answer'])
            for c in cells)

    for kind, source in (('arrival', content.get('arrivals') or {}),
                         ('exit', content.get('exits') or {})):
        donor = exemplar_doc.xpath('//*[@data-%s-root]' % kind)
        if not donor:
            report['omitted'].append('[data-%s-root] (exemplar has none to clone)' % kind)
            continue
        if not any((source.get(r) or []) for r in ROUTES):
            report['omitted'].append('[data-%s-root] (pack has no %s cells)' % (kind, kind))
            continue
        root = copy.deepcopy(donor[0])
        for panel in root.xpath('.//*[@data-%s-panel]' % kind):
            route = panel.get('data-%s-panel' % kind)
            replace_children(panel, cell_markup(kind, source.get(route) or []))
        existing = doc.xpath('//*[@data-%s-root]' % kind)
        if existing:
            existing[0].getparent().replace(existing[0], root)
        else:
            deck.addnext(root)
        report['filled'].append('[data-%s-root] (cloned from the exemplar)' % kind)

    exits = content.get('exits') or {}
    for route in ROUTES:
        node = by_id(doc, 'print-exit-' + route)
        cells = exits.get(route) or []
        if node is None or not cells:
            continue
        if (content.get('pages') or {}):
            continue  # a real pack print page already filled it below
        markup = ''
        for cell in cells:
            markup += ('<article class="question-card"><p class="question-prompt">%s %s</p>'
                       '<div class="question-help">%s</div><div class="paper-lines"></div></article>'
                       % (cell['title'], cell['question'], cell['help']))
        replace_children(node, markup)
        report['filled'].append('#print-exit-' + route)

    # dialog bodies
    for identifier, key in DIALOG_MAP.items():
        node = by_id(doc, identifier)
        markup = content.get(key) or ''
        if node is None:
            continue
        if not markup:
            report['omitted'].append('#%s (pack has no %s)' % (identifier, key))
            continue
        inner = node.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," v4-modal ")]')
        holder = inner[0] if inner else node
        # Contract row 39: a dialog's controls belong to the chassis, not to the lesson.
        # Walk the exemplar's own children in order and keep the heading, every subtree the
        # shell scripts own by id (the TA brief's #ta-current-title / #ta-current-text,
        # #staff-card-view), and every child that carries a control the shell binds — the
        # close button, the slide jump, the print packs, the staff-card buttons. Measured on
        # all three exemplars this keeps control furniture only: no lesson prose rides along
        # (details.teacher-only has no control, so Sugar's notes stay out of a Rocks lesson).
        # The pack's body then takes the place the exemplar's prose occupied, so trailing
        # controls stay below it.
        # A control is only worth keeping if it still drives something in the transplanted
        # deck. The pack owns #print-area at runtime (its script rewrites innerHTML), so the
        # exemplar's print furniture — the staff cards, the print packs, printSection() — has
        # no surviving target here and is recorded as a named gap instead of shipped dead.
        SAFE = ('.//*[@data-action="close"]|.//*[@data-action="goto"]'
                '|.//select|.//input')
        control_tags = ('button', 'input', 'select', 'textarea')
        def drives_something(child):
            if child.get('data-action') in ('close', 'goto'):
                return True
            if child.tag in ('select', 'input'):
                return True
            return bool(child.xpath(SAFE))
        originals = list(holder)
        ordered = []
        insert_at = None
        for child in originals:
            if (child.tag == 'h2' or child.get('id') in shell_refs
                    or drives_something(child)):
                ordered.append(child)
                continue
            owned = [e for e in child.iter()
                     if e is not child and e.get('id') in shell_refs]
            owned = [e for e in owned
                     if not any(e in list(other.iter()) for other in owned if other is not e)]
            if owned:
                ordered.extend(owned)
                continue
            if insert_at is None:
                insert_at = len(ordered)
        if insert_at is None:
            insert_at = len(ordered)
        for child in originals:
            holder.remove(child)
        holder.text = None
        for element in ordered:
            holder.append(element)
        # The pack's script reads its own content through its own dialog id
        # ( $('#dialog-ko .organiser') ). Wrap the transplanted body in that id so the hook
        # still resolves to the SAME content — nesting the pack's hook, not duplicating it.
        pack_hook = (content.get('dialog_source_ids') or {}).get(key)
        wrapper = ('<div id="%s">%s</div>' % (pack_hook, markup)) if pack_hook else markup
        extra = LH.fragment_fromstring('<div>' + wrapper + '</div>')
        for offset, child in enumerate(list(extra)):
            holder.insert(insert_at + offset, child)
        report['filled'].append('#' + identifier)

    # print sections
    pages = content.get('pages') or {}
    for identifier, candidates in PRINT_MAP.items():
        node = by_id(doc, identifier)
        if node is None:
            continue
        source = next((pages[c] for c in candidates if c in pages and pages[c]), None)
        if not source:
            # Row 37: leaving the exemplar's own lesson here is a provenance failure. Clear it
            # and name the gap instead.
            replace_children(node, '', protect=shell_refs)
            report['omitted'].append('#%s (no pack page among %s) — emptied' % (identifier, ','.join(candidates) or 'none'))
            continue
        replace_children(node, source, protect=shell_refs)
        report['filled'].append('#' + identifier)

    # config blocks
    for node in doc.xpath('//script[not(@src) and not(@id)]'):
        body = node.text or ''
        if body.strip().startswith('window.CLASSIC_LESSON'):
            node.text = 'window.CLASSIC_LESSON=%s;' % json.dumps(
                {'title': heading, 'id': (content.get('config') or {}).get('key', '')}, ensure_ascii=False)
    config = by_id(doc, 'lesson-config')
    if config is not None and content.get('config'):
        config.text = json.dumps(content['config'], ensure_ascii=False)

    # the pack's own styles and lesson script ride along; the shell's own stay
    if content.get('lesson_css'):
        style = etree.SubElement(doc.head, 'style')
        style.set('id', 'sx3-pack-css')
        style.text = content['lesson_css']
    if content.get('lesson_js'):
        script = etree.SubElement(doc.body, 'script')
        script.set('id', 'sx3-pack-js')
        script.text = content['lesson_js']

    # R-ALIAS: the pack's script expects its own chrome. Every id it looks up that the
    # transplanted page does not already carry gets a PRIVATE inert node in a hidden shim —
    # never the exemplar's real control. The exemplar keeps sole ownership of navigation,
    # timer, progress and reset, so the pack script cannot double-drive them: it is not bound
    # to them at all. #lesson-data is re-emitted from the pack, not from the exemplar.
    EXEMPLAR_OWNED = {'previous-slide', 'next-slide', 'auto-timer-toggle', 'auto-timer-reset',
                      'auto-timer-display', 'progressBar', 'progressLabel', 'classic-status',
                      'slide-picker', 'print-area', 'ta-dialog'}
    # Only shim what the PACK'S OWN DOM actually had and the transplant dropped. An id the
    # pack never carried is one its script already guards for ( if($('#particles')){...} );
    # creating it turns a guarded no-op into a thrown error.
    pack_ids = set((content.get('id_tags') or {}))
    pack_classes = set((content.get('class_tags') or {}))
    wanted = script_ids(content.get('lesson_js') or '') & pack_ids
    wanted_classes = script_classes(content.get('lesson_js') or '') & pack_classes
    present = {e.get('id') for e in doc.xpath('//*[@id]')}
    aliases = []
    shim_parts = []
    for identifier in sorted(wanted - present):
        if identifier == 'lesson-data':
            continue
        # the shim must be the SAME ELEMENT the pack used, or a canvas becomes a div and
        # getContext('2d') throws
        kind = (content.get('id_tags') or {}).get(identifier)
        if not kind:
            kind = 'button' if re.search(r'toggle|reset|prev|next|confirm|go-|check|download', identifier) else 'div'
        shim_parts.append('<%s id="%s" hidden></%s>' % (kind, identifier, kind))
        aliases.append({'packId': identifier, 'boundTo': 'private inert node (#sx3-pack-shim)',
                        'exemplarControl': 'none — exemplar keeps ' + (
                            'navigation' if identifier in ('prev', 'next') else
                            'the timer' if 'timer' in identifier else
                            'progress' if 'progress' in identifier or 'stage-count' in identifier else
                            'reset' if 'reset' in identifier else 'its own controls'),
                        'verdict': 'neutralised' if re.search(r'prev|next|timer|reset', identifier) else 'inert'})
    for identifier in sorted(wanted & EXEMPLAR_OWNED):
        aliases.append({'packId': identifier, 'boundTo': "the exemplar's own element",
                        'exemplarControl': identifier, 'verdict': 'shared — pack reads only'})
    present_classes = set()
    for element in doc.xpath('//*[@class]'):
        present_classes |= set((element.get('class') or '').split())
    pack_tags = content.get('class_tags') or {}
    for name in sorted(wanted_classes - present_classes):
        tag = pack_tags.get(name, 'div')
        shim_parts.append('<%s class="%s" hidden></%s>' % (tag, name, tag))
        aliases.append({'packId': '.' + name, 'boundTo': 'private inert node (#sx3-pack-shim)',
                        'exemplarControl': 'none — the exemplar owns the served layout',
                        'verdict': 'neutralised'})

    if shim_parts:
        shim = LH.fragment_fromstring('<div id="sx3-pack-shim" hidden>' + ''.join(shim_parts) + '</div>')
        doc.body.insert(0, shim)
    if 'lesson-data' in wanted or doc.xpath('//script[contains(text(),"lesson-data")]'):
        data_script = etree.Element('script')
        doc.body.insert(0, data_script)
        data_script.set('id', 'lesson-data')
        data_script.set('type', 'application/json')
        data_script.text = json.dumps(content.get('lesson_data') or content.get('config') or {},
                                      ensure_ascii=False).replace('</', '<\\/')
        aliases.append({'packId': 'lesson-data', 'boundTo': 're-emitted from the pack',
                        'exemplarControl': 'none', 'verdict': 'inert'})
    report['aliases'] = aliases

    # The exemplar carries shell scripts (classic controls, TA wiring, the guide) AND one
    # lesson-specific block wired to ITS OWN lesson's DOM. Keeping the latter is what threw
    # "Cannot read properties of null": it binds to elements this lesson does not have.
    # Measured rule: drop an exemplar inline script that reaches for an id the exemplar has
    # and this deck does not. Nothing is dropped by name.
    live_ids = {e.get('id') for e in doc.xpath('//*[@id]')}
    exemplar_ids = {e.get('id') for e in LH.fromstring(exemplar_path.read_bytes()).xpath('//*[@id]')}
    gone = exemplar_ids - live_ids
    dropped_scripts = []
    for node in list(doc.xpath('//script[not(@src)]')):
        body = node.text or ''
        if node.get('id') in ('n6m-guide-js', 'lesson-config', 'lesson-data'):
            continue
        if 'CLASSIC_LESSON' in body or 'sx3-pack' == (node.get('id') or ''):
            continue
        hit = script_ids(body) & gone
        if hit:
            node.getparent().remove(node)
            dropped_scripts.append(sorted(hit)[:4])
    report['dropped_exemplar_scripts'] = dropped_scripts

    # Contract row 40: the pack opens its own dialogs with $('#dialog-'+key).showModal().
    # The transplant folds each pack dialog's BODY into the exemplar dialog that owns that
    # region (DIALOG_MAP) and nests the pack's id there so the pack's content hooks
    # ( $('#dialog-ko .organiser') ) still resolve to the same nodes. That nesting makes the
    # pack's id a <div>, so .showModal() threw. Remap, do not re-create: the nested wrapper
    # forwards showModal/show/close/open to the exemplar <dialog> that now holds the content,
    # so the pack's own control opens the dialog its content actually lives in. No second
    # dialog is created and no exemplar control is bound twice.
    source_ids = content.get('dialog_source_ids') or {}
    region_host = {key: identifier for identifier, key in DIALOG_MAP.items()}
    remap = {}
    for key, pack_id in source_ids.items():
        host_id = region_host.get(key)
        if not host_id or not pack_id or pack_id == host_id:
            continue
        if by_id(doc, pack_id) is None or by_id(doc, host_id) is None:
            continue
        remap[pack_id] = host_id
    if remap:
        node = etree.Element('script')
        node.set('id', 'sx3-dialog-remap')
        node.text = (
            "(function(){var m=%s;Object.keys(m).forEach(function(k){"
            "var n=document.getElementById(k),h=document.getElementById(m[k]);"
            "if(!n||!h||n===h||typeof h.showModal!=='function')return;"
            # Forward OPENING only. The pack's own [data-close] handler already does
            # this.closest('dialog').close(), which reaches the exemplar dialog because the
            # wrapper is nested inside it. Forwarding close as well fired a second close on
            # #ta-dialog, and the exemplar's own close handler strips .mbm-guide-on — which
            # its CSS needs to show the TA brief at all. Measured: 40 of 71 decks opened the
            # TA dialog to a blank 0x0 box until this forward was removed.
            "['showModal','show'].forEach(function(f){"
            "n[f]=function(){return h[f].apply(h,arguments);};});"
            "try{Object.defineProperty(n,'open',{get:function(){return h.open;},"
            "configurable:true});}catch(e){}});})();" % json.dumps(remap)
        )
        doc.body.append(node)
        for pack_id, host_id in sorted(remap.items()):
            aliases.append({'packId': pack_id, 'boundTo': '#' + host_id + ' (forwarded open/close)',
                            'exemplarControl': '#' + host_id,
                            'verdict': 'remapped to the dialog holding its content'})
    report['dialog_remap'] = remap

    # Row 42, emitted: a bubble-phase listener on each exemplar-owned control stops the event
    # reaching the document, so the pack's delegated [data-action] handler never sees it. The
    # exemplar's own per-element listeners are on the SAME element and still run —
    # stopPropagation does not touch them. Pack-owned [data-action] controls (its own
    # download, route and print buttons) carry no tag and keep working exactly as before.
    shell_controls = doc.xpath('//*[@data-sx3-shell]')
    if shell_controls:
        guard = etree.Element('script')
        guard.set('id', 'sx3-control-guard')
        guard.text = ("document.querySelectorAll('[data-sx3-shell]').forEach(function(el){"
                      "el.addEventListener('click',function(e){e.stopPropagation();});});")
        doc.body.append(guard)
    report['shell_controls_guarded'] = len(shell_controls)


    # ORDER SX3-GO2b ruling 1: do NOT re-inject the guidance block. The GROW and LAUNCH
    # exemplars carry n6m-guide:v1, so every deck normalised onto them inherited it — 23
    # census routes that never had it would have GAINED the marker, growing the pinned
    # identity set from 47 and breaking a digest the ruling holds fixed. A deck keeps exactly
    # the guidance state it already had: present stays present, absent stays absent. Decided
    # per deck from the served file, never from the exemplar and never by name.
    if had_guide is False:
        for node in doc.xpath('//style[@id="n6m-guide-css"]|//script[@id="n6m-guide-js"]'):
            node.getparent().remove(node)
        for node in doc.xpath('//comment()'):
            if 'n6m-guide' in (node.text or ''):
                node.getparent().remove(node)
        report['guide_block'] = 'stripped (deck had none)'
    else:
        report['guide_block'] = 'kept' if doc.xpath('//style[@id="n6m-guide-css"]') else 'none'

    # Contract row 41: a dialog the deck still carries must still be OPENABLE. All three
    # exemplars keep the knowledge-organiser opener inside slide 1, so the slide rebuild
    # takes it with them. BUILD and GROW packs happen to supply their own
    # [data-action="organiser"]; the LAUNCH packs do not, which left 38 decks carrying a
    # populated #organiser-dialog no teacher could open. Restore the exemplar's own opener
    # — same rule as row 39: a chassis control is kept when it still drives something, and
    # this one drives a dialog that exists and has content. Only the opener is restored;
    # the print button beside it calls the shell printSection() the pack has taken over, so
    # it stays a named gap and the pack's own organiser print (proved A4) serves.
    exemplar_doc = LH.fromstring(exemplar_path.read_bytes())
    restored_openers = []
    slides_now = doc.xpath('//main[@id="lessonDeck"]/section')
    for identifier in DIALOG_MAP:
        node = by_id(doc, identifier)
        if node is None:
            continue
        found = exemplar_doc.xpath('//*[@data-action][ancestor-or-self::*[@id=$i]]', i=identifier)
        openers = [e for e in exemplar_doc.xpath('//*[@data-action]')
                   if _opens_dialog(e.get('data-action'), identifier)]
        if not openers:
            continue
        action = openers[0].get('data-action')
        if doc.xpath('//*[@data-action=$a]', a=action):
            continue
        if not slides_now:
            continue
        parent = openers[0].getparent()
        host = LH.Element('div')
        host.set('class', parent.get('class') or 'knowledge-shortcut')
        clone = LH.fromstring(LH.tostring(openers[0]))
        for child in list(clone):
            clone.remove(child)
        clone.text = (openers[0].text_content() or '').strip()
        for attribute in list(clone.attrib):
            if attribute not in ('type', 'data-action', 'class', 'data-sx3-shell'):
                del clone.attrib[attribute]
        host.append(clone)
        slides_now[0].append(host)
        restored_openers.append(action)
        aliases.append({'packId': 'none — pack supplied no opener',
                        'boundTo': '#' + identifier,
                        'exemplarControl': '[data-action="%s"]' % action,
                        'verdict': 'exemplar opener restored (row 41)'})
    report['restored_openers'] = restored_openers

    # The exemplar's controls reach for estate attribute containers by name. Where the pack
    # spells the same thing differently, the pack's own wrapper takes the estate attribute —
    # the same structural mapping used for the arrival cells, recorded per deck so it is
    # auditable. Nothing is invented and no pack markup is replaced.
    ATTR_MAP = {'data-check': 'data-choice-task', 'data-sort-root': 'data-sort',
                'data-model-root': 'data-model', 'data-application-root': 'data-application'}
    mapped = []
    for estate_attr, pack_attr in ATTR_MAP.items():
        if doc.xpath('//*[@%s]' % estate_attr):
            continue
        hosts = doc.xpath('//*[@%s]' % pack_attr)
        if not hosts:
            continue
        for host in hosts:
            host.set(estate_attr, host.get(pack_attr) or '')
        mapped.append('%s <- %s (%d)' % (estate_attr, pack_attr, len(hosts)))
    report['attribute_mappings'] = mapped

    # The lesson-complete overlay is structural (contract row 8) AND content-bearing: the BUILD
    # exemplar's carries "BUILD · SCIENCE · Week 8 · Sugar evidence". Preserving the element
    # preserved its caption, so eleven decks rendered the exemplar's week. The caption is
    # rewritten from this deck's own title and its SPINE week — never the exemplar's, never a
    # literal carried over.
    overlay = by_id(doc, 'lc-overlay')
    if overlay is not None:
        week_text = ('Week %s · ' % spine_week) if spine_week else ''
        line = '%s · SCIENCE · %s%s' % (pathway, week_text, heading)
        for node in overlay.iter():
            if isinstance(node.tag, str) and node.text and re.search(r'·\s*SCIENCE\s*·', node.text, re.I):
                node.text = line
                report.setdefault('rewritten', []).append('#lc-overlay caption -> %r' % line)

    report['back_links'] = set_back_links(doc, pathway, target_rel)

    # A2, applied to EVERY relative href, not just the back-links. The exemplar's own sibling
    # navigation ("Next · W8L2 · Amylase and pH") and its resource downloads point at files
    # that sit next to the EXEMPLAR, not next to this deck. Shipping them would leave 37 of 75
    # decks carrying dead links. A link that does not resolve from this deck's own folder is
    # unwrapped to its text and named — never left clickable and broken.
    base = (ROOT / target_rel).parent

    # A2: the packs hardcode the origin. Rewrite an absolute Lessons URL to the real relative
    # path from THIS deck's folder — never to a bare basename, which is what turned three decks'
    # links into dead ends.
    prefix_rel = depth_prefix(target_rel)
    for anchor in doc.xpath('//a[@href]'):
        href = anchor.get('href') or ''
        match = re.match(r'https?://(?:www\.)?madebymatt\.uk/Lessons/(.*)$', href)
        if not match:
            continue
        rest = match.group(1)
        if rest.startswith('index.html'):
            anchor.set('href', prefix_rel + rest)
            continue
        path, _, query = rest.partition('?')
        target = ROOT / unquote(path)
        if target.is_file():
            anchor.set('href', os.path.relpath(target, base) + (('?' + query) if query else ''))
        else:
            anchor.set('href', prefix_rel + rest)

    dead = []
    for anchor in list(doc.xpath('//a[@href]')):
        href = anchor.get('href') or ''
        if href.startswith(('http://', 'https://', 'mailto:', '#', 'data:', 'javascript:')):
            continue
        if (base / href.split('?', 1)[0].split('#', 1)[0]).is_file():
            continue
        dead.append((href, re.sub(r'\s+', ' ', anchor.text_content() or '').strip()[:40]))
        parent = anchor.getparent()
        text = anchor.text_content() or ''
        tail = anchor.tail or ''
        index = list(parent).index(anchor)
        parent.remove(anchor)
        if index == 0:
            parent.text = (parent.text or '') + text + tail
        else:
            sibling = list(parent)[index - 1]
            sibling.tail = (sibling.tail or '') + text + tail
    report['dead_links_removed'] = dead

    # Row 44, applied: unwrap an exemplar anchor that points at ANOTHER lesson file. Unwrapped
    # to its text, exactly as a dead link is — never left clickable and never left claiming a
    # neighbouring lesson this deck does not have.
    own_name = Path(target_rel).name
    stale_nav = []
    for anchor in doc.xpath('//a[@href][@data-sx3-shell-link]'):
        href = (anchor.get('href') or '').split('#')[0].split('?')[0]
        name = href.rsplit('/', 1)[-1]
        if not (name.startswith('SCI_') and name.endswith('.html')) or name == own_name:
            continue
        stale_nav.append((name, re.sub(r'\s+', ' ', anchor.text_content() or '').strip()[:40]))
        parent = anchor.getparent()
        text = anchor.text_content() or ''
        tail = anchor.tail or ''
        index = list(parent).index(anchor)
        parent.remove(anchor)
        if index == 0:
            parent.text = (parent.text or '') + text + tail
        else:
            sibling = list(parent)[index - 1]
            sibling.tail = (sibling.tail or '') + text + tail
    report['exemplar_nav_unwrapped'] = stale_nav
    for anchor in doc.xpath('//a[@data-sx3-shell-link]'):
        del anchor.attrib['data-sx3-shell-link']

    out = etree.tostring(doc, method='html', encoding='unicode', doctype='<!doctype html>')
    source = exemplar_path.read_text(encoding='utf-8')
    blocks_src = re.findall(r'<!--n6-nav1:v1-->.*?<!--/n6-nav1-->', source, re.S)
    blocks_out = re.findall(r'<!--n6-nav1:v1-->.*?<!--/n6-nav1-->', out, re.S)
    # lxml's HTML parser lowercases camelCase SVG attribute names on READ, so they come back
    # lowercased on write even where the source had them right. viewBox and preserveAspectRatio
    # are case-sensitive; restoring them is a repair, not an edit.
    for camel in ('viewBox', 'preserveAspectRatio', 'gradientUnits', 'gradientTransform',
                  'patternUnits', 'markerWidth', 'markerHeight', 'clipPath', 'textLength',
                  'baseProfile', 'spreadMethod', 'refX', 'refY'):
        out = re.sub(r'(?<=[\s<])%s=' % camel.lower(), camel + '=', out)
        out = out.replace('<%s ' % camel.lower(), '<%s ' % camel).replace('</%s>' % camel.lower(), '</%s>' % camel)

    if len(blocks_src) == len(blocks_out):
        prefix = depth_prefix(target_rel)
        for old, src in zip(blocks_out, blocks_src):
            out = out.replace(old, src.replace('href="../../../index.html"',
                                               'href="%sindex.html"' % prefix), 1)

    # Contract row 43: estate navigation furniture the SERVED deck already carried, which its
    # exemplar does not supply, is restored rather than dropped. The BUILD exemplar is an aut1
    # lesson and reaches the catalogue through the runtime HUD, so it carries no <a class=
    # "mbmhome">; the eleven BUILD decks normalised onto it are aut2 pack members, where the
    # published offline-pack gate requires a visible home control ("Reachable lesson home
    # control"). Eleven decks lost their way back to the catalogue. This is the deck's own
    # furniture, put back verbatim with its href re-derived for this deck's depth — never
    # invented, and never taken from the exemplar.
    prefix = depth_prefix(target_rel)
    prior_text = prior if isinstance(prior, str) else (prior or b'').decode('utf-8', 'replace')
    restored_furniture = []
    if prior_text:
        insert = []
        if not blocks_out:
            for block in re.findall(r'<!--n6-nav1:v1-->.*?<!--/n6-nav1-->', prior_text, re.S):
                insert.append(block.replace('href="../../../index.html"',
                                            'href="%sindex.html"' % prefix))
                restored_furniture.append('n6-nav1:v1')
        if 'class="mbmhome"' not in out:
            for link in re.findall(r'<a class="mbmhome"[^>]*>.*?</a>', prior_text, re.S):
                insert.append(re.sub(r'href="[^"]*"', 'href="%sindex.html"' % prefix, link, count=1))
                restored_furniture.append('a.mbmhome')
                break
        if insert:
            out = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + ''.join(insert), out, count=1)
        # A1: the Live-Teaching HUD tag is cross-repo furniture in its exact verbatim form,
        # <script defer src="/hud.js"></script>, at the end of body. The BUILD exemplar carries
        # it; the GROW and LAUNCH exemplars do not, so 15 LAUNCH decks that HAD it lost it and
        # the published aut1 pack gate waited 12s for a #mbmhud-pill that could never appear.
        # Restored only where the served deck already had it, verbatim, never re-pointed.
        hud_tag = '<script defer src="/hud.js"></script>'
        if 'src="/hud.js"' in prior_text and 'src="/hud.js"' not in out:
            out = out.replace('</body>', hud_tag + '</body>', 1)
            restored_furniture.append('hud.js tag')
    report['restored_furniture'] = restored_furniture
    return out, report
