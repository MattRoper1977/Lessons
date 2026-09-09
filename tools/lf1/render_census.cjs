// tools/lf1/render_census.cjs - a RENDERED census of a phrase across lesson pages.
//
// Why this exists: the first LF1 measurement counted matching LINES with a source
// grep and reported 31 occurrences. The real figure was 121, and two of the three
// worst pages were not in the search set at all. A claim about what a pupil reads
// has to be measured on the DOM a browser builds, on every route the page has.
//
// Per page it reports each occurrence once, and says which routes render it:
//
//   deck   - visible at some point while driving the real slide control forward
//            (showSlide lives inside a closure on these decks, so the walk clicks
//            #next and falls back to ArrowRight; a count taken on slide 1 is not
//            the deck)
//   print  - visible under print emulation, which is a different subtree: the
//            .printpack worksheet a pupil is handed on paper
//   guide  - visible with html.mbm-guide-on, the staff/TA layer
//   staff  - the occurrence itself sits inside [data-mbm-guide]
//
// It also reports GUIDE-DOUBLED pairs: a pupil-facing node and its
// span.mbm-cal-staff twin rendering together with guide on, which reads as the
// placeholder immediately followed by the real week ("...for the the next unit
// rock investigation.Write or select one clear question for the W14 rock
// investigation."). That is what a source-level tag strip shows too.
//
// Usage:  node tools/lf1/render_census.cjs <file-list> <out.json> [--phrase "..."]
//         LESSONS_ROOT=<tree>  SITE_ROOT=<site tree>
// Exit 1 if any occurrence renders on any route, 0 if none does.
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const http = require('http'), fs = require('fs'), path = require('path');

const SITE = process.env.SITE_ROOT || '/home/user/mattroper1977.github.io';
const LES  = process.env.LESSONS_ROOT || process.cwd();
const PHRASES = (process.argv.includes('--phrase')
  ? [process.argv[process.argv.indexOf('--phrase') + 1]]
  : ['the previous unit', 'the next unit']);
const TYPES = {'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml',
  '.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.mp4':'video/mp4',
  '.json':'application/json','.pdf':'application/pdf','.woff2':'font/woff2','.txt':'text/plain'};

(async () => {
  const pages = fs.readFileSync(process.argv[2], 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
  const server = http.createServer((q, r) => {
    const c = decodeURIComponent(q.url.split('?')[0].split('#')[0]);
    const p = c.startsWith('/Lessons/') ? path.join(LES, c.slice('/Lessons/'.length))
                                        : path.join(SITE, c.replace(/^\//, ''));
    if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404).end(''); return; }
    r.writeHead(200, {'content-type': TYPES[path.extname(p).toLowerCase()] || 'application/octet-stream'});
    r.end(fs.readFileSync(p));
  });
  await new Promise(res => server.listen(0, '127.0.0.1', res));
  const base = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch();
  const out = {};

  // One stable id per occurrence: text-node ordinal in body order, plus which
  // match within that node. Every route uses the same walker, so the routes can
  // be unioned without guessing that two counts refer to the same words.
  const SCAN = (phrases) => {
    const rx = new RegExp(phrases.map(p => p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), 'g');
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const rows = []; let n, i = 0;
    while ((n = w.nextNode())) {
      i++;
      const el = n.parentElement;
      if (!el || ['SCRIPT','STYLE','TEMPLATE','NOSCRIPT'].includes(el.tagName)) continue;
      const m = n.nodeValue.match(rx);
      if (!m) continue;
      let hidden = false;
      for (let x = el; x; x = x.parentElement) {
        const cs = getComputedStyle(x);
        if (cs.display === 'none' || cs.visibility === 'hidden') { hidden = true; break; }
      }
      const staff = !!el.closest('[data-mbm-guide], .mbm-cal-staff, .ta-drawer, .staff-only, .teacher-only');
      const p = []; for (let x = el; x && x.tagName; x = x.parentElement)
        p.unshift(x.tagName.toLowerCase() + (typeof x.className === 'string' && x.className.trim()
          ? '.' + x.className.trim().split(/\s+/)[0] : ''));
      for (let k = 0; k < m.length; k++)
        rows.push({id: i + ':' + k, hidden, staff, path: p.slice(-4).join('>'), kind: 'text',
                   text: n.nodeValue.replace(/\s+/g, ' ').trim().slice(0, 240)});
    }
    // Accessible names are read aloud, so they are pupil-facing text too. Three
    // of the 121 LF1 occurrences were aria-labels and no text walker sees them.
    let j = 0;
    for (const el of document.querySelectorAll('[aria-label],[title],[alt],[data-title]')) {
      j++;
      for (const a of ['aria-label', 'title', 'alt', 'data-title']) {
        const v = el.getAttribute(a); if (!v) continue;
        const mm = v.match(rx); if (!mm) continue;
        let hidden = false;
        for (let x = el; x; x = x.parentElement) {
          const cs = getComputedStyle(x);
          if (cs.display === 'none' || cs.visibility === 'hidden') { hidden = true; break; }
        }
        for (let k = 0; k < mm.length; k++)
          rows.push({id: 'a' + j + ':' + a + ':' + k, hidden, staff: !!el.closest('[data-mbm-guide]'),
                     path: el.tagName.toLowerCase() + '[' + a + ']', kind: 'attr',
                     text: v.replace(/\s+/g, ' ').trim().slice(0, 240)});
      }
    }
    return rows;
  };

  for (const rel of pages) {
    let ctx = await browser.newContext({viewport: {width: 1280, height: 900}});
    let page = await ctx.newPage();
    await page.goto(base + '/Lessons/' + rel.split('/').map(encodeURIComponent).join('/'),
                    {waitUntil: 'load', timeout: 60000});
    await page.waitForTimeout(350);

    const seen = new Map();          // id -> {routes, meta}
    const absorb = (rows, route) => rows.forEach(r => {
      const e = seen.get(r.id) || (seen.set(r.id, {routes: new Set(), staff: r.staff, path: r.path, text: r.text, kind: r.kind}), seen.get(r.id));
      if (!r.hidden) e.routes.add(route);
      if (route === 'dom') e.routes.add('dom');       // present in the document at all
    });

    absorb(await page.evaluate(SCAN, PHRASES), 'dom');
    const slides = await page.evaluate(() => document.querySelectorAll('.slide,[data-slide]').length || 1);

    // Press the controls that gate pupil-facing content. .tier is display:none
    // until its tier button is pressed and .model-step / .scaffold until their
    // reveal is; content behind one press is pupil-facing, so leaving it
    // unpressed is an undercount, not a caveat.
    // Press each control and sample AFTER EACH ONE. Pressing them in a batch and
    // sampling once only ever shows the last tier chosen: Supported, Standard and
    // Stretch are three separate panels and a pupil sees whichever their teacher
    // selects, so all three have to be sampled.
    // Two chassis, two conventions: the Science decks gate on data-attributes,
    // the Humanities ones on inline onclick="tier(...)" / "toggle(...)" with a
    // .tierbtn or aria-expanded button. Missing the second left three Standard
    // and Stretch panels uncounted.
    const GATES = '[data-reveal],[data-toggle],[data-tier-button],.tierbtn,button[aria-expanded]';
    const openEverything = async (route) => {
      const n = await page.evaluate((g) => document.querySelectorAll(g).length, GATES);
      for (let round = 0; round < 3; round++) {        // model reveals advance one step per press
        for (let k = 0; k < n; k++) {
          await page.evaluate(([g, i]) => {
            const el = document.querySelectorAll(g)[i]; if (el) { try { el.click(); } catch (e) {} }
          }, [GATES, k]);
          await page.waitForTimeout(40);
          absorb(await page.evaluate(SCAN, PHRASES), route);
        }
      }
    };

    // PRINT first, on the page as loaded. The worksheet has its own tier
    // selector, so the honest figure is the union over every tier a teacher can
    // print -- and it has to be taken before the deck presses, which change it.
    await page.emulateMedia({media: 'print'}); await page.waitForTimeout(150);
    absorb(await page.evaluate(SCAN, PHRASES), 'print');
    const tiers = await page.evaluate(() => document.querySelectorAll('[data-print-tier]').length);
    for (let t = 0; t < tiers; t++) {
      await page.evaluate((k) => { const b = document.querySelectorAll('[data-print-tier]')[k]; if (b) b.click(); }, t);
      await page.waitForTimeout(90);
      absorb(await page.evaluate(SCAN, PHRASES), 'print');
    }
    await page.emulateMedia({media: 'screen'});

    // DECK on a clean load, so the print-tier presses above cannot colour it.
    await page.reload({waitUntil: 'load'}); await page.waitForTimeout(350);
    await openEverything('deck'); await page.waitForTimeout(120);
    absorb(await page.evaluate(SCAN, PHRASES), 'deck');
    for (let i = 0; i < slides + 3; i++) {
      const clicked = await page.evaluate(() => {
        const el = document.querySelector('#next,[data-nav="next"],button[aria-label*="Next" i]');
        if (el) { el.click(); return true; } return false;
      });
      if (!clicked) await page.keyboard.press('ArrowRight');
      await page.waitForTimeout(80);
      await openEverything('deck'); await page.waitForTimeout(90);
      absorb(await page.evaluate(SCAN, PHRASES), 'deck');
    }

    // The guide pass needs a genuinely clean page, not a reload. These decks
    // persist the chosen tier, so after the deck walk a reload comes back with
    // whatever tier was selected last and the other panels hidden -- which
    // silently hid three of the adjacent-identical pairs the first time.
    await ctx.close();
    ctx = await browser.newContext({viewport: {width: 1280, height: 900}});
    page = await ctx.newPage();
    await page.goto(base + '/Lessons/' + rel.split('/').map(encodeURIComponent).join('/'),
                    {waitUntil: 'load', timeout: 60000});
    await page.waitForTimeout(400);
    await page.evaluate(() => document.documentElement.classList.add('mbm-guide-on'));
    await page.waitForTimeout(120);
    absorb(await page.evaluate(SCAN, PHRASES), 'guide');
    // LF1-B 2.2: two adjacent rendered nodes saying exactly the same thing. This
    // is measured with guide ON, the strictest view, because that is where a
    // pupil-facing line and its staff twin can both render.
    const adjacent = await page.evaluate(() => {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      const vis = []; let n;
      while ((n = w.nextNode())) {
        const el = n.parentElement; if (!el || ['SCRIPT','STYLE'].includes(el.tagName)) continue;
        let hidden = false;
        for (let x = el; x; x = x.parentElement) {
          const cs = getComputedStyle(x);
          if (cs.display === 'none' || cs.visibility === 'hidden') { hidden = true; break; }
        }
        const t = n.nodeValue.replace(/\s+/g, ' ').trim();
        if (!hidden && t.length >= 20) vis.push(t);
      }
      const out = [];
      for (let i = 1; i < vis.length; i++) if (vis[i] === vis[i - 1]) out.push(vis[i].slice(0, 120));
      return out;
    });

    const doubled = await page.evaluate(() => {
      const pairs = [];
      for (const s of document.querySelectorAll('span.mbm-cal-staff')) {
        if (getComputedStyle(s).display === 'none') continue;
        const host = s.parentElement; if (!host) continue;
        const before = (host.textContent || '').replace(s.textContent || '', '');
        if (/the previous unit|the next unit/.test(before))
          pairs.push({shown: before.replace(/\s+/g, ' ').trim().slice(0, 150),
                      twin: (s.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 150)});
      }
      return pairs;
    });
    await page.evaluate(() => document.documentElement.classList.remove('mbm-guide-on'));

    out[rel] = {slides, guideDoubled: doubled, adjacentIdentical: adjacent,
      occurrences: [...seen.entries()].map(([id, e]) => ({id, routes: [...e.routes], staff: e.staff, path: e.path, kind: e.kind, text: e.text}))};
    await ctx.close();
    process.stderr.write('.');
  }
  await browser.close(); server.close();
  fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
  process.stderr.write('\n');

  const tot = (f) => Object.values(out).reduce((a, o) => a + o.occurrences.filter(f).length, 0);
  const R = (r) => (x) => x.routes.includes(r);
  const rendered = (x) => x.routes.some(r => r !== 'dom');
  console.log('pages                       : ' + pages.length);
  console.log('occurrences in the document : ' + tot(() => true));
  console.log('  rendered on the DECK      : ' + tot(R('deck')));
  console.log('  rendered in PRINT         : ' + tot(R('print')));
  console.log('  rendered with GUIDE on    : ' + tot(R('guide')));
  console.log('  rendered on NO route      : ' + tot(x => !rendered(x)));
  console.log('  inside a staff layer      : ' + tot(x => x.staff));
  console.log('  in an accessible name     : ' + tot(x => x.kind === 'attr'));
  console.log('guide-doubled pairs         : ' + Object.values(out).reduce((a, o) => a + o.guideDoubled.length, 0));
  console.log('adjacent identical nodes    : ' + Object.values(out).reduce((a, o) => a + o.adjacentIdentical.length, 0) + '   (guide on, >=20 chars)');
  for (const k of pages) {
    const o = out[k]; if (!o.occurrences.length) continue;
    console.log('  ' + k.split('/').pop().slice(0, 52).padEnd(54) +
      ('dom ' + o.occurrences.length).padStart(8) +
      ('deck ' + o.occurrences.filter(R('deck')).length).padStart(9) +
      ('print ' + o.occurrences.filter(R('print')).length).padStart(10) +
      ('guide ' + o.occurrences.filter(R('guide')).length).padStart(10) +
      ('doubled ' + o.guideDoubled.length).padStart(12));
  }
  process.exit(tot(rendered) ? 1 : 0);
})();
