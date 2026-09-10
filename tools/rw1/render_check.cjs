// RW1-B §H4/§H3 · prove the two fixes FUNCTION, and settle the one row where the
// substring count and the DOM count disagree.
//
// The static parse says button.n6m-guide-btn is 0 in BOTH the live file and ours,
// against a substring count of 6. Either the estate has been shipping a guide
// toggle that does not exist, or the button is created at runtime by the carried
// script. A static parse cannot tell those apart. This renders and asks.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs'), path = require('path');

const FILES = process.argv.slice(2).filter(a => !a.startsWith('--'));
const PLANT = process.argv.includes('--plant-strip-splash');

(async () => {
  const browser = await chromium.launch();
  let bad = 0;
  for (const f of FILES) {
    let html = fs.readFileSync(f, 'utf8');
    // Balanced walk, not a regex. The first plant used
    //   /<div class="n6-splash">[\s\S]*?<\/div>\s*<\/div>/
    // which never matched, so the "red proof" proved nothing and reported PASS on
    // a file it had not touched. A plant that cannot fire is worse than no plant.
    if (PLANT) {
      const k = html.indexOf('<div class="n6-splash"');
      if (k < 0) throw new Error('PLANT CANNOT FIRE: no splash div to remove');
      let depth = 0, i = k;
      while (i < html.length) {
        if (html.startsWith('<div', i)) { depth++; i += 4; }
        else if (html.startsWith('</div>', i)) { depth--; i += 6; if (!depth) break; }
        else i++;
      }
      if (depth !== 0) throw new Error('PLANT CANNOT FIRE: unbalanced splash block');
      html = html.slice(0, k) + html.slice(i);
    }
    const tmp = path.join(path.dirname(f), '.rw1-render-' + path.basename(f));
    fs.writeFileSync(tmp, html);
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await ctx.newPage();
    // GW1-B R1: a zero is only a result next to its denominator. "0 console
    // errors" is vacuous if the page logged nothing at all, and "0 non-file
    // requests" is vacuous if it made no requests. Count both populations.
    const errors = [], requests = [];
    let consoleTotal = 0, requestTotal = 0;
    page.on('console', m => { consoleTotal++; if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push('pageerror: ' + e.message));
    page.on('request', r => { requestTotal++; const u = new URL(r.url()); if (u.protocol !== 'file:') requests.push(u.host); });
    await page.goto('file://' + path.resolve(tmp), { waitUntil: 'load' });

    const r = await page.evaluate(() => {
      const q = s => document.querySelectorAll(s).length;
      const splash = document.querySelector('div.n6-splash');
      const box = splash && splash.getBoundingClientRect();
      const btn = document.querySelector('button.n6m-guide-btn') || document.querySelector('.n6m-guide-btn');
      const bb = btn && btn.getBoundingClientRect();
      return {
        splashInDom: !!splash,
        splashVisible: !!(box && box.width > 0 && box.height > 0),
        splashSvg: splash ? splash.querySelectorAll('svg').length : 0,
        splashLabel: splash ? (splash.querySelector('svg')?.getAttribute('aria-label') || '') : '',
        guideBtnInDom: !!btn,
        guideBtnVisible: !!(bb && bb.width > 0 && bb.height > 0),
        guideBtnText: btn ? (btn.textContent || '').trim().slice(0, 40) : '',
        skip: q('a.skip'), deck: q('#lessonDeck'),
        deckIsSlideContainer: !!document.querySelector('main#lessonDeck.slide-container'),
        dupIds: (() => { const m = new Map(); document.querySelectorAll('[id]').forEach(e => m.set(e.id, (m.get(e.id) || 0) + 1)); return [...m].filter(([, n]) => n > 1).map(([i]) => i); })(),
        idTotal: document.querySelectorAll('[id]').length,
        elementTotal: document.querySelectorAll('*').length,
      };
    });

    // H4: the skip link must MOVE FOCUS to the deck, not merely exist.
    let focusMoved = null;
    if (r.skip) {
      await page.click('a.skip');
      focusMoved = await page.evaluate(() => {
        const a = document.activeElement;
        const d = document.getElementById('lessonDeck');
        return !!(a && d && (a === d || d.contains(a) || location.hash === '#lessonDeck'));
      });
    }

    const name = path.basename(f);
    console.log('=== %s%s', name, PLANT ? '   [PLANTED: splash stripped]' : '');
    console.log('   splash  in DOM %s · visible %s · svg %d · aria-label "%s"',
      r.splashInDom, r.splashVisible, r.splashSvg, r.splashLabel);
    console.log('   guide   button in DOM %s · visible %s · text "%s"   <- the SUB≠DOM row, answered by rendering',
      r.guideBtnInDom, r.guideBtnVisible, r.guideBtnText);
    console.log('   skip    link %d · #lessonDeck %d · deck is main.slide-container %s · FOCUS MOVES %s',
      r.skip, r.deck, r.deckIsSlideContainer, focusMoved);
    console.log('   dupIds  %d of %d ids examined (%d elements in the document) %s',
      r.dupIds.length, r.idTotal, r.elementTotal, r.dupIds.join(',') || '');
    console.log('   console errors %d of %d console messages · non-file requests %d of %d requests %s',
      errors.length, consoleTotal, requests.length, requestTotal,
      JSON.stringify([...new Set(requests)]));
    // A denominator of zero is a failure, not a pass: if nothing was examined,
    // the zero above measured nothing.
    if (r.idTotal === 0 || r.elementTotal === 0 || requestTotal === 0)
      console.log('   [DENOMINATOR ZERO] ids %d · elements %d · requests %d -- this run examined nothing',
        r.idTotal, r.elementTotal, requestTotal);
    const ok = PLANT ? !r.splashInDom
      : (r.splashInDom && r.splashVisible && r.guideBtnInDom && r.guideBtnVisible
         && r.skip === 1 && r.deck === 1 && r.deckIsSlideContainer && focusMoved === true
         && r.dupIds.length === 0
         && r.idTotal > 0 && r.elementTotal > 0 && requestTotal > 0);
    console.log('   %s\n', PLANT ? (ok ? 'PLANT CONFIRMED: with the splash removed the check fails'
                                       : 'PLANT DID NOT FIRE  <-- the guard is not guarding')
                                 : (ok ? 'PASS' : 'FAIL'));
    if (!ok) bad++;
    fs.unlinkSync(tmp);
    await ctx.close();
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
