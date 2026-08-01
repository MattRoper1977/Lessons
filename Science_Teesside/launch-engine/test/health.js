/* ==========================================================================
   Health check — every Science_Teesside deck, all three pathways.
   Renders each deck, walks every slide, and reports only what is actually
   broken. Findings are separated from observations: a deck that differs from
   its neighbours is not thereby faulty.
   ========================================================================== */
let chromium;
try { ({ chromium } = require('playwright-core')); }
catch (e) {
  console.error('playwright-core not installed. npm install --no-save playwright-core');
  process.exit(2);
}
const fs = require('fs'), path = require('path');
const ROOT = require('path').join(__dirname, '..', '..');
const EXEC = process.env.SCI_CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

/* /hud.js is a site-root script; it 404s under file:// in EVERY deck, injected
   or not, and always has. Not a finding. */
const IGNORE = /hud\.js|ERR_FILE_NOT_FOUND|favicon/;

(async () => {
  const browser = await chromium.launch({ executablePath: EXEC, args: ['--no-sandbox'] });
  const rows = [];

  for (const pathway of ['Build', 'Grow', 'Launch']) {
    const dir = path.join(ROOT, pathway);
    if (!fs.existsSync(dir)) continue;
    for (const file of fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort()) {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      const errs = [];
      page.on('pageerror', e => errs.push('pageerror: ' + String(e).split('\n')[0]));
      page.on('console', m => {
        if (m.type() === 'error' && !IGNORE.test(m.text())) errs.push('console: ' + m.text().slice(0, 140));
      });

      await page.goto('file://' + path.join(dir, file));
      await page.waitForTimeout(350);

      const base = await page.evaluate(() => ({
        slides: document.querySelectorAll('.slide').length,
        titles: [...document.querySelectorAll('.slide')].map(s => s.getAttribute('data-title')),
        xpTotal: (document.getElementById('xpTotal') || {}).textContent,
        sci: document.querySelectorAll('.sci').length,
        sciReport: window.SCI && window.SCI.report,
        /* grow-anim is IIFE-scoped and exposes no global — detect it by the
           block inject.py leaves behind, not by window.GROW (which is always
           undefined and made GROW look unwired when it is not). */
        grow: !!document.getElementById('grow-anim-script'),
        /* BUILD has its OWN framework (build-anim/, `ba-` prefix, BUILD-ANIM:
           marker comments). It does not use grow-anim, so it needs its own
           probe — looking for the wrong marker is what made BUILD read as
           unanimated after build-anim landed. */
        build: document.querySelectorAll('[class*="ba-"]').length > 0,
        buildNodes: document.querySelectorAll('[class*="ba-"]').length,
        /* which motion vocabulary is this deck speaking? */
        sharedMotion: document.querySelectorAll('[class*="g-draw"],[class*="g-glow"],[class*="g-pulse"],[class*="g-flow"],[class*="g-zoom"]').length,
        growParts: document.querySelectorAll('[data-part]').length,
        growLabels: document.querySelectorAll('[data-label]').length,
        growNodes: document.querySelectorAll('[data-part],[data-label],.g-draw,.g-glow,.g-pulse,.g-flow-jiggle,.g-zoom-layer').length,
        motionCSS: !!document.getElementById('grow-motion-css'),
        svgs: document.querySelectorAll('svg').length,
        printArea: !!document.getElementById('print-area'),
        /* duplicate ids break url(#…) references silently — the trap that hid
           the eyepiece clip failure */
        dupIds: (() => {
          const seen = {}, dupes = [];
          document.querySelectorAll('[id]').forEach(n => {
            seen[n.id] = (seen[n.id] || 0) + 1;
            if (seen[n.id] === 2) dupes.push(n.id);
          });
          return dupes;
        })(),
        /* an SVG reference pointing at an id that is not in the SAME svg is
           dropped by Chromium when the first match sits on a hidden slide */
        crossSvgRefs: (() => {
          const bad = [];
          document.querySelectorAll('[clip-path],[fill^="url"],[filter],[mask]').forEach(n => {
            ['clip-path', 'fill', 'filter', 'mask'].forEach(a => {
              const v = n.getAttribute(a);
              const m = v && v.match(/url\(#([^)]+)\)/);
              if (!m) return;
              const t = document.getElementById(m[1]);
              if (t && n.ownerSVGElement && t.ownerSVGElement && t.ownerSVGElement !== n.ownerSVGElement) bad.push(m[1]);
            });
          });
          return [...new Set(bad)];
        })()
      }));

      /* walk every slide: overflow and late errors only show up on the slide
         that owns the content */
      let maxOver = 0, offenders = [];
      for (let i = 0; i < base.slides; i++) {
        await page.evaluate(j => window.showSlide && window.showSlide(j), i);
        await page.waitForTimeout(110);
        const o = await page.evaluate(() =>
          document.documentElement.scrollWidth - document.documentElement.clientWidth);
        if (o > maxOver) { maxOver = o; }
        if (o > 0) offenders.push(base.titles[i] + ' +' + o + 'px');
      }

      /* narrow viewport — projectors are wide but staff review on laptops */
      await page.setViewportSize({ width: 768, height: 800 });
      await page.waitForTimeout(200);
      const over768 = await page.evaluate(() =>
        document.documentElement.scrollWidth - document.documentElement.clientWidth);

      /* PRINT — DELIBERATELY NOT AUDITED. See REGISTER R-E05.

         This slot held `return a ? getComputedStyle(a).display !== 'none' || true : true`
         — `X || true`, a tautology that passed every deck in every state.

         Replacing it with a real measurement (rendered height of #print-area
         under print media) fired on 25 decks out of 25, 24 of which were
         untouched. Cause: `.print-section{display:none}` with `.visible` added
         by `printPack(level)`, so the pack is legitimately empty until a tier
         is chosen. The assertion encoded a wrong model of the subsystem.

         R-E05 records the chain 691 -> 12 -> 4 -> 7 -> 0: five alarms, five
         retirements, zero real defects, because "a subsystem with many valid
         designs generates false positives in proportion to its variety, not
         its defect rate". This attempt reproduced that on its first run.

         So the assertion is retired rather than repaired. A tautology and an
         always-firing check are equally uninformative; the difference is that
         the second one costs somebody an afternoon. Print is audited by
         `LundyLoop/tools/print_pack_audit.py` and by a human with a printer. */

      rows.push({ pathway, file, ...base, errs, maxOver, offenders, over768 });
      await ctx.close();
    }
  }

  await browser.close();

  /* ---------------------------------------------------------------- report */
  const RED = [];
  console.log('\n═══ DECK HEALTH · Science_Teesside ═══\n');
  console.log('pathway file                              slides  svg  anim  xp   errors  overflow');
  console.log('─'.repeat(94));
  for (const r of rows) {
    const anim = r.pathway === 'Launch' ? `sci ${r.sci}`
      : r.grow ? `grow ${r.growParts}p`
      : r.build ? `build ${r.buildNodes}n`
      : 'NONE';
    const over = r.maxOver > 0 || r.over768 > 0 ? `1280:${r.maxOver} 768:${r.over768}` : 'none';
    const bad = r.errs.length || r.maxOver > 0 || r.over768 > 0 || r.dupIds.length || r.crossSvgRefs.length;
    console.log(
      `${r.pathway.padEnd(7)} ${r.file.slice(0, 34).padEnd(35)} ${String(r.slides).padStart(4)} ${String(r.svgs).padStart(4)} ` +
      `${anim.padEnd(9)} ${String(r.xpTotal || '—').padStart(3)} ${String(r.errs.length).padStart(6)}  ${over}`);
    if (bad) RED.push(r);
  }

  console.log('\n─── findings ───');
  if (!RED.length) console.log('  none — every deck renders clean');
  RED.forEach(r => {
    console.log(`\n  ${r.pathway}/${r.file}`);
    r.errs.slice(0, 4).forEach(e => console.log('    · ' + e));
    if (r.maxOver > 0) console.log('    · horizontal overflow at 1280: ' + r.offenders.join(', '));
    if (r.over768 > 0) console.log('    · horizontal overflow at 768: +' + r.over768 + 'px');
    if (r.dupIds.length) console.log('    · duplicate ids (' + r.dupIds.length + '): ' + r.dupIds.slice(0, 6).join(', '));
    if (r.crossSvgRefs.length) console.log('    · url(#) resolving to another svg: ' + r.crossSvgRefs.slice(0, 6).join(', '));
  });

  console.log('\n─── pathway summary ───');
  ['Build', 'Grow', 'Launch'].forEach(p => {
    const set = rows.filter(r => r.pathway === p);
    if (!set.length) return;
    const clean = set.filter(r => !RED.includes(r)).length;
    const animated = set.filter(r => r.pathway === 'Launch' ? r.sci > 0 : (r.grow || r.build)).length;
    const shared = set.filter(r => r.sharedMotion > 0).length;
    console.log(`  ${p.padEnd(7)} ${set.length} decks · ${clean} clean · ${animated} carrying an animation layer · ` +
      `median ${Math.round(set.map(r => r.svgs).sort((a, b) => a - b)[Math.floor(set.length / 2)])} svg per deck · ` +
      `${shared}/${set.length} speak the shared g- motion language`);
  });
  console.log('');
  process.exit(RED.length ? 1 : 0);
})();
