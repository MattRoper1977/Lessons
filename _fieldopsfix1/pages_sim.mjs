#!/usr/bin/env node
// Reproduce the owner's phone-check against a server that behaves the way GitHub
// Pages does: a directory URL serves <dir>/index.html if it exists, else 404.
// No directory listing — that absence is the entire defect.
import http from 'http'; import fs from 'fs'; import path from 'path'; import { execSync } from 'child_process';
const ROOT = process.argv[2];                 // tree to serve
const LABEL = process.argv[3] || ROOT;
const srv = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  let fsp = path.join(ROOT, p);
  if (p.endsWith('/')) {
    const idx = path.join(fsp, 'index.html');
    if (fs.existsSync(idx) && fs.statSync(idx).isFile()) fsp = idx;
    else { res.writeHead(404); return res.end('404'); }   // Pages: no listing
  }
  if (!fs.existsSync(fsp) || !fs.statSync(fsp).isFile()) { res.writeHead(404); return res.end('404'); }
  res.writeHead(200, { 'content-type': fsp.endsWith('.html') ? 'text/html; charset=utf-8' : 'text/plain' });
  res.end(fs.readFileSync(fsp));
});
await new Promise(r => srv.listen(0, r));
const port = srv.address().port;
const get = async u => { const r = await fetch(`http://127.0.0.1:${port}${u}`); return { s: r.status, b: r.status === 200 ? await r.text() : '' }; };

const CASES = [
  ['/Science_Teesside/Build/v4_fieldops/',                                    'the bare directory URL the owner hit'],
  ['/Science_Teesside/Build/v4_fieldops/01_Newport_Bridge_Lift_Permit_Lab.html','one lab direct'],
  ['/Science_Teesside/Build/v3_40min/',                                        'sibling app-index directory (known-good reference)'],
  ['/Science_Teesside/Build/',                                                 'CONTROL: a directory with no index.html — must stay 404'],
];
console.log(`--- serving ${LABEL}`);
for (const [u, why] of CASES) {
  const r = await get(u);
  let extra = '';
  if (r.s === 200) { const m = r.b.match(/<title>([^<]*)<\/title>/); extra = m ? ` title=${JSON.stringify(m[1])}` : ' (no title)'; }
  console.log(`  ${String(r.s).padEnd(4)} ${u}${extra}   # ${why}`);
}
srv.close();
