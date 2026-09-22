// STOP-R2 oracle: a REAL HTML5 parser decides whether the mark-up changed the document.
// lxml cannot be the judge here -- libxml2 does not implement HTML5's head/body inference,
// so it puts flow content inside <head> and would call an exact repair a change. Chromium
// is the parser that actually serves these pages, so Chromium is the oracle.
import pw from 'playwright';
const { chromium } = pw;
import { readFileSync, writeFileSync, mkdtempSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

const pairs = JSON.parse(readFileSync(process.argv[2], 'utf8'));  // [{id, before, after}]
const browser = await chromium.launch();
const page = await browser.newPage();
const dir = mkdtempSync(join(tmpdir(), 'r2-'));

async function dom(bytes) {
  const f = join(dir, 'p.html');
  writeFileSync(f, bytes);
  await page.goto('file://' + f, { waitUntil: 'domcontentloaded' });
  return await page.evaluate(() => {
    const d = document;
    // The browser's own normalised view: the doctype, the element tree, and where the
    // parser decided head ends and body begins.
    return JSON.stringify({
      doctype: d.doctype ? d.doctype.name : null,
      head: d.head.innerHTML,
      body: d.body.innerHTML,
      title: d.title,
      elements: d.getElementsByTagName('*').length,
    });
  });
}

const out = [];
for (const p of pairs) {
  const b = await dom(readFileSync(p.before));
  const a = await dom(readFileSync(p.after));
  out.push({ id: p.id, same: b === a,
             before: b === a ? null : b.slice(0, 300), after: b === a ? null : a.slice(0, 300) });
}
await browser.close();
console.log(JSON.stringify(out));
