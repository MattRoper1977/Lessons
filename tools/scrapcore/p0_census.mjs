/* A-P0.1 — derive what the estate actually injects into a game route.
 *
 * Not from a hand-list and not from the source: the site repo is served over
 * http and every route is loaded in a real browser, and every request the page
 * makes is recorded. "The file contains a script tag" and "the page requests
 * that script" are different claims, and this one is the second.
 *
 * Writes qa/P0_estate_injection_census.json.
 */
import fs from 'node:fs'; import path from 'node:path'; import http from 'node:http';
const _pw = await import(process.env.SC_PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright/index.js')
  .catch(() => import('playwright'));
const chromium = _pw.chromium || _pw.default.chromium;
const ROOT = process.env.SC_ROOT || path.dirname(new URL(import.meta.url).pathname);
const SITE = process.env.MBM_SITE || '/workspace/mattroper1977.github.io';

/* ---- the route set, DERIVED from the same record the estate's own gate uses */
const index = JSON.parse(fs.readFileSync(path.join(SITE, 'data', 'mbm-search-index.json'), 'utf8'));
const ROOT_ROUTE = /^\/[a-z0-9-]+\/$/;
const routes = [...new Set(index.entries.filter(e => e.category === 'game' && ROOT_ROUTE.test(e.route || ''))
  .map(e => e.route))].sort();
const coverage = JSON.parse(fs.readFileSync(path.join(SITE, 'data', 'hud-coverage.json'), 'utf8'));
const excluded = new Set((coverage.excluded || []).map(e => e.route));

/* ---- a static server over the real repo, so absolute paths resolve --------- */
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css',
               '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml',
               '.webp': 'image/webp', '.ico': 'image/x-icon', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel.endsWith('/')) rel += 'index.html';
  const file = path.join(SITE, rel);
  if (!file.startsWith(SITE) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.writeHead(404); res.end('not found'); return;
  }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const BASE = `http://127.0.0.1:${server.address().port}`;

const browser = await chromium.launch();
const census = { _what: 'every same-origin subresource each root game route actually REQUESTS in a browser, not what its source mentions',
                 _base: BASE, _routes: routes.length, _measuredAt: null, routes: {} };
for (const route of routes) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const pg = await ctx.newPage();
  const reqs = [], violations = [], errs = [];
  pg.on('request', r => { const u = new URL(r.url()); if (u.origin === BASE) reqs.push({ path: u.pathname, type: r.resourceType() }); });
  pg.on('requestfailed', r => { const u = new URL(r.url()); if (u.origin === BASE) reqs.push({ path: u.pathname, type: r.resourceType(), failed: r.failure() && r.failure().errorText }); });
  pg.on('pageerror', e => errs.push(String(e).slice(0, 120)));
  await pg.addInitScript(() => {
    window.__csp = [];
    document.addEventListener('securitypolicyviolation', e => window.__csp.push({ directive: e.violatedDirective, blocked: e.blockedURI }));
  });
  await pg.goto(BASE + route, { waitUntil: 'load', timeout: 45000 }).catch(e => errs.push('goto: ' + String(e).slice(0, 90)));
  await pg.waitForTimeout(1600);
  const csp = await pg.evaluate(() => window.__csp || []).catch(() => []);
  const hasOwnCsp = await pg.evaluate(() => !!document.querySelector('meta[http-equiv="Content-Security-Policy"]')).catch(() => null);
  const hudRan = await pg.evaluate(() => typeof window.__mbmExit !== 'undefined' || !!document.querySelector('[data-mbm-hud],.mbm-hud,#mbm-hud')).catch(() => null);
  await ctx.close();
  const sub = reqs.filter(r => r.path !== route && r.path !== route + 'index.html');
  census.routes[route] = {
    excluded: excluded.has(route),
    subresources: sub,
    subresourcePaths: [...new Set(sub.map(r => r.path))],
    shipsOwnCSP: hasOwnCsp,
    cspViolations: csp,
    pageErrors: errs,
    exitAffordanceMounted: hudRan,
  };
}
await browser.close();
server.close();

/* ---- the summary that decides P0.2 --------------------------------------- */
const all = Object.entries(census.routes);
const withSubs = all.filter(([, v]) => v.subresourcePaths.length);
const byPath = {};
for (const [r, v] of all) for (const p of v.subresourcePaths) (byPath[p] = byPath[p] || []).push(r);
census.summary = {
  routesMeasured: all.length,
  excludedFromHud: all.filter(([, v]) => v.excluded).map(([r]) => r),
  routesRequestingAnySameOriginSubresource: withSubs.map(([r]) => r),
  subresourceToRoutes: byPath,
  routesShippingTheirOwnCSP: all.filter(([, v]) => v.shipsOwnCSP).map(([r]) => r),
  routesWithCSPViolations: all.filter(([, v]) => v.cspViolations.length).map(([r, v]) => ({ route: r, violations: v.cspViolations })),
};
fs.mkdirSync(path.join(ROOT, 'qa'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'qa', 'P0_estate_injection_census.json'), JSON.stringify(census, null, 2));

console.log(`routes measured: ${all.length}   (derived from data/mbm-search-index.json, category=game, root-level)`);
console.log(`declared unable to carry the HUD (data/hud-coverage.json): ${census.summary.excludedFromHud.length}`);
console.log(`routes shipping their own CSP meta: ${census.summary.routesShippingTheirOwnCSP.length ? census.summary.routesShippingTheirOwnCSP.join(', ') : 'NONE'}`);
console.log('\nsame-origin subresource -> the routes that actually request it:');
for (const [p, rs] of Object.entries(byPath).sort((a, b) => b[1].length - a[1].length))
  console.log(`  ${p.padEnd(28)} ${rs.length}/${all.length}  ${rs.join(' ')}`);
console.log(`\nroutes requesting NOTHING same-origin: ${all.length - withSubs.length}`);
console.log(`  ${all.filter(([, v]) => !v.subresourcePaths.length).map(([r]) => r).join(' ')}`);
console.log(`\nqa/P0_estate_injection_census.json written`);
