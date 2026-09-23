#!/usr/bin/env python3
"""C (ruling 2026-09-23): take the product name off the served weekly-plan workbooks.

    xlsx_evidence_platform.py WORKBOOK...        rewrite in place, print provenance JSON
    xlsx_evidence_platform.py --check WORKBOOK... exit 1 if any cell text still names it

"EFL" -> "evidence platform" in CELL TEXT ONLY: the <t> text nodes of shared strings and
inline strings. Formulas (<f>), styles, sheet structure and every other part of the package
are left byte-identical. This writes at XML level on purpose: an openpyxl load/save, even with
no change, rewrites 11 of 12 parts and drops xl/sharedStrings.xml, which is exactly what the
ruling forbids. openpyxl is used instead as the independent verifier (see --verify).
"""
from __future__ import annotations
import hashlib, json, re, sys, zipfile, shutil, tempfile, os

NAME = re.compile(r'\bEFL\b')
T_NODE = re.compile(r'(<t(?:\s[^>]*)?>)(.*?)(</t>)', re.S)
TEXT_PARTS = re.compile(r'^xl/(sharedStrings\.xml|worksheets/sheet\d+\.xml)$')


def rewrite_part(xml: str):
    n = 0
    def fix(m):
        nonlocal n
        body, k = NAME.subn('evidence platform', m.group(2))
        n += k
        return m.group(1) + body + m.group(3)
    out = T_NODE.sub(fix, xml)
    # anything the text-node pass did not reach (e.g. inside a formula) is refused, never edited
    rest = NAME.findall(T_NODE.sub('', out))
    if rest:
        raise SystemExit('refusing: product name outside cell text (%d)' % len(rest))
    return out, n


def rewrite(path: str) -> dict:
    before = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    src = zipfile.ZipFile(path)
    changed, cells = [], 0
    fd, tmp = tempfile.mkstemp(suffix='.xlsx'); os.close(fd)
    with zipfile.ZipFile(tmp, 'w') as dst:
        for info in src.infolist():                    # same order, same names, same dates
            data = src.read(info.filename)
            if TEXT_PARTS.match(info.filename):
                xml = data.decode('utf-8')
                new, k = rewrite_part(xml)
                if k:
                    data = new.encode('utf-8'); changed.append(info.filename); cells += k
            dst.writestr(info, data, compress_type=info.compress_type)
    if cells:
        shutil.move(tmp, path)
    else:
        os.remove(tmp)
    return {'file': path, 'sha256Before': before,
            'sha256After': hashlib.sha256(open(path, 'rb').read()).hexdigest(),
            'occurrencesReplaced': cells, 'partsChanged': changed}


def remaining(path: str) -> int:
    z = zipfile.ZipFile(path)
    return sum(len(NAME.findall(z.read(n).decode('utf-8', 'replace')))
               for n in z.namelist() if n.endswith('.xml'))


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[:1] == ['--check']:
        bad = {p: remaining(p) for p in args[1:] if remaining(p)}
        print(json.dumps({'checked': len(args) - 1, 'withName': bad}))
        sys.exit(1 if bad else 0)
    print(json.dumps([rewrite(p) for p in args], indent=1))
