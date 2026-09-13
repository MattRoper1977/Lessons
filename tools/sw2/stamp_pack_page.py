#!/usr/bin/env python3
"""Stamp K's new page from the already approved Site chrome, at an exact pin.

No existing page or historical carrier is changed. The committed output is
checked with --check; the external Site dependency is explicit, like T's chrome.
"""
import argparse
import subprocess
import sys
from pathlib import Path

SITE_PIN = '9829c4f2db37b7235d1918dbbb58c5a2e277d8af'
ROOT = Path(__file__).resolve().parents[2]


def render(site):
    assert subprocess.check_output(['git','-C',str(site),'rev-parse','HEAD'],text=True).strip() == SITE_PIN
    sys.path.insert(0,str(site / 'domain-split'))
    from shared_navigation import header, audience_rows, chrome_template
    head = header('/Lessons/pack.html', audience_rows(site), adult=True, theme=True)
    footer = chrome_template('footer.html','published-signoff',{}) + chrome_template('footer.html','published-links',{'contact_label':'Contact'})
    return '''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lesson packs — Made by Matt</title>
<meta name="description" content="Editable slides, pupil resources and teacher guides, grouped with their teaching lesson.">
<meta name="theme-color" content="#161d3d">
<link rel="icon" href="/favicon.svg">
<!-- mbm-chrome:tokens --><link rel="stylesheet" href="/assets/mbm-tokens.css"><!-- /mbm-chrome:tokens -->
<link rel="stylesheet" href="/assets/education-palette.css">
<link rel="stylesheet" href="/assets/shared-navigation.css">
<link rel="stylesheet" href="/assets/shared-footer.css">
<link rel="stylesheet" href="assets/catalogue/pack.css">
<script>try{var t=localStorage.getItem('mbm_reading_theme');if(t&&t!=='cream')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>
<script defer src="assets/mbm-theme.js"></script>
<script defer src="/assets/shared-navigation.js"></script>
<script defer src="assets/catalogue/hub.js"></script>
<script defer src="assets/catalogue/pack.js"></script>
</head><body class="mbm-pack" data-mbm-palette="education" data-mbm-estate="lessons">
<a class="skip" href="#main">Skip to content</a>
<!-- mbm-chrome:header -->''' + head + '''<!-- /mbm-chrome:header -->
<main id="main" class="pk-main"><div id="pack-content"><h1>Lesson packs</h1><p>Loading the pack catalogue…</p></div>
<noscript><p>Choose your subject to find lesson packs and downloads.</p><a class="pk-action" href="/Lessons/">Choose a subject →</a> <a class="pk-action" href="/resources/">Resources →</a></noscript></main>
<!-- mbm-chrome:footer --><footer class="pk-footer">''' + footer + '''</footer><!-- /mbm-chrome:footer -->
</body></html>
'''


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--site',type=Path,required=True);p.add_argument('--check',action='store_true');a=p.parse_args()
    text=render(a.site.resolve());target=ROOT/'pack.html'
    if a.check: assert target.read_text()==text, 'Pack shell differs from its approved template pin'
    else: target.write_text(text)
    print('Pack chrome PASS: '+SITE_PIN)
