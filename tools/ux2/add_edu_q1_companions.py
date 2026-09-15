#!/usr/bin/env python3
"""EDU-TRY-LESSON prerequisite (CX2 §5.3, approved by Matt 16 Sep 2026): give the two
EDU-Q1 pilots that lack one a companion-pack catalogue row, the way Sugar has.

    python3 tools/ux2/add_edu_q1_companions.py [--check]

The catalogue's pack rows are DERIVED from data/companion-packs.json (the D2 placement
manifest) by tools/ux2/companion_catalogue.py and never typed, and the display-title
reference (W-token) comes from the same manifest through build_display_titles.py. The
Friction (GROW W3A) and Diffusion (LAUNCH W4L1) natives were authored under EDU-Q1 and
already sit in the tree, so they never went through the D2 intake and have no manifest
entry; without one the homepage Try-a-lesson rotation cannot bind their pack route,
reference or preview, and would fall back to a single static Sugar card.

This appends the two entries in the manifest's own shape, measured from the files on
disk (bytes, sha256; intakeSha256 = sha256 because there is no separate intake), with
title from the lesson's own label and builtFrom = the lesson's sha256, then runs the
existing derivers in order: pack rows and evidence, display titles, lesson order,
resource sizes, the static check and the pack checker (C1-C7), and re-cuts the
catalogue pins and PIN1. It refuses to add an entry that already exists.
"""
from pathlib import Path
import argparse, hashlib, importlib, json, re, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'data/companion-packs.json'
HELPER = ROOT / 'tools/catalogue/pin_catalogue_contract.py'
GATE = ROOT / 'tools/verify_cross_estate_unification.py'
sys.path.insert(0, str(ROOT / 'tools/downloads'))
from build_download_pack import lesson_label  # noqa: E402

NEW = [
    {'id': 'pack-grow-science-w3a', 'folder': 'SCI_G_W3_Friction', 'subject': 'Science', 'pathway': 'GROW',
     'wtoken': 'W3A', 'term': 'Autumn 1', 'companionOf': 'Science_Teesside/Grow/SCI_G_W3_Friction.html',
     'files': [('lesson', 'pptx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_Science_Autumn1_W3A_Friction.pptx'),
               ('slides', 'pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_Science_Autumn1_W3A_Friction.pdf'),
               ('teacher', 'docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.docx'),
               ('teacher', 'pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.pdf'),
               ('pupil', 'docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.docx'),
               ('pupil', 'pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.pdf')]},
    {'id': 'pack-launch-science-w4l1', 'folder': 'SCI_L_W4_L1_Diffusion', 'subject': 'Science', 'pathway': 'LAUNCH',
     'wtoken': 'W4L1', 'term': 'Autumn 1', 'companionOf': 'Science_Teesside/Launch/SCI_L_W4_L1_Diffusion.html',
     'files': [('lesson', 'pptx', 'Science_Teesside/Teaching_Packs/LAUNCH/Week_4/W4L1_Diffusion.pptx'),
               ('slides', 'pdf', 'Science_Teesside/Teaching_Packs/LAUNCH/Week_4/W4L1_Diffusion.pdf'),
               ('pupil', 'docx', 'Science_Teesside/Teaching_Packs/LAUNCH/Week_4/W4L1_Worksheet.docx'),
               ('pupil', 'pdf', 'Science_Teesside/Teaching_Packs/LAUNCH/Week_4/W4L1_Worksheet.pdf')]},
]


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def entry(spec):
    lesson = ROOT / spec['companionOf']
    files = []
    for role, kind, rel in spec['files']:
        p = ROOT / rel
        assert p.is_file(), 'missing ' + rel
        d = sha(p)
        files.append({'role': role, 'type': kind, 'path': rel, 'bytes': p.stat().st_size, 'sha256': d, 'intakeSha256': d})
    return {'id': spec['id'], 'folder': spec['folder'], 'subject': spec['subject'], 'pathway': spec['pathway'],
            'wtoken': spec['wtoken'], 'term': spec['term'], 'title': lesson_label(lesson.read_bytes()),
            'companionOf': spec['companionOf'], 'matchMethod': 'title', 'builtFrom': sha(lesson),
            'packRevisionDrift': False, 'driftFields': [], 'held': [], 'files': files}


def run(*cmd):
    return subprocess.run([sys.executable, *cmd], cwd=ROOT, capture_output=True, text=True)


def repin():
    sys.path.insert(0, str(HELPER.parent))
    helper = importlib.reload(importlib.import_module('pin_catalogue_contract'))
    committed = subprocess.check_output(['git', '-C', str(ROOT), 'show', 'HEAD:tools/verify_cross_estate_unification.py']).decode()
    apps_digest = re.search(r'"apps\.json":\s*"([0-9a-f]{64})"', committed).group(1)
    with tempfile.TemporaryDirectory(prefix='apps-gate-stand-in-') as temp:
        apps = Path(temp); (apps / 'tools').mkdir()
        shutil.copyfile(GATE, apps / 'tools/verify_cross_estate_unification.py'); (apps / 'apps.json').write_bytes(b'{}')
        result = helper.pin(ROOT, apps, check=False)
    text = GATE.read_text()
    text, n = re.subn(r'("apps\.json":\s*")[0-9a-f]{64}(")', lambda m: m[1] + apps_digest + m[2], text); assert n == 1
    GATE.write_text(text)
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    m = json.loads(MANIFEST.read_text())
    have = {p['id'] for p in m['packs']}
    added = []
    for spec in NEW:
        if spec['id'] in have:
            continue
        added.append(entry(spec))
    if a.check:
        print(json.dumps({'missing': [e['id'] for e in added]})); raise SystemExit(1 if added else 0)
    m['packs'] += added
    m['counts']['packs'] = len(m['packs']); m['counts']['placed'] = sum(len(p['files']) for p in m['packs'])
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
    report = {'added': [{'id': e['id'], 'title': e['title'], 'files': len(e['files'])} for e in added]}
    steps = (('packRows', ('tools/ux2/companion_catalogue.py', '--write')),
             ('packCheck', ('tools/ux2/companion_catalogue.py', '--check')),
             ('displayTitles', ('tools/catalogue/build_display_titles.py',)),
             ('lessonOrder', ('tools/catalogue/build_lesson_order.py',)),
             ('resourceSizes', ('tools/ux2/resource_sizes.py', '--write')),
             ('staticCheck', ('tools/catalogue/check_catalogue_static.py',)),
             ('companionPacks', ('tools/ux2/check_companion_packs.py',)))
    codes = {}
    for label, cmd in steps:
        proc = run(*cmd); codes[label] = proc.returncode
        report[label] = {'returncode': proc.returncode, 'tail': (proc.stdout + proc.stderr).strip()[-240:]}
    report['pin'] = repin()
    p1 = run('tools/pin1/derive_triggers.py', '--write'); codes['pin1'] = p1.returncode
    report['pin1'] = {'returncode': p1.returncode, 'tail': (p1.stdout + p1.stderr).strip()[-120:]}
    print(json.dumps(report, indent=1, default=str))
    raise SystemExit(0 if all(c == 0 for c in codes.values()) else 1)
