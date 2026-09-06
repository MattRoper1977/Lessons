// RUN12-A :root scope migration proof, per deck, before vs after.
//
// Clause 1  every custom property resolved on the ROOT element has the same
//           computed value before and after, at 390 and 1365 and under print
//           media. This is the whole point: the values move selector, not value.
// Clause 2  the screen is unchanged: same visible element identities, same
//           count, no element moved more than 3px (reduced motion emulated).
// Clause 3  the print pack is unchanged: for the cold state and each of the
//           three tier routes, the printed text is byte-identical.
//
// Usage: node root_scope_prove.mjs <before.html> <after.html> <outPrefix>
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs'
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'

const [before, after, out] = process.argv.slice(2)
const abs = (p) => 'file://' + path.resolve(p)
const sha = (s) => crypto.createHash('sha256').update(s).digest('hex').slice(0, 16)
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' })

// Every custom property NAME the file declares anywhere, read off the source so
// the probe cannot miss one the CSSOM hides.
const names = (file) => [...new Set((fs.readFileSync(file, 'utf8').match(/--[A-Za-z_][\w-]*/g) || []))].sort()
const ALL = [...new Set([...names(before), ...names(after)])]

async function tokens(file, width, media) {
  const page = await browser.newPage({ viewport: { width, height: width < 500 ? 844 : 768 } })
  await page.emulateMedia({ reducedMotion: 'reduce', media })
  await page.goto(abs(file))
  await page.waitForTimeout(350)
  const values = await page.evaluate((list) => {
    const root = getComputedStyle(document.documentElement)
    const body = getComputedStyle(document.body)
    const out = {}
    for (const n of list) out[n] = [root.getPropertyValue(n).trim(), body.getPropertyValue(n).trim()]
    return out
  }, ALL)
  await page.close()
  return values
}

async function screen(file, width) {
  const page = await browser.newPage({ viewport: { width, height: width < 500 ? 844 : 768 } })
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.goto(abs(file))
  await page.waitForTimeout(500)
  const fp = await page.evaluate(() => {
    const els = Array.from(document.querySelectorAll('body *')).filter((e) => {
      const r = e.getBoundingClientRect()
      const cs = getComputedStyle(e)
      return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden' && r.top < innerHeight
    })
    return {
      count: els.length,
      ident: els.map((e) => e.tagName + (e.id ? '#' + e.id : '') + '.' + (typeof e.className === 'string' ? e.className.split(' ').slice(0, 2).join('.') : '')).join(','),
      pos: els.map((e) => [Math.round(e.getBoundingClientRect().top), Math.round(e.getBoundingClientRect().left)]),
      colours: els.slice(0, 200).map((e) => getComputedStyle(e).backgroundColor + '|' + getComputedStyle(e).color + '|' + getComputedStyle(e).borderTopColor).join(','),
    }
  })
  await page.screenshot({ path: `${out}_${path.basename(file, '.html').slice(0, 24)}_${width}.png` })
  await page.close()
  return fp
}

async function printText(file, arm) {
  const page = await browser.newPage({ viewport: { width: 1365, height: 800 } })
  await page.addInitScript(() => { window.print = () => {} })
  await page.goto(abs(file))
  await page.waitForTimeout(250)
  if (arm) await page.evaluate(`printPack('${arm}')`)
  await page.emulateMedia({ media: 'print' })
  const text = await page.evaluate(() =>
    Array.from(document.querySelectorAll('#print-area .print-section'))
      .filter((e) => getComputedStyle(e).display !== 'none')
      .map((e) => e.innerText)
      .join('\n')
      .replace(/\s+/g, ' ')
      .trim(),
  )
  await page.close()
  return text
}

const rec = { file: after, before, subject: 'RUN12-A :root scope migration proof: root-element token values, screen and print pack all unchanged', clauses: {}, detail: {} }

// clause 1
const tokenDiffs = []
for (const [width, media] of [[390, 'screen'], [1365, 'screen'], [1365, 'print']]) {
  const b = await tokens(before, width, media)
  const a = await tokens(after, width, media)
  for (const n of ALL) {
    const [br, bb] = b[n] || ['', '']
    const [ar, ab] = a[n] || ['', '']
    if (br !== ar || bb !== ab) tokenDiffs.push({ token: n, width, media, before: [br, bb], after: [ar, ab] })
  }
}
rec.detail.tokensProbed = ALL.length
rec.detail.tokenDiffs = tokenDiffs.slice(0, 20)
rec.clauses.rootTokensIdentical = tokenDiffs.length === 0

// clause 2
rec.detail.screen = {}
let screenOk = true
for (const w of [390, 1365]) {
  const b = await screen(before, w)
  const a = await screen(after, w)
  const shift = Math.max(0, ...b.pos.map((p, i) => (a.pos[i] ? Math.max(Math.abs(p[0] - a.pos[i][0]), Math.abs(p[1] - a.pos[i][1])) : 999)))
  const ok = b.count === a.count && sha(b.ident) === sha(a.ident) && sha(b.colours) === sha(a.colours) && shift <= 3
  rec.detail.screen[w] = { count: [b.count, a.count], identSha: [sha(b.ident), sha(a.ident)], colourSha: [sha(b.colours), sha(a.colours)], maxShiftPx: shift, ok }
  screenOk = screenOk && ok
}
rec.clauses.screenUnchanged = screenOk

// clause 3
rec.detail.print = {}
let printOk = true
for (const arm of [null, 'supported', 'standard', 'stretch']) {
  const b = await printText(before, arm)
  const a = await printText(after, arm)
  const ok = b === a
  rec.detail.print[arm || 'cold'] = { chars: [b.length, a.length], sha: [sha(b), sha(a)], ok }
  printOk = printOk && ok
}
rec.clauses.printIdentical = printOk

await browser.close()
rec.status = rec.clauses.rootTokensIdentical && rec.clauses.screenUnchanged && rec.clauses.printIdentical ? 'PASS' : 'RED'
fs.writeFileSync(`${out}_rootscope.json`, JSON.stringify(rec, null, 1))
console.log(rec.status, 'tokens', ALL.length, 'diffs', tokenDiffs.length, '| screen', JSON.stringify(Object.fromEntries(Object.entries(rec.detail.screen).map(([k, v]) => [k, v.ok]))), '| print', printOk)
