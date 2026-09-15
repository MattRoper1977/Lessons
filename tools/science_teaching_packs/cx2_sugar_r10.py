#!/usr/bin/env python3
"""CX2 §4.8 hygiene on the accepted BUILD W8A Sugar lesson: no product name on a public
surface (ruling R10), and the BUILD checksum rows brought back to the bytes on disk.

Edits, idempotently:
  * Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html — three staff
    sentences that named the evidence product now name the school's digital evidence
    platform (the same wording the Friction, Diffusion and return-week cards use);
  * .../W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Teacher.docx — the same
    three sentences; the Teacher PDF is re-rendered from it by LibreOffice;
  * Science_Teesside/Teaching_Packs/BUILD/SHA256SUMS.txt — the six W8A rows recomputed
    (they were left at the pre-correction digests when the Sugar accessibility
    corrections landed; measured 2026-09-15: all six rows differed from disk);
  * _glv3/tools/verify_change_boundary.py — its own reviewed replacement transaction over
    the four files, declared after the merged Sugar one (which it supersedes on those
    paths; the tool's declaration order is review order);
  * tools/catalogue/TERM_AND_STYLE_EVIDENCE.json — the lesson's sha256; then lesson order,
    resource sizes, the static check, CATALOGUE_PINS and the PIN1 triggers through the
    existing tools.

    python3 tools/science_teaching_packs/cx2_sugar_r10.py [--check]

Nothing pupil-facing changes: the three sentences sit in the staff feedback card.
No pupil data is touched. Banned wording is asserted absent afterwards.
"""
from pathlib import Path
import argparse, hashlib, importlib, json, re, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[2]
LESSON = 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html'
PACK = 'Science_Teesside/Teaching_Packs/BUILD/'
STEM = PACK + 'lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label'
TEACHER_DOCX = STEM + '_Teacher.docx'
TEACHER_PDF = STEM + '_Teacher.pdf'
SUMS = PACK + 'SHA256SUMS.txt'
BOUNDARY = ROOT / '_glv3/tools/verify_change_boundary.py'
HELPER = ROOT / 'tools/catalogue/pin_catalogue_contract.py'
GATE = ROOT / 'tools/verify_cross_estate_unification.py'
EVIDENCE = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
PLATFORM = "the school's digital evidence platform"
# (old, new) pairs; the HTML pair set uses the em dash the lesson uses, the DOCX the hyphen it uses.
PAIRS_HTML = [
    ('the 16-page EFL version.', 'the 16-page copy.'),
    ('EFL capture should be lean and purposeful, with clips listened to before tagging.',
     'Evidence capture on ' + PLATFORM + ' should be lean and purposeful, with clips listened to before tagging.'),
    ('E — evidence on EFL;', 'E — evidence captured on ' + PLATFORM + ';'),
]
PAIRS_DOCX = [
    ('the 16-page EFL version.', 'the 16-page copy.'),
    ('EFL capture should be lean and purposeful, with clips listened to before tagging.',
     'Evidence capture on ' + PLATFORM + ' should be lean and purposeful, with clips listened to before tagging.'),
    ('E - evidence on EFL;', 'E - evidence captured on ' + PLATFORM + ';'),
]
BANNED = re.compile(r'\bEarwig\b|\bEfL\b|\bEFL\b', re.I)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def edit_html(check):
    path = ROOT / LESSON
    text = path.read_text(encoding='utf-8')
    new = text
    for old, rep in PAIRS_HTML:
        n = new.count(old)
        assert n in (0, 1), (old, n)
        new = new.replace(old, rep)
    scrubbed = re.sub(r'<script.*?</script>|<style.*?</style>', '', new, flags=re.S)
    assert not BANNED.search(scrubbed), 'a product name remains in the lesson text'
    changed = new != text
    if changed and check:
        raise SystemExit('[FAIL] lesson still carries the product name')
    if changed:
        path.write_text(new, encoding='utf-8')
    return changed


def edit_docx(check):
    from docx import Document
    path = ROOT / TEACHER_DOCX
    doc = Document(str(path))
    changed = False
    for para in doc.paragraphs:
        for old, rep in PAIRS_DOCX:
            if old in para.text:
                assert len(para.runs) == 1, ('sentence spans runs', para.text[:60])
                para.runs[0].text = para.runs[0].text.replace(old, rep)
                changed = True
    for para in doc.paragraphs:
        assert not BANNED.search(para.text), para.text[:80]
    if changed and check:
        raise SystemExit('[FAIL] teacher document still carries the product name')
    if changed:
        doc.save(str(path))
        with tempfile.TemporaryDirectory(prefix='sugar-render-') as temp:
            subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', temp, str(path)],
                           check=True, capture_output=True, timeout=300)
            produced = Path(temp) / (path.stem + '.pdf')
            assert produced.is_file()
            shutil.copyfile(produced, ROOT / TEACHER_PDF)
    return changed


def refresh_sums(check):
    path = ROOT / SUMS
    rows = path.read_text().splitlines()
    out, changed = [], []
    for row in rows:
        old, rel = row.split('  ', 1)
        current = sha(ROOT / PACK / rel)
        if current != old:
            assert rel.startswith('lessons/W8A/'), 'checksum row moved outside W8A: ' + rel
            changed.append(rel)
        out.append(f'{current}  {rel}')
    assert len(out) == len(rows)
    if changed and check:
        raise SystemExit('[FAIL] checksum rows stale: ' + ', '.join(changed))
    if changed:
        path.write_text('\n'.join(out) + '\n')
    return changed


REVIEW_BASE = 'a8b3c9689d9b1d74e56a70f065773bf3942b63c9'   # main after Diffusion #546 merged (CX2 §3)
MEMBERS = (LESSON, TEACHER_DOCX, TEACHER_PDF, SUMS)
VAR, NAME, MARK = 'SUGAR_R10_REPLACEMENTS', 'Sugar R10 hygiene', 'SUGAR R10 HYGIENE'


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args]).decode()


def transaction():
    files = {}
    for rel in MEMBERS:
        entry = git('ls-tree', REVIEW_BASE, '--', rel).split()
        assert entry and entry[0] == '100644' and entry[1] == 'blob', rel
        assert git('diff', '--name-status', REVIEW_BASE, '--', rel).startswith('M\t'), 'not a modification vs review base: ' + rel
        files[rel] = {'beforeGitBlob': entry[2], 'afterSha256': sha(ROOT / rel), 'bytes': (ROOT / rel).stat().st_size}
    return dict(sorted(files.items()))


def declare_transaction(files, check):
    """Its own transaction, declared after the merged Sugar one so it supersedes the
    Sugar claim on the four paths it revises (declaration order is review order)."""
    text = BOUNDARY.read_text()
    block = '# BEGIN %s REPLACEMENTS\n%s = %r\n# END %s REPLACEMENTS\n' % (MARK, VAR, files, MARK)
    if 'SUGAR_R10_REVIEW_BASE' not in text:
        text = text.replace('# BEGIN DECLARED TRANSACTIONS\n',
                            "# CX2 4.8: the accepted Sugar lesson's staff card without a product name (R10), the\n"
                            "# re-rendered teacher document and the refreshed BUILD checksum rows, written by\n"
                            "# tools/science_teaching_packs/cx2_sugar_r10.py.\nSUGAR_R10_REVIEW_BASE = %r\n# BEGIN DECLARED TRANSACTIONS\n" % REVIEW_BASE, 1)
    pattern = r'# BEGIN %s REPLACEMENTS\n.*?# END %s REPLACEMENTS\n' % (MARK, MARK)
    if re.search(pattern, text, flags=re.S):
        text = re.sub(pattern, lambda _: block, text, flags=re.S)
    else:
        text = text.replace('# END DECLARED TRANSACTIONS\n', block + '# END DECLARED TRANSACTIONS\n', 1)
    entry = "    %r: (SUGAR_R10_REVIEW_BASE, %s),\n" % (NAME, VAR)
    if entry not in text:
        text = text.replace('    # END DECLARED TRANSACTION ENTRIES\n', entry + '    # END DECLARED TRANSACTION ENTRIES\n', 1)
    assert text.count(entry) == 1 and text.count('# BEGIN %s REPLACEMENTS' % MARK) == 1
    changed = text != BOUNDARY.read_text()
    if changed and check:
        raise SystemExit('[FAIL] boundary transaction differs from the tree')
    if changed:
        BOUNDARY.write_text(text)
    return changed


def extend_reviewed_paths(files, check):
    """Every member needs an owner-reviewed digest in CATALOGUE_PINS; the checksum
    list was allowed to change but never pinned, so it is admitted here."""
    sys.path.insert(0, str(HELPER.parent))
    helper = importlib.import_module('pin_catalogue_contract')
    missing = [rel for rel in files if rel not in helper.REVIEWED_PATHS]
    if missing:
        if check:
            raise SystemExit('[FAIL] reviewed-path list lacks: ' + ', '.join(missing))
        text = HELPER.read_text()
        addition = ('\n\n# CX2 4.8 Sugar hygiene: the BUILD checksum list joins the reviewed Sugar files.\n'
                    'REVIEWED_PATHS += (\n' + ''.join('    %r,\n' % rel for rel in missing) + ')\n')
        anchor = "\n\ndef pack_rows_for(lessons: Path, rows: list) -> list:"
        assert text.count(anchor) == 1
        HELPER.write_text(text.replace(anchor, addition + anchor))
        importlib.reload(helper)
    return missing


def refresh_evidence(check):
    data = json.loads(EVIDENCE.read_text())
    entry = data['entries'][LESSON]
    current = sha(ROOT / LESSON)
    changed = entry.get('sha256') != current
    if changed and check:
        raise SystemExit('[FAIL] evidence sha256 stale for the lesson')
    if changed:
        entry['sha256'] = current
        EVIDENCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    return changed


def run(*cmd):
    return subprocess.run([sys.executable, *cmd], cwd=ROOT, capture_output=True, text=True)


def repin(check):
    sys.path.insert(0, str(HELPER.parent))
    helper = importlib.reload(importlib.import_module('pin_catalogue_contract'))
    committed = git('show', 'HEAD:tools/verify_cross_estate_unification.py')
    apps_digest = re.search(r'"apps\.json":\s*"([0-9a-f]{64})"', committed).group(1)
    before = GATE.read_bytes()
    with tempfile.TemporaryDirectory(prefix='apps-gate-stand-in-') as temp:
        apps = Path(temp); (apps / 'tools').mkdir()
        shutil.copyfile(GATE, apps / 'tools/verify_cross_estate_unification.py')
        (apps / 'apps.json').write_bytes(b'{}')
        try:
            result = helper.pin(ROOT, apps, check=False)
        except ValueError as exc:
            raise SystemExit('[FAIL] ' + str(exc))
    after = GATE.read_text()
    after, count = re.subn(r'("apps\.json":\s*")[0-9a-f]{64}(")', lambda m: m[1] + apps_digest + m[2], after)
    assert count == 1
    if check:
        GATE.write_bytes(before)
        if after.encode() != before:
            raise SystemExit('[FAIL] reviewed catalogue pins differ from the tree; re-run without --check')
        result['mode'] = 'check'
    else:
        GATE.write_text(after)
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    report = {'lessonEdited': edit_html(args.check), 'teacherEdited': edit_docx(args.check),
              'checksumRows': refresh_sums(args.check)}
    files = transaction()
    report['boundaryChanged'] = declare_transaction(files, args.check)
    report['reviewedPathsAdded'] = extend_reviewed_paths(files, args.check)
    report['evidenceRefreshed'] = refresh_evidence(args.check)
    codes = {}
    for label, cmd in (('resourceSizes', ('tools/ux2/resource_sizes.py', '--check' if args.check else '--write')),
                       ('lessonOrder', ('tools/catalogue/build_lesson_order.py', *(['--check'] if args.check else []))),
                       ('staticCheck', ('tools/catalogue/check_catalogue_static.py',))):
        proc = run(*cmd); codes[label] = proc.returncode
        report[label] = {'returncode': proc.returncode, 'tail': (proc.stdout + proc.stderr).strip()[-160:]}
    report['pin'] = repin(args.check)
    pin1 = run('tools/pin1/derive_triggers.py', '--check' if args.check else '--write'); codes['pin1'] = pin1.returncode
    report['pin1'] = {'returncode': pin1.returncode, 'tail': (pin1.stdout + pin1.stderr).strip()[-160:]}
    print(json.dumps(report, indent=2, default=str))
    raise SystemExit(0 if all(c == 0 for c in codes.values()) else 1)
