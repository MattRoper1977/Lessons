/* ============================================================================
   BUILD Animation Framework — asset preview harness
   ---------------------------------------------------------------------------
   Renders assets from the library in a real browser and writes a PNG, so an
   asset can be LOOKED AT rather than guessed at. Use it while authoring: draw,
   render, look, fix. A shape that reads fine in source often reads as a smudge
   on a classroom projector.

     node build-anim/tools/preview.mjs --out /tmp/arm.png
     node build-anim/tools/preview.mjs --assets arm,armmodel --out /tmp/arm.png
     node build-anim/tools/preview.mjs --assets plate --script teach --step 3 --out /tmp/p.png
     node build-anim/tools/preview.mjs --assets arm --dark --cols 1 --out /tmp/d.png

   --assets  comma list, or omitted for every registered asset
   --script  which script to run (default: teach), --step N stops part way
   --cols    grid columns (default 3), --dark render on a dark ground
   --json    print the asset manifest instead of rendering
   Exit code is 1 if the page threw, so a broken asset fails loudly.
   ========================================================================== */
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function arg(name, dflt) {
  const i = process.argv.indexOf('--' + name);
  if (i < 0) return dflt;
  const v = process.argv[i + 1];
  return (v === undefined || v.startsWith('--')) ? true : v;
}

const libs = ['bio-svg.js', 'body-svg.js', 'food-svg.js', 'chain-svg.js']
  .filter(f => fs.existsSync(path.join(DIR, f)));
const read = f => fs.readFileSync(path.join(DIR, f), 'utf8');

const dark = !!arg('dark', false);
const cols = parseInt(arg('cols', '3'), 10) || 3;
const only = arg('assets', '');
const script = arg('script', 'teach');
const step = arg('step', '');
const out = arg('out', '/tmp/preview.png');

const page_html = `<!doctype html><html><head><meta charset="utf-8"><style>
*,*::before,*::after{box-sizing:border-box}
body{margin:0;padding:14px;font-family:system-ui,sans-serif;
     background:${dark ? '#15181C' : '#F6F7F9'};color:${dark ? '#E8EAED' : '#1B1F24'}}
.grid{display:grid;gap:14px;grid-template-columns:repeat(${cols},1fr)}
.cell{background:${dark ? '#1D2126' : '#fff'};border:1px solid ${dark ? '#31373E' : '#dbe0e6'};
      border-radius:12px;padding:8px 10px}
.cell h3{margin:2px 0 4px;font-size:.9rem}
.cell h3 em{font-style:normal;font-weight:500;opacity:.6;font-size:.78rem}
.err{color:#dc2626;font-weight:700;font-size:.8rem}
${read('build-anim.css')}
${dark ? '.ba-stage{background:#1D2126;border-color:#31373E}.ba-bar{display:none}' : '.ba-bar{display:none}'}
</style></head><body>
<div class="grid" id="g"></div>
<script>${libs.map(read).join('\n;\n')}</script>
<script>${read('build-anim.js')}</script>
<script>
window.__names = ${JSON.stringify(String(only) === 'true' || !only ? null : String(only).split(',').map(s => s.trim()).filter(Boolean))};
window.__script = ${JSON.stringify(String(script))};
(function(){
  var names = window.__names || BioSVG.list();
  document.getElementById('g').innerHTML = names.map(function(n){
    var a = BioSVG.asset(n);
    if(!a) return '<div class="cell"><h3>'+n+'</h3><p class="err">NOT REGISTERED</p></div>';
    var sc = a[window.__script] ? '@'+window.__script : (a.teach ? '@teach' : '');
    return '<div class="cell"><h3>'+(a.title||n)+' <em>'+n+(a.kind?' · '+a.kind:'')+'</em></h3>'+
      '<div class="ba-stage" data-ba-asset="'+n+'" data-ba-script="'+sc+'"></div></div>';
  }).join('');
  BuildAnim.init(document.getElementById('g'));
})();
</script></body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: Math.min(1800, 430 * cols + 40), height: 1000 }, deviceScaleFactor: 2 });
const errs = [];
page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
page.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });
await page.setContent(page_html, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(400);

if (arg('json', false)) {
  const man = await page.evaluate((s) => BioSVG.list().map(n => {
    const a = BioSVG.asset(n);
    const el = document.createElement('div');
    el.innerHTML = BioSVG.render(n);
    return {
      name: n, title: a.title, kind: a.kind || null,
      parts: [...new Set([...el.querySelectorAll('[data-part]')].map(e => e.dataset.part))],
      labels: [...new Set([...el.querySelectorAll('[data-label]')].map(e => e.dataset.label))],
      scripts: Object.keys(a).filter(k => typeof a[k] === 'string' && a[k].includes('::'))
    };
  }), script);
  console.log(JSON.stringify(man, null, 1));
} else {
  const n = await page.evaluate((st) => {
    const stages = [...document.querySelectorAll('.ba-stage')];
    stages.forEach(s => { if (st) { for (let i = 0; i < +st; i++) BuildAnim.next(s); } else BuildAnim.all(s); });
    return stages.length;
  }, step === '' || step === true ? null : step);
  await page.waitForTimeout(2600);
  const grid = await page.$('#g');
  await grid.screenshot({ path: out });
  console.log(`rendered ${n} asset(s) -> ${out}`);
}

if (errs.length) { console.error(errs.join('\n')); await browser.close(); process.exit(1); }
await browser.close();
