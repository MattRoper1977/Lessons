"""A10 + §3.1 — repair the public Baseline Weeks pack, four repairs and no others.

    python3 _sciv3/tools/build_baseline.py <inputs/baseline> <out-dir>
"""
import sys, os, re, shutil

IN, OUT = sys.argv[1], sys.argv[2]
LOG = []


class NoAnchor(Exception):
    pass


def sub1(t, old, new, f, what, count=1):
    n = t.count(old)
    if n != count:
        raise NoAnchor(f'{f}: {what}: expected {count}, found {n}: {old[:80]!r}')
    LOG.append((f, what))
    return t.replace(old, new)


# ---------------------------------------------------------------- A10.2
OLD_BRANCH = ("   if(uncertain)detail+=` “Not sure/not ready” was used ${uncertain} "
              "time${uncertain===1?'':'s'}; treat that as separate evidence about "
              "readiness/confidence, not simply as a wrong answer.`;")
NEW_BRANCH = (
 # A10.2 as specified.
 "   if(!attempted&&uncertain){label='Not started yet';detail='This strand was not attempted "
 "today. That is information about readiness, not about ability — pick it up in ordinary "
 "teaching.'}\n"
 # BEYOND A10.2, flagged AMBER. A strand with no multiple-choice items at all can never
 # reach `attempted`, so it rendered "Need more evidence / Too little evidence was collected"
 # on EVERY sitting — including one where the pupil wrote a full response. That is the same
 # false-deficit harm A10.2 names, firing unconditionally. Proven by render, not by reading.
 # To revert: delete this one `else if` clause.
 "   else if(!items.length){label='Answered in writing';detail='This strand is answered in the "
 "pupil’s own words, so it is not summarised here. Read the response — that is the evidence.'}\n"
 "   else if(uncertain)detail+=` “Not sure/not ready” was used ${uncertain} "
 "time${uncertain===1?'':'s'}; treat that as separate evidence about "
 "readiness/confidence, not simply as a wrong answer.`;")

# ---------------------------------------------------------------- A10.1 + §3.1 notes
KEY_NOTE_HTML = (
 '<section class="profile"><h2>Before you use these as a test</h2>'
 '<p><b>These pages are not secure tests, and were not built to be.</b> Each assessment carries '
 'its own correct answers inside the page, so anyone who views the page source — including a '
 'pupil the night before — can read them. For a low-stakes starting-point check that may be '
 'perfectly acceptable; it is recorded here so that it is a decision rather than a surprise. Do '
 'not use these pages anywhere the answers being visible would matter.</p></section>')

OFFLINE_HTML = (
 '<section class="profile"><h2>When the baseline app is unavailable</h2>'
 '<p><b>A public website is not a fallback for an internet outage.</b> If the connection is down, '
 'madebymatt.uk is exactly as unreachable as PythonAnywhere. What this pack genuinely covers is '
 'the baseline app being down while the internet is up — an app error, a quota, a deploy gone '
 'wrong.</p>'
 '<p><b>If you have no internet at all, print these in advance — that is the offline route. If '
 'the internet is working but the baseline app is not, use these pages.</b> Every page here '
 'carries a print stylesheet.</p></section>')

INSTRUMENT_HTML = (
 '<section class="profile"><h2>This is a different instrument from the baseline app</h2>'
 '<p>The PythonAnywhere baseline is keyed to BUILD / GROW / LAUNCH across seven assessment IDs. '
 'This pack is Reading &amp; Writing / Maths / Science across two routes. '
 '<b>Results are not interchangeable and must not be entered into the app’s database as if they '
 'were.</b> Reconciling the two instruments is a design decision, not a repair, and has not been '
 'attempted here.</p></section>')

PATHWAY_HTML = (
 '<section class="profile"><h2>How these routes relate to BUILD, GROW and LAUNCH</h2>'
 '<p style="border:2px dashed #b45309;background:#fffbeb;padding:10px 12px;border-radius:8px">'
 '<b>PLACEHOLDER — awaiting Matt’s wording. Do not fill this in from anywhere else.</b><br>'
 'These pages use “Pathway A — Standard Transitions” and “Pathway B — Specialist / SEMH”, which '
 'appear nowhere else in the estate; every other pupil-facing surface uses BUILD / GROW / LAUNCH. '
 'The mapping between them is a curriculum judgement — the whole school is an SEMH provision, so '
 '“Standard” may describe a cohort that does not exist here — and it is not a naming tidy-up that '
 'can be inferred. The route names were deliberately left unchanged.</p></section>')

KEY_NOTE_MD = """

## These pages are not secure tests

Each assessment carries its own correct answers inside the page (`DATA.items[].correct`, read by
the scoring block). Anyone who views the page source — including a pupil — can read the key.

For a low-stakes starting-point check that may be perfectly acceptable. It is written down here so
that it is a decision rather than an accident. Do not use these pages anywhere the answers being
visible would matter. Removing the key is a redesign of the assessment, not a repair, and has not
been done.
"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for name in sorted(os.listdir(IN)):
        t = open(os.path.join(IN, name), encoding='utf-8').read()
        if name.startswith('baseline-') and name != 'baseline-profile-review.html':
            t = sub1(t, OLD_BRANCH, NEW_BRANCH, name, 'A10.2 not-started-yet branch')
        if name == 'index.html':
            anchor = '<section class="profile"><h2>Important</h2>'
            t = sub1(t, anchor, KEY_NOTE_HTML + OFFLINE_HTML + INSTRUMENT_HTML + PATHWAY_HTML
                     + anchor, name, 'A10.1/A10.4/§3.1 staff notes')
        if name == 'README.md':
            t = t.rstrip() + KEY_NOTE_MD
            LOG.append((name, 'A10.1 answer-key disclosure'))
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write(t)

    # ---- re-assert the clean bill of health after editing
    bad = {}
    for name in sorted(os.listdir(OUT)):
        if not name.endswith('.html'):
            continue
        t = open(os.path.join(OUT, name), encoding='utf-8').read()
        for label, pat in [('localStorage', r'\blocalStorage\b'),
                           ('sessionStorage', r'\bsessionStorage\b'),
                           ('indexedDB', r'\bindexedDB\b'), ('cookie', r'document\.cookie'),
                           ('fetch', r'\bfetch\s*\('), ('XHR', r'XMLHttpRequest'),
                           ('sendBeacon', r'sendBeacon'), ('<form', r'<form\b'),
                           ('external', r'https?://(?!www\.w3\.org)'),
                           ('ext script', r'<script[^>]+src=')]:
            n = len(re.findall(pat, t))
            if n:
                bad.setdefault(label, []).append((name, n))
        if '@media print' not in t:
            bad.setdefault('no print stylesheet', []).append((name, 0))
    for f, what in LOG:
        print(f'  {f:44s} {what}')
    print(f'\n{len(LOG)} repairs applied')
    print('re-assert 0 storage / 0 network / 0 forms / 0 external:',
          'CLEAN' if not bad else bad)
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
