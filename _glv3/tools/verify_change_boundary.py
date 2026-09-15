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
SUGAR_REPLACEMENTS = {'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html': {'beforeGitBlob': 'bd1d6da15f32efc7ce068e9f4e846bb7038bb80a', 'afterSha256': '8594f15916211ff3de03bb928b2de3756bff0dbe8c52adabd3e4cccfda9d42a3', 'bytes': 628443}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label.pdf': {'beforeGitBlob': 'abd9261ff123775b2af979761d08dbe1ea5e2662', 'afterSha256': 'fc9ba726c94177000d872c28e3c7db3812c268d6552e936a316c38654a95a0dd', 'bytes': 431296}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label.pptx': {'beforeGitBlob': 'aff41a6c51c8eb21fbce611316590ed255be7078', 'afterSha256': 'd93b814710bcf57ece951ba0aaf82ed41320247571ec48147e26a5423b3c07e3', 'bytes': 158524}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Pupil.docx': {'beforeGitBlob': '81015f010d39c157bdd7f5c3f453ad2e6912c11e', 'afterSha256': 'be71bc9be6c6d9c23383ee35ec739df80830ad5e336e7095098deaf3003a6d64', 'bytes': 42521}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Pupil.pdf': {'beforeGitBlob': 'a1e81df065fe01d01d0eda19549ec33883bc1a27', 'afterSha256': '25544b193963f552a1511ac17bd5b5353cbeeca71d6788ac4deddbc61f905dc4', 'bytes': 170636}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Teacher.docx': {'beforeGitBlob': 'b111d7326d3bcad325167f2357b7f3741917dad1', 'afterSha256': '033a59447d5b42ea990dd0737c93db99a717e9055307f1c6b6ebe5bf7262c9b3', 'bytes': 43099}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Teacher.pdf': {'beforeGitBlob': '3fd844034e225e1c404a5cb50985951a0b4406ec', 'afterSha256': 'a4f9888e6b742339d54ba9128da824904b65e786054e8820d60df9980fa4af86', 'bytes': 114441}}

# EDU-Q1 GROW W3 Friction: the reviewed paired lesson, its two resource pages,
# the Week 3 native companions, START_HERE files, the pack records and the seven
# archives that carry Week 3 content, plus the download hub. Written by
# tools/grow_resources/admit_w3_friction.py; never a directory-wide permission.
GROW_W3_REVIEW_BASE = '929cf731173aeca8c9941cecd76cb350387499d1'
# BEGIN GROW W3 REPLACEMENTS
GROW_W3_REPLACEMENTS = {'Science_Teesside/Grow/SCI_G_W3_Friction.html': {'beforeGitBlob': '472809373600a6f8529ccb59faa05939cd4de58a', 'afterSha256': '508f1967b6481671dafb149d7177b620b194074312cee0dbdd30553c166b634a', 'bytes': 414467}, 'Science_Teesside/Grow/resources/GS_W3A.html': {'beforeGitBlob': '7be51ce3f70cfb8b6cdfea586d1ab3a34f85d577', 'afterSha256': 'e5bfaf2bc70912aeb59fe9a2eb1032d86c7a473a1059ba782fee1be7b3513dc1', 'bytes': 8345}, 'Science_Teesside/Grow/resources/GS_W3B.html': {'beforeGitBlob': 'a8cd838436ead513a47449c0ec5c264153835c72', 'afterSha256': 'fb6580bfd1e02d82627d60e1c2e08c3a34b227d0cbe760545502a8e51ab91208', 'bytes': 9105}, 'Science_Teesside/Teaching_Packs/GROW/DOWNLOAD_INDEX.json': {'beforeGitBlob': '15be31339565a36e14b231ea7ee92f72e3de2044', 'afterSha256': 'f4838737eba7f6db77bf5d8741cdaf046a21d15159da70cbc550030824cddd63', 'bytes': 55385}, 'Science_Teesside/Teaching_Packs/GROW/SHA256SUMS.txt': {'beforeGitBlob': '50b80da129c8715b6bb42c50c26f0300e47340e1', 'afterSha256': '758dcbdd646219106ef7c416034c24e5e89da1423df5393621eef985e0c4a3a1', 'bytes': 41955}, 'Science_Teesside/Teaching_Packs/GROW/SOURCE_MANIFEST.json': {'beforeGitBlob': '9991c027829d89569b88fc71ee895f82bd275748', 'afterSha256': '78b1d12b1b817c05a5743688a0946b855a8c211c954d7b29ba41575a2e2f7156', 'bytes': 31944}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3-W7_DOCX_Collection.zip': {'beforeGitBlob': 'a809670f0f3bfece5943f01d7685957915891c27', 'afterSha256': '2482706e4f9c7e192287acfd02e7c09381597a1a9fc772c9d39fe630eba5a3aa', 'bytes': 934810}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3-W7_PDF_Collection.zip': {'beforeGitBlob': '695654bf6d71a68bf529f828df8140b7b551f6c9', 'afterSha256': 'b3116412bb38368b96c0236e2b41902deb76e96461f1ca1c3fb134d878f842f0', 'bytes': 4897326}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3-W7_PPTX_Collection.zip': {'beforeGitBlob': '9acea60c01a9bcd69998aa0e26ba8aaa83c4bb53', 'afterSha256': '592f59c2ccae4f9531af5296eb30064c8fee92c44ba2b896db8038cf2a93dce8', 'bytes': 11610595}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3A.zip': {'beforeGitBlob': 'b640797c2be2729b1d6f70c7f9b3f85083ee0d28', 'afterSha256': '2596818e45a67ea1b306f7c9287fa70795ab8142c6c93b9e63e1f99e1a4e5b22', 'bytes': 3047141}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3B.zip': {'beforeGitBlob': 'fbc60fd5f192deeaf7f2086bd04630cf9ab4d669', 'afterSha256': '4fedd9c4a162c3e712a327afd85554b19c55ad1f5b8cacea057b0fdecbb305ed', 'bytes': 2887914}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week3.zip': {'beforeGitBlob': 'ac91b2d4ef3a2623584b12d4d4fdb58e299a615c', 'afterSha256': '5a8606a41a4b9e5a7accdf3ee730d727b709d92734f669d07a1e84324fa8035b', 'bytes': 5628922}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Weeks3-7_Teaching_Pack.zip': {'beforeGitBlob': '9a2ee88e2a3b3ebc1f83b7d85c2bef742c4398e4', 'afterSha256': 'd8b6f0ce61e7925089aadbc66b63756316268c9c2934575ccdf18e74cb41e6ce', 'bytes': 17481035}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_Science_Autumn1_W3A_Friction.pdf': {'beforeGitBlob': '448f78231000d204c3da1e26921a677a929d4b83', 'afterSha256': '0e57d93e45bf29236754a735e42f6d2ae923aa1a23c65ebe9ed19041347ced7d', 'bytes': 342104}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_Science_Autumn1_W3A_Friction.pptx': {'beforeGitBlob': '7ad84a84ba5d20e6da8a5677d684a206f94cf9ce', 'afterSha256': '13dceb4a32f65165df9353349a69c87465e7f33b9f941036f8f714fd10a9f9da', 'bytes': 2038042}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.docx': {'beforeGitBlob': '9b06c7bcb266853c3eb9fce55667b5799ed3222a', 'afterSha256': '9f8afdf8df90eb845d3ea352d36b9bd19dd192a6c040883fe70957eb8be487de', 'bytes': 58755}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.pdf': {'beforeGitBlob': '97b9364c72863f6efc262ad1d50828deeb5687b3', 'afterSha256': '856691efece9acaae40a529f949f3d26567345c8f658de9e26eab1bbbdc585cb', 'bytes': 249351}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.docx': {'beforeGitBlob': '8a37234fb19d83349f6d311daa261ed0fc35b1b6', 'afterSha256': '9da8a692bd1ad6b4a040e4b4a970275c90577cbaf73342492d1908148c5d8717', 'bytes': 47511}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.pdf': {'beforeGitBlob': '46caf3569c44878a024acb7fe4694c4a6eeaac44', 'afterSha256': '08c926202671c6b2c25778d5d2dcf2f99a473dd704201f0ef9a58e3a359b18f9', 'bytes': 217509}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/START_HERE.txt': {'beforeGitBlob': 'c4f568f594b12fd1ad55204e9192a3824119c57b', 'afterSha256': 'b5c46c92125be91cb86f64c5969ad8378ab3948b41a82e7be01e7378ccdfc81c', 'bytes': 838}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test.pdf': {'beforeGitBlob': 'be31fba447c41634bbac03a61a388924895072a4', 'afterSha256': '1ce1ba083eb62b521368b3c5863c098733ae7d677a1e7c0e641b8e0fd7681d3a', 'bytes': 320920}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test.pptx': {'beforeGitBlob': '778ea423b30e885e32add933dc789cfd39e75271', 'afterSha256': '3049816d76009ebe3ad1b609e9ca22ec54c3abc82d3e8037b012386759ba278b', 'bytes': 2027282}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Pupil.docx': {'beforeGitBlob': '80053558ef4bde01454927512a375ca7944a016b', 'afterSha256': 'e4333309ef2e2dcf587385063c8e43eee56c3a285089b4f749580124d8c128ea', 'bytes': 41418}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Pupil.pdf': {'beforeGitBlob': '92123f2f8a5bf90f750e4102410148da821f307e', 'afterSha256': '7ddb70eb886f743fd0813b5d581435b36bdfb1a5813e23a6cb6f3b95ccdfee8b', 'bytes': 127894}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Teacher.docx': {'beforeGitBlob': '0279a5cee651b1d4e173b605e38124a5936dbfc3', 'afterSha256': 'c0e2ae5adaff89fa05b28e389f7d422e0f638ca9edd33313da61d57d258732cb', 'bytes': 43338}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Teacher.pdf': {'beforeGitBlob': 'f6628955910b4beb057263eafe1dd4849aa86131', 'afterSha256': 'c9c7bf0a6dc4b4a69c1df89bf7fc3a2fdd73c57828ecb0619688611b52a61d5d', 'bytes': 147273}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/START_HERE.txt': {'beforeGitBlob': '473e2fe98c17f732f9507405c26ae7e560c5639f', 'afterSha256': '70a87773d7f0bc53b67cc1023263f2837ec473ceffc6ec1fc79b82823805c756', 'bytes': 665}, 'Science_Teesside/Teaching_Packs/index.html': {'beforeGitBlob': '0e8cab0cb461779787e6fef503788c3b38bd51f3', 'afterSha256': '33f5021dbb05a35048447a3b79f144f265e3dd8209a8bbd96a916b3fd8b7fc81', 'bytes': 73131}}
# END GROW W3 REPLACEMENTS

# Each transaction is judged on its own: every member present as exactly one
# modification, previous identities from the actual merge base, exact bytes and
# a matching owner-reviewed catalogue admission for every member.
REPLACEMENT_TRANSACTIONS = {
    'Sugar': (SUGAR_REVIEW_BASE, SUGAR_REPLACEMENTS),
    'GROW W3 Friction': (GROW_W3_REVIEW_BASE, GROW_W3_REPLACEMENTS),
}
ALL_REPLACEMENTS = {rel: name for name, (_, files) in REPLACEMENT_TRANSACTIONS.items() for rel in files}


def git_before_entries(root, base, paths=None):
    # Match git_changes' triple-dot semantics; do not trust a supplied manifest
    # for the previous file identities.
    merge_base = subprocess.check_output(['git', 'merge-base', base, 'HEAD'], cwd=root).decode().strip()
    raw = subprocess.check_output(['git', 'ls-tree', '-z', merge_base, '--', *sorted(paths if paths is not None else SUGAR_REPLACEMENTS)], cwd=root)
    result = {}
    for record in raw.decode().split('\0'):
        if not record:
            continue
        fields, path = record.split('\t', 1)
        mode, kind, blob = fields.split()
        result[path] = (mode, kind, blob)
    return result


def replacement_errors(name, files, root, changes, pins, before_entries):
    selected = [(status, rel) for status, rel in changes if rel in files]
    if not selected:
        return []
    if len(selected) != len(files) or {rel for _, rel in selected} != set(files):
        return [name + ' replacement must contain exactly the ' + number_word(len(files)) + ' reviewed file modifications']
    errors = []
    for status, rel in selected:
        reviewed = files[rel]
        path = root / rel
        if status != 'M':
            errors.append(name + ' replacement is not a modification: ' + rel)
        if before_entries.get(rel) != ('100644', 'blob', reviewed['beforeGitBlob']):
            errors.append(name + ' previous file identity or mode differs: ' + rel)
        if path.is_symlink() or not path.is_file() or path.resolve().is_relative_to(root.resolve()) is False:
            errors.append(name + ' replacement must be a regular file inside the tree: ' + rel)
        elif path.stat().st_size != reviewed['bytes'] or sha(path) != reviewed['afterSha256']:
            errors.append(name + ' replacement bytes differ: ' + rel)
        if pins.get(rel) != reviewed['afterSha256']:
            errors.append(name + ' replacement lacks matching owner-reviewed catalogue admission: ' + rel)
    return errors


def number_word(n):
    return {7: 'seven'}.get(n, str(n))


def sugar_replacement_errors(root, changes, pins, before_entries):
    return replacement_errors('Sugar', SUGAR_REPLACEMENTS, root, changes, pins, before_entries)


def sugar_controls(root, proposed_pins=None):
    return transaction_controls(root, 'Sugar', proposed_pins)


def transaction_controls(root, name, proposed_pins=None):
    # CI uses the real reviewed pin map. The optional map lets a review harness
    # exercise the proposed transaction before paired admissions are staged;
    # such a run is conditional evidence, never a production gate pass.
    base, files = REPLACEMENT_TRANSACTIONS[name]
    if not files:
        return []
    errors_for = lambda *a: replacement_errors(name, files, *a)
    pins = pin_map(root) if proposed_pins is None else proposed_pins
    changes = [('M', rel) for rel in sorted(files)]
    before = git_before_entries(root, base, files)
    rows = []
    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        rows.append({'name': name, 'status': 'PASS'})
    check(name + ': all reviewed replacements pass the bounded rule', not errors_for(root, changes, pins, before))
    for rel in sorted(files):
        missing_pin = dict(pins); missing_pin.pop(rel, None)
        check(name + ' missing owner admission rejected: ' + rel, bool(errors_for(root, changes, missing_pin, before)))
        wrong_before = dict(before); wrong_before[rel] = ('100644', 'blob', '0' * 40)
        check(name + ' wrong previous identity rejected: ' + rel, bool(errors_for(root, changes, pins, wrong_before)))
        wrong_mode = dict(before); wrong_mode[rel] = ('120000', 'blob', files[rel]['beforeGitBlob'])
        check(name + ' previous symlink mode rejected: ' + rel, bool(errors_for(root, changes, pins, wrong_mode)))
        for status in ('A', 'D', 'T'):
            altered = [(status if path == rel else kind, path) for kind, path in changes]
            check(name + ' wrong change type '+status+' rejected: ' + rel, bool(errors_for(root, altered, pins, before)))
        check(name + ' omitted replacement rejected: ' + rel, bool(errors_for(root, [(kind, path) for kind, path in changes if path != rel], pins, before)))
    check(name + ' duplicate replacement rejected', bool(errors_for(root, changes + [changes[0]], pins, before)))
    with tempfile.TemporaryDirectory(prefix='replacement-proof-') as temp:
        fixture = Path(temp)
        for rel in files:
            target = fixture / rel; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / rel, target)
        check(name + ' actual candidate bytes pass in disposable fixture', not errors_for(fixture, changes, pins, before))
        for rel in sorted(files):
            path = fixture / rel; original = path.read_bytes()
            try:
                path.write_bytes(original + b'changed')
                check(name + ' changed candidate bytes rejected: ' + rel, bool(errors_for(fixture, changes, pins, before)))
                # Even changing the caller's catalogue digest cannot change the
                # independent exact replacement review.
                repinned = dict(pins); repinned[rel] = sha(path)
                check(name + ' repinned changed bytes still rejected: ' + rel, bool(errors_for(fixture, changes, repinned, before)))
                path.unlink()
                check(name + ' missing candidate file rejected: ' + rel, bool(errors_for(fixture, changes, pins, before)))
                path.symlink_to(root / rel)
                check(name + ' candidate symlink rejected: ' + rel, bool(errors_for(fixture, changes, pins, before)))
            finally:
                if path.is_symlink(): path.unlink()
                path.write_bytes(original)
        check(name + ' all sabotage was restored', not errors_for(fixture, changes, pins, before))
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
        for name, (_, files) in REPLACEMENT_TRANSACTIONS.items():
            if any(path in files for _, path in relevant):
                if base is None:
                    return [name + ' replacements require the actual comparison base']
                errors.extend(replacement_errors(name, files, root, relevant, pins, git_before_entries(root, base, files)))
        if errors:
            return errors
        cover_paths = explicit_cover_paths(root)
        label_paths = public_label_paths(root, pins)
        for status, rel in relevant:
            if rel in SHELVES:
                if status not in ('A', 'M') or not (root / rel).is_file() or pins.get(rel) != sha(root / rel):
                    errors.append('reviewed shelf bytes or change type differ: ' + rel)
            elif rel in ALL_REPLACEMENTS:
                # Already checked as one exact M transaction above.
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
    science_additions = [('A', rel) for rel in pin_map(root) if rel.startswith(SCIENCE_PACKS) and rel not in ALL_REPLACEMENTS]
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
    for name in REPLACEMENT_TRANSACTIONS:
        rows.extend(transaction_controls(root, name))
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
