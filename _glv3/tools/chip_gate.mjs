#!/usr/bin/env node
import fs from 'node:fs';
import { chromium } from 'playwright';

const BASE = process.env.GLV3_BASE_URL || 'http://127.0.0.1:8123';
const resources = JSON.parse(fs.readFileSync('resources.json', 'utf8'));
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
    await page.goto(BASE + '/index.html', { waitUntil: 'networkidle' });
    await page.waitForSelector('.ytab[data-year="2026-27"]');

    const collection = page.locator('.ytab[data-year="2026-27"]');
    if (await collection.count() !== 1) {
      throw new Error(`2026-27 year tab count=${await collection.count()}`);
    }
    await collection.click();
    await page.waitForTimeout(80);

    const activeYear = await page.locator('.ytab[aria-pressed="true"]').getAttribute('data-year');
    if (activeYear !== '2026-27') {
      throw new Error(`2026-27 year tab did not become active: ${activeYear}`);
    }

    await page.waitForSelector('#quicknav .chip');
    const button = page.locator('#quicknav .chip').filter({ hasText: chip });
    if (await button.count() !== 1) {
      throw new Error(`${chip}: current chip count=${await button.count()}`);
    }

    const cls = (await button.getAttribute('class')) || '';
    if (cls.split(/\s+/).includes('lib')) {
      throw new Error(`${chip}: chip is outside the active collection`);
    }

    const label = ((await button.innerText()) || '').replace(/\s+/g, ' ').trim();
    const advertisedMatch = label.match(/\((\d+)\)\s*$/);
    if (!advertisedMatch) {
      throw new Error(`${chip}: advertised count missing from chip label "${label}"`);
    }
    const advertised = Number(advertisedMatch[1]);

    await button.click();
    await page.waitForTimeout(120);
    const cards = await page.evaluate(() => [...document.querySelectorAll('#cards article.card')].map(el => {
      const anchor = el.querySelector('a[href]');
      return {
        href: anchor?.getAttribute('href') || '',
        text: (el.textContent || '').replace(/\s+/g, ' ').trim(),
      };
    }));

    const returned = cards.length;
    const expected = resources.filter(x => x.subject === chip && x.year === '2026-27').length;
    if (advertised !== returned || returned !== expected) {
      throw new Error(`${chip}: advertised=${advertised} returned=${returned} expected=${expected}`);
    }

    const hrefs = cards.map(x => decodeURIComponent(x.href.split('#')[0].split('?')[0]));
    const wantedNew = newResources.filter(x => x.subject === chip && x.year === '2026-27');
    const missing = wantedNew.filter(resource =>
      !hrefs.some(href => href.endsWith(resource.file)) &&
      !cards.some(card => card.text.includes(resource.title))
    );
    if (missing.length) {
      throw new Error(
        `${chip}: ${missing.length}/${wantedNew.length} GLV3 entries are not reachable: ` +
        missing.slice(0, 6).map(x => x.file).join(', ')
      );
    }

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
      `${value.glv3_reachable}/${value.glv3_entries} new GLV3 entries reachable in active 2026-27.`
    )
    .join('\n') + '\n'
);
fs.appendFileSync(
  '_glv3/DECISIONS.md',
  '\n## Chip-count browser gate\n\n' +
  Object.entries(report)
    .map(([key, value]) =>
      `- ${key}: advertised ${value.advertised} = returned ${value.returned} = JSON-derived ${value.expected} ` +
      `in active 2026-27; all ${value.glv3_entries} GLV3 additions on the chip are reachable.`
    )
    .join('\n') + '\n'
);

console.log(JSON.stringify(report, null, 2));
