#!/usr/bin/env node
import fs from 'node:fs';
import { chromium } from 'playwright';
import { expectedSubjectRows, verifySubjectCards, catalogueMembershipControls } from './catalogue_membership.mjs';

catalogueMembershipControls();

const BASE = process.env.GLV3_BASE_URL || process.argv[2] || 'http://127.0.0.1:8123';
const resources = JSON.parse(fs.readFileSync('resources.json', 'utf8'));
const order = JSON.parse(fs.readFileSync('assets/catalogue/lesson-order.json', 'utf8'));
const newResources = resources.filter(x => String(x.id || '').startsWith('glv3-'));
if (newResources.length !== 88) {
  throw new Error(`expected 88 GLV3 resources, got ${newResources.length}`);
}

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

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
const report = {};

try {
  for (const chip of chips) {
    // UX2 Part A (Lessons #437) retired the hub's year tabs and #quicknav subject
    // chips: every year now renders, and a subject is reached by the subject card
    // or the ?subject= query, which resolves to the hub's flat results. The gate's
    // content is unchanged — advertised == returned == derived from the record, and
    // every GLV3 entry for the subject reachable — measured on the surface that
    // carries it. Dropping the year clause is not a widening: the results view
    // shows every year, so the derivation must too, and the GLV3 rows it must
    // still find are all 2026-27.
    await page.goto(BASE + '/index.html?subject=' + encodeURIComponent(chip), { waitUntil: 'networkidle' });
    await page.waitForFunction(() => /\d+ of \d+ resources/.test(document.querySelector('#count')?.textContent || ''));

    const label = ((await page.locator('#count').innerText()) || '').replace(/\s+/g, ' ').trim();
    const advertisedMatch = label.match(/^(\d+) of \d+ resources/);
    if (!advertisedMatch) {
      throw new Error(`${chip}: advertised count missing from the results line "${label}"`);
    }
    const advertised = Number(advertisedMatch[1]);

    const cards = await page.evaluate(() => [...document.querySelectorAll('#cards .card')].map(el => ({
      path: el.getAttribute('data-resource-path') || '',
      href: el.querySelector('h3 a[href]')?.getAttribute('href') || '',
      text: (el.textContent || '').replace(/\s+/g, ' ').trim(),
    })));

    const returned = cards.length;
    const expectedRows = expectedSubjectRows(resources, order, chip);
    const expected = expectedRows.length;
    verifySubjectCards({subject: chip, expected: expectedRows, advertised, cards, base: BASE});
    const wantedNew = newResources.filter(x => x.subject === chip);

    report[chip] = {
      advertised,
      returned,
      expected,
      glv3_entries: wantedNew.length,
      glv3_reachable: wantedNew.length,
    };
  }
} finally {
  await browser.close();
}

fs.writeFileSync('_glv3/GATES_CHIPS.json', JSON.stringify(report, null, 2) + '\n');
fs.appendFileSync(
  '_glv3/REPORT.md',
  '\n## Chip-count browser gate\n\n' +
  Object.entries(report)
    .map(([key, value]) =>
      `- ${key}: advertised ${value.advertised} = returned ${value.returned} = JSON-derived ${value.expected}; ` +
      `${value.glv3_reachable}/${value.glv3_entries} new GLV3 entries reachable in the subject's results.`
    )
    .join('\n') + '\n'
);
fs.appendFileSync(
  '_glv3/DECISIONS.md',
  '\n## Chip-count browser gate\n\n' +
  Object.entries(report)
    .map(([key, value]) =>
      `- ${key}: advertised ${value.advertised} = returned ${value.returned} = JSON-derived ${value.expected} ` +
      `in the subject's results; all ${value.glv3_entries} GLV3 additions for the subject are reachable.`
    )
    .join('\n') + '\n'
);

console.log(JSON.stringify(report, null, 2));
