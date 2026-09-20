#!/usr/bin/env python3
"""ORDER HUM-T, STOP-T3 ruling Q2 (Matt Roper, 2026-09-20) — re-stamp the David cover
pack's route pins to the transplanted bytes of a SIGNED batch.

tools/humanities_resources/SOURCE_MANIFEST.json pins 30 existing lesson routes by digest
("existing_routes"), and check_resources.py asserts each against the working tree through
the GLV3 boundary gate. Nothing derives that manifest, so a transplanted route was red with
no remedy. The ruling:

    The David cover pack manifest may be re-stamped by a tool that derives every digest
    from the transplanted bytes, with the stated basis "re-stamped to HUM-T transplanted
    bytes under Matt's STOP-SIGN per batch; original review basis unchanged", refusing
    any route outside the signed batch. Manifest pinned afterwards.

So this tool:
  * reads the batch's declared GLV3 replacement transaction from
    _glv3/tools/verify_change_boundary.py (the signed batch IS that declaration);
  * for every existing route named in that transaction, derives the digest from the bytes
    on disk and requires it to EQUAL the transaction's afterSha256 — the transplanted bytes
    the batch declared, nothing else;
  * refuses a route outside the batch, a route whose bytes differ from the declaration, and
    a batch with no declaration;
  * rewrites ONLY the sha256 of a matching route and records the basis beside it, per route.

The manifest is a REVIEWED_PATHS member, so the pin writer carries its new digest into both
gate copies afterwards.

  restamp_cover_routes.py --batch "HUM-T batch 2 GROW" [--write]
  restamp_cover_routes.py --self-test
"""
from __future__ import annotations
import argparse, ast, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'tools/humanities_resources/SOURCE_MANIFEST.json'
BOUNDARY = ROOT / '_glv3/tools/verify_change_boundary.py'
BASIS = ("re-stamped to HUM-T transplanted bytes under Matt's STOP-SIGN per batch; "
         "original review basis unchanged")


class Refuse(Exception):
    pass


def slug(name):
    return re.sub(r'[^A-Z0-9]+', '_', name.upper()).strip('_')


def declared_batch(name, source=None):
    text = source if source is not None else BOUNDARY.read_text()
    m = re.search(r'^%s_REPLACEMENTS = (\{.*?\})\n' % re.escape(slug(name)), text, re.S | re.M)
    if not m:
        raise Refuse('no declared replacement transaction for batch %r' % name)
    return ast.literal_eval(m.group(1))


def plan(routes, batch, digest_of):
    """Pure: (restamps, refusals, noops) for the manifest's routes against a declared batch.

    `routes` is the list of existing_routes dicts; `batch` maps path -> {afterSha256};
    `digest_of(path)` reads the tree."""
    restamps, refused, noops = [], [], []
    for r in routes:
        rel = r['path']
        if rel not in batch:
            continue  # untouched: outside this batch, this run has nothing to say about it
        actual = digest_of(rel)
        if actual is None:
            refused.append((rel, 'route is not a regular file in the tree')); continue
        if actual != batch[rel]['afterSha256']:
            refused.append((rel, 'bytes on disk %s differ from the declared transplanted bytes %s'
                            % (actual[:12], batch[rel]['afterSha256'][:12]))); continue
        if actual == r['sha256']:
            noops.append(rel); continue
        restamps.append((rel, r['sha256'], actual))
    return restamps, refused, noops


def self_test():
    bad = 0
    def check(name, cond):
        nonlocal bad
        print('  [%s] %s' % ('ok' if cond else 'FAIL', name)); bad += 0 if cond else 1
    routes = [{'path': 'H/a.html', 'sha256': 'a' * 64}, {'path': 'H/b.html', 'sha256': 'b' * 64},
              {'path': 'H/c.html', 'sha256': 'c' * 64}]
    batch = {'H/a.html': {'afterSha256': '1' * 64}, 'H/c.html': {'afterSha256': 'c' * 64}}
    tree = {'H/a.html': '1' * 64, 'H/b.html': '2' * 64, 'H/c.html': 'c' * 64}
    rs, rf, no = plan(routes, batch, tree.get)
    check('a route in the signed batch whose bytes equal the declared transplant is re-stamped',
          rs == [('H/a.html', 'a' * 64, '1' * 64)])
    check('a route outside the batch is never touched, even though its bytes moved',
          all(x[0] != 'H/b.html' for x in rs) and all(x[0] != 'H/b.html' for x in rf))
    check('a route already at the declared bytes is a no-op', no == ['H/c.html'])
    rs, rf, no = plan(routes, {'H/a.html': {'afterSha256': '9' * 64}}, tree.get)
    check('bytes that differ from the declared transplant are refused', rf and 'differ from the declared' in rf[0][1] and not rs)
    rs, rf, no = plan(routes, {'H/a.html': {'afterSha256': '1' * 64}}, lambda p: None)
    check('a route missing from the tree is refused', rf and 'not a regular file' in rf[0][1])
    try:
        declared_batch('HUM-T batch 99 NOPE', source='X = 1\n'); check('a batch with no declaration is refused', False)
    except Refuse as x:
        check('a batch with no declaration is refused', 'no declared replacement transaction' in str(x))
    src = "HUM_T_BATCH_1_BUILD_REPLACEMENTS = {'H/a.html': {'beforeGitBlob': 'x', 'afterSha256': '1'}}\n"
    check("the declaration is read from the boundary file by the batch's slug", declared_batch('HUM-T batch 1 BUILD', source=src) == {'H/a.html': {'beforeGitBlob': 'x', 'afterSha256': '1'}})
    print('self-test ' + ('PASS' if not bad else 'FAIL (%d)' % bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--batch'); ap.add_argument('--write', action='store_true'); ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.batch:
        ap.error('--batch is required unless --self-test')
    try:
        batch = declared_batch(a.batch)
    except Refuse as x:
        print('[FAIL] ' + str(x)); return 1
    doc = json.loads(MANIFEST.read_text())
    routes = [r for rec in doc['records'] for r in rec['existing_routes']]
    def digest_of(rel):
        p = ROOT / rel
        return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() and not p.is_symlink() else None
    rs, rf, no = plan(routes, batch, digest_of)
    print('SEARCH SCOPE: %d existing routes in %s; batch %r declares %d member(s); %d in both'
          % (len(routes), MANIFEST.relative_to(ROOT), a.batch, len(batch), len(rs) + len(rf) + len(no)))
    for rel, why in rf: print('  REFUSED %s: %s' % (rel, why))
    for rel in no: print('  NO-OP   %s already at the declared bytes' % rel)
    for rel, old, new in rs: print('  RESTAMP %s\n      %s\n   -> %s' % (rel, old, new))
    if rf:
        print('[FAIL] %d refusal(s); nothing written' % len(rf)); return 1
    if a.write and rs:
        moved = {rel: new for rel, _o, new in rs}
        for rec in doc['records']:
            for r in rec['existing_routes']:
                if r['path'] in moved:
                    r['sha256'] = moved[r['path']]
                    r['restamp'] = {'basis': BASIS, 'batch': a.batch, 'by': 'tools/hum/restamp_cover_routes.py'}
        MANIFEST.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
        print('[DONE] %d route(s) re-stamped; run the pin writer so both gate copies carry the manifest\'s new digest' % len(rs))
    return 0


if __name__ == '__main__':
    sys.exit(main())
