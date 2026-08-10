#!/usr/bin/env node
import fs from 'node:fs';
import { chromium } from 'playwright';

const BASE = process.env.GLV3_BASE_URL || 'http://127.0.0.1:8123';
const resources = JSON.parse(fs.readFileSync('resources.json','utf8'));
const newResources = resources.filter(x => String(x.id || '').startsWith('glv3-'));
if (newResources.length !== 88) throw new Error(`expected 88 GLV3 resources, got ${newResources.length}`);
const chips = [...new Set(newResources.map(x => x.subject))].sort();

const browser = await chromium.launch({headless:true});
const page = await browser.newPage({viewport:{width:1440,height:900}});
const report = {};
for (const chip of chips) {
  await page.goto(BASE + '/index.html', {waitUntil:'networkidle'});
  const collection = page.locator('button.collection', {hasText:'2026-27'});
  if (await collection.count() !== 1) throw new Error(`2026-27 collection button count=${await collection.count()}`);
  await collection.click();
  await page.waitForTimeout(50);
  const button = page.locator('button.chip', {hasText:chip});
  if (await button.count() !== 1) throw new Error(`${chip}: chip button count=${await button.count()}`);
  const label = (await button.innerText()).replace(/\s+/g,' ').trim();
  const nums = [...label.matchAll(/(\d[\d,]*)/g)].map(m => Number(m[1].replaceAll(',','')));
  if (!nums.length) throw new Error(`${chip}: advertised count missing from chip label "${label}"`);
  const advertised = nums.at(-1);
  await button.click();
  await page.waitForTimeout(50);
  const returned = await page.evaluate(() =>
    [...document.querySelectorAll('.resource-item')].filter(el => getComputedStyle(el).display !== 'none').length
  );
  const expected = resources.filter(x => x.subject === chip && x.year === '2026-27').length;
  if (advertised !== returned || returned !== expected) {
    throw new Error(`${chip}: advertised=${advertised} returned=${returned} expected=${expected}`);
  }
  report[chip] = {advertised, returned, expected};
}
await browser.close();
fs.writeFileSync('_glv3/GATES_CHIPS.json', JSON.stringify(report,null,2)+'\n');
fs.appendFileSync('_glv3/REPORT.md',
  '\n## Chip-count browser gate\n\n' +
  Object.entries(report).map(([k,v]) => `- ${k}: advertised ${v.advertised} = returned ${v.returned} (active 2026-27).`).join('\n') + '\n');
fs.appendFileSync('_glv3/DECISIONS.md',
  '\n## Chip-count browser gate\n\n' +
  Object.entries(report).map(([k,v]) => `- ${k}: advertised ${v.advertised} = returned ${v.returned} in active 2026-27.`).join('\n') + '\n');
console.log(JSON.stringify(report,null,2));
