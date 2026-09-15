#!/usr/bin/env python3
"""CX2 S3 (R4, §25.4): name the offline companion pages for what they are.

Matt's ruling, 15 September 2026: relabel the whole set rather than retire Week 3.

Measured first, on main: all twenty companion pages (BUILD and GROW, weeks 3-7) are a
separate ~70KB chassis that shares no sampled text run with its 285-413KB canonical
lesson, in any week. They were never exports of the lesson, and no generator for them
exists in the repository or its history. Retiring Week 3 alone would have left eighteen
pages in the same condition, so the hub names the set instead.

The pack hub Science_Teesside/Teaching_Packs/web-slides.html is edited, idempotently:

  * each pathway's standing sentence becomes an explicit statement that these are a
    lightweight offline edition and not the full lesson;
  * each of the twenty lesson entries gains a link to its canonical online lesson, and
    its first link is renamed so "web slides" is not mistaken for the lesson itself.

Nothing else moves: no page is deleted, no route is removed, the editable pack files and
the companions themselves are untouched. The wording claims no feature a given lesson may
not have -- only that the online lesson is the current, complete version.

    python3 tools/science_teaching_packs/cx2_s3_offline_edition.py [--check]
"""
from pathlib import Path
import argparse, hashlib, html, importlib, json, re, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[2]
HUB = 'Science_Teesside/Teaching_Packs/web-slides.html'
BOUNDARY = ROOT / '_glv3/tools/verify_change_boundary.py'
HELPER = ROOT / 'tools/catalogue/pin_catalogue_contract.py'
GATE = ROOT / 'tools/verify_cross_estate_unification.py'
EVIDENCE = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
VAR, NAME, MARK = 'CX2_S3_REPLACEMENTS', 'S3 offline edition labelling', 'S3 OFFLINE EDITION'

OLD_SENTENCE = ('<p>These pages are web-slide views of the existing PowerPoint decks; '
                'the editable files and PDFs stay in the pack above.</p>')
NEW_SENTENCE = ('<p><strong>Lightweight offline edition.</strong> These pages are compact web-slide views of the '
                'PowerPoint decks, for teaching without a network. They are not the full lesson: the online lesson '
                'is the current, complete version, and each lesson below links to it. The editable files and PDFs '
                'stay in the pack above.</p>')
# The hub stores a literal arrow, not the entity; matching the entity silently renamed nothing.
OLD_LINK_TEXT = '>Open as web slides \u2192<'
NEW_LINK_TEXT = '>Open the offline web slides<'

# Each week's A and B companion belong to that week's single canonical paired lesson.
CANONICAL = {
    ('build', 3): 'Build/SCI_B_W3_Backbones.html',
    ('build', 4): 'Build/SCI_B_W4_Muscle_Pairs.html',
    ('build', 5): 'Build/SCI_B_W5_Right_Nutrition.html',
    ('build', 6): 'Build/SCI_B_W6_Balanced_Plate.html',
    ('build', 7): 'Build/SCI_B_W7_Where_Food_Comes_From.html',
    ('grow', 3): 'Grow/SCI_G_W3_Friction.html',
    ('grow', 4): 'Grow/SCI_G_W4_Mechanisms.html',
    ('grow', 5): 'Grow/SCI_G_W5_Fair_Test.html',
    ('grow', 6): 'Grow/SCI_G_W6_Earth_And_Planets.html',
    ('grow', 7): 'Grow/SCI_G_W7_The_Moon.html',
}
ARTICLE = re.compile(r'(<article class="lesson" id="(build|grow)-\w+_science_w(\d)[ab]">)(.*?)(</article>)', re.S | re.I)
MARKER = 'class="canonical-lesson"'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args]).decode()


def rewrite(text):
    """Idempotent: a tree already carrying the new wording and links is returned unchanged."""
    if OLD_SENTENCE in text:
        assert text.count(OLD_SENTENCE) == 2, text.count(OLD_SENTENCE)
        text = text.replace(OLD_SENTENCE, NEW_SENTENCE)
    if OLD_LINK_TEXT in text:
        assert text.count(OLD_LINK_TEXT) == 20, text.count(OLD_LINK_TEXT)
        text = text.replace(OLD_LINK_TEXT, NEW_LINK_TEXT)

    def add_link(match):
        head, pathway, week, body, tail = match.groups()
        if MARKER in body:
            return match.group(0)
        target = CANONICAL[(pathway.lower(), int(week))]
        assert (ROOT / 'Science_Teesside' / target).is_file(), target
        link = ('<p class="canonical-lesson"><a href="../%s">Open the full online lesson</a> '
                '&mdash; the current, complete version of this lesson.</p>' % html.escape(target))
        return head + body + link + tail

    text, count = ARTICLE.subn(add_link, text)
    assert count == 20, count
    return text


def edit_hub(check):
    path = ROOT / HUB
    text = path.read_text(encoding='utf-8')
    new = rewrite(text)
    assert rewrite(new) == new, 'rewrite is not idempotent'
    assert new.count(MARKER) == 20 and NEW_SENTENCE in new
    changed = new != text
    if changed and check:
        raise SystemExit('[FAIL] the pack hub does not carry the offline-edition labelling')
    if changed:
        path.write_text(new, encoding='utf-8')
    return changed


def transaction():
    entry = git('ls-tree', REVIEW_BASE, '--', HUB).split()
    assert entry and entry[0] == '100644' and entry[1] == 'blob', HUB
    assert git('diff', '--name-status', REVIEW_BASE, '--', HUB).startswith('M\t'), 'not a modification vs review base'
    return {HUB: {'beforeGitBlob': entry[2], 'afterSha256': sha(ROOT / HUB), 'bytes': (ROOT / HUB).stat().st_size}}


def declare_transaction(files, check):
    text = BOUNDARY.read_text()
    block = '# BEGIN %s REPLACEMENTS\n%s = %r\n# END %s REPLACEMENTS\n' % (MARK, VAR, files, MARK)
    if 'CX2_S3_REVIEW_BASE' not in text:
        text = text.replace('# BEGIN DECLARED TRANSACTIONS\n',
                            "# CX2 S3 (Matt's ruling, 15 September 2026): the pack hub names the offline companion\n"
                            "# set as a lightweight offline edition and links each entry to its canonical lesson,\n"
                            "# written by tools/science_teaching_packs/cx2_s3_offline_edition.py.\n"
                            "CX2_S3_REVIEW_BASE = %r\n# BEGIN DECLARED TRANSACTIONS\n" % REVIEW_BASE, 1)
    pattern = r'# BEGIN %s REPLACEMENTS\n.*?# END %s REPLACEMENTS\n' % (MARK, MARK)
    if re.search(pattern, text, flags=re.S):
        text = re.sub(pattern, lambda _: block, text, flags=re.S)
    else:
        text = text.replace('# END DECLARED TRANSACTIONS\n', block + '# END DECLARED TRANSACTIONS\n', 1)
    entry = "    %r: (CX2_S3_REVIEW_BASE, %s),\n" % (NAME, VAR)
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
    sys.path.insert(0, str(HELPER.parent))
    helper = importlib.import_module('pin_catalogue_contract')
    missing = [rel for rel in files if rel not in helper.REVIEWED_PATHS]
    if missing:
        if check:
            raise SystemExit('[FAIL] reviewed-path list lacks: ' + ', '.join(missing))
        text = HELPER.read_text()
        addition = ('\n\n# CX2 S3: the teaching-pack hub, relabelled so the offline companion set is not read\n'
                    '# as the lesson itself.\nREVIEWED_PATHS += (\n'
                    + ''.join('    %r,\n' % rel for rel in missing) + ')\n')
        anchor = "\n\ndef pack_rows_for(lessons: Path, rows: list) -> list:"
        assert text.count(anchor) == 1
        HELPER.write_text(text.replace(anchor, addition + anchor))
        importlib.reload(helper)
    return missing


def refresh_evidence(check):
    data = json.loads(EVIDENCE.read_text())
    entry = data['entries'].get(HUB)
    if entry is None or 'sha256' not in entry:
        return False
    current = sha(ROOT / HUB)
    changed = entry['sha256'] != current
    if changed and check:
        raise SystemExit('[FAIL] evidence sha256 stale for the pack hub')
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
    ap.add_argument('--base', default=None, help='review base (default: the merge base with origin/main)')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    REVIEW_BASE = args.base or git('merge-base', 'origin/main', 'HEAD').strip()
    report = {'reviewBase': REVIEW_BASE, 'hubEdited': edit_hub(args.check)}
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
