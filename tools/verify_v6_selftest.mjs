#!/usr/bin/env node
/* The V6 release self-test, run in a browser, for every game that declares one.
 *
 * WHY THIS FILE EXISTS. data/hud-coverage.json excluded five games from the HUD
 * requirement and cited their verifier as the prose string
 *   "window.__MBM_V6_RELEASE__.selfTest plus Games rendered regression".
 * verify_hud_on_lessons_games.mjs resolves a cited verifier by fs.existsSync, so
 * a sentence is not a verifier: the exclusion cited a check that could not be
 * found, and the daily cross-estate run went red on it.
 *
 * The rule the estate applies here is "never delete a coverage row" - so rather
 * than rewriting the citation to something that already existed and quietly
 * dropping the self-test half, the missing half is REGISTERED. The games really
 * do carry window.__MBM_V6_RELEASE__.selfTest; nothing ran it. Now something
 * does, and the exclusions cite two files that exist:
 *   tools/verify_v6_selftest.mjs     this file
 *   tools/verify_games_rendered.mjs  the rendered regression
 *
 * WHAT IT MEASURES. Each declaring game is served and loaded, selfTest() is
 * called and recorded; the verdict is then taken at ROUTE scope (see below). Originally:
 * called, and its own per-check map is read. A game that reports ok:false fails
 * with the failing check named. A game that declares the object but whose
 * selfTest throws, returns nothing, or reports ok as anything but a boolean is a
 * failure too, not a pass by omission.
 *
 * NON-VACUITY. --self-test asserts this file can fail: it stubs the release
 * object on a real page so selfTest reports ok:false and requires the run to go
 * red. A checker that has never been seen to fail has measured nothing.
 *
 * Usage:
 *   node tools/verify_v6_selftest.mjs [--only <substring>] [--json <out>]
 *   node tools/verify_v6_selftest.mjs --self-test
 */
import { chromium } from 'playwright'
import http from 'node:http'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const argv = process.argv.slice(2)
const arg = (n) => (argv.includes(n) ? argv[argv.indexOf(n) + 1] : null)
const ONLY = arg('--only')
const OUT = arg('--json')
const SELFTEST = argv.includes('--self-test')
const NAV_MS = 30000
const CALL_MS = 15000

/* ROUTE SCOPE (ORDER VB-RUN15 H14-1, RULE_CHOICE=b). The offline/standalone check inside
 * each game is a FILE rule; data/hud-coverage.json now carries the same rule at ROUTE
 * scope (routeScope): a hud-wired route may carry exactly the HUD script line, a
 * single-file route may carry nothing, and link[rel=canonical] is metadata, not a
 * request. Each game's own selfTest still runs and its file-level result is recorded
 * unchanged; what reds this run is the route-scope verdict. A control plants a
 * non-permitted external on a real page and requires the route-scope verdict to fail. */
const LEDGER = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'hud-coverage.json'), 'utf8'))
const ROUTE_SCOPE = LEDGER.routeScope
const EXCLUDED = new Set((LEDGER.excluded || []).map((e) => e.route))
const SCOPE_CHECKS = new Set(['offline', 'standalone'])
const routeClass = (file) => (EXCLUDED.has(`/Lessons/Games/${file}`) ? 'single-file' : 'hud-wired')
const games = fs.readdirSync(path.join(ROOT, 'Games'))
  .filter((f) => f.endsWith('.html') || !f.includes('.'))
  .filter((f) => {
    const p = path.join(ROOT, 'Games', f)
    return fs.statSync(p).isFile() && fs.readFileSync(p, 'utf8').includes('__MBM_V6_RELEASE__')
  })
  .filter((f) => !ONLY || f.includes(ONLY))
  .sort()

const serve = () => new Promise((resolve) => {
  const server = http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split('?')[0])
    if (p.startsWith('/Lessons/')) p = p.slice('/Lessons'.length)
    const f = path.join(ROOT, p)
    if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('not found') }
    const ext = path.extname(f)
    res.writeHead(200, { 'content-type': ext === '.html' || ext === '' ? 'text/html; charset=utf-8'
      : ext === '.js' ? 'text/javascript' : ext === '.css' ? 'text/css' : 'application/octet-stream' })
    res.end(fs.readFileSync(f))
  })
  server.listen(0, () => resolve({ server, port: server.address().port }))
})

const run = async (browser, port, file, stub, plantExternal) => {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } })
  const row = { game: `Games/${file}` }
  try {
    if (stub) {
      await page.addInitScript(() => {
        Object.defineProperty(window, '__MBM_V6_RELEASE__', {
          configurable: true,
          get: () => ({ selfTest: () => ({ ok: false, pass: false, checks: { planted: false } }) }),
        })
      })
    }
    if (plantExternal) {
      await page.addInitScript(() => {
        document.addEventListener('DOMContentLoaded', () => {
          const s = document.createElement('script'); s.src = '/planted-not-permitted.js'; document.head.appendChild(s)
        })
      })
    }
    await page.goto(`http://127.0.0.1:${port}/Lessons/Games/${encodeURIComponent(file)}`,
      { waitUntil: 'domcontentloaded', timeout: NAV_MS })
    await page.waitForFunction(() => !!window.__MBM_V6_RELEASE__, { timeout: CALL_MS })
    const r = await page.evaluate(() => {
      const rel = window.__MBM_V6_RELEASE__
      if (!rel || typeof rel.selfTest !== 'function') return { declared: !!rel, callable: false }
      try { return { declared: true, callable: true, result: rel.selfTest() } }
      catch (e) { return { declared: true, callable: true, threw: String(e).slice(0, 200) } }
    })
    Object.assign(row, r)
    const res = r.result
    row.ok = r.callable && res && typeof res.ok === 'boolean' && res.ok === true
    row.failingChecks = res && res.checks
      ? Object.entries(res.checks).filter(([, v]) => !v).map(([k]) => k) : []
    row.gameId = res && res.gameId
    row.version = res && res.version
    // route scope: the page's real external elements, judged against the route's class
    const ext = await page.evaluate(() => Array.from(document.querySelectorAll('script[src],link[href],img[src],audio[src],video[src],source[src]')).map((el) => ({
      tag: el.tagName.toLowerCase(), rel: el.getAttribute('rel') || '', src: el.getAttribute('src') || el.getAttribute('href') || '', outer: el.outerHTML.slice(0, 120) })))
    const cls = routeClass(file)
    const permitted = new Set((ROUTE_SCOPE.classes[cls].permittedExternal || []))
    const metadata = (e) => e.tag === 'link' && e.rel.split(/\s+/).includes('canonical')
    const permittedLine = (e) => e.tag === 'script' && permitted.has(`<script defer src="${e.src}"></script>`)
    // a data: URI, a fragment or a javascript: href is not a request; a root-relative or
    // network URL is. (The games' own filter counts only network URLs, which is why the
    // canonical link and nothing else fails them at file scope.)
    const isRequest = (e) => !/^(data:|#|javascript:|$)/i.test(e.src.trim())
    const real = ext.filter((e) => isRequest(e) && !metadata(e) && !permittedLine(e))
    row.routeClass = cls
    row.externals = ext.map((e) => e.outer)
    row.realExternals = real.map((e) => e.outer)
    row.fileScopeOk = row.ok
    const nonScopeFailing = row.failingChecks.filter((k) => !SCOPE_CHECKS.has(k))
    row.routeScopeOk = r.callable && res && typeof res.ok === 'boolean' && nonScopeFailing.length === 0 && real.length === 0
    row.routeScopeFailing = [...nonScopeFailing, ...(real.length ? ['route-scope: non-permitted external'] : [])]
  } catch (e) {
    row.ok = false
    row.error = String(e).slice(0, 200)
  } finally { await page.close() }
  return row
}

const { server, port } = await serve()
const browser = await chromium.launch({ executablePath: process.env.MBM_CHROMIUM_PATH || undefined })
let exit = 0

if (SELFTEST) {
  const probe = games[0]
  const real = await run(browser, port, probe, false)
  const planted = await run(browser, port, probe, true)
  const plantedExt = await run(browser, port, probe, false, true)
  const ok = real.routeScopeOk === true && planted.routeScopeOk === false && plantedExt.routeScopeOk === false && plantedExt.realExternals.length === 1
  console.log(`  real page        file=${real.fileScopeOk} route=${real.routeScopeOk} class=${real.routeClass}`)
  console.log(`  planted failure  route=${planted.routeScopeOk}  failing=${JSON.stringify(planted.routeScopeFailing)}`)
  console.log(`  planted external route=${plantedExt.routeScopeOk}  real=${JSON.stringify(plantedExt.realExternals)}`)
  console.log(ok ? '[SELF-TEST] PASS — this checker can fail' : '[SELF-TEST] FAIL — it cannot be made to fail')
  exit = ok ? 0 : 1
} else {
  const rows = []
  for (const g of games) rows.push(await run(browser, port, g, false))
  for (const r of rows) {
    console.log(`  ${r.routeScopeOk ? 'PASS' : 'FAIL'}  ${r.game}  [${r.routeClass}] file-scope=${r.fileScopeOk ? 'pass' : 'FAIL ' + JSON.stringify(r.failingChecks)}` +
      (r.routeScopeOk ? '' : `  ${r.error || JSON.stringify(r.routeScopeFailing)}`))
  }
  const failed = rows.filter((r) => !r.routeScopeOk)
  const fileFailed = rows.filter((r) => !r.fileScopeOk)
  console.log(`\n${rows.length - failed.length}/${rows.length} games pass at route scope; ${rows.length - fileFailed.length}/${rows.length} pass their own file-level self-test`)
  if (OUT) fs.writeFileSync(path.join(ROOT, OUT), JSON.stringify({
    file: 'tools/verify_v6_selftest.mjs',
    subject: 'the V6 release self-test run in a browser on every game that declares one',
    games: rows, passed: rows.length - failed.length, total: rows.length, passedFileScope: rows.length - fileFailed.length, scope: 'route (data/hud-coverage.json routeScope); file-level results recorded per game',
    status: failed.length ? 'RED' : 'PASS',
  }, null, 1) + '\n')
  exit = failed.length ? 1 : 0
}

await browser.close(); server.close()
process.exit(exit)
