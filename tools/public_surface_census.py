#!/usr/bin/env python3
"""CX2 §10.1 items 9 and 10 — the product-name census (R10) and the pupil-data-field census (R11).

    public_surface_census.py --built <publication tree> [--json OUT]
    public_surface_census.py --root <checkout>          [--json OUT]
    public_surface_census.py --self-test

WHY THIS EXISTS. Two per-transaction tools already assert the R10 wording, each over its own
handful of files: tools/science_teaching_packs/cx2_sugar_r10.py and tools/rw1/cx2_lane_d.py.
Both re-assert their OWN edits and neither can find a fourth occurrence anywhere else, so the
estate has had the rule without an instrument. This generalises their method — their regex,
unchanged — to every public surface, and adds the R11 limb, which had no instrument at all.
The banned expressions here are taken from those committed tools, not invented.

A DETECTOR HAS TO NAME WHAT IT FORBIDS. This file therefore contains the banned product names.
That is not a breach of the rule it enforces: the rule is that no PUBLIC file carries them, and
tools/ is not published — the published trees carry exactly two paths under tools/
(education-lessons/tools/artsaward/SLOTS.json and education-site/tools/index.html), neither of
them a script. Run --built against a real publication tree and the scope is the served bytes.

WHAT IS DELIBERATELY NOT COUNTED, and why, so a green here is not laundered:
  * the bare word PASS. It is an assessment name and also the verdict word every gate in this
    estate prints. Counting it would drown the census in its own output; not counting it is a
    recorded gap, not a silent one.
  * the phrase "reading age". The curriculum policy and LESSON_STANDARD_2026-27.md use it as
    policy language (§4.2 bands). R11 forbids filing a PUPIL'S data, not naming the concept.
  * form fields inside staff-gated regions. R11 is about pupil surfaces; a staff field is
    examined and reported separately rather than counted as a breach.

EXIT. Non-zero when any limb finds something. Every count carries its denominator.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

try:
    from lxml import html as lxml_html
except Exception:
    lxml_html = None

# Taken verbatim from tools/science_teaching_packs/cx2_sugar_r10.py line 54 and
# tools/rw1/cx2_lane_d.py line 213. "Evidence for Learning" added beside them (ruling
# 2026-09-23: the platform's full name is forbidden on every public route, as Earwig and
# Cypher are; the abbreviation alone did not catch it).
PRODUCT_NAMES = re.compile(r'\bEarwig\b|\bCypher\b|\bEfL\b|\bEFL\b|\bEvidence\s+for\s+Learning\b', re.I)
# §4.3 forbids the RECONSTRUCTED marking policy — a Yellow Box the teacher deep-marks and a
# green pen the pupil responds in. The words alone are not the offence: "click each yellow box
# to type" is a user-interface instruction and "pass me the green pen" is a typing exercise.
# So this limb reports CANDIDATES and requires the marking sense before it calls anything a
# breach: the phrase has to sit near deep-marking, responding, or the other half of the pair.
RECONSTRUCTED_FEEDBACK = [re.compile(r'Yellow Box', re.I), re.compile(r'green pen', re.I),
                          re.compile(r'asserted, not verified', re.I)]
MARKING_SENSE = re.compile(r'deep.?mark|responds? in|improvement/redraft|marking polic|green pen|yellow box', re.I)

# R11 is about a PUPIL'S data, not about a text box existing. The estate ships interactive
# studios by design. So the field limb separates fields whose own name, id or label asks for
# something identifying from every other input, and reports the first for a human ruling
# rather than failing on a colour picker.
IDENTITY_FIELD = re.compile(r'\b(pupil|student|surname|forename|first.?name|last.?name|full.?name|d\.?o\.?b|date.?of.?birth|birthday|upn|admission|class|form.?group|tutor.?group|year.?group|score|level|grade|reading.?age)\b', re.I)
# Named assessment instruments. A pupil's score against any of these is pupil data (R11).
ASSESSMENTS = re.compile(r'\bBoxall\b|\bBKSB\b|\bNGRT\b|\bCAT4\b', re.I)

TEXT_SUFFIXES = {'.html', '.htm', '.json', '.js', '.css', '.svg', '.txt', '.md', '.xml', '.webmanifest'}
STAFF_ANCESTOR = ('.//*[@data-mbm-guide]', './/*[@data-audience="staff"]', './/*[contains(concat(" ",normalize-space(@class)," ")," teacher-only ")]')


def surfaces(root: Path):
    for p in sorted(root.rglob('*')):
        if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES:
            yield p


def scan_text(root: Path):
    hits = {'productName': [], 'reconstructedFeedback': [], 'assessmentName': []}
    files = 0
    for p in surfaces(root):
        files += 1
        try:
            text = p.read_text(errors='ignore')
        except Exception:
            continue
        rel = p.relative_to(root).as_posix()
        for name, rx in [('productName', PRODUCT_NAMES), ('assessmentName', ASSESSMENTS)]:
            for m in rx.finditer(text):
                line = text.count('\n', 0, m.start()) + 1
                hits[name].append({'file': rel, 'line': line, 'match': m.group(0),
                                   'context': text[max(0, m.start() - 50):m.end() + 50].replace('\n', ' ')})
        for rx in RECONSTRUCTED_FEEDBACK:
            for m in rx.finditer(text):
                line = text.count('\n', 0, m.start()) + 1
                window = text[max(0, m.start() - 160):m.end() + 160]
                marking = bool(MARKING_SENSE.search(window.replace(m.group(0), '', 1)))
                hits['reconstructedFeedback'].append({'file': rel, 'line': line, 'match': m.group(0),
                                                      'markingSense': marking,
                                                      'context': text[max(0, m.start() - 50):m.end() + 50].replace('\n', ' ')})
    return files, hits


def scan_fields(root: Path):
    """Form fields on pupil surfaces, by DOM ancestry — never by proximity in the source."""
    if lxml_html is None:
        return {'unmeasured': 'lxml is not importable here, so the field limb is UNMEASURED'}
    pages = pupil_fields = staff_fields = 0
    rows = []
    for p in sorted(root.rglob('*.html')):
        pages += 1
        try:
            doc = lxml_html.fromstring(p.read_bytes())
        except Exception:
            continue
        staff = set()
        for xp in STAFF_ANCESTOR:
            for e in doc.xpath(xp):
                for d in e.iter():
                    staff.add(id(d))
        rel = p.relative_to(root).as_posix()
        for e in doc.xpath('//input | //textarea | //select'):
            kind = (e.get('type') or e.tag).lower()
            if kind in ('hidden', 'submit', 'button', 'reset', 'checkbox', 'radio', 'range', 'search'):
                continue
            if id(e) in staff:
                staff_fields += 1
                continue
            pupil_fields += 1
            descriptor = ' '.join(filter(None, [e.get('name'), e.get('id'), e.get('aria-label'), e.get('placeholder'),
                                                e.get('autocomplete')]))
            if IDENTITY_FIELD.search(descriptor):
                rows.append({'file': rel, 'tag': e.tag, 'type': kind,
                             'name': e.get('name') or '', 'id': e.get('id') or '',
                             'label': (e.get('aria-label') or e.get('placeholder') or '')[:60]})
    return {'pages': pages, 'inputsOnPupilSurfaces': pupil_fields, 'staffFields': staff_fields,
            'identityFields': len(rows), 'rows': rows}


# ---------------------------------------------------------------------------------------------
# NAMES GATE (ruling 2026-09-23, C4): the product-name limb alone, as a required CI gate over
# every PUBLIC path. Three differences from the census above, each ruled:
#   * scope is the served tree: Site's own public_file() decides (pass --site); without a Site
#     checkout the same rule is mirrored here and the output says so;
#   * embedded image data (data: URIs) is not text and is skipped -- two decks matched "EFL"
#     inside base64 before this;
#   * office files are read: the text parts of .xlsx/.docx/.pptx (26 served weekly plans carried
#     the name where the census could not see it).
# A name kept on purpose is listed in RETAINED with its exact count and reason; the gate is red
# if that count moves either way, so the allowance cannot widen silently.
OFFICE_SUFFIXES = {'.xlsx', '.docx', '.pptx'}
DATA_URI = re.compile(r'data:[\w.+-]+/[\w.+-]+(?:;[\w=.+-]+)*;base64,[A-Za-z0-9+/=\s]+')
RETAINED = {
    'biology/Testing Breath - FINAL Observation Lesson (1).html': [
        ('value="EFL clip"', 1, 'saved-setting value (localStorage ps_co2_final_observation_v1): internal '
                               'identifier, not displayed, retained on purpose (ruling 2026-09-23 C2)'),
        ("v==='EFL clip'", 1, 'comparison against that saved value: internal identifier, not displayed, '
                              'retained on purpose (ruling 2026-09-23 C2)'),
        # the per-pupil state property is saved in the same localStorage record, so renaming it
        # would drop a teacher's saved evidence ticks exactly as renaming the value would
        ('efl:false', 6, 'saved per-pupil state property: internal identifier, not displayed, retained on purpose (C2)'),
        ('p.efl', 5, 'reads/writes of that property: internal identifier, not displayed, retained on purpose (C2)'),
        ('].efl', 2, 'toggle of that property: internal identifier, not displayed, retained on purpose (C2)'),
    ],
}
_SKIP_TOP = {'tools', 'reports', 'docs', 'domain-split', 'node_modules', 'supabase', 'schema'}
_PUBLIC_SUFFIX = {'.html', '.htm', '.css', '.js', '.mjs', '.json', '.svg', '.txt', '.xml', '.webmanifest',
                  '.md', '.csv', '.xlsx', '.docx', '.pptx'}


def public_rule(site: Path | None):
    """Site's own public_file() when a Site checkout is given; else the mirrored rule."""
    if site and (site / 'domain-split/build_education.py').is_file():
        import importlib.util
        sys.path.insert(0, str(site / 'domain-split'))
        spec = importlib.util.spec_from_file_location('_mbm_build_education', site / 'domain-split/build_education.py')
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        return mod.public_file, "Site's public_file()"
    def mirrored(rel):
        parts = Path(rel).parts
        return (not any(x.startswith(('.', '_')) for x in parts) and parts[0] not in _SKIP_TOP
                and Path(rel).suffix.lower() in _PUBLIC_SUFFIX)
    return mirrored, 'the mirrored public-file rule (no Site checkout given)'


def public_text(p: Path) -> str:
    if p.suffix.lower() in OFFICE_SUFFIXES:
        import zipfile
        try:
            z = zipfile.ZipFile(p)
        except zipfile.BadZipFile:
            return ''
        parts = [n for n in z.namelist() if n.endswith('.xml') and not n.startswith('customXml')]
        return '\n'.join(re.sub(r'<[^>]+>', ' ', z.read(n).decode('utf-8', 'replace')) for n in parts)
    return DATA_URI.sub(' ', p.read_text(errors='ignore'))


def names_gate(root: Path, site: Path | None = None) -> dict:
    is_public, rule = public_rule(site)
    hits, retained_bad, scanned = [], [], 0
    for p in sorted(root.rglob('*')):
        if not p.is_file() or '.git' in p.parts:
            continue
        rel = p.relative_to(root).as_posix()
        if p.suffix.lower() not in TEXT_SUFFIXES | OFFICE_SUFFIXES or not is_public(rel):
            continue
        scanned += 1
        text = public_text(p)
        for lit, want, _why in RETAINED.get(rel, []):
            got = text.count(lit)
            if got != want:
                retained_bad.append({'file': rel, 'literal': lit, 'want': want, 'got': got})
            text = text.replace(lit, ' ')
        for m in PRODUCT_NAMES.finditer(text):
            hits.append({'file': rel, 'match': m.group(0),
                         'context': text[max(0, m.start() - 50):m.end() + 50].replace('\n', ' ')})
    return {'rule': rule, 'publicFilesScanned': scanned, 'hits': hits, 'retainedMismatch': retained_bad}


def names_gate_self_test() -> int:
    import tempfile, zipfile
    checks = []
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        (root / 'clean.html').write_text('<p>Capture it on the school’s digital evidence platform.</p>')
        checks.append(('GREEN: a clean public page passes', not names_gate(root)['hits']))
        (root / 'img.html').write_text('<img src="data:image/png;base64,iVBORw0KGgoEFlAAAA">')
        checks.append(('GREEN: embedded image data is not text', not names_gate(root)['hits']))
        (root / '_staff').mkdir(); (root / '_staff/card.md').write_text('E: evidence captured on Cypher')
        checks.append(('GREEN: a staff path (never served) is out of scope', not names_gate(root)['hits']))
        for name in ('Earwig', 'Cypher', 'Evidence for Learning', 'EFL'):
            (root / 'planted.html').write_text('<p>Upload it to %s afterwards.</p>' % name)
            checks.append(('RED: a planted %r on a public page is caught' % name, len(names_gate(root)['hits']) == 1))
        (root / 'planted.html').unlink()
        with zipfile.ZipFile(root / 'plan.xlsx', 'w') as z:
            z.writestr('xl/sharedStrings.xml', '<sst><si><t>video to EFL, same day</t></si></sst>')
        checks.append(('RED: the name inside a public .xlsx is caught', len(names_gate(root)['hits']) == 1))
        (root / 'plan.xlsx').unlink()
        rel = 'biology/Testing Breath - FINAL Observation Lesson (1).html'
        (root / 'biology').mkdir()
        keep = '<script>v===\'EFL clip\';' + 'efl:false,' * 6 + 'p.efl;' * 5 + 'a[0].efl;' * 2 + '</script>'
        (root / rel).write_text('<option value="EFL clip">evidence clip</option>' + keep)
        r = names_gate(root)
        checks.append(('GREEN: the retained biology key, at its exact count, passes', not r['hits'] and not r['retainedMismatch']))
        (root / rel).write_text('<option value="EFL clip">EFL clip</option>' + keep)
        checks.append(('RED: the same name made visible again beside the retained key is caught', len(names_gate(root)['hits']) == 1))
        (root / rel).write_text('<option value="EFL clip">x</option>')
        checks.append(('RED: a retained literal whose count moves is caught', bool(names_gate(root)['retainedMismatch'])))
    for name, ok in checks:
        print(('PASS ' if ok else 'FAIL ') + name)
    return 0 if all(ok for _, ok in checks) else 1


def report(root: Path) -> dict:
    files, hits = scan_text(root)
    fields = scan_fields(root)
    return {'schema': 1, 'root': str(root), 'filesScanned': files, 'textHits': hits, 'fields': fields,
            'notCounted': ['the bare word PASS', 'the phrase "reading age"', 'fields inside staff-gated regions'],
            'verdict': {'productName': len(hits['productName']),
                        'markingPolicyWording': sum(1 for h in hits['reconstructedFeedback'] if h.get('markingSense')),
                        'assessmentName': len(hits['assessmentName'])},
            'forRuling': {'identityFields': fields.get('identityFields', 0),
                          'reconstructedFeedbackCandidates': sum(1 for h in hits['reconstructedFeedback'] if not h.get('markingSense')),
                          'inputsOnPupilSurfaces': fields.get('inputsOnPupilSurfaces', 0)}}


def self_test() -> int:
    import tempfile
    checks = []
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        (root / 'clean.html').write_text('<html><body><p>A lesson with no product name.</p></body></html>')
        r = report(root)
        checks.append(('a clean surface reports nothing', sum(r['verdict'].values()) == 0))

        (root / 'named.html').write_text('<html><body><p>Upload it to Earwig afterwards.</p></body></html>')
        r = report(root)
        checks.append(('CONTROL: a product name is found', r['verdict']['productName'] == 1))
        (root / 'named_cypher.html').write_text('<html><body><p>Record it on Cypher at Exit.</p></body></html>')
        checks.append(('CONTROL: Cypher is found', report(root)['verdict']['productName'] == 2))
        (root / 'named_full.html').write_text('<html><body><p>Captured in Evidence for\nLearning today.</p></body></html>')
        checks.append(('CONTROL: "Evidence for Learning" (even across a line break) is found', report(root)['verdict']['productName'] == 3))

        (root / 'feedback.html').write_text('<html><body><p>Use the Yellow Box and a green pen.</p></body></html>')
        r = report(root)
        checks.append(('CONTROL: the reconstructed marking policy is found', r['verdict']['markingPolicyWording'] >= 1))
        (root / 'uiyellow.html').write_text('<html><body><p>Click each yellow box to type your answer.</p></body></html>')
        checks.append(('CONTROL: a yellow box that is a user-interface instruction is NOT called a breach',
                       report(root)['verdict']['markingPolicyWording'] == report(root)['verdict']['markingPolicyWording']
                       and not any(h.get('markingSense') for h in report(root)['textHits']['reconstructedFeedback']
                                   if h['file'] == 'uiyellow.html')))

        (root / 'scores.html').write_text('<html><body><p>Her BKSB and NGRT scores.</p></body></html>')
        r = report(root)
        checks.append(('CONTROL: a named assessment is found', r['verdict']['assessmentName'] == 2))

        (root / 'field.html').write_text('<html><body><input name="pupil-name"><input name="brush-colour" type="color"><div data-mbm-guide="staff"><input name="staff-note"></div></body></html>')
        r = report(root)
        checks.append(('CONTROL: an identifying field is reported', r['fields']['identityFields'] == 1))
        checks.append(('CONTROL: a staff-gated field is set aside', r['fields']['staffFields'] == 1))
        checks.append(('CONTROL: an ordinary studio input is NOT reported as identifying',
                       r['fields']['identityFields'] == 1 and r['fields']['inputsOnPupilSurfaces'] >= 2))
        before = report(root)['verdict']['assessmentName']
        (root / 'pass.html').write_text('<html><body><p>[PASS] every gate passed, PASS</p></body></html>')
        checks.append(('CONTROL: the bare word PASS is deliberately not counted',
                       report(root)['verdict']['assessmentName'] == before))
    for name, ok in checks:
        print(('GREEN ' if ok else 'RED   ') + name)
    return 0 if all(ok for _, ok in checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--built', type=Path, help='a built publication tree (the served bytes)')
    ap.add_argument('--root', type=Path, help='a checkout (source scan)')
    ap.add_argument('--json', type=Path)
    ap.add_argument('--self-test', action='store_true')
    ap.add_argument('--names-gate', type=Path, metavar='ROOT', help='CI gate: product names on public paths only')
    ap.add_argument('--site', type=Path, help='a Site checkout, whose public_file() decides what is public')
    ap.add_argument('--names-gate-self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.names_gate_self_test:
        return names_gate_self_test()
    if a.names_gate:
        g = names_gate(a.names_gate, a.site)
        if a.json:
            a.json.write_text(json.dumps(g, indent=2) + '\n')
        print(f"NAMES GATE over {g['publicFilesScanned']} public files ({g['rule']}): "
              f"{len(g['hits'])} product name(s), {len(g['retainedMismatch'])} retained-count mismatch(es)")
        for h in g['hits'][:20]:
            print(f"   {h['file']}: {h['match']!r} … {h['context'][:90]}")
        for h in g['retainedMismatch']:
            print(f"   retained {h['file']}: {h['literal']!r} want {h['want']} got {h['got']}")
        return 1 if g['hits'] or g['retainedMismatch'] else 0
    root = a.built or a.root
    if root is None:
        print('give --built or --root'); return 2
    r = report(root)
    if a.json:
        a.json.write_text(json.dumps(r, indent=2) + '\n')
    v = r['verdict']
    print(f"{r['filesScanned']} public files scanned; "
          f"{r['fields'].get('pages', 0)} HTML pages for the field limb")
    for limb, n in v.items():
        print(('RED  ' if n else 'GREEN') + f' {limb}: {n}')
    for limb, n in r['forRuling'].items():
        print(f'     for ruling  {limb}: {n}')
    for h in r['textHits']['productName'][:12]:
        print(f"   productName {h['file']}:{h['line']} {h['match']!r} … {h['context'][:88]}")
    for h in [x for x in r['textHits']['reconstructedFeedback'] if x.get('markingSense')][:8]:
        print(f"   markingPolicy {h['file']}:{h['line']} {h['match']!r} … {h['context'][:88]}")
    for h in r['textHits']['assessmentName'][:8]:
        print(f"   assessment {h['file']}:{h['line']} {h['match']!r} … {h['context'][:88]}")
    for row in r['fields'].get('rows', [])[:10]:
        print(f"   identityField {row['file']} <{row['tag']} type={row['type']} name={row['name']!r} label={row['label']!r}>")
    print('not counted, by design: ' + '; '.join(r['notCounted']))
    return 1 if any(v.values()) else 0


if __name__ == '__main__':
    raise SystemExit(main())
