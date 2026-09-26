#!/usr/bin/env python3
"""DLG-1 (ruling LAND-A2 R5 §2): give a control the same audience as the dialog it opens.

A dialog tagged data-mbm-guide="staff" does not show while the staff guide is off. Its button did,
so pressing it opened an invisible modal and froze the lesson. The ruled fix copies the dialog's own
audience attributes (data-audience, data-mbm-guide: exactly the values the dialog carries, no others)
onto the opening tag of the control that opens it, so with the guide off neither shows and with it on
both do. Nothing else in the file changes.

The pairs are not guessed. check_dialog_audience.cjs --json measures, in Chromium, which visible
control opened which hidden dialog on which page; this tool reads that and edits exactly those
controls, found by the attribute the probe recorded (data-action="…").

THE PAIRS RECORD (ruling LAND-A2 R8 §1-§2). The probe JSON is hundreds of KB of measurement; what
the fix needs from it is one row per control: page, data-action, dialog. tools/hum/DLG1_PAIRS.json
is that record, derived from the probe by --write-record and carrying its provenance: the probe
command, the Lessons commit it ran on, and the sha256 of the full probe JSON. A page held out by
ruling is named there with its dates and has no pair. The GLV3 DLG-1 limb
(tools/hum/admit_transaction.py) reads the record and calls fix_text() below on the BASE bytes, so
"the bytes on disk equal this tool applied to the base bytes" is judged by the code that wrote them.

Refuses, and writes nothing, when:
  - the dialog carries no audience attribute (nothing to copy: the defect is something else)
  - the control's attribute matches no <button> tag outside <script>, or a match sits inside <script>
  - a matched tag already carries a different audience
  - one tag would be edited for two dialogs

  fix_dialog_audience.py --root DIR (--probe dlg.json | --pairs tools/hum/DLG1_PAIRS.json) [--apply] [--recut]
  fix_dialog_audience.py --probe dlg.json --write-record OUT --provenance PROV.json [--check]

--recut re-cuts, for every recorded page, the digest of the row that names it in each pack manifest
listing it (SHA256SUMS.txt / CHECKSUMS.sha256 in the page's folder or any ancestor, and the named
JSON manifests below). Only that row's digest changes: row set, row order, every other digest --
even one already stale -- and every other byte stay as they were (R8 §2 "manifests may re-cut
digests only"; R8 §5 for the Fallback pack's MANIFEST.json).
Idempotent: a tag that already carries the dialog's audience is counted as done and left alone.
"""
import argparse, hashlib, json, re, sys
from pathlib import Path

AUD = ('data-audience', 'data-mbm-guide')
RECORD_SCHEMA = 'dlg1-pairs/1'
SUMS_NAMES = ('SHA256SUMS.txt', 'CHECKSUMS.sha256')
# A JSON manifest is named, with the folder its keys are relative to, never found by pattern.
JSON_MANIFESTS = {
    'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/MANIFEST.json':
        'Humanities_Teesside/Teaching_Packs/',
}
HEX64 = re.compile(r'[0-9a-f]{64}')
_SUMS_ROW = re.compile(r'^(?P<digest>[0-9a-f]{64})(?P<rest>  (?P<name>[^\r\n]+?)(?P<eol>\r?\n?))$')
_JSON_ROW = re.compile(r'^(?P<head>\s*"(?P<key>(?:[^"\\]|\\.)*)"\s*:\s*")(?P<digest>[0-9a-f]{64})'
                       r'(?P<rest>"\s*,?\s*\r?\n?)$')


class Refuse(Exception):
    """A page or record this tool will not touch. Nothing is written."""


def attrs(tag):
    return dict(re.findall(r'\s([a-zA-Z-]+)="([^"]*)"', tag))


def fix_text(text, pairs):
    """Pure. (new text, [(offset, inserted, action, dialog)]) for one page's text and its pairs.

    Raises Refuse naming every reason when any pair cannot be fixed; touches no disk. An empty edit
    list means the page already carries every recorded audience."""
    scripts = [(m.start(), m.end()) for m in re.finditer(r'<script\b.*?</script>', text, re.S | re.I)]
    in_script = lambda i: any(a <= i < b for a, b in scripts)
    edits, refusals, taken = [], [], {}
    for action, dialog in sorted({(a, d) for a, d in pairs}):
        d = re.search(r'<dialog\b[^>]*\bid="%s"[^>]*>' % re.escape(dialog), text)
        want = {k: v for k, v in attrs(d.group(0)).items() if k in AUD} if d else {}
        if not want:
            refusals.append(f'#{dialog} carries no audience attribute to copy')
            continue
        tags = [m for m in re.finditer(r'<button\b[^>]*\bdata-action="%s"[^>]*>' % re.escape(action), text)]
        live = [m for m in tags if not in_script(m.start())]
        if not live or len(live) != len(tags):
            refusals.append(f'data-action="{action}" matches {len(live)} tag(s) outside <script>, {len(tags) - len(live)} inside')
            continue
        for m in live:
            have = {k: v for k, v in attrs(m.group(0)).items() if k in AUD}
            if have == want:
                continue  # already done
            if have and have != want:
                refusals.append(f'data-action="{action}" already carries a different audience {have}')
                continue
            if m.start() in taken:
                refusals.append(f'one tag would be edited for two dialogs: #{taken[m.start()]} and #{dialog}')
                continue
            taken[m.start()] = dialog
            add = ''.join(f' {k}="{v}"' for k, v in want.items())
            edits.append((m.end() - 1, add, action, dialog))
    if refusals:
        raise Refuse('; '.join(refusals))
    out = text
    for pos, add, _, _ in sorted(edits, reverse=True):
        out = out[:pos] + add + out[pos:]
    return out, sorted(edits)


def pairs_from_probe(rows):
    """{page: [(action, dialog)]}: every visible control the probe saw open a hidden dialog, in either
    staff-guide state."""
    out = {}
    for row in rows:
        pairs = {(o['action'], o['dialog']) for st in row['states'].values() for o in st['opens'] if not o['visible']}
        if pairs:
            out[row['page']] = sorted(pairs)
    return out


def record_pairs(record):
    """{page: [(action, dialog)]} from a DLG1_PAIRS record; refuses a record that is not the schema."""
    if record.get('schema') != RECORD_SCHEMA:
        raise Refuse('not a %s record' % RECORD_SCHEMA)
    out, seen = {}, set()
    for row in record['pairs']:
        if set(row) != {'page', 'action', 'dialog'}:
            raise Refuse('a pair row must be exactly page, action, dialog: %r' % (row,))
        key = (row['page'], row['action'], row['dialog'])
        if key in seen:
            raise Refuse('a pair row appears twice: %r' % (key,))
        seen.add(key)
        out.setdefault(row['page'], []).append((row['action'], row['dialog']))
    held = held_out(record)
    both = sorted(set(held) & set(out))
    if both:
        raise Refuse('a page is both held out and paired: ' + both[0])
    return {page: sorted(v) for page, v in out.items()}


def held_out(record):
    """{page: row} for the pages the record holds out by ruling."""
    return {row['page']: row for row in record.get('heldOut', [])}


def record_from_probe(probe_bytes, provenance):
    """Pure. The DLG1_PAIRS record: every measured pair, minus the pages the provenance holds out."""
    rows = json.loads(probe_bytes)
    measured = pairs_from_probe(rows)
    held = {row['page']: row for row in provenance.get('heldOut', [])}
    absent = sorted(set(held) - set(measured))
    if absent:
        raise Refuse('a held-out page has no measured pair to hold: ' + absent[0])
    pairs = [{'page': p, 'action': a, 'dialog': d}
             for p in sorted(measured) if p not in held for a, d in measured[p]]
    return {
        'schema': RECORD_SCHEMA,
        'what': 'The controls DLG-1 edits: on each page, the control (by its data-action) that the probe '
                'saw open a dialog while the dialog stayed hidden. fix_dialog_audience.py copies that '
                "dialog's own audience attributes onto the control's opening tag.",
        'ruling': provenance['ruling'],
        'probe': dict(provenance['probe'],
                      sha256=hashlib.sha256(probe_bytes).hexdigest(),
                      bytes=len(probe_bytes),
                      pagesWithADialog=len(rows),
                      pagesFailing=len(measured),
                      hiddenDialogOpens=sum(len(v) for v in measured.values())),
        'heldOut': [dict(held[p], pairs=[{'action': a, 'dialog': d} for a, d in measured[p]])
                    for p in sorted(held)],
        'pages': len({r['page'] for r in pairs}),
        'controls': len(pairs),
        'pairs': pairs,
    }


def dump_record(record):
    """The record as committed: two-space JSON, one pair per line."""
    head = dict(record)
    pairs = head.pop('pairs')
    text = json.dumps(head, indent=2, ensure_ascii=False)
    assert text.endswith('\n}')
    return (text[:-2] + ',\n  "pairs": [\n'
            + ',\n'.join('    ' + json.dumps(p, ensure_ascii=False) for p in pairs) + '\n  ]\n}\n')


def recut_lines(text, digests, row_re, key):
    """Pure. (`text` with the digest of each row named in `digests` replaced, the rows that moved).
    Every other byte is kept: the line, its row name, its ending, and every other row."""
    out, moved = [], []
    for line in text.splitlines(keepends=True):
        m = row_re.match(line)
        if m and key(m) in digests and m.group('digest') != digests[key(m)]:
            line = line[:m.start('digest')] + digests[key(m)] + line[m.end('digest'):]
            moved.append(key(m))
        out.append(line)
    return ''.join(out), moved


def sums_key(m):
    return m.group('name')


def json_key(m):
    return json.loads('"%s"' % m.group('key'))


def listing(root, page):
    """[(manifest rel, row name, kind)] for every pack manifest on disk that names this page."""
    out, parts = [], page.split('/')
    for i in range(len(parts) - 1, 0, -1):
        folder = '/'.join(parts[:i]) + '/'
        for name in SUMS_NAMES:
            p = root / folder / name
            if p.is_file():
                row = page[len(folder):]
                text = p.read_bytes().decode('utf-8')
                if any((m := _SUMS_ROW.match(line)) and m.group('name') == row
                       for line in text.splitlines(keepends=True)):
                    out.append((folder + name, row, 'sums'))
    for manifest, keyroot in JSON_MANIFESTS.items():
        p = root / manifest
        if page.startswith(keyroot) and p.is_file() and page[len(keyroot):] in json.loads(p.read_bytes()):
            out.append((manifest, page[len(keyroot):], 'json'))
    return out


def recut(root, pages):
    """Re-cut the listing row of every page in every manifest naming it, from the page's bytes on
    disk. Returns {manifest: [rows re-cut]}; writes only a manifest whose bytes change."""
    by_manifest = {}
    for page in pages:
        digest = hashlib.sha256((root / page).read_bytes()).hexdigest()
        for manifest, row, kind in listing(root, page):
            by_manifest.setdefault((manifest, kind), {})[row] = digest
    report = {}
    for (manifest, kind), digests in sorted(by_manifest.items()):
        p = root / manifest
        before = p.read_bytes().decode('utf-8')
        row_re, key = (_SUMS_ROW, sums_key) if kind == 'sums' else (_JSON_ROW, json_key)
        after, moved = recut_lines(before, digests, row_re, key)
        if len(after.splitlines(keepends=True)) != len(before.splitlines(keepends=True)):
            raise Refuse(f'{manifest}: the re-cut moved a line; refusing to write')
        if after != before:
            p.write_bytes(after.encode('utf-8'))
        report[manifest] = sorted(moved)
    return report


def plan(root, pairs_by_page):
    edits, refusals, texts = {}, [], {}
    for page, pairs in sorted(pairs_by_page.items()):
        text = (root / page).read_bytes().decode('utf-8')  # bytes, so CRLF and offsets survive exactly
        try:
            new, page_edits = fix_text(text, pairs)
        except Refuse as why:
            refusals.append(f'{page}: {why}')
            continue
        if page_edits:
            edits[page] = page_edits
            texts[page] = new
    return edits, refusals, texts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument('--probe', type=Path, help='check_dialog_audience.cjs --json output')
    src.add_argument('--pairs', type=Path, help='the committed record, tools/hum/DLG1_PAIRS.json')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--recut', action='store_true', help='re-cut the listing row digests of the recorded pages')
    ap.add_argument('--write-record', type=Path, help='derive the pairs record from --probe')
    ap.add_argument('--provenance', type=Path, help='with --write-record: ruling, probe command and commit, held-out pages')
    ap.add_argument('--check', action='store_true', help='with --write-record: compare, write nothing')
    a = ap.parse_args()

    if a.write_record:
        if not a.probe or not a.provenance:
            ap.error('--write-record needs --probe and --provenance')
        try:
            text = dump_record(record_from_probe(a.probe.read_bytes(), json.loads(a.provenance.read_text())))
        except Refuse as why:
            print(f'REFUSED, nothing written: {why}'); sys.exit(1)
        same = a.write_record.is_file() and a.write_record.read_text() == text
        if a.check:
            print('record matches the probe' if same else '[FAIL] the record differs from the probe derivation')
            sys.exit(0 if same else 1)
        if not same:
            a.write_record.write_text(text)
        print(f'record {"unchanged" if same else "written"}: {a.write_record}')
        return
    if not a.root:
        ap.error('--root is required')
    if a.pairs:
        record = json.loads(a.pairs.read_text())
        try:
            pairs_by_page = record_pairs(record)
        except Refuse as why:
            print(f'REFUSED, nothing written: {why}'); sys.exit(1)
    else:
        pairs_by_page = pairs_from_probe(json.loads(a.probe.read_text()))
    edits, refusals, texts = plan(a.root, pairs_by_page)
    if refusals:
        print('REFUSED, nothing written:'); [print('  ' + r) for r in refusals]
        sys.exit(1)
    n = sum(len(v) for v in edits.values())
    by = {}
    for v in edits.values():
        for _, add, action, dialog in v:
            by[(action, dialog, add.strip())] = by.get((action, dialog, add.strip()), 0) + 1
    print(f'{len(edits)} page(s), {n} control tag(s):')
    for (action, dialog, add), c in sorted(by.items()):
        print(f'  {c:4}  data-action="{action}" -> #{dialog}  gains {add}')
    if a.apply:
        for rel, new in texts.items():
            (a.root / rel).write_bytes(new.encode('utf-8'))
        print('applied')
    if a.recut:
        try:
            report = recut(a.root, sorted(pairs_by_page))
        except Refuse as why:
            print(f'REFUSED: {why}'); sys.exit(1)
        rows = sum(len(v) for v in report.values())
        print(f're-cut {rows} row digest(s) in {len(report)} manifest(s)')
        for manifest, r in report.items():
            print(f'  {len(r):4}  {manifest}')


if __name__ == '__main__':
    main()
