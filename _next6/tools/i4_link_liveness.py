#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORDER N6-I · I4 — first liveness measurement of the packs' external citations.

Order TS D3: a URL is not dead on one reading. Two measurements at least an hour
apart are required, and only a URL dead in BOTH is ledgered for removal. This
tool takes ONE timestamped measurement and writes it as an artifact; it never
proposes a removal.

It also distinguishes the two things a zero can mean, which is the whole reason
a second reading exists:

  * a per-host failure — some URLs answer, this one does not: a candidate dead link;
  * a uniform failure across every host, with the local egress proxy answering 403
    to CONNECT — an infrastructure signature, not thirty simultaneously dead
    citations. The tool says which it saw and refuses to call the second case
    a liveness result.

Usage: i4_link_liveness.py <pack_root> [<pack_root>...] --out <artifact.json>
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse

URL_RX = re.compile(r'https?://[^\s"\'<>)\]}]+')
# Hosts the environment allowlists for package installs. They are reachable here
# and are NOT citations, so they are excluded from the citation set — but they
# are probed separately as a CONTROL, which is what makes an all-zero citation
# result interpretable rather than ambiguous.
CONTROL_URLS = ['https://pypi.org/simple/', 'https://registry.npmjs.org/']


def urls_in(roots):
    found = {}
    for root in roots:
        for dirpath, _dirs, names in os.walk(root):
            for n in names:
                if not n.lower().endswith(('.html', '.md', '.json', '.csv', '.txt')):
                    continue
                p = os.path.join(dirpath, n)
                try:
                    s = open(p, encoding='utf-8', errors='replace').read()
                except OSError:
                    continue
                for m in URL_RX.finditer(s):
                    u = m.group(0).rstrip('.,;:')
                    u = u.replace('&amp;', '&')
                    found.setdefault(u, []).append(p)
    return found


def probe(url, timeout=20):
    """One HEAD-then-GET reading. Returns (code, note)."""
    for args in (['-I'], ['-r', '0-0']):
        try:
            r = subprocess.run(
                ['curl', '-sS', '-o', '/dev/null', '-L', '--max-time', str(timeout),
                 '-w', '%{http_code}'] + args + [url],
                capture_output=True, text=True, timeout=timeout + 10)
            code = (r.stdout or '').strip()[-3:]
            if code.isdigit() and code != '000':
                return int(code), (r.stderr or '').strip()[:200]
            last = (r.stderr or '').strip()[:200]
        except subprocess.TimeoutExpired:
            last = 'client timeout'
    return 0, last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('roots', nargs='+')
    ap.add_argument('--out', required=True)
    ap.add_argument('--stamp', required=True,
                    help='ISO-8601 UTC timestamp for this reading, supplied by the caller')
    ap.add_argument('--timeout', type=int, default=20)
    a = ap.parse_args()

    found = urls_in(a.roots)
    citations = sorted(u for u in found
                       if urllib.parse.urlsplit(u).hostname
                       and not urllib.parse.urlsplit(u).hostname.endswith(
                           ('pypi.org', 'npmjs.org', 'pythonhosted.org', 'jsr.io')))

    controls = []
    for c in CONTROL_URLS:
        code, note = probe(c, a.timeout)
        controls.append({'url': c, 'code': code, 'note': note})

    readings = []
    for u in citations:
        code, note = probe(u, a.timeout)
        readings.append({'url': u, 'code': code, 'note': note,
                         'host': urllib.parse.urlsplit(u).hostname,
                         'carriers': sorted(set(found[u]))})
        print('%-4s %s' % (code or 'ERR', u))

    live = [r for r in readings if 200 <= r['code'] < 400]
    reachable_control = [c for c in controls if 200 <= c['code'] < 400]
    all_zero = readings and all(r['code'] == 0 for r in readings)

    if all_zero and reachable_control:
        verdict = ('MEASUREMENT INVALID — every citation host returned 000 while the '
                   'allowlisted control hosts answered. That is an egress policy '
                   'signature, not %d simultaneously dead links. No reading is '
                   'recorded and nothing is proposed for removal.' % len(readings))
        valid = False
    elif all_zero:
        verdict = ('MEASUREMENT INVALID — every host returned 000 including the '
                   'controls. There is no network here.')
        valid = False
    else:
        verdict = ('reading 1 of 2 — %d/%d answered. Order TS D3 requires a second '
                   'reading at least an hour later; only a URL dead in BOTH is '
                   'ledgered for removal.' % (len(live), len(readings)))
        valid = True

    art = {'order': 'N6-I · I4', 'reading': 1, 'takenAtUTC': a.stamp,
           'roots': a.roots, 'uniqueCitationUrls': len(readings),
           'controls': controls, 'valid': valid, 'verdict': verdict,
           'readings': readings}
    json.dump(art, open(a.out, 'w'), indent=1)
    print()
    print(verdict)
    print('artifact -> %s' % a.out)
    return 0 if valid else 3


if __name__ == '__main__':
    sys.exit(main())
