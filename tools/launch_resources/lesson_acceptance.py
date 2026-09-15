"""All-stage lesson acceptance (the tools/grow_resources/friction_acceptance.py
procedure, parametrised): accessibility, keyboard, layout, enlarged text, motion,
media, no-JavaScript and print, standalone and over local HTTP.

Local browser evidence only. It is not live publication proof, not a served-file
check and not a human assistive-technology journey. Requires Python Playwright
(Chromium), PyMuPDF and axe-core at NODE_PATH/axe-core/axe.min.js.

    NODE_PATH=/path/to/node_modules python3 tools/launch_resources/lesson_acceptance.py CONFIG.json REPO_ROOT OUT_DIR

CONFIG.json names the lesson (rel), its stage timers, resource pages, print sections,
the per-route print sections, the pack exclusions and the no-JS expectations.
"""
import functools, http.server, json, os, sys, threading
from pathlib import Path
import pymupdf as fitz
from playwright.sync_api import sync_playwright

CFG = json.loads(Path(sys.argv[1]).read_text())
ROOT = Path(sys.argv[2]).resolve(); OUT = Path(sys.argv[3]).resolve(); OUT.mkdir(parents=True, exist_ok=True)
AXE = Path(os.environ['NODE_PATH']) / 'axe-core/axe.min.js'
REL = CFG['rel']; RESOURCE_PAGES = CFG.get('resource_pages', []); TIMERS = CFG['timers']; N = len(TIMERS)
WIDTHS = [320, 390, 768, 1280]
PRINT_SECTIONS = CFG['print_sections']; ROUTED = set(CFG['routed_sections']); PACK_EXCLUDED = set(CFG['pack_excluded'])
NOJS = CFG['nojs']
LEVELS = ['supported', 'standard', 'stretch']


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass


server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
report = {'scope': __doc__.strip(), 'config': CFG, 'stages': [], 'keyboard': [], 'enlarged': [], 'themes': [], 'media': [], 'nojs': [],
          'prints': [], 'packs': [], 'resource_pages': [], 'errors': [], 'console_errors': []}


def overflow(page, width):
    return page.evaluate('''(w)=>{const q=s=>[...document.querySelectorAll(s)];const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
      const active=document.querySelector('.slide.active')||document.body;
      const scrolls=e=>{for(let a=e.parentElement;a;a=a.parentElement){const o=getComputedStyle(a).overflowX;if(o==='auto'||o==='scroll')return true}return false};const lim=Math.min(w+1,active.getBoundingClientRect().right+1);const wide=q('.slide.active *, .controls *, .progress-label').filter(e=>vis(e)&&!scrolls(e)&&e.getBoundingClientRect().right>(e.closest('.slide.active')?lim:w+1)).map(e=>e.tagName+'#'+e.id+'.'+String(e.className).slice(0,30));
      return {docScrollWidth:document.documentElement.scrollWidth, slideScroll:active.scrollWidth, slideClient:active.clientWidth, wide:wide.slice(0,6)}}''', width)


def axe(page, context=None):
    page.add_script_tag(path=str(AXE))
    return page.evaluate('''async (ctx)=>{const r=await axe.run(ctx||document,{resultTypes:['violations']});
      return r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.length,targets:v.nodes.slice(0,3).map(n=>n.target.join(' '))}))}''', context)


def new_page(browser, width, height=900, **kw):
    ctx = browser.new_context(viewport={'width': width, 'height': height}, **kw)
    page = ctx.new_page(); page.set_default_timeout(8000)
    page.on('pageerror', lambda e: report['errors'].append(str(e)))
    page.on('console', lambda m: report['console_errors'].append(m.text) if m.type == 'error' and 'hud.js' not in m.text else None)
    return ctx, page


def stage_checks(browser, mode, url, width, motion):
    ctx, page = new_page(browser, width, reduced_motion=motion)
    page.goto(url)
    assert page.locator('.slide').count() == N
    assert page.locator('.slide').evaluate_all('ns=>ns.map(n=>Number(n.dataset.timer))') == TIMERS
    for i in range(N):
        page.evaluate('(i)=>showSlide(i)', i); page.wait_for_timeout(120 if motion == 'reduce' else 900)
        title = page.locator('.slide.active').get_attribute('data-title')
        focus = page.evaluate("()=>{const a=document.activeElement;return a?a.tagName+'#'+a.id+':'+(a.textContent||'').trim().slice(0,40):null}")
        ov = overflow(page, width)
        violations = axe(page)
        report['stages'].append({'mode': mode, 'width': width, 'motion': motion, 'index': i, 'title': title, 'focus': focus, 'overflow': ov, 'axe': violations})
        assert ov['docScrollWidth'] <= width + 1 and not ov['wide'], (mode, width, i, ov)
        assert not [v for v in violations if v['impact'] in ('serious', 'critical')], (mode, width, motion, i, violations)
        if width == 1280 and motion == 'reduce':
            page.screenshot(path=str(OUT / f'{mode}-{width}-stage{i}.png'))
    page.evaluate('()=>showSlide(0)'); page.wait_for_timeout(100)
    for i in range(N - 1):
        page.locator('.slide.active h1, .slide.active h2').first.focus()
        presses = 0
        while presses < 12:
            page.keyboard.press('ArrowRight'); page.wait_for_timeout(120); presses += 1
            idx = page.evaluate("()=>[...document.querySelectorAll('.slide')].indexOf(document.querySelector('.slide.active'))")
            if idx != i:
                break
        heading_focused = page.evaluate("()=>{const a=document.activeElement;return !!a&&/^H[12]$/.test(a.tagName)&&!!a.closest('.slide.active')}")
        report['keyboard'].append({'mode': mode, 'width': width, 'motion': motion, 'from': i, 'to': idx, 'presses': presses, 'headingFocused': heading_focused})
        assert idx == i + 1 and heading_focused, (mode, width, i, idx, presses, heading_focused)
    page.keyboard.press('ArrowLeft'); page.wait_for_timeout(100)
    assert page.evaluate("()=>[...document.querySelectorAll('.slide')].indexOf(document.querySelector('.slide.active'))") == N - 2
    ctx.close()


def enlarged(browser, mode, url):
    for label, width, dsf, font in [('zoom200-1280', 640, 2, None), ('reflow320-dsf2', 320, 2, None), ('text200-1280', 1280, 1, '200%'), ('text200-390', 390, 1, '200%')]:
        ctx, page = new_page(browser, width, 450 if dsf == 2 else 900, device_scale_factor=dsf, reduced_motion='reduce')
        page.goto(url)
        if font:
            page.evaluate("(f)=>{document.documentElement.style.fontSize=f}", font)
        worst = []
        for i in range(N):
            page.evaluate('(i)=>showSlide(i)', i); page.wait_for_timeout(100)
            ov = overflow(page, width)
            controls = page.evaluate("()=>[...document.querySelectorAll('.controls button')].map(b=>{const r=b.getBoundingClientRect();return {t:b.textContent.trim().slice(0,12),h:Math.round(r.height),w:Math.round(r.width),visible:r.width>0&&r.right<=innerWidth+1}})")
            worst.append({'index': i, 'docScrollWidth': ov['docScrollWidth'], 'wide': ov['wide'], 'controls': controls})
            if i in (1, N - 3):
                page.screenshot(path=str(OUT / f'{mode}-{label}-stage{i}.png'))
        report['enlarged'].append({'mode': mode, 'label': label, 'viewport': width, 'stages': worst})
        assert all(s['docScrollWidth'] <= width + 1 and not s['wide'] for s in worst), (label, [s for s in worst if s['wide']])
        assert all(all(c['visible'] and c['h'] >= 24 for c in s['controls']) for s in worst), label
        ctx.close()


def themes(browser, mode, url):
    for label, kw in [('dark', {'color_scheme': 'dark'}), ('forced-colors', {'forced_colors': 'active'})]:
        ctx, page = new_page(browser, 1280, reduced_motion='reduce', **kw)
        page.goto(url)
        rows = []
        for i in sorted(set([0, 1, 3, N - 3, N - 2, N - 1])):
            page.evaluate('(i)=>showSlide(i)', i); page.wait_for_timeout(300)
            rows.append({'index': i, 'axe': axe(page)})
            if i in (1, N - 3):
                page.screenshot(path=str(OUT / f'{mode}-{label}-stage{i}.png'))
        report['themes'].append({'mode': mode, 'label': label, 'stages': rows})
        assert not [v for r in rows for v in r['axe'] if v['impact'] in ('serious', 'critical') and not (label == 'forced-colors' and v['id'] == 'color-contrast')], (label, rows)
        ctx.close()


def media(browser, mode, base):
    ctx, page = new_page(browser, 1280, reduced_motion='reduce')
    page.goto(base(REL))
    lesson_media = page.evaluate("()=>document.querySelectorAll('video,audio,iframe,[autoplay]').length")
    animated = page.evaluate("()=>[...document.querySelectorAll('*')].filter(e=>{const s=getComputedStyle(e);return s.animationName!=='none'&&s.animationDuration!=='0s'}).length")
    external = page.evaluate("()=>[...document.querySelectorAll('[src]')].map(e=>e.getAttribute('src')).filter(s=>/^https?:/.test(s))")
    report['media'].append({'mode': mode, 'lessonMediaElements': lesson_media, 'runningAnimationsUnderReducedMotion': animated, 'externalSrcLoaded': external})
    assert lesson_media == 0 and not external, (lesson_media, external)
    for rel in RESOURCE_PAGES:
        page.goto(base(rel))
        info = page.evaluate("()=>[...document.querySelectorAll('video,audio')].map(v=>({tag:v.tagName,autoplay:v.autoplay,controls:v.controls,preload:v.preload,paused:v.paused,tracks:v.querySelectorAll('track').length,fallbackText:v.textContent.trim().slice(0,60),hasLocalSource:!!v.querySelector('source[src]')}))")
        violations = axe(page)
        report['resource_pages'].append({'mode': mode, 'page': rel, 'media': info, 'axe': violations,
                                         'dayWords': page.evaluate("()=>/Monday|Tuesday|\\d\\d:\\d\\d/.test(document.body.innerText)")})
        assert all(not m['autoplay'] and m['controls'] and m['paused'] and m['preload'] == 'none' for m in info), (rel, info)
        assert not [v for v in violations if v['impact'] in ('serious', 'critical')], (rel, violations)
    ctx.close()


def nojs(browser, mode, url):
    for width in (320, 1280):
        ctx, page = new_page(browser, width, java_script_enabled=False)
        page.goto(url)
        r = page.evaluate('''([w,cfg])=>{const q=s=>[...document.querySelectorAll(s)];const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=='hidden'};
          return {slides:q('.slide').filter(vis).length, arrivalQuestions:q(cfg.arrivalQuestionSelector).filter(vis).length,
            exitItems:q(cfg.exitItemSelector).filter(vis).length, organiser:vis(document.getElementById('print-ko')), note:vis(document.querySelector('.nojs-note')),
            controls:q('.controls,.progress-label').filter(vis).length, docScrollWidth:document.documentElement.scrollWidth,
            wide:q('body *').filter(e=>vis(e)&&!(function(x){for(let a=x.parentElement;a;a=a.parentElement){const o=getComputedStyle(a).overflowX;if(o==='auto'||o==='scroll')return true}return false})(e)&&e.getBoundingClientRect().right>w+1).map(e=>e.tagName+'#'+e.id+'.'+String(e.className).slice(0,30)).slice(0,5)}}''', [width, NOJS])
        report['nojs'].append({'mode': mode, 'width': width, **r})
        page.screenshot(path=str(OUT / f'{mode}-nojs-{width}.png'))
        assert r['slides'] == N and r['arrivalQuestions'] == NOJS['arrivalQuestions'] and r['exitItems'] == NOJS['exitItems'] and r['organiser'] and r['note'] and r['controls'] == 0 and r['docScrollWidth'] <= width + 1 and not r['wide'], r
        ctx.close()


def pdf_pages(path):
    doc = fitz.open(path)
    return len(doc), [len(p.get_text().strip()) for p in doc]


def prints(browser, mode, url):
    ctx, page = new_page(browser, 1280, reduced_motion='reduce')
    page.goto(url); page.evaluate("()=>{window.print=()=>{window.__printed=(window.__printed||0)+1}}")
    for section in PRINT_SECTIONS:
        levels = LEVELS if section in ROUTED else ['standard']
        for level in levels:
            page.evaluate("([id,l])=>printSection(id,l)", [section, level])
            visible = page.evaluate("()=>[...document.querySelectorAll('.print-section.visible')].map(e=>e.id)")
            target = OUT / f'{mode}-print-{section}-{level}.pdf'
            page.pdf(path=str(target), format='A4', print_background=True)
            pages, text = pdf_pages(target)
            report['prints'].append({'mode': mode, 'section': section, 'level': level, 'visibleSections': visible, 'pages': pages, 'textPerPage': text})
            assert visible == ['print-' + section] and pages >= 1 and all(t > 0 for t in text), (section, level, visible, pages, text)
    for level in LEVELS:
        page.evaluate("(l)=>printArm(l)", level)
        visible = page.evaluate("()=>[...document.querySelectorAll('.print-section.visible')].map(e=>e.id)")
        target = OUT / f'{mode}-pack-{level}.pdf'
        page.pdf(path=str(target), format='A4', print_background=True)
        pages, text = pdf_pages(target)
        report['packs'].append({'mode': mode, 'level': level, 'visibleSections': visible, 'pages': pages, 'textPerPage': text})
        assert all(t > 0 for t in text), (level, text)
        assert not any(s in visible for s in PACK_EXCLUDED), visible
        if mode == 'standalone':
            doc = fitz.open(target)
            for n, pg in enumerate(doc, 1):
                pg.get_pixmap(dpi=60).save(str(OUT / f'pack-{level}-p{n:02d}.png'))
    ctx.close()


with sync_playwright() as p:
    browser = p.chromium.launch()
    for mode, base in [('standalone', lambda rel: (ROOT / rel).as_uri()), ('http', lambda rel: f'http://127.0.0.1:{server.server_port}/{rel}')]:
        url = base(REL)
        for width in WIDTHS:
            stage_checks(browser, mode, url, width, 'reduce')
        for width in (390, 1280):
            stage_checks(browser, mode, url, width, 'no-preference')
        enlarged(browser, mode, url); themes(browser, mode, url); media(browser, mode, base); nojs(browser, mode, url); prints(browser, mode, url)
    browser.close()

report['summary'] = {
    'stageCases': len(report['stages']), 'axeRunsZeroViolations': sum(1 for s in report['stages'] if not s['axe']),
    'axeRunsWithMinorOrModerate': [(s['mode'], s['width'], s['index'], s['axe']) for s in report['stages'] if s['axe']][:20],
    'keyboardTransitions': len(report['keyboard']), 'enlargedCases': len(report['enlarged']), 'themeCases': len(report['themes']),
    'nojsCases': len(report['nojs']), 'printCases': len(report['prints']), 'packCases': len(report['packs']),
    'multiPagePrints': [(r['mode'], r['section'], r['level'], r['pages']) for r in report['prints'] if r['pages'] > 1],
    'packPages': [(r['mode'], r['level'], r['pages']) for r in report['packs']],
    'pageErrors': report['errors'], 'consoleErrors': report['console_errors'][:10], 'result': 'PASS'}
(OUT / 'acceptance-report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
print(json.dumps(report['summary'], indent=2, ensure_ascii=False))
