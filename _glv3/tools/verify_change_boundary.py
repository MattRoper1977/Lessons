#!/usr/bin/env python3
"""Retain GLV3 isolation while checking the explicitly reviewed cover additions.

This replaces only the old blanket changed-path assertion. All generated-tree,
GLV3 count, browser, print, contact-sheet and original tamper checks still run.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
PROTECTED = ('Art_Teesside', 'GROW_ASDAN', 'LAUNCH_ASDAN', 'Grow/Slideshows',
             'Launch/Slideshows', 'Science_Teesside', 'Humanities_Teesside',
             'Baseline_Weeks', 'BUILD_Estate_v3')
SHELVES = ('Science_Teesside/index.html', 'Humanities_Teesside/index.html')
COVER = 'Humanities_Teesside/David_Cover_Autumn1_W3-W7'
SCIENCE_PACKS = 'Science_Teesside/Teaching_Packs/'
SOURCE = 'tools/humanities_resources/SOURCE_MANIFEST.json'
DOWNLOADS = 'tools/humanities_resources/DOWNLOAD_MANIFEST.json'
LABEL_EDITS = 'tools/humanities_resources/PUBLIC_LABEL_CHANGES.json'
BOUND_INPUTS = (SOURCE, DOWNLOADS, LABEL_EDITS, 'tools/humanities_resources/CONTENT.json',
                'tools/humanities_resources/ORIGINAL_MEMBER_MANIFEST.json',
                'tools/humanities_resources/build_resources.py',
                'tools/humanities_resources/check_resources.py',
                'tools/humanities_resources/resource.css',
                'tools/humanities_resources/resource.js')


# EDU-Q1: exactly the reviewed Sugar HTML and six existing companions.
# This is a replacement transaction, never a directory-wide permission.
SUGAR_REVIEW_BASE = '11bba1875e27016547186754ed65752152e27c9b'
SUGAR_REPLACEMENTS = {'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html': {'beforeGitBlob': 'bd1d6da15f32efc7ce068e9f4e846bb7038bb80a', 'afterSha256': 'fdf2d09803e19d11e8f82949efaeb8255893627841fd1a3f7860093350bbca1e', 'bytes': 626431}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label.pdf': {'beforeGitBlob': 'abd9261ff123775b2af979761d08dbe1ea5e2662', 'afterSha256': 'fc9ba726c94177000d872c28e3c7db3812c268d6552e936a316c38654a95a0dd', 'bytes': 431296}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label.pptx': {'beforeGitBlob': 'aff41a6c51c8eb21fbce611316590ed255be7078', 'afterSha256': 'd93b814710bcf57ece951ba0aaf82ed41320247571ec48147e26a5423b3c07e3', 'bytes': 158524}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Pupil.docx': {'beforeGitBlob': '81015f010d39c157bdd7f5c3f453ad2e6912c11e', 'afterSha256': 'be71bc9be6c6d9c23383ee35ec739df80830ad5e336e7095098deaf3003a6d64', 'bytes': 42521}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Pupil.pdf': {'beforeGitBlob': 'a1e81df065fe01d01d0eda19549ec33883bc1a27', 'afterSha256': '25544b193963f552a1511ac17bd5b5353cbeeca71d6788ac4deddbc61f905dc4', 'bytes': 170636}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Teacher.docx': {'beforeGitBlob': 'b111d7326d3bcad325167f2357b7f3741917dad1', 'afterSha256': '033a59447d5b42ea990dd0737c93db99a717e9055307f1c6b6ebe5bf7262c9b3', 'bytes': 43099}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Teacher.pdf': {'beforeGitBlob': '3fd844034e225e1c404a5cb50985951a0b4406ec', 'afterSha256': 'a4f9888e6b742339d54ba9128da824904b65e786054e8820d60df9980fa4af86', 'bytes': 114441}}

def git_before_entries(root, base):
    # Match git_changes' triple-dot semantics; do not trust a supplied manifest
    # for the previous file identities.
    merge_base = subprocess.check_output(['git', 'merge-base', base, 'HEAD'], cwd=root).decode().strip()
    raw = subprocess.check_output(['git', 'ls-tree', '-z', merge_base, '--', *sorted(SUGAR_REPLACEMENTS)], cwd=root)
    result = {}
    for record in raw.decode().split('\0'):
        if not record:
            continue
        fields, path = record.split('\t', 1)
        mode, kind, blob = fields.split()
        result[path] = (mode, kind, blob)
    return result


def sugar_replacement_errors(root, changes, pins, before_entries):
    selected = [(status, rel) for status, rel in changes if rel in SUGAR_REPLACEMENTS]
    if not selected:
        return []
    if len(selected) != len(SUGAR_REPLACEMENTS) or {rel for _, rel in selected} != set(SUGAR_REPLACEMENTS):
        return ['Sugar replacement must contain exactly the seven reviewed file modifications']
    errors = []
    for status, rel in selected:
        reviewed = SUGAR_REPLACEMENTS[rel]
        path = root / rel
        if status != 'M':
            errors.append('Sugar replacement is not a modification: ' + rel)
        if before_entries.get(rel) != ('100644', 'blob', reviewed['beforeGitBlob']):
            errors.append('Sugar previous file identity or mode differs: ' + rel)
        if path.is_symlink() or not path.is_file() or path.resolve().is_relative_to(root.resolve()) is False:
            errors.append('Sugar replacement must be a regular file inside the tree: ' + rel)
        elif path.stat().st_size != reviewed['bytes'] or sha(path) != reviewed['afterSha256']:
            errors.append('Sugar replacement bytes differ: ' + rel)
        if pins.get(rel) != reviewed['afterSha256']:
            errors.append('Sugar replacement lacks matching owner-reviewed catalogue admission: ' + rel)
    return errors


def sugar_controls(root, proposed_pins=None):
    # CI uses the real reviewed pin map. The optional map lets a review harness
    # exercise the proposed transaction before paired admissions are staged;
    # such a run is conditional evidence, never a production gate pass.
    pins = pin_map(root) if proposed_pins is None else proposed_pins
    changes = [('M', rel) for rel in sorted(SUGAR_REPLACEMENTS)]
    before = git_before_entries(root, SUGAR_REVIEW_BASE)
    rows = []
    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        rows.append({'name': name, 'status': 'PASS'})
    check('All seven reviewed replacements pass the bounded rule', not sugar_replacement_errors(root, changes, pins, before))
    for rel in sorted(SUGAR_REPLACEMENTS):
        missing_pin = dict(pins); missing_pin.pop(rel, None)
        check('Missing owner admission rejected: ' + rel, bool(sugar_replacement_errors(root, changes, missing_pin, before)))
        wrong_before = dict(before); wrong_before[rel] = ('100644', 'blob', '0' * 40)
        check('Wrong previous identity rejected: ' + rel, bool(sugar_replacement_errors(root, changes, pins, wrong_before)))
        wrong_mode = dict(before); wrong_mode[rel] = ('120000', 'blob', SUGAR_REPLACEMENTS[rel]['beforeGitBlob'])
        check('Previous symlink mode rejected: ' + rel, bool(sugar_replacement_errors(root, changes, pins, wrong_mode)))
        for status in ('A', 'D', 'T'):
            altered = [(status if path == rel else kind, path) for kind, path in changes]
            check('Wrong change type '+status+' rejected: ' + rel, bool(sugar_replacement_errors(root, altered, pins, before)))
        check('Omitted replacement rejected: ' + rel, bool(sugar_replacement_errors(root, [(kind, path) for kind, path in changes if path != rel], pins, before)))
    check('Duplicate replacement rejected', bool(sugar_replacement_errors(root, changes + [changes[0]], pins, before)))
    with tempfile.TemporaryDirectory(prefix='sugar-replacement-proof-') as temp:
        fixture = Path(temp)
        for rel in SUGAR_REPLACEMENTS:
            target = fixture / rel; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / rel, target)
        check('Actual candidate bytes pass in disposable fixture', not sugar_replacement_errors(fixture, changes, pins, before))
        for rel in sorted(SUGAR_REPLACEMENTS):
            path = fixture / rel; original = path.read_bytes()
            try:
                path.write_bytes(original + b'changed')
                check('Changed candidate bytes rejected: ' + rel, bool(sugar_replacement_errors(fixture, changes, pins, before)))
                # Even changing the caller's catalogue digest cannot change the
                # independent exact replacement review.
                repinned = dict(pins); repinned[rel] = sha(path)
                check('Repinned changed bytes still rejected: ' + rel, bool(sugar_replacement_errors(fixture, changes, repinned, before)))
                path.unlink()
                check('Missing candidate file rejected: ' + rel, bool(sugar_replacement_errors(fixture, changes, pins, before)))
                path.symlink_to(root / rel)
                check('Candidate symlink rejected: ' + rel, bool(sugar_replacement_errors(fixture, changes, pins, before)))
            finally:
                if path.is_symlink(): path.unlink()
                path.write_bytes(original)
        check('All sabotage was restored', not sugar_replacement_errors(fixture, changes, pins, before))
    return rows


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protected(path):
    return any(path == prefix or path.startswith(prefix + '/') for prefix in PROTECTED)


def pin_map(root):
    tree = ast.parse((root / 'tools/verify_cross_estate_unification.py').read_text())
    values = [ast.literal_eval(node.value) for node in tree.body
              if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'CATALOGUE_PINS' for t in node.targets)]
    if len(values) != 1:
        raise ValueError('expected exactly one reviewed catalogue pin block')
    return values[0]['files']


def explicit_cover_paths(root):
    source = json.loads((root / SOURCE).read_text())
    downloads = json.loads((root / DOWNLOADS).read_text())
    ids = [row['id'] for row in source['records']]
    if len(ids) != 25 or len(set(ids)) != 25 or not all(re.fullmatch(r'(?:BH|BR|GH|GR|LH)_W[3-7]', value) for value in ids):
        raise ValueError('cover IDs do not identify the 25 reviewed periods')
    dependencies = [row['path'] for row in downloads['dependencies']]
    if len(dependencies) != 69 or len(set(dependencies)) != 69:
        raise ValueError('expected 66 downloads plus three pathway archives')
    for rel in dependencies:
        path = PurePosixPath(rel)
        if path.is_absolute() or '..' in path.parts or '\\' in rel or not rel.startswith(COVER + '/'):
            raise ValueError('download manifest escapes the reviewed cover directory: ' + rel)
    return {*(COVER + '/' + name + '.html' for name in ids),
            COVER + '/index.html', COVER + '/resource.css', COVER + '/resource.js', *dependencies}


def verify_humanities(root):
    directory = root / 'tools/humanities_resources'
    sys.path.insert(0, str(directory))
    try:
        # The generator import must come from the same exact reviewed fixture.
        saved = sys.modules.pop('build_resources', None)
        spec = importlib.util.spec_from_file_location('glv3_humanities_check', directory / 'check_resources.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        report = module.check(root, root)
        if report['result'] != 'PASS' or report['existing_routes_preserved'] != 30 or report['additional_coverage_claimed'] != 0:
            raise ValueError('Humanities preservation verdict is incomplete')
    finally:
        sys.path.pop(0)
        sys.modules.pop('build_resources', None)
        if saved is not None: sys.modules['build_resources'] = saved


def public_label_paths(root, pins):
    manifest = root / LABEL_EDITS
    if not manifest.is_file() or pins.get(LABEL_EDITS) != sha(manifest):
        raise ValueError('Public label amendment is not reviewed')
    changes = json.loads(manifest.read_text())['files']
    source = json.loads((root / SOURCE).read_text())['records']
    expected = {COVER+'/'+r['id']+'.html' for r in source} | {COVER+'/index.html'}
    if {r['path'] for r in changes} != expected or len(changes) != len(expected):
        raise ValueError('Public label changes must name exactly the existing cover HTML pages')
    for row in changes:
        path = root / row['path']
        text = path.read_text()
        if sha(path) != row['afterSha256'] or pins.get(row['path']) != row['afterSha256']:
            raise ValueError('Unreviewed public cover bytes: '+row['path'])
        for edit in reversed(row['edits']):
            start, before, after = edit['start'], edit['before'], edit['after']
            if any(c in before+after for c in '<>') or 'David' not in before or 'David' in after:
                raise ValueError('Label amendment must be visible naming only')
            if text[start:start+len(after)] != after:
                raise ValueError('Public label edit position changed')
            text = text[:start]+before+text[start+len(after):]
        if hashlib.sha256(text.encode()).hexdigest() != row['beforeSha256']:
            raise ValueError('Content changed beyond approved public labels: '+row['path'])
    return expected


def judge(root, changes, base=None):
    relevant = [(status, path) for status, path in changes if protected(path)]
    if not relevant:
        return []
    errors = []
    try:
        pins = pin_map(root)
        if any(path in SUGAR_REPLACEMENTS for _, path in relevant):
            if base is None:
                return ['Sugar replacements require the actual comparison base']
            errors.extend(sugar_replacement_errors(root, relevant, pins, git_before_entries(root, base)))
            if errors:
                return errors
        cover_paths = explicit_cover_paths(root)
        label_paths = public_label_paths(root, pins)
        for status, rel in relevant:
            if rel in SHELVES:
                if status not in ('A', 'M') or not (root / rel).is_file() or pins.get(rel) != sha(root / rel):
                    errors.append('reviewed shelf bytes or change type differ: ' + rel)
            elif rel in SUGAR_REPLACEMENTS:
                # Already checked as one exact seven-file M transaction above.
                pass
            elif rel.startswith(SCIENCE_PACKS) and rel in pins:
                # Owner-requested 6 September additive BUILD/GROW downloads.
                # Every individual file has an explicit reviewed digest; the
                # prefix alone never admits a file or an existing-file edit.
                if status != 'A' or not (root / rel).is_file() or pins[rel] != sha(root / rel):
                    errors.append('Science teaching pack must be an exact reviewed addition: ' + rel)
            elif rel in cover_paths:
                # This ruling installs new cover resources. It does not permit
                # edits, deletions or renames of existing lesson payloads.
                if status != 'A' and not (status == 'M' and rel in label_paths):
                    errors.append('cover change is neither additive nor an exact approved public-label edit: ' + rel)
            else:
                errors.append('original GLV3 protected-path fence rejected: ' + rel)
        if errors:
            return errors
        # Bind the validator and all sources before invoking it. A manifest
        # cannot enlarge this exception or rewrite the checked old-route hashes.
        for rel in (*BOUND_INPUTS, COVER + '/index.html'):
            path = root / rel
            if not path.is_file() or pins.get(rel) != sha(path):
                errors.append('unreviewed cover validation input: ' + rel)
        if not errors:
            verify_humanities(root)
    except (AssertionError, ValueError, OSError, KeyError, TypeError, ImportError, subprocess.CalledProcessError) as exc:
        errors.append('reviewed catalogue/cover proof failed: ' + str(exc))
    return errors


def git_changes(root, base):
    command = ['git', 'diff', '--name-status', '-z', '--no-renames', base + '...HEAD', '--', *PROTECTED]
    raw = subprocess.check_output(command, cwd=root).decode('utf-8').split('\0')
    if raw[-1] == '': raw.pop()
    if len(raw) % 2:
        raise ValueError('git returned an incomplete changed-path record')
    rows = list(zip(raw[::2], raw[1::2]))
    if any(status not in ('A', 'M', 'D', 'T', 'U', 'X', 'B') for status, _ in rows):
        raise ValueError('unexpected git change status')
    return rows


def controls(root):
    rows = []
    def check(name, condition):
        if not condition: raise AssertionError(name)
        rows.append({'name': name, 'status': 'PASS'})
    additions = [('A', p) for p in sorted(explicit_cover_paths(root))]
    reviewed = [('A', p) for p in SHELVES] + additions
    check('Exact reviewed shelves and all manifest-bound cover additions pass', not judge(root, reviewed))
    check('An unrelated generated-tree change does not expand protected-path permissions', not judge(root, [('M', 'GROW_Estate_v3/index.html')]))
    source = json.loads((root / SOURCE).read_text())
    retained = {item['path'] for record in source['records'] for item in record['existing_routes']}
    check('All 30 retained Humanities/RE lesson paths reject modifications', len(retained) == 30 and all(judge(root, [('M', path)]) for path in retained))
    science = 'Science_Teesside/Build/SCI_B_W3_Backbones.html'
    check('An existing Science lesson path remains protected', (root / science).is_file() and bool(judge(root, [('M', science)])))
    for prefix in PROTECTED:
        check('Original protected prefix remains fenced: ' + prefix, bool(judge(root, [('A', prefix + '/unreviewed.html')])))
    check('An undeclared cover file is rejected', bool(judge(root, [('A', COVER + '/unreviewed.html')])))
    check('A modification of an existing cover file is not an additive installation', bool(judge(root, [('M', COVER+'/resource.css')])))
    check('A deleted shelf is rejected', bool(judge(root, [('D', SHELVES[0])])))
    check('Rename-as-delete/add cannot move a retained lesson into the cover exception', bool(judge(root, [('D', sorted(retained)[0]), additions[0]])))
    science_additions = [('A', rel) for rel in pin_map(root) if rel.startswith(SCIENCE_PACKS) and rel not in SUGAR_REPLACEMENTS]
    if science_additions:
        check('Exact individually pinned Science teaching files pass as additions', not judge(root, science_additions))
        first = science_additions[0][1]
        check('An existing Science teaching download remains protected from replacement', bool(judge(root, [('M', first)])))
        check('A Science teaching download cannot be deleted', bool(judge(root, [('D', first)])))
        check('An unlisted Science teaching file is rejected', bool(judge(root, [('A', SCIENCE_PACKS+'unreviewed.pptx')])))
    with tempfile.TemporaryDirectory(prefix='glv3-reviewed-boundary-') as temp:
        fixture = Path(temp)
        files = {*explicit_cover_paths(root), *SHELVES, *retained, *BOUND_INPUTS, *(rel for _, rel in science_additions),
                 'tools/verify_cross_estate_unification.py', 'index.html'}
        for rel in files:
            target = fixture / rel; target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(root / rel, target)
        check('Disposable fixture is initially accepted by the real validators', not judge(fixture, reviewed))
        if science_additions:
            check('Disposable Science fixture is initially accepted', not judge(fixture, science_additions))
        def mutate(rel, replacement, message, changes=reviewed):
            path = fixture / rel; original = path.read_bytes()
            try:
                changed = replacement(original); check(message + ' sabotage changes bytes', changed != original); path.write_bytes(changed)
                check(message, bool(judge(fixture, changes)))
            finally: path.write_bytes(original)
        if science_additions:
            native = next(rel for _, rel in science_additions if rel.endswith('.pptx'))
            mutate(native, lambda b: b + b'changed', 'Changed native Science bytes fail without re-pinning', science_additions)
        mutate(SHELVES[0], lambda b: b + b'<!-- unreviewed -->', 'Shelf byte drift is rejected')
        mutate(SOURCE, lambda b: b + b'\n', 'A changed source manifest cannot redefine retained lessons')
        mutate(DOWNLOADS, lambda b: b + b'\n', 'A changed download manifest cannot enlarge the allowed set')
        page = next(path for path in sorted(explicit_cover_paths(root)) if re.search(r'/BH_W3\.html$', path))
        mutate(page, lambda b: b.replace(b'data-minutes="3"', b'data-minutes="43"', 1), 'Changed teaching minutes are rejected by the shared Humanities validator')
        native = next(row['path'] for row in json.loads((root / DOWNLOADS).read_text())['dependencies'] if row['path'].endswith('.pdf'))
        mutate(native, lambda b: b + b'\n', 'Native download byte drift is rejected')
        mutate(sorted(retained)[0], lambda b: b + b'\n', 'Retained Humanities content drift is rejected even if omitted from the supplied diff')
    rows.extend(sugar_controls(root))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--base', required=True)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args(); root = args.root.resolve()
    try:
        changes = git_changes(root, args.base)
        errors = judge(root, changes, args.base)
        report = {'status': 'FAIL' if errors else 'PASS', 'protectedChanges': len(changes), 'errors': errors}
        if args.self_test:
            report['controls'] = controls(root)
            report['controlCount'] = len(report['controls'])
        print(json.dumps(report, indent=2))
        return 1 if errors else 0
    except (AssertionError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        print('[FAIL] change boundary could not be verified: ' + str(exc)); return 1


if __name__ == '__main__': raise SystemExit(main())
