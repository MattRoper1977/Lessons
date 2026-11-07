#!/usr/bin/env python3
"""The four renamed Play games keep their old file as a redirect stub, so old
links and the published search index (which still names the old routes until
the Site rename lands) reach the new page. A stub carries no game and no HUD, so
data/hud-coverage.json declares it; this script is the verifier that declaration
cites. Each stub must: be small, carry no script, set noindex, meta-refresh at
once to exactly its renamed page, offer a visible link to the same page, and
point at a page that exists and carries the HUD script tag."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUBS = {
    'Games/voxelcraft.html': 'Games/Block_Builder.html',
    'Games/WorldCup_ThreeLions_Final.html': 'Games/Cup_Final.html',
    'Games/WorldCup_v3_MatchDirector.html': 'Games/Match_Director.html',
    'Games/WorldCup_v5_Showdown.html': 'Games/Cup_Showdown.html',
}
HUD_TAG = re.compile(r'<script\b[^>]*\bsrc="/hud\.js"[^>]*>')


def errors(root=ROOT):
    out = []
    for stub, target in STUBS.items():
        s, t = root / stub, root / target
        if not s.is_file():
            out.append(f'{stub}: missing'); continue
        text = s.read_text('utf-8')
        url = '/Lessons/' + target
        if len(text) > 2048:
            out.append(f'{stub}: larger than a stub ({len(text)} bytes)')
        if re.search(r'<script', text, re.I):
            out.append(f'{stub}: carries a script')
        if not re.search(r'<meta name="robots" content="noindex">', text):
            out.append(f'{stub}: no noindex')
        if f'<meta http-equiv="refresh" content="0; url={url}">' not in text:
            out.append(f'{stub}: does not refresh at once to {url}')
        if f'<a href="{url}">' not in text:
            out.append(f'{stub}: no visible link to {url}')
        if not t.is_file():
            out.append(f'{stub}: target {target} does not exist')
        elif not HUD_TAG.search(t.read_text('utf-8')):
            out.append(f'{stub}: target {target} carries no HUD script')
    return out


def self_test():
    import shutil, tempfile
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        for rel in list(STUBS) + list(STUBS.values()):
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, tmp / rel)
        assert not errors(tmp), errors(tmp)
        stub = tmp / 'Games/voxelcraft.html'
        good = stub.read_text('utf-8')
        for name, bad in [('wrong target', good.replace('Block_Builder', 'Voxel_Frontier')),
                          ('a script', good.replace('<body>', '<body><script>x()</script>')),
                          ('no noindex', good.replace(' content="noindex"', ' content="index"'))]:
            stub.write_text(bad, 'utf-8')
            assert errors(tmp), name
            print(f'  [PASS] red control: {name} is caught')
        stub.write_text(good, 'utf-8')
        (tmp / 'Games/Cup_Final.html').unlink()
        assert errors(tmp), 'missing target'
        print('  [PASS] red control: a missing target is caught')


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        self_test()
    problems = errors()
    for p in problems:
        print('  [FAIL]', p)
    print('PASS: 4 rename stubs redirect to HUD-wired pages' if not problems else f'FAIL: {len(problems)} problem(s)')
    sys.exit(1 if problems else 0)
