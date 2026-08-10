"""§3 / §3.1 — lay the repaired packs into the repository.

    python3 _sciv3/tools/install.py <staging-lessons> <staging-baseline>

Science_Teesside/{Grow,Build,Launch}/v3_40min/   parallel 40-minute routes
_sciv3/{grow,build,launch}/                      the three doc sets, kept apart
Baseline_Weeks/                                  the public baseline pack
"""
import sys, os, re, shutil

STAGE, BASE = sys.argv[1], sys.argv[2]
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PACKS = {'grow': 'Grow', 'build': 'Build', 'launch': 'Launch'}
DOCS = {'README.md', 'POLICY_ALIGNMENT.md', 'SOW_AND_POLICY_ALIGNMENT.md'}

# A9 step 4 — the LAUNCH curriculum block, corrected without inventing baseline content.
SOW_OLD = """Uploaded LAUNCH KS4 2026/27 SOW:
- Aut1 W1: eukaryotic and prokaryotic cells
- W2: microscope core practical
- W3: magnification"""
SOW_NEW = """Uploaded LAUNCH KS4 2026/27 SOW, corrected for the baseline weeks:
- Aut1 W1: baseline assessment (delivered separately, not in this repo)
- W2: baseline assessment (delivered separately, not in this repo)
- W3: magnification — **the taught sequence starts here**"""

SOW_NOTE = """

## Autumn 1 W1–W2 are baseline weeks

No science was taught in W1 or W2; they are baseline assessment weeks. This pack originally
described a taught W2 (microscope core practical) and retrieved it at W3L1. That claim has been
removed from the lesson, the hub and the manifest, and the W3L1 arrival now opens from what pupils
already know.

**Nothing here states what the baseline covered.** The baseline runs on PythonAnywhere and is not
in this repository, so no lesson cites it as prior learning and no baseline topic is named. A
separate public `Baseline_Weeks/` pack exists in this repo; it is a *different instrument* from the
PythonAnywhere baseline and is not what any given pupil sat.
"""


def main():
    n = 0
    for pack, Cap in PACKS.items():
        dst = os.path.join(REPO, 'Science_Teesside', Cap, 'v3_40min')
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        os.makedirs(dst)
        docdst = os.path.join(REPO, '_sciv3', pack)
        os.makedirs(docdst, exist_ok=True)
        for name in sorted(os.listdir(os.path.join(STAGE, pack))):
            src = os.path.join(STAGE, pack, name)
            if name in DOCS:
                t = open(src, encoding='utf-8').read()
                if name == 'SOW_AND_POLICY_ALIGNMENT.md':
                    assert SOW_OLD in t, 'SOW curriculum block anchor missing'
                    t = t.replace(SOW_OLD, SOW_NEW).rstrip() + SOW_NOTE
                open(os.path.join(docdst, name), 'w', encoding='utf-8').write(t)
            else:
                shutil.copy2(src, os.path.join(dst, name))
                n += 1
        print(f'  {pack:7s} -> Science_Teesside/{Cap}/v3_40min  '
              f'({len(os.listdir(dst))} files)  docs -> _sciv3/{pack}')

    bdst = os.path.join(REPO, 'Baseline_Weeks')
    if os.path.isdir(bdst):
        shutil.rmtree(bdst)
    shutil.copytree(BASE, bdst)
    print(f'  baseline -> Baseline_Weeks ({len(os.listdir(bdst))} files)')
    print(f'\n{n} route files installed')


if __name__ == '__main__':
    main()
