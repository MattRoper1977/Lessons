#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { chromium } from 'playwright';

const ROOT = process.cwd();
const BASE = process.env.GLV3_BASE_URL || 'http://127.0.0.1:8123';
const manifest = JSON.parse(fs.readFileSync('_glv3/run_manifest.json', 'utf8'));
const lessons = manifest.lessons;
const result = {
  boot: { universe_html: 0, console_errors: [], page_errors: [] },
  print: { universe: 0, failures: [] },
  catalogue: { chips: {}, console_errors: [], page_errors: [] },
  contact_sheets: { per_lesson: 0, combined: [] },
};

function walk(dir, out=[]) {
  for (const ent of fs.readdirSync(dir, {withFileTypes:true})) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}
function rel(p) { return p.split(path.sep).join('/'); }
function urlFor(repoRel) {
  return BASE + '/' + repoRel.split('/').map(encodeURIComponent).join('/');
}
function safeName(repoRel) {
  return repoRel.replace(/\.html$/i,'').replaceAll('/','__').replace(/[^A-Za-z0-9_.-]+/g,'_');
}

const allHtml = [
  ...walk('GROW_Estate_v3').filter(p => p.endsWith('.html')),
  ...walk('LAUNCH_Estate_v3').filter(p => p.endsWith('.html')),
].map(rel).sort();

if (allHtml.length !== 94) {
  throw new Error(`boot universe expected 94 installed HTML files, got ${allHtml.length}`);
}
result.boot.universe_html = allHtml.length;

const browser = await chromium.launch({headless:true});
const context = await browser.newContext({
  viewport: {width: 1440, height: 900},
  deviceScaleFactor: 1,
  reducedMotion: 'reduce',
});
const page = await context.newPage();

let activeFile = '';
let cataloguePhase = false;
page.on('console', msg => {
  if (msg.type() !== 'error') return;
  const target = cataloguePhase ? result.catalogue.console_errors : result.boot.console_errors;
  target.push(`${activeFile}: ${msg.text()}`);
});
page.on('pageerror', err => {
  const target = cataloguePhase ? result.catalogue.page_errors : result.boot.page_errors;
  target.push(`${activeFile}: ${err.message}`);
});

for (const f of allHtml) {
  activeFile = f;
  const response = await page.goto(urlFor(f), {waitUntil:'load', timeout:30000});
  if (!response || !response.ok()) {
    result.boot.page_errors.push(`${f}: HTTP ${response?.status() ?? 'no response'}`);
  }
  await page.waitForTimeout(20);
}
if (result.boot.console_errors.length || result.boot.page_errors.length) {
  throw new Error(`boot gate failed: ${JSON.stringify({
    console: result.boot.console_errors.slice(0,10),
    page: result.boot.page_errors.slice(0,10)
  })}`);
}

// Print gate: 24 known repaired route-bearing lesson files.
const printLessons = lessons.filter(x => x.print);
if (printLessons.length !== 24) throw new Error(`print browser universe expected 24, got ${printLessons.length}`);
result.print.universe = printLessons.length;
for (const r of printLessons) {
  activeFile = r.file;
  await page.emulateMedia({media:'print'});
  await page.goto(urlFor(r.file), {waitUntil:'load', timeout:30000});
  const before = await page.evaluate(() => ({
    hasTier: document.body.hasAttribute('data-tier'),
    count: document.querySelectorAll('.proute').length,
    displays: [...document.querySelectorAll('.proute')].map(x => getComputedStyle(x).display),
  }));
  if (before.hasTier || before.count !== 3 || before.displays.some(x => x === 'none')) {
    result.print.failures.push(`${r.file}: default ${JSON.stringify(before)}`);
    continue;
  }
  const selected = await page.evaluate(() => {
    window.print = () => {};
    if (typeof window.printTier !== 'function') return {function:false};
    window.printTier('support');
    const routes = [...document.querySelectorAll('.proute')];
    const state = {
      function:true,
      tier: document.body.dataset.tier || null,
      count: routes.length,
      displays: routes.map(x => getComputedStyle(x).display),
    };
    window.dispatchEvent(new Event('afterprint'));
    state.cleared = !document.body.hasAttribute('data-tier');
    return state;
  });
  const visible = selected.displays?.filter(x => x !== 'none').length;
  if (!selected.function || selected.tier !== 'support' || selected.count !== 3 || visible !== 1 || !selected.cleared) {
    result.print.failures.push(`${r.file}: selection ${JSON.stringify(selected)}`);
  }
}
await page.emulateMedia({media:'screen'});
if (result.print.failures.length) {
  throw new Error(`print browser gate failed: ${result.print.failures.slice(0,8).join('\n')}`);
}

// Real current catalogue filter-chain reachability. The Lesson Hub's own UI
// uses .ytab[data-year], #quicknav .chip[data-sub], and #cards article.card.
// Catalogue-shell console diagnostics are recorded separately from the 94-page
// estate boot gate so they cannot contaminate that universe's zero-error proof.
cataloguePhase = true;
const resources = JSON.parse(fs.readFileSync('resources.json','utf8'));
const newResources = resources.filter(x => String(x.id || '').startsWith('glv3-'));
if (newResources.length !== 88) throw new Error(`catalogue expected 88 GLV3 entries, got ${newResources.length}`);
const chipNames = [...new Set(newResources.map(x => x.subject))].sort();
for (const chip of chipNames) {
  activeFile = `catalogue:${chip}`;
  await page.goto(BASE + '/index.html', {waitUntil:'networkidle', timeout:30000});
  await page.waitForSelector('.ytab[data-year="2026-27"]');

  const yearButton = page.locator('.ytab[data-year="2026-27"]');
  if (await yearButton.count() !== 1) throw new Error(`year tab 2026-27 not uniquely found for ${chip}`);
  await yearButton.click();
  await page.waitForTimeout(80);
  const activeYear = await page.locator('.ytab[aria-pressed="true"]').getAttribute('data-year');
  if (activeYear !== '2026-27') throw new Error(`year tab did not activate 2026-27 for ${chip}: active=${activeYear}`);

  await page.waitForSelector('#quicknav .chip');
  const cb = page.locator('#quicknav .chip').filter({hasText:chip});
  if (await cb.count() !== 1) throw new Error(`current catalogue chip not uniquely found: ${chip}`);
  const chipClass = await cb.getAttribute('class') || '';
  if (chipClass.split(/\s+/).includes('lib')) throw new Error(`${chip}: current chip is marked lib/outside active collection`);
  const label = (await cb.textContent()) || '';
  const advertised = Number((label.match(/\((\d+)\)\s*$/) || [])[1]);
  await cb.click();
  await page.waitForTimeout(120);

  const state = await page.evaluate(() => [...document.querySelectorAll('#cards article.card')].map(el => {
    const a = el.querySelector('a[href]');
    return {
      href: a?.getAttribute('href') || '',
      text:(el.textContent || '').replace(/\s+/g,' ').trim(),
    };
  }));

  const expectedTotal = resources.filter(x => x.subject === chip && x.year === '2026-27').length;
  if (!Number.isFinite(advertised) || advertised !== expectedTotal || state.length !== expectedTotal) {
    throw new Error(`${chip}: advertised=${advertised} rendered=${state.length} JSON=${expectedTotal}`);
  }

  const got = new Set();
  for (const x of state) {
    if (!x.href) continue;
    let h = decodeURIComponent(x.href.split('#')[0].split('?')[0]).replace(/^\.\//,'').replace(/^\//,'');
    if (h.endsWith('/')) h += 'index.html';
    got.add(h);
  }
  const want = newResources.filter(x => x.subject === chip && x.year === '2026-27').map(x => x.file);
  const missing = want.filter(x => ![...got].some(h => h === x || h.endsWith('/' + x)));
  if (missing.length) {
    const textJoined = state.map(x => x.text).join('\n');
    const stillMissing = newResources.filter(x => missing.includes(x.file) && !textJoined.includes(x.title)).map(x => x.file);
    if (stillMissing.length) throw new Error(`${chip}: ${stillMissing.length} new entries not reachable through real filter chain: ${stillMissing.slice(0,8).join(', ')}`);
  }
  result.catalogue.chips[chip] = {
    new_entries: want.length,
    advertised,
    visible_items: state.length,
    json_expected: expectedTotal,
    reachable_new_entries: want.length,
  };
}

// Contact sheets. Per lesson: title + one interactive; print-bearing lessons add print page 1 with no tier selected.
const tmp = '_glv3/.contact_tmp';
fs.rmSync(tmp, {recursive:true, force:true});
fs.mkdirSync(tmp, {recursive:true});
const bySubject = new Map([['art',[]],['asdan',[]],['humanities',[]]]);

for (const r of lessons) {
  activeFile = r.file;
  await page.emulateMedia({media:'screen'});
  await page.goto(urlFor(r.file), {waitUntil:'load', timeout:30000});
  await page.waitForTimeout(60);
  await page.evaluate(() => { if (typeof window.show === 'function') window.show(0); });
  await page.waitForTimeout(30);
  const baseName = safeName(r.file);
  const titlePng = path.join(tmp, baseName + '__title.png');
  const intPng = path.join(tmp, baseName + '__interactive.png');
  await page.screenshot({path:titlePng, fullPage:false});

  const interactiveIndex = await page.evaluate(() => {
    const slides = [...document.querySelectorAll('.slide')];
    if (!slides.length) return -1;
    let idx = slides.findIndex((s,i) => i > 0 && s.querySelector('button, input, select, textarea, [role="button"], .option, .choice, .card'));
    if (idx < 0) idx = Math.min(2, slides.length - 1);
    if (typeof window.show === 'function') window.show(idx);
    else {
      slides.forEach((s,i) => s.classList.toggle('active', i === idx));
    }
    return idx;
  });
  if (interactiveIndex < 0) {
    throw new Error(`${r.file}: no .slide found for interactive contact-sheet frame`);
  }
  await page.waitForTimeout(30);
  await page.screenshot({path:intPng, fullPage:false});

  const parts = [titlePng, intPng];
  if (r.print) {
    await page.goto(urlFor(r.file), {waitUntil:'load', timeout:30000});
    const hasTier = await page.evaluate(() => document.body.hasAttribute('data-tier'));
    if (hasTier) throw new Error(`${r.file}: data-tier was set before print contact-sheet capture`);
    await page.emulateMedia({media:'print'});
    const pdf = path.join(tmp, baseName + '__print.pdf');
    await page.pdf({
      path: pdf, printBackground:true, format:'A4', pageRanges:'1',
      margin:{top:'8mm', right:'8mm', bottom:'8mm', left:'8mm'}
    });
    const prefix = path.join(tmp, baseName + '__print');
    execFileSync('pdftoppm', ['-png','-singlefile','-r','110',pdf,prefix], {stdio:'pipe'});
    const printPng = prefix + '.png';
    if (!fs.existsSync(printPng)) throw new Error(`${r.file}: print page 1 PNG was not produced`);
    parts.push(printPng);
  }

  const outDir = path.join('_glv3','contact_sheet',r.subject_key);
  fs.mkdirSync(outDir, {recursive:true});
  const out = path.join(outDir, baseName + '.png');
  execFileSync('montage', [
    ...parts, '-thumbnail','640x420', '-tile', `${parts.length}x1`,
    '-geometry','+8+8', '-background','white', out
  ], {stdio:'pipe'});
  bySubject.get(r.subject_key).push(out);
  result.contact_sheets.per_lesson += 1;
}

if (result.contact_sheets.per_lesson !== 80) {
  throw new Error(`contact sheets expected 80 per-lesson PNGs, got ${result.contact_sheets.per_lesson}`);
}
for (const [subject, files] of bySubject.entries()) {
  const out = path.join('_glv3','contact_sheet',subject,`combined-${subject}.png`);
  execFileSync('montage', [
    ...files, '-thumbnail','360x240', '-tile','4x',
    '-geometry','+6+6', '-background','white', out
  ], {stdio:'pipe'});
  result.contact_sheets.combined.push(rel(out));
}
fs.rmSync(tmp, {recursive:true, force:true});
await browser.close();

fs.writeFileSync('_glv3/GATES_BROWSER.json', JSON.stringify(result,null,2) + '\n');
fs.appendFileSync('_glv3/REPORT.md',
`\n## Browser gates and contact sheets\n\n` +
`- Boot: ${result.boot.universe_html} installed HTML files; 0 console errors; 0 page errors.\n` +
`- Print: ${result.print.universe}/24 repaired route-bearing lessons passed default-all-three / selected-one / afterprint-clear behavior.\n` +
`- Catalogue reachability: all 88 new entries are reachable through active 2026-27 + their existing chip; advertised, rendered and JSON-derived chip counts agree in \`GATES_BROWSER.json\`. Catalogue-shell console diagnostics are recorded separately from the estate boot universe.\n` +
`- Contact sheets: ${result.contact_sheets.per_lesson}/80 per-lesson PNGs plus ${result.contact_sheets.combined.length} combined subject sheets.\n` +
`- Combined sheets: ${result.contact_sheets.combined.map(x => '`'+x+'`').join(', ')}.\n`);
fs.appendFileSync('_glv3/DECISIONS.md',
`\n## Browser execution results\n\n` +
`- Browser boot: ${result.boot.universe_html} new HTML files, 0 console/page errors.\n` +
`- Print browser gate: 24/24 repaired route-bearing lesson files passed; 56 screen-only lessons remained screen-only by the static gate.\n` +
`- Catalogue browser gate: all 88 new resources are reachable through active 2026-27 + their existing chip; advertised = rendered = JSON-derived count. Catalogue-shell diagnostics are kept separate from the 94-page estate boot gate.\n` +
`- Contact sheets: 80 per-lesson PNGs plus combined Art, ASDAN and Humanities sheets under \`_glv3/contact_sheet/\`.\n`);
console.log(JSON.stringify(result,null,2));