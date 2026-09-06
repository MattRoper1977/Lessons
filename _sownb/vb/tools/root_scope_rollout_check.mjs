// RUN12-A :root scope migration, per-deck rollout check.
//
// The full three-clause proof (root_scope_prove.mjs) runs on one deck per lane.
// Every other migrated deck gets this lighter check, which still measures the
// two things the migration could break:
//   1. every custom property resolved on the root element and on body has the
//      same computed value as the unmigrated deck (screen media, 1365);
//   2. the cold print pack prints the same text.
// The unmigrated copy is written into the SAME directory as the deck, because a
// deck's own scripts resolve relative paths against their location and a copy
// under /tmp is therefore not the same page.
//
// Usage: node root_scope_rollout_check.mjs <file-list.txt> <out.json>
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'

const [listFile, outFile] = process.argv.slice(2)
const files = fs.readFileSync(listFile, 'utf8').trim().split('\n').filter(Boolean)
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' })
const out = {}

async function probe(file, names) {
  const page = await browser.newPage({ viewport: { width: 1365, height: 768 } })
  await page.addInitScript(() => { window.print = () => {} })
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.goto('file://' + path.resolve(file))
  await page.waitForTimeout(300)
  const tokens = await page.evaluate((list) => {
    const r = getComputedStyle(document.documentElement)
    const b = getComputedStyle(document.body)
    return list.map((n) => n + '=' + r.getPropertyValue(n).trim() + '|' + b.getPropertyValue(n).trim()).join(';')
  }, names)
  await page.emulateMedia({ media: 'print' })
  const print = await page.evaluate(() =>
    Array.from(document.querySelectorAll('#print-area .print-section'))
      .filter((e) => getComputedStyle(e).display !== 'none')
      .map((e) => e.innerText).join('\n').replace(/\s+/g, ' ').trim(),
  )
  await page.close()
  return { tokens, print }
}

for (const file of files) {
  const dir = path.dirname(file)
  const before = path.join(dir, '.rsb_' + path.basename(file))
  const rec = {}
  try {
    fs.writeFileSync(before, execFileSync('git', ['show', `HEAD:${file}`], { maxBuffer: 64 * 1024 * 1024 }))
    const names = [...new Set((fs.readFileSync(file, 'utf8').match(/--[A-Za-z_][\w-]*/g) || []))].sort()
    const b = await probe(before, names)
    const a = await probe(file, names)
    rec.tokensProbed = names.length
    rec.tokensIdentical = b.tokens === a.tokens
    rec.printIdentical = b.print === a.print
    rec.printChars = a.print.length
    // The claim of THIS check is "the migration changed nothing". Whether a deck
    // prints anything at all when cold is a separate, pre-existing property (R4);
    // it is reported, never folded into this verdict.
    rec.coldPrintBlank = a.print.length === 0
    rec.status = rec.tokensIdentical && rec.printIdentical ? 'PASS' : 'RED'
    if (!rec.tokensIdentical) {
      const bs = b.tokens.split(';'), as = a.tokens.split(';')
      rec.firstTokenDiff = bs.map((x, i) => (x === as[i] ? null : [x, as[i]])).filter(Boolean).slice(0, 5)
    }
  } catch (e) {
    rec.status = 'ERR'
    rec.err = String(e).slice(0, 200)
  } finally {
    fs.rmSync(before, { force: true })
  }
  out[file] = rec
  console.log(rec.status, file, rec.tokensProbed ?? '', rec.tokensIdentical ?? '', rec.printIdentical ?? '')
}
await browser.close()
const pass = Object.values(out).filter((r) => r.status === 'PASS').length
const blank = Object.values(out).filter((r) => r.coldPrintBlank).length
fs.writeFileSync(outFile, JSON.stringify({
  file: '_sownb/vb/tools/root_scope_migrate.py',
  subject: 'RUN12-A :root scope migration rollout check: per deck, every custom property resolved on the root element and on body is unchanged and the cold print pack prints the same text; the unmigrated copy is compared from the same directory',
  decks: out, count: files.length, pass, coldPrintBlank: blank,
  coldPrintBlankNote: 'a deck that prints nothing cold has not had the R4 default-Standard fix; that is a pre-existing property of the deck, not an effect of this migration',
  status: pass === files.length ? 'PASS' : 'RED',
}, null, 1))
console.log(`\n${pass}/${files.length} PASS`)
