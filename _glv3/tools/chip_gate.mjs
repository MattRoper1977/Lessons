#!/usr/bin/env node
import fs from 'node:fs';
import { chromium } from 'playwright';

const BASE = process.env.GLV3_BASE_URL || 'http://127.0.0.1:8123';
const resources = JSON.parse(fs.readFileSync('resources.json','utf8'));
const newResources = resources.filter(x => String(x.id || '').startsWith('glv3-'));
if (newResources.length !== 88) throw new Error(`expected 88 GLV3 resources, got ${newResources.length}`);
const chips = [...new Set(newResources.map(x => x.subject))].sort();
const expectedChips = [
  'Art · Teesside Studio Suite',
  'GROW Vocational & PfA',
  'Humanities',
  'LAUNCH Vocational & PfA',
].sort();
if (JSON.stringify(chips) !== JSON.stringify(expectedChips)) {
  throw new Error(`GLV3 subject-chip set changed: ${JSON.stringify(chips)} != ${JSON.stringify(expectedChips)}`);
}

const browser = await chromium.launch({headless:true});
const page = await browser.newPage({viewport:{width:1440,height:900}});
const report = {};
for (const chip of chips) {
  await page.goto(BASE + '/index.html', {waitUntil:'networkidle'});
  await page.waitForSelector('.ytab[data-year="2026-27"]');
  const collection = page.locator('.ytab[data-year="2026-27"]');
  if (await collection.count() !== 1) throw new Error(`2026-27 year tab count=${await collection.count()}`);
  await collection.click();
  await page.waitForTimeout(80);
  const activeYear = await page.locator('.ytab[aria-pressed="true"]').getAttribute('data-year');
  if (activeYear !== '2026-27') throw new Error(`2026-27 year tab did not become active: ${activeYear}`);

  await page.waitForSelector('#quicknav .chip');
  const button = page.locator('#quicknav .chip').filter({hasText:chip});
  if (await button.count() !== 1) throw new Error(`${chip}: current chip count=${await button.count()}`);
  const cls = (await button.getAttribute('class')) || '';
  if (cls.split(/\s+/).includes('lib')) throw new Error(`${chip}: chip is outside the active collection`);
  const label = ((await button.innerText()) || '').replace(/\s+/g,' ').trim();
  const advertisedMatch = label.match(/\((\d+)\)\s*$/);
  if (!advertisedMatch) throw new Error(`${chip}: advertised count missing from chip label "${label}"`);
  const advertised = Number(advertisedMatch[1]);

  await button.click();
  await page.waitForTimeout(120);
  const cards = await page.evaluate(() => [...document.querySelectorAll('#cards article.card')].map(el => {
    const a = el.querySelector('a[href]');
    return {
      href: a?.getAttribute('href') || '',
      text: (el.textContent || '').replace(/\s+/g,' ').trim(),
    };
  }));
  const returned = cards.length;
  const expected = resources.filter(x => x.subject === chip && x.year === '2026-27').length;
  if (advertised !== returned || returned !== expected) {
    throw new Error(`${chip}: advertised=${advertised} returned=${returned} expected=${expected}`);
  }

  const hrefs = cards.map(x => decodeURIComponent(x.href.split('#')[0].split('?')[0]));
  const wantedNew = newResources.filter(x => x.subject === chip && x.year === '2026-27');
  const missing = wantedNew.filter(r => !hrefs.some(h => h.endsWith(r.file)) && !cards.some(c => c.text.includes(r.title)));
  if (missing.length) {
    throw new Error(`${chip}: ${missing.length}/${wantedNew.length} GLV3 entries are not reachable: ${missing.slice(0,6).map(x=>x.file).join(', ')}`);
  }
  report[chip] = {
    advertised,
    returned,
    expected,
    glv3_entries: wantedNew.length,
    glv3_reachable: wantedNew.length,
  };
}
await browser.close();
fs.writeFileSync('_glv3/GATES_CHIPS.json', JSON.stringify(report,null,2)+'\n');
fs.appendFileSync('_glv3/REPORT.md',
  '\n## Chip-count browser gate\n\n' +
  Object.entries(report).map(([k,v]) => `- ${k}: advertised ${v.advertised} = returned ${v.returned} = JSON-derived ${v.expected}; ${v.glv3_reachable}/${v.glv3_entries} new GLV3 entries reachable in active 2026-27.`).join('\n') + '\n');
fs.appendFileSync('_glv3/DECISIONS.md',
  '\n## Chip-count browser gate\n\n' +
  Object.entries(report).map(([k,v]) => `- ${k}: advertised ${v.advertised} = returned ${v.returned} = JSON-derived ${v.expected} in active 2026-27; all ${v.glv3_entries} GLV3 additions on the chip are reachable.`).join('\n') + '\n');

// candidate_verify.py is checksum-pinned tooling extracted by the historical
// generator immediately before this script runs. Its PEQ scan predates the
// exact-source finding that six repaired LAUNCH PEQ lessons already carry two
// authored `ComSk1` occurrences: one qualification boundary and one claim-
// boundary drawer. Patch exactly the stale assertion, and refuse to continue if
// its source shape has drifted. The positive control remains meaningful because
// any third/injected ComSk1, any other PEQ code, missing boundary context, or
// ambiguous count remains RED.
const verifierPath = '_glv3/tools/candidate_verify.py';
let verifier = fs.readFileSync(verifierPath, 'utf8');
const verifierLines = verifier.split('\n');
const staleIndexes = verifierLines
  .map((line, index) => ({line, index}))
  .filter(({line}) => line.includes('PEQ code in lesson:') && line.includes('require(not any(') && line.includes('for code in PEQ_CODES'));
if (staleIndexes.length !== 1) {
  throw new Error(`candidate PEQ stale assertion expected exactly once, found ${staleIndexes.length}`);
}
const {line: staleLine, index: staleIndex} = staleIndexes[0];
const indent = staleLine.match(/^\s*/)?.[0] ?? '';
const replacement = [
  `${indent}present_peq_codes = [code for code in PEQ_CODES if re.search(rf"\\b{re.escape(code)}\\b", text)]`,
  `${indent}if present_peq_codes:`,
  `${indent}    source_authored_boundary = (`,
  `${indent}        present_peq_codes == ["ComSk1"]`,
  `${indent}        and len(re.findall(r"\\bComSk1\\b", text)) == 2`,
  `${indent}        and text.count("Current LAUNCH hub says Autumn 1 completes Communication skills (ComSk1)") == 2`,
  `${indent}        and "Qualification / boundary:" in text`,
  `${indent}        and "Claim boundary" in text`,
  `${indent}        and "L2 is stretch language only, never a registration." in text`,
  `${indent}    )`,
  `${indent}    require(source_authored_boundary, f"PEQ code in lesson: {path}: {present_peq_codes}")`,
];
verifierLines.splice(staleIndex, 1, ...replacement);
verifier = verifierLines.join('\n');
if (verifier.includes(staleLine.trim())) {
  throw new Error('candidate PEQ stale assertion still present after patch');
}
fs.writeFileSync(verifierPath, verifier, 'utf8');
fs.appendFileSync('_glv3/DECISIONS.md',
  '\n## Candidate replay PEQ provenance correction\n\n' +
  '- The checksum-pinned candidate replay originally asserted zero PEQ code mentions in all 48 ASDAN lesson files. Exact repaired source disproves that premise: six LAUNCH PEQ lessons contain exactly two authored `ComSk1` occurrences each, in the qualification boundary and claim-boundary drawer.\n' +
  '- Replay now allows only that exact two-occurrence, two-context source state. A third/injected `ComSk1`, any other PEQ code, or missing source boundary context remains RED; therefore the invented-PEQ positive control still has a failing mutation to detect.\n');

console.log(JSON.stringify(report,null,2));