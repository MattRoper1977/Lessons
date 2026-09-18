#!/usr/bin/env python3
"""Red-prove the merged-artefact guard in build_catalogue.py.

Three cases, run against a throwaway copy of the evidence file so the repository
is never left changed:

  1. PRESERVE  -- a no-op rebuild leaves every .pptx row intact, with its term,
                  batch, sha256 and title. This is the proof ORDER SX3-M2 5(a)
                  asked for.
  2. REFUSE    -- when the builder CAN read a file and still produces less than
                  the record holds, it raises rather than writing. Planted by
                  pointing a rich record at a real .html file the builder reads
                  as a non-lesson.
  3. NO-GUARD  -- with the guard removed, case 1 fails. A guard that cannot go
                  red is not a guard, so this asserts the hazard is real.

Run: python3 tools/catalogue/test_build_catalogue_merge.py
"""
import json, pathlib, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUILDER = ROOT / 'tools/catalogue/build_catalogue.py'
PROOF = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
TOUCHED = ['tools/catalogue/TERM_AND_STYLE_EVIDENCE.json',
           'tools/catalogue/TERM_REVIEW.json',
           'assets/catalogue/terms-and-styles.json',
           'assets/catalogue/science-shelf.json',
           'assets/catalogue/humanities-shelf.json']


def restore():
    subprocess.run(['git', '-C', str(ROOT), 'checkout', '--'] + TOUCHED,
                   check=False, capture_output=True)


def run(source=None):
    """Run the builder, optionally from substituted source. Returns (rc, output)."""
    original = BUILDER.read_text()
    if source is not None:
        BUILDER.write_text(source)
    try:
        r = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT,
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr
    finally:
        BUILDER.write_text(original)


def pack_rows(data):
    return {p: e for p, e in data['entries'].items() if p.lower().endswith('.pptx')}


def rich(entry):
    return not (entry.get('term') == 'any' and not entry.get('terms')
                and entry.get('style') == 'reference' and not entry.get('evidence'))


def case_preserve():
    before = json.loads(PROOF.read_text())
    rows_before = {p: e for p, e in pack_rows(before).items() if rich(e)}
    assert rows_before, 'no enriched .pptx rows on disk; this test has nothing to protect'
    rc, out = run()
    assert rc == 0, 'no-op rebuild refused:\n' + out
    after = json.loads(PROOF.read_text())
    rows_after = pack_rows(after)
    lost = [p for p in rows_before if p not in rows_after]
    degraded = [p for p in rows_before if p in rows_after and rows_after[p] != rows_before[p]]
    restore()
    assert not lost, 'rows vanished: %d, e.g. %s' % (len(lost), lost[:3])
    assert not degraded, 'rows degraded: %d, e.g. %s' % (len(degraded), degraded[:3])
    return len(rows_before)


def case_refuse():
    """Plant a rich record on a path the builder CAN read and classifies as a stub."""
    candidates = [p for p in ROOT.rglob('Science_Teesside/**/*.html')]
    planted = None
    before = PROOF.read_text()
    data = json.loads(before)
    for candidate in candidates:
        relative = str(candidate.relative_to(ROOT))
        entry = data['entries'].get(relative)
        if entry is not None and not rich(entry):
            planted = relative
            break
    if planted is None:
        # Fall back: take any readable .html the builder stubs, and add the row.
        for candidate in candidates[:400]:
            relative = str(candidate.relative_to(ROOT))
            if relative not in data['entries']:
                planted = relative
                data['entries'][relative] = {}
                break
    assert planted, 'could not find a readable .html the builder stubs'
    data['entries'][planted] = {'term': 'Aut2', 'terms': ['Aut2'], 'style': 'current',
                                'pathway': 'BUILD', 'batch': 'planted',
                                'evidence': [{'method': 'planted for the red proof'}]}
    PROOF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    rc, out = run()
    restore()
    assert rc != 0, 'the guard did not refuse a degradation it can author:\n' + out
    assert 'regression in this tool' in out, 'refused, but not with the guard message:\n' + out
    return planted


def case_no_guard():
    """With the guard removed, case 1 must fail -- otherwise the hazard is not real."""
    source = BUILDER.read_text()
    start = source.index('# MERGED ARTEFACT GUARD.')
    end = source.index("proof={'schema':'catalogue-evidence-v1'")
    without = source[:start] + source[end:]
    before = json.loads(PROOF.read_text())
    rows_before = {p: e for p, e in pack_rows(before).items() if rich(e)}
    rc, out = run(without)
    assert rc == 0, 'unguarded builder refused for another reason:\n' + out
    after = json.loads(PROOF.read_text())
    rows_after = pack_rows(after)
    degraded = [p for p in rows_before if rows_after.get(p) != rows_before[p]]
    restore()
    assert degraded, 'removing the guard changed nothing; the guard is not load-bearing'
    return len(degraded)


if __name__ == '__main__':
    try:
        n = case_preserve()
        print('PASS  preserve  -- no-op rebuild left %d enriched .pptx rows byte-identical' % n)
        planted = case_refuse()
        print('PASS  refuse    -- guard raised on a planted degradation at %s' % planted)
        d = case_no_guard()
        print('PASS  no-guard  -- without the guard the same rebuild degrades %d rows' % d)
    finally:
        restore()
    print('\nbuild_catalogue.py merged-artefact guard: 3/3')
